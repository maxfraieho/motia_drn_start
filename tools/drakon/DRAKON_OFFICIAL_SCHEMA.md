# Official DrakonWidget JSON Schema

**Source:** DrakonWidget repository - `js/examples.js`
**Date Analyzed:** 2025-10-11
**Version:** Latest from GitHub

---

## Root Diagram Structure

```json
{
  "name": "string",           // REQUIRED: Diagram name
  "access": "write|read",     // OPTIONAL: Access mode (missing in examples!)
  "items": {                  // REQUIRED: Dictionary of items (string keys)
    "item_id": { ... }
  },
  "params": "string",         // OPTIONAL: Parameters (newline-separated)
  "style": "json_string"      // OPTIONAL: Diagram style as JSON string
}
```

### CRITICAL FINDING ⚠️

**Official examples DON'T have `"access"` field!**

Looking at official examples:
```json
{
  "name": "Adaptive design",
  "items": { ... }
}
```

```json
{
  "name": "Go out",
  "items": { ... }
}
```

**NO `"access"` field present!**

Our generated diagrams have:
```json
{
  "name": "test-step - Initialization",
  "access": "write",  // <-- This field is NOT in official examples!
  "items": { ... }
}
```

---

## Item Structure

### Base Fields (Common to All Items)

```json
{
  "type": "string",           // REQUIRED: Icon type
  "content": "string",        // OPTIONAL: Main text content
  "one": "string",            // OPTIONAL: ID of item below (vertical link)
  "two": "string",            // OPTIONAL: ID of item to the right (horizontal link)
  "side": "string",           // OPTIONAL: ID of duration marker (left link)
  "link": "string",           // OPTIONAL: External hyperlink
  "flag1": 0|1,               // OPTIONAL: Orientation flag
  "branchId": number,         // REQUIRED for branch: Branch number
  "margin": number,           // OPTIONAL: Left margin adjustment
  "style": "json_string"      // OPTIONAL: Item style (JSON as string!)
}
```

---

## Supported Icon Types

From official examples, here are ALL icon types found:

### 1. **branch** - Branch Header
```json
{
  "type": "branch",
  "branchId": 0,              // REQUIRED! First branch = 0, second = 1, etc.
  "one": "3",                 // Link to first item
  "content": "Optional title" // OPTIONAL: Branch name/title
}
```

**Example:**
```json
"2": {
  "type": "branch",
  "branchId": 0,
  "one": "3"
}
```

---

### 2. **action** - Action Block
```json
{
  "type": "action",
  "content": "Do something",
  "one": "next_id"
}
```

**Example:**
```json
"3": {
  "type": "action",
  "content": "Put on clothes",
  "one": "4"
}
```

---

### 3. **question** - Decision Point (If/Then/Else)
```json
{
  "type": "question",
  "content": "Is it raining?",
  "flag1": 0,                // 0 = YES down/NO right, 1 = NO down/YES right
  "one": "yes_branch_id",    // YES or NO depending on flag1
  "two": "no_branch_id"      // NO or YES depending on flag1
}
```

**Examples:**
```json
// flag1: 0 means YES goes down (one), NO goes right (two)
"4": {
  "flag1": 0,
  "type": "question",
  "content": "Is it raining?",
  "one": "7",   // YES
  "two": "5"    // NO
}

// flag1: 1 means NO goes down (one), YES goes right (two)
"12": {
  "flag1": 1,
  "type": "question",
  "content": "Did you understand the word?",
  "one": "13",  // NO
  "two": "14"   // YES
}
```

---

### 4. **select** - Switch/Case Start
```json
{
  "type": "select",
  "content": "What is the device type?",
  "one": "first_case_id"
}
```

**Example:**
```json
"6": {
  "type": "select",
  "content": "What is the device type?",
  "one": "5"
}
```

---

### 5. **case** - Case Branch
```json
{
  "type": "case",
  "content": "Phone",
  "one": "action_id",       // Action for this case
  "two": "next_case_id"     // Next case or end
}
```

**Example:**
```json
"7": {
  "type": "case",
  "one": "19",    // Action for Phone case
  "content": "Phone",
  "two": "3"      // Next case (Tablet)
}
```

---

### 6. **end** - End Point
```json
{
  "type": "end"
  // No "one" link - this is terminal
}
```

**Example:**
```json
"1": {
  "type": "end"
}
```

---

### 7. **insertion** - Call to Another Diagram
```json
{
  "type": "insertion",
  "content": "Leave the house",
  "one": "next_id"
}
```

**Example:**
```json
"7": {
  "type": "insertion",
  "content": "Leave the house",
  "one": "1"
}
```

---

### 8. **loopbegin** - Loop Start
```json
{
  "type": "loopbegin",
  "content": "For each word in the phrase",
  "one": "loop_body_id"
}
```

**Example:**
```json
"10": {
  "type": "loopbegin",
  "one": "11",
  "content": "For each word in the phrase"
}
```

---

### 9. **loopend** - Loop End
```json
{
  "type": "loopend",
  "content": "Next word",
  "one": "after_loop_id"
}
```

**Example:**
```json
"9": {
  "type": "loopend",
  "one": "15",
  "content": "Next word"
}
```

---

### 10. **arrow-loop** - Back Arrow (Loop Back)
```json
{
  "type": "arrow-loop",
  "one": "target_id"        // Points back to earlier item
}
```

**Example:**
```json
"16": {
  "type": "arrow-loop",
  "one": "8"
}
```

---

### 11. **parbegin** - Parallel Begin (Fork)
```json
{
  "type": "parbegin",
  "one": "thread1_id",
  "two": "thread2_id"       // Start second parallel thread
}
```

**Example:**
```json
"6": {
  "type": "parbegin",
  "one": "7",
  "two": "5"
}
```

---

### 12. **parend** - Parallel End (Join)
```json
{
  "type": "parend",
  "one": "after_join_id"
}
```

**Example:**
```json
"4": {
  "type": "parend",
  "one": "13"
}
```

---

### 13. **duration** - Time Duration Marker
```json
{
  "type": "duration",
  "content": "2 мин"
}
```

**Example:**
```json
"14": {
  "type": "duration",
  "content": "2 мин"
}
```

Used with `"side"` link from question:
```json
"11": {
  "type": "action",
  "content": "Вдувай 1 раз каждые 5-6 секунд",
  "one": "12",
  "side": "14"    // Links to duration marker
}
```

---

### 14. **group-duration** - Group Duration (with coordinates)
```json
{
  "type": "group-duration",
  "flag1": 1,
  "x": 590,
  "y": 270,
  "loX": -110,
  "loY": 75,
  "hiX": -470,
  "hiY": -100,
  "zIndex": 0,
  "content": "10 сек"
}
```

**Note:** This has geometric coordinates - layout information!

---

## Critical Rules

### 1. Item IDs MUST be strings

✅ **CORRECT:**
```json
"items": {
  "1": { "type": "branch", ... },
  "2": { "type": "action", ... }
}
```

❌ **WRONG:**
```json
"items": {
  1: { "type": "branch", ... },  // Integer keys - WRONG!
  2: { "type": "action", ... }
}
```

---

### 2. First item should be `branch` with `branchId: 0`

**Every diagram starts with:**
```json
"2": {
  "type": "branch",
  "branchId": 0,
  "one": "first_action_id"
}
```

Note: The item ID doesn't have to be "2", but conventionally it is.

---

### 3. Links must point to existing item IDs

All `one`, `two`, `side` values must be keys in the `items` dictionary.

---

### 4. Terminal items have no `one` link

Items with `type: "end"` don't have `"one"` field.

---

### 5. `params` is newline-separated string

```json
"params": "Author: Irina Kolosova\nhttps://youtu.be/JOtwQbNdIGs"
```

---

### 6. `style` is JSON serialized as string

```json
"style": "{\"iconBack\":\"darkgreen\",\"color\":\"white\"}"
```

**NOT an object:**
```json
"style": {"iconBack": "darkgreen"}  // WRONG!
```

---

## Complete Example (Minimal)

```json
{
  "name": "Go out",
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
      "one": "4",
      "content": "Put on clothes"
    },
    "4": {
      "flag1": 0,
      "type": "question",
      "content": "Is it raining?",
      "one": "7",
      "two": "5"
    },
    "5": {
      "type": "action",
      "one": "7",
      "content": "- Take umbrella\n- Take rubber boots"
    },
    "7": {
      "type": "insertion",
      "content": "Leave the house",
      "one": "1"
    }
  }
}
```

---

## Our Format vs Official Format

### What We Do WRONG ❌

1. **We add `"access": "write"` field**
   - Official examples DON'T have this!
   - Should be OPTIONAL, not always present

### What We Do RIGHT ✅

1. ✅ Item IDs are strings
2. ✅ `items` is a dictionary (not array)
3. ✅ Links use `one`, `two`, `side` properties
4. ✅ First item is `branch` with `branchId: 0`
5. ✅ `content` field for text (not `text`)

---

## Icon Types Summary

| Type | Purpose | Required Fields | Optional Fields |
|------|---------|----------------|-----------------|
| `branch` | Branch header | `type`, `branchId`, `one` | `content` |
| `action` | Action block | `type` | `content`, `one`, `link` |
| `question` | Decision | `type`, `one`, `two` | `content`, `flag1` |
| `select` | Switch start | `type`, `one` | `content` |
| `case` | Case branch | `type`, `one`, `two` | `content` |
| `end` | End point | `type` | - |
| `insertion` | Call diagram | `type`, `one` | `content` |
| `loopbegin` | Loop start | `type`, `one` | `content` |
| `loopend` | Loop end | `type`, `one` | `content` |
| `arrow-loop` | Back arrow | `type`, `one` | - |
| `parbegin` | Parallel fork | `type`, `one`, `two` | - |
| `parend` | Parallel join | `type`, `one` | - |
| `duration` | Time marker | `type` | `content` |
| `group-duration` | Group time | `type`, coordinates | `content` |

---

## Recommendations for Our Generator

### Fix #1: Make `access` field optional

**Current (WRONG):**
```python
diagram = {
    "name": f"{step_name} - Initialization",
    "access": "write",  # Always present
    "items": items
}
```

**Fixed (CORRECT):**
```python
diagram = {
    "name": f"{step_name} - Initialization",
    # "access": "write",  # REMOVE - official examples don't have it!
    "items": items
}
```

### Fix #2: Keep everything else as-is

Our format is already correct for:
- Item structure
- Link format
- Icon types
- String IDs

---

## Test Cases

### Test 1: Load Official Example
1. Copy "Go out" example from `examples.js`
2. Save as `test-official.json`
3. Load in DrakonWidget
4. Should render perfectly ✅

### Test 2: Load Our Generated Diagram
1. Remove `"access": "write"` from our diagram
2. Save as `test-ours.json`
3. Load in DrakonWidget
4. Should render perfectly ✅

---

**Conclusion:** We need to REMOVE the `"access"` field from our generator!
