#!/usr/bin/env python3
"""
CLI Interface for DRAKON Converters

Provides command-line interface to convert .drakon pseudocode files
to both .drn (DRAKON Editor) and .json (DrakonHub) formats.
"""

import argparse
import sys
from pathlib import Path
from parse_drakon_pseudocode import parse_drakon_file
from drakon_to_drn import DrnExporter, DrakonDiagram
from drakon_to_json import JsonExporter, DrakonDiagramJSON


def convert_to_drn(input_file: Path, output_file: Path) -> bool:
    """Convert .drakon file to .drn format"""
    try:
        # Parse input
        parsed = parse_drakon_file(input_file)

        # Create exporter
        exporter = DrnExporter(output_file)
        icons = exporter.calculate_layout(parsed['items'], vertical_spacing=80)

        # Create diagram
        diagram = DrakonDiagram(
            id=1,
            name=parsed['title'],
            description=f"Author: {parsed['author']}, Date: {parsed['date']}",
            origin="0 0",
            icons=icons,
            zoom=1.0
        )

        # Export
        exporter.export_diagram(diagram)
        exporter.close()

        return True
    except Exception as e:
        print(f"Error converting to .drn: {e}", file=sys.stderr)
        return False


def convert_to_json(input_file: Path, output_file: Path) -> bool:
    """Convert .drakon file to .json format"""
    try:
        # Parse input
        parsed = parse_drakon_file(input_file)

        # Create exporter
        exporter = JsonExporter(output_file, pretty=True)
        items = exporter.create_items_from_data(parsed['items'])

        # Create diagram
        diagram = DrakonDiagramJSON(
            name=parsed['title'],
            access="write",
            items=items
        )

        # Export
        exporter.export_diagram(diagram)

        return True
    except Exception as e:
        print(f"Error converting to .json: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert DRAKON pseudocode to visual diagram formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert to .drn format
  %(prog)s --input diagram.drakon --output diagram.drn

  # Convert to .json format
  %(prog)s --input diagram.drakon --output diagram.json

  # Auto-detect format from extension
  %(prog)s -i diagram.drakon -o diagram.drn
  %(prog)s -i diagram.drakon -o diagram.json

  # Convert to both formats (use output directory)
  %(prog)s -i diagram.drakon -d ./diagrams/ --both
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Input .drakon pseudocode file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (.drn or .json)'
    )

    parser.add_argument(
        '-d', '--output-dir',
        type=Path,
        help='Output directory (for --both mode)'
    )

    parser.add_argument(
        '--both',
        action='store_true',
        help='Generate both .drn and .json formats'
    )

    parser.add_argument(
        '--format',
        choices=['drn', 'json'],
        help='Force specific output format (overrides auto-detection)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress informational messages'
    )

    args = parser.parse_args()

    # Validate input
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    if not args.input.suffix == '.drakon':
        print(f"Warning: Input file doesn't have .drakon extension", file=sys.stderr)

    # Determine output mode
    if args.both:
        # Generate both formats
        if not args.output_dir:
            args.output_dir = args.input.parent

        args.output_dir.mkdir(parents=True, exist_ok=True)
        base_name = args.input.stem

        drn_file = args.output_dir / f"{base_name}.drn"
        json_file = args.output_dir / f"{base_name}.json"

        success = True

        if not args.quiet:
            print(f"Converting {args.input.name} to both formats...")

        if convert_to_drn(args.input, drn_file):
            if not args.quiet:
                print(f"  ✓ Created: {drn_file}")
        else:
            success = False

        if convert_to_json(args.input, json_file):
            if not args.quiet:
                print(f"  ✓ Created: {json_file}")
        else:
            success = False

        return 0 if success else 1

    elif args.output:
        # Single output file

        # Detect format from extension or use --format flag
        if args.format:
            output_format = args.format
        else:
            output_format = args.output.suffix.lstrip('.')

        if output_format not in ['drn', 'json']:
            print(f"Error: Unknown output format: {output_format}", file=sys.stderr)
            print("Use .drn or .json extension, or specify --format", file=sys.stderr)
            return 1

        # Convert
        if output_format == 'drn':
            success = convert_to_drn(args.input, args.output)
            if success and not args.quiet:
                print(f"✓ Created {args.output}")
                print(f"  Open with DRAKON Editor")
        else:
            success = convert_to_json(args.input, args.output)
            if success and not args.quiet:
                print(f"✓ Created {args.output}")
                print(f"  Upload to https://drakonhub.com/editor")

        return 0 if success else 1

    else:
        print("Error: Either --output or --both must be specified", file=sys.stderr)
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
