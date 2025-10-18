# DRAKON Editor v3.2 - Playwright Automated Tests

These files implement the automated test plan you provided as a Playwright script.

## Files created
- package.json
- test.js (Playwright script that implements Tests 1..10)
- README.md (this file)

## Requirements
- Node.js (>=16)
- npm
- Recommended: run in a machine with GUI (the script launches Chromium in non-headless mode by default)

## Install & Run
1. Extract this folder (if downloaded).
2. In the folder, run:
   ```bash
   npm install
   npx playwright install
   npm test
   ```
3. The script will open Chromium, run tests sequentially, capture console logs, and save:
   - `AI_browser_test_report.md` in the same folder
   - screenshots on failures (failure_*.png)
   - downloaded JSON files into `downloads/` directory

## Notes & Troubleshooting
- The script uses heuristic selectors to interact with the app. If your app uses different button labels or custom modals, adjust selector strings in `test.js`.
- If a native `prompt()` is used to enter the diagram name, Playwright cannot fill native prompts; the script attempts to fallback to in-page API calls.
- For headless execution, change `headless: false` to `true` in the script (in browser.launch).

## Where files are saved in this environment
The generated files are available from the notebook filesystem at:
`/mnt/data/drakon_playwright_test/`

After running `npm test` locally, the generated report will appear at:
`/path/to/drakon_playwright_test/AI_browser_test_report.md`
