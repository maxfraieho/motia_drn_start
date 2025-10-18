#!/usr/bin/env python3
"""
Code to DRAKON Converter

Analyzes TypeScript/JavaScript code and generates DRAKON diagrams
directly from control flow structures.

Supports:
- Function/method definitions
- if/else statements
- for/while loops
- try/catch/finally
- switch/case
- async/await patterns
"""

import re
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CodeBlock:
    """Represents a block of code with control flow"""
    type: str  # function, if, else, for, while, try, catch, switch
    content: str
    line_start: int
    line_end: int
    children: List['CodeBlock'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class CodeAnalyzer:
    """Analyze code structure and extract control flow"""

    def __init__(self, code: str, language: str = 'typescript'):
        self.code = code
        self.language = language
        self.lines = code.split('\n')

    def extract_functions(self) -> List[Dict[str, Any]]:
        """Extract all functions/methods from code"""
        functions = []

        # Patterns for function definitions
        patterns = [
            # TypeScript: export function name(...) { }
            r'export\s+(async\s+)?function\s+(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{',
            # TypeScript: const name = async (...) => { }
            r'(?:const|let|var)\s+(\w+)\s*=\s*(async\s+)?\([^)]*\)\s*=>\s*\{',
            # Class methods: async methodName(...) { }
            r'(async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{',
        ]

        for i, line in enumerate(self.lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    func_name = match.group(2) if match.lastindex >= 2 else match.group(1)
                    if func_name and func_name not in ['if', 'for', 'while', 'switch']:
                        # Extract function body
                        body_start = i
                        body_end = self._find_closing_brace(i)

                        if body_end:
                            functions.append({
                                'name': func_name,
                                'line_start': body_start,
                                'line_end': body_end,
                                'body': '\n'.join(self.lines[body_start:body_end + 1]),
                                'is_async': 'async' in line
                            })
                    break

        return functions

    def _find_closing_brace(self, start_line: int) -> Optional[int]:
        """Find matching closing brace for opening brace"""
        depth = 0
        for i in range(start_line, len(self.lines)):
            line = self.lines[i]
            depth += line.count('{') - line.count('}')
            if depth == 0 and '}' in line:
                return i
        return None

    def analyze_function_flow(self, func_body: str, func_name: str) -> List[Dict[str, Any]]:
        """Analyze control flow within a function and generate DRAKON items"""
        items = []

        # Always start with branch header (REQUIRED!)
        items.append({
            'type': 'branch',
            'text': ''
        })

        # Add function start
        items.append({
            'type': 'action',
            'text': f'START: {func_name}'
        })

        # Parse function body line by line
        lines = func_body.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines and comments
            if not line or line.startswith('//') or line.startswith('/*'):
                i += 1
                continue

            # Try/catch blocks
            if line.startswith('try'):
                items.append({
                    'type': 'action',
                    'text': 'BEGIN: Error handling'
                })
                i += 1
                continue

            elif 'catch' in line:
                # Extract error variable
                error_var = re.search(r'catch\s*\((\w+)\)', line)
                error_name = error_var.group(1) if error_var else 'error'
                items.append({
                    'type': 'action',
                    'text': f'CATCH: Handle {error_name}'
                })
                i += 1
                continue

            # If/else statements
            elif line.startswith('if'):
                condition = self._extract_condition(line)
                items.append({
                    'type': 'question',
                    'text': condition
                })
                i += 1
                continue

            elif line.startswith('else if'):
                condition = self._extract_condition(line)
                items.append({
                    'type': 'question',
                    'text': condition
                })
                i += 1
                continue

            elif line.startswith('else'):
                items.append({
                    'type': 'action',
                    'text': 'ELSE branch'
                })
                i += 1
                continue

            # Loops
            elif line.startswith('for') or line.startswith('while'):
                condition = self._extract_condition(line)
                items.append({
                    'type': 'action',
                    'text': f'LOOP: {condition}'
                })
                i += 1
                continue

            # Switch statements
            elif line.startswith('switch'):
                condition = self._extract_condition(line)
                items.append({
                    'type': 'select',
                    'text': f'SWITCH: {condition}'
                })
                i += 1
                continue

            elif line.startswith('case'):
                case_value = line.replace('case', '').replace(':', '').strip()
                items.append({
                    'type': 'case',
                    'text': f'CASE: {case_value}'
                })
                i += 1
                continue

            # Return statements
            elif 'return' in line:
                return_value = line.replace('return', '').replace(';', '').strip()
                if return_value:
                    items.append({
                        'type': 'action',
                        'text': f'RETURN: {return_value}'
                    })
                i += 1
                continue

            # Throw statements
            elif 'throw' in line:
                error_msg = line.replace('throw', '').strip()
                items.append({
                    'type': 'action',
                    'text': f'THROW: {error_msg}'
                })
                i += 1
                continue

            # Await/async operations
            elif 'await' in line:
                # Extract the awaited operation
                operation = line.replace('const', '').replace('let', '').replace('var', '')
                operation = operation.replace('await', '').strip()
                if '=' in operation:
                    operation = operation.split('=', 1)[1].strip()
                items.append({
                    'type': 'action',
                    'text': f'AWAIT: {operation}'
                })
                i += 1
                continue

            # Variable declarations and assignments
            elif any(keyword in line for keyword in ['const', 'let', 'var', '=']):
                # Extract variable name and value
                if '=' in line:
                    var_part = line.split('=')[0].strip()
                    var_part = var_part.replace('const', '').replace('let', '').replace('var', '').strip()
                    items.append({
                        'type': 'action',
                        'text': f'SET: {var_part}'
                    })
                i += 1
                continue

            # Function calls
            elif '(' in line and ')' in line:
                func_call = line.split('(')[0].strip()
                # Remove any leading keywords
                func_call = func_call.split()[-1]
                items.append({
                    'type': 'action',
                    'text': f'CALL: {func_call}()'
                })
                i += 1
                continue

            i += 1

        # Add function end
        items.append({
            'type': 'end',
            'text': ''
        })

        return items

    def _extract_condition(self, line: str) -> str:
        """Extract condition from if/while/for/switch statement"""
        # Remove keywords
        line = line.replace('if', '').replace('while', '').replace('switch', '')
        line = line.replace('for', '').replace('else if', '')

        # Extract content between parentheses
        match = re.search(r'\((.*?)\)', line)
        if match:
            condition = match.group(1).strip()
            # Truncate if too long
            if len(condition) > 50:
                condition = condition[:47] + '...'
            return condition
        return 'condition'


def analyze_code_file(file_path: Path, output_dir: Path, format: str = 'both') -> List[Path]:
    """
    Analyze code file and generate DRAKON diagrams for each function

    Args:
        file_path: Path to source code file
        output_dir: Directory for output diagrams
        format: 'drn', 'json', or 'both'

    Returns:
        List of generated file paths
    """
    # Read code
    code = file_path.read_text(encoding='utf-8')

    # Detect language
    language = 'typescript' if file_path.suffix in ['.ts', '.tsx'] else 'javascript'

    # Analyze
    analyzer = CodeAnalyzer(code, language)
    functions = analyzer.extract_functions()

    if not functions:
        print(f"No functions found in {file_path}", file=sys.stderr)
        return []

    print(f"Found {len(functions)} functions in {file_path.name}")

    # Generate diagrams for each function
    output_files = []
    output_dir.mkdir(parents=True, exist_ok=True)

    from drakon_to_drn import DrnExporter, DrakonDiagram
    from drakon_to_json import JsonExporter, DrakonDiagramJSON

    for func in functions:
        func_name = func['name']
        print(f"  Analyzing: {func_name}()")

        # Analyze control flow
        items = analyzer.analyze_function_flow(func['body'], func_name)

        if len(items) <= 3:  # Only branch + start + end
            print(f"    → Skipped (too simple, no control flow)")
            continue

        print(f"    → Generated {len(items)} DRAKON items")

        # Generate .drn
        if format in ['drn', 'both']:
            drn_file = output_dir / f"{func_name}.drn"
            try:
                exporter = DrnExporter(drn_file)
                icons = exporter.calculate_layout(items, vertical_spacing=80)

                diagram = DrakonDiagram(
                    id=1,
                    name=f"{func_name}",
                    description=f"Generated from {file_path.name} (lines {func['line_start']}-{func['line_end']})",
                    origin="0 0",
                    icons=icons,
                    zoom=1.0
                )

                exporter.export_diagram(diagram)
                exporter.close()
                output_files.append(drn_file)
                print(f"    ✓ Created: {drn_file.name}")
            except Exception as e:
                print(f"    ✗ Error creating .drn: {e}", file=sys.stderr)

        # Generate .json
        if format in ['json', 'both']:
            json_file = output_dir / f"{func_name}.json"
            try:
                exporter = JsonExporter(json_file, pretty=True)
                items_dict = exporter.create_items_from_data(items)

                diagram = DrakonDiagramJSON(
                    name=f"{func_name}",
                    access="write",
                    items=items_dict,
                    params=[]
                )

                exporter.export_diagram(diagram)
                output_files.append(json_file)
                print(f"    ✓ Created: {json_file.name}")
            except Exception as e:
                print(f"    ✗ Error creating .json: {e}", file=sys.stderr)

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description='Generate DRAKON diagrams from TypeScript/JavaScript code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze handler.ts and generate both formats
  %(prog)s handler.ts -o ./diagrams/ --format both

  # Analyze specific file, only .drn
  %(prog)s src/service.ts -o ./docs/diagrams/ --format drn

  # Analyze multiple files
  %(prog)s handler.ts utils.ts -o ./diagrams/
        """
    )

    parser.add_argument(
        'files',
        type=Path,
        nargs='+',
        help='Source code files to analyze'
    )

    parser.add_argument(
        '-o', '--output-dir',
        type=Path,
        required=True,
        help='Output directory for diagrams'
    )

    parser.add_argument(
        '--format',
        choices=['drn', 'json', 'both'],
        default='both',
        help='Output format (default: both)'
    )

    args = parser.parse_args()

    # Process each file
    all_outputs = []
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            continue

        outputs = analyze_code_file(file_path, args.output_dir, args.format)
        all_outputs.extend(outputs)

    # Summary
    print(f"\n✅ Generated {len(all_outputs)} diagram files")
    if all_outputs:
        print("\n📊 Visualization:")
        if args.format in ['drn', 'both']:
            print("  • .drn files → Open in DRAKON Editor")
        if args.format in ['json', 'both']:
            print("  • .json files → Upload to https://drakonhub.com/editor")

    return 0 if all_outputs else 1


if __name__ == '__main__':
    sys.exit(main())
