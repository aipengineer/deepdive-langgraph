# LangGraph Deep Dive Tutorial

## Project Overview
A comprehensive 3-hour hands-on tutorial designed to teach the fundamentals of LangGraph, a library for building stateful, multi-actor applications with LLMs. The tutorial focuses on practical, hands-on learning through progressive exercises.

## Prerequisites
- Python programming experience
- Basic understanding of LLMs and API interactions
- No prior LangChain experience required
- Python 3.13 environment

## Required APIs/Tools
- OpenAI API key for LLM interactions
- UV for environment management
- Ruff for code formatting and linting

## Tutorial Structure
The tutorial is divided into 4 units, each building upon the previous one. Each unit contains:
- Conceptual introduction (10-15 minutes)
- Hands-on exercises (30-35 minutes)
- Review and Q&A (5-10 minutes)

### Unit 1: Graph Basics & State Management
**Learning Goals:**
- Understand core LangGraph concepts (StateGraph, nodes, edges)
- Learn state management and message handling
- Master basic graph flow control
- Implement proper typing and state updates

**Exercises:**
1. "Hello LangGraph"
   - Create basic StateGraph with LLM node
   - Implement proper state typing
   - Handle message updates
   - Manage basic error cases

2. "Message Memory"
   - Extend basic graph with conversation memory
   - Implement message windowing
   - Add message summarization
   - Handle metadata and state updates

3. "Conditional Router"
   - Create multi-path response system
   - Implement message classification
   - Handle routing logic
   - Manage edge cases

### Unit 2: Building Agents with LangGraph
**Learning Goals:**
- Understand tool integration
- Master tool calling patterns
- Learn parallel execution
- Handle tool errors and retries

**Exercises:**
1. "Simple Tool User"
   - Integrate search tool
   - Implement proper validation
   - Handle retries and errors
   - Provide user feedback

2. "Multi-Tool Agent"
   - Integrate multiple tools
   - Implement tool selection
   - Manage rate limits
   - Track tool usage

3. "Parallel Tool Executor"
   - Execute tools in parallel
   - Aggregate results
   - Handle partial failures
   - Track execution progress

### Unit 3: Checkpointing & Persistence
**Learning Goals:**
- Master LangGraph's checkpointing system
- Understand state persistence
- Learn branching and versioning
- Manage multiple threads

**Exercises:**
1. "Checkpoint Basics"
   - Implement basic checkpointing
   - Add state versions
   - Restore from checkpoints
   - Clean up old states

2. "Time Travel"
   - Create checkpoint branches
   - Track state differences
   - Merge branches
   - Handle conflicts

3. "Multi-Thread Management"
   - Manage thread pools
   - Synchronize shared data
   - Clean up threads
   - Monitor thread health

### Unit 4: Human-in-the-Loop Patterns
**Learning Goals:**
- Integrate human oversight
- Handle state modifications
- Implement approval flows
- Create dynamic routing

**Exercises:**
1. "Basic Oversight"
   - Create approval workflows
   - Track approval status
   - Handle rejections
   - Send notifications

2. "State Editor"
   - Modify graph state
   - Validate changes
   - Track edit history
   - Implement rollbacks

3. "Dynamic Routing"
   - Handle human decisions
   - Suggest routes
   - Manage fallbacks
   - Track routing history

## Project Structure
```
deepdive-langgraph/
├── src/
│   ├── exercises/
│   │   ├── unit1/  # Graph Basics
│   │   ├── unit2/  # Tool Usage
│   │   ├── unit3/  # Checkpointing
│   │   └── unit4/  # Human-in-Loop
│   └── utils/
│       ├── validation.py  # Exercise validators
│       └── mocking.py     # API mocking
├── solutions/            # Complete exercise solutions
├── tests/               # Exercise test cases
└── docs/               # Additional documentation
```

## Development Workflow
1. Environment Setup:
   ```bash
   make setup  # Creates venv and installs dependencies
   ```

2. Development:
   ```bash
   make format  # Format code
   make lint    # Check style
   make test    # Run tests
   ```

3. Testing:
   - Unit tests for exercise validation
   - Integration tests with real APIs
   - Mocked tests for development

## Exercise Completion Criteria
For each exercise:
1. All tests pass
2. Code is properly formatted
3. Type hints are complete
4. Error cases are handled
5. Documentation is clear

## Additional Resources
- LangGraph Documentation
- LangSmith for monitoring
- Example applications
- Troubleshooting guides

## Next Steps
1. Complete initial exercise implementations
2. Create test suite
3. Add comprehensive documentation
4. Create solution guide


# Learning Goals

## UNIT 1: Graph Basics & State Management

### Exercise 1.1 - "Hello LangGraph"
#### Requirements:
- Create a StateGraph with a single LLM node
- Define a basic State type using TypedDict and Annotated 
- Implement proper input/output message handling
- Include basic error handling for API failures

Expected Implementation:
```python
# Must implement roughly this pattern:
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(State)
graph.add_node("llm", llm_node)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)
```

#### Success Criteria:
- Graph responds coherently to user input
- Messages are properly added to state
- Proper type hints throughout
- Basic error handling implemented

#### Stretch Goals:
- Add configurable system messages
- Add streaming support

### Exercise 1.2 - "Message Memory"
#### Requirements:
- Extend Exercise 1.1 to maintain conversation context
- Add a message summarization node for long conversations
- Implement a configurable message window size
- Add metadata to messages (timestamps, roles, etc.)

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    summary: str
    window_size: int

# Must implement nodes for:
- LLM responses
- Message windowing
- Summary generation
```

#### Success Criteria:
- Maintains coherent conversations over multiple turns
- Properly manages message history
- Summarizes long conversations effectively
- Memory constraints are properly handled

#### Stretch Goals:
- Add different summarization strategies
- Implement message pruning

### Exercise 1.3 - "Conditional Router"
#### Requirements:
- Create a graph with multiple response nodes
- Implement a classifier node for message routing
- Add at least 3 different response paths
- Implement proper handling for ambiguous cases

####  Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    classification: str
    confidence: float

# Must implement:
- Classifier node
- Multiple response nodes
- Conditional edges with routing logic
```

####  Success Criteria:
- Correctly classifies and routes messages
- Handles edge cases gracefully
- Maintains conversation coherence across routes
- Proper error handling for classification failures

#### Stretch Goals:
- Add confidence thresholds for routing
- Implement fallback routes

Let me continue with the detailed requirements for the remaining units.

## UNIT 2: Building Agents with LangGraph

### Exercise 2.1 - "Simple Tool User"
#### Requirements:
- Create a graph that integrates with TavilySearchResults tool
- Implement proper tool calling with JSON validation
- Add retry logic for failed tool calls
- Include proper error messaging to users

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    tool_calls: list[ToolCall]
    tool_outputs: list[ToolOutput]

# Must implement:
- LLM node with tool binding
- Tool execution node
- Tool result processing node
```

#### Success Criteria:
- Successfully calls tools when needed
- Properly validates tool inputs
- Handles tool failures gracefully
- Maintains conversation coherence

#### Stretch Goals:
- Add tool usage tracking
- Implement tool output caching

### Exercise 2.2 - "Multi-Tool Agent"
#### Requirements:
- Integrate multiple tools (search, math, weather)
- Implement tool selection logic
- Add tool usage constraints (rate limits, usage quotas)
- Include tool usage explanations to users

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    available_tools: list[Tool]
    tool_usage: dict[str, int]
    rate_limits: dict[str, RateLimit]

# Must implement:
- Tool selection node
- Rate limiting logic
- Usage tracking
```

#### Success Criteria:
- Selects appropriate tools for tasks
- Respects rate limits and quotas
- Provides clear explanations for tool choices
- Handles multi-tool sequences properly

#### Stretch Goals:
- Add tool cost optimization
- Implement tool result ranking

### Exercise 2.3 - "Parallel Tool Executor"
#### Requirements:
- Implement parallel tool execution
- Add result aggregation logic
- Implement proper error handling for partial failures
- Include progress reporting

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    pending_tools: list[ToolCall]
    results: dict[str, ToolResult]
    errors: dict[str, str]

# Must implement:
- Parallel execution node
- Result aggregator
- Error handler
```

#### Success Criteria:
- Successfully executes tools in parallel
- Properly aggregates results
- Handles partial failures gracefully
- Reports progress clearly

#### Stretch Goals:
- Add dynamic parallelism based on load
- Implement result caching

## UNIT 3: Checkpointing & Persistence

### Exercise 3.1 - "Checkpoint Basics"
#### Requirements:
- Implement basic checkpointing with MemorySaver
- Add state versioning
- Implement reload from checkpoint
- Add checkpoint cleanup logic

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    version: str
    metadata: dict[str, Any]

# Must implement:
- Checkpoint creation
- State restoration
- Cleanup logic
```

#### Success Criteria:
- Successfully saves and restores state
- Handles versioning properly
- Manages cleanup effectively
- Maintains data consistency

#### Stretch Goals:
- Add checkpoint compression
- Implement checkpoint validation

### Exercise 3.2 - "Time Travel"
#### Requirements:
- Implement checkpoint branching
- Add state diffing functionality
- Implement branch merging
- Add branch cleanup logic

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    branch_id: str
    parent_checkpoint: str
    changes: list[StateChange]

# Must implement:
- Branch creation
- State diffing
- Branch merging
```

#### Success Criteria:
- Successfully creates and manages branches
- Properly tracks state changes
- Merges branches correctly
- Handles conflicts gracefully

#### Stretch Goals:
- Add branch visualization
- Implement change reversal

### Exercise 3.3 - "Multi-Thread Management"
#### Requirements:
- Implement thread pooling
- Add thread synchronization
- Implement thread cleanup
- Add thread monitoring

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    thread_id: str
    shared_data: dict[str, Any]
    locks: list[str]

# Must implement:
- Thread pool manager
- Synchronization logic
- Monitoring system
```

#### Success Criteria:
- Successfully manages multiple threads
- Properly synchronizes shared data
- Cleans up inactive threads
- Monitors thread health

#### Stretch Goals:
- Add thread prioritization
- Implement thread migration

## UNIT 4: Human-in-the-Loop Patterns

### Exercise 4.1 - "Basic Oversight"
#### Requirements:
- Implement pre-execution approval flow
- Add result review functionality
- Implement approval tracking
- Add notification system

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    pending_approvals: list[Approval]
    approved_actions: list[Action]
    notifications: list[Notification]

# Must implement:
- Approval request node
- Review handler
- Notification sender
```

#### Success Criteria:
- Successfully requests approvals
- Properly tracks approval status
- Handles rejections gracefully
- Maintains audit trail

#### Stretch Goals:
- Add approval delegation
- Implement approval expiration

### Exercise 4.2 - "State Editor"
Requirements:
- Implement state modification UI
- Add validation for edits
- Implement edit history
- Add rollback functionality

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    edits: list[StateEdit]
    validators: dict[str, Validator]
    history: list[StateVersion]

# Must implement:
- Edit handler
- Validation logic
- History tracker
```

#### Success Criteria:
- Successfully modifies state
- Validates changes properly
- Tracks edit history
- Handles rollbacks correctly

Stretch Goals:
- Add collaborative editing
- Implement edit suggestions

### Exercise 4.3 - "Dynamic Routing"
#### Requirements:
- Implement human decision points
- Add routing suggestions
- Implement fallback paths
- Add routing history

#### Expected Implementation:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    decision_points: list[Decision]
    suggestions: list[Suggestion]
    routing_history: list[Route]

# Must implement:
- Decision handler
- Suggestion generator
- History tracker
```

#### Success Criteria:
- Successfully handles decisions
- Provides useful suggestions
- Maintains routing history
- Handles fallbacks properly

#### Stretch Goals:
- Add decision automation
- Implement route optimization