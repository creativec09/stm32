"""
Code example tools for STM32 documentation.

These tools provide specialized access to code examples for common
STM32 development patterns including interrupts, DMA, and low power modes.
"""

import logging
from typing import Optional

from storage.chroma_store import STM32ChromaStore
from storage.metadata import DocType, Peripheral, ContentType

logger = logging.getLogger(__name__)


def _format_code_results(results: list[dict], title: str) -> str:
    """Format code example results into a readable string."""
    if not results:
        return f"No code examples found for: {title}"

    output = [f"# {title}\n"]

    for i, r in enumerate(results, 1):
        meta = r.get('metadata', {})
        output.append(f"## Example {i}")
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*")

        if meta.get('peripheral'):
            output.append(f"*Peripheral: {meta['peripheral']}*")
        if meta.get('section_path'):
            output.append(f"*Section: {meta['section_path']}*")
        if meta.get('doc_type'):
            output.append(f"*Document Type: {meta['doc_type']}*")

        output.append("")
        output.append(r.get('content', ''))
        output.append("")
        output.append("---")
        output.append("")

    return "\n".join(output)


def get_interrupt_example(
    store: STM32ChromaStore,
    peripheral: str,
    interrupt_type: str = ""
) -> str:
    """
    Get interrupt handling examples for a peripheral.

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to get interrupt examples for
        interrupt_type: Specific interrupt type (e.g., "RXNE", "TC", "update")

    Returns:
        Interrupt handling code examples with context

    Examples:
        - get_interrupt_example(store, "UART")
        - get_interrupt_example(store, "TIM", "update")
        - get_interrupt_example(store, "EXTI", "rising edge")
    """
    logger.info(f"Searching for interrupt example: {peripheral} ({interrupt_type})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        logger.warning(f"Unknown peripheral: {peripheral}")

    # Build search query
    query_parts = [
        peripheral,
        "interrupt",
        "callback",
        "handler",
        "IRQHandler",
        "NVIC"
    ]

    if interrupt_type:
        query_parts.append(interrupt_type)

        # Add specific keywords based on interrupt type
        int_type_upper = interrupt_type.upper()
        if "RXNE" in int_type_upper or "RX" in int_type_upper:
            query_parts.extend(["receive", "RXNE", "data ready"])
        elif "TC" in int_type_upper or "TX" in int_type_upper:
            query_parts.extend(["transmit", "complete", "TXE"])
        elif "UPDATE" in int_type_upper:
            query_parts.extend(["update", "overflow", "UIE"])
        elif "CAPTURE" in int_type_upper or "CC" in int_type_upper:
            query_parts.extend(["capture", "compare", "CCx"])
        elif "EXTI" in int_type_upper or "EDGE" in int_type_upper:
            query_parts.extend(["EXTI", "edge", "trigger"])
        elif "ERROR" in int_type_upper:
            query_parts.extend(["error", "fault", "overrun"])
        elif "DMA" in int_type_upper:
            query_parts.extend(["DMA", "transfer", "complete"])

    search_query = " ".join(query_parts[:10])

    # Search for code examples
    results = store.search(
        query=search_query,
        n_results=6,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.2
    )

    # Also search for callback functions specifically
    callback_results = store.search(
        query=f"{peripheral} HAL callback interrupt",
        n_results=4,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.3
    )

    # Combine and deduplicate
    all_results = results + callback_results

    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"Interrupt Examples: {peripheral}"
    if interrupt_type:
        title += f" ({interrupt_type})"

    return _format_code_results(unique_results[:6], title)


def get_dma_example(
    store: STM32ChromaStore,
    peripheral: str,
    direction: str = ""  # TX, RX, or both
) -> str:
    """
    Get DMA configuration examples for a peripheral.

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to get DMA examples for
        direction: Transfer direction (TX, RX, both, or empty for all)

    Returns:
        DMA configuration code examples with context

    Examples:
        - get_dma_example(store, "UART")
        - get_dma_example(store, "SPI", "TX")
        - get_dma_example(store, "ADC", "RX")
    """
    logger.info(f"Searching for DMA example: {peripheral} ({direction})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        logger.warning(f"Unknown peripheral: {peripheral}")

    # Build search query
    query_parts = [
        peripheral,
        "DMA",
        "configuration",
        "transfer",
        "stream",
        "channel"
    ]

    if direction:
        direction_upper = direction.upper()
        if "TX" in direction_upper or "TRANSMIT" in direction_upper:
            query_parts.extend(["transmit", "TX", "memory to peripheral"])
        elif "RX" in direction_upper or "RECEIVE" in direction_upper:
            query_parts.extend(["receive", "RX", "peripheral to memory"])
        elif "BOTH" in direction_upper or "CIRCULAR" in direction_upper:
            query_parts.extend(["circular", "continuous", "bidirectional"])

    search_query = " ".join(query_parts[:10])

    # Search for DMA examples
    results = store.search(
        query=search_query,
        n_results=6,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.2
    )

    # Also search in DMA peripheral docs
    dma_results = store.search(
        query=f"DMA {peripheral} {direction}".strip(),
        n_results=4,
        peripheral=Peripheral.DMA,
        require_code=True,
        min_score=0.3
    )

    # Combine and deduplicate
    all_results = results + dma_results

    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"DMA Examples: {peripheral}"
    if direction:
        title += f" ({direction})"

    return _format_code_results(unique_results[:6], title)


def get_low_power_example(
    store: STM32ChromaStore,
    mode: str = ""  # Sleep, Stop, Standby
) -> str:
    """
    Get low power mode examples.

    Args:
        store: ChromaDB store instance
        mode: Low power mode (Sleep, Stop, Standby, or empty for all)

    Returns:
        Low power configuration code examples

    Examples:
        - get_low_power_example(store)
        - get_low_power_example(store, "Sleep")
        - get_low_power_example(store, "Stop")
        - get_low_power_example(store, "Standby")
    """
    logger.info(f"Searching for low power example: {mode}")

    # Build search query
    query_parts = [
        "low power",
        "mode",
        "configuration",
        "PWR",
        "wakeup"
    ]

    if mode:
        mode_upper = mode.upper()
        query_parts.append(mode)

        if "SLEEP" in mode_upper:
            query_parts.extend(["sleep", "WFI", "WFE", "__WFI"])
        elif "STOP" in mode_upper:
            query_parts.extend(["stop", "regulator", "voltage scaling"])
        elif "STANDBY" in mode_upper:
            query_parts.extend(["standby", "backup", "WKUP pin"])
        elif "RUN" in mode_upper:
            query_parts.extend(["low power run", "LPR", "reduced frequency"])
        elif "SHUTDOWN" in mode_upper:
            query_parts.extend(["shutdown", "ultra low power"])

    search_query = " ".join(query_parts[:10])

    # Search for low power examples
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=Peripheral.PWR,
        require_code=True,
        min_score=0.2
    )

    # Fallback without code requirement
    if not results:
        results = store.search(
            query=search_query,
            n_results=8,
            peripheral=Peripheral.PWR,
            min_score=0.2
        )

    # Also search general documentation
    general_results = store.search(
        query=f"low power {mode}".strip(),
        n_results=4,
        require_code=True,
        min_score=0.3
    )

    # Combine and deduplicate
    all_results = results + general_results

    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = "Low Power Mode Examples"
    if mode:
        title += f": {mode}"

    return _format_code_results(unique_results[:8], title)


def get_callback_example(
    store: STM32ChromaStore,
    peripheral: str,
    callback_type: str = ""
) -> str:
    """
    Get HAL callback function examples.

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to get callback examples for
        callback_type: Specific callback type (e.g., "TxCplt", "RxCplt", "Error")

    Returns:
        HAL callback implementation examples

    Examples:
        - get_callback_example(store, "UART")
        - get_callback_example(store, "SPI", "TxRxCplt")
        - get_callback_example(store, "I2C", "Error")
    """
    logger.info(f"Searching for callback example: {peripheral} ({callback_type})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        logger.warning(f"Unknown peripheral: {peripheral}")

    # Build search query
    query_parts = [
        peripheral,
        "HAL",
        "callback",
        "Cplt",
        "implementation"
    ]

    if callback_type:
        query_parts.append(callback_type)

        # Add specific callback patterns
        cb_upper = callback_type.upper()
        if "TX" in cb_upper and "CPLT" in cb_upper:
            query_parts.extend(["TxCpltCallback", "transmit complete"])
        elif "RX" in cb_upper and "CPLT" in cb_upper:
            query_parts.extend(["RxCpltCallback", "receive complete"])
        elif "TXRX" in cb_upper:
            query_parts.extend(["TxRxCpltCallback", "transmit receive"])
        elif "ERROR" in cb_upper:
            query_parts.extend(["ErrorCallback", "error handling"])
        elif "HALF" in cb_upper:
            query_parts.extend(["HalfCpltCallback", "half transfer"])
        elif "ABORT" in cb_upper:
            query_parts.extend(["AbortCpltCallback", "abort"])

    search_query = " ".join(query_parts[:10])

    # Search for callback examples
    results = store.search(
        query=search_query,
        n_results=6,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.2
    )

    # Also search HAL guides
    hal_results = store.search(
        query=f"HAL_{peripheral}_Callback",
        n_results=4,
        doc_type=DocType.HAL_GUIDE,
        require_code=True,
        min_score=0.3
    )

    # Combine and deduplicate
    all_results = results + hal_results

    seen_content = set()
    unique_results = []
    for r in all_results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"Callback Examples: {peripheral}"
    if callback_type:
        title += f" ({callback_type})"

    return _format_code_results(unique_results[:6], title)


def get_peripheral_init_template(
    store: STM32ChromaStore,
    peripheral: str,
    mode: str = ""
) -> str:
    """
    Get a complete peripheral initialization template.

    Args:
        store: ChromaDB store instance
        peripheral: The peripheral to get init template for
        mode: Specific mode or configuration (e.g., "master", "slave", "PWM")

    Returns:
        Complete initialization template with all required steps

    Examples:
        - get_peripheral_init_template(store, "SPI")
        - get_peripheral_init_template(store, "SPI", "master")
        - get_peripheral_init_template(store, "TIM", "PWM")
    """
    logger.info(f"Searching for init template: {peripheral} ({mode})")

    # Parse peripheral
    periph_filter = None
    try:
        periph_filter = Peripheral(peripheral.upper())
    except ValueError:
        logger.warning(f"Unknown peripheral: {peripheral}")

    # Build comprehensive search query for init template
    query_parts = [
        peripheral,
        "initialization",
        "complete",
        "template",
        "example",
        "clock enable",
        "GPIO",
        "configuration"
    ]

    if mode:
        query_parts.append(mode)
        mode_upper = mode.upper()

        # Add mode-specific keywords
        if "MASTER" in mode_upper:
            query_parts.extend(["master", "NSS", "CS"])
        elif "SLAVE" in mode_upper:
            query_parts.extend(["slave", "NSS"])
        elif "PWM" in mode_upper:
            query_parts.extend(["PWM", "output compare", "duty cycle"])
        elif "INPUT" in mode_upper:
            query_parts.extend(["input capture", "trigger"])
        elif "ENCODER" in mode_upper:
            query_parts.extend(["encoder", "quadrature"])
        elif "BLOCKING" in mode_upper:
            query_parts.extend(["blocking", "polling"])
        elif "INTERRUPT" in mode_upper:
            query_parts.extend(["interrupt", "IT", "callback"])
        elif "DMA" in mode_upper:
            query_parts.extend(["DMA", "transfer"])

    search_query = " ".join(query_parts[:12])

    # Search for initialization examples
    results = store.search(
        query=search_query,
        n_results=8,
        peripheral=periph_filter,
        require_code=True,
        min_score=0.2
    )

    # Fallback without code requirement
    if len(results) < 3:
        additional = store.search(
            query=f"{peripheral} init {mode}".strip(),
            n_results=5,
            peripheral=periph_filter,
            min_score=0.2
        )
        results.extend(additional)

    # Remove duplicates
    seen_content = set()
    unique_results = []
    for r in results:
        content_hash = hash(r.get('content', '')[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_results.append(r)

    unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)

    title = f"Initialization Template: {peripheral}"
    if mode:
        title += f" ({mode})"

    return _format_code_results(unique_results[:8], title)


# Export all functions
__all__ = [
    "get_interrupt_example",
    "get_dma_example",
    "get_low_power_example",
    "get_callback_example",
    "get_peripheral_init_template",
]
