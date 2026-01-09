# STM32 Multi-Agent Architecture Specification

## Overview

This document describes a comprehensive multi-agent architecture for STM32 embedded development assistance. The system uses specialized agents to handle different domains of embedded systems expertise, coordinated by a triage agent.

## Architecture Diagram

```
                                    ┌─────────────────┐
                                    │   User Query    │
                                    └────────┬────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │       TRIAGE AGENT           │
                              │  - Query classification      │
                              │  - Domain detection          │
                              │  - Agent routing             │
                              │  - Result synthesis          │
                              └──────────────┬───────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
         ┌──────────┴──────────┐  ┌─────────┴─────────┐  ┌──────────┴──────────┐
         │                     │  │                   │  │                     │
    ┌────┴────┐          ┌────┴────┐           ┌────┴────┐          ┌────┴────┐
    │FIRMWARE │          │PERIPH   │           │HARDWARE │          │SECURITY │
    │  CORE   │◄────────►│ COMM    │◄─────────►│ DESIGN  │◄────────►│         │
    └────┬────┘          └────┬────┘           └────┬────┘          └────┬────┘
         │                    │                     │                    │
    ┌────┴────┐          ┌────┴────┐           ┌────┴────┐          ┌────┴────┐
    │PERIPH   │          │PERIPH   │           │ POWER   │          │ SAFETY  │
    │ ANALOG  │◄────────►│GRAPHICS │◄─────────►│MANAGEMENT│◄────────►│  CERT   │
    └────┬────┘          └────┬────┘           └────┬────┘          └────┴────┘
         │                    │                     │
         │              ┌─────┴─────┐               │
         └─────────────►│BOOTLOADER │◄──────────────┘
                        │PROGRAMMING│
                        └─────┬─────┘
                              │
                        ┌─────┴─────┐
                        │   DEBUG   │
                        └───────────┘
```

## Agent Hierarchy and Routing

### 1. Triage Agent (Master Router)

**Location:** `.claude/agents/triage.md`

**Responsibilities:**
- Analyze incoming queries for technical domain
- Route to appropriate specialized agent(s)
- Coordinate multi-agent responses
- Synthesize final unified response

**Routing Decision Tree:**
```
Query Analysis
    │
    ├─► Single Domain?
    │       │
    │       ├─► YES: Direct dispatch to specialist
    │       │
    │       └─► NO: Multi-domain handling
    │               │
    │               ├─► Independent sub-queries?
    │               │       └─► Parallel dispatch
    │               │
    │               └─► Dependent sub-queries?
    │                       └─► Sequential chain
    │
    └─► Ambiguous?
            └─► Request clarification
```

### 2. Routing Keywords Matrix

| Keywords/Patterns | Primary Agent | Secondary Agents |
|-------------------|---------------|------------------|
| HAL_, LL_, RCC, NVIC, timer, DMA, interrupt | firmware-core | - |
| USART, SPI, I2C, CAN, USB, Ethernet | peripheral-comm | firmware-core |
| ADC, DAC, analog, sensor, audio, DFSDM | peripheral-analog | firmware-core |
| LTDC, display, DMA2D, camera, GUI | peripheral-graphics | firmware-core |
| PCB, EMC, crystal, decoupling, layout | hardware-design | - |
| secure boot, encryption, TrustZone, RNG | security | firmware-core |
| IEC 61508, SIL, Class B, safety | safety-certification | security |
| low-power, sleep, stop, standby | power-management | firmware-core |
| bootloader, IAP, firmware update, DFU | bootloader-programming | security |
| debug, HardFault, SWD, trace | debug | firmware-core |

### 3. Handoff Protocol

When agents need to collaborate:

```json
{
  "handoff": {
    "from_agent": "peripheral-comm",
    "to_agent": "firmware-core",
    "reason": "Clock configuration needed for baud rate",
    "context": {
      "peripheral": "USART1",
      "required_baud": 115200,
      "current_issue": "Baud rate calculation incorrect"
    },
    "findings_so_far": [
      "USART configuration is correct",
      "Clock source may be misconfigured"
    ]
  }
}
```

## Agent Specification Template

Each agent follows this structure:

```markdown
# Agent Name

## Description
Brief description for agent selection

<examples>
- Example query 1
- Example query 2
</examples>

<triggers>
keyword1, keyword2, keyword3
</triggers>

<excludes>
Queries to route elsewhere -> other-agent
</excludes>

<collaborates_with>
- other-agent: When collaboration needed
</collaborates_with>

---

[Full system prompt content]
```

### Agent Directory Structure

```
.claude/
└── agents/
    ├── triage.md              # Master router
    ├── firmware-core.md       # Cortex-M, HAL/LL, timers
    ├── peripheral-comm.md     # UART, SPI, I2C, CAN, USB
    ├── peripheral-analog.md   # ADC, DAC, audio
    ├── peripheral-graphics.md # Display, camera, DMA2D
    ├── hardware-design.md     # PCB, EMC, thermal
    ├── security.md            # Secure boot, crypto
    ├── safety-certification.md # IEC 61508, Class B
    ├── power-management.md    # Low-power modes
    ├── bootloader-programming.md # IAP, DFU
    └── debug.md               # Fault analysis, SWD
```

## Inter-Agent Communication

### 1. Shared Context Structure

```python
class AgentContext:
    original_query: str
    detected_domains: List[str]
    stm32_family: Optional[str]  # F4, H7, L4, etc.
    complexity: str  # simple, medium, complex
    related_findings: List[Finding]

class Finding:
    agent: str
    confidence: float  # 0.0-1.0
    answer: str
    code_snippets: List[str]
    references: List[str]
    follow_up_needed: List[str]
```

### 2. Communication Patterns

#### Pattern A: Parallel Dispatch
For independent sub-questions:

```
User: "How do I configure SPI DMA and optimize power consumption?"

Triage Analysis:
├── SPI DMA → peripheral-comm
└── Power optimization → power-management

Execution: Run both agents in parallel
Synthesis: Combine responses
```

#### Pattern B: Sequential Chain
For dependent questions:

```
User: "Set up secure OTA firmware updates"

Sequence:
1. security → Secure boot architecture
2. bootloader-programming → Update mechanism (uses security output)
3. peripheral-comm → Communication protocol details
```

#### Pattern C: Iterative Refinement
For debugging scenarios:

```
User: "USB not enumerating"

Iteration:
1. peripheral-comm → Initial USB diagnosis
   └─► Finding: "Check clock configuration"
2. firmware-core → Verify USB clock (48MHz)
   └─► Finding: "Clock OK, check hardware"
3. hardware-design → USB layout review
```

### 3. Result Aggregation Strategy

```markdown
## Summary
[Unified answer addressing the core question]

## Detailed Analysis

### [Domain 1] - from {agent-name}
[Agent 1's findings with confidence level]

### [Domain 2] - from {agent-name}
[Agent 2's findings with confidence level]

## Integrated Solution
[How the pieces fit together]

## Code Example
```c
// Combined/integrated code
```

## Cross-Domain Considerations
[Potential interactions between domains]

## References
[Consolidated reference list from all agents]
```

## Claude Code Integration

### Using the Task Tool with Agents

```python
# Example: Invoking specialized agent
Task(
    description="Configure STM32H7 SPI with DMA for high-speed data transfer",
    subagent_type="peripheral-comm"  # Routes to peripheral-comm.md
)

# Example: Multi-agent query
Task(
    description="Analyze HardFault in USB communication code",
    subagent_type="debug"  # Primary agent
    # Will auto-handoff to peripheral-comm if needed
)
```

### Foreground vs Background Execution

| Scenario | Execution Mode | Rationale |
|----------|---------------|-----------|
| Simple single-domain query | Foreground | Quick response expected |
| Code generation | Foreground | User waiting for code |
| Multi-file analysis | Background | Long-running task |
| Documentation generation | Background | Non-blocking |
| Build/test verification | Background | Can be interrupted |

### Decision Matrix

```python
def choose_execution_mode(query):
    if query.is_simple_lookup:
        return "foreground"
    if query.requires_code_generation:
        return "foreground"
    if query.spans_multiple_files > 5:
        return "background"
    if query.involves_external_tools:
        return "background"
    return "foreground"
```

## Multi-Domain Query Handling

### Example: Complex Query Processing

**Query:** "I'm designing a battery-powered STM32L4 device with USB-C and need secure firmware updates. Help me with the architecture."

**Triage Analysis:**
```
Domains detected:
1. Power management (battery-powered, L4)
2. Communication (USB-C)
3. Security (secure firmware updates)
4. Bootloader (firmware updates)
5. Hardware (USB-C design)

Complexity: Complex (5 domains)
Strategy: Sequential with parallel sub-tasks
```

**Execution Plan:**
```
Phase 1 (Parallel):
├── power-management: L4 low-power architecture
├── hardware-design: USB-C circuit design
└── security: Secure update requirements

Phase 2 (Sequential, depends on Phase 1):
├── bootloader-programming: Update mechanism design
└── peripheral-comm: USB implementation details

Phase 3 (Synthesis):
└── triage: Combine all findings into cohesive architecture
```

## Agent Tool Access

### Common Tools (All Agents)
- Read: Access documentation and code
- Grep: Search codebase
- Glob: Find files
- Edit: Modify code
- Bash: Run commands (build, flash)

### Agent-Specific Tool Usage

| Agent | Primary Tools | Special Access |
|-------|--------------|----------------|
| firmware-core | Read, Edit, Bash (build) | HAL/LL source |
| peripheral-comm | Read, Edit | Protocol analyzers |
| peripheral-analog | Read, Edit | Calibration data |
| peripheral-graphics | Read, Edit, Bash | Image tools |
| hardware-design | Read, WebFetch | Component datasheets |
| security | Read, Edit | Crypto tools |
| safety-certification | Read, Edit | Test harnesses |
| power-management | Read, Edit, Bash | Power profilers |
| bootloader-programming | Read, Edit, Bash | Flash tools |
| debug | Read, Bash | Debug tools, GDB |

## Performance Optimization

### Caching Strategy
```
Cache Layer 1: Query classification results (60s TTL)
Cache Layer 2: Agent responses for common queries (5min TTL)
Cache Layer 3: Code snippets and templates (persistent)
```

### Parallel Execution
```
Maximum parallel agents: 3
Timeout per agent: 30 seconds
Total multi-agent timeout: 60 seconds
```

## Error Handling

### Agent Failure Recovery
```python
def handle_agent_failure(agent, error):
    if error.is_timeout:
        return retry_with_simplified_query(agent)
    if error.is_capability_mismatch:
        return reroute_to_alternate_agent(agent)
    if error.is_ambiguous:
        return request_user_clarification()
    return graceful_degradation(agent)
```

### Conflict Resolution
When agents provide conflicting information:
1. Prefer more specialized agent for domain
2. Prefer agent with higher confidence score
3. Present both options with trade-offs to user

## Example Session Flow

```
User: "My STM32F4 ADC readings are noisy and the USB CDC drops data"

Triage Agent:
├── Detects: ADC noise (analog) + USB issues (comm)
├── Routes: peripheral-analog (primary), peripheral-comm (secondary)
└── Strategy: Parallel dispatch

Peripheral-Analog Agent:
├── Analyzes ADC configuration
├── Suggests: Sampling time, averaging, filtering
├── Finds: Potential clock interference
└── Handoff: firmware-core for clock check

Peripheral-Comm Agent:
├── Analyzes USB CDC setup
├── Suggests: Buffer sizes, flow control
├── Finds: DMA configuration issue
└── Handoff: firmware-core for DMA priorities

Firmware-Core Agent (via handoffs):
├── Reviews clock tree
├── Reviews DMA priorities
└── Finds: ADC and USB competing for same DMA

Triage Agent (synthesis):
└── Combines findings into unified solution
    ├── ADC noise: Increase sampling time + averaging
    ├── USB drops: Adjust DMA priorities
    └── Root cause: Resource conflict resolution
```

## Deployment Configuration

### Agent Registration
```yaml
# .claude/agents/config.yaml
agents:
  - name: triage
    file: triage.md
    role: router
    priority: 0

  - name: firmware-core
    file: firmware-core.md
    role: specialist
    domains: [cortex-m, hal, ll, timer, dma, nvic, rcc]

  - name: peripheral-comm
    file: peripheral-comm.md
    role: specialist
    domains: [uart, spi, i2c, can, usb, ethernet]
    collaborates: [firmware-core, power-management]

  # ... additional agents
```

## Metrics and Monitoring

### Quality Metrics
- **Routing Accuracy:** Did the right agent handle the query?
- **Response Completeness:** Was follow-up needed?
- **Agent Utilization:** Balanced workload across agents?
- **Resolution Time:** Single vs multi-agent query times?

### Logging
```
[TRIAGE] Query: "Configure SPI DMA"
[TRIAGE] Domains: [peripheral-comm]
[TRIAGE] Routing to: peripheral-comm
[PERIPH-COMM] Processing query...
[PERIPH-COMM] Confidence: 0.95
[PERIPH-COMM] Handoff needed: firmware-core (DMA setup)
[FIRMWARE] Processing handoff...
[TRIAGE] Synthesizing response...
[TRIAGE] Response delivered (1.2s)
```

---

## Quick Reference

### Agent Selection Guide

| "I want to..." | Primary Agent |
|----------------|---------------|
| Configure a peripheral | firmware-core or specific peripheral agent |
| Debug a crash | debug |
| Optimize power | power-management |
| Add encryption | security |
| Update firmware | bootloader-programming |
| Design a PCB | hardware-design |
| Meet safety standards | safety-certification |
| Set up communication | peripheral-comm |
| Process analog signals | peripheral-analog |
| Display graphics | peripheral-graphics |

### Emergency Contacts (Handoff Shortcuts)

- Clock issues → firmware-core
- DMA issues → firmware-core
- Signal quality → hardware-design
- Certification questions → safety-certification
- Any security concern → security
