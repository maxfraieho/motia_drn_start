#!/usr/bin/env python3
"""
Parse .drakon pseudocode files to internal structure

Converts custom DRAKON pseudocode format to Python data structures
that can be fed to drakon_to_drn.py and drakon_to_json.py
"""

import re
from typing import List, Dict, Any
from pathlib import Path


def parse_drakon_file(filepath: Path) -> Dict[str, Any]:
    """Parse .drakon pseudocode file

    Returns:
        Dictionary with 'title', 'author', 'date', 'items'
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    title_match = re.search(r'TITLE:\s*(.+)', content)
    author_match = re.search(r'AUTHOR:\s*(.+)', content)
    date_match = re.search(r'DATE:\s*(.+)', content)

    title = title_match.group(1).strip() if title_match else filepath.stem
    author = author_match.group(1).strip() if author_match else "Unknown"
    date = date_match.group(1).strip() if date_match else "Unknown"

    # Parse nodes
    items = []

    # Find all node definitions: [node_id] TYPE "text"
    node_pattern = r'\[(\w+)\]\s+(ACTION|QUESTION|STATE)\s+"([^"]+)"'
    nodes = re.findall(node_pattern, content)

    # Add branch header first (required!)
    items.append({
        'type': 'branch',
        'text': ''
    })

    # Add START action
    items.append({
        'type': 'action',
        'text': 'START'
    })

    # Add parsed nodes
    for node_id, node_type, node_text in nodes:
        if node_type == 'ACTION' or node_type == 'STATE':
            items.append({
                'type': 'action',
                'text': node_text
            })
        elif node_type == 'QUESTION':
            items.append({
                'type': 'question',
                'text': node_text
            })

    # Add END
    items.append({
        'type': 'end',
        'text': ''
    })

    return {
        'title': title,
        'author': author,
        'date': date,
        'items': items
    }


if __name__ == '__main__':
    # Test with one file
    test_file = Path('/home/vokov/motia/motia-output/steps/config-service/diagrams/logic-flow.drakon')
    if test_file.exists():
        result = parse_drakon_file(test_file)
        print(f"Title: {result['title']}")
        print(f"Items: {len(result['items'])}")
        for i, item in enumerate(result['items'][:5]):
            print(f"  {i+1}. {item['type']}: {item['text'][:50]}")
