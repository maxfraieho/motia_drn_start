# DRAKON Implementation Gotchas and Common Pitfalls

**Source:** Comprehensive Research + Analysis (2025-10-10)
**Status:** Production-Ready Reference
**Purpose:** Avoid critical mistakes when implementing DRAKON converters

---

## 🚨 CRITICAL GOTCHAS (Will Break Compatibility)

### 1. Half-Width/Half-Height Confusion

**Problem:** In .drn format, `w` and `h` fields are HALF of the actual dimensions

```python
# ❌ WRONG - This creates a 240×80 pixel icon!
icon = {'x': 100, 'y': 100, 'w': 120, 'h': 40}

# ✅ CORRECT - This creates a 120×40 pixel icon
icon = {'x': 100, 'y': 100, 'w': 60, 'h': 20}
```

**Why it matters:** DRAKON Editor will display icons at double the intended size
**Detection:** Icons appear oversized in DRAKON Editor
**Fix:** Always divide dimensions by 2 before setting w/h

```python
def create_icon(type, x, y, full_width, full_height):
    return {
        'x': x,
        'y': y,
        'w': full_width // 2,   # Half-width!
        'h': full_height // 2,  # Half-height!
        'type': type
    }
```

---

### 2. Center vs Corner Positioning

**Problem:** .drn uses center coordinates, not top-left

```python
# ❌ WRONG - Treating (x, y) as top-left corner
def get_bounds(icon):
    return {
        'left': icon['x'],
        'top': icon['y'],
        'right': icon['x'] + icon['w'],
        'bottom': icon['y'] + icon['h']
    }

# ✅ CORRECT - (x, y) is the geometric center
def get_bounds(icon):
    return {
        'left': icon['x'] - icon['w'],    # w is half-width
        'top': icon['y'] - icon['h'],     # h is half-height
        'right': icon['x'] + icon['w'],
        'bottom': icon['y'] + icon['h']
    }
```

**Why it matters:** Incorrect positioning breaks visual layout
**Detection:** Icons appear shifted by half their size
**Fix:** Always treat (x, y) as center point

---

### 3. Branch Execution Order

**Problem:** Assuming first item in dictionary is the start point

```javascript
// ❌ WRONG - Dictionary order is not guaranteed
const firstItem = Object.keys(items)[0];
startExecution(items[firstItem]);

// ✅ CORRECT - Find branch with lowest branchId
const startBranch = Object.values(items)
    .filter(item => item.type === 'branch')
    .reduce((min, item) =>
        (item.branchId || 0) < (min.branchId || 0) ? item : min
    );
startExecution(startBranch);
```

**Why it matters:** Execution may start at wrong point
**Detection:** Diagram executes in unexpected order
**Fix:** Always find branch with minimum branchId

---

### 4. TCL List Format for origin

**Problem:** Using JSON array syntax instead of TCL list

```python
# ❌ WRONG - JSON array format
origin = "[100, 200]"

# ❌ ALSO WRONG - Python list
origin = [100, 200]

# ✅ CORRECT - TCL list (space-separated string)
origin = "100 200"
```

**Why it matters:** DRAKON Editor won't parse origin correctly
**Detection:** Viewport position resets to (0, 0)
**Fix:** Use space-separated string format

---

### 5. Style as JSON String Embedding

**Problem:** Storing style as Python dict instead of JSON string

```python
# ❌ WRONG - Python dictionary
item['style'] = {'color': 'red', 'background': 'blue'}

# ✅ CORRECT - JSON string
item['style'] = '{"color":"red","background":"blue"}'
```

**Why it matters:** DRAKON Editor expects JSON string
**Detection:** Styles not applied in editor
**Fix:** Always use `json.dumps()` for style values

```python
import json

style_obj = {'color': 'red', 'background': 'blue'}
item['style'] = json.dumps(style_obj)  # Convert to JSON string
```

---

## ⚠️ ERROR-PRONE PATTERNS

### 6. Question Icon flag1 Confusion

**Problem:** Misunderstanding YES/NO orientation

```json
{
  "type": "question",
  "content": "Is valid?",
  "flag1": 0  // ← What does this mean?
}
```

**Correct interpretation:**
- `flag1 = 0`: YES goes down (one), NO goes right (two) — **DEFAULT**
- `flag1 = 1`: NO goes down (one), YES goes right (two) — **FLIPPED**

**Why it matters:** Logic branches execute backwards
**Detection:** Wrong branch executes for condition
**Fix:** Document which path is YES and which is NO

```python
# Good practice: explicit documentation
question = {
    'type': 'question',
    'content': 'Is user authenticated?',
    'flag1': 0,  # YES=down, NO=right
    'one': yes_path_id,
    'two': no_path_id
}
```

---

### 7. Color Field Format

**Problem:** Using hex color without 'fg'/'bg' prefixes

```python
# ❌ WRONG
color = "#ff0000"

# ❌ ALSO WRONG
color = "fg:#ff0000 bg:#00ff00"

# ✅ CORRECT
color = "fg #ff0000 bg #00ff00"  # Note: space after fg/bg, no colon
```

**Why it matters:** Colors won't display correctly
**Detection:** Icons display with default colors
**Fix:** Use exact format `"fg #rrggbb bg #rrggbb"`

---

### 8. Items vs Nodes Terminology

**Problem:** Using 'nodes' in JSON format (wrong field name)

```json
{
  "name": "My Diagram",
  "access": "write",
  "nodes": {...}  // ❌ WRONG field name
}

// ✅ CORRECT
{
  "name": "My Diagram",
  "access": "write",
  "items": {...}  // Must be 'items', not 'nodes'
}
```

**Why it matters:** DrakonHub/DrakonWidget won't recognize diagram
**Detection:** Diagram fails to load in web tools
**Fix:** Always use `items` for JSON format

---

### 9. Links as Separate Structure

**Problem:** Creating separate 'links' array instead of embedding in items

```json
// ❌ WRONG - Separate links array
{
  "items": {...},
  "links": [
    {"from": "1", "to": "2"}
  ]
}

// ✅ CORRECT - Links embedded in items
{
  "items": {
    "1": {
      "type": "action",
      "one": "2"  // Link embedded as property
    },
    "2": {
      "type": "end"
    }
  }
}
```

**Why it matters:** Separate links don't exist in official format
**Detection:** Connections not displayed
**Fix:** Embed connections as `one`, `two`, `side` properties

---

### 10. Missing Branch Header

**Problem:** Generating diagram without branch icon

```python
# ❌ WRONG - No branch header
items = {
    "1": {"type": "action", "content": "Do something"},
    "2": {"type": "end"}
}

# ✅ CORRECT - Always start with branch
items = {
    "1": {"type": "branch", "branchId": 0, "one": "2"},
    "2": {"type": "action", "content": "Do something", "one": "3"},
    "3": {"type": "end"}
}
```

**Why it matters:** Diagram structure is invalid
**Detection:** DRAKON tools reject diagram
**Fix:** Always prepend branch header with `branchId: 0`

---

## 📋 FORMAT-SPECIFIC GOTCHAS

### .drn Format (SQLite)

#### No Separate Links Table

```python
# ❌ WRONG - Creating links table
CREATE TABLE links (
    link_id INTEGER,
    src_icon_id INTEGER,
    dst_icon_id INTEGER
);

# ✅ CORRECT - Derive links from geometry
# Links are inferred from icon positions:
# - Icons below (y > current.y) are connected via vertical lines
# - Icons to right (x > current.x) are connected via horizontal lines
```

**Why it matters:** Official format doesn't use links table
**Detection:** File structure incompatible with DRAKON Editor
**Fix:** Remove links table, derive connections from positions

---

#### Items, Not Icons

```python
# ❌ WRONG table name
CREATE TABLE icons (...)

# ✅ CORRECT table name
CREATE TABLE items (...)
```

**Why it matters:** DRAKON Editor looks for 'items' table
**Detection:** Database schema error on open
**Fix:** Use 'items' as table name

---

### .json Format (DrakonHub/DrakonWidget)

#### No Diagram Wrapper

```json
// ❌ WRONG - Unnecessary wrapper
{
  "diagram": {
    "name": "...",
    "items": {...}
  }
}

// ✅ CORRECT - Direct root structure
{
  "name": "...",
  "access": "write",
  "items": {...}
}
```

**Why it matters:** Parser expects flat structure
**Detection:** Diagram not recognized
**Fix:** Remove 'diagram' wrapper

---

#### Content, Not Text

```json
// ❌ WRONG field name
{
  "type": "action",
  "text": "Do something"
}

// ✅ CORRECT field name
{
  "type": "action",
  "content": "Do something"
}
```

**Why it matters:** Field name mismatch
**Detection:** Text doesn't display
**Fix:** Use `content` for primary text

---

## 🔍 DETECTION CHECKLIST

Use this checklist to verify your implementation:

### .drn Format Validation

- [ ] All w/h values are half of full dimensions
- [ ] All x/y coordinates are center points
- [ ] origin field uses TCL format (space-separated)
- [ ] color field uses "fg #rrggbb bg #rrggbb" format
- [ ] Table named 'items', not 'icons'
- [ ] No separate 'links' table
- [ ] info table contains type='drakon', version='5'
- [ ] state table initialized with row=1
- [ ] All diagrams have at least one branch item

### .json Format Validation

- [ ] Root has name, access, items (no 'diagram' wrapper)
- [ ] items is object/dictionary, not array
- [ ] Item IDs are strings, not integers
- [ ] Links are properties (one, two), not separate array
- [ ] Uses 'content', not 'text'
- [ ] style values are JSON strings, not objects
- [ ] Every diagram starts with branch (branchId: 0)
- [ ] access field is present ('read' or 'write')

---

## 🛠️ DEBUGGING TIPS

### Visual Debugging

**Symptom:** Icons appear too large
**Cause:** Forgot to divide by 2 for w/h
**Fix:** Check icon creation code for half-value calculation

**Symptom:** Icons shifted from expected position
**Cause:** Treating x/y as top-left instead of center
**Fix:** Verify coordinate system conversion

**Symptom:** Diagram empty when opened
**Cause:** Missing branch header or wrong table names
**Fix:** Check database schema and first item type

### Execution Debugging

**Symptom:** Wrong execution order
**Cause:** Not finding correct start branch
**Fix:** Sort branches by branchId, use lowest

**Symptom:** Condition branches backwards
**Cause:** Misunderstanding flag1 orientation
**Fix:** Document YES/NO paths explicitly

---

## 📚 QUICK REFERENCE

### Dimension Conversion

| Full Size | w (half) | h (half) |
|-----------|----------|----------|
| 120×40    | 60       | 20       |
| 120×60    | 60       | 30       |
| 180×40    | 90       | 20       |
| 60×40     | 30       | 20       |

### Field Name Mapping

| Concept    | .drn format | .json format |
|------------|-------------|--------------|
| Primary text | text      | content      |
| Secondary text | text2   | secondary    |
| Next down  | (geometry)  | one          |
| Next right | (geometry)  | two          |
| Left marker | (geometry) | side         |
| Coordinates | x, y (center) | (not used) |
| Dimensions | w, h (half) | (not used)   |

### Required vs Optional

| Field     | .drn | .json | Notes |
|-----------|------|-------|-------|
| type      | ✅   | ✅    | Always required |
| text/content | ⭕ | ⭕  | Optional for most types |
| x, y      | ✅   | ❌    | .drn only |
| w, h      | ✅   | ❌    | .drn only (half-values!) |
| one       | ❌   | ⭕    | .json only (optional) |
| access    | ❌   | ✅    | .json only (required) |
| branchId  | ❌   | ✅    | .json only (for branch type) |

---

**Remember:** When in doubt, refer to official examples and test with DRAKON Editor!
