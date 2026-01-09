"""
MCP Resource handlers for STM32 documentation.

Resources provide direct access to documentation content without
requiring search queries. They are useful for:
- Browsing available documentation
- Getting comprehensive peripheral overviews
- Accessing structured content by category
"""

from pathlib import Path
from typing import Optional
import json
import logging
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral, DocType

logger = logging.getLogger(__name__)


class DocumentationResources:
    """Handler for documentation resources."""

    def __init__(self, store: STM32ChromaStore):
        self.store = store

    def get_peripheral_overview(self, peripheral: str) -> str:
        """Get comprehensive overview for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.search_by_peripheral(
            periph,
            "overview introduction features capabilities",
            n_results=5
        )

        if not results:
            return f"No documentation for {peripheral}"

        content = [f"# {peripheral} Overview\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_registers(self, peripheral: str) -> str:
        """Get register documentation for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.search(
            query=f"{peripheral} register map offset bits fields",
            n_results=10,
            peripheral=periph,
            require_register=True
        )

        if not results:
            return f"No register documentation for {peripheral}"

        content = [f"# {peripheral} Registers\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_examples(self, peripheral: str) -> str:
        """Get all code examples for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.get_code_examples(
            topic=f"{peripheral} example initialization",
            peripheral=periph,
            n_results=10
        )

        if not results:
            return f"No code examples for {peripheral}"

        content = [f"# {peripheral} Code Examples\n"]
        for i, r in enumerate(results, 1):
            content.append(f"## Example {i}")
            content.append(f"*Source: {r['metadata'].get('source_file', 'Unknown')}*\n")
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_interrupts(self, peripheral: str) -> str:
        """Get interrupt documentation for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.search(
            query=f"{peripheral} interrupt handler IRQ callback NVIC",
            n_results=8,
            peripheral=periph
        )

        if not results:
            return f"No interrupt documentation for {peripheral}"

        content = [f"# {peripheral} Interrupts\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_dma(self, peripheral: str) -> str:
        """Get DMA configuration for a peripheral."""
        results = self.store.search(
            query=f"{peripheral} DMA configuration channel stream request",
            n_results=8
        )

        if not results:
            return f"No DMA documentation for {peripheral}"

        content = [f"# {peripheral} DMA Configuration\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_stats(self) -> str:
        """Get detailed documentation statistics."""
        stats = self.store.get_stats()
        periph_dist = self.store.get_peripheral_distribution()
        doc_dist = self.store.get_doc_type_distribution()

        return json.dumps({
            "total_chunks": stats.get('total_chunks', 0),
            "peripheral_distribution": periph_dist,
            "document_type_distribution": doc_dist,
            "collection_name": stats.get('collection_name', 'stm32_docs'),
            "embedding_model": stats.get('embedding_model', 'unknown'),
        }, indent=2)

    def list_sources(self) -> str:
        """List all documentation source files."""
        sources = self.store.list_sources()

        output = ["# Documentation Sources\n"]

        # Group by type
        app_notes = [s for s in sources if s.startswith("an")]
        ref_manuals = [s for s in sources if s.startswith("rm")]
        user_manuals = [s for s in sources if s.startswith("um")]
        prog_manuals = [s for s in sources if s.startswith("pm")]
        other = [s for s in sources if s not in app_notes + ref_manuals + user_manuals + prog_manuals]

        if ref_manuals:
            output.append("## Reference Manuals")
            for s in sorted(ref_manuals):
                output.append(f"- {s}")
            output.append("")

        if app_notes:
            output.append("## Application Notes")
            for s in sorted(app_notes):
                output.append(f"- {s}")
            output.append("")

        if user_manuals:
            output.append("## User Manuals")
            for s in sorted(user_manuals):
                output.append(f"- {s}")
            output.append("")

        if prog_manuals:
            output.append("## Programming Manuals")
            for s in sorted(prog_manuals):
                output.append(f"- {s}")
            output.append("")

        if other:
            output.append("## Other Documents")
            for s in sorted(other):
                output.append(f"- {s}")
            output.append("")

        output.append(f"\n**Total sources**: {len(sources)}")
        return "\n".join(output)

    def get_hal_functions_list(self, peripheral: str = "") -> str:
        """List HAL functions for a peripheral or all peripherals."""
        if peripheral:
            query = f"HAL_{peripheral} function"
        else:
            query = "HAL_ function API"

        results = self.store.search(query, n_results=20, require_code=True)

        # Extract function names from results
        import re
        functions = set()
        pattern = r'(HAL_[A-Z][a-zA-Z0-9_]+)\s*\('

        for r in results:
            matches = re.findall(pattern, r['content'])
            functions.update(matches)

        output = [f"# HAL Functions" + (f" for {peripheral}" if peripheral else "") + "\n"]
        for func in sorted(functions):
            output.append(f"- `{func}()`")

        return "\n".join(output)

    def get_document_by_type(self, doc_type: str) -> str:
        """Get documentation summary for a document type."""
        try:
            dtype = DocType(doc_type.lower())
        except ValueError:
            valid = ", ".join(d.value for d in DocType)
            return f"Unknown document type: {doc_type}. Valid: {valid}"

        results = self.store.search(
            query=f"{doc_type} overview",
            n_results=10,
            doc_type=dtype
        )

        if not results:
            return f"No {doc_type} documentation found"

        # Get unique sources
        sources = set()
        for r in results:
            sources.add(r['metadata'].get('source_file', 'unknown'))

        output = [f"# {doc_type.replace('_', ' ').title()} Documents\n"]
        output.append(f"Found {len(sources)} documents of this type:\n")
        for s in sorted(sources):
            output.append(f"- {s}")

        return "\n".join(output)
