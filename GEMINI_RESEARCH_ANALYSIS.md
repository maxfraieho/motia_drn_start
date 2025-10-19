# Аналіз результатів дослідження Gemini AI Pro

**Дата:** 2025-10-19
**Документ:** Enhancing DRAKON Diagram Generation.pdf (24 стор.)
**Статус:** ✅ Дослідження завершено, готово до імплементації

---

## 🎯 Executive Summary

Gemini AI Pro провів глибокий аналіз системи та надав **практичний roadmap** для покращення генерації DRAKON діаграм з **4-6x збільшенням деталізації** та **100% сумісністю** з офіційними редакторами.

### Ключові досягнення дослідження:
- ✅ Відповідь на критичне питання про drakonWidget API (Question 7)
- ✅ Детальна архітектура гібридної системи
- ✅ 4-фазний план імплементації (11-16 тижнів)
- ✅ Конкретні бібліотеки та інструменти
- ✅ Risk analysis з mitigation strategies

---

## 🔥 КРИТИЧНИЙ ВИСНОВОК: DrakonWidget API Integration (Question 7)

### Питання:
Чи можна використовувати drakonWidget API для програмної генерації замість ручного JSON?

### Відповідь Gemini:

#### ❌ Пряме використання НЕМОЖЛИВЕ
```
drakonWidget.js ПОТРЕБУЄ:
- window object (browser)
- DOM (Document Object Model)
- Canvas 2D API
- CSS rendering

⚠️ PyExecJS та Node.js (headless) НЕ мають цих компонентів
```

#### ✅ РЕКОМЕНДОВАНЕ РІШЕННЯ: Headless Browser Microservice

**Архітектура:**
```
Python Backend (code analysis)
    ↓ HTTP POST /generate
Node.js Microservice
    ↓
Puppeteer Controller
    ↓
Headless Chrome Instance (pool)
    ↓
drakonWidget.js API
    ↓
Valid JSON ← Guaranteed compatible!
```

**Переваги:**
- ✅ **100% format compatibility** (використовує офіційну бібліотеку)
- ✅ **Future-proof** (auto-updates з drakonWidget)
- ✅ **Automatic validation** (drakonWidget не створює invalid діаграми)
- ✅ **Full feature support** (auto-layout, advanced nodes, etc.)

**Недоліки:**
- ⚠️ Performance overhead (startup browser instances)
- **Mitigation:** Instance pooling (warm instances pool)

---

#### ✅ АЛЬТЕРНАТИВА: Direct .drn SQLite Generation

**ВІДКРИТТЯ Gemini:**
```
.drn формат = SQLite 3.6 database!
```

**Schema (documented):**
```sql
-- diagrams table
CREATE TABLE diagrams (
  diagram_id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  zoom DOUBLE
);

-- items table
CREATE TABLE items (
  item_id INTEGER PRIMARY KEY,
  diagram_id INTEGER,
  type TEXT,  -- 'action', 'branch', 'end', etc.
  text TEXT,
  one INTEGER,  -- connection to next node
  two INTEGER,  -- alternative path
  x, y, w, h INTEGER  -- position & size
);
```

**Переваги:**
- ✅ **Дуже висока продуктивність** (native SQLite I/O)
- ✅ **Можна генерувати з Python** (без JavaScript)
- ✅ **Сумісність з Desktop DRAKON Editor**

**Недоліки:**
- ⚠️ Schema-dependent (може змінитися в нових версіях)
- ⚠️ Треба вручну реалізувати всі features

---

### 🎯 ГІБРИДНА СТРАТЕГІЯ (Рекомендація Gemini)

| Method | Use Case | Compatibility | Performance | Maintenance |
|--------|----------|---------------|-------------|-------------|
| **Headless drakonWidget** (Primary) | Day-to-day use | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Very Low |
| **Direct .drn SQLite** (Secondary) | Bulk processing, fallback | ⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐ Medium |
| Manual JSON (Current) | **DEPRECATE** | ⭐ Low | ⭐⭐⭐⭐ High | ⭐ High |

---

## 📊 Multi-Layered Code Analysis Architecture

### Layer 1: Control Flow Graph (CFG)

**Проблема:** AST показує синтаксис, але не execution flow

**Рішення:** CFG (graph of basic blocks)

**Бібліотеки:**
- Python: `py2cfg`, `staticfg`
- TypeScript: `esgraph`, `styx`

**Переваги:**
- ✅ Представлення всіх execution paths
- ✅ Nested loops → graph cycles
- ✅ Exception handling → exceptional edges (try → catch → finally)

**Приклад:**
```python
try:
    result = risky_operation()
    if result.success:
        process(result)
except Exception as e:
    handle_error(e)
finally:
    cleanup()
```

CFG буде мати:
- Normal edge: try → if → process → finally
- Exception edge: risky_operation → catch → finally

---

### Layer 2: Data Flow Analysis (DFA)

**Інструмент:** **CodeQL** (GitHub)

**Мета:** Відстеження lifecycle змінних

**Use Case:** State Machine Visualization
```python
current_state = 'INIT'
# DFA tracks: current_state as "variable of interest"

current_state = 'PROCESS'  # Source: state transition
# → Generate DRAKON node: "Transition to PROCESS state"

if current_state == 'PROCESS':  # Sink: state check
    # ...
```

**Результат:** Явні "State Transition" вузли в діаграмі

---

### Layer 3: Advanced Control Flow Patterns

#### Pattern 1: Async/Await → Promise Graph

**DRAKON Representation:**
```
await fetchData() →  [Async Action Node]
                    ↓ one (success)  ↓ two (failure)
               Process Data      .catch() handler
```

#### Pattern 2: State Machine → UML State Diagram

**Python:**
```python
while current_state != 'DONE':
    if current_state == 'VALIDATE':
        # ...
    elif current_state == 'PROCESS':
        # ...
```

**DRAKON:**
- Кожен `elif current_state ==` → окремий "State Node"
- `current_state = 'X'` → transition arrow

---

### Layer 4: AI-Powered Pattern Recognition

#### Hybrid Architecture: GNN + CodeT5

**Component 1: Graph Neural Network (GNN)**
- Input: CFG/DFA graph
- Task: Structural pattern recognition
- Examples:
  - Design patterns (State, Observer, Command)
  - Anti-patterns (callback hell, deep nesting)
  - Code smells

**Component 2: Transformer (CodeT5)**
- Input: Source code text
- Task: Semantic understanding
- Examples:
  - Node label generation
  - Intent extraction from variable names
  - Business logic summarization

**Synergy:**
```
1. GNN identifies "complex business logic block" in CFG
2. Extract source code for that block
3. CodeT5 generates: "Verify user has admin privileges"
   Instead of: "checkPermissions(user, level)"
```

**Comparison Table:**

| Capability | GNN | CodeT5 | Hybrid |
|------------|-----|--------|--------|
| Primary Input | Graph (CFG) | Text (Code) | Graph + Text |
| Core Strength | Structural patterns | Semantic meaning | **Structure + Meaning** |
| Ideal Use | Pattern detection | Code summarization | **Find pattern → Summarize** |
| Recommendation | Use for structure | Use for semantics | **✅ Adopt as primary** |

---

## 🚀 Phased Implementation Plan

### Phase 1: The Generation Backbone (2-3 weeks)

**Goal:** Досягти 100% valid diagram generation

**Tasks:**
1. Develop Node.js microservice
   - Express.js API endpoint: `/generate`
   - Puppeteer integration
   - Instance pooling for performance

2. Create minimal HTML host page
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <script src="drakonwidget.js"></script>
   </head>
   <body id="editor"></body>
   </html>
   ```

3. Implement API wrapper
   - High-level commands: `createDiagram()`, `addNode()`, `connect()`
   - Expose via HTTP

4. Refactor `code_to_drakon.py`
   - Replace manual JSON building
   - Send command list to Node.js service
   - Receive validated JSON

**Deliverable:**
- ✅ Future-proof generation (auto-updates with drakonWidget)
- ✅ Same diagram quality as current, but guaranteed valid

---

### Phase 2: Deep Control Flow Analysis (3-4 weeks)

**Goal:** Досягти 15-20+ вузлів для складних функцій

**Tasks:**
1. Integrate CFG libraries
   - Python: `py2cfg`
   - TypeScript: `styx` or `esgraph`

2. Rewrite Diagram Logic Builder
   - Traverse CFG instead of AST
   - Map basic blocks → DRAKON nodes
   - Map edges → connections

3. Implement CFG → DRAKON mapping
   - Branches (if-else)
   - Loops (while, for)
   - Exception paths (try-catch-finally)

**Expected Result:**
```
Before (AST-based):
handleUserRequest() → 4-6 nodes

After (CFG-based):
handleUserRequest() → 15-20 nodes
- All conditional paths
- Exception handling paths
- Nested loop iterations
```

---

### Phase 3: AI Enrichment (4-6 weeks, parallel з Phase 2)

**Goal:** Human-readable node labels, pattern detection

**Tasks:**

**3.1 CodeT5 Integration**
1. Setup CodeT5 model (Hugging Face)
2. Fine-tune on project code (optional)
3. Integrate into pipeline:
   ```python
   def generate_node_label(code_block):
       prompt = f"Summarize: {code_block}"
       label = codet5.generate(prompt)
       return label
   ```

**3.2 GNN Training (Stretch Goal)**
1. Build dataset: CFGs + pattern labels
2. Train GNN (PyTorch Geometric)
3. Detect 3-5 key patterns:
   - State Machine
   - Observer pattern
   - Retry logic

**Expected Result:**
- Node labels: "Verify user has admin privileges" (not "checkPermissions()")
- Detected patterns highlighted in diagram
- >80% similarity vs human intent

---

### Phase 4: Advanced Visualization (2-3 weeks)

**Goal:** Hierarchical diagrams, async patterns

**Tasks:**

**4.1 Cognitive Complexity**
```python
def should_collapse(code_block, user_detail_level):
    complexity = calculate_cognitive_complexity(code_block)
    threshold = 25 - (user_detail_level * 4)
    return complexity > threshold
```

**4.2 Detail Levels (1-5)**
- Level 1: Overview (collapse all loops/complex blocks)
- Level 3: Default (balanced)
- Level 5: Exhaustive (every statement)

**4.3 Specialized Patterns**
- Async/await → Promise Graph visualization
- State machines → UML State Diagram style

---

## 📈 Projected Improvements

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Avg nodes (complex fn) | 4-6 | 20-30 | **4-6x** |
| Control flow coverage | ~50% | >95% | **+45%** |
| Compatibility | Manual tracking | 100% guaranteed | **∞** |
| Node label quality | Literal code | AI-generated intent | **Human-like** |

---

## ⚠️ Risk Analysis & Mitigation

### Risk 1: drakonWidget API Changes
**Probability:** Medium | **Impact:** High

**Mitigation:**
1. **Anti-Corruption Layer:** Node.js service isolates rest of system
2. **Integration Tests:** Snapshot testing on canonical diagrams
3. **Fallback:** Direct .drn SQLite generation

---

### Risk 2: Performance (Headless Browser)
**Probability:** High | **Impact:** Medium

**Mitigation:**
1. **Instance Pooling:**
   ```javascript
   const browserPool = new Pool({
     create: () => puppeteer.launch(),
     min: 2,
     max: 10
   });
   ```
   Eliminates startup overhead

2. **High-Performance Mode:**
   ```bash
   ./unified-motia-workflow.sh drakon --mode=sqlite
   ```
   Use .drn generation for bulk processing

---

### Risk 3: AI Hallucinations
**Probability:** Medium | **Impact:** Medium

**Mitigation:**
1. **Few-Shot Prompting:**
   ```
   Examples:
   Code: if (!user.isAdmin) return 403;
   Label: "Verify user is admin"

   Code: await db.save(record);
   Label: "Save record to database"

   Now summarize: {code_block}
   ```

2. **Confidence Scoring:**
   ```python
   label, confidence = codet5.generate_with_score(code)
   if confidence < 0.7:
       label = fallback_label(code)  # Use function name
   ```

---

## 🛠️ Tool & Library Recommendations

| Category | Tool | Language | Rationale |
|----------|------|----------|-----------|
| **AST Parsing** | tree-sitter | Python/JS | Already in use |
| **CFG Generation** | py2cfg | Python | Generates CFGs from Python 3 |
| | styx | TypeScript | CFGs from ESTree ASTs |
| **DFA** | CodeQL | Python/TS | Industry-leading static analysis |
| **Headless Browser** | Puppeteer | Node.js | Robust Chrome automation |
| **Web Service** | Express.js | Node.js | Fast, mature framework |
| **LLM** | CodeT5 | Python | Open-source code understanding |
| **GNN** | PyTorch Geometric | Python | Flexible GNN framework |

---

## 📋 Next Steps

### Immediate Actions (This Week)

1. ✅ **Проаналізовано дослідження Gemini** (completed)

2. **Review з командою:**
   - Обговорити phased plan
   - Затвердити гібридну стратегію
   - Вибрати пріоритет: Phase 1 first or Phase 2?

3. **Proof of Concept:**
   - Створити мінімальний Node.js + Puppeteer demo
   - Згенерувати 1 діаграму через headless drakonWidget
   - Виміряти performance

### Week 1-2: Phase 1 Kickoff

4. **Setup Node.js microservice:**
   ```bash
   cd /home/vokov/motia_drn_start
   mkdir -p services/drakon-generator
   cd services/drakon-generator
   npm init -y
   npm install express puppeteer
   ```

5. **Implement `/generate` endpoint**

6. **Integration tests**

### Week 3-6: Phase 2 (CFG/DFA)

7. Integrate `py2cfg` for Python
8. Integrate `styx` for TypeScript
9. Rewrite diagram builder

### Week 7-12: Phase 3 (AI)

10. Setup CodeT5
11. Train GNN (optional)

### Week 13-15: Phase 4 (UX)

12. Cognitive Complexity
13. Detail levels

---

## 📚 Appendix: Code Examples from Research

### A.1 CFG Traversal Pseudocode

```python
def generateFromCFG(cfg, drakonBuilder):
    visited = set()
    worklist = [cfg.entry_block]

    while worklist:
        block = worklist.pop()
        if block in visited:
            continue
        visited.add(block)

        parent_node = process_block(block, drakonBuilder)

        for exit_link in block.exits:
            if exit_link.is_conditional():
                # Create branch node
                branch_id = drakonBuilder.addBranch(
                    condition=exit_link.condition,
                    parent=parent_node
                )
                # Connect yes/no paths
                connect(branch_id, 'one', exit_link.target)
                connect(branch_id, 'two', else_block)
            else:
                # Unconditional link
                connect(parent_node, 'one', exit_link.target)

            worklist.append(exit_link.target)
```

### A.2 Cognitive Complexity Mapping

```python
def shouldCollapseNode(code_block, user_detail_level):
    # user_detail_level: 1 (min) to 5 (max)
    complexity = calculateCognitiveComplexity(code_block)

    LOW = 10
    HIGH = 25

    # Higher detail = lower collapse threshold
    threshold = HIGH - (user_detail_level * 4)

    return complexity > threshold
```

---

## 🎯 Success Criteria (from Research)

**Minimum Viable:**
- ✅ 2x increase in node count
- ✅ 90%+ control flow coverage
- ✅ Maintain readability

**Stretch Goals:**
- ✅ AI-generated labels match human intent (>80%)
- ✅ Detect 15+ design patterns
- ✅ Multi-level diagrams (zoom)
- ✅ 100% compatibility with Stepan Mitkin's editors
- ✅ .drn format export support

---

## 📖 References (31 джерел)

Gemini включив посилання на:
1. drakonwidget GitHub repo
2. Puppeteer/Playwright docs
3. CodeQL documentation
4. Academic papers (Promise Graphs, GNNs, CodeT5)
5. .drn file format specification
6. Cognitive Complexity research

**Повний список:** Див. сторінки 22-24 PDF

---

**Статус:** ✅ Дослідження завершено
**Готовність до імплементації:** 🟢 HIGH
**Рекомендація:** Почати з Phase 1 (Node.js microservice) для швидкого ROI

**Наступний крок:** Створити Proof of Concept для headless drakonWidget
