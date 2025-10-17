# DRAKON Visual Programming Language - Comprehensive Research Report

## Executive Summary

This report provides complete technical specifications for the DRAKON visual programming language ecosystem, including file formats, icon types, conversion methods, and implementation guidelines for building production-grade DRAKON converters compatible with Stepan Mitkin's official tools.

---

## Section 1: File Format Specifications

### 1.1 .drn Format (SQLite Database)

DRAKON Editor uses SQLite 3.6 database format for .drn files, with backward and forward compatibility guaranteed within major versions [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

#### Complete Database Schema

**info table** - File metadata and properties:
```sql
CREATE TABLE info (
    key TEXT UNIQUE,
    value TEXT
);
```

Typical content includes type (drakon), version number, start_version for major version, and language setting for code generation [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**diagrams table** - Diagram definitions:
```sql
CREATE TABLE diagrams (
    diagram_id INTEGER UNIQUE PRIMARY KEY,
    name TEXT UNIQUE,
    origin TEXT,  -- TCL list format: "x y"
    description TEXT,
    zoom DOUBLE DEFAULT 1.0
);
```

The origin field stores viewport position as a TCL list with X and Y coordinates, used for scrolling, while zoom represents the visible scale in percents where 100 means one-to-one mapping [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**state table** - Global state information:
```sql
CREATE TABLE state (
    row INTEGER UNIQUE DEFAULT 1,
    current_dia INTEGER REFERENCES diagrams(diagram_id),
    description TEXT
);
```

This table always contains only one row with the field 'row' equal to 1, storing the currently visible diagram reference [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**diagram_info table** - Per-diagram properties:
```sql
CREATE TABLE diagram_info (
    diagram_id INTEGER REFERENCES diagrams(diagram_id),
    name TEXT,
    value TEXT,
    PRIMARY KEY (diagram_id, name)
);
```

Export parameters are stored as diagram properties in key-value format [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**items table** - All diagram elements (icons, lines, connectors):
```sql
CREATE TABLE items (
    item_id INTEGER UNIQUE PRIMARY KEY,
    diagram_id INTEGER REFERENCES diagrams(diagram_id),
    type TEXT NOT NULL,
    text TEXT,
    text2 TEXT,  -- Secondary text for shelf icons
    selected INTEGER DEFAULT 0,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    w INTEGER NOT NULL,
    h INTEGER NOT NULL,
    a INTEGER,
    b INTEGER,
    color TEXT,  -- Format: "fg #000000 bg #aaaa00"
    aux_value TEXT,
    format TEXT
);
```

**tree_nodes table** - Tree view structure:
```sql
CREATE TABLE tree_nodes (
    node_id INTEGER UNIQUE PRIMARY KEY,
    parent INTEGER REFERENCES tree_nodes(node_id),
    type TEXT,  -- 'folder' or 'item'
    name TEXT,
    diagram_id INTEGER REFERENCES diagrams(diagram_id)
);
```

#### Item Type Coordinate Interpretations

**Rectangle-based icons** (action, beginend, end, question, address, etc.):
x and y are the geometric center coordinates, w is half the width, h is half the height, while a and b are ignored [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**Double-text icons** (shelf, input, output, process):
text2 contains secondary text placed in the upper text field, with 'a' representing the distance between top edge and horizontal middle line [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**Horizontal lines** (horizontal):
x and y are the left end coordinates, w is the distance between left and right ends, h is ignored, and 'a' encodes the line type [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

Line type encoding in field 'a':
- Plain: 0
- Left arrow: 40100
- Right arrow: 20100
- Left transparent arrow: 40200
- Right transparent arrow: 20200
- Left paw: 40300
- Right paw: 20300
- Parallel: 50100

**Vertical lines** (vertical):
x and y are the top end coordinates, w is ignored, h is the distance between top and bottom ends, and 'a' encodes the line type [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

Vertical line types:
- Plain: 0
- Up arrow: 10100
- Down arrow: 30100
- Up transparent arrow: 10200
- Down transparent arrow: 30200
- Up paw: 10300
- Down paw: 30300

**Arrow with two angles** (arrow):
x and y are the top end coordinates of the vertical segment, w is the length of upper horizontal segment, h is the height of vertical segment, 'a' is the length of lower horizontal segment, and 'b' is 0 for left-pointing or 1 for right-pointing [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**If icon** (question):
x and y are the geometric center, w is half the width, h is half the height, 'a' is the length of the horizontal line at right side, and 'b' is 0 if right exit is YES or 1 if right exit is NO [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**Comment icon** (comment):
x and y are the geometric center, w is half the width, h is half the height, 'a' is the length of the horizontal line at the side, and 'b' is 0 if line goes left or 1 if line goes right [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

**Branch header and footer** (branch, address):
x and y are the geometric center, w is half the width, h is half the height, 'a' is ignored, and 'b' is 1 if icon has a cycle mark or 0 if it doesn't [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

### 1.2 JSON Format (DrakonWidget/DrakonHub)

#### Complete JSON Structure

A minimal diagram requires name, access, and items properties, with the first icon on the diagram being the branch icon with the lowest branchId [GitHub](https://github.com/stepan-mitkin/drakonwidget) .

```json
{
  "name": "Diagram Name",
  "access": "write",
  "params": "param1\nparam2",
  "style": "{\"background\":\"grey\"}",
  "items": {
    "1": {
      "type": "end"
    },
    "2": {
      "type": "branch",
      "branchId": 0,
      "one": "3"
    },
    "3": {
      "type": "action",
      "content": "Hello!",
      "one": "1",
      "style": "{\"color\":\"yellow\"}"
    }
  }
}
```

#### Item Properties

Items are stored in a dictionary where keys are item ids, with required type property and optional content, secondary, link, one, two, side, flag1, branchId, margin, and style properties [GitHub](https://github.com/stepan-mitkin/drakonwidget) .

**Required fields:**
- `type` - Icon type identifier

**Optional fields:**
- `content` - Main content (must be string, can be JSON)
- `secondary` - Secondary content for double icons
- `link` - Link/reference text
- `one` - ID of next item below
- `two` - ID of next item to the right
- `side` - ID of duration item to the left
- `flag1` - YES/NO orientation for Question icon
- `branchId` - Branch ordinal for Branch icon
- `margin` - Additional left margin (in metre units)
- `style` - Item styling (must be JSON string)

**Diagram-level properties:**
- `name` - Diagram name (required)
- `access` - "read" or "write" (required)
- `params` - Parameters icon content
- `style` - Diagram style (JSON string)
- `items` - Items dictionary (required)

---

## Section 2: Icon Types and Structures

### 2.1 Complete Icon Type Reference

DrakonWidget supports the following item types for insertion: action, question, select, case, foreach, branch, insertion, comment, parblock, par, timer, pause, duration, shelf, process, input, output, ctrlstart, ctrlend, and drakon-image [GitHub](https://github.com/stepan-mitkin/drakonwidget) .

| Icon Type | Description | Usage | Required Links | Default Size |
|-----------|-------------|-------|----------------|--------------|
| **action** | Action/operation block | General code execution | 1 down | 120×40 |
| **question** | Decision point (if) | Binary branching | 1 down, 1 right | 120×40 |
| **select** | Switch/case construct | Multi-way branching | Multiple | 120×40 |
| **case** | Case branch option | Part of select | 1 down | 60×40 |
| **beginend** | Start/end marker | Algorithm boundaries | 1 down | 120×40 |
| **end** | Terminal end | Final termination | None | 120×40 |
| **loopbegin** | Loop start (for) | Loop initialization | 1 down | 120×40 |
| **loopend** | Loop end | Loop termination | 1 down | 120×40 |
| **foreach** | For-each loop | Collection iteration | 1 down | 120×40 |
| **branch** | Silhouette branch header | Branch definition | 1 down | 180×40 |
| **address** | Branch footer/jump | Next branch address | None | 180×40 |
| **comment** | Standalone comment | Documentation | 0-1 | 120×60 |
| **insertion** | Sub-routine call | Call external diagram | 1 down | 120×40 |
| **shelf** | Double-text container | Two-part content | 1 down | 120×60 |
| **input** | Input operation | Data input | 1 down | 120×40 |
| **output** | Output operation | Data output | 1 down | 120×40 |
| **process** | Process box | Sub-process | 1 down | 120×60 |
| **timer** | Timer operation | Real-time timing | 1 down | 120×40 |
| **pause** | Pause operation | Delay | 1 down | 120×40 |
| **duration** | Duration marker | Time measurement | 1 left | 60×40 |
| **parblock** | Parallel block | Concurrent start | Multiple | 120×40 |
| **par** | Parallel end | Concurrent join | 1 down | 120×40 |
| **ctrlstart** | Control start | State machine | 1 down | 120×40 |
| **ctrlend** | Control end | State machine | None | 120×40 |
| **drakon-image** | Image placeholder | Visual content | 1 down | Variable |

### 2.2 DRAKON Principles

The DRAKON diagram has several vertical sections called branches that represent logical decomposition, with branch names placed in the header to answer the Three Questions of the King: What is the name of the problem, how many parts does it have, and what are the names of the parts [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**The Skewer Principle:**
The entry and main exit of a branch are connected by a straight vertical line, with icons comprising the main path lying on that vertical line, called the skewer [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**The Main Route (царська дорога):**
The main route is the path leading to greatest success or the happy path, which must lie on the skewer, with the main route being immediately noticeable [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**Secondary Routes (чем правее, тем хуже):**
Secondary routes are placed to the right from the main route, following the rule that the further to the right, the worse it is, meaning the further away a route is from the main route, the less pleasant the situation it describes [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

### 2.3 Structural Rules

A branch has one entry and one or more exits, with the entry being a special icon at the top holding the branch name, and exits located at the bottom as either Address icons showing the next branch name or End icons marking algorithm termination [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**Branch Ordering:**
Branches are ordered from left to right according to their sequence in time, with the rule that going to the right is going forward in time [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**No Line Intersections:**
Line intersections and breaks are not allowed, as all types of line intersections are considered ergonomically harmful, with this ban being a serious topological limitation that has been mathematically proven to still allow expression of any possible algorithm [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**Joining Rules:**
After a horizontal joining the execution flow goes to the left, and after a vertical joining the execution flow goes down, ensuring readers don't need to think which direction to go [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

**Loop Arrows:**
A loop is the only situation when a line is directed upwards, with lines pointing up being rare exceptions that end with arrows, as all arrows inside a branch represent loops while other lines don't have arrow heads [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf) .

---

## Section 3: Conversion Guide

### 3.1 .drn to .json Conversion

**Step 1: Extract Diagram Metadata**
```python
# Read from .drn
SELECT d.diagram_id, d.name, d.description, d.zoom, d.origin
FROM diagrams d

# Map to JSON
{
  "name": name,
  "access": "write",
  "params": params_from_diagram_info,
  "style": style_from_diagram_info
}
```

**Step 2: Convert Items**
```python
# Read all items for diagram
SELECT item_id, type, text, text2, x, y, w, h, a, b, color
FROM items
WHERE diagram_id = ?

# Transform each item
for item in items:
    json_item = {
        "type": map_type(item.type),
        "content": item.text,
        "secondary": item.text2
    }
    
    # Calculate links based on geometry
    json_item["one"] = find_next_below(item)
    json_item["two"] = find_next_right(item)
    
    # Handle special fields
    if item.type == "question":
        json_item["flag1"] = item.b  # YES/NO orientation
    elif item.type == "branch":
        json_item["branchId"] = extract_branch_id(item)
```

**Step 3: Reconstruct Link Structure**

The .drn format stores geometric positions, while .json stores logical connections:

```python
def find_next_below(item):
    """Find item directly below this one"""
    # Look for items with x ≈ item.x and y > item.y
    # Return closest match
    
def find_next_right(item):
    """Find item to the right (for question/select)"""
    # Look for items with y ≈ item.y and x > item.x
    # Return closest match
```

**Type Mapping:**
- `beginend` → `branch` (for silhouettes)
- `loopbegin`/`loopend` → `foreach` (simplified)
- Most types map 1:1

### 3.2 .json to .drn Conversion

**Step 1: Create Database Structure**
```python
import sqlite3

conn = sqlite3.connect("output.drn")
cursor = conn.cursor()

# Create tables using schema from Section 1.1
# Insert metadata
cursor.execute("""
    INSERT INTO info (key, value) VALUES
    ('type', 'drakon'),
    ('version', '5'),
    ('start_version', '1')
""")
```

**Step 2: Layout Calculation**

For rectangle-based icons, x and y represent the geometric center, w is half the width, and h is half the height [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

```python
def calculate_layout(json_items):
    """Calculate geometric positions from logical structure"""
    
    # Constants
    ICON_WIDTH = 120
    ICON_HEIGHT = 40
    VERTICAL_SPACING = 60
    HORIZONTAL_SPACING = 200
    
    positions = {}
    branches = group_by_branch(json_items)
    
    x_offset = 100
    for branch_id, branch_items in enumerate(branches):
        y_offset = 100
        
        for item_id in branch_items:
            item = json_items[item_id]
            
            # Calculate center position
            x = x_offset + (ICON_WIDTH // 2)
            y = y_offset + (ICON_HEIGHT // 2)
            w = ICON_WIDTH // 2
            h = ICON_HEIGHT // 2
            
            positions[item_id] = {
                'x': x, 'y': y,
                'w': w, 'h': h,
                'a': 0, 'b': 0
            }
            
            y_offset += ICON_HEIGHT + VERTICAL_SPACING
        
        x_offset += ICON_WIDTH + HORIZONTAL_SPACING
    
    return positions
```

**Step 3: Insert Items**
```python
for item_id, item in json_items.items():
    pos = positions[item_id]
    
    cursor.execute("""
        INSERT INTO items (
            item_id, diagram_id, type,
            text, text2, selected,
            x, y, w, h, a, b,
            color, aux_value, format
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(item_id), 1, item["type"],
        item.get("content", ""), item.get("secondary", ""), 0,
        pos['x'], pos['y'], pos['w'], pos['h'], pos['a'], pos['b'],
        "", "", ""
    ))
```

---

## Section 4: Code Examples

### 4.1 Python .drn Exporter

```python
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DrakonIcon:
    id: int
    diagram_id: int
    type: str
    text: str
    x: int
    y: int
    w: int
    h: int
    a: int = 0
    b: int = 0
    text2: str = ""
    color: str = ""

@dataclass
class DrakonDiagram:
    id: int
    name: str
    icons: List[DrakonIcon]
    zoom: float = 1.0
    origin: str = "0 0"

class DrnExporter:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.conn = sqlite3.connect(filepath)
        self.cursor = self.conn.cursor()
        self._create_schema()
    
    def _create_schema(self):
        """Create DRAKON Editor database schema"""
        schema = """
        CREATE TABLE IF NOT EXISTS info (
            key TEXT UNIQUE,
            value TEXT
        );
        
        CREATE TABLE IF NOT EXISTS diagrams (
            diagram_id INTEGER UNIQUE PRIMARY KEY,
            name TEXT UNIQUE,
            origin TEXT,
            description TEXT,
            zoom DOUBLE DEFAULT 1.0
        );
        
        CREATE TABLE IF NOT EXISTS state (
            row INTEGER UNIQUE DEFAULT 1,
            current_dia INTEGER,
            description TEXT
        );
        
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER UNIQUE PRIMARY KEY,
            diagram_id INTEGER,
            type TEXT NOT NULL,
            text TEXT,
            text2 TEXT,
            selected INTEGER DEFAULT 0,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            w INTEGER NOT NULL,
            h INTEGER NOT NULL,
            a INTEGER,
            b INTEGER,
            color TEXT,
            aux_value TEXT,
            format TEXT
        );
        
        CREATE TABLE IF NOT EXISTS tree_nodes (
            node_id INTEGER UNIQUE PRIMARY KEY,
            parent INTEGER,
            type TEXT,
            name TEXT,
            diagram_id INTEGER
        );
        """
        self.cursor.executescript(schema)
        
        # Insert file metadata
        self.cursor.execute(
            "INSERT OR REPLACE INTO info VALUES ('type', 'drakon')"
        )
        self.cursor.execute(
            "INSERT OR REPLACE INTO info VALUES ('version', '5')"
        )
        self.cursor.execute(
            "INSERT OR REPLACE INTO info VALUES ('start_version', '1')"
        )
        self.conn.commit()
    
    def export_diagram(self, diagram: DrakonDiagram):
        """Export diagram to database"""
        # Insert diagram
        self.cursor.execute("""
            INSERT INTO diagrams (diagram_id, name, origin, zoom)
            VALUES (?, ?, ?, ?)
        """, (diagram.id, diagram.name, diagram.origin, diagram.zoom))
        
        # Insert icons
        for icon in diagram.icons:
            self.cursor.execute("""
                INSERT INTO items (
                    item_id, diagram_id, type, text, text2,
                    x, y, w, h, a, b, color
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                icon.id, icon.diagram_id, icon.type, icon.text, icon.text2,
                icon.x, icon.y, icon.w, icon.h, icon.a, icon.b, icon.color
            ))
        
        # Update state
        self.cursor.execute("""
            INSERT OR REPLACE INTO state (row, current_dia)
            VALUES (1, ?)
        """, (diagram.id,))
        
        self.conn.commit()
    
    def close(self):
        self.conn.close()

# Usage
exporter = DrnExporter(Path("example.drn"))
icons = [
    DrakonIcon(1, 1, "beginend", "Start", 100, 50, 60, 20),
    DrakonIcon(2, 1, "action", "Process", 100, 120, 60, 20),
    DrakonIcon(3, 1, "end", "End", 100, 190, 60, 20)
]
diagram = DrakonDiagram(1, "Example", icons)
exporter.export_diagram(diagram)
exporter.close()
```

### 4.2 JavaScript JSON Parser

```javascript
class DrakonJsonParser {
    constructor(jsonData) {
        this.diagram = jsonData;
        this.items = jsonData.items || {};
    }
    
    getStartItem() {
        // Find branch with lowest branchId
        let minBranchId = Infinity;
        let startItem = null;
        
        for (const [id, item] of Object.entries(this.items)) {
            if (item.type === 'branch') {
                const branchId = item.branchId || 0;
                if (branchId < minBranchId) {
                    minBranchId = branchId;
                    startItem = { id, ...item };
                }
            }
        }
        
        return startItem;
    }
    
    traverseItem(itemId) {
        const item = this.items[itemId];
        if (!item) return null;
        
        return {
            id: itemId,
            type: item.type,
            content: item.content || '',
            nextDown: item.one,
            nextRight: item.two,
            secondary: item.secondary
        };
    }
    
    getExecutionPath() {
        const path = [];
        let current = this.getStartItem();
        
        while (current) {
            path.push(current);
            
            // Follow 'one' link (down)
            if (current.one) {
                current = this.traverseItem(current.one);
            } else {
                break;
            }
        }
        
        return path;
    }
}

// Usage
const diagram = {
    name: "Example",
    access: "write",
    items: {
        "1": { type: "branch", branchId: 0, one: "2" },
        "2": { type: "action", content: "Step 1", one: "3" },
        "3": { type: "end" }
    }
};

const parser = new DrakonJsonParser(diagram);
const path = parser.getExecutionPath();
console.log(path.map(item => `${item.type}: ${item.content}`));
```

---

## Section 5: Sample Files

### 5.1 Minimal .drn File Structure

When opened with SQLite Browser, a minimal .drn file contains:

**info table:**
```
key             | value
----------------|-------
type            | drakon
version         | 5
start_version   | 1
```

**diagrams table:**
```
diagram_id | name    | origin | description | zoom
-----------|---------|--------|-------------|-----
1          | Example | 0 0    | NULL        | 1.0
```

**items table (3 icons):**
```
item_id | diagram_id | type     | text    | x   | y   | w  | h  | a | b
--------|------------|----------|---------|-----|-----|----|----|---|---
1       | 1          | beginend | Start   | 100 | 50  | 60 | 20 | 0 | 0
2       | 1          | action   | Process | 100 | 120 | 60 | 20 | 0 | 0
3       | 1          | end      | End     | 100 | 190 | 60 | 20 | 0 | 0
```

### 5.2 Minimal .json File

```json
{
  "name": "Minimal Example",
  "access": "write",
  "items": {
    "1": {
      "type": "branch",
      "branchId": 0,
      "one": "2"
    },
    "2": {
      "type": "action",
      "content": "Hello World",
      "one": "3"
    },
    "3": {
      "type": "end"
    }
  }
}
```

### 5.3 Complex Example with Branching

```json
{
  "name": "Conditional Logic",
  "access": "write",
  "items": {
    "1": {
      "type": "branch",
      "branchId": 0,
      "one": "2"
    },
    "2": {
      "type": "action",
      "content": "Initialize",
      "one": "3"
    },
    "3": {
      "type": "question",
      "content": "value > 0?",
      "flag1": 0,
      "one": "4",
      "two": "5"
    },
    "4": {
      "type": "action",
      "content": "Positive path",
      "one": "6"
    },
    "5": {
      "type": "action",
      "content": "Negative path",
      "one": "6"
    },
    "6": {
      "type": "end"
    }
  }
}
```

---

## Section 6: Best Practices

### 6.1 Layout Guidelines

**Vertical Spacing:**
- Icon center-to-center: 60-80 pixels
- Minimum clearance: 20 pixels
- The metre configuration parameter sets the minimum distance between icons, defaulting to 20 [GitHub](https://github.com/stepan-mitkin/drakonwidget)

**Horizontal Spacing:**
- Branch-to-branch: 180-220 pixels
- Question right branch: 140-180 pixels from main path

**Icon Sizing:**
Default icon dimensions are minWidth 100, maxWidth 500, and maxHeight 600 pixels, with padding of 10 pixels inside icons [GitHub](https://github.com/stepan-mitkin/drakonwidget)

### 6.2 Auto-Layout Algorithm

```python
def auto_layout_vertical(icons_data):
    """Automatic vertical layout following DRAKON principles"""
    
    START_Y = 100
    ICON_HEIGHT = 40
    SPACING = 60
    CENTER_X = 200
    
    positions = []
    current_y = START_Y
    
    for icon_data in icons_data:
        w = 60  # half-width
        h = 20  # half-height
        
        if icon_data['type'] in ['shelf', 'process', 'comment']:
            h = 30  # taller icons
        
        positions.append({
            'id': len(positions) + 1,
            'type': icon_data['type'],
            'text': icon_data['text'],
            'x': CENTER_X,
            'y': current_y + h,
            'w': w,
            'h': h
        })
        
        current_y += (h * 2) + SPACING
    
    return positions
```

### 6.3 Validation Rules

**Structural Validation:**
1. Every diagram must have at least one branch
2. A branch has one entry and one or more exits [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf)
3. Question icons must have exactly 2 outgoing connections
4. Select icons must have 2+ case icons immediately following
5. Loop constructs (foreach) must have matching begin/end pairs

**Topological Validation:**
6. Line intersections and breaks are not allowed [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf)
7. Arrows never point to icons, arrows point only to lines that go down [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf)
8. Never put any icon on a line that goes up or sideways [SourceForge](https://drakon-editor.sourceforge.net/DRAKON.pdf)

## Section 6: Best Practices (Continued)

### 6.4 Connection Validation

**Link Consistency Check:**
```python
def validate_links(json_diagram):
    """Validate link consistency in JSON format"""
    items = json_diagram.get('items', {})
    errors = []
    
    for item_id, item in items.items():
        # Check 'one' link exists
        if 'one' in item and item['one'] not in items:
            errors.append(f"Item {item_id} references non-existent item {item['one']}")
        
        # Check 'two' link exists (for branching)
        if 'two' in item and item['two'] not in items:
            errors.append(f"Item {item_id} references non-existent item {item['two']}")
        
        # Validate question icon has both paths
        if item['type'] == 'question':
            if 'one' not in item or 'two' not in item:
                errors.append(f"Question icon {item_id} missing required paths")
        
        # Validate end icon has no outgoing links
        if item['type'] == 'end':
            if 'one' in item or 'two' in item:
                errors.append(f"End icon {item_id} should not have outgoing links")
    
    return errors
```

### 6.5 Style and Theme Management

The theme object controls visual appearance with properties including background, iconBack, iconBorder, color, lineWidth, shadowColor, and icon-specific overrides [SourceForge](https://drakon-editor.sourceforge.net/howto.html) .

**Default Theme Configuration:**
```json
{
  "background": "#74a8fc",
  "iconBack": "white",
  "iconBorder": "black",
  "borderWidth": 1,
  "color": "black",
  "lineWidth": 1,
  "shadowBlur": 6,
  "shadowColor": "rgba(0, 0, 0, 0.2)",
  "icons": {
    "question": {
      "iconBack": "blue",
      "iconBorder": "black",
      "borderWidth": 0,
      "color": "yellow"
    }
  }
}
```

### 6.6 Content Formatting

The textFormat configuration can be plain, markdown, or html, controlling how content and secondary fields are interpreted [SourceForge](https://drakon-editor.sourceforge.net/howto.html) .

**Content Handling:**
```python
def sanitize_content(content, format_type='plain'):
    """Sanitize content based on format type"""
    if format_type == 'plain':
        # Remove HTML/markdown, keep plain text
        return strip_formatting(content)
    elif format_type == 'markdown':
        # Validate markdown syntax
        return validate_markdown(content)
    elif format_type == 'html':
        # Sanitize HTML
        return sanitize_html(content)
    return content

def format_for_export(content, max_width=500):
    """Format content for icon display"""
    lines = []
    words = content.split()
    current_line = []
    
    # Simple word wrapping
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > (max_width / 8):  # ~8px per char
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)
```

---

## Section 7: Gotchas and Common Pitfalls

### 7.1 Coordinate System Gotchas

**Problem 1: Half-Width Confusion**

For rectangle-based icons, w is half the width and h is half the height [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) , not the full dimensions.

```python
# WRONG
icon = {'x': 100, 'y': 100, 'w': 120, 'h': 40}  # This is 240×80 pixels!

# CORRECT
icon = {'x': 100, 'y': 100, 'w': 60, 'h': 20}   # This is 120×40 pixels
```

**Problem 2: Center vs Corner Positioning**

The .drn format uses center coordinates, while many drawing systems use top-left corners.

```python
def center_to_rect(x, y, w, h):
    """Convert DRAKON center coordinates to rectangle"""
    return {
        'left': x - w,
        'top': y - h,
        'width': w * 2,
        'height': h * 2
    }

def rect_to_center(left, top, width, height):
    """Convert rectangle to DRAKON center coordinates"""
    return {
        'x': left + (width // 2),
        'y': top + (height // 2),
        'w': width // 2,
        'h': height // 2
    }
```

### 7.2 Branch Ordering Issues

**Problem 3: Branch Execution Order**

The first icon on the diagram is the branch icon with the lowest branchId [SourceForge](https://drakon-editor.sourceforge.net/howto.html) , not the first item in the dictionary.

```javascript
// WRONG - assumes order
const firstItem = Object.keys(items)[0];

// CORRECT - find lowest branchId
function findStartBranch(items) {
    let minBranchId = Infinity;
    let startItem = null;
    
    for (const [id, item] of Object.entries(items)) {
        if (item.type === 'branch') {
            const branchId = item.branchId || 0;
            if (branchId < minBranchId) {
                minBranchId = branchId;
                startItem = id;
            }
        }
    }
    
    return startItem;
}
```

### 7.3 Loop Detection Pitfalls

**Problem 4: Infinite Loop Detection**

A line that is pointing up is such a rare exception that DRAKON ends that line with an arrow, with all arrows inside a branch representing loops [GitHub](https://github.com/stepan-mitkin/drakon_editor/blob/master/docs/drn%20file%20format/drn_file_format.html) .

```python
def detect_loop(item_id, items, visited=None):
    """Detect if item is part of a loop"""
    if visited is None:
        visited = set()
    
    if item_id in visited:
        return True  # Loop detected
    
    visited.add(item_id)
    
    item = items.get(item_id)
    if not item:
        return False
    
    # Check both paths
    if 'one' in item:
        if detect_loop(item['one'], items, visited.copy()):
            return True
    
    if 'two' in item:
        if detect_loop(item['two'], items, visited.copy()):
            return True
    
    return False
```

### 7.4 Text Encoding Issues

**Problem 5: TCL List Format for origin**

The origin is stored as a tcl list with two elements, the first element is X, the second element is Y [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

```python
# WRONG - JSON array
origin = "[100, 200]"  # This won't parse correctly

# CORRECT - TCL list (space-separated)
origin = "100 200"

def parse_tcl_list(tcl_string):
    """Parse TCL list format"""
    return [int(x) for x in tcl_string.split()]

def create_tcl_list(x, y):
    """Create TCL list format"""
    return f"{x} {y}"
```

### 7.5 Style JSON Embedding

**Problem 6: Nested JSON Strings**

The diagram style must be a string with JSON, and item style must be a string with JSON [SourceForge](https://drakon-editor.sourceforge.net/howto.html) .

```python
# WRONG - Python dict
item['style'] = {'color': 'red', 'background': 'blue'}

# CORRECT - JSON string
import json
item['style'] = json.dumps({'color': 'red', 'background': 'blue'})

# When reading
style_dict = json.loads(item['style']) if item.get('style') else {}
```

### 7.6 Question Icon Orientation

**Problem 7: flag1 Interpretation**

For the if icon, b is 0 if the right exit is YES or 1 if the right exit is NO [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

```python
def set_question_orientation(item, yes_goes_down=True):
    """Set question icon YES/NO orientation
    
    Args:
        yes_goes_down: If True, YES goes down (flag1=0)
                       If False, NO goes down (flag1=1)
    """
    if yes_goes_down:
        item['flag1'] = 0  # YES down, NO right
        item['b'] = 0      # For .drn format
    else:
        item['flag1'] = 1  # NO down, YES right
        item['b'] = 1      # For .drn format
```

### 7.7 Select/Case Structure

**Problem 8: Case Icon Placement**

The Case icons must immediately follow the Select icon, with no icons or joinings between the Select icon and the Case icons [GitHub](https://github.com/stepan-mitkin/drakon_editor/blob/master/docs/drn%20file%20format/drn_file_format.html) .

```python
def validate_select_structure(items):
    """Validate select/case structure"""
    errors = []
    
    for item_id, item in items.items():
        if item['type'] == 'select':
            # Find all outgoing paths
            next_items = []
            if 'one' in item:
                next_items.append(items.get(item['one']))
            if 'two' in item:
                next_items.append(items.get(item['two']))
            
            # All next items must be case icons
            for next_item in next_items:
                if next_item and next_item['type'] != 'case':
                    errors.append(
                        f"Select {item_id} must be followed by case icons, "
                        f"found {next_item['type']}"
                    )
    
    return errors
```

### 7.8 File Version Compatibility

**Problem 9: Version Mismatches**

DRAKON files are guaranteed to be backward and forward compatible within the major version, with no conversion needed when a new version comes out [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

```python
def check_version_compatibility(drn_file):
    """Check if .drn file version is compatible"""
    conn = sqlite3.connect(drn_file)
    cursor = conn.cursor()
    
    # Get version info
    cursor.execute("SELECT key, value FROM info WHERE key IN ('version', 'start_version')")
    versions = dict(cursor.fetchall())
    
    major = int(versions.get('start_version', '1'))
    minor = int(versions.get('version', '1'))
    
    # Check compatibility (example: we support 1.x)
    SUPPORTED_MAJOR = 1
    
    if major != SUPPORTED_MAJOR:
        raise ValueError(
            f"Incompatible major version {major}.{minor}. "
            f"Expected {SUPPORTED_MAJOR}.x"
        )
    
    conn.close()
    return True
```

### 7.9 Color Format Parsing

**Problem 10: Color Field Format**

The color field format is 'fg #000000 bg #aaaa00' where fg is foreground and text color, and bg is background color [SourceForge](https://drakon-editor.sourceforge.net/file_format.html) .

```python
def parse_color_field(color_string):
    """Parse DRAKON color field format"""
    if not color_string:
        return {'fg': None, 'bg': None}
    
    # Example: "fg #000000 bg #aaaa00"
    parts = color_string.split()
    result = {}
    
    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            key = parts[i]  # 'fg' or 'bg'
            value = parts[i + 1]  # '#rrggbb'
            result[key] = value
    
    return result

def create_color_field(fg_color=None, bg_color=None):
    """Create DRAKON color field format"""
    parts = []
    if fg_color:
        parts.extend(['fg', fg_color])
    if bg_color:
        parts.extend(['bg', bg_color])
    return ' '.join(parts)
```

### 7.10 Empty vs Missing Fields

**Problem 11: Distinguishing Empty from Missing**

```python
def safe_get_content(item, field, default=''):
    """Safely get content field handling None vs empty string"""
    value = item.get(field)
    
    # None means field doesn't exist
    if value is None:
        return default
    
    # Empty string is valid content
    return value

# Example usage
content = safe_get_content(item, 'content', default='<no content>')
secondary = safe_get_content(item, 'secondary', default='')
```

---

## Section 8: Advanced Implementation Topics

### 8.1 Silhouette (Multi-Branch) Handling

The DRAKON diagram has several vertical sections called branches representing a logical decomposition of the problem, with branch names placed in the header [GitHub](https://github.com/stepan-mitkin/drakon_editor/blob/master/docs/drn%20file%20format/drn_file_format.html) .

**Silhouette Structure:**
```python
class SilhouetteDiagram:
    """Represents a multi-branch silhouette diagram"""
    
    def __init__(self, name):
        self.name = name
        self.branches = []  # List of Branch objects
    
    def add_branch(self, branch_name, start_icon_id):
        """Add a branch to the silhouette"""
        branch = {
            'name': branch_name,
            'branchId': len(self.branches),
            'start_icon': start_icon_id,
            'icons': []
        }
        self.branches.append(branch)
        return branch
    
    def to_json(self):
        """Convert to JSON format"""
        items = {}
        
        for branch in self.branches:
            # Create branch header
            header_id = f"branch_{branch['branchId']}"
            items[header_id] = {
                'type': 'branch',
                'branchId': branch['branchId'],
                'one': branch['start_icon']
            }
            
            # Add branch icons
            for icon in branch['icons']:
                items[icon['id']] = icon
        
        return {
            'name': self.name,
            'access': 'write',
            'items': items
        }
```

### 8.2 Branch Loop Implementation

The branch loop occurs when an Address icon points to the same branch or a branch to the left, with both the Address icon and the branch start needing special cycle mark [GitHub](https://github.com/stepan-mitkin/drakon_editor/blob/master/docs/drn%20file%20format/drn_file_format.html) .

```python
def create_branch_loop(branches, loop_start_idx, loop_end_idx):
    """Create a branch loop structure
    
    Args:
        branches: List of branch dictionaries
        loop_start_idx: Index of branch where loop starts
        loop_end_idx: Index of branch where loop returns
    """
    # Mark loop start branch
    start_branch = branches[loop_start_idx]
    start_branch['cycle_mark'] = True
    start_branch['b'] = 1  # For .drn format
    
    # Mark loop end address icon
    end_branch = branches[loop_end_idx]
    end_address = end_branch['address_icon']
    end_address['cycle_mark'] = True
    end_address['b'] = 1  # For .drn format
    
    # Set address to point back
    end_address['text'] = start_branch['name']
    
    return branches
```

### 8.3 Auto-Layout for Complex Diagrams

**Multi-Branch Layout:**
```python
def layout_silhouette(branches_data):
    """Layout multiple branches side-by-side"""
    
    BRANCH_WIDTH = 200
    BRANCH_SPACING = 50
    START_X = 100
    START_Y = 100
    
    all_items = {}
    
    for branch_idx, branch_data in enumerate(branches_data):
        branch_x = START_X + (branch_idx * (BRANCH_WIDTH + BRANCH_SPACING))
        
        # Layout header
        header_id = f"h{branch_idx}"
        all_items[header_id] = {
            'type': 'branch',
            'branchId': branch_idx,
            'text': branch_data['name'],
            'x': branch_x + BRANCH_WIDTH // 2,
            'y': START_Y,
            'w': BRANCH_WIDTH // 2,
            'h': 20
        }
        
        # Layout branch icons vertically
        current_y = START_Y + 80
        for icon_data in branch_data['icons']:
            icon_id = icon_data['id']
            all_items[icon_id] = {
                **icon_data,
                'x': branch_x + BRANCH_WIDTH // 2,
                'y': current_y,
                'w': (BRANCH_WIDTH - 20) // 2,
                'h': 20
            }
            current_y += 60
        
        # Layout address at bottom
        address_id = f"a{branch_idx}"
        all_items[address_id] = {
            'type': 'address',
            'text': branch_data.get('next_branch', 'Exit'),
            'x': branch_x + BRANCH_WIDTH // 2,
            'y': current_y,
            'w': BRANCH_WIDTH // 2,
            'h': 20
        }
    
    return all_items
```

### 8.4 Code Generation from DRAKON

DRAKON-2 is a more low-level version that contains statements in a formal programming language like C++ or Java instead of free text, with the diagram being transformed into a source file during build time [GitHub](https://github.com/stepan-mitkin/drakon_editor/blob/master/docs/drn%20file%20format/drn_file_format.html) .

**Simple Code Generator:**
```python
class DrakonCodeGenerator:
    """Generate code from DRAKON diagram"""
    
    def __init__(self, diagram, language='python'):
        self.diagram = diagram
        self.language = language
        self.indent_level = 0
    
    def generate(self):
        """Generate code from diagram"""
        items = self.diagram['items']
        start_item = self.find_start_item(items)
        
        code_lines = []
        code_lines.append(f"def {self.diagram['name']}():")
        self.indent_level = 1
        
        # Generate function body
        body = self.generate_sequence(start_item, items, set())
        code_lines.extend(body)
        
        return '\n'.join(code_lines)
    
    def generate_sequence(self, item_id, items, visited):
        """Generate code for a sequence of items"""
        if not item_id or item_id in visited:
            return []
        
        visited.add(item_id)
        item = items[item_id]
        code = []
        indent = '    ' * self.indent_level
        
        if item['type'] == 'action':
            # Generate action code
            content = item.get('content', '').strip()
            if content:
                code.append(f"{indent}{content}")
            
            # Continue with next item
            if 'one' in item:
                code.extend(self.generate_sequence(item['one'], items, visited))
        
        elif item['type'] == 'question':
            # Generate if statement
            condition = item.get('content', 'condition')
            code.append(f"{indent}if {condition}:")
            
            # Generate then branch
            self.indent_level += 1
            if 'one' in item:
                code.extend(self.generate_sequence(item['one'], items, visited.copy()))
            self.indent_level -= 1
            
            # Generate else branch
            if 'two' in item:
                code.append(f"{indent}else:")
                self.indent_level += 1
                code.extend(self.generate_sequence(item['two'], items, visited.copy()))
                self.indent_level -= 1
        
        elif item['type'] == 'foreach':
            # Generate for loop
            loop_expr = item.get('content', 'item in collection')
            code.append(f"{indent}for {loop_expr}:")
            
            self.indent_level += 1
            if 'one' in item:
                code.extend(self.generate_sequence(item['one'], items, visited.copy()))
            self.indent_level -= 1
        
        elif item['type'] == 'end':
            code.append(f"{indent}return")
        
        return code
    
    def find_start_item(self, items):
        """Find the first item to execute"""
        # Find branch with lowest branchId
        for item_id, item in items.items():
            if item['type'] == 'branch' and item.get('branchId', 0) == 0:
                return item.get('one')
        return None
```

### 8.5 Diff and Merge for Version Control

**Diagram Comparison:**
```python
def diff_diagrams(old_diagram, new_diagram):
    """Compare two DRAKON diagrams"""
    old_items = old_diagram.get('items', {})
    new_items = new_diagram.get('items', {})
    
    changes = {
        'added': [],
        'removed': [],
        'modified': []
    }
    
    # Find added and modified items
    for item_id, new_item in new_items.items():
        if item_id not in old_items:
            changes['added'].append({
                'id': item_id,
                'type': new_item['type'],
                'content': new_item.get('content', '')
            })
        else:
            old_item = old_items[item_id]
            if old_item != new_item:
                changes['modified'].append({
                    'id': item_id,
                    'old': old_item,
                    'new': new_item
                })
    
    # Find removed items
    for item_id in old_items:
        if item_id not in new_items:
            changes['removed'].append({
                'id': item_id,
                'type': old_items[item_id]['type']
            })
    
    return changes

def generate_diff_report(changes):
    """Generate human-readable diff report"""
    report = []
    
    if changes['added']:
        report.append("Added items:")
        for item in changes['added']:
            report.append(f"  + [{item['type']}] {item['id']}: {item.get('content', '')}")
    
    if changes['removed']:
        report.append("\nRemoved items:")
        for item in changes['removed']:
            report.append(f"  - [{item['type']}] {item['id']}")
    
    if changes['modified']:
        report.append("\nModified items:")
        for item in changes['modified']:
            report.append(f"  * [{item['new']['type']}] {item['id']}")
            if item['old'].get('content') != item['new'].get('content'):
                report.append(f"      old: {item['old'].get('content', '')}")
                report.append(f"      new: {item['new'].get('content', '')}")
    
    return '\n'.join(report)
```

### 8.6 Performance Optimization

**Lazy Loading for Large Diagrams:**
```python
class LazyDrakonDiagram:
    """Lazy-loading wrapper for large diagrams"""
    
    def __init__(self, drn_file):
        self.conn = sqlite3.connect(drn_file)
        self.cursor = self.conn.cursor()
        self._cache = {}
    
    def get_diagram_info(self, diagram_id):
        """Get diagram metadata"""
        if diagram_id in self._cache:
            return self._cache[diagram_id]
        
        self.cursor.execute("""
            SELECT diagram_id, name, description, zoom, origin
            FROM diagrams WHERE diagram_id = ?
        """, (diagram_id,))
        
        row = self.cursor.fetchone()
        if row:
            info = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'zoom': row[3],
                'origin': row[4]
            }
            self._cache[diagram_id] = info
            return info
        return None
    
    def get_items_batch(self, diagram_id, offset=0, limit=100):
        """Get items in batches for large diagrams"""
        self.cursor.execute("""
            SELECT item_id, type, text, x, y, w, h
            FROM items
            WHERE diagram_id = ?
            ORDER BY item_id
            LIMIT ? OFFSET ?
        """, (diagram_id, limit, offset))
        
        return self.cursor.fetchall()
    
    def __del__(self):
        self.conn.close()
```

---

## Section 9: API Integration

### 9.1 DrakonHub API (Hypothetical)

While specific DrakonHub API documentation wasn't found in the research, here's a typical REST API implementation pattern:

```python
import requests
import json

class DrakonHubClient:
    """Client for DrakonHub API"""
    
    def __init__(self, api_key, base_url='https://api.drakonhub.com/v1'):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def upload_diagram(self, diagram_json):
        """Upload a diagram to DrakonHub"""
        response = self.session.post(
            f'{self.base_url}/diagrams',
            json=diagram_json
        )
        response.raise_for_status()
        return response.json()
    
    def get_diagram(self, diagram_id):
        """Download a diagram from DrakonHub"""
        response = self.session.get(
            f'{self.base_url}/diagrams/{diagram_id}'
        )
        response.raise_for_status()
        return response.json()
    
    def update_diagram(self, diagram_id, diagram_json):
        """Update an existing diagram"""
        response = self.session.put(
            f'{self.base_url}/diagrams/{diagram_id}',
            json=diagram_json
        )
        response.raise_for_status()
        return response.json()
    
    def list_diagrams(self, page=1, per_page=20):
        """List all diagrams"""
        response = self.session.get(
            f'{self.base_url}/diagrams',
            params={'page': page, 'per_page': per_page}
        )
        response.raise_for_status()
        return response.json()
```

### 9.2 DrakonWidget Embedding

DrakonWidget is a plain JavaScript file with no dependencies that can be used with any framework or without one [SourceForge](https://drakon-editor.sourceforge.net/howto.html) .

```html
<!DOCTYPE html>
<html>
<head>
    <title>Embedded DRAKON Diagram</title>
    <script src="drakonwidget.js"></script>
    <style>
        #editor-area {
            width: 100%;
            height: 600px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div id="editor-area"></div>
    
    <script>
        // Create widget instance
        var drakon = createDrakonWidget();
        
        // Build configuration
        var config = {
            startEditContent: function(item, isReadonly) {
                // Show content editor
                var newContent = prompt('Edit content:', item.content || '');
                if (newContent !== null) {
                    drakon.setContent(item.id, newContent);
                }
            },
            showContextMenu: function(left, top, items) {
                // Show context menu
                console.log('Context menu at', left, top);
            },
            canSelect: true,
            theme: {
                background: '#f0f0f0',
                iconBack: 'white',
                iconBorder: '#333'
            }
        };
        
        // Render widget
        var editorArea = document.getElementById('editor-area');
        var rect = editorArea.getBoundingClientRect();
        var widgetElement = drakon.render(rect.width, rect.height, config);
        editorArea.appendChild(widgetElement);
        
        // Create edit sender
        var sender = {
            stop: function() {},
            pushEdit: function(edit) {
                console.log('Edit:', edit);
                // Send to backend for persistence
            }
        };
        
        // Load diagram
        var diagram = {
            name: "Example Diagram",
            access: "write",
            items: {
                "1": { type: "branch", branchId: 0, one: "2" },
                "2": { type: "action", content: "Step 1", one: "3" },
                "3": { type: "end" }
            }
        };
        
        drakon.setDiagram("diagram-1", diagram, sender).then(function(fonts) {
            console.log('Diagram loaded, fonts:', fonts);
            drakon.redraw();
        });
    </script>
</body>
</html>
```

---

## Section 10: Testing and Quality Assurance

### 10.1 Unit Tests for Converters

```python
import unittest
import sqlite3
import json
from pathlib import Path

class TestDrnExporter(unittest.TestCase):
    """Test .drn file export"""
    
    def setUp(self):
        self.test_file = Path('test_diagram.drn')
        if self.test_file.exists():
            self.test_file.unlink()
    
    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
    
    def test_schema_creation(self):
        """Test database schema is created correctly"""
        exporter = DrnExporter(self.test_file)
        conn = sqlite3.connect(self.test_file)
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """)
        tables = {row[0] for row in cursor.fetchall()}
        
        self.assertIn('info', tables)
        self.assertIn('diagrams', tables)
        self.assertIn('items', tables)
        self.assertIn('state', tables)
        
        conn.close()
        exporter.close()
    
    def test_icon_insertion(self):
        """Test icon data is correctly inserted"""
        exporter = DrnExporter(self.test_file)
        
        icons = [
            DrakonIcon(1, 1, 'action', 'Test', 100, 100, 60, 20)
        ]
        diagram = DrakonDiagram(1, 'Test', icons)
        exporter.export_diagram(diagram)
        
        conn = sqlite3.connect(self.test_file)
        cursor = conn.cursor()
        cursor.execute("SELECT type, text FROM items WHERE item_id=1")
        row = cursor.fetchone()
        
        self.assertEqual(row[0], 'action')
        self.assertEqual(row[1], 'Test')
        
        conn.close()
        exporter.close()

class TestJsonExporter(unittest.TestCase):
    """Test JSON export"""
    
    def test_minimal_diagram(self):
        """Test minimal diagram export"""
        diagram = {
            'name': 'Test',
тести не дороблені, доробиш сам.