#!/usr/bin/env python3
"""
Convert all .drakon pseudocode files to .drn and .json formats

Uses parse_drakon_pseudocode.py + drakon_to_drn.py + drakon_to_json.py
"""

import sys
from pathlib import Path
from parse_drakon_pseudocode import parse_drakon_file
from drakon_to_drn import DrnExporter, DrakonDiagram
from drakon_to_json import JsonExporter, DrakonDiagramJSON

# List of .drakon files to convert
DRAKON_FILES = [
    '/home/vokov/motia/motia-output/steps/config-service/diagrams/logic-flow.drakon',
    '/home/vokov/motia/motia-output/steps/config-service/diagrams/error-handling.drakon',
    '/home/vokov/motia/motia-output/steps/config-service/diagrams/data-processing.drakon',
    '/home/vokov/motia/motia-output/steps/config-service/diagrams/state-transitions.drakon'
]


def convert_drakon_file(drakon_path: Path):
    """Convert single .drakon file to both .drn and .json"""

    print(f"\n{'='*60}")
    print(f"Converting: {drakon_path.name}")
    print(f"{'='*60}")

    # Parse .drakon file
    print("  [1/3] Parsing .drakon pseudocode...")
    parsed = parse_drakon_file(drakon_path)
    print(f"    ✓ Title: {parsed['title']}")
    print(f"    ✓ Items: {len(parsed['items'])}")

    # Prepare output paths
    output_dir = drakon_path.parent
    base_name = drakon_path.stem
    drn_path = output_dir / f"{base_name}.drn"
    json_path = output_dir / f"{base_name}.json"

    # Convert to .drn
    print(f"  [2/3] Converting to .drn format...")
    try:
        drn_exporter = DrnExporter(drn_path)
        icons = drn_exporter.calculate_layout(parsed['items'], vertical_spacing=80)

        diagram = DrakonDiagram(
            id=1,
            name=parsed['title'],
            description=f"Author: {parsed['author']}, Date: {parsed['date']}",
            origin="0 0",
            icons=icons,
            zoom=1.0
        )

        drn_exporter.export_diagram(diagram)
        drn_exporter.close()
        print(f"    ✓ Created: {drn_path.name}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

    # Convert to .json
    print(f"  [3/3] Converting to .json format...")
    try:
        json_exporter = JsonExporter(json_path, pretty=True)
        items = json_exporter.create_items_from_data(parsed['items'])

        diagram_json = DrakonDiagramJSON(
            name=parsed['title'],
            access="write",
            items=items
        )

        json_exporter.export_diagram(diagram_json)
        print(f"    ✓ Created: {json_path.name}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

    return True


def main():
    """Convert all .drakon files"""
    print("\n" + "="*60)
    print("DRAKON Pseudocode Batch Converter")
    print("="*60)
    print(f"Files to convert: {len(DRAKON_FILES)}")

    success_count = 0
    fail_count = 0

    for drakon_file in DRAKON_FILES:
        drakon_path = Path(drakon_file)

        if not drakon_path.exists():
            print(f"\n✗ File not found: {drakon_file}")
            fail_count += 1
            continue

        if convert_drakon_file(drakon_path):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print("\n" + "="*60)
    print("CONVERSION SUMMARY")
    print("="*60)
    print(f"  ✓ Successful: {success_count}")
    print(f"  ✗ Failed: {fail_count}")
    print(f"  Total: {len(DRAKON_FILES)}")
    print()

    if success_count > 0:
        print("Generated files:")
        for drakon_file in DRAKON_FILES:
            base = Path(drakon_file).stem
            dir_path = Path(drakon_file).parent
            print(f"  - {dir_path}/{base}.drn")
            print(f"  - {dir_path}/{base}.json")

    print("\nDone! 🎉")
    return 0 if fail_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
