# DrakonWidget Headless Generator Service

**Status:** 🚧 Proof of Concept (Not yet implemented)
**Purpose:** Generate valid DRAKON diagrams using official drakonWidget.js API via headless browser
**Architecture:** Node.js + Express.js + Puppeteer

---

## Why This Service Exists

### The Problem
Current system manually constructs DRAKON JSON:
- ❌ Brittle (breaks with format changes)
- ❌ No automatic validation
- ❌ Risk of incompatibility with official DRAKON editors

### The Solution
Use **drakonWidget.js** (official library by Stepan Mitkin) to generate diagrams:
- ✅ 100% format compatibility guaranteed
- ✅ Future-proof (auto-updates with library)
- ✅ Built-in validation
- ✅ Full feature support (auto-layout, advanced nodes)

### The Challenge
drakonWidget.js requires browser environment (DOM, Canvas API, window object)

### The Architecture
```
Python Backend (code_to_drakon.py)
    ↓ HTTP POST /generate
Node.js Microservice (this service)
    ↓
Puppeteer Controller
    ↓
Headless Chrome Instance (pooled)
    ↓ Loads drakonWidget.js
drakonWidget API (programmatic calls)
    ↓ Exports diagram
Valid JSON Response
```

---

## Quick Start (When Implemented)

### Installation
```bash
cd /home/vokov/motia_drn_start/services/drakon-generator
npm install
```

### Running the Service
```bash
# Development mode
npm run dev

# Production mode
npm start
```

### Testing
```bash
# Test single diagram generation
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d @test/sample_diagram.json
```

---

## API Specification

### POST /generate

**Request:**
```json
{
  "commands": [
    {"type": "createDiagram", "name": "Example Flow"},
    {"type": "addNode", "nodeType": "action", "content": "Step 1", "id": "1"},
    {"type": "addNode", "nodeType": "action", "content": "Step 2", "id": "2"},
    {"type": "connect", "from": "1", "to": "2"}
  ]
}
```

**Response (Success):**
```json
{
  "success": true,
  "diagram": {
    "name": "Example Flow",
    "access": "write",
    "params": [],
    "items": {
      "1": {"type": "action", "content": "Step 1", "one": "2"},
      "2": {"type": "action", "content": "Step 2"}
    }
  },
  "generationTime": 1234
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid command sequence",
  "details": "..."
}
```

---

## Project Structure (Planned)

```
services/drakon-generator/
├── README.md (this file)
├── package.json
├── src/
│   ├── server.js           # Express.js app
│   ├── puppeteer-pool.js   # Browser instance pool manager
│   ├── diagram-builder.js  # Command → drakonWidget API translator
│   └── utils/
│       ├── validator.js    # Command validation
│       └── logger.js       # Logging
├── public/
│   └── host.html          # Minimal HTML page for drakonWidget
├── test/
│   ├── sample_diagram.json
│   └── integration.test.js
└── Dockerfile
```

---

## Implementation Checklist

### Phase 1: Basic POC (Week 1)
- [ ] Setup npm project (`npm init`)
- [ ] Install dependencies (`express`, `puppeteer`)
- [ ] Create minimal `server.js`
- [ ] Create `host.html` with drakonWidget
- [ ] Implement single diagram generation
- [ ] Test: Generate 1 diagram manually

### Phase 2: Full Service (Weeks 2-3)
- [ ] Implement browser instance pooling
- [ ] Create command schema & validation
- [ ] Implement all drakonWidget API wrappers
- [ ] Add error handling & logging
- [ ] Performance optimization
- [ ] Integration tests (10+ diagrams)

### Phase 3: Python Integration
- [ ] Refactor `code_to_drakon.py`
- [ ] Replace manual JSON with HTTP client
- [ ] Migrate existing diagrams
- [ ] Benchmarking & optimization

---

## Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| **Cold start** | < 5s | Pre-warm browser pool on startup |
| **Warm request** | < 2s | Reuse existing browser instances |
| **Concurrent requests** | 10+ | Pool size = 5-10 instances |
| **Memory usage** | < 500MB | Instance limit, auto-cleanup |

---

## Alternative: Direct .drn Generation

For high-performance batch processing, use SQLite directly:

```python
# tools/drakon/converter/drn_generator.py
import sqlite3

def generate_drn(diagram_data, output_path):
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()

    # Create tables (diagrams, items)
    # Insert data
    # ...

    conn.commit()
    conn.close()
```

**Use cases:**
- CI/CD bulk processing (1000+ files)
- Fallback if service unavailable
- `--mode=sqlite` flag in workflow script

---

## Dependencies

```json
{
  "name": "drakon-generator",
  "version": "0.1.0",
  "dependencies": {
    "express": "^4.18.0",
    "puppeteer": "^21.0.0",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "supertest": "^6.3.0"
  }
}
```

---

## Docker Deployment

### docker-compose.yml
```yaml
services:
  drakon-generator:
    build: ./services/drakon-generator
    ports:
      - "3000:3000"
    environment:
      - PUPPETEER_HEADLESS=true
      - INSTANCE_POOL_SIZE=5
      - LOG_LEVEL=info
    volumes:
      - ./tools/drakon-viewer/public/js:/app/drakonwidget:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Dockerfile
```dockerfile
FROM node:18-alpine

# Install Chromium for Puppeteer
RUN apk add --no-cache chromium

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
EXPOSE 3000

CMD ["node", "src/server.js"]
```

---

## Resources

### Gemini AI Pro Research
- Full report: `../../deep-research/Enhancing DRAKON Diagram Generation.pdf`
- Analysis: `../../GEMINI_RESEARCH_ANALYSIS.md`
- Roadmap: `../../IMPLEMENTATION_ROADMAP.md`

### Official DRAKON
- drakonWidget: https://github.com/stepan-mitkin/drakonwidget
- Desktop Editor: https://drakon-editor.sourceforge.net/
- .drn format spec: https://drakon-editor.sourceforge.net/file_format.html

### Tools
- Puppeteer docs: https://pptr.dev/
- Express.js: https://expressjs.com/

---

**Status:** 📋 Ready to implement
**Next Step:** Create `package.json` and `server.js` POC
**Estimated Effort:** Phase 1 = 1 week
