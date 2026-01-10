---
name: stm32-setup
description: Set up STM32 MCP documentation server - installs dependencies and configures your project
---

# STM32 MCP Setup Command

Interactive setup for the STM32 documentation server. Handles dependency installation and project configuration.

## Usage

```
/stm32-setup                 Full setup (install deps, check MCP, update CLAUDE.md)
/stm32-setup --status        Show current installation status
/stm32-setup --update-claude Only update project CLAUDE.md
/stm32-setup --force-db      Force re-download of database
```

## Instructions for the Assistant

When the user runs `/stm32-setup`, follow these steps IN ORDER:

### Step 0: Detect Existing Agent Installations (CRITICAL - DO THIS FIRST)

**IMPORTANT:** Before installing anything, you MUST check for existing agent installations in BOTH locations to avoid duplicate installs.

**Directory Definitions:**
- **LOCAL** = `./.claude/agents/` (project directory, relative to cwd)
- **GLOBAL** = `~/.claude/agents/` (user's home directory)

**Detection Steps:**

1. Check LOCAL installation first:
   ```bash
   ls -la ./.claude/agents/*.md 2>/dev/null | head -5
   ```

2. Check GLOBAL installation:
   ```bash
   ls -la ~/.claude/agents/*.md 2>/dev/null | head -5
   ```

3. Look for STM32-specific agents (router.md, firmware.md, debug.md, etc.):
   ```bash
   ls ./.claude/agents/router.md ~/.claude/agents/router.md 2>/dev/null
   ```

**Decision Matrix:**

| Local Exists? | Global Exists? | Action |
|---------------|----------------|--------|
| YES | (any) | Report "Agents installed locally" → Skip to Step 2 (MCP check) |
| NO | YES | Report "Agents installed globally" → Ask if user wants local copy too |
| NO | NO | Proceed with installation (Step 1) |

**Priority Rule:** Local installation takes precedence. If agents exist locally, DO NOT install globally. This prevents cross-project contamination.

**Example Output:**
```
Checking for existing STM32 agent installations...
  Local (./.claude/agents/): 16 agents found ✓
  Global (~/.claude/agents/): 0 agents found

Status: Agents already installed locally. Skipping installation.
```

### Step 1: Check and Install uvx/uv

**CRITICAL: Do this FIRST before anything else.**

1. Check if uvx is available:
   ```bash
   command -v uvx
   ```

2. If uvx is NOT found, install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. After installation, update PATH for current session:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. Verify installation worked:
   ```bash
   ~/.local/bin/uvx --version
   ```

5. If uv installation fails, try pip fallback:
   ```bash
   pip install uv
   ```

6. If all uv methods fail, install the package directly via pip:
   ```bash
   pip install git+https://github.com/creativec09/stm32.git
   ```
   Then tell the user: "Installed via pip. The MCP server will use `python -m mcp_server` instead of uvx."

7. **After installing uvx**, tell the user:
   ```
   ✓ uvx installed successfully!

   ACTION REQUIRED: Please restart Claude Code to connect the MCP server.

   After restarting, run /stm32-setup again to complete configuration.
   ```
   Then STOP - don't continue to other steps until they restart.

### Step 2: Check MCP Server Connection

Only proceed here if uvx was already installed (not just installed in Step 1).

1. Try to read the `stm32://status` resource
2. If connection fails with error, diagnose:
   - "spawn uvx ENOENT" → uvx not in PATH, go back to Step 1
   - "ECONNREFUSED" → MCP server not starting, check logs
   - Other errors → report to user

3. If status shows "setup_required" or database is empty:
   - The database will auto-download on first query
   - Or user can wait for it to initialize

### Step 3: Verify Database

1. Call `mcp__stm32-docs__list_peripherals()` to verify the database works
2. If it returns results, report:
   - Number of peripherals documented
   - Number of chunks indexed
3. If it fails, the database may still be downloading - tell user to wait or try again

### Step 4: Update Project CLAUDE.md

1. Check if a CLAUDE.md exists in the current project directory
2. If it exists, check for existing STM32 section (look for "## STM32 Development Instructions")
3. If no STM32 section exists, append the template content below
4. If it doesn't exist, create it with STM32 instructions

### Step 5: Show Summary

Report to the user (adjust based on what was found in Step 0):

**If agents found LOCALLY:**
```
STM32 MCP Setup Complete
========================

Dependencies:
  ✓ uvx installed at ~/.local/bin/uvx

MCP Server:
  ✓ Connected to stm32-docs

Database:
  ✓ 13,815 document chunks indexed
  ✓ 80 source documentation files

Agents: 16 (LOCAL installation)
  Location: ./.claude/agents/
  router, triage, firmware, firmware-core, debug, bootloader,
  bootloader-programming, peripheral-comm, peripheral-analog,
  peripheral-graphics, power, power-management, safety,
  safety-certification, security, hardware-design
```

**If agents found GLOBALLY (no local):**
```
STM32 MCP Setup Complete
========================

Dependencies:
  ✓ uvx installed at ~/.local/bin/uvx

MCP Server:
  ✓ Connected to stm32-docs

Database:
  ✓ 13,815 document chunks indexed
  ✓ 80 source documentation files

Agents: 16 (GLOBAL installation)
  Location: ~/.claude/agents/
  Note: These agents are shared across all projects.
  Tip: Copy to ./.claude/agents/ for project-local customization.
```

**If no agents found (fresh install):**
```
STM32 MCP Setup Complete
========================

Dependencies:
  ✓ uvx installed at ~/.local/bin/uvx

MCP Server:
  ✓ Connected to stm32-docs

Database:
  ✓ 13,815 document chunks indexed
  ✓ 80 source documentation files

Agents Installed: 16 → ~/.claude/agents/ (global)
  router, triage, firmware, firmware-core, debug, bootloader,
  bootloader-programming, peripheral-comm, peripheral-analog,
  peripheral-graphics, power, power-management, safety,
  safety-certification, security, hardware-design

Commands Available:
  /stm32 <query>        - Search documentation
  /stm32-init <periph>  - Get initialization code
  /stm32-hal <func>     - Look up HAL function
  /stm32-debug <issue>  - Troubleshoot problems
  /stm32-setup          - This setup command

Quick Start:
  Try: /stm32 How do I configure UART with DMA on STM32F4?
```

## Troubleshooting Decision Tree

If something fails, follow this logic:

```
MCP Connection Failed?
├── "spawn uvx ENOENT" or "uvx not found"
│   └── Install uvx (Step 1) → Tell user to restart Claude Code
├── "ECONNREFUSED"
│   └── Check if Python/pip issues → Try pip install fallback
├── "Authentication" or "404" errors
│   └── Check GitHub access → Repo is public, should work
└── Database empty or missing
    └── Will auto-download on first query, or run /stm32-setup --force-db

Agent Detection Issues?
├── "Agents not found" but they exist
│   └── Check BOTH locations:
│       ├── Local: ./.claude/agents/
│       └── Global: ~/.claude/agents/
├── Duplicate agents (local AND global)
│   └── Local takes priority - this is fine, but you can remove global copies if desired
├── Wrong agents loading
│   └── Local agents override global - check ./.claude/agents/ first
└── Agents installed to wrong location
    └── Move from ~/.claude/agents/ to ./.claude/agents/ for project-local
```

## Local vs Global Agent Priority

Claude Code checks for agents in this order:
1. **Local first**: `./.claude/agents/` (project directory)
2. **Global fallback**: `~/.claude/agents/` (user home)

**Best Practice:**
- Use LOCAL (`./.claude/agents/`) for project-specific agent customizations
- Use GLOBAL (`~/.claude/agents/`) only when you want agents shared across ALL projects
- If both exist, LOCAL wins - this is intentional for project isolation

**To migrate from global to local:**
```bash
mkdir -p ./.claude/agents
cp ~/.claude/agents/router.md ./.claude/agents/
# ... copy other agents you want locally
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `mcp__stm32-docs__list_peripherals` | Verify database is working |
| Read resource `stm32://status` | Get server status |
| Read resource `stm32://health` | Check server health |

## CLAUDE.md Template Content

When updating the user's project CLAUDE.md, add the following content:

```markdown
## STM32 Development Instructions

This project uses the STM32 MCP documentation server for embedded development assistance.

### CRITICAL: Always Use Agents, Never Direct MCP Calls

When answering STM32 questions, NEVER call MCP tools directly in the main session. This burns context with hundreds of lines of raw results. Instead:

1. **ALWAYS use the Task tool** to invoke the `router` agent (or appropriate specialist agent)
2. The agent handles MCP queries in its own context window
3. The agent returns a concise, summarized answer
4. This keeps the main session context clean and efficient

**Example - Correct Approach:**
```
User: "How do I configure UART with DMA?"

Claude: [Uses Task tool to invoke router agent]
  -> Router agent calls mcp__stm32-docs__get_init_sequence("UART", "DMA")
  -> Router agent summarizes the results
  -> Returns: "Here's how to configure UART with DMA: [concise summary with code]"
```

**Example - WRONG Approach (Never Do This):**
```
User: "How do I configure UART with DMA?"

Claude: [Directly calls mcp__stm32-docs__get_init_sequence]
  -> Returns 500+ lines of raw documentation
  -> Burns main session context
  -> User has to scroll through walls of text
```

### Agent Entry Points

| Agent | When to Use |
|-------|-------------|
| `router` | **DEFAULT** - Routes to the right specialist, handles general queries |
| `firmware` | General firmware, HAL/LL, timers, interrupts |
| `peripheral-comm` | UART, SPI, I2C, CAN, USB questions |
| `peripheral-analog` | ADC, DAC, OPAMP questions |
| `debug` | Debugging, HardFault, troubleshooting |
| `power` | Low power modes, battery optimization |
| `bootloader` | Bootloader, firmware updates, IAP |
| `security` | Secure boot, TrustZone, encryption |
| `safety` | Safety-critical, IEC 61508, ISO 26262 |

### How to Invoke Agents

Use the Task tool with this pattern:
```
Task: "router" agent
Input: [user's STM32 question]
```

The router agent will:
1. Analyze the query
2. Either handle it directly or delegate to a specialist
3. Query MCP tools as needed
4. Return a summarized, actionable answer

### Available MCP Tools (For Agent Use Only)

| Tool | When to Use |
|------|-------------|
| `mcp__stm32-docs__search_stm32_docs` | General documentation search |
| `mcp__stm32-docs__get_peripheral_docs` | Peripheral-specific documentation |
| `mcp__stm32-docs__get_code_examples` | Find working code examples |
| `mcp__stm32-docs__get_register_info` | Register and bit field details |
| `mcp__stm32-docs__lookup_hal_function` | HAL/LL function documentation |
| `mcp__stm32-docs__troubleshoot_error` | Debug issues and errors |
| `mcp__stm32-docs__get_init_sequence` | Peripheral initialization code |
| `mcp__stm32-docs__get_clock_config` | Clock configuration examples |
| `mcp__stm32-docs__compare_peripheral_options` | Compare peripherals/modes |
| `mcp__stm32-docs__get_migration_guide` | Migration between STM32 families |
| `mcp__stm32-docs__get_interrupt_code` | Interrupt handling examples |
| `mcp__stm32-docs__get_dma_code` | DMA configuration examples |
| `mcp__stm32-docs__get_low_power_code` | Low power mode examples |
| `mcp__stm32-docs__get_callback_code` | HAL callback implementations |
| `mcp__stm32-docs__get_init_template` | Complete init templates |
| `mcp__stm32-docs__list_peripherals` | List documented peripherals |

### Available Slash Commands

- `/stm32 <query>` - Search STM32 documentation
- `/stm32-init <peripheral>` - Get initialization code
- `/stm32-hal <function>` - Look up HAL function
- `/stm32-debug <issue>` - Troubleshoot an issue
- `/stm32-setup` - Run setup and show status

### Available STM32 Agents

| Agent | Purpose |
|-------|---------|
| router | Query classification and routing |
| triage | Initial query analysis |
| firmware | General firmware development |
| firmware-core | Core HAL/LL, timers, DMA, interrupts |
| debug | Debugging and troubleshooting |
| bootloader | Bootloader development |
| bootloader-programming | Bootloader protocols |
| peripheral-comm | UART, SPI, I2C, CAN, USB |
| peripheral-analog | ADC, DAC, OPAMP, comparators |
| peripheral-graphics | LTDC, DMA2D, DCMI, TouchGFX |
| power | Power optimization |
| power-management | Sleep, Stop, Standby modes |
| safety | Safety-critical development |
| safety-certification | IEC 61508, ISO 26262 |
| security | Secure boot, TrustZone, crypto |
| hardware-design | PCB design, EMC, thermal |

### Best Practices

1. **Always use agents** - Never call MCP tools directly in the main session
2. **Be specific in queries** - Include STM32 family, peripheral, and use case
3. **Let the router decide** - The router agent knows which specialist to use
4. **Trust agent summaries** - Agents condense documentation into actionable answers

### Quick Reference

For any STM32 question, use this pattern:
```
[Invoke Task tool with "router" agent and the user's question]
```

The router will handle everything - MCP queries, specialist delegation, and summarization.
```
