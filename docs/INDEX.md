# Documentation Index

Complete index of all documentation for the STM32 MCP Documentation Server.

## Quick Links

- [README](../README.md) - Project overview and quick start
- [Getting Started](GETTING_STARTED.md) - Complete setup guide
- [Architecture](ARCHITECTURE.md) - System design and data flow

## User Guides

### Getting Started

| Document | Description | Level |
|----------|-------------|-------|
| [README](../README.md) | Project overview, features, and quick start | Beginner |
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

1. [Architecture](ARCHITECTURE.md) - System design
2. [Infrastructure](INFRASTRUCTURE.md) - Project structure
3. [MCP Server](MCP_SERVER.md) - Server implementation
4. [Storage](STORAGE.md) - Database layer
5. [Chunking](CHUNKING.md) - Document processing
6. [Testing](TESTING.md) - Test suite

### For System Architects

Start here if you want to design with or integrate the system:

1. [Architecture](ARCHITECTURE.md) - System overview
2. [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md) - Design patterns
3. [Execution Specifications](EXECUTION_SPECIFICATIONS.md) - Detailed specs
4. [Advanced Tools](ADVANCED_TOOLS.md) - Tool capabilities
5. [Resources](RESOURCES.md) - Resource API

## Documentation by Topic

### Installation & Setup

- [README - Quick Start](../README.md#quick-start)
- [Getting Started](GETTING_STARTED.md)
- [Infrastructure - Setup](INFRASTRUCTURE.md)

### Configuration

- [Getting Started - Configuration](GETTING_STARTED.md#configuration-reference)
- [Infrastructure - Configuration](INFRASTRUCTURE.md)
- [MCP Server - Configuration](MCP_SERVER.md#configuration)

### Usage

- [Quick Start](QUICK_START.md)
- [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md)
- [Agent Quick Reference](AGENT_QUICK_REFERENCE.md)

### Search & Retrieval

- [Advanced Tools](ADVANCED_TOOLS.md)
- [Resources](RESOURCES.md)
- [Storage - API Reference](STORAGE.md)

### Data Management

- [Ingestion](INGESTION.md)
- [Chunking](CHUNKING.md)
- [Storage](STORAGE.md)

### Development

- [Testing](TESTING.md)
- [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md)
- [Execution Specifications](EXECUTION_SPECIFICATIONS.md)

### Agents

- [Agent Quick Reference](AGENT_QUICK_REFERENCE.md)
- [Agent MCP Integration](AGENT_MCP_INTEGRATION.md)
- [Agent Routing Specification](AGENT_ROUTING_SPECIFICATION.md)
- [Agents MCP Guide](../.claude/agents/AGENTS_MCP_GUIDE.md)

### Troubleshooting

- [Getting Started - Troubleshooting](GETTING_STARTED.md#troubleshooting)
- [README - Troubleshooting](../README.md#troubleshooting)
- [Testing - Validation](TESTING.md)

## Component-Specific Documentation

### mcp_server/

| File | Documentation |
|------|---------------|
| server.py | [MCP Server](MCP_SERVER.md) |
| config.py | [Infrastructure - Configuration](INFRASTRUCTURE.md) |
| tools/ | [Advanced Tools](ADVANCED_TOOLS.md) |
| resources/ | [Resources](RESOURCES.md) |

### pipeline/

| File | Documentation |
|------|---------------|
| chunker.py | [Chunking](CHUNKING.md) |
| validator.py | [Chunking - Validation](CHUNKING.md#validation) |
| README.md | [Pipeline README](../pipeline/README.md) |

### storage/

| File | Documentation |
|------|---------------|
| chroma_store.py | [Storage](STORAGE.md) |
| metadata.py | [Storage - Metadata Schema](STORAGE.md#metadata-schema) |
| README.md | [Storage README](../storage/README.md) |
| SCHEMA_REFERENCE.md | [Storage Schema Reference](../storage/SCHEMA_REFERENCE.md) |

### scripts/

| File | Documentation |
|------|---------------|
| ingest_docs.py | [Ingestion](INGESTION.md) |
| test_retrieval.py | [Testing - Search Tests](TESTING.md) |
| verify_mcp.py | [Testing - System Validation](TESTING.md) |
| start_server.py | [MCP Server - Starting](MCP_SERVER.md) |
| README.md | [Scripts README](../scripts/README.md) |

### tests/

| Directory | Documentation |
|-----------|---------------|
| tests/ | [Testing](TESTING.md) |

### .claude/

| File/Directory | Documentation |
|----------------|---------------|
| mcp.json | [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md) |
| agents/ | [Agent MCP Integration](AGENT_MCP_INTEGRATION.md) |
| commands/ | [Quick Start - Slash Commands](QUICK_START.md) |

## Documentation by File Type

### Primary Guides (Start Here)

- [README](../README.md)
- [Getting Started](GETTING_STARTED.md)
- [Architecture](ARCHITECTURE.md)

### Quick References

- [Quick Start](QUICK_START.md)
- [Agent Quick Reference](AGENT_QUICK_REFERENCE.md)

### Component Documentation

- [MCP Server](MCP_SERVER.md)
- [Advanced Tools](ADVANCED_TOOLS.md)
- [Resources](RESOURCES.md)
- [Storage](STORAGE.md)
- [Chunking](CHUNKING.md)

### Integration Guides

- [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md)
- [Agent MCP Integration](AGENT_MCP_INTEGRATION.md)

### Process Documentation

- [Ingestion](INGESTION.md)
- [Testing](TESTING.md)

### Technical Specifications

- [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md)
- [Execution Specifications](EXECUTION_SPECIFICATIONS.md)
- [Agent Routing Specification](AGENT_ROUTING_SPECIFICATION.md)
- [STM32 Document Chunking Strategy](STM32_DOCUMENT_CHUNKING_STRATEGY.md)

### Component READMEs

- [Pipeline README](../pipeline/README.md)
- [Storage README](../storage/README.md)
- [Scripts README](../scripts/README.md)

## Common Tasks

### I want to...

#### Get Started
→ [README](../README.md) → [Getting Started](GETTING_STARTED.md)

#### Use the System
→ [Quick Start](QUICK_START.md) → [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md)

#### Search Documentation
→ [Advanced Tools](ADVANCED_TOOLS.md) → [Resources](RESOURCES.md)

#### Add Documentation
→ [Ingestion](INGESTION.md) → [Chunking](CHUNKING.md)

#### Understand Architecture
→ [Architecture](ARCHITECTURE.md) → [Infrastructure](INFRASTRUCTURE.md)

#### Configure Agents
→ [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) → [Agent MCP Integration](AGENT_MCP_INTEGRATION.md)

#### Run Tests
→ [Testing](TESTING.md)

#### Troubleshoot Issues
→ [Getting Started - Troubleshooting](GETTING_STARTED.md#troubleshooting) → [Testing](TESTING.md)

#### Deploy on Network
→ [Getting Started - Network Mode](GETTING_STARTED.md#network-mode-optional) → [MCP Server](MCP_SERVER.md)

#### Develop New Features
→ [Architecture](ARCHITECTURE.md) → [Architecture Best Practices](ARCHITECTURE_BEST_PRACTICES.md) → [Execution Specifications](EXECUTION_SPECIFICATIONS.md)

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

- **Total Documents**: 23 documentation files
- **Total Pages**: ~200 pages (estimated)
- **Total Words**: ~50,000 words (estimated)

### Categories

- User Guides: 4
- Architecture: 4
- Components: 5
- Development: 2
- Agents: 4
- Technical Specs: 4

## Contributing to Documentation

When adding or updating documentation:

1. **Follow the structure** - Use existing documents as templates
2. **Cross-reference** - Link to related documents
3. **Update INDEX.md** - Add new documents to this index
4. **Be consistent** - Follow naming conventions (UPPERCASE.md for docs)
5. **Include examples** - Show code snippets and commands
6. **Test commands** - Verify all commands work
7. **Update README** - If adding major documentation, update main README

## Documentation Maintenance

### Last Updated
- README: 2026-01-08
- Getting Started: 2026-01-08
- Architecture: 2026-01-08
- Index: 2026-01-08

### Needs Review
All documentation is current as of January 2026.

## Version History

### v0.1.0 (2026-01-08)
- Initial comprehensive documentation set
- Complete architecture documentation
- User guides and quick start
- Component documentation
- Testing and development guides

## Getting Help

If you can't find what you're looking for:

1. Check the [README](../README.md) for overview
2. Try [Getting Started](GETTING_STARTED.md) for setup help
3. Review [Troubleshooting sections](GETTING_STARTED.md#troubleshooting)
4. Read [Architecture](ARCHITECTURE.md) for system understanding
5. Check [Testing](TESTING.md) for validation procedures

## Documentation Feedback

To improve documentation:
- Note unclear sections
- Suggest missing topics
- Report errors or outdated information
- Propose new examples or use cases
