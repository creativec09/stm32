"""
STM32 Documentation MCP Server

Provides semantic search over STM32 documentation via MCP protocol.
Supports both local (stdio) and network (HTTP/SSE) modes for Tailscale.

This is the main entry point for the MCP server. It registers all tools,
resources, and prompts that are exposed to MCP clients.

Features:
- Auto-ingestion on first run when database is empty
- Status and health resources for monitoring
- Context-aware tools with helpful error messages

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

from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
import sys
import logging
import json

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP, Context
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


# ============================================================================
# SERVER CONTEXT - Shared state via lifespan
# ============================================================================

@dataclass
class ServerContext:
    """
    Server context shared across all handlers via lifespan.

    This dataclass holds the initialized store and resources,
    making them available to all tools and resources through
    the request context.
    """
    store: STM32ChromaStore
    resources: DocumentationResources
    status: str  # "ready", "setup_required", "ingesting"
    chunk_count: int
    message: str


@asynccontextmanager
async def server_lifespan(server: FastMCP):
    """
    Server lifespan context manager.

    This is called when the server starts up. It:
    1. Initializes the ChromaDB store
    2. Checks if the database is empty
    3. If empty and markdown files exist, auto-runs ingestion
    4. Creates the ServerContext for sharing across requests
    """
    logger.info("=" * 60)
    logger.info(f"STM32 MCP Server v{settings.SERVER_VERSION} starting...")
    logger.info("=" * 60)

    # Ensure required directories exist
    settings.ensure_directories()

    # Initialize the ChromaDB store
    logger.info(f"Initializing ChromaDB store at {settings.CHROMA_DB_PATH}")
    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME,
        embedding_model=settings.EMBEDDING_MODEL
    )

    chunk_count = store.count()
    logger.info(f"Current database: {chunk_count} chunks")

    # Check if database is empty and needs ingestion
    if chunk_count == 0:
        # Check if markdown files exist
        from mcp_server.ingestion import find_markdown_files
        md_files = find_markdown_files(settings.RAW_DOCS_DIR)

        if md_files:
            logger.info("=" * 60)
            logger.info("Database empty, starting auto-ingestion...")
            logger.info(f"Found {len(md_files)} markdown files in {settings.RAW_DOCS_DIR}")
            logger.info("=" * 60)

            # Run ingestion
            from mcp_server.ingestion import run_ingestion

            def log_progress(message: str, current: int, total: int):
                if current % 10 == 0 or current == total:
                    logger.info(f"[{current}/{total}] {message}")

            result = run_ingestion(
                source_dir=settings.RAW_DOCS_DIR,
                store=store,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                min_chunk_size=settings.MIN_CHUNK_SIZE,
                clear_existing=False,
                progress_callback=log_progress
            )

            chunk_count = store.count()

            if result["success"]:
                logger.info("=" * 60)
                logger.info(f"Ingestion complete!")
                logger.info(f"  Files processed: {result['total_files']}")
                logger.info(f"  Chunks created: {result['total_chunks']}")
                if result.get('failed_files', 0) > 0:
                    logger.warning(f"  Failed files: {result['failed_files']}")
                logger.info("=" * 60)
                status = "ready"
                message = f"Ready - {chunk_count:,} chunks indexed from {result['total_files']} documents"
            else:
                logger.error(f"Ingestion failed: {result.get('error', 'Unknown error')}")
                status = "setup_required"
                message = f"Ingestion failed: {result.get('error', 'Unknown error')}"
        else:
            logger.warning("=" * 60)
            logger.warning("Database is empty and no markdown files found!")
            logger.warning(f"Expected markdown files in: {settings.RAW_DOCS_DIR}")
            logger.warning("Please add STM32 documentation files to this directory.")
            logger.warning("=" * 60)
            status = "setup_required"
            message = f"No documentation files found in {settings.RAW_DOCS_DIR}"
    else:
        logger.info(f"Ready - {chunk_count:,} chunks available")
        status = "ready"
        message = f"Ready - {chunk_count:,} chunks indexed"

    # Create resources handler
    resources_handler = DocumentationResources(store)

    # Create the server context
    context = ServerContext(
        store=store,
        resources=resources_handler,
        status=status,
        chunk_count=chunk_count,
        message=message
    )

    logger.info("=" * 60)
    logger.info(f"Server status: {status}")
    logger.info(f"Mode: {settings.SERVER_MODE.value}")
    logger.info("=" * 60)

    # Yield the context - this makes it available via ctx.request_context.lifespan_context
    yield context

    # Cleanup on shutdown
    logger.info("STM32 MCP Server shutting down...")


# Initialize FastMCP server with lifespan
mcp = FastMCP(
    name=settings.SERVER_NAME,
    instructions=settings.SERVER_DESCRIPTION,
    lifespan=server_lifespan
)


# ============================================================================
# HELPER FUNCTIONS - Get store from context
# ============================================================================

def get_store_from_context(ctx: Context) -> STM32ChromaStore:
    """Get the store from the request context."""
    server_ctx: ServerContext = ctx.request_context.lifespan_context
    return server_ctx.store


def get_context_status(ctx: Context) -> ServerContext:
    """Get the full server context."""
    return ctx.request_context.lifespan_context


def check_database_ready(ctx: Context) -> tuple[bool, str]:
    """
    Check if the database is ready for queries.

    Returns:
        Tuple of (is_ready, message)
    """
    server_ctx = get_context_status(ctx)
    if server_ctx.status != "ready":
        return False, (
            f"Database not ready: {server_ctx.message}\n\n"
            "To set up the database:\n"
            "1. Ensure the package was installed correctly with bundled documentation\n"
            "2. Restart the MCP server to trigger auto-ingestion\n"
            "3. Or run 'stm32-ingest' manually"
        )
    if server_ctx.chunk_count == 0:
        return False, (
            "Database is empty. No documentation has been indexed.\n\n"
            "To populate the database:\n"
            "1. Ensure the package was installed correctly with bundled documentation\n"
            "2. Restart the MCP server to trigger auto-ingestion\n"
            "3. Or run 'stm32-ingest' manually"
        )
    return True, ""


# ============================================================================
# STATUS AND HEALTH RESOURCES
# ============================================================================

@mcp.resource("stm32://status")
def get_server_status(ctx: Context) -> str:
    """
    Get detailed server status including database state.

    Returns JSON with:
    - status: "ready" or "setup_required"
    - chunk_count: Number of indexed chunks
    - message: Human-readable status message
    - instructions: Setup instructions if needed
    """
    server_ctx = get_context_status(ctx)

    status_data = {
        "status": server_ctx.status,
        "chunk_count": server_ctx.chunk_count,
        "message": server_ctx.message,
        "server": settings.SERVER_NAME,
        "version": settings.SERVER_VERSION,
        "mode": settings.SERVER_MODE.value
    }

    if server_ctx.status == "setup_required":
        status_data["instructions"] = [
            "1. Ensure the package was installed correctly with bundled documentation",
            "2. Restart the MCP server to trigger auto-ingestion",
            "3. Or run 'stm32-ingest' manually"
        ]

    return json.dumps(status_data, indent=2)


@mcp.resource("stm32://health")
def get_health_status(ctx: Context) -> str:
    """
    Get server health status for monitoring.

    Simple health check endpoint that returns basic server info.
    """
    server_ctx = get_context_status(ctx)

    return json.dumps({
        "status": "healthy" if server_ctx.status == "ready" else "degraded",
        "server": settings.SERVER_NAME,
        "version": settings.SERVER_VERSION,
        "mode": settings.SERVER_MODE.value,
        "chunks_indexed": server_ctx.chunk_count,
        "embedding_model": settings.EMBEDDING_MODEL,
        "database_status": server_ctx.status
    }, indent=2)


# ============================================================================
# TOOLS - Core search functionality exposed to MCP clients
# ============================================================================

@mcp.tool()
def search_stm32_docs(
    ctx: Context,
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
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
    ctx: Context,
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
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
    ctx: Context,
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
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
def get_register_info(ctx: Context, register_name: str) -> str:
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
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
def list_peripherals(ctx: Context) -> str:
    """
    List all available peripherals and their documentation coverage.

    Use this tool to discover what peripherals are documented
    and how much content is available for each.

    Returns:
        List of peripherals with chunk counts
    """
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
def search_hal_function(ctx: Context, function_name: str) -> str:
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
    # Check database readiness
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg

    store = get_store_from_context(ctx)

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
def lookup_hal_function(ctx: Context, function_name: str) -> str:
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return _search_hal_function_impl(get_store_from_context(ctx), function_name)


@mcp.tool()
def troubleshoot_error(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_error_solution(get_store_from_context(ctx), error_description, peripheral or None)


@mcp.tool()
def get_init_sequence(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_initialization_sequence(get_store_from_context(ctx), peripheral, use_case)


@mcp.tool()
def get_clock_config(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_clock_configuration(get_store_from_context(ctx), target_frequency, clock_source)


@mcp.tool()
def compare_peripheral_options(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return compare_peripherals(get_store_from_context(ctx), peripheral1, peripheral2, aspect)


@mcp.tool()
def get_migration_guide(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_migration_info(get_store_from_context(ctx), from_family, to_family, peripheral or None)


@mcp.tool()
def get_electrical_specifications(ctx: Context, topic: str) -> str:
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_electrical_specs(get_store_from_context(ctx), topic)


@mcp.tool()
def get_timing_specifications(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return search_timing_info(get_store_from_context(ctx), peripheral, timing_type)


# ============================================================================
# CODE EXAMPLE TOOLS - Specialized example retrieval
# ============================================================================

@mcp.tool()
def get_interrupt_code(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return get_interrupt_example(get_store_from_context(ctx), peripheral, interrupt_type)


@mcp.tool()
def get_dma_code(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return get_dma_example(get_store_from_context(ctx), peripheral, direction)


@mcp.tool()
def get_low_power_code(ctx: Context, mode: str = "") -> str:
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return get_low_power_example(get_store_from_context(ctx), mode)


@mcp.tool()
def get_callback_code(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return get_callback_example(get_store_from_context(ctx), peripheral, callback_type)


@mcp.tool()
def get_init_template(
    ctx: Context,
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
    ready, error_msg = check_database_ready(ctx)
    if not ready:
        return error_msg
    return get_peripheral_init_template(get_store_from_context(ctx), peripheral, mode)


# ============================================================================
# ADDITIONAL RESOURCES - Direct documentation access via URIs
# ============================================================================

@mcp.resource("stm32://stats")
def get_documentation_stats(ctx: Context) -> str:
    """Get statistics about the documentation database."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_stats()


@mcp.resource("stm32://peripherals")
def list_all_peripherals(ctx: Context) -> str:
    """List all documented peripherals."""
    return list_peripherals(ctx)


@mcp.resource("stm32://peripherals/{peripheral}")
def get_peripheral_overview(ctx: Context, peripheral: str) -> str:
    """Get overview documentation for a specific peripheral."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_overview(peripheral)


@mcp.resource("stm32://sources")
def list_doc_sources(ctx: Context) -> str:
    """List all documentation source files."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.list_sources()


@mcp.resource("stm32://peripherals/{peripheral}/overview")
def peripheral_overview(ctx: Context, peripheral: str) -> str:
    """Get comprehensive peripheral overview documentation."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_overview(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/registers")
def peripheral_registers(ctx: Context, peripheral: str) -> str:
    """Get peripheral register documentation."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_registers(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/examples")
def peripheral_examples(ctx: Context, peripheral: str) -> str:
    """Get peripheral code examples."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_examples(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/interrupts")
def peripheral_interrupts(ctx: Context, peripheral: str) -> str:
    """Get peripheral interrupt documentation."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_interrupts(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/dma")
def peripheral_dma(ctx: Context, peripheral: str) -> str:
    """Get peripheral DMA configuration."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_peripheral_dma(peripheral)


@mcp.resource("stm32://hal-functions")
def list_hal_functions(ctx: Context) -> str:
    """List all HAL functions."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_hal_functions_list()


@mcp.resource("stm32://hal-functions/{peripheral}")
def list_peripheral_hal_functions(ctx: Context, peripheral: str) -> str:
    """List HAL functions for a specific peripheral."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_hal_functions_list(peripheral)


@mcp.resource("stm32://documents/{doc_type}")
def get_documents_by_type(ctx: Context, doc_type: str) -> str:
    """Get documents of a specific type."""
    server_ctx = get_context_status(ctx)
    return server_ctx.resources.get_document_by_type(doc_type)


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
        return JSONResponse({
            "status": "healthy",
            "server": settings.SERVER_NAME,
            "version": settings.SERVER_VERSION
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
