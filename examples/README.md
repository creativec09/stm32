# Configuration Examples

This directory contains example configuration files for the STM32 MCP Documentation Server.

## Files

### mcp.json.example
Example Claude Code MCP configuration for **local mode** (stdio transport).
Use this when running Claude Code on the same machine as the server.

**Recommended approach** - use Claude CLI:
```bash
claude mcp add stm32-docs -s user -- python -m mcp_server
```

**Manual approach** - copy config file:
```bash
# Copy to your Claude Code config directory
cp mcp.json.example ~/.claude.json  # Append to existing or create new
```

### mcp-network.json.example
Example Claude Code MCP configuration for **network mode** (HTTP/SSE transport).
Use this when accessing the server over Tailscale or other networks.

### config.env.example
Example environment configuration with common settings.
Copy to `.env` in the project root to customize behavior.

```bash
cp config.env.example ../.env
```

## Quick Setup

### For Local Development (Recommended)

1. Register with Claude CLI:
   ```bash
   claude mcp add stm32-docs -s user -- python -m mcp_server
   ```

2. Install the package:
   ```bash
   cd ..
   pip install -e .
   ```

3. Ingest documentation:
   ```bash
   stm32-ingest --source-dir ./markdowns
   ```

4. Start using with Claude Code

### For Network/Tailscale Access

1. Copy the environment config:
   ```bash
   cp config.env.example ../.env
   ```

2. Edit `.env` to set network mode:
   ```
   STM32_SERVER_MODE=network
   STM32_PORT=8765
   ```

3. Start the server:
   ```bash
   STM32_SERVER_MODE=network python -m mcp_server
   ```

4. Register on client machines:
   ```bash
   claude mcp add stm32-docs -s user --type sse --url "http://YOUR_TAILSCALE_IP:8765/sse"
   ```

## Environment Variables

All configuration options can be set via environment variables with the `STM32_` prefix.
See the main [.env.example](../.env.example) for a complete list of options.
