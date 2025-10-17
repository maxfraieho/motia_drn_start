#!/usr/bin/env python3
"""
DRAKON to .drn (SQLite) Converter

Converts internal DRAKON representation to Stepan Mitkin's .drn SQLite format
compatible with DRAKON Editor (desktop application).

.drn Format Structure:
- SQLite database with tables: diagrams, icons, links, texts, meta, settings
- Each icon has: id, diagram_id, type, x, y, w, h, text, format
- Links connect icons: id, diagram_id, src_icon_id, dst_icon_id, vertices (JSON array)

References:
- https://github.com/stepan-mitkin/drakon_editor
- DRAKON Editor source code: gui/model/database.py
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DrakonIcon:
    """DRAKON icon (node) representation

    CRITICAL: w and h are HALF-VALUES!
    For a 120x40 icon: w=60, h=20
    Coordinates (x, y) represent the GEOMETRIC CENTER, not top-left
    """
    id: int
    diagram_id: int
    type: str  # action, question, select, loopbegin, loopend, branch, address, start, end
    x: int  # Center X coordinate
    y: int  # Center Y coordinate
    w: int  # HALF of total width
    h: int  # HALF of total height
    text: str = ""
    text2: str = ""  # Secondary text (for shelf, input, output, process)
    selected: int = 0  # Selection state (0 or 1)
    a: int = 0  # Special parameters (line types, distances)
    b: int = 0  # Orientation, cycle marks
    color: str = ""  # Format: "fg #rrggbb bg #rrggbb"
    aux_value: str = ""
    format_str: str = ""  # Renamed from 'format' to avoid Python keyword conflict


@dataclass
class DrakonDiagram:
    """DRAKON diagram representation

    CRITICAL: Official .drn format does NOT use separate 'links' table!
    Links are inferred from geometric positions of icons.
    origin must be TCL list format: "x y" (space-separated string)
    """
    id: int
    name: str
    description: str = ""
    zoom: float = 1.0
    origin: str = "0 0"  # TCL list format: "x y"
    icons: List[DrakonIcon] = None
    params: str = ""  # Diagram parameters (optional)
    style: str = ""  # Diagram style (optional, JSON string)

    def __post_init__(self):
        if self.icons is None:
            self.icons = []


class DrnExporter:
    """Export DRAKON diagrams to .drn SQLite format"""

    # DRAKON icon types (from drakon_editor specification)
    ICON_TYPES = {
        'action': 'action',
        'question': 'question',
        'select': 'select',
        'case': 'case',
        'loop_begin': 'loopbegin',
        'loop_end': 'loopend',
        'for_loop': 'foreach',
        'branch': 'branch',
        'address': 'address',
        'start': 'start',
        'end': 'end',
        'params': 'parameters',
        'comment': 'comment'
    }

    # Default dimensions for icon types (in DRAKON grid units)
    ICON_DIMENSIONS = {
        'action': (120, 40),
        'question': (120, 60),
        'select': (120, 40),
        'loopbegin': (120, 30),
        'loopend': (120, 30),
        'foreach': (120, 40),
        'branch': (60, 60),
        'address': (80, 40),
        'start': (120, 40),
        'end': (120, 40),
        'parameters': (120, 40),
        'comment': (150, 60)
    }

    def __init__(self, output_path: Path):
        """
        Initialize DRN exporter

        Args:
            output_path: Path to output .drn file
        """
        self.output_path = Path(output_path)
        self.conn: Optional[sqlite3.Connection] = None

    def create_database_schema(self):
        """Create .drn database schema (DRAKON Editor compatible)

        Based on official DRAKON Editor specification v5
        Reference: knowledge_base/drn_complete_schema.sql
        """
        cursor = self.conn.cursor()

        # Info table: File metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS info (
                key TEXT UNIQUE,
                value TEXT
            )
        """)

        # State table: Global editor state
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state (
                row INTEGER UNIQUE DEFAULT 1,
                current_dia INTEGER REFERENCES diagrams(diagram_id),
                description TEXT
            )
        """)

        # Diagrams table: Diagram metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagrams (
                diagram_id INTEGER UNIQUE PRIMARY KEY,
                name TEXT UNIQUE,
                origin TEXT,
                description TEXT,
                zoom DOUBLE DEFAULT 1.0
            )
        """)

        # Diagram properties table: Extended diagram settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagram_info (
                diagram_id INTEGER REFERENCES diagrams(diagram_id),
                name TEXT,
                value TEXT,
                PRIMARY KEY (diagram_id, name)
            )
        """)

        # Items table: All diagram elements (icons + lines)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER UNIQUE PRIMARY KEY,
                diagram_id INTEGER REFERENCES diagrams(diagram_id),
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
            )
        """)

        # Tree nodes table: Project tree structure (optional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tree_nodes (
                node_id INTEGER UNIQUE PRIMARY KEY,
                parent INTEGER REFERENCES tree_nodes(node_id),
                type TEXT,
                name TEXT,
                diagram_id INTEGER REFERENCES diagrams(diagram_id)
            )
        """)

        # Insert required metadata
        cursor.execute("INSERT OR REPLACE INTO info VALUES ('type', 'drakon')")
        cursor.execute("INSERT OR REPLACE INTO info VALUES ('version', '5')")
        cursor.execute("INSERT OR REPLACE INTO info VALUES ('start_version', '1')")
        cursor.execute("INSERT OR REPLACE INTO info VALUES ('generator', 'Motia DRAKON Converter')")

        # Initialize state
        cursor.execute("INSERT OR REPLACE INTO state (row, current_dia) VALUES (1, NULL)")

        self.conn.commit()
        logger.info(f"✅ Created .drn database schema at {self.output_path}")

    def export_diagram(self, diagram: DrakonDiagram):
        """
        Export a DRAKON diagram to .drn format

        Args:
            diagram: DrakonDiagram object to export
        """
        if self.output_path.exists():
            logger.warning(f"Overwriting existing file: {self.output_path}")
            self.output_path.unlink()

        self.conn = sqlite3.connect(self.output_path)
        self.create_database_schema()

        cursor = self.conn.cursor()

        # Insert diagram
        cursor.execute("""
            INSERT INTO diagrams (diagram_id, name, origin, description, zoom)
            VALUES (?, ?, ?, ?, ?)
        """, (diagram.id, diagram.name, diagram.origin, diagram.description, diagram.zoom))

        # Update state to point to this diagram
        cursor.execute("""
            UPDATE state SET current_dia = ? WHERE row = 1
        """, (diagram.id,))

        # Insert diagram properties if present
        if diagram.params:
            cursor.execute("""
                INSERT INTO diagram_info (diagram_id, name, value)
                VALUES (?, 'params', ?)
            """, (diagram.id, diagram.params))

        if diagram.style:
            cursor.execute("""
                INSERT INTO diagram_info (diagram_id, name, value)
                VALUES (?, 'style', ?)
            """, (diagram.id, diagram.style))

        # Insert items (icons)
        for icon in diagram.icons:
            cursor.execute("""
                INSERT INTO items (
                    item_id, diagram_id, type, text, text2, selected,
                    x, y, w, h, a, b, color, aux_value, format
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                icon.id,
                icon.diagram_id,
                icon.type,
                icon.text,
                icon.text2,
                icon.selected,
                icon.x,
                icon.y,
                icon.w,
                icon.h,
                icon.a,
                icon.b,
                icon.color,
                icon.aux_value,
                icon.format_str
            ))

        self.conn.commit()
        logger.info(f"✅ Exported diagram '{diagram.name}' with {len(diagram.icons)} icons")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info(f"Database closed: {self.output_path}")

    @staticmethod
    def normalize_icon_type(icon_type: str) -> str:
        """
        Normalize icon type to DRAKON Editor format

        Args:
            icon_type: Internal icon type name

        Returns:
            DRAKON Editor compatible type name
        """
        normalized = icon_type.lower().replace('-', '_')
        return DrnExporter.ICON_TYPES.get(normalized, 'action')

    @staticmethod
    def calculate_layout(icons: List[Dict[str, Any]], vertical_spacing: int = 80) -> List[DrakonIcon]:
        """
        Calculate automatic layout for icons (simple vertical flow)

        CRITICAL: Returns icons with center coordinates and half-dimensions!
        For 120x40 icon: w=60 (half), h=20 (half)

        Args:
            icons: List of icon dictionaries from parser
            vertical_spacing: Space between icons

        Returns:
            List of DrakonIcon objects with calculated positions
        """
        drakon_icons = []
        current_y = 100  # Start position (top edge)
        base_x = 200     # Center column X

        for i, icon_data in enumerate(icons):
            icon_type = DrnExporter.normalize_icon_type(icon_data.get('type', 'action'))
            full_width, full_height = DrnExporter.ICON_DIMENSIONS.get(icon_type, (120, 40))

            # CRITICAL: w and h must be HALF of full dimensions
            half_w = full_width // 2
            half_h = full_height // 2

            # Calculate center position
            center_x = base_x
            center_y = current_y + half_h  # Center = top + half_height

            drakon_icon = DrakonIcon(
                id=i + 1,
                diagram_id=1,
                type=icon_type,
                x=center_x,     # Center X
                y=center_y,     # Center Y
                w=half_w,       # Half-width!
                h=half_h,       # Half-height!
                text=icon_data.get('text', ''),
                format_str=json.dumps({'style': 'default'})
            )

            drakon_icons.append(drakon_icon)
            current_y += full_height + vertical_spacing  # Move down by full height + spacing

        return drakon_icons

    @staticmethod
    def create_icon_with_full_dimensions(
        id: int,
        diagram_id: int,
        icon_type: str,
        center_x: int,
        center_y: int,
        full_width: int,
        full_height: int,
        text: str = ""
    ) -> DrakonIcon:
        """
        Helper: Create icon with full dimensions (automatically converts to half-values)

        CRITICAL: This helper handles the half-width/half-height conversion!

        Args:
            id: Icon ID
            diagram_id: Diagram ID
            icon_type: Icon type
            center_x: Center X coordinate
            center_y: Center Y coordinate
            full_width: FULL width (will be divided by 2)
            full_height: FULL height (will be divided by 2)
            text: Icon text

        Returns:
            DrakonIcon with correct half-dimensions
        """
        return DrakonIcon(
            id=id,
            diagram_id=diagram_id,
            type=icon_type,
            text=text,
            x=center_x,
            y=center_y,
            w=full_width // 2,   # Half-width!
            h=full_height // 2,  # Half-height!
        )


def example_usage():
    """Example: Convert pseudocode to .drn format"""

    # Example DRAKON structure (would come from parser)
    icons_data = [
        {'type': 'branch', 'text': ''},  # REQUIRED: Every diagram must start with branch!
        {'type': 'action', 'text': 'Initialize variables'},
        {'type': 'question', 'text': 'Is user authenticated?'},
        {'type': 'action', 'text': 'Load user data'},
        {'type': 'action', 'text': 'Process request'},
        {'type': 'end', 'text': ''}
    ]

    # Create exporter
    exporter = DrnExporter(Path("example_diagram.drn"))

    # Calculate layout (automatically uses half-dimensions and center coordinates)
    icons = exporter.calculate_layout(icons_data)

    # Create diagram object
    diagram = DrakonDiagram(
        id=1,
        name="Example Workflow",
        description="Example diagram with proper DRAKON v5 format",
        origin="0 0",  # TCL list format!
        zoom=1.0,
        icons=icons
    )

    # Export
    exporter.export_diagram(diagram)
    exporter.close()

    print(f"✅ Created example_diagram.drn")
    print(f"   Format: DRAKON Editor v5 compatible")
    print(f"   Icons: {len(icons)} (with half-dimensions and center coordinates)")
    print(f"   Open with DRAKON Editor: File → Open → example_diagram.drn")


if __name__ == "__main__":
    example_usage()
