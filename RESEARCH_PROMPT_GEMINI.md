# DRAKON Diagram Intelligence Enhancement - Deep Research

## Context

We have built an automated system that converts source code (Python, TypeScript, Bash) into DRAKON diagrams. The system currently works but produces overly simplified diagrams that don't capture the full complexity of the refactored codebase.

**Current System Architecture:**
```
Source Code → AST Parser → Pattern Detector → DRAKON Generator → JSON/DRN
     ↓              ↓              ↓                  ↓
  Python/TS    tree-sitter   FSM patterns      drakonwidget format
```

**Current Tools:**
- `tools/drakon/converter/code_to_drakon.py` - Main code analyzer
- `tools/drakon/converter/drakon_to_json.py` - JSON exporter
- AST analysis using tree-sitter
- Pattern detection (Observer, Command, Strategy, etc.)

## Problem Statement

Generated DRAKON diagrams are currently too simplistic:

1. **Single function calls** → Represented as 1-2 action nodes
2. **Complex conditional logic** → Simplified to single question nodes
3. **Nested loops and error handling** → Often flattened or omitted
4. **State transitions** → Not properly visualized
5. **Async/Promise flows** → Linearized incorrectly

**Example:**
A 150-line TypeScript handler with:
- 3 try-catch blocks
- 5 conditional branches
- 2 nested loops
- 4 async operations
- Event emission

Currently generates only 4-6 DRAKON nodes instead of 20-30 nodes that would properly represent the logic.

## Research Objectives

### PRIMARY GOAL
Develop an AI-enhanced algorithm that can:
1. **Deeply analyze code semantics** beyond AST structure
2. **Identify implicit logic flows** not obvious from syntax
3. **Generate detailed, accurate DRAKON representations** that match code complexity
4. **Preserve control flow fidelity** while maintaining diagram readability

### SECONDARY GOALS
- Improve pattern recognition accuracy
- Detect anti-patterns and code smells for visualization
- Generate meaningful node labels automatically
- Optimize diagram layout for readability

## Research Questions

### 1. Code Semantic Analysis
**Question:** How can we extract deeper semantic meaning from code to improve diagram detail?

**Areas to explore:**
- Control flow graph (CFG) analysis beyond basic AST
- Data flow analysis (DFA) for variable lifecycles
- Dependency graphs between functions/modules
- Temporal logic patterns (before/after conditions)
- Side effect detection and visualization

**Deliverable:** Propose 3-5 concrete techniques with implementation approach

---

### 2. Intelligent Pattern Recognition
**Question:** How can AI/ML enhance detection of code patterns and their DRAKON representation?

**Areas to explore:**
- Training models on code→DRAKON pairs
- LLM-based intent extraction from function names/comments
- Clustering similar code blocks for pattern library
- Cross-language pattern normalization
- Design pattern detection (GoF patterns)

**Deliverable:** Recommended AI architecture (transformer/GNN/hybrid) with pros/cons

---

### 3. Complexity Metrics & Granularity Control
**Question:** How do we balance diagram detail vs. readability?

**Areas to explore:**
- Cyclomatic complexity thresholds for node expansion
- Cognitive complexity as detail determinant
- Hierarchical diagram generation (zoom levels)
- Automatic diagram splitting for large functions
- User-configurable detail levels (1-5 scale)

**Deliverable:** Complexity→Detail mapping algorithm

---

### 4. Advanced Control Flow Visualization
**Question:** How to accurately represent modern programming constructs in DRAKON?

**Areas to explore:**
- Async/await and Promise chains → DRAKON flow
- Event-driven patterns → State diagrams
- Reactive programming (RxJS, Streams) → Flow representation
- Error propagation paths → Exception branches
- Callback hell → Linearized flow

**Deliverable:** DRAKON extension patterns for each construct

---

### 5. Context-Aware Node Generation
**Question:** How to generate meaningful, human-readable node labels automatically?

**Areas to explore:**
- LLM-based summarization of code blocks
- Intent extraction from variable names (camelCase parsing)
- Comment/docstring integration
- Business logic inference from domain keywords
- Multi-language label generation (code → Ukrainian/English)

**Deliverable:** Node labeling algorithm with examples

---

### 6. Real-time Code Understanding
**Question:** Can we use embeddings to understand code intent without full compilation?

**Areas to explore:**
- Code2Vec / Code embeddings for similarity detection
- BERT/CodeBERT for semantic code understanding
- GPT-4/Gemini API for on-demand code explanation
- Vector databases for pattern matching
- Few-shot learning for new patterns

**Deliverable:** Embedding-based architecture proposal

---

### 7. **CRITICAL:** DrakonWidget API Integration for Native Diagram Generation
**Question:** How can we use drakonWidget's internal API to programmatically generate diagrams instead of manually constructing JSON?

**Background:**
Currently, our system manually constructs JSON diagram structures:
```json
{
  "name": "example",
  "items": {
    "1": {"type": "branch", "one": "2", "content": ""},
    "2": {"type": "action", "content": "Do something", "one": "3"}
  }
}
```

However, `drakonwidget.js` (created by Stepan Mitkin, author of DRAKON) contains internal functions for creating diagram elements:
- `createNode(visuals, itemId, type, content, id)`
- `createNewItem(model, type)`
- `buildDiagramModel(widget, diagram)`
- `addItemToModel(model, item)`

**Areas to explore:**

1. **Headless DrakonWidget Usage**
   - Can drakonWidget run in Node.js (server-side) for diagram generation?
   - Which DOM dependencies can be mocked/eliminated?
   - How to extract diagram JSON after programmatic construction?

2. **API Discovery & Documentation**
   - Reverse-engineer drakonWidget's public/private API
   - Identify minimal API surface for programmatic diagram creation
   - Document parameter formats and validation rules

3. **Compatibility with Stepan Mitkin's Editors**
   - Desktop DRAKON Editor (.drn format) compatibility
   - DrakonHub online editor compatibility
   - Ensure generated JSON matches official spec

4. **Programmatic Diagram Construction Flow**
   ```
   Code AST → Semantic Analysis → DrakonWidget API calls → Native JSON
   ```
   Instead of:
   ```
   Code AST → Semantic Analysis → Manual JSON construction → Hope it's valid
   ```

5. **API-Based Node Creation**
   - How to create nodes programmatically using drakonWidget API?
   - How to connect nodes (one, two, three branches)?
   - How to set node properties (content, type, coordinates)?
   - How to validate diagram structure before export?

6. **Canvas Rendering vs. JSON Generation**
   - Can we use drakonWidget API without rendering to canvas?
   - Extract diagram model after API manipulation
   - Validate diagram completeness (all branches connected, etc.)

**Key Questions:**
1. Is there a documented API in drakonWidget for programmatic diagram creation?
2. Can we use `window.DrakonTestAPI` approach server-side (Node.js)?
3. How does Stepan Mitkin's desktop editor generate .drn files? Can we replicate this?
4. Would using drakonWidget API guarantee 100% compatibility with official editors?
5. What's the performance cost of running drakonWidget server-side vs manual JSON?

**Expected Benefits:**
- ✅ **Guaranteed compatibility** with official DRAKON tools
- ✅ **Automatic validation** (drakonWidget won't create invalid diagrams)
- ✅ **Future-proof** (updates to drakonWidget automatically propagate)
- ✅ **Correct layout metadata** (positions, connections, etc.)
- ✅ **Support for advanced features** (parameters, comments, etc.)

**Implementation Questions:**
- How to integrate drakonWidget API into `code_to_drakon.py`?
- Should we use PyExecJS to run drakonWidget from Python?
- Or create a Node.js microservice for diagram generation?
- How to handle diagram layout (auto-layout vs. manual positioning)?

**Deliverable:**
- Architecture for drakonWidget-based diagram generation
- API reference for programmatic node creation
- Compatibility validation strategy
- Performance comparison (API vs. manual JSON)
- Migration plan from current manual JSON to API-based generation

---

## Technical Constraints

**Must Support:**
- Python 3.8+
- TypeScript/JavaScript (Node.js)
- Bash scripts
- Tree-sitter AST parsing
- Output to DRAKON JSON format (compatible with drakonwidget)

**Performance Requirements:**
- Process 100-line function in < 5 seconds
- Maintain deterministic output (same code → same diagram)
- Memory efficient for large codebases (1000+ files)

**Integration:**
- Plug into existing `code_to_drakon.py`
- Minimal external dependencies
- CLI-friendly (for automation pipelines)

## Expected Deliverables

### 1. Research Report (3000-5000 words)
- Literature review of code analysis techniques
- Comparative analysis of AI approaches
- Recommended architecture with justification
- Implementation roadmap (phases)

### 2. Proof of Concept Algorithm
- Pseudocode for enhanced analyzer
- Sample input/output pairs showing improvement
- Complexity analysis (Big-O)

### 3. Evaluation Metrics
- Diagram completeness score (% logic coverage)
- Readability index (nodes, edges, nesting depth)
- Accuracy vs. manual diagrams (if available)
- Performance benchmarks

### 4. Implementation Guidelines
- Step-by-step integration plan
- Required libraries/models
- Training data requirements (if ML-based)
- Fallback strategies for edge cases

## Research Methodology Suggestions

1. **Literature Review** (Week 1)
   - Academic papers: program comprehension, CFG analysis
   - Industry solutions: Mermaid.js, PlantUML auto-generation
   - ML papers: code2vec, GraphCodeBERT, CodeT5

2. **Prototyping** (Week 2-3)
   - Implement 2-3 most promising techniques
   - Benchmark against current system
   - Collect metrics on real codebase samples

3. **Evaluation** (Week 4)
   - Human evaluation: developer feedback on diagrams
   - Automated metrics: complexity correlation
   - Edge case testing

4. **Recommendation** (Week 5)
   - Final architecture design
   - ROI analysis (effort vs. improvement)
   - Phased rollout plan

## Example Code Samples for Testing

### Sample 0: Current vs. API-Based Diagram Generation

**Current Approach (Manual JSON Construction):**
```python
# tools/drakon/converter/drakon_to_json.py
def generate_diagram_json(function_name, nodes):
    diagram = {
        "name": function_name,
        "access": "write",
        "params": [],
        "items": {}
    }

    # Manually build items dict
    node_id = 1
    for node in nodes:
        diagram["items"][str(node_id)] = {
            "type": node.type,  # "action", "branch", "end"
            "content": node.content,
            "one": str(node_id + 1) if node.next else None
        }
        node_id += 1

    return json.dumps(diagram)
```

**Proposed API-Based Approach:**
```javascript
// Using drakonWidget API (if we can run it server-side)
const drakonGenerator = require('./drakonwidget-headless');

function generateDiagramViaAPI(functionName, nodes) {
  const diagram = drakonGenerator.createDiagram(functionName);

  nodes.forEach((node, index) => {
    const nodeId = drakonGenerator.addNode(diagram, {
      type: node.type,
      content: node.content,
      connectTo: nodes[index + 1]?.id
    });

    // drakonWidget validates structure automatically!
  });

  return drakonGenerator.exportJSON(diagram);
  // Guaranteed compatible with Stepan Mitkin's editors!
}
```

**Question for Research:**
Is the API-based approach feasible? What are the technical barriers? How can we overcome them?

---

### Sample 1: TypeScript Event Handler (Current: 4 nodes → Target: 15+ nodes)
```typescript
async function handleUserRequest(req: Request, res: Response) {
  try {
    const userId = req.params.id;

    if (!userId) {
      return res.status(400).json({ error: 'Missing user ID' });
    }

    const user = await db.users.findById(userId);

    if (!user) {
      logger.warn(`User not found: ${userId}`);
      return res.status(404).json({ error: 'User not found' });
    }

    if (!user.isActive) {
      return res.status(403).json({ error: 'User inactive' });
    }

    const permissions = await checkPermissions(user);

    if (!permissions.canRead) {
      auditLog.record('unauthorized_access', userId);
      return res.status(403).json({ error: 'No permission' });
    }

    const data = await fetchUserData(user);
    eventBus.emit('user_accessed', { userId, timestamp: Date.now() });

    return res.json(data);

  } catch (error) {
    logger.error('Request failed:', error);
    return res.status(500).json({ error: 'Internal error' });
  }
}
```

### Sample 2: Python State Machine (Current: 6 nodes → Target: 25+ nodes)
```python
def process_workflow(state_machine, input_data):
    current_state = state_machine.initial_state

    while current_state != 'COMPLETED':
        if current_state == 'VALIDATE':
            if validate_input(input_data):
                current_state = 'PROCESS'
            else:
                log_error("Validation failed")
                current_state = 'ERROR'

        elif current_state == 'PROCESS':
            try:
                result = execute_processing(input_data)
                if result.success:
                    current_state = 'FINALIZE'
                else:
                    retry_count = getattr(state_machine, 'retries', 0)
                    if retry_count < 3:
                        state_machine.retries = retry_count + 1
                        time.sleep(2 ** retry_count)
                        continue
                    else:
                        current_state = 'ERROR'
            except Exception as e:
                handle_exception(e)
                current_state = 'ERROR'

        elif current_state == 'FINALIZE':
            save_results(result)
            notify_subscribers(state_machine.id, result)
            current_state = 'COMPLETED'

        elif current_state == 'ERROR':
            rollback_changes(state_machine)
            raise WorkflowException("Processing failed")

    return current_state
```

## Success Criteria

**Minimum Viable Improvement:**
- 2x increase in average diagram nodes for complex functions
- 90%+ control flow path coverage
- Maintains or improves readability scores
- **100% compatibility with Stepan Mitkin's DRAKON editors**

**Stretch Goals:**
- AI-generated node descriptions match human intent (>80% similarity)
- Automatic detection of 15+ design patterns
- Multi-level diagram generation (overview → detailed zoom)
- **Headless drakonWidget integration for guaranteed valid diagrams**
- **Support for .drn format export (desktop editor compatibility)**

## Additional Context

**Current Workflow:**
```
Developer writes code → unified-motia-workflow.sh drakon <step_name>
                               ↓
                    generate_step_diagrams.py
                               ↓
                    4 standard diagrams:
                    - initialization.json
                    - main-flow.json
                    - error-handling.json
                    - cleanup.json
```

**Desired Enhancement:**
- Same 4 diagrams but with 3-5x more detail
- Additional diagrams for complex branches
- Hierarchical diagrams (parent → child drill-down)

## Resources Available

- Existing codebase: `/home/vokov/motia_drn_start/`
- Tree-sitter grammars for Python, TypeScript, Bash
- DRAKON format specification (JSON schema)
- Sample diagrams (current output examples)
- Gemini AI Pro API access
- Compute resources for model training (if needed)
- **drakonwidget.js** - Official DRAKON rendering library by Stepan Mitkin
- **Existing Testing API** in app.js:
  ```javascript
  window.DrakonTestAPI = {
    createDiagram: (name) => {...},
    addNode: (type) => {...},
    getDiagram: () => {...},
    saveDiagram: () => {...}
  }
  ```
- Access to DRAKON community resources and documentation

## Timeline

**Preferred:** 2-4 weeks for comprehensive research
**Acceptable:** 1 week for rapid prototyping + recommendations

---

## OUTPUT FORMAT

Please structure your research response as:

### 1. Executive Summary (500 words)
Key findings and recommended approach

### 2. Technical Deep Dive (2000+ words)
Detailed analysis of each research question

### 3. Proposed Architecture
System diagram + component descriptions

### 4. Implementation Plan
Phased approach with effort estimates

### 5. Risk Analysis
Technical challenges and mitigation strategies

### 6. Appendix
Code samples, algorithm pseudocode, references

---

**Additional Instructions:**
- Prioritize practical, implementable solutions over theoretical perfection
- Consider computational cost vs. accuracy tradeoffs
- Suggest open-source libraries where applicable
- Provide code snippets in Python/TypeScript for proposed algorithms
- Include visualization examples (Mermaid diagrams for architecture)

**Bonus Points:**
- Novel approaches not found in literature
- Integration with existing DRAKON ecosystem
- Backward compatibility with current diagrams
- Extensibility for future programming languages
- **🔥 HIGHEST PRIORITY: Feasibility analysis of drakonWidget API integration (Question 7)**

---

## ⚠️ CRITICAL PRIORITY: Question 7 (DrakonWidget API)

**Please prioritize Question 7** as it has the highest impact on system architecture:

If we can successfully integrate drakonWidget API for diagram generation, this would:
1. **Solve compatibility issues** with official DRAKON editors permanently
2. **Reduce maintenance burden** (no need to track format changes)
3. **Guarantee correctness** (drakonWidget validates structure)
4. **Enable advanced features** (auto-layout, .drn export, etc.)

**Recommended Research Flow:**
1. Start with Question 7 - determine if API integration is feasible
2. If YES → Design architecture around drakonWidget API
3. If NO → Proceed with Questions 1-6 for manual JSON improvements
4. Combine both approaches if partial integration is possible

**Key Deliverable for Question 7:**
- Proof-of-concept code showing drakonWidget creating a simple diagram headless
- OR explanation of technical barriers and workarounds
- Performance benchmark: API vs. manual JSON

---

**Research Start:** Please begin with **Question 7 (DrakonWidget API Integration)** as the critical path determinant, then proceed to Question 1 and subsequent questions.
