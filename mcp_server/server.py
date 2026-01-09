"""
STM32 Documentation MCP Server

Provides semantic search over STM32 documentation via MCP protocol.
Supports both local (stdio) and network (HTTP/SSE) modes for Tailscale.

This is the main entry point for the MCP server. It registers all tools,
resources, and prompts that are exposed to MCP clients.

Usage:
    # Local mode (stdio for Claude Code)
    python -m mcp_server.server

    # Network mode (HTTP/SSE for Tailscale)
    STM32_SERVER_MODE=network python -m mcp_server.server

Environment Variables:
    STM32_SERVER_MODE: local, network, or hybrid
    STM32_HOST: Host to bind (default: 0.0.0.0)
    STM32_PORT: Port for network mode (default: 8765)
"""

from pathlib import Path
import sys
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral, DocType
from mcp_server.config import settings, ServerMode
from mcp_server.resources.handlers import DocumentationResources

# Import advanced search tools
from mcp_server.tools.search import (
    search_hal_function as _search_hal_function_impl,
    search_error_solution,
    search_initialization_sequence,
    search_clock_configuration,
    compare_peripherals,
    search_migration_info,
    search_electrical_specs,
    search_timing_info,
)
from mcp_server.tools.examples import (
    get_interrupt_example,
    get_dma_example,
    get_low_power_example,
    get_callback_example,
    get_peripheral_init_template,
)

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL.value,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger("stm32-docs")

# Initialize FastMCP server
# Note: FastMCP doesn't support version/description directly in constructor
# The server name is used for identification in the MCP protocol
mcp = FastMCP(
    name=settings.SERVER_NAME,
    instructions=settings.SERVER_DESCRIPTION
)

# Lazy-loaded storage instance
_store: STM32ChromaStore | None = None

# Lazy-loaded resources handler
_resources: DocumentationResources | None = None


def get_store() -> STM32ChromaStore:
    """
    Get or initialize the ChromaDB store.

    Uses lazy loading to avoid initialization overhead until first use.
    The store is cached globally for reuse across requests.

    Returns:
        STM32ChromaStore instance
    """
    global _store
    if _store is None:
        logger.info(f"Initializing ChromaDB store at {settings.CHROMA_DB_PATH}")
        _store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        logger.info(f"Store initialized with {_store.count()} chunks")
    return _store


def get_resources() -> DocumentationResources:
    """
    Get or initialize the resources handler.

    Uses lazy loading to avoid initialization overhead until first use.
    The resources handler is cached globally for reuse across requests.

    Returns:
        DocumentationResources instance
    """
    global _resources
    if _resources is None:
        _resources = DocumentationResources(get_store())
    return _resources


# ============================================================================
# TOOLS - Core search functionality exposed to MCP clients
# ============================================================================

@mcp.tool()
def search_stm32_docs(
    query: str,
    num_results: int = 5,
    peripheral: str = "",
    require_code: bool = False
) -> str:
    """
    Search STM32 documentation using semantic search.

    This is the primary search tool for finding relevant documentation.
    It uses vector embeddings to find semantically similar content.

    Args:
        query: Natural language query about STM32 development
        num_results: Number of results to return (1-20, default: 5)
        peripheral: Filter by peripheral (GPIO, UART, SPI, I2C, ADC, TIM, DMA, etc.)
        require_code: Only return results with code examples

    Returns:
        Relevant documentation snippets with sources and metadata

    Examples:
        - search_stm32_docs("How to configure UART for 115200 baud")
        - search_stm32_docs("DMA configuration", peripheral="DMA")
        - search_stm32_docs("GPIO toggle example", require_code=True)
    """
    store = get_store()

    # Parse peripheral filter
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            # Invalid peripheral name, log and continue without filter
            logger.warning(f"Unknown peripheral filter: {peripheral}")

    # Clamp results to valid range
    num_results = max(1, min(num_results, settings.MAX_SEARCH_RESULTS))

    # Execute search
    results = store.search(
        query=query,
        n_results=num_results,
        peripheral=periph_filter,
        require_code=require_code,
        min_score=settings.MIN_RELEVANCE_SCORE
    )

    if not results:
        return f"No documentation found for query: {query}"

    # Format output for readability
    output = []
    for i, r in enumerate(results, 1):
        meta = r['metadata']
        output.append(f"## Result {i} (relevance: {r['score']:.2f})")
        output.append(f"**Source**: {meta.get('source_file', 'Unknown')}")

        if meta.get('peripheral'):
            output.append(f"**Peripheral**: {meta['peripheral']}")
        if meta.get('section_path'):
            output.append(f"**Section**: {meta['section_path']}")
        if meta.get('has_code'):
            output.append("**Contains code examples**")

        output.append("")
        output.append(r['content'])
        output.append("")
        output.append("---")
        output.append("")

    logger.info(f"Search '{query[:50]}...' returned {len(results)} results")
    return "\n".join(output)


@mcp.tool()
def get_peripheral_docs(
    peripheral: str,
    topic: str = "",
    include_code: bool = True
) -> str:
    """
    Get documentation for a specific STM32 peripheral.

    Use this tool when you need comprehensive documentation about
    a particular peripheral. Results are filtered to that peripheral only.

    Args:
        peripheral: The peripheral name (GPIO, UART, SPI, I2C, ADC, TIM, DMA, RCC, NVIC, etc.)
        topic: Optional specific topic within the peripheral (e.g., "interrupt", "configuration")
        include_code: Include code examples in results (default: True)

    Returns:
        Comprehensive documentation for the peripheral

    Examples:
        - get_peripheral_docs("UART")
        - get_peripheral_docs("GPIO", topic="interrupt")
        - get_peripheral_docs("DMA", topic="circular mode")
    """
    store = get_store()

    # Validate peripheral
    try:
        periph = Peripheral(peripheral.upper())
    except ValueError:
        valid = ", ".join(p.value for p in Peripheral if p != Peripheral.GENERAL)
        return f"Unknown peripheral: {peripheral}. Valid options: {valid}"

    # Build search query
    query = f"{peripheral} {topic}".strip() if topic else f"{peripheral} overview configuration"

    # Search with peripheral filter
    results = store.search_by_peripheral(periph, query, n_results=10)

    if not results:
        return f"No documentation found for peripheral: {peripheral}"

    # Format output
    output = [f"# {peripheral} Documentation\n"]

    for r in results:
        meta = r['metadata']
        section = meta.get('section_title', 'General')

        output.append(f"## {section}")
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    logger.info(f"Retrieved {len(results)} docs for peripheral {peripheral}")
    return "\n".join(output)


@mcp.tool()
def get_code_examples(
    topic: str,
    peripheral: str = "",
    num_examples: int = 3
) -> str:
    """
    Get code examples for an STM32 topic.

    Use this tool to find working code examples for initialization,
    configuration, or common operations.

    Args:
        topic: The topic to find code examples for (e.g., "UART DMA receive", "GPIO toggle")
        peripheral: Optional peripheral filter
        num_examples: Number of examples to return (1-10, default: 3)

    Returns:
        Code examples with context and explanations

    Examples:
        - get_code_examples("UART transmit")
        - get_code_examples("PWM configuration", peripheral="TIM")
        - get_code_examples("ADC continuous mode")
    """
    store = get_store()

    # Parse optional peripheral filter
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            logger.warning(f"Unknown peripheral filter: {peripheral}")

    # Clamp number of examples
    num_examples = max(1, min(num_examples, 10))

    # Search for code examples
    results = store.get_code_examples(
        topic=topic,
        peripheral=periph_filter,
        n_results=num_examples
    )

    if not results:
        return f"No code examples found for: {topic}"

    # Format output
    output = [f"# Code Examples: {topic}\n"]

    for i, r in enumerate(results, 1):
        meta = r['metadata']
        output.append(f"## Example {i}")
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*")
        if meta.get('peripheral'):
            output.append(f"*Peripheral: {meta['peripheral']}*")
        output.append("")
        output.append(r['content'])
        output.append("\n---\n")

    logger.info(f"Found {len(results)} code examples for '{topic}'")
    return "\n".join(output)


@mcp.tool()
def get_register_info(register_name: str) -> str:
    """
    Get information about a specific STM32 register.

    Use this tool when you need detailed register documentation
    including bit fields, reset values, and configuration options.

    Args:
        register_name: The register name (e.g., "GPIOx_MODER", "USART_CR1", "RCC_AHB1ENR")

    Returns:
        Register documentation including bit fields and configuration options

    Examples:
        - get_register_info("GPIOx_MODER")
        - get_register_info("TIMx_CR1")
        - get_register_info("RCC_CFGR")
    """
    store = get_store()

    # Search for register documentation
    results = store.get_register_info(register_name, n_results=5)

    if not results:
        return f"No register information found for: {register_name}"

    # Format output
    output = [f"# Register: {register_name}\n"]

    for r in results:
        meta = r['metadata']
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    logger.info(f"Retrieved register info for {register_name}")
    return "\n".join(output)


@mcp.tool()
def list_peripherals() -> str:
    """
    List all available peripherals and their documentation coverage.

    Use this tool to discover what peripherals are documented
    and how much content is available for each.

    Returns:
        List of peripherals with chunk counts
    """
    store = get_store()

    # Get peripheral distribution
    dist = store.get_peripheral_distribution()

    output = ["# Available STM32 Peripherals\n"]
    output.append("The following peripherals have documentation available:\n")

    # Sort by count descending
    for periph, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
        if periph and periph != "GENERAL" and periph != "":
            output.append(f"- **{periph}**: {count} documentation chunks")

    # Add general count if present
    general_count = dist.get("GENERAL", 0) + dist.get("", 0)
    if general_count:
        output.append(f"\n*Plus {general_count} general documentation chunks*")

    # Get total stats
    stats = store.get_stats()
    output.append(f"\n**Total documentation chunks**: {stats.get('total_chunks', 0)}")

    return "\n".join(output)


@mcp.tool()
def search_hal_function(function_name: str) -> str:
    """
    Search for HAL/LL function documentation.

    Use this tool when you need to understand how to use a specific
    HAL or LL library function.

    Args:
        function_name: HAL/LL function name (e.g., "HAL_GPIO_Init", "LL_USART_Enable")

    Returns:
        Function documentation with parameters, return values, and usage examples

    Examples:
        - search_hal_function("HAL_GPIO_Init")
        - search_hal_function("HAL_UART_Transmit_DMA")
        - search_hal_function("LL_TIM_SetCounter")
    """
    store = get_store()

    # Search for the function
    results = store.search_hal_function(function_name, n_results=5)

    if not results:
        # Fallback to general search if HAL guide search fails
        results = store.search(
            query=function_name,
            n_results=5,
            require_code=True
        )

    if not results:
        return f"No documentation found for function: {function_name}"

    # Format output
    output = [f"# HAL Function: {function_name}\n"]

    for r in results:
        meta = r['metadata']
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    logger.info(f"Retrieved HAL function docs for {function_name}")
    return "\n".join(output)


# ============================================================================
# ADVANCED SEARCH TOOLS - Specialized search functionality
# ============================================================================

@mcp.tool()
def lookup_hal_function(function_name: str) -> str:
    """
    Look up documentation for a specific HAL/LL function.

    This is an enhanced version that handles various HAL/LL function patterns
    and extracts peripheral context automatically.

    Args:
        function_name: The HAL/LL function name (e.g., HAL_UART_Transmit, LL_GPIO_SetPinMode)

    Returns:
        Function documentation, parameters, and usage examples

    Examples:
        - lookup_hal_function("HAL_UART_Transmit")
        - lookup_hal_function("HAL_SPI_TransmitReceive_DMA")
        - lookup_hal_function("LL_GPIO_SetPinMode")
        - lookup_hal_function("__HAL_RCC_GPIOA_CLK_ENABLE")
    """
    return _search_hal_function_impl(get_store(), function_name)


@mcp.tool()
def troubleshoot_error(
    error_description: str,
    peripheral: str = ""
) -> str:
    """
    Search for solutions to STM32 errors and issues.

    This tool searches documentation for troubleshooting information,
    including errata, common issues, and solutions.

    Args:
        error_description: Description of the error or symptom
        peripheral: Optional peripheral to focus the search

    Returns:
        Troubleshooting steps and solutions

    Examples:
        - troubleshoot_error("UART not receiving data")
        - troubleshoot_error("HAL_TIMEOUT error", peripheral="I2C")
        - troubleshoot_error("HardFault after DMA transfer")
        - troubleshoot_error("SPI communication fails intermittently")
    """
    return search_error_solution(get_store(), error_description, peripheral or None)


@mcp.tool()
def get_init_sequence(
    peripheral: str,
    use_case: str = ""
) -> str:
    """
    Get complete initialization sequence for a peripheral.

    This tool finds comprehensive initialization examples including
    clock enable, GPIO configuration, and peripheral setup.

    Args:
        peripheral: The peripheral to initialize (GPIO, UART, SPI, I2C, ADC, TIM, etc.)
        use_case: Specific use case (e.g., "DMA mode", "interrupt driven", "continuous")

    Returns:
        Complete initialization code with explanations

    Examples:
        - get_init_sequence("UART")
        - get_init_sequence("SPI", use_case="DMA master mode")
        - get_init_sequence("ADC", use_case="continuous conversion")
        - get_init_sequence("TIM", use_case="PWM output")
    """
    return search_initialization_sequence(get_store(), peripheral, use_case)


@mcp.tool()
def get_clock_config(
    target_frequency: str = "",
    clock_source: str = ""
) -> str:
    """
    Get clock configuration documentation.

    This tool searches for clock tree configuration examples
    including PLL setup and clock source selection.

    Args:
        target_frequency: Target system clock frequency (e.g., "168MHz", "480MHz")
        clock_source: Clock source (HSE, HSI, PLL, LSE, LSI)

    Returns:
        Clock configuration code and explanations

    Examples:
        - get_clock_config("168MHz", "HSE")
        - get_clock_config("480MHz")
        - get_clock_config(clock_source="PLL")
        - get_clock_config("84MHz", "HSI")
    """
    return search_clock_configuration(get_store(), target_frequency, clock_source)


@mcp.tool()
def compare_peripheral_options(
    peripheral1: str,
    peripheral2: str,
    aspect: str = ""
) -> str:
    """
    Get documentation comparing two peripherals or modes.

    This tool helps understand differences between similar peripherals
    or different operating modes.

    Args:
        peripheral1: First peripheral to compare
        peripheral2: Second peripheral to compare
        aspect: Specific aspect to compare (e.g., "speed", "power", "features")

    Returns:
        Comparison documentation

    Examples:
        - compare_peripheral_options("UART", "USART")
        - compare_peripheral_options("SPI", "I2C", aspect="speed")
        - compare_peripheral_options("DMA", "BDMA")
        - compare_peripheral_options("ADC", "DAC", aspect="resolution")
    """
    return compare_peripherals(get_store(), peripheral1, peripheral2, aspect)


@mcp.tool()
def get_migration_guide(
    from_family: str,
    to_family: str,
    peripheral: str = ""
) -> str:
    """
    Get migration information between STM32 families.

    This tool searches for migration guides, differences, and
    code changes needed when porting between STM32 families.

    Args:
        from_family: Source STM32 family (e.g., "STM32F4", "STM32F7")
        to_family: Target STM32 family (e.g., "STM32H7", "STM32G4")
        peripheral: Optional specific peripheral to focus on

    Returns:
        Migration considerations, differences, and code changes

    Examples:
        - get_migration_guide("STM32F4", "STM32H7")
        - get_migration_guide("STM32F7", "STM32H7", peripheral="DMA")
        - get_migration_guide("STM32F1", "STM32G4", peripheral="ADC")
    """
    return search_migration_info(get_store(), from_family, to_family, peripheral or None)


@mcp.tool()
def get_electrical_specifications(topic: str) -> str:
    """
    Search for electrical specifications.

    This tool searches datasheets and reference manuals for
    electrical characteristics and specifications.

    Args:
        topic: The electrical specification topic

    Returns:
        Electrical specification documentation

    Examples:
        - get_electrical_specifications("GPIO drive strength")
        - get_electrical_specifications("ADC input impedance")
        - get_electrical_specifications("power consumption sleep mode")
        - get_electrical_specifications("operating voltage range")
    """
    return search_electrical_specs(get_store(), topic)


@mcp.tool()
def get_timing_specifications(
    peripheral: str,
    timing_type: str = ""
) -> str:
    """
    Search for timing specifications and diagrams.

    This tool searches for timing requirements, clock frequencies,
    and timing diagrams for peripherals.

    Args:
        peripheral: The peripheral to search timing info for
        timing_type: Specific timing type (e.g., "setup hold", "clock frequency", "latency")

    Returns:
        Timing specification documentation

    Examples:
        - get_timing_specifications("SPI", "clock frequency")
        - get_timing_specifications("I2C", "setup hold")
        - get_timing_specifications("UART", "baud rate")
        - get_timing_specifications("SDMMC", "latency")
    """
    return search_timing_info(get_store(), peripheral, timing_type)


# ============================================================================
# CODE EXAMPLE TOOLS - Specialized example retrieval
# ============================================================================

@mcp.tool()
def get_interrupt_code(
    peripheral: str,
    interrupt_type: str = ""
) -> str:
    """
    Get interrupt handling examples for a peripheral.

    This tool searches for interrupt configuration and callback
    implementation examples.

    Args:
        peripheral: The peripheral to get interrupt examples for
        interrupt_type: Specific interrupt type (e.g., "RXNE", "TC", "update", "error")

    Returns:
        Interrupt handling code examples with context

    Examples:
        - get_interrupt_code("UART")
        - get_interrupt_code("TIM", interrupt_type="update")
        - get_interrupt_code("EXTI", interrupt_type="rising edge")
        - get_interrupt_code("ADC", interrupt_type="conversion complete")
    """
    return get_interrupt_example(get_store(), peripheral, interrupt_type)


@mcp.tool()
def get_dma_code(
    peripheral: str,
    direction: str = ""
) -> str:
    """
    Get DMA configuration examples for a peripheral.

    This tool searches for DMA setup and configuration examples
    including stream/channel configuration.

    Args:
        peripheral: The peripheral to get DMA examples for
        direction: Transfer direction (TX, RX, both, or empty for all)

    Returns:
        DMA configuration code examples with context

    Examples:
        - get_dma_code("UART")
        - get_dma_code("SPI", direction="TX")
        - get_dma_code("ADC", direction="RX")
        - get_dma_code("I2C", direction="both")
    """
    return get_dma_example(get_store(), peripheral, direction)


@mcp.tool()
def get_low_power_code(mode: str = "") -> str:
    """
    Get low power mode examples.

    This tool searches for low power mode configuration including
    entry, exit, and wakeup source configuration.

    Args:
        mode: Low power mode (Sleep, Stop, Standby, or empty for all)

    Returns:
        Low power configuration code examples

    Examples:
        - get_low_power_code()
        - get_low_power_code("Sleep")
        - get_low_power_code("Stop")
        - get_low_power_code("Standby")
    """
    return get_low_power_example(get_store(), mode)


@mcp.tool()
def get_callback_code(
    peripheral: str,
    callback_type: str = ""
) -> str:
    """
    Get HAL callback function examples.

    This tool searches for HAL callback implementations
    for specific peripherals.

    Args:
        peripheral: The peripheral to get callback examples for
        callback_type: Specific callback type (e.g., "TxCplt", "RxCplt", "Error")

    Returns:
        HAL callback implementation examples

    Examples:
        - get_callback_code("UART")
        - get_callback_code("SPI", callback_type="TxRxCplt")
        - get_callback_code("I2C", callback_type="Error")
        - get_callback_code("DMA", callback_type="HalfCplt")
    """
    return get_callback_example(get_store(), peripheral, callback_type)


@mcp.tool()
def get_init_template(
    peripheral: str,
    mode: str = ""
) -> str:
    """
    Get a complete peripheral initialization template.

    This tool searches for comprehensive initialization templates
    including all required configuration steps.

    Args:
        peripheral: The peripheral to get init template for
        mode: Specific mode or configuration (e.g., "master", "slave", "PWM")

    Returns:
        Complete initialization template with all required steps

    Examples:
        - get_init_template("SPI")
        - get_init_template("SPI", mode="master")
        - get_init_template("TIM", mode="PWM")
        - get_init_template("UART", mode="DMA")
    """
    return get_peripheral_init_template(get_store(), peripheral, mode)


# ============================================================================
# RESOURCES - Direct documentation access via URIs
# ============================================================================

@mcp.resource("stm32://stats")
def get_documentation_stats() -> str:
    """Get statistics about the documentation database."""
    return get_resources().get_stats()


@mcp.resource("stm32://peripherals")
def list_all_peripherals() -> str:
    """List all documented peripherals."""
    return list_peripherals()


@mcp.resource("stm32://peripherals/{peripheral}")
def get_peripheral_overview(peripheral: str) -> str:
    """Get overview documentation for a specific peripheral."""
    return get_resources().get_peripheral_overview(peripheral)


@mcp.resource("stm32://sources")
def list_doc_sources() -> str:
    """List all documentation source files."""
    return get_resources().list_sources()


@mcp.resource("stm32://health")
def get_health_status() -> str:
    """Get server health status."""
    import json
    store = get_store()

    return json.dumps({
        "status": "healthy",
        "server": settings.SERVER_NAME,
        "version": settings.SERVER_VERSION,
        "mode": settings.SERVER_MODE.value,
        "chunks_indexed": store.count(),
        "embedding_model": settings.EMBEDDING_MODEL
    }, indent=2)


@mcp.resource("stm32://peripherals/{peripheral}/overview")
def peripheral_overview(peripheral: str) -> str:
    """Get comprehensive peripheral overview documentation."""
    return get_resources().get_peripheral_overview(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/registers")
def peripheral_registers(peripheral: str) -> str:
    """Get peripheral register documentation."""
    return get_resources().get_peripheral_registers(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/examples")
def peripheral_examples(peripheral: str) -> str:
    """Get peripheral code examples."""
    return get_resources().get_peripheral_examples(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/interrupts")
def peripheral_interrupts(peripheral: str) -> str:
    """Get peripheral interrupt documentation."""
    return get_resources().get_peripheral_interrupts(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/dma")
def peripheral_dma(peripheral: str) -> str:
    """Get peripheral DMA configuration."""
    return get_resources().get_peripheral_dma(peripheral)


@mcp.resource("stm32://hal-functions")
def list_hal_functions() -> str:
    """List all HAL functions."""
    return get_resources().get_hal_functions_list()


@mcp.resource("stm32://hal-functions/{peripheral}")
def list_peripheral_hal_functions(peripheral: str) -> str:
    """List HAL functions for a specific peripheral."""
    return get_resources().get_hal_functions_list(peripheral)


@mcp.resource("stm32://documents/{doc_type}")
def get_documents_by_type(doc_type: str) -> str:
    """Get documents of a specific type."""
    return get_resources().get_document_by_type(doc_type)


# ============================================================================
# PROMPTS - Guided assistance templates
# ============================================================================

@mcp.prompt()
def debug_peripheral(peripheral: str, error: str) -> str:
    """Generate a debugging assistance prompt for peripheral issues."""
    return f"""You are debugging an STM32 {peripheral} issue.

Error/Symptom: {error}

Please search the documentation for:
1. Common {peripheral} configuration issues
2. Known errata or limitations
3. Troubleshooting steps

Use the search_stm32_docs tool with relevant queries to find documentation that helps diagnose this issue.

Start by searching for: "{peripheral} troubleshooting {error[:50]}"

Then check for:
- Clock configuration issues (search: "{peripheral} clock enable RCC")
- Interrupt configuration (search: "{peripheral} interrupt NVIC")
- Pin configuration if applicable
"""


@mcp.prompt()
def configure_peripheral(peripheral: str, requirements: str) -> str:
    """Generate a peripheral configuration assistance prompt."""
    return f"""You are helping configure the STM32 {peripheral} peripheral.

Requirements: {requirements}

Steps to follow:
1. Use get_peripheral_docs("{peripheral}") to understand {peripheral} capabilities
2. Use get_code_examples("{peripheral} initialization") to find similar configurations
3. Check for any specific requirements in the documentation
4. Provide complete initialization code with explanations

Search for relevant documentation before providing configuration code.

Key areas to document:
- Clock enable (RCC)
- GPIO configuration if needed
- {peripheral} initialization structure
- Interrupt configuration if required
- DMA setup if applicable
"""


@mcp.prompt()
def explain_hal_function(function_name: str) -> str:
    """Generate a HAL function explanation prompt."""
    return f"""Explain the STM32 HAL function: {function_name}

Use the documentation tools to find:
1. Function signature and parameters
2. Return values and error codes
3. Usage examples
4. Common pitfalls

Search for: search_hal_function("{function_name}")

After finding documentation, explain:
- What the function does
- When to use it
- Required prerequisites (clock, GPIO, etc.)
- Example usage with proper error handling
"""


@mcp.prompt()
def migration_guide(from_family: str, to_family: str, peripheral: str) -> str:
    """Generate a migration assistance prompt."""
    return f"""You are helping migrate STM32 code from {from_family} to {to_family}.

Peripheral focus: {peripheral}

Search for migration-relevant documentation:
1. search_stm32_docs("{to_family} {peripheral} differences")
2. search_stm32_docs("{peripheral} migration {from_family} {to_family}")
3. get_peripheral_docs("{peripheral}") for the target family

Key areas to check:
- Register differences
- Clock configuration changes
- HAL API changes
- Pin mapping differences
- Interrupt vector changes
"""


# ============================================================================
# SERVER STARTUP
# ============================================================================

def run_local():
    """Run server in local stdio mode for Claude Code integration."""
    logger.info("Starting STM32 MCP server in LOCAL mode (stdio)")
    logger.info(f"Database path: {settings.CHROMA_DB_PATH}")
    mcp.run()


def run_network():
    """Run server in network HTTP/SSE mode for Tailscale access."""
    import uvicorn
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse

    logger.info(f"Starting STM32 MCP server in NETWORK mode on {settings.HOST}:{settings.PORT}")
    logger.info(f"Database path: {settings.CHROMA_DB_PATH}")

    # Create SSE transport for MCP over HTTP
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        """Handle SSE connections for MCP protocol."""
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0], streams[1], mcp._mcp_server.create_initialization_options()
            )

    async def health_check(request):
        """Health check endpoint for monitoring."""
        store = get_store()
        return JSONResponse({
            "status": "healthy",
            "server": settings.SERVER_NAME,
            "version": settings.SERVER_VERSION,
            "chunks_indexed": store.count()
        })

    async def server_info(request):
        """Server information endpoint."""
        return JSONResponse({
            "name": settings.SERVER_NAME,
            "version": settings.SERVER_VERSION,
            "description": settings.SERVER_DESCRIPTION,
            "mode": settings.SERVER_MODE.value,
            "endpoints": {
                "sse": "/sse",
                "messages": "/messages",
                "health": "/health"
            }
        })

    # Create Starlette app with routes
    app = Starlette(
        routes=[
            Route("/", server_info),
            Route("/health", health_check),
            Route("/sse", handle_sse),
        ]
    )

    # Run with uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.value.lower()
    )


def main():
    """
    Main entry point - select mode based on configuration.

    Modes:
    - LOCAL: stdio transport for Claude Code
    - NETWORK: HTTP/SSE transport for Tailscale
    - HYBRID: defaults to local (use start_server.py for explicit control)
    """
    # Ensure required directories exist
    settings.ensure_directories()

    logger.info(f"STM32 MCP Server v{settings.SERVER_VERSION}")
    logger.info(f"Mode: {settings.SERVER_MODE.value}")

    if settings.SERVER_MODE == ServerMode.LOCAL:
        run_local()
    elif settings.SERVER_MODE == ServerMode.NETWORK:
        run_network()
    else:  # HYBRID - default to local
        # In hybrid mode, we default to local for simplicity
        # Network mode requires explicit configuration or use of start_server.py
        logger.info("Hybrid mode: defaulting to local (stdio) transport")
        run_local()


if __name__ == "__main__":
    main()
