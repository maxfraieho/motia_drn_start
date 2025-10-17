-- DRAKON Editor .drn Format - Complete SQLite Schema
-- Version: 5 (official DRAKON Editor compatible)
-- Source: Perplexity + Claude Sonnet Deep Research (2025-10-10)
-- Reference: https://github.com/stepan-mitkin/drakon_editor

-- ============================================================================
-- METADATA TABLES
-- ============================================================================

-- Info table: File metadata and version information
CREATE TABLE IF NOT EXISTS info (
    key TEXT UNIQUE,
    value TEXT
);

-- Required metadata entries
INSERT OR REPLACE INTO info VALUES ('type', 'drakon');
INSERT OR REPLACE INTO info VALUES ('version', '5');
INSERT OR REPLACE INTO info VALUES ('start_version', '1');

-- Optional metadata
-- INSERT INTO info VALUES ('language', 'python');  -- For code generation
-- INSERT INTO info VALUES ('generator', 'Motia DRAKON Converter');

-- ============================================================================
-- STATE MANAGEMENT
-- ============================================================================

-- State table: Global editor state
CREATE TABLE IF NOT EXISTS state (
    row INTEGER UNIQUE DEFAULT 1,  -- Always = 1 (singleton pattern)
    current_dia INTEGER REFERENCES diagrams(diagram_id),  -- Currently selected diagram
    description TEXT
);

-- Initialize state
INSERT OR REPLACE INTO state (row, current_dia) VALUES (1, NULL);

-- ============================================================================
-- DIAGRAM STRUCTURE
-- ============================================================================

-- Diagrams table: Diagram metadata
CREATE TABLE IF NOT EXISTS diagrams (
    diagram_id INTEGER UNIQUE PRIMARY KEY,
    name TEXT UNIQUE,
    origin TEXT,  -- TCL list format: "x y" (viewport position, e.g., "0 0")
    description TEXT,
    zoom DOUBLE DEFAULT 1.0  -- Scale in percents (1.0 = 100%)
);

-- Diagram properties table: Extended diagram settings
CREATE TABLE IF NOT EXISTS diagram_info (
    diagram_id INTEGER REFERENCES diagrams(diagram_id),
    name TEXT,  -- Property name (e.g., 'language', 'params', 'style')
    value TEXT,  -- Property value
    PRIMARY KEY (diagram_id, name)
);

-- ============================================================================
-- DIAGRAM ELEMENTS (Icons, Lines, Connections)
-- ============================================================================

-- Items table: All diagram elements (icons + lines)
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER UNIQUE PRIMARY KEY,
    diagram_id INTEGER REFERENCES diagrams(diagram_id),
    type TEXT NOT NULL,  -- Icon type (see ICON TYPES section)
    text TEXT,           -- Primary text content
    text2 TEXT,          -- Secondary text (shelf, input, output, process)
    selected INTEGER DEFAULT 0,  -- Selection state (0 or 1)
    x INTEGER NOT NULL,  -- X coordinate (CENTER for icons, start for lines)
    y INTEGER NOT NULL,  -- Y coordinate (CENTER for icons, start for lines)
    w INTEGER NOT NULL,  -- Half-width for icons, length for horizontal lines
    h INTEGER NOT NULL,  -- Half-height for icons, length for vertical lines
    a INTEGER,           -- Special parameter (line types, distances)
    b INTEGER,           -- Orientation, cycle marks
    color TEXT,          -- Format: "fg #rrggbb bg #rrggbb"
    aux_value TEXT,      -- Auxiliary value
    format TEXT          -- JSON metadata
);

-- ============================================================================
-- PROJECT STRUCTURE
-- ============================================================================

-- Tree nodes table: Project tree structure
CREATE TABLE IF NOT EXISTS tree_nodes (
    node_id INTEGER UNIQUE PRIMARY KEY,
    parent INTEGER REFERENCES tree_nodes(node_id),
    type TEXT,  -- 'folder' or 'item'
    name TEXT,
    diagram_id INTEGER REFERENCES diagrams(diagram_id)
);

-- ============================================================================
-- ICON TYPES REFERENCE
-- ============================================================================

-- Icon types supported by DRAKON Editor (23 types):
--
-- Basic Flow Control:
--   - action: Action/operation (rectangle)
--   - question: Decision/if (diamond with rounded corners)
--   - select: Switch/case (hexagon)
--   - case: Case branch (part of select)
--   - beginend: Start/end marker
--   - end: Terminal point
--
-- Loops:
--   - loopbegin: Loop initialization
--   - loopend: Loop termination
--   - foreach: For-each iteration
--
-- Structure:
--   - branch: Branch header (silhouette)
--   - address: Branch footer/jump target
--
-- Documentation:
--   - comment: Comment box
--   - insertion: Sub-routine call
--
-- Input/Output:
--   - shelf: Double-text container
--   - input: Input operation
--   - output: Output operation
--   - process: Process box
--
-- Timing:
--   - timer: Timer operation
--   - pause: Pause/delay
--   - duration: Duration marker
--
-- Concurrency:
--   - parblock: Parallel block start
--   - par: Parallel end
--
-- State Machines:
--   - ctrlstart: Control start
--   - ctrlend: Control end
--
-- Visual:
--   - drakon-image: Image placeholder

-- ============================================================================
-- COORDINATE SYSTEM EXPLANATION
-- ============================================================================

-- CRITICAL: w and h are HALF-VALUES for rectangle-based icons!
--
-- Rectangle icons (action, beginend, end, question, address):
--   x, y = geometric center coordinates
--   w = HALF of total width
--   h = HALF of total height
--
-- Example: To create 120x40 action icon at center (100, 100):
--   INSERT INTO items VALUES (1, 1, 'action', 'Do something', '', 0,
--                            100, 100, 60, 20, 0, 0, '', '', '');
--                            --x  --y  --w --h  (w=120/2, h=40/2)
--
-- Double-text icons (shelf, input, output, process):
--   text2 = secondary text (upper field)
--   a = distance from top edge to horizontal dividing line
--
-- Horizontal lines:
--   x, y = coordinates of LEFT end
--   w = distance between left and right ends
--   h = ignored
--   a = line type encoding:
--       0 = plain line
--       40100 = left arrow
--       20100 = right arrow
--       60100 = both arrows
--
-- Vertical lines:
--   x, y = coordinates of TOP end
--   w = ignored
--   h = distance between top and bottom ends
--   a = line type encoding:
--       0 = plain line
--       10100 = up arrow
--       30100 = down arrow
--       50100 = both arrows
--
-- Question icon:
--   a = length of horizontal line to the right
--   b = 0 if right output is YES, 1 if right output is NO
--
-- Branch/Address icons:
--   b = 1 if icon has cycle mark (loop), 0 otherwise

-- ============================================================================
-- DEFAULT DIMENSIONS (full sizes, need to divide by 2 for w/h)
-- ============================================================================

-- action: 120x40
-- question: 120x40
-- select: 120x40
-- case: 60x40
-- beginend: 120x40
-- end: 120x40
-- loopbegin: 120x40
-- loopend: 120x40
-- foreach: 120x40
-- branch: 180x40
-- address: 180x40
-- comment: 120x60
-- insertion: 120x40
-- shelf: 120x60
-- input: 120x40
-- output: 120x40
-- process: 120x60
-- timer: 120x40
-- pause: 120x40
-- duration: 60x40
-- parblock: 120x40
-- par: 120x40
-- ctrlstart: 120x40
-- ctrlend: 120x40

-- ============================================================================
-- USAGE EXAMPLES
-- ============================================================================

-- Example 1: Create a simple diagram with 3 actions
--
-- INSERT INTO diagrams VALUES (1, 'Simple Flow', '0 0', NULL, 1.0);
-- INSERT INTO state VALUES (1, 1, NULL);
--
-- -- Branch header (required!)
-- INSERT INTO items VALUES (1, 1, 'branch', '', '', 0, 100, 50, 90, 20, 0, 0, '', '', '');
--
-- -- Action icons (note: w=60 is half of 120, h=20 is half of 40)
-- INSERT INTO items VALUES (2, 1, 'action', 'Step 1', '', 0, 100, 120, 60, 20, 0, 0, '', '', '');
-- INSERT INTO items VALUES (3, 1, 'action', 'Step 2', '', 0, 100, 200, 60, 20, 0, 0, '', '', '');
-- INSERT INTO items VALUES (4, 1, 'action', 'Step 3', '', 0, 100, 280, 60, 20, 0, 0, '', '', '');
--
-- -- End icon
-- INSERT INTO items VALUES (5, 1, 'end', '', '', 0, 100, 360, 60, 20, 0, 0, '', '', '');

-- Example 2: Question icon with branching
--
-- INSERT INTO items VALUES (10, 1, 'question', 'Valid?', '', 0, 100, 200, 60, 20, 150, 0, '', '', '');
-- --                                                            --x  --y  --w --h  --a  --b
-- -- a=150: horizontal line extends 150 pixels to the right
-- -- b=0: right output is YES (down is NO)

-- Example 3: Shelf icon with two text fields
--
-- INSERT INTO items VALUES (20, 1, 'shelf', 'Primary text', 'Secondary text', 0,
--                          100, 200, 60, 30, 15, 0, '', '', '');
-- --                                  --w --h  --a
-- -- w=60 (half of 120), h=30 (half of 60)
-- -- a=15: distance from top to dividing line

-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Check if database is valid:
-- SELECT * FROM info WHERE key IN ('type', 'version', 'start_version');

-- List all diagrams:
-- SELECT diagram_id, name, zoom FROM diagrams;

-- Count items per diagram:
-- SELECT diagram_id, COUNT(*) as item_count FROM items GROUP BY diagram_id;

-- Find all branch headers:
-- SELECT item_id, text FROM items WHERE type = 'branch';

-- Find orphaned items (no diagram reference):
-- SELECT item_id, type FROM items WHERE diagram_id NOT IN (SELECT diagram_id FROM diagrams);
