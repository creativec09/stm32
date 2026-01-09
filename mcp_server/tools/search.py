"""
Advanced search tools for STM32 documentation.

These tools provide specialized search functionality for common
STM32 development workflows including HAL function lookup, error
troubleshooting, initialization sequences, and migration guides.
"""

import logging
import re
from typing import Optional

from storage.chroma_store import STM32ChromaStore
from storage.metadata import DocType, Peripheral, ContentType

logger = logging.getLogger(__name__)


def _extract_peripheral_from_hal_function(function_name: str) -> Optional[Peripheral]:
    """
    Extract peripheral from HAL function name.

    Examples:
        HAL_UART_Transmit -> UART
        HAL_GPIO_Init -> GPIO
        LL_SPI_Enable -> SPI
        __HAL_RCC_GPIOA_CLK_ENABLE -> RCC
    """
    # Pattern for standard HAL/LL functions
    match = re.match(r'^(?:HAL|LL|__HAL)_([A-Z0-9]+)(?:_|$)', function_name.upper())
    if match:
        peripheral_name = match.group(1)
        # Handle special cases
        if peripheral_name.startswith('GPIO'):
            peripheral_name = 'GPIO'
        elif peripheral_name.startswith('TIM'):
            peripheral_name = 'TIM'
        elif peripheral_name.startswith('USART'):
            peripheral_name = 'USART'
        elif peripheral_name.startswith('UART'):
            peripheral_name = 'UART'

        try:
            return Peripheral(peripheral_name)
        except ValueError:
            return None
    return None


def _format_results(results: list[dict], title: str) -> str:
    """Format search results into a readable string."""
    if not results:
        return f"No documentation found for: {title}"

    output = [f"# {title}\n"]

    for i, r in enumerate(results, 1):
        meta = r.get('metadata', {})
        output.append(f"## Result {i} (relevance: {r.get('score', 0):.2f})")
        output.append(f"**Source**: {meta.get('source_file', 'Unknown')}")

        if meta.get('peripheral'):
            output.append(f"**Peripheral**: {meta['peripheral']}")
        if meta.get('section_path'):
            output.append(f"**Section**: {meta['section_path']}")
        if meta.get('doc_type'):
            output.append(f"**Doc Type**: {meta['doc_type']}")
        if meta.get('has_code'):
            output.append("**Contains code examples**")

        output.append("")
        output.append(r.get('content', ''))
        output.append("")
        output.append("---")
        output.append("")

    return "\n".join(output)


def search_hal_function(
    store: STM32ChromaStore,
    function_name: str
) -> str:
    """
    Search for documentation about a specific HAL/LL function.

    Handles patterns like:
    - HAL_UART_Transmit
    - HAL_GPIO_Init
    - LL_GPIO_SetPinMode
    - __HAL_RCC_GPIOA_CLK_ENABLE

    Args:
        store: ChromaDB store instance
        function_name: The HAL/LL function name to search for

    Returns:
        Formatted documentation about the function
    """
    logger.info(f"Searching for HAL function: {function_name}")

    # Extract peripheral from function name for filtering
    peripheral = _extract_peripheral_from_hal_function(function_name)

    # Build enhanced search query
    # Include function name and common documentation keywords
    search_query = f"{function_name} function parameters return"

    # First try searching in HAL guides
    results = store.search(
        query=search_query,
        n_results=5,
        doc_type=DocType.HAL_GUIDE,
        peripheral=peripheral,
        min_score=0.3
    )

    # If no HAL guide results, search all documentation
    if not results:
        results = store.search(
            query=search_query,
            n_results=5,
            peripheral=peripheral,
            require_code=True,
            min_score=0.2
        )

    # Fallback to general search
    if not results:
        results = store.search(
            query=function_name,
            n_results=5,
            min_score=0.2
        )

    return _format_results(results, f"HAL Function: {function_name}")


def search_error_solution(
    store: STM32ChromaStore,
    error_description: str,
    peripheral: Optional[str] = None
) -> str:
    """
    Search for solutions to common STM32 errors.

    Handles error patterns like:
    - HAL_TIMEOUT
    - HardFault
    - Bus Error
    - Configuration issues

    Args:
        store: ChromaDB store instance
        error_description: Description of the error or symptom
        peripheral: Optional peripheral to focus the search

    Returns:
        Troubleshooting steps and solutions
    """
    logger.info(f"Searching for error solution: {error_description}")

    # Parse peripheral filter if provided
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            logger.warning(f"Unknown peripheral filter: {peripheral}")

    # Build search query with troubleshooting context
    # Include common troubleshooting keywords
    search_terms = [
        error_description,
        "troubleshooting",
        "error",
        "solution",
        "fix"
    ]

    # Detect specific error patterns and add relevant terms
    error_upper = error_description.upper()

    if "TIMEOUT" in error_upper:
        search_terms.extend(["timeout", "busy flag", "clock", "configuration"])
    elif "HARDFAULT" in error_upper or "HARD FAULT" in error_upper:
        search_terms.extend(["hardfault", "stack overflow", "memory access", "null pointer"])
    elif "BUS ERROR" in error_upper or "BUSFAULT" in error_upper:
        search_terms.extend(["bus error", "memory", "alignment", "access"])
    elif "DMA" in error_upper:
        search_terms.extend(["DMA", "transfer", "stream", "channel", "FIFO"])
    elif "CLOCK" in error_upper or "RCC" in error_upper:
        search_terms.extend(["clock", "RCC", "PLL", "HSE", "HSI"])
    elif "NOT RECEIVING" in error_upper or "NO DATA" in error_upper:
        search_terms.extend(["receive", "interrupt", "NVIC", "enable"])

    search_query = " ".join(search_terms[:8])  # Limit query length

    # Search for troubleshooting content
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=periph_filter,
        min_score=0.2
    )

    # Also search errata documents for known issues
    errata_results = store.search(
        query=error_description,
        n_results=3,
        doc_type=DocType.ERRATA,
        peripheral=periph_filter,
        min_score=0.3
    )

    # Combine results, prioritizing troubleshooting content
    combined_results = results + errata_results

    # Remove duplicates based on content similarity
    seen_content = set()
    unique_results = []
    for r in combined_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    # Sort by relevance score
    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    return _format_results(unique_results[:8], f"Troubleshooting: {error_description}")


def search_initialization_sequence(
    store: STM32ChromaStore,
    peripheral: str,
    use_case: str = ""
) -> str:
    """
    Search for complete initialization sequences for a peripheral.

    Use cases:
    - Basic initialization
    - DMA mode
    - Interrupt mode
    - Low power mode

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to initialize
        use_case: Specific use case (e.g., "DMA mode", "interrupt driven")

    Returns:
        Complete initialization code with explanations
    """
    logger.info(f"Searching for init sequence: {peripheral} ({use_case})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        logger.warning(f"Unknown peripheral: {peripheral}")

    # Build search query
    query_parts = [peripheral, "initialization", "init", "configuration"]

    if use_case:
        query_parts.append(use_case)
        use_case_upper = use_case.upper()

        # Add specific keywords based on use case
        if "DMA" in use_case_upper:
            query_parts.extend(["DMA", "transfer", "circular", "stream"])
        elif "INTERRUPT" in use_case_upper:
            query_parts.extend(["interrupt", "callback", "NVIC", "IRQ"])
        elif "LOW POWER" in use_case_upper:
            query_parts.extend(["low power", "sleep", "stop", "standby"])
        elif "CONTINUOUS" in use_case_upper:
            query_parts.extend(["continuous", "conversion", "scan"])
        elif "MASTER" in use_case_upper:
            query_parts.extend(["master", "mode"])
        elif "SLAVE" in use_case_upper:
            query_parts.extend(["slave", "mode"])

    search_query = " ".join(query_parts[:8])

    # Search for code examples with initialization
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.2
    )

    # If no code results, try without require_code
    if not results:
        results = store.search(
            query=search_query,
            n_results=8,
            peripheral=periph_filter,
            min_score=0.2
        )

    title = f"Initialization Sequence: {peripheral}"
    if use_case:
        title += f" ({use_case})"

    return _format_results(results, title)


def search_clock_configuration(
    store: STM32ChromaStore,
    target_frequency: str = "",
    clock_source: str = ""
) -> str:
    """
    Search for clock configuration examples.

    Parameters:
    - target_frequency: e.g., "168MHz", "480MHz", "84MHz"
    - clock_source: HSE, HSI, PLL, LSE, LSI

    Args:
        store: ChromaDB store instance
        target_frequency: Target system clock frequency
        clock_source: Clock source (HSE, HSI, PLL)

    Returns:
        Clock configuration code and explanations
    """
    logger.info(f"Searching for clock config: {target_frequency} / {clock_source}")

    # Build search query
    query_parts = ["clock", "configuration", "RCC", "system clock"]

    if target_frequency:
        query_parts.append(target_frequency)
        # Extract numeric value for context
        freq_match = re.search(r'(\d+)\s*[Mm][Hh][Zz]', target_frequency)
        if freq_match:
            query_parts.append(f"SYSCLK {freq_match.group(1)}")

    if clock_source:
        clock_source_upper = clock_source.upper()
        query_parts.append(clock_source)

        # Add related terms
        if clock_source_upper == "PLL":
            query_parts.extend(["PLL", "PLLM", "PLLN", "PLLP", "PLLQ"])
        elif clock_source_upper == "HSE":
            query_parts.extend(["HSE", "external oscillator", "crystal"])
        elif clock_source_upper == "HSI":
            query_parts.extend(["HSI", "internal oscillator"])
        elif clock_source_upper == "LSE":
            query_parts.extend(["LSE", "32.768", "RTC"])
        elif clock_source_upper == "LSI":
            query_parts.extend(["LSI", "watchdog"])

    search_query = " ".join(query_parts[:10])

    # Search with RCC peripheral filter
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=Peripheral.RCC,
        require_code=True,
        min_score=0.2
    )

    # Fallback without code requirement
    if not results:
        results = store.search(
            query=search_query,
            n_results=8,
            peripheral=Peripheral.RCC,
            min_score=0.2
        )

    title = "Clock Configuration"
    if target_frequency:
        title += f" ({target_frequency})"
    if clock_source:
        title += f" - {clock_source}"

    return _format_results(results, title)


def compare_peripherals(
    store: STM32ChromaStore,
    peripheral1: str,
    peripheral2: str,
    aspect: str = ""
) -> str:
    """
    Get documentation comparing two peripherals or modes.

    Examples:
    - UART vs USART
    - SPI vs I2C
    - DMA vs BDMA vs MDMA

    Args:
        store: ChromaDB store instance
        peripheral1: First peripheral to compare
        peripheral2: Second peripheral to compare
        aspect: Specific aspect to compare (e.g., "speed", "power consumption")

    Returns:
        Documentation comparing the two peripherals
    """
    logger.info(f"Comparing peripherals: {peripheral1} vs {peripheral2}")

    # Build search query
    query_parts = [peripheral1, peripheral2, "comparison", "difference", "vs"]

    if aspect:
        query_parts.append(aspect)

    search_query = " ".join(query_parts)

    # Search for comparison documentation
    results = store.search(
        query=search_query,
        n_results=6,
        min_score=0.2
    )

    # Also get documentation for each peripheral separately
    periph1_results = []
    periph2_results = []

    try:
        periph1_enum = Peripheral(peripheral1.upper())
        periph1_results = store.search_by_peripheral(
            periph1_enum,
            query=f"overview features {aspect}".strip(),
            n_results=3
        )
    except ValueError:
        pass

    try:
        periph2_enum = Peripheral(peripheral2.upper())
        periph2_results = store.search_by_peripheral(
            periph2_enum,
            query=f"overview features {aspect}".strip(),
            n_results=3
        )
    except ValueError:
        pass

    # Combine results
    all_results = results + periph1_results[:2] + periph2_results[:2]

    # Remove duplicates
    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    # Sort by relevance
    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"Comparison: {peripheral1} vs {peripheral2}"
    if aspect:
        title += f" ({aspect})"

    return _format_results(unique_results[:8], title)


def search_migration_info(
    store: STM32ChromaStore,
    from_family: str,
    to_family: str,
    peripheral: str = ""
) -> str:
    """
    Search for migration information between STM32 families.

    Examples:
    - STM32F4 to STM32H7
    - STM32F1 to STM32G4

    Args:
        store: ChromaDB store instance
        from_family: Source STM32 family (e.g., "STM32F4")
        to_family: Target STM32 family (e.g., "STM32H7")
        peripheral: Optional specific peripheral to focus on

    Returns:
        Migration considerations, differences, and code changes
    """
    logger.info(f"Searching migration info: {from_family} -> {to_family}")

    # Normalize family names
    from_family = from_family.upper()
    to_family = to_family.upper()

    # Add STM32 prefix if not present
    if not from_family.startswith("STM32"):
        from_family = f"STM32{from_family}"
    if not to_family.startswith("STM32"):
        to_family = f"STM32{to_family}"

    # Build search query
    query_parts = [
        from_family, to_family,
        "migration", "porting", "differences",
        "compatibility"
    ]

    if peripheral:
        query_parts.append(peripheral)

    search_query = " ".join(query_parts)

    # Parse peripheral filter if provided
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            pass

    # Search in migration guides first
    results = store.search(
        query=search_query,
        n_results=8,
        doc_type=DocType.MIGRATION_GUIDE,
        peripheral=periph_filter,
        min_score=0.2
    )

    # Also search application notes
    app_note_results = store.search(
        query=search_query,
        n_results=4,
        doc_type=DocType.APPLICATION_NOTE,
        peripheral=periph_filter,
        min_score=0.3
    )

    # General search for family-specific info
    general_results = store.search(
        query=f"{from_family} {to_family} {peripheral}".strip(),
        n_results=4,
        peripheral=periph_filter,
        min_score=0.3
    )

    # Combine and deduplicate
    all_results = results + app_note_results + general_results

    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"Migration Guide: {from_family} to {to_family}"
    if peripheral:
        title += f" ({peripheral})"

    return _format_results(unique_results[:8], title)


def search_electrical_specs(
    store: STM32ChromaStore,
    topic: str
) -> str:
    """
    Search for electrical specifications.

    Topics:
    - GPIO drive strength
    - ADC input impedance
    - Power consumption
    - Operating voltage

    Args:
        store: ChromaDB store instance
        topic: The electrical specification topic

    Returns:
        Electrical specification documentation
    """
    logger.info(f"Searching electrical specs: {topic}")

    # Build search query with electrical context
    query_parts = [
        topic,
        "electrical", "specifications", "characteristics"
    ]

    # Add specific terms based on topic
    topic_upper = topic.upper()

    if "DRIVE" in topic_upper or "STRENGTH" in topic_upper:
        query_parts.extend(["drive strength", "current", "mA", "output"])
    elif "IMPEDANCE" in topic_upper:
        query_parts.extend(["impedance", "input", "ohm", "resistance"])
    elif "POWER" in topic_upper or "CONSUMPTION" in topic_upper:
        query_parts.extend(["power consumption", "current", "mA", "uA", "sleep"])
    elif "VOLTAGE" in topic_upper:
        query_parts.extend(["voltage", "VDD", "operating", "supply"])
    elif "TEMPERATURE" in topic_upper:
        query_parts.extend(["temperature", "range", "operating"])
    elif "TIMING" in topic_upper:
        query_parts.extend(["timing", "setup", "hold", "delay"])

    search_query = " ".join(query_parts[:10])

    # Search in datasheets first
    results = store.search(
        query=search_query,
        n_results=8,
        doc_type=DocType.DATASHEET,
        min_score=0.2
    )

    # Also search reference manuals
    ref_results = store.search(
        query=search_query,
        n_results=4,
        doc_type=DocType.REFERENCE_MANUAL,
        min_score=0.3
    )

    # Combine results
    all_results = results + ref_results

    # Remove duplicates
    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    return _format_results(unique_results[:8], f"Electrical Specifications: {topic}")


def search_timing_info(
    store: STM32ChromaStore,
    peripheral: str,
    timing_type: str = ""
) -> str:
    """
    Search for timing specifications and diagrams.

    Timing types:
    - Setup/hold times
    - Clock frequencies
    - Latency requirements

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to search timing info for
        timing_type: Specific timing type to search for

    Returns:
        Timing specification documentation
    """
    logger.info(f"Searching timing info: {peripheral} ({timing_type})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        pass

    # Build search query
    query_parts = [peripheral, "timing", "diagram"]

    if timing_type:
        query_parts.append(timing_type)
        timing_upper = timing_type.upper()

        if "SETUP" in timing_upper or "HOLD" in timing_upper:
            query_parts.extend(["setup", "hold", "time", "ns"])
        elif "CLOCK" in timing_upper or "FREQUENCY" in timing_upper:
            query_parts.extend(["clock", "frequency", "MHz", "prescaler"])
        elif "LATENCY" in timing_upper:
            query_parts.extend(["latency", "delay", "cycles"])
        elif "BAUD" in timing_upper:
            query_parts.extend(["baud rate", "speed", "bits per second"])

    search_query = " ".join(query_parts[:10])

    # Search for timing information
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=periph_filter,
        min_score=0.2
    )

    title = f"Timing Information: {peripheral}"
    if timing_type:
        title += f" ({timing_type})"

    return _format_results(results, title)


# Export all functions
__all__ = [
    "search_hal_function",
    "search_error_solution",
    "search_initialization_sequence",
    "search_clock_configuration",
    "compare_peripherals",
    "search_migration_info",
    "search_electrical_specs",
    "search_timing_info",
]
