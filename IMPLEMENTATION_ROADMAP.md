# DRAKON Enhancement Implementation Roadmap

**Based on:** Gemini AI Pro Research (2025-10-19)
**Source:** Enhancing DRAKON Diagram Generation.pdf
**Timeline:** 11-16 weeks (4 phases)

---

## 🎯 Strategic Goals

1. **100% Compatibility** with official DRAKON editors (drakonWidget, Desktop Editor)
2. **4-6x Detail Improvement** (from 4-6 nodes → 20-30 nodes for complex functions)
3. **AI-Enhanced Semantics** (human-readable node labels)
4. **Future-Proof Architecture** (auto-updates with drakonWidget changes)

---

## 📅 Phase 1: Generation Backbone (Weeks 1-3)

### Objective
Replace manual JSON generation with **headless drakonWidget microservice** → Guarantee 100% valid diagrams

### Architecture
```
Python Backend → Node.js Service → Puppeteer → Headless Chrome → drakonWidget.js → JSON
```

### Tasks

#### Week 1: Setup & Proof of Concept
- [ ] Create Node.js microservice skeleton
  ```bash
  mkdir -p services/drakon-generator
  cd services/drakon-generator
  npm init -y
  npm install express puppeteer
  ```
- [ ] Minimal HTML host page for drakonWidget
- [ ] Single diagram generation test

#### Week 2: API Development
- [ ] Implement `/generate` endpoint
- [ ] Command schema definition:
  ```json
  {
    "commands": [
      {"type": "createDiagram", "name": "Example"},
      {"type": "addNode", "nodeType": "action", "content": "..."},
      {"type": "connect", "from": "1", "to": "2"}
    ]
  }
  ```
- [ ] Puppeteer integration with instance pooling

#### Week 3: Integration & Testing
- [ ] Refactor `code_to_drakon.py` to use HTTP client
- [ ] Integration tests (10+ canonical diagrams)
- [ ] Performance benchmarking
- [ ] Fallback to .drn SQLite (if needed)

**Deliverable:**
- ✅ Future-proof diagram generation
- ✅ All existing diagrams migrate successfully
- ✅ Performance: < 5 seconds per function

---

## 📅 Phase 2: Deep Analysis Engine (Weeks 4-7)

### Objective
Implement **CFG + DFA** based analysis → Achieve 20-30 node diagrams

### Tasks

#### Week 4: CFG Integration
- [ ] Integrate `py2cfg` for Python
  ```bash
  pip install py2cfg
  ```
- [ ] Integrate `styx` for TypeScript
  ```bash
  npm install styx
  ```
- [ ] AST → CFG conversion pipeline

#### Week 5-6: Diagram Builder Rewrite
- [ ] New component: `CFGDiagramBuilder`
- [ ] Traverse CFG (not AST):
  - Basic blocks → DRAKON nodes
  - Edges → connections
- [ ] Map all constructs:
  - [x] Conditionals (if-else)
  - [x] Loops (while, for)
  - [x] Exception paths (try-catch-finally)

#### Week 7: Testing & Refinement
- [ ] Test on 50+ real functions
- [ ] Measure node count improvement
- [ ] Edge case handling

**Deliverable:**
- ✅ 15-20+ nodes for complex functions
- ✅ 95%+ control flow coverage
- ✅ Accurate exception handling visualization

---

## 📅 Phase 3: AI Enrichment (Weeks 4-10, parallel)

### Objective
**CodeT5** for semantic node labels + **GNN** for pattern detection

### Tasks

#### Week 4-5: CodeT5 Setup
- [ ] Install Hugging Face Transformers
  ```bash
  pip install transformers torch
  ```
- [ ] Load CodeT5 model:
  ```python
  from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
  
  tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
  model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")
  ```

#### Week 6-7: Node Label Generation
- [ ] Prompt engineering for action nodes
- [ ] Prompt engineering for condition nodes
- [ ] Integration into pipeline
- [ ] Few-shot learning examples

#### Week 8-10: GNN Pattern Detection (Stretch Goal)
- [ ] Create labeled CFG dataset (100+ examples)
- [ ] Train GNN (PyTorch Geometric)
- [ ] Detect patterns:
  - State Machine
  - Retry logic
  - Observer pattern

**Deliverable:**
- ✅ Human-readable node labels
- ✅ >80% similarity vs human intent
- ✅ Optional: Pattern detection highlights

---

## 📅 Phase 4: Advanced UX (Weeks 11-13)

### Objective
**Hierarchical diagrams** + **specialized patterns**

### Tasks

#### Week 11: Cognitive Complexity
- [ ] Implement Cognitive Complexity calculator
- [ ] Detail level mapping (1-5 scale)
- [ ] Auto-collapse high-complexity blocks

#### Week 12: Specialized Patterns
- [ ] Async/await → Promise Graph
- [ ] State machines → UML State Diagram style
- [ ] Event-driven patterns

#### Week 13: CLI & Documentation
- [ ] Add `--detail-level` flag:
  ```bash
  ./unified-motia-workflow.sh drakon my_func --detail-level=3
  ```
- [ ] Update documentation
- [ ] User guide

**Deliverable:**
- ✅ Interactive exploration (zoom levels)
- ✅ Modern construct support
- ✅ User-configurable detail

---

## 🔧 Alternative Path: Direct .drn Generation

**For high-performance batch processing**

### SQLite Schema Implementation
```python
import sqlite3

def generate_drn(diagram_data, output_path):
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE diagrams (
            diagram_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            zoom DOUBLE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE items (
            item_id INTEGER PRIMARY KEY,
            diagram_id INTEGER,
            type TEXT,
            text TEXT,
            one INTEGER,
            two INTEGER,
            x INTEGER, y INTEGER, w INTEGER, h INTEGER
        )
    ''')
    
    # Insert diagram
    cursor.execute("INSERT INTO diagrams VALUES (?, ?, ?)", 
                   (1, diagram_data['name'], 1.0))
    
    # Insert items
    for item_id, item in diagram_data['items'].items():
        cursor.execute("""
            INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, 0, 0, 100, 50)
        """, (int(item_id), 1, item['type'], item.get('content', ''),
              item.get('one'), item.get('two')))
    
    conn.commit()
    conn.close()
```

**Use Cases:**
- Batch processing (1000+ files)
- CI/CD pipeline integration
- Fallback if headless service unavailable

---

## ⚙️ Infrastructure & DevOps

### Docker Compose Update
```yaml
version: '3.8'

services:
  drakon-viewer:
    # ... existing config

  drakon-generator:
    build: ./services/drakon-generator
    ports:
      - "3000:3000"
    environment:
      - PUPPETEER_HEADLESS=true
      - INSTANCE_POOL_SIZE=5
    volumes:
      - ./tools/drakon-viewer/public/js:/app/drakonwidget:ro
```

### CI/CD Integration
```bash
# In CI pipeline
./unified-motia-workflow.sh drakon --all-steps --mode=sqlite --ci
```

---

## 📊 Success Metrics & KPIs

| Metric | Baseline | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|----------|---------|---------|---------|---------|
| Avg Nodes | 4-6 | 4-6 | **15-20** | 15-20 | **20-30** |
| Compatibility | Manual | **100%** | 100% | 100% | 100% |
| CF Coverage | ~50% | ~50% | **95%+** | 95%+ | 95%+ |
| Label Quality | Literal | Literal | Literal | **AI-enhanced** | AI-enhanced |
| Detail Control | None | None | None | None | **User-configurable** |

---

## 🚨 Risk Management

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| drakonWidget API changes | Medium | High | Anti-corruption layer, tests, .drn fallback |
| Performance overhead | High | Medium | Instance pooling, .drn mode |
| AI hallucinations | Medium | Medium | Few-shot prompting, confidence scoring |
| Timeline overrun | Medium | Medium | Phased approach, parallel work |

---

## 🛠️ Technical Stack

### Required Libraries

**Python:**
```bash
pip install py2cfg staticfg transformers torch codeql requests
```

**Node.js:**
```bash
npm install express puppeteer playwright
```

**Optional (GNN):**
```bash
pip install torch-geometric
```

---

## 📋 Checklist: Pre-Implementation

Before starting Phase 1:
- [ ] Review Gemini research PDF (all team members)
- [ ] Approve phased roadmap
- [ ] Allocate resources (dev time)
- [ ] Setup development environment
- [ ] Create feature branch: `git checkout -b feature/ai-enhanced-drakon`

---

## 🎯 Quick Start (Week 1, Day 1)

```bash
# 1. Create microservice
cd /home/vokov/motia_drn_start
mkdir -p services/drakon-generator
cd services/drakon-generator

# 2. Initialize
npm init -y
npm install express puppeteer

# 3. Create server.js
cat > server.js << 'JS'
const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
app.use(express.json());

let browserPool = [];

// Initialize browser pool
async function initPool() {
  for (let i = 0; i < 2; i++) {
    const browser = await puppeteer.launch({ headless: true });
    browserPool.push(browser);
  }
  console.log('Browser pool initialized');
}

app.post('/generate', async (req, res) => {
  const { commands } = req.body;
  
  // Get browser from pool
  const browser = browserPool[0];
  const page = await browser.newPage();
  
  // Load drakonwidget
  await page.goto('file:///app/host.html');
  
  // Execute commands
  const result = await page.evaluate((cmds) => {
    // ... drakonWidget API calls
    return { success: true, json: {} };
  }, commands);
  
  await page.close();
  res.json(result);
});

initPool().then(() => {
  app.listen(3000, () => console.log('Server running on :3000'));
});
JS

# 4. Run
node server.js
```

---

## 📖 Documentation Updates Required

- [ ] Update `SUMMARY.md` with new architecture
- [ ] Create `services/drakon-generator/README.md`
- [ ] Update `unified-motia-workflow.sh --help`
- [ ] Add examples to `HOW_TO_USE_RESEARCH.md`

---

**Status:** 📋 Roadmap Created
**Next Action:** Review → Approve → Start Phase 1, Week 1
**Estimated Completion:** ~3-4 months from kickoff

---

_This roadmap is based on Gemini AI Pro's strategic recommendations. Adjustments may be needed based on team capacity and business priorities._
