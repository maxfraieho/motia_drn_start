#!/usr/bin/env python3
"""
Generate DRAKON diagrams for a Motia Step

Reads Step README, extracts algorithm descriptions, generates DRAKON diagrams
in both .drn (DRAKON Editor) and .json (DrakonWidget/DrakonHub) formats.

Usage:
    ./generate_step_diagrams.py --step-name config-service \
                                 --step-dir /path/to/steps/config-service \
                                 --output-dir /path/to/steps/config-service/diagrams \
                                 --formats drn,json

Author: Motia DRAKON Pipeline Module
Version: 1.0
Date: 2025-10-10
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from drakon_to_drn import DrnExporter, DrakonDiagram, DrakonIcon
from drakon_to_json import JsonExporter, DrakonDiagramJSON

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class StepDiagramGenerator:
    """Generate DRAKON diagrams for Motia Steps"""

    DIAGRAM_TYPES = [
        'initialization',
        'main-flow',
        'error-handling',
        'cleanup'
    ]

    def __init__(self, step_name: str, step_dir: Path, output_dir: Path):
        """
        Initialize diagram generator

        Args:
            step_name: Name of the Motia Step
            step_dir: Path to Step directory
            output_dir: Path to output directory for diagrams
        """
        self.step_name = step_name
        self.step_dir = Path(step_dir)
        self.output_dir = Path(output_dir)
        self.readme_file = self.step_dir / 'README.md'
        self.config_file = self.step_dir / 'config.json'

    def load_step_metadata(self) -> Dict[str, Any]:
        """Load Step metadata from config.json"""
        if not self.config_file.exists():
            logger.warning(f"config.json not found, using defaults")
            return {}

        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config.json: {e}")
            return {}

    def parse_readme_algorithms(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse README.md and extract algorithm descriptions

        Returns:
            Dict mapping diagram type to list of icon data
        """
        metadata = self.load_step_metadata()
        step_type = metadata.get('type', 'api')
        pattern = metadata.get('pattern', 'observer')

        # TODO: Implement intelligent README parsing
        # For now, generate template-based diagrams

        return {
            'initialization': self._generate_initialization_flow(step_type, pattern),
            'main-flow': self._generate_main_flow(step_type, pattern),
            'error-handling': self._generate_error_handling_flow(step_type),
            'cleanup': self._generate_cleanup_flow(step_type)
        }

    def _generate_initialization_flow(self, step_type: str, pattern: str) -> List[Dict[str, Any]]:
        """Generate initialization algorithm

        CRITICAL: Always starts with branch header (required by DRAKON spec)
        """
        icons = [
            {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
            {'type': 'action', 'text': f'Initialize {self.step_name}'},
            {'type': 'action', 'text': 'Load configuration from config.json'},
            {'type': 'action', 'text': 'Validate schema against schema.json'},
            {'type': 'question', 'text': 'Configuration valid?'},
        ]

        # Branch for invalid configuration
        icons.extend([
            {'type': 'action', 'text': 'Log configuration error'},
            {'type': 'action', 'text': 'Throw ConfigurationError'},
        ])

        # Continue with valid configuration
        icons.extend([
            {'type': 'action', 'text': 'Initialize dependencies'},
        ])

        # Type-specific initialization
        if step_type == 'event':
            icons.append({'type': 'action', 'text': 'Setup event listeners'})
            icons.append({'type': 'action', 'text': 'Subscribe to relevant events'})
        elif step_type == 'api':
            icons.append({'type': 'action', 'text': 'Setup HTTP routes'})
            icons.append({'type': 'action', 'text': 'Configure middleware'})
        elif step_type == 'cron':
            icons.append({'type': 'action', 'text': 'Setup cron schedule'})
            icons.append({'type': 'action', 'text': 'Initialize job queue'})
        elif step_type == 'stream':
            icons.append({'type': 'action', 'text': 'Open stream connection'})
            icons.append({'type': 'action', 'text': 'Setup data handlers'})

        icons.extend([
            {'type': 'action', 'text': 'Emit "initialized" event'},
            {'type': 'end', 'text': 'Ready'}
        ])

        return icons

    def _generate_main_flow(self, step_type: str, pattern: str) -> List[Dict[str, Any]]:
        """Generate main execution flow

        CRITICAL: Always starts with branch header (required by DRAKON spec)
        """
        icons = []

        if step_type == 'event':
            icons = [
                {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
                {'type': 'action', 'text': 'Event received'},
                {'type': 'action', 'text': 'Extract event payload'},
                {'type': 'action', 'text': 'Validate event schema'},
                {'type': 'question', 'text': 'Schema valid?'},
                {'type': 'action', 'text': 'Process event data'},
            ]

            # Pattern-specific processing
            if 'observer' in pattern.lower():
                icons.append({'type': 'action', 'text': 'Notify observers'})
            elif 'command' in pattern.lower():
                icons.append({'type': 'action', 'text': 'Execute command'})
            elif 'strategy' in pattern.lower():
                icons.append({'type': 'select', 'text': 'Select strategy'})

            icons.extend([
                {'type': 'action', 'text': 'Emit result event'},
                {'type': 'end', 'text': 'Complete'}
            ])

        elif step_type == 'api':
            icons = [
                {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
                {'type': 'action', 'text': 'HTTP request received'},
                {'type': 'action', 'text': 'Parse request body'},
                {'type': 'action', 'text': 'Validate input schema'},
                {'type': 'question', 'text': 'Input valid?'},
                {'type': 'action', 'text': 'Authenticate request'},
                {'type': 'question', 'text': 'Authorized?'},
                {'type': 'action', 'text': 'Process request'},
                {'type': 'action', 'text': 'Format response'},
                {'type': 'action', 'text': 'Return HTTP 200 OK'},
                {'type': 'end', 'text': 'Complete'}
            ]

        elif step_type == 'cron':
            icons = [
                {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
                {'type': 'action', 'text': 'Cron trigger fired'},
                {'type': 'action', 'text': 'Check job schedule'},
                {'type': 'question', 'text': 'Time to execute?'},
                {'type': 'action', 'text': 'Run scheduled task'},
                {'type': 'action', 'text': 'Update last execution time'},
                {'type': 'action', 'text': 'Emit completion event'},
                {'type': 'end', 'text': 'Complete'}
            ]

        elif step_type == 'stream':
            icons = [
                {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
                {'type': 'action', 'text': 'Stream data received'},
                {'type': 'loopbegin', 'text': 'For each chunk'},
                {'type': 'action', 'text': 'Process chunk'},
                {'type': 'action', 'text': 'Emit partial result'},
                {'type': 'loopend', 'text': 'End loop'},
                {'type': 'action', 'text': 'Finalize stream'},
                {'type': 'end', 'text': 'Complete'}
            ]

        else:  # noop or unknown
            icons = [
                {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
                {'type': 'action', 'text': f'Execute {self.step_name}'},
                {'type': 'action', 'text': 'Perform operation'},
                {'type': 'end', 'text': 'Complete'}
            ]

        return icons

    def _generate_error_handling_flow(self, step_type: str) -> List[Dict[str, Any]]:
        """Generate error handling flow

        CRITICAL: Always starts with branch header (required by DRAKON spec)
        """
        return [
            {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
            {'type': 'action', 'text': 'Error detected'},
            {'type': 'action', 'text': 'Extract error details'},
            {'type': 'action', 'text': 'Log error with stack trace'},
            {'type': 'question', 'text': 'Recoverable error?'},
            {'type': 'action', 'text': 'Attempt graceful recovery'},
            {'type': 'question', 'text': 'Recovery successful?'},
            {'type': 'action', 'text': 'Resume normal operation'},
            {'type': 'action', 'text': 'Emit error event'},
            {'type': 'select', 'text': 'Error severity'},
            {'type': 'action', 'text': 'Log warning (case: warning)'},
            {'type': 'action', 'text': 'Alert operator (case: critical)'},
            {'type': 'action', 'text': 'Initiate shutdown (case: fatal)'},
            {'type': 'end', 'text': 'End'}
        ]

    def _generate_cleanup_flow(self, step_type: str) -> List[Dict[str, Any]]:
        """Generate cleanup/teardown flow

        CRITICAL: Always starts with branch header (required by DRAKON spec)
        """
        icons = [
            {'type': 'branch', 'text': ''},  # REQUIRED: Branch header!
            {'type': 'action', 'text': 'Shutdown signal received'},
            {'type': 'action', 'text': 'Stop accepting new requests'},
            {'type': 'action', 'text': 'Wait for pending operations'},
        ]

        # Type-specific cleanup
        if step_type == 'event':
            icons.append({'type': 'action', 'text': 'Unsubscribe from events'})
            icons.append({'type': 'action', 'text': 'Remove event listeners'})
        elif step_type == 'api':
            icons.append({'type': 'action', 'text': 'Close HTTP server'})
            icons.append({'type': 'action', 'text': 'Terminate connections'})
        elif step_type == 'cron':
            icons.append({'type': 'action', 'text': 'Cancel scheduled jobs'})
            icons.append({'type': 'action', 'text': 'Clear job queue'})
        elif step_type == 'stream':
            icons.append({'type': 'action', 'text': 'Close stream connections'})
            icons.append({'type': 'action', 'text': 'Flush buffers'})

        icons.extend([
            {'type': 'action', 'text': 'Release allocated resources'},
            {'type': 'action', 'text': 'Close database connections'},
            {'type': 'action', 'text': 'Emit "terminated" event'},
            {'type': 'end', 'text': 'Shutdown complete'}
        ])

        return icons

    def generate_drn_diagram(self, diagram_type: str, icons_data: List[Dict]) -> Path:
        """
        Generate .drn format diagram

        Args:
            diagram_type: Type of diagram (initialization, main-flow, etc.)
            icons_data: List of icon dictionaries

        Returns:
            Path to generated .drn file
        """
        output_file = self.output_dir / f"{diagram_type}.drn"

        exporter = DrnExporter(output_file)
        icons = exporter.calculate_layout(icons_data, vertical_spacing=80)

        diagram = DrakonDiagram(
            id=1,
            name=f"{self.step_name} - {diagram_type.replace('-', ' ').title()}",
            description=f"Generated DRAKON diagram for {self.step_name}",
            origin="0 0",  # TCL format!
            icons=icons,
            zoom=1.0
        )

        exporter.export_diagram(diagram)
        exporter.close()

        return output_file

    def generate_json_diagram(self, diagram_type: str, icons_data: List[Dict]) -> Path:
        """
        Generate .json format diagram

        Args:
            diagram_type: Type of diagram (initialization, main-flow, etc.)
            icons_data: List of icon dictionaries

        Returns:
            Path to generated .json file
        """
        output_file = self.output_dir / f"{diagram_type}.json"

        exporter = JsonExporter(output_file, pretty=True)
        items = exporter.create_items_from_data(icons_data)

        diagram = DrakonDiagramJSON(
            name=f"{self.step_name} - {diagram_type.replace('-', ' ').title()}",
            items=items  # Dictionary, not array!
        )

        exporter.export_diagram(diagram)

        return output_file

    def generate_all(self, formats: List[str] = ['drn', 'json']) -> Dict[str, List[Path]]:
        """
        Generate all diagrams in specified formats

        Args:
            formats: List of formats to generate ('drn', 'json')

        Returns:
            Dict mapping diagram type to list of generated files
        """
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Parse algorithms from README
        algorithms = self.parse_readme_algorithms()
        generated_files = {}

        for diagram_type in self.DIAGRAM_TYPES:
            if diagram_type not in algorithms:
                logger.warning(f"No algorithm found for {diagram_type}, skipping")
                continue

            icons_data = algorithms[diagram_type]
            files = []

            # Generate .drn format
            if 'drn' in formats:
                try:
                    drn_file = self.generate_drn_diagram(diagram_type, icons_data)
                    files.append(drn_file)
                    logger.info(f"✅ Generated {drn_file.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to generate {diagram_type}.drn: {e}")

            # Generate .json format
            if 'json' in formats:
                try:
                    json_file = self.generate_json_diagram(diagram_type, icons_data)
                    files.append(json_file)
                    logger.info(f"✅ Generated {json_file.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to generate {diagram_type}.json: {e}")

            if files:
                generated_files[diagram_type] = files

        return generated_files


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate DRAKON diagrams for a Motia Step',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate both .drn and .json formats
  %(prog)s --step-name config-service \\
           --step-dir /home/vokov/motia/steps/config-service \\
           --output-dir /home/vokov/motia/steps/config-service/diagrams

  # Generate only .json format
  %(prog)s --step-name auth-middleware \\
           --step-dir /home/vokov/motia/steps/auth-middleware \\
           --output-dir /home/vokov/motia/steps/auth-middleware/diagrams \\
           --formats json

Output:
  4 diagram types generated:
    - initialization: Step initialization sequence
    - main-flow: Main execution flow
    - error-handling: Error handling logic
    - cleanup: Cleanup/teardown sequence

  Each diagram is generated in specified formats:
    - .drn: DRAKON Editor (desktop application)
    - .json: DrakonWidget/DrakonHub (web platform)
        """
    )

    parser.add_argument(
        '--step-name',
        required=True,
        help='Name of the Motia Step'
    )
    parser.add_argument(
        '--step-dir',
        required=True,
        help='Path to Step directory'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Path to output directory for diagrams'
    )
    parser.add_argument(
        '--formats',
        default='drn,json',
        help='Comma-separated formats to generate (default: drn,json)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Parse formats
    formats = [f.strip() for f in args.formats.split(',')]
    valid_formats = ['drn', 'json']
    formats = [f for f in formats if f in valid_formats]

    if not formats:
        logger.error("No valid formats specified. Use: drn, json")
        return 1

    # Create generator
    generator = StepDiagramGenerator(
        step_name=args.step_name,
        step_dir=Path(args.step_dir),
        output_dir=Path(args.output_dir)
    )

    logger.info(f"Generating DRAKON diagrams for Step: {args.step_name}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Formats: {', '.join(formats)}")
    logger.info("")

    try:
        # Generate diagrams
        generated_files = generator.generate_all(formats=formats)

        # Report results
        if not generated_files:
            logger.error("❌ No diagrams were generated")
            return 1

        total_files = sum(len(files) for files in generated_files.values())
        logger.info("")
        logger.info(f"✅ Successfully generated {total_files} DRAKON diagram files")
        logger.info("")

        for diagram_type, files in generated_files.items():
            logger.info(f"  {diagram_type}:")
            for file in files:
                size = file.stat().st_size if file.exists() else 0
                logger.info(f"    - {file.name} ({size:,} bytes)")

        logger.info("")
        logger.info("Next steps:")
        logger.info("  - Open .drn files in DRAKON Editor")
        logger.info("  - Upload .json files to https://drakonhub.com/editor")
        logger.info("")

        return 0

    except Exception as e:
        logger.error(f"❌ Failed to generate diagrams: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
