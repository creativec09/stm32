# Agent Execution Specifications for STM32 Development

## Comprehensive Guide to Claude Code Task Tool Execution Patterns

---

## Table of Contents

1. [Overview](#1-overview)
2. [Foreground Execution Patterns](#2-foreground-execution-patterns)
3. [Background Execution Patterns](#3-background-execution-patterns)
4. [Model Selection Strategy](#4-model-selection-strategy)
5. [Parallelization Patterns](#5-parallelization-patterns)
6. [Error Handling and Recovery](#6-error-handling-and-recovery)
7. [Execution Decision Matrix](#7-execution-decision-matrix)
8. [Implementation Examples](#8-implementation-examples)

---

## 1. Overview

### 1.1 Task Tool Capabilities

The Claude Code Task tool provides the following execution parameters:

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `subagent_type` | `code`, `research`, `review`, `custom` | Specialized agent behavior |
| `run_in_background` | `true`, `false` | Async vs sync execution |
| Model Selection | `opus`, `sonnet`, `haiku` | Reasoning capability level |
| Agent ID | UUID | Resume/track agent state |

### 1.2 Core Principles

1. **Right-Size Execution**: Match execution mode to task requirements
2. **Cost Efficiency**: Use appropriate model tier for task complexity
3. **User Experience**: Prioritize responsiveness for interactive tasks
4. **Reliability**: Build in fault tolerance and recovery mechanisms

---

## 2. Foreground Execution Patterns

### 2.1 When to Use Synchronous Execution

Foreground (synchronous) execution is appropriate when:

- **User is waiting for immediate response**
- **Task duration < 30 seconds expected**
- **Interactive feedback loop required**
- **Results needed before next user action**
- **Simple, well-defined scope**

### 2.2 Foreground Execution Categories

#### Category F1: Quick Lookups (< 5 seconds)

```
Trigger Conditions:
- Single-fact retrieval from documentation
- Register value lookups
- Pin configuration queries
- Peripheral capability checks

Execution Config:
  model: haiku
  run_in_background: false
  timeout: 10000ms
  subagent_type: research

Examples:
- "What is the base address of TIM1?"
- "Which pins support SPI3 on STM32H723?"
- "What is the max clock speed for USART1?"
```

**STM32 Use Cases:**
| Query Type | Expected Time | Model |
|------------|---------------|-------|
| Register address lookup | 1-3s | Haiku |
| Pin alternate function | 2-4s | Haiku |
| Clock constraint check | 2-4s | Haiku |
| Peripheral availability | 1-2s | Haiku |

#### Category F2: Code Generation with Feedback (10-30 seconds)

```
Trigger Conditions:
- User needs to review/modify generated code
- Interactive refinement expected
- Single peripheral initialization
- Template-based generation

Execution Config:
  model: sonnet
  run_in_background: false
  timeout: 60000ms
  subagent_type: code

Examples:
- "Generate USART2 initialization for 115200 baud"
- "Create a PWM output on TIM3 CH1"
- "Initialize ADC1 for single conversion mode"
```

**Feedback Loop Pattern:**
```
User Request --> [Sonnet Agent] --> Generated Code
                                          |
                                          v
                                    User Review
                                          |
                            +-------------+-------------+
                            |                           |
                            v                           v
                        Approve                     Request Changes
                            |                           |
                            v                           v
                        Complete              [Refinement Agent]
                                                       |
                                                       v
                                              Updated Code
```

#### Category F3: Real-time Validation (5-15 seconds)

```
Trigger Conditions:
- User submitted code for review
- Configuration validation needed
- Quick compliance check
- Error explanation required

Execution Config:
  model: sonnet
  run_in_background: false
  timeout: 30000ms
  subagent_type: review

Examples:
- "Check if this clock configuration is valid"
- "Validate my DMA setup for ADC"
- "Is this interrupt priority scheme correct?"
```

### 2.3 Timeout Strategies for Foreground Tasks

```
Timeout Hierarchy:
+------------------+------------------+------------------+
| Level 1          | Level 2          | Level 3          |
| Quick Timeout    | Standard Timeout | Extended Timeout |
+------------------+------------------+------------------+
| 10 seconds       | 30 seconds       | 120 seconds      |
| Lookups          | Code gen         | Complex analysis |
| Simple queries   | Validation       | Multi-file review|
+------------------+------------------+------------------+

Timeout Handling:
- Level 1 timeout -> Retry with Level 2
- Level 2 timeout -> Offer background execution
- Level 3 timeout -> Require background execution
```

### 2.4 User Interaction Requirements

**Interactive Response Protocol:**
```
1. Acknowledgment Phase (immediate)
   - Confirm task receipt
   - Indicate expected duration
   - Show progress indicator if > 5s expected

2. Processing Phase (variable)
   - Stream partial results when possible
   - Provide status updates for long operations
   - Allow cancellation

3. Completion Phase (final)
   - Present results clearly
   - Offer refinement options
   - Suggest next steps
```

---

## 3. Background Execution Patterns

### 3.1 When to Use Async/Background Execution

Background execution is appropriate when:

- **Task duration > 2 minutes expected**
- **No immediate user interaction needed**
- **Large-scale analysis required**
- **User can continue other work**
- **Resource-intensive operations**

### 3.2 Background Execution Categories

#### Category B1: Full Codebase Analysis (5-30 minutes)

```
Trigger Conditions:
- Analyzing entire project structure
- Cross-file dependency mapping
- Comprehensive code review
- Documentation generation

Execution Config:
  model: opus (for synthesis), sonnet (for analysis)
  run_in_background: true
  timeout: 600000ms (10 minutes per phase)
  subagent_type: research

Examples:
- "Analyze all peripheral usage across the project"
- "Generate complete API documentation"
- "Find all potential memory safety issues"
```

**Output File Strategy:**
```
Project Root/
├── .stm32-agent/
│   ├── analysis/
│   │   ├── peripheral_map.json      # Discovered peripheral usage
│   │   ├── dependency_graph.json    # File dependencies
│   │   ├── code_metrics.json        # Complexity, coverage
│   │   └── analysis_report.md       # Human-readable summary
│   ├── logs/
│   │   ├── agent_{id}_progress.log  # Real-time progress
│   │   └── agent_{id}_errors.log    # Error capture
│   └── state/
│       └── agent_{id}_checkpoint.json # Resumption state
```

#### Category B2: Documentation Indexing (10-60 minutes)

```
Trigger Conditions:
- Building searchable documentation index
- Processing new reference manuals
- Creating embedding vectors
- Cross-reference generation

Execution Config:
  model: sonnet
  run_in_background: true
  timeout: 600000ms
  subagent_type: research

Examples:
- "Index all STM32H7 reference manual sections"
- "Build peripheral cross-reference database"
- "Process and chunk new application notes"
```

#### Category B3: Multi-File Refactoring (5-20 minutes)

```
Trigger Conditions:
- Renaming across codebase
- API migration
- Style standardization
- Pattern replacement

Execution Config:
  model: sonnet
  run_in_background: true
  timeout: 300000ms
  subagent_type: code

Examples:
- "Update all HAL calls to use new naming convention"
- "Migrate from HAL to LL for all timer code"
- "Add error handling to all peripheral init functions"
```

### 3.3 Output File Monitoring Strategies

#### Strategy 1: Progress File Watching

```python
# Monitor pattern for background tasks
monitoring_config = {
    "progress_file": ".stm32-agent/logs/agent_{id}_progress.log",
    "poll_interval_ms": 5000,
    "notification_events": [
        "phase_complete",    # Major milestone reached
        "error_encountered", # Non-fatal error
        "user_input_needed", # Requires interaction
        "task_complete"      # Final completion
    ]
}
```

**Progress File Format:**
```json
{
  "agent_id": "abc-123",
  "task": "codebase_analysis",
  "started_at": "2026-01-08T10:00:00Z",
  "current_phase": "peripheral_scanning",
  "phases_complete": 2,
  "phases_total": 5,
  "files_processed": 47,
  "files_total": 156,
  "current_file": "src/drivers/usart.c",
  "errors": [],
  "warnings": ["Deprecated HAL function in tim.c:234"]
}
```

#### Strategy 2: Checkpoint-Based Monitoring

```
Checkpoint Events:
+------------------+------------------+------------------+
| Checkpoint Type  | Trigger          | Contains         |
+------------------+------------------+------------------+
| INIT             | Task started     | Config, scope    |
| PROGRESS         | % complete       | Partial results  |
| PHASE            | Phase change     | Phase summary    |
| ERROR            | Error occurred   | Error details    |
| COMPLETE         | Task finished    | Full results     |
+------------------+------------------+------------------+
```

#### Strategy 3: Result Aggregation Pattern

```
Background Agent Output Structure:

results/
├── summary.md              # Executive summary (read first)
├── detailed_findings.json  # Machine-readable details
├── code_changes/           # Generated/modified code
│   ├── change_001.patch
│   └── change_002.patch
├── recommendations/        # Suggested improvements
│   └── priority_actions.md
└── metadata.json           # Execution stats, timing
```

### 3.4 Long-Running Task Scenarios

#### Scenario: Complete HAL Migration

```
Task: Migrate STM32F4 project to STM32H7

Execution Plan:
Phase 1: Analysis (Background, Opus)
  - Identify all F4-specific code
  - Map peripheral differences
  - Document incompatibilities
  Duration: 10-15 minutes

Phase 2: Planning (Background, Opus)
  - Generate migration roadmap
  - Create dependency order
  - Identify required manual changes
  Duration: 5-10 minutes

Phase 3: Automated Migration (Background, Sonnet)
  - Apply automated transformations
  - Update header includes
  - Modify clock configurations
  Duration: 15-30 minutes

Phase 4: Validation (Background, Sonnet)
  - Static analysis
  - Compile checks
  - Generate test plan
  Duration: 5-10 minutes

Total Expected Duration: 35-65 minutes
User Checkpoints: After each phase
```

---

## 4. Model Selection Strategy

### 4.1 Model Capability Matrix

| Model | Strengths | Limitations | Cost Factor |
|-------|-----------|-------------|-------------|
| **Opus** | Complex reasoning, architecture design, nuanced analysis | Slower, higher cost | 15x base |
| **Sonnet** | Balanced performance, code generation, general tasks | Less deep reasoning | 3x base |
| **Haiku** | Fast responses, simple queries, lookups | Limited complexity | 1x base |

### 4.2 When to Use Opus

**Opus-Appropriate Tasks:**

1. **System Architecture Design**
   ```
   - Designing multi-peripheral interaction systems
   - Planning memory layout for complex applications
   - Creating boot sequence with multiple dependencies
   - Safety-critical system design review
   ```

2. **Complex Debugging**
   ```
   - Race condition analysis
   - Memory corruption root cause analysis
   - Timing-sensitive issue diagnosis
   - Multi-peripheral interaction bugs
   ```

3. **Documentation Synthesis**
   ```
   - Creating comprehensive technical specifications
   - Synthesizing information from multiple reference manuals
   - Writing design rationale documents
   - Generating training materials
   ```

4. **Code Architecture Review**
   ```
   - Evaluating system design decisions
   - Identifying architectural anti-patterns
   - Suggesting refactoring strategies
   - Security vulnerability analysis
   ```

**Opus Selection Criteria:**
```
Use Opus when ANY of these apply:
- Task requires reasoning across 5+ documents
- Output requires nuanced judgment
- Failure cost is high (safety, security)
- Architectural decisions involved
- Novel problem without clear patterns
```

### 4.3 When to Use Sonnet

**Sonnet-Appropriate Tasks:**

1. **Standard Code Generation**
   ```
   - Peripheral initialization functions
   - Interrupt handlers
   - DMA configuration
   - Standard driver implementations
   ```

2. **Code Review and Validation**
   ```
   - Checking HAL compliance
   - Validating clock configurations
   - Reviewing interrupt priorities
   - Verifying DMA settings
   ```

3. **Documentation Retrieval and Summarization**
   ```
   - Finding relevant application notes
   - Summarizing reference manual sections
   - Extracting code examples
   - Answering "how-to" questions
   ```

4. **Refactoring Tasks**
   ```
   - Applying consistent patterns
   - Updating deprecated APIs
   - Adding error handling
   - Implementing coding standards
   ```

**Sonnet Selection Criteria:**
```
Use Sonnet when:
- Task has clear patterns to follow
- Standard code generation needed
- Moderate complexity analysis
- Quality matters but speed important
- Cost-performance balance needed
```

### 4.4 When to Use Haiku

**Haiku-Appropriate Tasks:**

1. **Quick Lookups**
   ```
   - Register addresses
   - Pin mappings
   - Clock frequencies
   - Peripheral base addresses
   ```

2. **Simple Transformations**
   ```
   - Format conversions
   - Simple code fixes
   - Syntax corrections
   - Comment generation
   ```

3. **Classification Tasks**
   ```
   - Categorizing user queries
   - Routing to specialized agents
   - Determining task complexity
   - Validating input format
   ```

4. **Repetitive Operations**
   ```
   - Batch file processing
   - Pattern matching
   - Simple validations
   - Status checks
   ```

**Haiku Selection Criteria:**
```
Use Haiku when:
- Single-fact retrieval
- Response time critical (< 2s)
- High-volume, low-complexity tasks
- Cost minimization important
- Task is well-defined and narrow
```

### 4.5 Cost/Performance Decision Tree

```
                        +------------------+
                        |  Incoming Task   |
                        +--------+---------+
                                 |
                    +------------+------------+
                    |                         |
              Complex?                   Simple?
                    |                         |
                    v                         v
         +------------------+       +------------------+
         | Multi-document?  |       | Single lookup?   |
         +--------+---------+       +--------+---------+
                  |                          |
         +--------+--------+         +-------+-------+
         |                 |         |               |
        Yes               No        Yes             No
         |                 |         |               |
         v                 v         v               v
      OPUS            SONNET      HAIKU          SONNET
   (15x cost)        (3x cost)  (1x cost)       (3x cost)


Cost Estimation Formula:
  estimated_cost = base_rate * model_factor * token_estimate

  where:
    model_factor = {opus: 15, sonnet: 3, haiku: 1}
    token_estimate = input_tokens + (output_tokens * 3)
```

### 4.6 Model Escalation Patterns

```
Escalation Triggers:
1. Haiku -> Sonnet
   - Answer confidence < 80%
   - Task complexity increased during execution
   - User requests more detail

2. Sonnet -> Opus
   - Multiple conflicting interpretations found
   - Safety/security implications identified
   - Architectural decisions required
   - User explicitly requests deeper analysis
```

---

## 5. Parallelization Patterns

### 5.1 When to Spawn Multiple Agents

**Parallel Execution Appropriate When:**

1. **Independent Subtasks**
   - Tasks have no data dependencies
   - Results can be merged post-completion
   - Failure of one doesn't block others

2. **Different Perspectives Needed**
   - Multiple analysis viewpoints
   - Cross-domain expertise required
   - Validation from different angles

3. **Time-Critical Operations**
   - User waiting for combined results
   - Sequential would exceed timeout
   - Parallel reduces total time significantly

### 5.2 Parallelization Patterns

#### Pattern P1: Fan-Out/Fan-In

```
                    +----------------+
                    |   Orchestrator |
                    +-------+--------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
        +---------+   +---------+   +---------+
        | Agent 1 |   | Agent 2 |   | Agent 3 |
        | (Clock) |   | (Power) |   | (Safety)|
        +----+----+   +----+----+   +----+----+
              |             |             |
              v             v             v
        +---------+   +---------+   +---------+
        | Result1 |   | Result2 |   | Result3 |
        +----+----+   +----+----+   +----+----+
              |             |             |
              +-------------+-------------+
                            |
                            v
                    +----------------+
                    |   Aggregator   |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Combined Report|
                    +----------------+
```

**Implementation:**
```python
parallel_task_config = {
    "pattern": "fan_out_fan_in",
    "agents": [
        {
            "name": "clock_analysis",
            "model": "sonnet",
            "task": "Analyze clock tree configuration",
            "output": "clock_analysis.json"
        },
        {
            "name": "power_analysis",
            "model": "sonnet",
            "task": "Analyze power consumption",
            "output": "power_analysis.json"
        },
        {
            "name": "safety_review",
            "model": "opus",
            "task": "Review safety compliance",
            "output": "safety_review.json"
        }
    ],
    "aggregator": {
        "model": "opus",
        "task": "Synthesize findings into unified report",
        "inputs": ["clock_analysis.json", "power_analysis.json", "safety_review.json"]
    }
}
```

#### Pattern P2: Speculative Execution

```
When outcome is uncertain, run multiple approaches in parallel:

                    +----------------+
                    |     Query      |
                    +-------+--------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
        +---------+   +---------+   +---------+
        | HAL     |   | LL      |   | Register|
        | Approach|   | Approach|   | Approach|
        +----+----+   +----+----+   +----+----+
              |             |             |
              +-------------+-------------+
                            |
                            v
                    +----------------+
                    |    Selector    |
                    | (Pick best or  |
                    |  present all)  |
                    +----------------+
```

**Use Cases:**
- Generate code using multiple abstraction levels
- Try different peripheral configurations
- Explore alternative implementations

#### Pattern P3: Pipeline with Parallel Stages

```
+--------+     +------------------+     +--------+
| Parse  | --> | Parallel         | --> | Merge  |
| Input  |     | Analysis Stage   |     | Results|
+--------+     +--------+---------+     +--------+
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     +--------+    +--------+    +--------+
     | File 1 |    | File 2 |    | File 3 |
     | Agent  |    | Agent  |    | Agent  |
     +--------+    +--------+    +--------+
```

**Use Case: Multi-File Code Analysis**
- Parse all files in parallel
- Analyze each file independently
- Merge findings for cross-file analysis

### 5.3 Result Aggregation Strategies

#### Strategy A1: Simple Merge

```
For independent results that don't conflict:

results = []
for agent in completed_agents:
    results.append(agent.output)

final_output = merge_json(results)
```

#### Strategy A2: Conflict Resolution

```
For potentially conflicting results:

def aggregate_with_resolution(results, resolver_model="opus"):
    conflicts = find_conflicts(results)
    if conflicts:
        resolution = resolver_agent.resolve(conflicts)
        results = apply_resolution(results, resolution)
    return merge(results)
```

#### Strategy A3: Weighted Combination

```
For results requiring quality assessment:

weights = {}
for agent_id, result in results.items():
    confidence = evaluate_confidence(result)
    relevance = evaluate_relevance(result, original_query)
    weights[agent_id] = confidence * relevance

final = weighted_merge(results, weights)
```

### 5.4 Dependency Handling Between Agents

#### Dependency Graph Definition

```yaml
agent_dependencies:
  clock_config:
    depends_on: []
    outputs: [clock_tree.json]

  peripheral_init:
    depends_on: [clock_config]
    inputs: [clock_tree.json]
    outputs: [peripheral_config.json]

  dma_setup:
    depends_on: [peripheral_init]
    inputs: [peripheral_config.json]
    outputs: [dma_config.json]

  interrupt_config:
    depends_on: [peripheral_init, dma_setup]
    inputs: [peripheral_config.json, dma_config.json]
    outputs: [interrupt_config.json]
```

#### Execution Order Resolution

```
Dependency Resolution Algorithm:

1. Build dependency graph
2. Identify independent tasks (no dependencies)
3. Execute independent tasks in parallel
4. As tasks complete, check for unblocked dependents
5. Execute newly unblocked tasks
6. Repeat until all complete

Execution Timeline:
T0: [clock_config] starts
T1: [clock_config] completes
T1: [peripheral_init] starts (unblocked)
T2: [peripheral_init] completes
T2: [dma_setup] starts (unblocked)
T3: [dma_setup] completes
T3: [interrupt_config] starts (all deps satisfied)
T4: [interrupt_config] completes
```

---

## 6. Error Handling and Recovery

### 6.1 Agent Failure Scenarios

| Failure Type | Cause | Detection | Impact |
|--------------|-------|-----------|--------|
| **Timeout** | Task exceeds time limit | Timer expiration | Partial results may exist |
| **Model Error** | API failure, rate limit | Exception/error response | No results |
| **Invalid Output** | Malformed response | Schema validation | Results unusable |
| **Context Overflow** | Too much input data | Token count check | Task cannot complete |
| **Logic Error** | Incorrect reasoning | Validation failure | Wrong results |
| **Resource Exhaustion** | Memory, disk full | System errors | System degraded |

### 6.2 Retry Strategies

#### Strategy R1: Simple Retry with Backoff

```python
retry_config = {
    "max_attempts": 3,
    "initial_delay_ms": 1000,
    "backoff_multiplier": 2,
    "max_delay_ms": 30000,
    "retryable_errors": [
        "TIMEOUT",
        "RATE_LIMIT",
        "TRANSIENT_ERROR"
    ]
}

def retry_with_backoff(task, config):
    delay = config.initial_delay_ms
    for attempt in range(config.max_attempts):
        try:
            return execute_task(task)
        except RetryableError as e:
            if attempt == config.max_attempts - 1:
                raise
            sleep(delay)
            delay = min(delay * config.backoff_multiplier,
                       config.max_delay_ms)
```

#### Strategy R2: Retry with Model Escalation

```
Escalation Retry Pattern:

Attempt 1: Haiku (if originally Haiku)
     |
     v (failure)
Attempt 2: Sonnet (escalate)
     |
     v (failure)
Attempt 3: Opus (final escalation)
     |
     v (failure)
Return error with diagnostic info
```

#### Strategy R3: Retry with Task Decomposition

```
If task fails due to complexity:

Original Task: "Analyze entire codebase"
     |
     v (timeout failure)
Decomposed:
  - Task 1a: "Analyze src/ directory"
  - Task 1b: "Analyze lib/ directory"
  - Task 1c: "Analyze drivers/ directory"
     |
     v (execute in parallel)
Aggregate Results
```

### 6.3 Fallback Patterns

#### Fallback F1: Graceful Degradation

```
Primary: Full code generation with validation
     |
     v (failure)
Fallback 1: Code generation without validation
     |
     v (failure)
Fallback 2: Code template with manual placeholders
     |
     v (failure)
Fallback 3: Documentation reference only
```

#### Fallback F2: Alternative Agent

```
If specialized agent fails, try generalist:

Primary: [Timer Peripheral Agent]
     |
     v (failure)
Fallback: [General Code Agent with timer context]
     |
     v (still failing)
Manual: Return documentation references
```

#### Fallback F3: Cached Response

```python
fallback_cache = {
    "strategy": "nearest_match",
    "cache_ttl_hours": 24,
    "similarity_threshold": 0.85
}

def get_fallback_response(query, cache):
    similar_queries = cache.find_similar(query, threshold=0.85)
    if similar_queries:
        return {
            "response": similar_queries[0].response,
            "is_cached": True,
            "cache_age": similar_queries[0].age,
            "confidence": similar_queries[0].similarity
        }
    return None
```

### 6.4 Error Recovery Workflows

#### Recovery Workflow 1: Checkpoint Resume

```
For long-running background tasks:

1. Task saves checkpoint every N operations
2. On failure, load most recent checkpoint
3. Resume from checkpoint state
4. Continue to completion

Checkpoint Schema:
{
  "agent_id": "abc-123",
  "checkpoint_id": "chk-456",
  "timestamp": "2026-01-08T10:30:00Z",
  "phase": 3,
  "progress": {
    "files_processed": 45,
    "current_file": "usart.c",
    "partial_results": {...}
  },
  "context_snapshot": {...}
}
```

#### Recovery Workflow 2: Human-in-the-Loop

```
When automated recovery fails:

1. Detect unrecoverable error
2. Save all available state
3. Generate diagnostic summary
4. Present options to user:
   - Retry with different parameters
   - Simplify the request
   - Provide additional context
   - Abort and report issue
5. Execute user's chosen action
```

### 6.5 Error Reporting and Diagnostics

```json
{
  "error_report": {
    "agent_id": "abc-123",
    "task_description": "Generate USART driver",
    "failure_type": "VALIDATION_ERROR",
    "error_details": {
      "message": "Generated code uses undefined macro",
      "location": "usart_init.c:45",
      "expected": "USART_BAUDRATE macro defined",
      "actual": "USART_BAUDRATE referenced but not defined"
    },
    "context": {
      "model": "sonnet",
      "attempt": 2,
      "elapsed_ms": 15234,
      "input_tokens": 4521,
      "output_tokens": 1203
    },
    "recovery_attempted": [
      {
        "strategy": "retry_with_additional_context",
        "result": "failed",
        "reason": "Same error reproduced"
      }
    ],
    "recommendations": [
      "Verify project includes stm32h7xx_hal_conf.h",
      "Check USART_BAUDRATE is defined in project config",
      "Try regenerating with explicit baudrate value"
    ]
  }
}
```

---

## 7. Execution Decision Matrix

### 7.1 Complete Decision Matrix for STM32 Tasks

| Task Category | Task Example | Model | Mode | Timeout | Parallel |
|---------------|--------------|-------|------|---------|----------|
| **Lookup** | Register address | Haiku | Foreground | 10s | No |
| **Lookup** | Pin alternate function | Haiku | Foreground | 10s | No |
| **Lookup** | Clock constraint | Haiku | Foreground | 10s | No |
| **Generation** | Single peripheral init | Sonnet | Foreground | 60s | No |
| **Generation** | Multiple peripheral init | Sonnet | Foreground | 120s | Yes |
| **Generation** | Complete driver | Opus | Background | 300s | No |
| **Analysis** | Single file review | Sonnet | Foreground | 60s | No |
| **Analysis** | Multi-file review | Opus | Background | 600s | Yes |
| **Analysis** | Full codebase audit | Opus | Background | 1800s | Yes |
| **Debug** | Simple error explanation | Sonnet | Foreground | 30s | No |
| **Debug** | Complex issue diagnosis | Opus | Foreground | 180s | No |
| **Debug** | Root cause analysis | Opus | Background | 600s | No |
| **Migration** | API update (single file) | Sonnet | Foreground | 120s | No |
| **Migration** | HAL version upgrade | Opus | Background | 1800s | Yes |
| **Migration** | MCU family migration | Opus | Background | 3600s | Yes |
| **Documentation** | Function documentation | Sonnet | Foreground | 60s | No |
| **Documentation** | Module documentation | Opus | Background | 300s | No |
| **Documentation** | Project documentation | Opus | Background | 1800s | Yes |
| **Validation** | Syntax check | Haiku | Foreground | 10s | No |
| **Validation** | HAL compliance | Sonnet | Foreground | 60s | No |
| **Validation** | Safety compliance | Opus | Background | 600s | No |

### 7.2 Quick Reference Decision Tree

```
START
  |
  v
Is this a simple lookup?
  |-- Yes --> Use Haiku, Foreground, 10s
  |-- No  --> Continue
  |
  v
Is user actively waiting?
  |-- Yes --> Foreground execution
  |   |
  |   v
  |   Can complete in < 60s?
  |   |-- Yes --> Use Sonnet, Foreground
  |   |-- No  --> Ask user: wait or background?
  |
  |-- No  --> Background execution
      |
      v
      Requires deep reasoning?
      |-- Yes --> Use Opus, Background
      |-- No  --> Use Sonnet, Background
      |
      v
      Can be parallelized?
      |-- Yes --> Spawn multiple agents
      |-- No  --> Single agent execution
```

### 7.3 STM32-Specific Task Classification

```yaml
stm32_task_classification:
  peripheral_tasks:
    gpio:
      simple_config: {model: haiku, mode: foreground, timeout: 15s}
      complex_config: {model: sonnet, mode: foreground, timeout: 60s}

    usart:
      baud_lookup: {model: haiku, mode: foreground, timeout: 10s}
      basic_init: {model: sonnet, mode: foreground, timeout: 45s}
      dma_init: {model: sonnet, mode: foreground, timeout: 90s}

    spi:
      basic_init: {model: sonnet, mode: foreground, timeout: 45s}
      with_dma: {model: sonnet, mode: foreground, timeout: 90s}

    timer:
      basic_pwm: {model: sonnet, mode: foreground, timeout: 60s}
      complex_pwm: {model: opus, mode: foreground, timeout: 120s}
      encoder_mode: {model: sonnet, mode: foreground, timeout: 60s}

    adc:
      single_channel: {model: sonnet, mode: foreground, timeout: 45s}
      multi_channel: {model: sonnet, mode: foreground, timeout: 90s}
      with_dma: {model: opus, mode: foreground, timeout: 120s}

    dma:
      simple_transfer: {model: sonnet, mode: foreground, timeout: 60s}
      circular_mode: {model: opus, mode: foreground, timeout: 90s}
      multi_stream: {model: opus, mode: foreground, timeout: 120s}

  system_tasks:
    clock_config:
      pll_setup: {model: sonnet, mode: foreground, timeout: 90s}
      full_tree: {model: opus, mode: foreground, timeout: 180s}

    power_management:
      sleep_modes: {model: sonnet, mode: foreground, timeout: 60s}
      low_power_design: {model: opus, mode: background, timeout: 600s}

    memory:
      mpu_config: {model: opus, mode: foreground, timeout: 120s}
      cache_config: {model: sonnet, mode: foreground, timeout: 60s}

  project_tasks:
    code_review:
      single_file: {model: sonnet, mode: foreground, timeout: 120s}
      full_project: {model: opus, mode: background, timeout: 1800s}

    documentation:
      inline_comments: {model: sonnet, mode: foreground, timeout: 60s}
      api_docs: {model: opus, mode: background, timeout: 600s}

    migration:
      hal_version: {model: opus, mode: background, timeout: 1800s}
      mcu_family: {model: opus, mode: background, timeout: 3600s}
```

---

## 8. Implementation Examples

### 8.1 Example: Peripheral Initialization Request

**User Request:** "Initialize USART2 for 115200 baud with DMA receive"

```python
# Execution determination
task_analysis = {
    "type": "peripheral_generation",
    "peripheral": "usart",
    "complexity": "medium",  # Involves DMA
    "estimated_time": "45-90 seconds",
    "user_waiting": True
}

execution_config = {
    "model": "sonnet",
    "run_in_background": False,
    "timeout": 90000,
    "subagent_type": "code",
    "context": {
        "mcu": "STM32H723ZG",
        "peripheral": "USART2",
        "requirements": {
            "baud_rate": 115200,
            "dma": {
                "enabled": True,
                "direction": "rx"
            }
        }
    }
}

# Agent invocation
result = task_tool.execute(
    description="Generate USART2 initialization with DMA RX",
    config=execution_config
)
```

### 8.2 Example: Full Project Analysis

**User Request:** "Analyze my entire STM32 project for optimization opportunities"

```python
# Execution determination
task_analysis = {
    "type": "project_analysis",
    "scope": "full_codebase",
    "complexity": "high",
    "estimated_time": "15-30 minutes",
    "user_waiting": False
}

# Phase 1: Parallel file analysis
phase1_config = {
    "pattern": "fan_out_fan_in",
    "run_in_background": True,
    "agents": [
        {
            "name": "peripheral_analyzer",
            "model": "sonnet",
            "task": "Identify all peripheral usage patterns",
            "files": ["src/drivers/**/*.c"]
        },
        {
            "name": "memory_analyzer",
            "model": "sonnet",
            "task": "Analyze memory usage and allocation",
            "files": ["**/*.c", "**/*.h"]
        },
        {
            "name": "power_analyzer",
            "model": "sonnet",
            "task": "Identify power consumption patterns",
            "files": ["src/**/*.c"]
        }
    ]
}

# Phase 2: Synthesis (after phase 1 completes)
phase2_config = {
    "model": "opus",
    "run_in_background": True,
    "task": "Synthesize findings and generate optimization report",
    "inputs": [
        "peripheral_analysis.json",
        "memory_analysis.json",
        "power_analysis.json"
    ],
    "output": "optimization_report.md"
}

# Progress monitoring
monitoring = {
    "progress_file": ".stm32-agent/analysis_progress.json",
    "notification_webhook": "http://localhost:8080/agent-updates",
    "checkpoint_interval": 60  # seconds
}
```

### 8.3 Example: Interactive Debugging Session

**User Request:** "My SPI communication is failing intermittently"

```python
# Initial classification (foreground, quick)
classification_config = {
    "model": "haiku",
    "run_in_background": False,
    "timeout": 10000,
    "task": "Classify debugging task complexity"
}

# Based on classification result: complex debugging needed
debug_config = {
    "model": "opus",  # Complex debugging requires deep reasoning
    "run_in_background": False,  # User wants interactive help
    "timeout": 180000,  # 3 minutes for initial analysis
    "subagent_type": "research",
    "context": {
        "peripheral": "SPI",
        "symptom": "intermittent_failure",
        "relevant_docs": [
            "rm0468_spi_chapter",
            "an5543_spi_guidelines"
        ]
    }
}

# Follow-up investigation (if needed)
deep_investigation_config = {
    "model": "opus",
    "run_in_background": True,  # Longer analysis
    "timeout": 600000,
    "task": "Perform comprehensive SPI timing analysis",
    "output_file": ".stm32-agent/spi_debug_report.md"
}
```

### 8.4 Example: Error Handling in Practice

```python
def execute_with_recovery(task_config, max_attempts=3):
    """Execute task with comprehensive error handling."""

    attempts = 0
    last_error = None

    while attempts < max_attempts:
        attempts += 1

        try:
            result = task_tool.execute(task_config)

            # Validate result
            if not validate_output(result, task_config.expected_schema):
                raise ValidationError("Output schema mismatch")

            return result

        except TimeoutError as e:
            last_error = e
            # Strategy: Extend timeout or move to background
            if task_config.run_in_background:
                task_config.timeout *= 2
            else:
                # Offer background execution to user
                if user_accepts_background():
                    task_config.run_in_background = True
                    task_config.timeout = 600000

        except ModelError as e:
            last_error = e
            # Strategy: Escalate model
            if task_config.model == "haiku":
                task_config.model = "sonnet"
            elif task_config.model == "sonnet":
                task_config.model = "opus"
            else:
                raise  # Already at highest model

        except ValidationError as e:
            last_error = e
            # Strategy: Add more context
            task_config.context.additional_instructions = (
                "Ensure output strictly follows the expected format"
            )

        except RateLimitError as e:
            last_error = e
            # Strategy: Exponential backoff
            sleep(2 ** attempts)

    # All attempts failed
    return create_error_report(task_config, last_error, attempts)
```

---

## Appendix A: Configuration Templates

### A.1 Foreground Task Template

```yaml
foreground_task:
  model: sonnet  # or haiku, opus
  run_in_background: false
  timeout: 60000
  subagent_type: code  # or research, review
  retry:
    max_attempts: 3
    backoff_ms: 1000
  context:
    mcu: STM32H723ZG
    project_path: /path/to/project
    relevant_files: []
```

### A.2 Background Task Template

```yaml
background_task:
  model: opus
  run_in_background: true
  timeout: 600000
  subagent_type: research
  checkpoint:
    enabled: true
    interval_seconds: 60
    path: .stm32-agent/checkpoints/
  output:
    path: .stm32-agent/results/
    format: json
  monitoring:
    progress_file: .stm32-agent/progress.json
    log_file: .stm32-agent/agent.log
```

### A.3 Parallel Execution Template

```yaml
parallel_execution:
  pattern: fan_out_fan_in
  agents:
    - name: agent_1
      model: sonnet
      task: "Task description"
      timeout: 120000
    - name: agent_2
      model: sonnet
      task: "Task description"
      timeout: 120000
  aggregator:
    model: opus
    strategy: weighted_merge
    timeout: 180000
  error_handling:
    continue_on_partial_failure: true
    minimum_success_count: 1
```

---

## Appendix B: Metrics and Monitoring

### B.1 Execution Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| `task_success_rate` | Percentage of tasks completing successfully | > 95% |
| `p50_latency` | Median task completion time | < 30s (foreground) |
| `p95_latency` | 95th percentile completion time | < 120s (foreground) |
| `model_escalation_rate` | Frequency of model upgrades | < 10% |
| `retry_rate` | Percentage of tasks requiring retry | < 5% |
| `background_completion_rate` | Background tasks completing fully | > 98% |
| `cost_per_task` | Average API cost per task | Varies by type |

### B.2 Alert Thresholds

```yaml
alerts:
  task_failure_rate:
    warning: 5%
    critical: 10%
  p95_latency:
    warning: 120s
    critical: 300s
  model_escalation_rate:
    warning: 15%
    critical: 25%
  background_task_timeout:
    warning: 3
    critical: 5
```

---

*Document Version: 1.0*
*Last Updated: January 2026*
*Companion to: ARCHITECTURE_BEST_PRACTICES.md*
