#!/usr/bin/env python3
"""
DRAKON to JSON Converter (DrakonWidget/DrakonHub compatible)

Converts internal DRAKON representation to JSON format compatible with:
- DrakonWidget (browser-based viewer/editor)
- DrakonHub (web platform)

JSON Format Structure (from https://github.com/stepan-mitkin/drakonwidget):
{
  "diagram": {
    "name": "Diagram Name",
    "type": "drakon",
    "nodes": [
      {"id": 1, "type": "action", "text": "Do something", "x": 100, "y": 100}
    ],
    "links": [
      {"from": 1, "to": 2, "points": [[x1, y1], [x2, y2]]}
    ],
    "settings": {
      "gridSize": 20,
      "zoom": 1.0
    }
  }
}
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DrakonItem:
    """DRAKON item in JSON format

    CRITICAL CHANGES FROM OLD FORMAT:
    - Use 'content' instead of 'text'
    - No x, y, width, height (geometric layout not stored in JSON)
    - Links are properties (one, two, side), not separate array
    """
    id: str  # String ID!
    type: str  # action, question, select, loopbegin, loopend, branch, address, etc.
    content: str = ""  # Primary text (renamed from 'text')
    secondary: str = ""  # Secondary text (for shelf, input, output, process)
    link: str = ""  # Reference/link field
    one: Optional[str] = None  # ID of next item down
    two: Optional[str] = None  # ID of next item right
    side: Optional[str] = None  # ID of duration marker (left)
    flag1: Optional[int] = None  # YES/NO orientation for question (0 or 1)
    branch_id: Optional[int] = None  # Branch ID (required for branch type)
    margin: Optional[int] = None  # Additional left margin
    style: Optional[str] = None  # Style as JSON string (not object!)


@dataclass
class DrakonDiagramJSON:
    """Complete DRAKON diagram in JSON format

    CRITICAL: Official DrakonHub/DrakonWidget format (from examples.js)
    - No 'diagram' wrapper!
    - 'items' is dictionary (not array!)
    - No separate 'links' array
    - NO 'access' field (official examples don't have it!)
    - 'style' must be JSON string (not object)
    """
    name: str  # Required
    items: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # Dictionary, not array!
    params: Optional[str] = None  # Newline-separated parameters
    style: Optional[str] = None  # JSON string (not object!)


class JsonExporter:
    """Export DRAKON diagrams to DrakonWidget/DrakonHub JSON format"""

    # Icon type mappings (internal → DrakonWidget)
    ICON_TYPE_MAP = {
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

    # Default dimensions (DrakonWidget uses width/height in pixels)
    DEFAULT_DIMENSIONS = {
        'action': {'width': 120, 'height': 60},
        'question': {'width': 120, 'height': 80},
        'select': {'width': 120, 'height': 60},
        'loopbegin': {'width': 120, 'height': 40},
        'loopend': {'width': 120, 'height': 40},
        'foreach': {'width': 120, 'height': 60},
        'branch': {'width': 80, 'height': 80},
        'address': {'width': 100, 'height': 50},
        'start': {'width': 120, 'height': 50},
        'end': {'width': 120, 'height': 50},
        'parameters': {'width': 140, 'height': 60},
        'comment': {'width': 160, 'height': 80}
    }

    def __init__(self, output_path: Path, pretty: bool = True):
        """
        Initialize JSON exporter

        Args:
            output_path: Path to output .json file
            pretty: Whether to pretty-print JSON
        """
        self.output_path = Path(output_path)
        self.pretty = pretty

    def export_diagram(self, diagram: DrakonDiagramJSON):
        """
        Export DRAKON diagram to JSON format

        CRITICAL: Exports in official DrakonHub/DrakonWidget format
        - No 'diagram' wrapper
        - items as dictionary (string keys)
        - No separate links array
        - NO 'access' field (official examples don't have it!)

        Args:
            diagram: DrakonDiagramJSON object to export
        """
        # Build correct structure (no wrapper!)
        diagram_dict = {
            "name": diagram.name
        }

        # Add optional fields
        if diagram.params:
            diagram_dict["params"] = diagram.params

        if diagram.style:
            diagram_dict["style"] = diagram.style  # Must be JSON string!

        # Add items (as dictionary!)
        diagram_dict["items"] = diagram.items

        # Write to file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            if self.pretty:
                json.dump(diagram_dict, f, indent=2, ensure_ascii=False)
            else:
                json.dump(diagram_dict, f, ensure_ascii=False)

        logger.info(f"✅ Exported diagram '{diagram.name}' to {self.output_path}")
        logger.info(f"   Items: {len(diagram.items)}")
        logger.info(f"   Format: Official DrakonHub/DrakonWidget compatible")

    @staticmethod
    def item_to_dict(item: DrakonItem) -> Dict[str, Any]:
        """Convert DrakonItem to dictionary for JSON export

        Only includes non-empty/non-None fields
        """
        item_dict = {"type": item.type}  # Type is always required

        # Add optional fields (only if present)
        if item.content:
            item_dict["content"] = item.content
        if item.secondary:
            item_dict["secondary"] = item.secondary
        if item.link:
            item_dict["link"] = item.link
        if item.one:
            item_dict["one"] = item.one
        if item.two:
            item_dict["two"] = item.two
        if item.side:
            item_dict["side"] = item.side
        if item.flag1 is not None:
            item_dict["flag1"] = item.flag1
        if item.branch_id is not None:
            item_dict["branchId"] = item.branch_id  # Camel case!
        if item.margin is not None:
            item_dict["margin"] = item.margin
        if item.style:
            item_dict["style"] = item.style  # Must be JSON string!

        return item_dict

    @staticmethod
    def normalize_icon_type(icon_type: str) -> str:
        """
        Normalize icon type to DrakonWidget format

        Args:
            icon_type: Internal icon type name

        Returns:
            DrakonWidget compatible type name
        """
        normalized = icon_type.lower().replace('-', '_')
        return JsonExporter.ICON_TYPE_MAP.get(normalized, 'action')

    @staticmethod
    def create_items_from_data(items_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Create items dictionary from list of item data

        CRITICAL: Returns dictionary with string keys, not array!
        Automatically creates sequential 'one' links

        Args:
            items_data: List of item dictionaries from parser

        Returns:
            Dictionary mapping string IDs to item dictionaries
        """
        items = {}

        for i, item_data in enumerate(items_data):
            item_id = str(i + 1)
            item_type = JsonExporter.normalize_icon_type(item_data.get('type', 'action'))

            # Build item dictionary
            item = {"type": item_type}

            # Add text content (use 'content', not 'text'!)
            if 'text' in item_data and item_data['text']:
                item["content"] = item_data['text']

            # Add sequential link (one = next item down)
            if i < len(items_data) - 1:
                next_id = str(i + 2)
                item["one"] = next_id

            # Special handling for branch type
            if item_type == 'branch':
                item["branchId"] = 0  # First branch always has ID 0

            items[item_id] = item

        return items

    @staticmethod
    def from_drn_format(drn_data: Dict[str, Any]) -> DrakonDiagramJSON:
        """
        Convert from .drn format data to JSON format

        Args:
            drn_data: Dictionary containing drn format data (from SQLite)

        Returns:
            DrakonDiagramJSON object
        """
        # Extract data from drn format
        diagram_info = drn_data.get('diagram', {})
        icons = drn_data.get('icons', [])
        links = drn_data.get('links', [])

        # Convert icons to nodes
        nodes = []
        for icon in icons:
            node = DrakonNode(
                id=icon['icon_id'],
                type=icon['type'],
                text=icon.get('text', ''),
                x=icon['x'],
                y=icon['y'],
                width=icon.get('w'),
                height=icon.get('h')
            )
            nodes.append(node)

        # Convert links
        json_links = []
        for link in links:
            json_link = DrakonLink(
                id=link['link_id'],
                source=link['src_icon_id'],
                target=link['dst_icon_id'],
                points=json.loads(link.get('vertices', '[]'))
            )
            json_links.append(json_link)

        # Create diagram
        return DrakonDiagramJSON(
            name=diagram_info.get('name', 'Untitled'),
            type='drakon',
            nodes=nodes,
            links=json_links,
            settings=DrakonSettings(
                zoom=diagram_info.get('zoom', 1.0)
            )
        )


def example_usage():
    """Example: Create and export DRAKON diagram to JSON"""

    # Example workflow data
    items_data = [
        {'type': 'branch', 'text': ''},  # REQUIRED: Every diagram must start with branch!
        {'type': 'action', 'text': 'Load configuration'},
        {'type': 'question', 'text': 'Configuration valid?'},
        {'type': 'action', 'text': 'Initialize system'},
        {'type': 'loopbegin', 'text': 'For each task'},
        {'type': 'action', 'text': 'Process task'},
        {'type': 'loopend', 'text': 'End loop'},
        {'type': 'action', 'text': 'Save results'},
        {'type': 'end', 'text': ''}
    ]

    # Create exporter
    exporter = JsonExporter(Path("example_workflow.json"), pretty=True)

    # Create items dictionary (automatically links items)
    items = exporter.create_items_from_data(items_data)

    # Create diagram
    diagram = DrakonDiagramJSON(
        name="Example Workflow",
        access="write",  # Required!
        items=items  # Dictionary, not array!
    )

    # Export
    exporter.export_diagram(diagram)

    print(f"✅ Created example_workflow.json")
    print(f"   Format: Official DrakonHub/DrakonWidget compatible")
    print(f"   Items: {len(items)} (as dictionary with string keys)")
    print(f"   Links: Embedded in items as 'one', 'two' properties")
    print(f"   Load in DrakonWidget: https://drakonhub.com/editor")
    print(f"   Or use locally with drakonwidget.js")


if __name__ == "__main__":
    example_usage()
