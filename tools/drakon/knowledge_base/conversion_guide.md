# DRAKON Format Conversion Guide

**Version:** 1.0
**Date:** 2025-10-10
**Source:** Comprehensive Research (Perplexity + Claude Sonnet)
**Purpose:** Bidirectional conversion between .drn ↔ .json formats

---

## Overview

This guide provides complete specifications for converting between:
- **.drn format** → SQLite database (DRAKON Editor desktop)
- **.json format** → JSON structure (DrakonHub/DrakonWidget web)

---

## 🔄 Conversion Direction 1: .drn → .json

### Step 1: Read SQLite Database

```python
import sqlite3
import json

def read_drn_file(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row  # Access columns by name
    cursor = conn.cursor()

    # Read diagram metadata
    diagram = cursor.execute("""
        SELECT diagram_id, name, description, zoom, origin
        FROM diagrams
        LIMIT 1
    """).fetchone()

    # Read diagram properties
    properties = cursor.execute("""
        SELECT name, value
        FROM diagram_info
        WHERE diagram_id = ?
    """, (diagram['diagram_id'],)).fetchall()

    # Read all items
    items = cursor.execute("""
        SELECT item_id, type, text, text2, x, y, w, h, a, b, color
        FROM items
        WHERE diagram_id = ?
        ORDER BY y, x  -- Sort by position (top to bottom, left to right)
    """, (diagram['diagram_id'],)).fetchall()

    conn.close()

    return {
        'diagram': dict(diagram),
        'properties': {p['name']: p['value'] for p in properties},
        'items': [dict(item) for item in items]
    }
```

### Step 2: Convert Metadata

```python
def convert_metadata(drn_data):
    diagram = drn_data['diagram']
    properties = drn_data['properties']

    json_root = {
        'name': diagram['name'],
        'access': 'write'  # Default to write access
    }

    # Add optional fields
    if 'params' in properties:
        json_root['params'] = properties['params']

    if 'style' in properties:
        # Ensure style is JSON string
        json_root['style'] = properties['style']

    return json_root
```

### Step 3: Reconstruct Logical Connections from Geometry

**Critical:** .drn stores geometric positions; .json stores logical links

```python
def reconstruct_connections(items):
    """
    Infer logical connections from geometric positions.

    Connection rules:
    - one (down): Find item directly below (same x, greater y)
    - two (right): Find item directly right (same y, greater x)
    """
    connections = {}

    for item in items:
        item_id = str(item['item_id'])
        connections[item_id] = {'one': None, 'two': None}

        # Find next item down (one)
        # Look for items with similar x coordinate and greater y
        candidates_down = [
            other for other in items
            if abs(other['x'] - item['x']) < 10  # Tolerance for alignment
            and other['y'] > item['y']
        ]
        if candidates_down:
            # Choose closest one
            next_down = min(candidates_down, key=lambda i: i['y'])
            connections[item_id]['one'] = str(next_down['item_id'])

        # Find next item right (two)
        # Only for question/select types
        if item['type'] in ['question', 'select']:
            candidates_right = [
                other for other in items
                if abs(other['y'] - item['y']) < 10  # Tolerance
                and other['x'] > item['x']
            ]
            if candidates_right:
                next_right = min(candidates_right, key=lambda i: i['x'])
                connections[item_id]['two'] = str(next_right['item_id'])

    return connections
```

### Step 4: Convert Items to JSON Format

```python
def convert_items_to_json(drn_items):
    """Convert .drn items to .json format"""
    connections = reconstruct_connections(drn_items)
    json_items = {}

    for item in drn_items:
        item_id = str(item['item_id'])

        json_item = {
            'type': item['type']  # Type name stays same
        }

        # Add content (primary text)
        if item['text']:
            json_item['content'] = item['text']

        # Add secondary text (for shelf, input, output, process)
        if item['text2']:
            json_item['secondary'] = item['text2']

        # Add connections
        if connections[item_id]['one']:
            json_item['one'] = connections[item_id]['one']
        if connections[item_id]['two']:
            json_item['two'] = connections[item_id]['two']

        # Special fields
        if item['type'] == 'question' and item['b'] is not None:
            json_item['flag1'] = item['b']

        if item['type'] == 'branch':
            # Determine branchId from position (leftmost = 0)
            branch_items = [i for i in drn_items if i['type'] == 'branch']
            sorted_branches = sorted(branch_items, key=lambda b: b['x'])
            json_item['branchId'] = sorted_branches.index(item)

        # Convert color to style
        if item['color']:
            style = parse_color_to_style(item['color'])
            json_item['style'] = json.dumps(style)

        json_items[item_id] = json_item

    return json_items

def parse_color_to_style(color_str):
    """Parse .drn color format to style object"""
    # Format: "fg #rrggbb bg #rrggbb"
    parts = color_str.split()
    style = {}

    for i in range(0, len(parts), 2):
        if parts[i] == 'fg':
            style['color'] = parts[i+1]
        elif parts[i] == 'bg':
            style['background'] = parts[i+1]

    return style
```

### Step 5: Complete Conversion

```python
def drn_to_json(drn_filepath, json_filepath):
    """Complete .drn → .json conversion"""
    # Read .drn file
    drn_data = read_drn_file(drn_filepath)

    # Convert to JSON structure
    json_diagram = convert_metadata(drn_data)
    json_diagram['items'] = convert_items_to_json(drn_data['items'])

    # Write JSON file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_diagram, f, indent=2, ensure_ascii=False)

    print(f"✅ Converted {drn_filepath} → {json_filepath}")
    return json_diagram
```

---

## 🔄 Conversion Direction 2: .json → .drn

### Step 1: Read JSON File

```python
def read_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Step 2: Calculate Layout Positions

**Critical:** .json has logical structure; .drn needs geometric positions

```python
def calculate_layout(json_items):
    """
    Calculate geometric positions from logical structure.

    Layout algorithm:
    1. Identify branches (separate columns)
    2. Traverse 'one' links vertically
    3. Traverse 'two' links horizontally
    """
    # Constants
    START_X = 200
    START_Y = 100
    ICON_WIDTH = 120
    ICON_HEIGHT = 40
    VERTICAL_SPACING = 60
    HORIZONTAL_SPACING = 200

    positions = {}

    # Find all branches
    branches = {
        item_id: item
        for item_id, item in json_items.items()
        if item.get('type') == 'branch'
    }

    # Sort branches by branchId
    sorted_branches = sorted(
        branches.items(),
        key=lambda x: x[1].get('branchId', 0)
    )

    # Layout each branch column
    for branch_idx, (branch_id, branch) in enumerate(sorted_branches):
        base_x = START_X + branch_idx * (ICON_WIDTH + HORIZONTAL_SPACING)

        # Traverse main path (one links)
        current_id = branch_id
        current_y = START_Y
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            item = json_items[current_id]

            # Determine icon size
            item_type = item['type']
            if item_type in ['shelf', 'process', 'comment']:
                height = 60
            else:
                height = ICON_HEIGHT

            # Calculate center position
            positions[current_id] = {
                'x': base_x + (ICON_WIDTH // 2),  # Center X
                'y': current_y + (height // 2),    # Center Y
                'w': ICON_WIDTH // 2,              # Half-width!
                'h': height // 2,                  # Half-height!
                'type': item_type
            }

            # Move down
            current_y += height + VERTICAL_SPACING

            # Next item
            current_id = item.get('one')

    # Layout right branches (two links)
    for item_id, item in json_items.items():
        if item.get('two') and item['two'] in json_items:
            parent_pos = positions.get(item_id)
            if parent_pos:
                # Place to the right
                right_id = item['two']
                if right_id not in positions:
                    positions[right_id] = {
                        'x': parent_pos['x'] + HORIZONTAL_SPACING,
                        'y': parent_pos['y'],
                        'w': ICON_WIDTH // 2,
                        'h': ICON_HEIGHT // 2,
                        'type': json_items[right_id]['type']
                    }

    return positions
```

### Step 3: Create SQLite Database

```python
def create_drn_database(json_diagram, positions, drn_filepath):
    """Create .drn SQLite database from JSON"""
    import sqlite3

    # Remove existing file
    if Path(drn_filepath).exists():
        Path(drn_filepath).unlink()

    conn = sqlite3.connect(drn_filepath)
    cursor = conn.cursor()

    # Create schema (from knowledge_base/drn_complete_schema.sql)
    cursor.executescript("""
        CREATE TABLE info (key TEXT UNIQUE, value TEXT);
        CREATE TABLE state (row INTEGER UNIQUE DEFAULT 1, current_dia INTEGER, description TEXT);
        CREATE TABLE diagrams (diagram_id INTEGER UNIQUE PRIMARY KEY, name TEXT UNIQUE, origin TEXT, description TEXT, zoom DOUBLE DEFAULT 1.0);
        CREATE TABLE diagram_info (diagram_id INTEGER, name TEXT, value TEXT, PRIMARY KEY (diagram_id, name));
        CREATE TABLE items (item_id INTEGER UNIQUE PRIMARY KEY, diagram_id INTEGER, type TEXT NOT NULL, text TEXT, text2 TEXT, selected INTEGER DEFAULT 0, x INTEGER NOT NULL, y INTEGER NOT NULL, w INTEGER NOT NULL, h INTEGER NOT NULL, a INTEGER, b INTEGER, color TEXT, aux_value TEXT, format TEXT);
        CREATE TABLE tree_nodes (node_id INTEGER UNIQUE PRIMARY KEY, parent INTEGER, type TEXT, name TEXT, diagram_id INTEGER);
    """)

    # Insert metadata
    cursor.execute("INSERT INTO info VALUES ('type', 'drakon')")
    cursor.execute("INSERT INTO info VALUES ('version', '5')")
    cursor.execute("INSERT INTO info VALUES ('start_version', '1')")

    # Insert diagram
    cursor.execute("""
        INSERT INTO diagrams (diagram_id, name, origin, zoom)
        VALUES (1, ?, '0 0', 1.0)
    """, (json_diagram['name'],))

    # Insert state
    cursor.execute("INSERT INTO state VALUES (1, 1, NULL)")

    # Insert diagram properties
    if 'params' in json_diagram:
        cursor.execute("""
            INSERT INTO diagram_info VALUES (1, 'params', ?)
        """, (json_diagram['params'],))

    if 'style' in json_diagram:
        cursor.execute("""
            INSERT INTO diagram_info VALUES (1, 'style', ?)
        """, (json_diagram['style'],))

    # Insert items
    for item_id, item in json_diagram['items'].items():
        pos = positions.get(item_id, {
            'x': 0, 'y': 0, 'w': 60, 'h': 20
        })

        # Convert style to color format
        color = ''
        if 'style' in item:
            style = json.loads(item['style'])
            if 'color' in style or 'background' in style:
                fg = style.get('color', '#000000')
                bg = style.get('background', '#ffffff')
                color = f"fg {fg} bg {bg}"

        # Special parameters
        a = 0
        b = 0
        if item['type'] == 'question':
            b = item.get('flag1', 0)

        cursor.execute("""
            INSERT INTO items (item_id, diagram_id, type, text, text2, selected, x, y, w, h, a, b, color, aux_value, format)
            VALUES (?, 1, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, '', '')
        """, (
            int(item_id),
            item['type'],
            item.get('content', ''),
            item.get('secondary', ''),
            pos['x'],
            pos['y'],
            pos['w'],
            pos['h'],
            a,
            b,
            color
        ))

    conn.commit()
    conn.close()

    print(f"✅ Created {drn_filepath}")
```

### Step 4: Complete Conversion

```python
def json_to_drn(json_filepath, drn_filepath):
    """Complete .json → .drn conversion"""
    # Read JSON
    json_diagram = read_json_file(json_filepath)

    # Calculate layout
    positions = calculate_layout(json_diagram['items'])

    # Create database
    create_drn_database(json_diagram, positions, drn_filepath)

    print(f"✅ Converted {json_filepath} → {drn_filepath}")
```

---

## 📋 Validation After Conversion

### Validate .json Output

```python
def validate_json_diagram(diagram):
    errors = []

    # Required fields
    if 'name' not in diagram:
        errors.append("Missing required field: name")
    if 'access' not in diagram:
        errors.append("Missing required field: access")
    if 'items' not in diagram:
        errors.append("Missing required field: items")

    # Items structure
    if not isinstance(diagram.get('items'), dict):
        errors.append("items must be dictionary, not array")

    # Check each item
    for item_id, item in diagram.get('items', {}).items():
        if 'type' not in item:
            errors.append(f"Item {item_id} missing required field: type")

        # Validate references
        if 'one' in item and item['one'] not in diagram['items']:
            errors.append(f"Item {item_id} references non-existent item {item['one']}")
        if 'two' in item and item['two'] not in diagram['items']:
            errors.append(f"Item {item_id} references non-existent item {item['two']}")

    return errors
```

### Validate .drn Output

```python
def validate_drn_file(filepath):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    errors = []

    # Check required tables
    tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table'
    """).fetchall()
    table_names = {t[0] for t in tables}

    required_tables = {'info', 'state', 'diagrams', 'items'}
    missing_tables = required_tables - table_names
    if missing_tables:
        errors.append(f"Missing required tables: {missing_tables}")

    # Check metadata
    info = cursor.execute("SELECT key, value FROM info").fetchall()
    info_dict = {row[0]: row[1] for row in info}

    if info_dict.get('type') != 'drakon':
        errors.append("info.type must be 'drakon'")
    if info_dict.get('version') != '5':
        errors.append("info.version must be '5'")

    # Check items have reasonable coordinates
    items = cursor.execute("""
        SELECT item_id, x, y, w, h FROM items
    """).fetchall()

    for item_id, x, y, w, h in items:
        if w > 200 or h > 100:
            errors.append(f"Item {item_id} has suspiciously large w/h ({w}, {h}). Remember: w and h are half-values!")

    conn.close()
    return errors
```

---

## 🔧 Utility Functions

### Find Start Point

```python
def find_start_branch(items):
    """Find the start branch (lowest branchId)"""
    branches = {
        item_id: item
        for item_id, item in items.items()
        if item.get('type') == 'branch'
    }

    if not branches:
        raise ValueError("No branch found in diagram")

    start = min(branches.items(), key=lambda x: x[1].get('branchId', 0))
    return start[0]  # Return item_id
```

### Traverse Diagram

```python
def traverse_diagram(items, start_id=None):
    """Traverse diagram in execution order"""
    if start_id is None:
        start_id = find_start_branch(items)

    visited = set()
    execution_order = []

    def visit(item_id):
        if item_id in visited or item_id not in items:
            return

        visited.add(item_id)
        item = items[item_id]
        execution_order.append((item_id, item))

        # Visit 'one' (down)
        if 'one' in item:
            visit(item['one'])

        # Visit 'two' (right)
        if 'two' in item:
            visit(item['two'])

    visit(start_id)
    return execution_order
```

---

## 📚 Complete Example

```python
# Example: Round-trip conversion
def test_roundtrip():
    # Create test JSON diagram
    json_diagram = {
        "name": "Test Diagram",
        "access": "write",
        "items": {
            "1": {"type": "branch", "branchId": 0, "one": "2"},
            "2": {"type": "action", "content": "Initialize", "one": "3"},
            "3": {"type": "question", "content": "Valid?", "flag1": 0, "one": "4", "two": "5"},
            "4": {"type": "action", "content": "Process YES", "one": "6"},
            "5": {"type": "action", "content": "Process NO", "one": "6"},
            "6": {"type": "end"}
        }
    }

    # Convert JSON → DRN
    json_to_drn_temp = 'test_diagram.json'
    drn_temp = 'test_diagram.drn'

    with open(json_to_drn_temp, 'w') as f:
        json.dump(json_diagram, f)

    json_to_drn(json_to_drn_temp, drn_temp)

    # Convert DRN → JSON
    json_roundtrip = 'test_diagram_roundtrip.json'
    drn_to_json(drn_temp, json_roundtrip)

    # Validate
    with open(json_roundtrip, 'r') as f:
        result = json.load(f)

    errors_json = validate_json_diagram(result)
    errors_drn = validate_drn_file(drn_temp)

    print(f"JSON validation errors: {len(errors_json)}")
    print(f"DRN validation errors: {len(errors_drn)}")

    if errors_json:
        print("JSON errors:", errors_json)
    if errors_drn:
        print("DRN errors:", errors_drn)

if __name__ == '__main__':
    test_roundtrip()
```

---

## ⚠️ Common Pitfalls

1. **Forgetting half-width/height conversion** (.drn w/h are half-values!)
2. **Wrong coordinate system** (.drn uses center, not top-left)
3. **Incorrect connection inference** (must consider tolerance for floating point)
4. **Missing branch header** (every diagram needs at least one)
5. **Style format mismatch** (.json style must be JSON string)
6. **Wrong field names** (content vs text, items vs nodes)

---

**See also:**
- `knowledge_base/drn_complete_schema.sql` - Complete database schema
- `knowledge_base/icon_types.json` - Icon type reference
- `knowledge_base/gotchas.md` - Common mistakes to avoid
- `knowledge_base/validation_rules.json` - Validation rules
