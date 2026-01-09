# Documentation Index

Complete index of all documentation for the STM32 MCP Documentation Server.

## Quick Links

- [README](../README.md) - Project overview and quick start
- [CLAUDE.md](../CLAUDE.md) - Claude Code project instructions
- [Getting Started](GETTING_STARTED.md) - Complete setup guide
- [Architecture](ARCHITECTURE.md) - System design and data flow

## Installation

The recommended installation method is via `uvx`:

```bash
claude mcp add stm32-docs --scope user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32.git stm32-mcp-docs
```

See [Getting Started](GETTING_STARTED.md) for detailed instructions.

## User Guides

### Getting Started

| Document | Description | Level |
|----------|-------------|-------|
| [README](../README.md) | Project overview, features, and quick start | Beginner |
| [CLAUDE.md](../CLAUDE.md) | Instructions for Claude Code | Beginner |
| [Getting Started](GETTING_STARTED.md) | Step-by-step installation and first use | Beginner |
| [Quick Start](QUICK_START.md) | Essential commands and quick reference | Beginner |
| [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md) | Using with Claude Code CLI | Intermediate |

### Usage Guides

| Document | Description | Level |
|----------|-------------|-------|
| [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) | Specialized agent capabilities | Intermediate |
| [Agent MCP Integration](AGENT_MCP_INTEGRATION.md) | Agent configuration and MCP tools | Advanced |

## Architecture Documentation

### System Design

| Document | Description | Audience |
|----------|-------------|----------|
| [Architecture](ARCHITECTURE.md) | Complete system architecture and data flow | All |
| [Infrastructure](INFRASTRUCTURE.md) | Project structure and setup | Developers |
| [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md) | Design patterns and conventions | Architects |
| [Execution Specifications](EXECUTION_SPECIFICATIONS.md) | Detailed execution specs | Developers |

### Component Documentation

| Document | Description | Component |
|----------|-------------|-----------|
| [MCP Server](MCP_SERVER.md) | Server implementation details | mcp_server/ |
| [Advanced Tools](ADVANCED_TOOLS.md) | Search tool reference and usage | mcp_server/tools/ |
| [Resources](RESOURCES.md) | MCP resource URI reference | mcp_server/resources/ |
| [Chunking](CHUNKING.md) | Document processing strategy | pipeline/ |
| [Storage](STORAGE.md) | ChromaDB configuration and API | storage/ |

## Development Documentation

### Setup and Maintenance

| Document | Description | Purpose |
|----------|-------------|---------|
| [Ingestion](INGESTION.md) | Document ingestion process | Data management |
| [Testing](TESTING.md) | Test suite and validation | Quality assurance |

### Reference Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [Agent Routing Specification](AGENT_ROUTING_SPECIFICATION.md) | Agent routing logic | Agent developers |
| [STM32 Document Chunking Strategy](STM32_DOCUMENT_CHUNKING_STRATEGY.md) | Detailed chunking algorithm | Pipeline developers |

### Agent Documentation

| Document | Description | Location |
|----------|-------------|----------|
| [Agents MCP Guide](../.claude/agents/AGENTS_MCP_GUIDE.md) | How agents use MCP tools | .claude/agents/ |

## Documentation by Role

### For End Users

Start here if you want to use the system:

1. [README](../README.md) - Overview
2. [Getting Started](GETTING_STARTED.md) - Setup
3. [Quick Start](QUICK_START.md) - Commands
4. [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) - Specialized agents

### For Developers

Start here if you want to understand or modify the system:

1. [CLAUDE.md](../CLAUDE.md) - Project instructions
2. [Architecture](ARCHITECTURE.md) - System design
3. [Infrastructure](INFRASTRUCTURE.md) - Project structure
4. [MCP Server](MCP_SERVER.md) - Server implementation
5. [Storage](STORAGE.md) - Database layer
6. [Chunking](CHUNKING.md) - Document processing
7. [Testing](TESTING.md) - Test suite

### For System Architects

Start here if you want to design with or integrate the system:

1. [Architecture](ARCHITECTURE.md) - System overview
2. [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md) - Design patterns
3. [Execution Specifications](EXECUTION_SPECIFICATIONS.md) - Detailed specs
4. [Advanced Tools](ADVANCED_TOOLS.md) - Tool capabilities
5. [Resources](RESOURCES.md) - Resource API

## Key Features Summary

### Auto-Install on First Run

- **16 STM32 agents** installed to `~/.claude/agents/`
- **Vector database** (13,815 chunks) built from 80 bundled docs
- **Marker files** prevent re-installation

### MCP Tools (15+)

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search |
| `get_peripheral_docs` | Peripheral documentation |
| `get_code_examples` | Code examples |
| `get_register_info` | Register details |
| `lookup_hal_function` | HAL function docs |
| `troubleshoot_error` | Error troubleshooting |
| `get_init_sequence` | Initialization code |
| `get_clock_config` | Clock configuration |
| `compare_peripheral_options` | Compare peripherals |
| `get_migration_guide` | Migration guides |
| `get_interrupt_code` | Interrupt examples |
| `get_dma_code` | DMA examples |
| `get_low_power_code` | Low power modes |
| `get_callback_code` | HAL callbacks |
| `get_init_template` | Init templates |
| `list_peripherals` | List peripherals |

### Agents (16)

| Category | Agents |
|----------|--------|
| Routing | router, triage |
| Firmware | firmware, firmware-core |
| Debugging | debug |
| Bootloader | bootloader, bootloader-programming |
| Peripherals | peripheral-comm, peripheral-analog, peripheral-graphics |
| Power | power, power-management |
| Safety | safety, safety-certification |
| Security | security |
| Hardware | hardware-design |

## Common Tasks

### I want to...

#### Install the System
[README](../README.md) -> [Getting Started](GETTING_STARTED.md)

#### Use with Claude Code
[Claude Code Integration](CLAUDE_CODE_INTEGRATION.md)

#### Search Documentation
[Advanced Tools](ADVANCED_TOOLS.md) -> [Resources](RESOURCES.md)

#### Understand the Agents
[Agent Quick Reference](AGENT_QUICK_REFERENCE.md) -> [Agent MCP Integration](AGENT_MCP_INTEGRATION.md)

#### Understand Architecture
[Architecture](ARCHITECTURE.md) -> [Infrastructure](INFRASTRUCTURE.md)

#### Run Tests
[Testing](TESTING.md)

#### Troubleshoot Issues
[Getting Started - Troubleshooting](GETTING_STARTED.md#troubleshooting)

#### Deploy on Network
[Claude Code Integration - Network Mode](CLAUDE_CODE_INTEGRATION.md#network-mode-tailscale)

#### Develop New Features
[CLAUDE.md](../CLAUDE.md) -> [Architecture](ARCHITECTURE.md) -> [Testing](TESTING.md)

## External Resources

### MCP Protocol
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

### Dependencies
- [ChromaDB](https://www.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Claude Code](https://claude.ai/claude-code)

### STM32 Documentation
- [STM32 Official Documentation](https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html)

## Documentation Statistics

### Coverage

- **Total Documents**: 24+ documentation files
- **Categories**: User Guides, Architecture, Components, Development, Agents

### Last Updated
- All documentation: January 2026

## Version History

### v1.0.0 (January 2026)
- uvx installation support
- Auto-installation of agents and vector database
- 16 specialized agents
- 15+ MCP tools
- Full documentation set

## Getting Help

If you can't find what you're looking for:

1. Check the [README](../README.md) for overview
2. Read [CLAUDE.md](../CLAUDE.md) for Claude Code instructions
3. Try [Getting Started](GETTING_STARTED.md) for setup help
4. Review [Troubleshooting sections](GETTING_STARTED.md#troubleshooting)
5. Read [Architecture](ARCHITECTURE.md) for system understanding
