# DRAKON Pipeline Module for Motia

**Version:** 1.0
**Created:** 2025-10-10
**Purpose:** Visual algorithm documentation using DRAKON flowcharts

## Overview

This module provides production-grade DRAKON diagram generation for Motia event-driven Steps. It converts algorithm pseudocode into visual DRAKON flowcharts compatible with Stepan Mitkin's official DRAKON ecosystem.

### What is DRAKON?

**DRAKON** is a visual algorithmic language originally developed for the **Buran space program** in Russia. Created by engineer **Stepan Mitkin**, it provides a standardized way to represent algorithms visually using a strict set of icons and layout rules.

**Key Principles:**
- **"Царська дорога" (Royal Road)** - Main execution path is always vertical
- **"Чем правее, тем хуже" (The further right, the worse)** - Error/exception handling on the right
- **No crossing lines** - Clean, readable diagrams

**Official Tools:**
- **DRAKON Editor** - Desktop application (C#/Qt) - [github.com/stepan-mitkin/drakon_editor](https://github.com/stepan-mitkin/drakon_editor)
- **DrakonWidget** - Browser-based viewer/editor (JavaScript) - [github.com/stepan-mitkin/drakonwidget](https://github.com/stepan-mitkin/drakonwidget)
- **DrakonHub** - Web collaboration platform - [drakonhub.com](https://drakonhub.com)

---

## Module Structure

```
/home/vokov/motia/tools/drakon/
├── converter/                      # DRAKON format converters
│   ├── drakon_to_drn.py           # SQLite .drn format (DRAKON Editor)
│   ├── drakon_to_json.py          # JSON format (DrakonWidget/DrakonHub)
│   ├── pseudocode_to_drakon.py    # [TODO] Pseudocode parser
│   └── format_validator.py        # [TODO] Format validation
│
├── perplexity/                     # Deep research integration
│   ├── perplexity_config.json     # Perplexity Labs API config
│   ├── perplexity_prompt.txt      # Comprehensive research prompt
│   ├── run_perplexity_lab.sh      # Research pipeline orchestrator
│   ├── research_output/           # Research results (auto-generated)
│   └── knowledge_base/            # Accumulated DRAKON knowledge
│
├── templates/                      # [TODO] DRAKON diagram templates
│   ├── action_template.json
│   ├── question_template.json
│   └── silhouette_template.json
│
├── tests/                          # [TODO] Test suite
│   ├── test_drn_export.py
│   └── test_json_compatibility.py
│
└── README.md                       # This file
```

---

## File Format Support

### 1. `.drn` Format (SQLite Database)

**Used by:** DRAKON Editor (desktop application)
**Implementation:** `converter/drakon_to_drn.py`

**Database Schema:**
```sql
CREATE TABLE diagrams (
    diagram_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    origin_x INTEGER DEFAULT 0,
    origin_y INTEGER DEFAULT 0,
    zoom REAL DEFAULT 1.0
);

CREATE TABLE icons (
    icon_id INTEGER PRIMARY KEY,
    diagram_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    w INTEGER NOT NULL,
    h INTEGER NOT NULL,
    text TEXT,
    format TEXT
);

CREATE TABLE links (
    link_id INTEGER PRIMARY KEY,
    diagram_id INTEGER NOT NULL,
    src_icon_id INTEGER NOT NULL,
    dst_icon_id INTEGER NOT NULL,
    vertices TEXT DEFAULT '[]'  -- JSON array: [[x,y], ...]
);
```

**Icon Types:**
- `action` - Action block
- `question` - Decision point (if/then/else)
- `select` - Switch/case
- `loopbegin` - Loop start
- `loopend` - Loop end
- `foreach` - For-each loop
- `branch` - Branch point
- `address` - Jump/goto
- `start` - Start point
- `end` - End point
- `parameters` - Function parameters
- `comment` - Comment annotation

**Usage:**
```python
from drakon_to_drn import DrnExporter, DrakonDiagram, DrakonIcon, DrakonLink

# Create exporter
exporter = DrnExporter(Path("my_algorithm.drn"))

# Build diagram
icons = [
    DrakonIcon(id=1, diagram_id=1, type='start', x=200, y=100, w=120, h=40, text='Start'),
    DrakonIcon(id=2, diagram_id=1, type='action', x=200, y=180, w=120, h=40, text='Process data'),
    DrakonIcon(id=3, diagram_id=1, type='end', x=200, y=260, w=120, h=40, text='End')
]

links = [
    DrakonLink(id=1, diagram_id=1, src_icon_id=1, dst_icon_id=2, vertices='[]'),
    DrakonLink(id=2, diagram_id=1, src_icon_id=2, dst_icon_id=3, vertices='[]')
]

diagram = DrakonDiagram(id=1, name="My Algorithm", icons=icons, links=links)

# Export
exporter.export_diagram(diagram)
exporter.close()

# Open in DRAKON Editor: File → Open → my_algorithm.drn
```

### 2. `.json` Format (DrakonWidget/DrakonHub)

**Used by:** DrakonWidget (browser), DrakonHub (web platform)
**Implementation:** `converter/drakon_to_json.py`

**JSON Structure:**
```json
{
  "diagram": {
    "name": "My Algorithm",
    "type": "drakon",
    "nodes": [
      {
        "id": 1,
        "type": "start",
        "text": "Start",
        "x": 200,
        "y": 100,
        "width": 120,
        "height": 40
      },
      {
        "id": 2,
        "type": "action",
        "text": "Process data",
        "x": 200,
        "y": 180,
        "width": 120,
        "height": 40
      }
    ],
    "links": [
      {
        "id": 1,
        "from": 1,
        "to": 2,
        "points": []
      }
    ],
    "settings": {
      "gridSize": 20,
      "zoom": 1.0,
      "theme": "default"
    }
  }
}
```

**Usage:**
```python
from drakon_to_json import JsonExporter, DrakonDiagramJSON, DrakonNode, DrakonLink

# Create exporter
exporter = JsonExporter(Path("my_algorithm.json"), pretty=True)

# Build diagram
nodes = [
    DrakonNode(id=1, type='start', text='Start', x=200, y=100, width=120, height=40),
    DrakonNode(id=2, type='action', text='Process data', x=200, y=180, width=120, height=40),
    DrakonNode(id=3, type='end', text='End', x=200, y=260, width=120, height=40)
]

links = [
    DrakonLink(id=1, source=1, target=2),
    DrakonLink(id=2, source=2, target=3)
]

diagram = DrakonDiagramJSON(name="My Algorithm", nodes=nodes, links=links)

# Export
exporter.export_diagram(diagram)

# Load in browser: https://drakonhub.com/editor
```

---

## Perplexity Labs Integration

The module includes deep research capabilities using **Perplexity Labs API** to gather comprehensive knowledge about the DRAKON ecosystem.

### Purpose

Automatically research:
- Complete `.drn` SQLite schema specifications
- Full JSON format documentation
- All DRAKON icon types and usage rules
- Conversion algorithms between formats
- Layout and rendering rules
- Validation constraints
- Real-world examples from official repositories

### Configuration

Edit `perplexity/perplexity_config.json`:

```json
{
  "perplexity_api": {
    "endpoint": "https://api.perplexity.ai/chat/completions",
    "model": "sonar-research",
    "api_key_env": "PERPLEXITY_API_KEY"
  },
  "request_parameters": {
    "temperature": 0.1,
    "max_tokens": 16000,
    "search_recency_filter": "month",
    "return_citations": true
  },
  "search_domain_filter": [
    "github.com",
    "stepan-mitkin.github.io",
    "drakonhub.com"
  ]
}
```

### Usage

```bash
# Set API key
export PERPLEXITY_API_KEY='your-api-key-here'

# Run full research pipeline
cd /home/vokov/motia/tools/drakon/perplexity
./run_perplexity_lab.sh research

# Check status
./run_perplexity_lab.sh status

# Validate research quality
./run_perplexity_lab.sh validate

# Get help
./run_perplexity_lab.sh help
```

### Pipeline Steps

1. **Validation** - Check environment, API key, dependencies
2. **Submission** - Send comprehensive research prompt to Perplexity Labs
3. **Processing** - Extract structured data from research results
4. **Extraction** - Parse SQL schemas, JSON structures, code samples
5. **Validation** - Verify against success criteria
6. **Reporting** - Generate summary report

### Output

```
perplexity/
├── research_output/
│   ├── raw/
│   │   └── perplexity_response_20251010_120000.json
│   ├── processed/
│   │   └── DRAKON_RESEARCH_20251010_120000.md
│   ├── schemas/
│   │   ├── drn_sql_schema.sql
│   │   └── json_schemas.json
│   ├── code_samples/
│   │   ├── sample_1.py
│   │   └── sample_2.js
│   └── citations.json
├── knowledge_base/
│   └── drakon_icon_types.json
└── logs/
    └── perplexity_research_20251010_120000.log
```

---

## Integration with Motia Workflow

### Current Integration

The DRAKON module is integrated with the unified Motia workflow for automatic diagram generation during Step creation.

**Workflow location:** `/home/vokov/motia/scripts/unified-motia-workflow.sh`

### Commands

```bash
# From project root
cd /home/vokov/motia

# Generate DRAKON diagrams for a Step
./scripts/unified-motia-workflow.sh drakon <step-name>

# Full pipeline (includes DRAKON generation)
./scripts/unified-motia-workflow.sh full-pipeline \
  <step-name> <type> <pattern> "<description>" <runtime>

# Example: Generate database-service with DRAKON diagrams
./scripts/unified-motia-workflow.sh full-pipeline \
  database-service noop "Repository + Facade" \
  "Data access layer with repository pattern" typescript
```

### Auto-Generated Diagrams

For each Motia Step, the following DRAKON diagrams are generated:

1. **`initialization.drn/.json`** - Initialization sequence
2. **`main-flow.drn/.json`** - Main execution flow
3. **`error-handling.drn/.json`** - Error handling logic
4. **`cleanup.drn/.json`** - Cleanup/teardown sequence

**Location:** `/home/vokov/motia/steps/<step-name>/diagrams/`

---

## Development Status

### ✅ Completed

- [x] `.drn` SQLite format exporter
- [x] `.json` DrakonWidget/DrakonHub format exporter
- [x] Perplexity Labs integration
- [x] Comprehensive research prompt
- [x] Research pipeline orchestrator
- [x] Auto-layout algorithms (vertical flow)
- [x] Icon type mappings
- [x] Sequential link generation

### 📋 Pending (TODO)

- [ ] **Pseudocode parser** (`converter/pseudocode_to_drakon.py`)
  - Parse algorithm descriptions from Step documentation
  - Convert to DRAKON node structures
  - Handle control flow (if/else, loops, switch)

- [ ] **Format validator** (`converter/format_validator.py`)
  - Validate .drn format against DRAKON Editor specs
  - Validate JSON format against DrakonWidget specs
  - Check structural constraints (royal road, no crossing lines)

- [ ] **DRAKON templates** (`templates/`)
  - Pre-built templates for common patterns
  - Observer, Command, Strategy, etc.

- [ ] **Test suite** (`tests/`)
  - Unit tests for converters
  - Integration tests with DRAKON Editor
  - Compatibility tests with DrakonHub

- [ ] **Advanced features**
  - Silhouettes (sub-diagrams)
  - Branch optimization
  - Multi-diagram files
  - Custom styling and themes

---

## Research Questions Addressed

The Perplexity research prompt (`perplexity/perplexity_prompt.txt`) seeks answers to:

### Critical Priority
- Complete SQLite schema for `.drn` files
- All fields in `icons`, `links`, `diagrams` tables
- Complete JSON schema for DrakonWidget/DrakonHub
- All supported node types and their identifiers
- Conversion process between `.drn` ↔ `.json`

### High Priority
- Complete list of DRAKON icon types
- Icon size constraints and default dimensions
- Real-world examples from public repositories
- Canonical "hello world" DRAKON diagrams

### Medium Priority
- Validation rules (structural constraints)
- Auto-layout algorithms
- API access (DrakonHub REST API)
- Rendering rules (spacing, coordinates)

### Low Priority
- Advanced features (silhouettes, nested diagrams)
- Code generation capabilities
- Export formats (PNG, SVG, PDF)

---

## References

### Official DRAKON Resources

- **Creator:** Stepan Mitkin - [github.com/stepan-mitkin](https://github.com/stepan-mitkin)
- **DRAKON Editor:** [github.com/stepan-mitkin/drakon_editor](https://github.com/stepan-mitkin/drakon_editor)
- **DrakonWidget:** [github.com/stepan-mitkin/drakonwidget](https://github.com/stepan-mitkin/drakonwidget)
- **DrakonHub:** [github.com/stepan-mitkin/drakonhub](https://github.com/stepan-mitkin/drakonhub)
- **Web Platform:** [drakonhub.com](https://drakonhub.com)
- **Official Site:** [drakon.su](https://drakon.su)

### Academic Papers

- "DRAKON: An Algorithmic Visual Programming Language"
- Original documentation from Buran space program

### Community Resources

- DRAKON forums and wikis
- Russian-language documentation
- Code examples in public repositories

---

## Contributing

To extend this module:

1. **Add new converter:**
   ```python
   # Create converter/my_format.py
   class MyFormatExporter:
       def export_diagram(self, diagram):
           # Implementation
   ```

2. **Add new template:**
   ```json
   // Create templates/my_pattern.json
   {
     "pattern": "My Pattern",
     "nodes": [...],
     "links": [...]
   }
   ```

3. **Add tests:**
   ```python
   # Create tests/test_my_feature.py
   def test_export():
       # Test implementation
   ```

4. **Update research:**
   - Modify `perplexity/perplexity_prompt.txt`
   - Run `./run_perplexity_lab.sh research`
   - Review findings in `research_output/`

---

## Troubleshooting

### DRAKON Editor won't open .drn file

**Cause:** Invalid SQLite schema or corrupted database

**Solution:**
```bash
# Validate SQLite file
sqlite3 my_diagram.drn "PRAGMA integrity_check;"

# Check schema
sqlite3 my_diagram.drn ".schema"

# Compare with reference
sqlite3 my_diagram.drn "SELECT * FROM meta WHERE key='version';"
```

### DrakonWidget shows empty diagram

**Cause:** Invalid JSON structure

**Solution:**
```bash
# Validate JSON
jq empty my_diagram.json

# Check required fields
jq '.diagram | keys' my_diagram.json

# Compare with template
diff <(jq -S . my_diagram.json) <(jq -S . templates/action_template.json)
```

### Perplexity research fails

**Cause:** Missing API key or network issue

**Solution:**
```bash
# Check API key
echo $PERPLEXITY_API_KEY

# Test connectivity
curl -I https://api.perplexity.ai

# Check logs
cat perplexity/logs/perplexity_research_*.log
```

---

## License

Part of the **Motia** project - Event-driven backend framework with AI-assisted development.

**Created by:** Claude Sonnet 4.5
**Date:** 2025-10-10
**Version:** 1.0

---

## Next Steps

1. **Run Perplexity research** to gather comprehensive DRAKON knowledge:
   ```bash
   export PERPLEXITY_API_KEY='your-key'
   cd tools/drakon/perplexity
   ./run_perplexity_lab.sh research
   ```

2. **Implement pseudocode parser** using research findings

3. **Create validation rules** based on official specifications

4. **Build template library** for common design patterns

5. **Test with DRAKON Editor** to ensure 100% compatibility

6. **Integrate with Motia Step generation** for automatic diagram creation

---

**For questions or issues, see:**
- `/home/vokov/motia/SESSION-CONTEXT.md` - Project overview
- `/home/vokov/motia/REFACTORING-CHECKLIST.md` - Migration guide
- `perplexity/RESEARCH_SUMMARY.md` - Research results (after running pipeline)
