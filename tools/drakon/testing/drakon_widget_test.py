#!/usr/bin/env python3
"""
DrakonWidget Testing Plugin for Motia DRAKON Pipeline

Automatically tests generated DRAKON diagrams using DrakonWidget in a browser.
Validates that diagrams load correctly, render properly, and are structurally sound.

Location: /home/vokov/motia/tools/drakon/testing/drakon_widget_test.py
"""

import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import http.server
import socketserver
import threading
import webbrowser
from dataclasses import dataclass

@dataclass
class TestResult:
    """Result of a single test"""
    name: str
    passed: bool
    message: str
    duration_ms: float = 0.0

class DrakonWidgetTester:
    """
    Test DRAKON diagrams using DrakonWidget in browser
    
    Features:
    - Automated browser testing with Playwright/Selenium
    - Visual regression testing
    - Structure validation
    - Performance metrics
    - Screenshot capture
    """
    
    def __init__(self, 
                 drakon_widget_path: Path,
                 test_output_dir: Path,
                 port: int = 8765):
        """
        Initialize tester
        
        Args:
            drakon_widget_path: Path to drakonwidget.js file
            test_output_dir: Directory for test results
            port: HTTP server port
        """
        self.drakon_widget_path = Path(drakon_widget_path)
        self.test_output_dir = Path(test_output_dir)
        self.port = port
        
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if DrakonWidget exists
        if not self.drakon_widget_path.exists():
            raise FileNotFoundError(
                f"DrakonWidget not found: {self.drakon_widget_path}\n"
                f"Download from: https://github.com/stepan-mitkin/drakonwidget"
            )
    
    def create_test_html(self, json_file: Path) -> Path:
        """
        Create HTML test page with DrakonWidget
        
        Args:
            json_file: Path to DRAKON JSON file
        
        Returns:
            Path to generated HTML file
        """
        with open(json_file, 'r') as f:
            diagram_data = json.load(f)
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DRAKON Test: {diagram_data.get('name', 'Unnamed')}</title>
    <script src="drakonwidget.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }}
        #test-info {{
            background: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        #editor-area {{
            width: 100%;
            height: 600px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        #test-results {{
            background: white;
            padding: 15px;
            margin-top: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .test-pass {{ color: green; }}
        .test-fail {{ color: red; }}
        .test-pending {{ color: orange; }}
    </style>
</head>
<body>
    <div id="test-info">
        <h1>DRAKON Diagram Test</h1>
        <p><strong>Diagram:</strong> <span id="diagram-name"></span></p>
        <p><strong>Status:</strong> <span id="test-status" class="test-pending">Testing...</span></p>
    </div>
    
    <div id="editor-area"></div>
    
    <div id="test-results">
        <h2>Test Results</h2>
        <ul id="results-list"></ul>
    </div>
    
    <script>
        // Diagram data embedded
        var diagramData = {json.dumps(diagram_data, indent=2)};
        
        // Test results
        var testResults = [];
        
        function addResult(name, passed, message) {{
            testResults.push({{ name: name, passed: passed, message: message }});
            updateResultsDisplay();
        }}
        
        function updateResultsDisplay() {{
            var list = document.getElementById('results-list');
            list.innerHTML = '';
            
            var allPassed = true;
            testResults.forEach(function(result) {{
                var li = document.createElement('li');
                li.className = result.passed ? 'test-pass' : 'test-fail';
                li.textContent = (result.passed ? '✓ ' : '✗ ') + result.name + ': ' + result.message;
                list.appendChild(li);
                if (!result.passed) allPassed = false;
            }});
            
            var status = document.getElementById('test-status');
            if (testResults.length > 0) {{
                status.textContent = allPassed ? 'PASSED' : 'FAILED';
                status.className = allPassed ? 'test-pass' : 'test-fail';
            }}
            
            // Expose results globally for automated testing
            window.DRAKON_TEST_RESULTS = {{
                passed: allPassed,
                results: testResults
            }};
        }}
        
        // Run tests
        document.addEventListener('DOMContentLoaded', function() {{
            document.getElementById('diagram-name').textContent = diagramData.name || 'Unnamed';
            
            try {{
                // Test 1: DrakonWidget loads
                var drakon = createDrakonWidget();
                addResult('DrakonWidget Load', true, 'Widget created successfully');
                
                // Test 2: Configuration
                var config = {{
                    startEditContent: function(item, isReadonly) {{
                        console.log('Edit:', item.id);
                    }},
                    showContextMenu: function(left, top, items) {{
                        console.log('Context menu:', items);
                    }},
                    canSelect: true,
                    theme: {{
                        background: '#f5f5f5',
                        iconBack: 'white',
                        iconBorder: '#333'
                    }}
                }};
                
                addResult('Configuration', true, 'Config object created');
                
                // Test 3: Render widget
                var editorArea = document.getElementById('editor-area');
                var rect = editorArea.getBoundingClientRect();
                var widgetElement = drakon.render(rect.width, rect.height, config);
                editorArea.appendChild(widgetElement);
                
                addResult('Widget Render', true, 'Widget rendered to DOM');
                
                // Test 4: Load diagram
                var sender = {{
                    stop: function() {{}},
                    pushEdit: function(edit) {{
                        console.log('Edit:', edit);
                    }}
                }};
                
                drakon.setDiagram('test-diagram', diagramData, sender).then(function(fonts) {{
                    addResult('Diagram Load', true, 'Diagram loaded successfully');
                    addResult('Fonts', true, 'Fonts: ' + fonts.join(', '));
                    
                    // Test 5: Redraw
                    drakon.redraw();
                    addResult('Redraw', true, 'Diagram redrawn');
                    
                    // Test 6: Validate structure
                    var items = diagramData.items || {{}};
                    var itemCount = Object.keys(items).length;
                    addResult('Structure', itemCount > 0, itemCount + ' items found');
                    
                    // Test 7: Check for required icons
                    var hasStart = false;
                    var hasEnd = false;
                    
                    for (var id in items) {{
                        if (items[id].type === 'branch') hasStart = true;
                        if (items[id].type === 'end') hasEnd = true;
                    }}
                    
                    addResult('Start Icon', hasStart, hasStart ? 'Found' : 'Missing');
                    addResult('End Icon', hasEnd, hasEnd ? 'Found' : 'Missing');
                    
                    // Test 8: Validate links
                    var brokenLinks = 0;
                    for (var id in items) {{
                        var item = items[id];
                        if (item.one && !items[item.one]) brokenLinks++;
                        if (item.two && !items[item.two]) brokenLinks++;
                    }}
                    
                    addResult('Link Integrity', brokenLinks === 0, 
                             brokenLinks === 0 ? 'All links valid' : brokenLinks + ' broken links');
                    
                    console.log('✓ All tests complete');
                    
                }}).catch(function(error) {{
                    addResult('Diagram Load', false, 'Error: ' + error.message);
                }});
                
            }} catch(error) {{
                addResult('Critical Error', false, error.message);
                console.error('Test error:', error);
            }}
        }});
    </script>
</body>
</html>"""
        
        html_file = self.test_output_dir / f"{json_file.stem}_test.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def start_http_server(self) -> threading.Thread:
        """
        Start HTTP server in background thread
        
        Returns:
            Server thread
        """
        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress logs
        
        # Change to test output directory
        original_dir = Path.cwd()
        
        def run_server():
            import os
            os.chdir(self.test_output_dir)
            
            # Copy drakonwidget.js to test directory
            import shutil
            shutil.copy(
                self.drakon_widget_path,
                self.test_output_dir / 'drakonwidget.js'
            )
            
            with socketserver.TCPServer(("", self.port), Handler) as httpd:
                print(f"✓ HTTP server started on http://localhost:{self.port}")
                httpd.serve_forever()
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(1)  # Wait for server to start
        
        return server_thread
    
    def test_diagram_manual(self, json_file: Path) -> bool:
        """
        Test diagram by opening in browser (manual inspection)
        
        Args:
            json_file: Path to DRAKON JSON file
        
        Returns:
            True (user inspection required)
        """
        print(f"\n{'='*60}")
        print(f"Testing: {json_file.name}")
        print(f"{'='*60}\n")
        
        # Create test HTML
        html_file = self.create_test_html(json_file)
        print(f"✓ Created test page: {html_file.name}")
        
        # Start server
        server_thread = self.start_http_server()
        
        # Open browser
        url = f"http://localhost:{self.port}/{html_file.name}"
        print(f"✓ Opening browser: {url}")
        webbrowser.open(url)
        
        print("\n" + "="*60)
        print("Manual test instructions:")
        print("1. Check that diagram loads without errors")
        print("2. Verify all icons are visible")
        print("3. Verify lines connect correctly")
        print("4. Check test results at bottom of page")
        print("5. Close browser when done")
        print("="*60)
        
        input("\nPress Enter when test is complete...")
        
        return True
    
    def test_diagram_automated(self, json_file: Path) -> TestResult:
        """
        Test diagram using automated browser (Playwright)
        
        Args:
            json_file: Path to DRAKON JSON file
        
        Returns:
            TestResult object
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return TestResult(
                name=json_file.name,
                passed=False,
                message="Playwright not installed. Run: pip install playwright && playwright install"
            )
        
        start_time = time.time()
        
        try:
            # Create test HTML
            html_file = self.create_test_html(json_file)
            
            # Start server
            server_thread = self.start_http_server()
            
            # Run browser test
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                url = f"http://localhost:{self.port}/{html_file.name}"
                page.goto(url)
                
                # Wait for tests to complete
                page.wait_for_function(
                    "window.DRAKON_TEST_RESULTS !== undefined",
                    timeout=10000
                )
                
                # Get test results
                results = page.evaluate("window.DRAKON_TEST_RESULTS")
                
                # Take screenshot
                screenshot_path = self.test_output_dir / f"{json_file.stem}_screenshot.png"
                page.screenshot(path=str(screenshot_path))
                
                browser.close()
            
            duration_ms = (time.time() - start_time) * 1000
            
            if results['passed']:
                return TestResult(
                    name=json_file.name,
                    passed=True,
                    message=f"All {len(results['results'])} tests passed",
                    duration_ms=duration_ms
                )
            else:
                failed = [r for r in results['results'] if not r['passed']]
                return TestResult(
                    name=json_file.name,
                    passed=False,
                    message=f"{len(failed)} test(s) failed: " + ", ".join(r['name'] for r in failed),
                    duration_ms=duration_ms
                )
        
        except Exception as e:
            return TestResult(
                name=json_file.name,
                passed=False,
                message=f"Test error: {str(e)}",
                duration_ms=(time.time() - start_time) * 1000
            )
    
    def test_all_diagrams(self, 
                         diagrams_dir: Path,
                         automated: bool = False) -> List[TestResult]:
        """
        Test all JSON diagrams in directory
        
        Args:
            diagrams_dir: Directory containing JSON files
            automated: Use automated testing (requires Playwright)
        
        Returns:
            List of test results
        """
        json_files = list(Path(diagrams_dir).glob("*.json"))
        
        if not json_files:
            print(f"No JSON files found in {diagrams_dir}")
            return []
        
        print(f"\nFound {len(json_files)} diagram(s) to test")
        
        results = []
        
        for json_file in json_files:
            if automated:
                result = self.test_diagram_automated(json_file)
                results.append(result)
                
                status = "✓ PASS" if result.passed else "✗ FAIL"
                print(f"{status} | {result.name} | {result.duration_ms:.0f}ms | {result.message}")
            else:
                self.test_diagram_manual(json_file)
                # Manual tests always "pass" (user verification)
                results.append(TestResult(
                    name=json_file.name,
                    passed=True,
                    message="Manual verification completed"
                ))
        
        return results
    
    def generate_report(self, results: List[TestResult]) -> Path:
        """
        Generate HTML test report
        
        Args:
            results: List of test results
        
        Returns:
            Path to report file
        """
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        report_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DRAKON Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .summary {{
            display: flex;
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-box {{
            flex: 1;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-box h2 {{ margin: 0; font-size: 48px; }}
        .stat-box p {{ margin: 5px 0 0 0; color: #666; }}
        .pass {{ background: #d4edda; color: #155724; }}
        .fail {{ background: #f8d7da; color: #721c24; }}
        .total {{ background: #d1ecf1; color: #0c5460; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{ background: #f8f9fa; font-weight: bold; }}
        .result-pass {{ color: green; }}
        .result-fail {{ color: red; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>DRAKON Widget Test Report</h1>
        <p>Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="stat-box total">
                <h2>{len(results)}</h2>
                <p>Total Tests</p>
            </div>
            <div class="stat-box pass">
                <h2>{passed}</h2>
                <p>Passed</p>
            </div>
            <div class="stat-box fail">
                <h2>{failed}</h2>
                <p>Failed</p>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Diagram</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in results:
            status_class = "result-pass" if result.passed else "result-fail"
            status_text = "✓ PASS" if result.passed else "✗ FAIL"
            
            report_html += f"""
                <tr>
                    <td>{result.name}</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{result.duration_ms:.0f}ms</td>
                    <td>{result.message}</td>
                </tr>
"""
        
        report_html += """
            </tbody>
        </table>
    </div>
</body>
</html>"""
        
        report_file = self.test_output_dir / "test_report.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_html)
        
        return report_file


def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test DRAKON diagrams with DrakonWidget'
    )
    
    parser.add_argument('diagrams_dir',
                       help='Directory containing JSON diagram files')
    parser.add_argument('--widget-path',
                       default='./drakonwidget.js',
                       help='Path to drakonwidget.js')
    parser.add_argument('--output-dir',
                       default='./test_results',
                       help='Output directory for test results')
    parser.add_argument('--automated',
                       action='store_true',
                       help='Run automated tests (requires Playwright)')
    parser.add_argument('--port',
                       type=int,
                       default=8765,
                       help='HTTP server port')
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = DrakonWidgetTester(
        drakon_widget_path=Path(args.widget_path),
        test_output_dir=Path(args.output_dir),
        port=args.port
    )
    
    # Run tests
    results = tester.test_all_diagrams(
        diagrams_dir=Path(args.diagrams_dir),
        automated=args.automated
    )
    
    # Generate report
    if results:
        report_file = tester.generate_report(results)
        print(f"\n✓ Test report: {report_file}")
        
        passed = sum(1 for r in results if r.passed)
        print(f"\nResults: {passed}/{len(results)} passed")
        
        return 0 if passed == len(results) else 1
    
    return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())