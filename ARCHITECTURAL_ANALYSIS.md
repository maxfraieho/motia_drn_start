# Comprehensive Architectural Analysis Report
## Claude Code Telegram Bot → Motia Framework Refactoring

**Generated**: 2025-10-09
**Source File**: `/home/vokov/motia/src.md`
**Total Lines**: 34,620
**Total Components**: 93 files

---

## Executive Summary

This is a sophisticated **Telegram Bot** that provides remote access to **Claude AI CLI**, featuring:
- Real-time Claude Code integration with streaming responses
- Multi-language support (Ukrainian/English)
- MCP (Model Context Protocol) server management
- Advanced image processing capabilities
- DRACON diagram system for workflow visualization
- Comprehensive security and rate limiting
- Scheduled task execution with auto-response
- Session persistence and state management

### Current Architecture Pattern
**Monolithic Application** with modular organization following **Layered Architecture**:
```
├── Presentation Layer (Bot Handlers)
├── Business Logic Layer (Features/Services)
├── Integration Layer (Claude/MCP)
├── Data Access Layer (Storage/Repositories)
└── Infrastructure Layer (Config/Security/Utils)
```

---

## Component Inventory & Analysis

### 1. CONFIGURATION LAYER

#### 1.1 Config Module (`/home/vokov/motia/src.md` lines 2372-3111)

**Files**:
- `config/__init__.py` (390 bytes)
- `config/settings.py` (12,536 bytes) - Main configuration with Pydantic
- `config/loader.py` (6,316 bytes) - Environment-based config loading
- `config/features.py` (3,408 bytes) - Feature flags management
- `config/environments.py` (2,275 bytes) - Environment-specific overrides

**Primary Responsibility**: Centralized configuration management with validation

**Input/Output**:
- **Input**: Environment variables (.env), YAML config files
- **Output**: Validated `Settings` object with typed properties

**Dependencies**:
- `pydantic` for validation
- `pydantic-settings` for env var loading
- `python-dotenv` for .env file support

**Motia Step Recommendation**: **Noop Step**
- **Type**: External Configuration Provider
- **Pattern**: Factory + Builder
- **Justification**: Configuration is a cross-cutting concern that should be injected as a dependency

**Data Structures**:
```python
Settings {
  telegram_bot_token: SecretStr
  approved_directory: Path
  claude_cli_path: Optional[str]
  claude_model: str = "claude-3-5-sonnet-20241022"
  rate_limit_requests: int
  database_url: str
  enable_mcp: bool
  enable_image_processing: bool
  enable_localization: bool
  claude_availability: ClaudeAvailabilitySettings
}

ClaudeAvailabilitySettings {
  enabled: bool
  check_interval_seconds: int
  notify_chat_ids: List[int]
  dnd_start: time
  dnd_end: time
}
```

---

### 2. SECURITY LAYER

#### 2.1 Authentication Module (`/home/vokov/motia/src.md` lines ~32000+)

**Files**:
- `security/auth.py` - Multi-provider authentication
- `security/validators.py` - Path and input validation
- `security/rate_limiter.py` (10,493 bytes) - Token bucket rate limiting
- `security/audit.py` - Audit logging

**Primary Responsibility**: Secure access control and request validation

**Event Triggers**:
- Every incoming Telegram message/callback
- Before each Claude CLI execution
- File operation requests

**Authentication Flow**:
```
Telegram Update → AuthenticationManager → [
  WhitelistAuthProvider (user_id check)
  TokenAuthProvider (JWT/token validation)
] → Authorization Decision
```

**Motia Step Recommendation**: **API Step Middleware**
- **Type**: Pre-request Middleware Chain
- **Pattern**: Chain of Responsibility + Strategy
- **Justification**: Authentication should be a reusable middleware that can be composed

**Key Components**:
1. **AuthenticationManager** (Mediator pattern)
2. **WhitelistAuthProvider** (Strategy)
3. **TokenAuthProvider** (Strategy)
4. **SecurityValidator** (Validator pattern)
5. **RateLimiter** (Token Bucket algorithm)

**Rate Limiting Design**:
```python
RateLimitBucket {
  capacity: int
  tokens: float
  last_update: datetime
  refill_rate: float

  consume(tokens) -> bool
  get_wait_time(tokens) -> float
}

RateLimiter {
  request_buckets: Dict[user_id, RateLimitBucket]
  cost_tracker: Dict[user_id, float]

  check_rate_limit(user_id, cost, tokens) -> (allowed, message)
}
```

---

### 3. STORAGE LAYER

#### 3.1 Database Management (`/home/vokov/motia/src.md` lines 32492-33912)

**Files**:
- `storage/database.py` - Async SQLite/PostgreSQL connection manager
- `storage/models.py` - SQLAlchemy ORM models
- `storage/repositories.py` - Repository pattern for data access
- `storage/facade.py` - Storage facade pattern
- `storage/session_storage.py` - Session persistence

**Primary Responsibility**: Data persistence and retrieval

**Database Schema** (Key Tables):
```sql
-- User sessions
CREATE TABLE user_sessions (
  user_id INTEGER PRIMARY KEY,
  session_id TEXT,
  working_directory TEXT,
  created_at TIMESTAMP,
  last_used TIMESTAMP
);

-- MCP servers configuration
CREATE TABLE user_mcp_servers (
  user_id INTEGER,
  server_name TEXT,
  server_type TEXT,
  server_command TEXT,
  server_args JSON,
  server_env JSON,
  is_enabled BOOLEAN,
  status TEXT,
  PRIMARY KEY (user_id, server_name)
);

-- MCP usage tracking
CREATE TABLE mcp_usage_log (
  user_id INTEGER,
  server_name TEXT,
  query TEXT,
  response_time INTEGER,
  success BOOLEAN,
  cost REAL,
  created_at TIMESTAMP
);

-- Localization preferences
CREATE TABLE user_language_preferences (
  user_id INTEGER PRIMARY KEY,
  language_code TEXT,
  updated_at TIMESTAMP
);

-- Scheduled prompts
CREATE TABLE scheduled_prompts (
  id TEXT PRIMARY KEY,
  title TEXT,
  prompt TEXT,
  enabled BOOLEAN,
  schedule JSON,
  conditions JSON
);
```

**Motia Step Recommendation**: **Noop Step**
- **Type**: Data Repository Service
- **Pattern**: Repository + Unit of Work
- **Justification**: Database access should be abstracted behind repositories

**Key Patterns**:
1. **Facade Pattern**: `Storage` class provides unified interface
2. **Repository Pattern**: Separate repos for different entities
3. **Connection Pooling**: Async context managers for connections
4. **Transaction Management**: Commit/rollback support

---

### 4. CLAUDE INTEGRATION LAYER

#### 4.1 Claude CLI Integration (`/home/vokov/motia/src.md` lines 3113-5989)

**Files**:
- `claude/facade.py` (32,527 bytes) - Main integration facade
- `claude/integration.py` - Process manager for CLI
- `claude/sdk_integration.py` (15,963 bytes) - Python SDK integration
- `claude/session.py` - Session management
- `claude/monitor.py` (7,092 bytes) - Tool usage monitoring
- `claude/parser.py` - Output parsing
- `claude/exceptions.py` - Claude-specific errors

**Primary Responsibility**: Execute Claude AI commands and manage sessions

**Architecture**:
```
ClaudeIntegration (Facade)
  ├── ClaudeProcessManager (CLI subprocess)
  ├── ClaudeSDKManager (Python SDK - disabled)
  ├── SessionManager (session persistence)
  ├── ToolMonitor (security validation)
  └── OutputParser (response formatting)
```

**Execution Flow**:
```
1. Receive prompt from user
2. SessionManager → Get/Create session
3. ToolMonitor → Validate allowed tools
4. Process/SDK Manager → Execute Claude CLI
5. Parser → Extract response, tools used, cost
6. SessionStorage → Persist session state
7. Return ClaudeResponse
```

**Data Structures**:
```python
ClaudeResponse {
  content: str
  session_id: str
  cost: float
  duration_ms: int
  num_turns: int
  is_error: bool
  error_type: Optional[str]
  tools_used: List[Dict[str, Any]]
}

ClaudeSession {
  session_id: str
  user_id: int
  working_directory: Path
  created_at: datetime
  last_used: datetime
  conversation_turns: int
}
```

**Tool Monitoring**:
```python
Allowed Tools: [
  "Read", "Write", "Edit", "Bash", "Glob", "Grep",
  "Task", "MultiEdit", "NotebookRead", "NotebookEdit",
  "WebFetch", "TodoRead", "TodoWrite", "WebSearch"
]

Disallowed: ["git commit", "git push"]
```

**Motia Step Recommendation**: **API Step**
- **Type**: External API Integration
- **Pattern**: Facade + Strategy + Observer
- **Justification**: Claude integration is a core business capability that should be wrapped as a service

**Key Responsibilities**:
1. CLI subprocess management
2. Streaming response handling
3. Tool usage validation
4. Cost tracking
5. Session persistence
6. Error recovery

---

### 5. MCP (Model Context Protocol) LAYER

#### 5.1 MCP Server Management (`/home/vokov/motia/src.md` lines 783-2370)

**Files**:
- `mcp/manager.py` (20,120 bytes) - Core MCP server lifecycle
- `mcp/context_handler.py` (12,431 bytes) - Context selection & execution
- `mcp/server_configs.py` (18,508 bytes) - Server templates
- `mcp/claude_integration.py` (9,196 bytes) - Claude CLI MCP bridge
- `mcp/exceptions.py` - MCP-specific errors

**Primary Responsibility**: Manage MCP servers for extended Claude capabilities

**Supported Server Types**:
1. **GitHub** - Repository access, issues, PRs
2. **Filesystem** - File read/write in specified directories
3. **PostgreSQL** - Database queries and management
4. **SQLite** - Local database access
5. **Git** - Repository operations
6. **Playwright** - Web automation and scraping

**MCP Architecture**:
```
MCPManager
  ├── get_server_templates() - Available server configs
  ├── add_server(user_id, config) - Register new server
  ├── enable_server(user_id, name) - Activate server
  ├── disable_server(user_id, name) - Deactivate server
  ├── get_server_status(user_id, name) - Health check
  └── log_usage(user_id, server, query, success) - Analytics

MCPContextHandler
  ├── get_active_context(user_id) - Current server selection
  ├── set_active_context(user_id, server) - Switch context
  ├── execute_contextual_query(user_id, query) - Run with context
  └── get_context_suggestions(user_id, query) - Smart suggestions
```

**Server Configuration Template**:
```python
MCPServerConfig {
  name: str
  server_type: str
  command: str  # e.g., "npx"
  args: List[str]  # e.g., ["-y", "@modelcontextprotocol/server-github"]
  env: Dict[str, str]  # API keys, tokens
  config: Dict[str, Any]  # Server-specific settings
  is_enabled: bool
}
```

**Example: GitHub Server Setup**:
```python
{
  "name": "github-main",
  "server_type": "github",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
  },
  "config": {},
  "is_enabled": true
}
```

**Motia Step Recommendation**: **Event Step**
- **Type**: Background Service Manager
- **Pattern**: Strategy + Factory + Observer
- **Justification**: MCP servers are external service integrations that should be managed asynchronously

**Context-Aware Execution**:
```
User Query → MCPContextHandler → Active Server → Claude CLI with MCP → Response
```

**Smart Suggestions**:
- Analyzes query content (keywords: "github", "file", "database", etc.)
- Suggests relevant servers based on context
- Tracks usage patterns for recommendations

---

### 6. BOT CORE LAYER

#### 6.1 Telegram Bot Handlers (`/home/vokov/motia/src.md` lines 7532-17822)

**Files**:
- `bot/core.py` (8,061 lines total section) - Main bot application
- `bot/handlers/command.py` (3,503 lines) - Command handlers
- `bot/handlers/message.py` (1,488 lines) - Message processing
- `bot/handlers/callback.py` (2,847 lines) - Button callbacks
- `bot/handlers/mcp_commands.py` (2,548 lines) - MCP management commands
- `bot/handlers/mcp_callbacks.py` (537 lines) - MCP button interactions
- `bot/handlers/task_commands.py` (285 lines) - Task management
- `bot/handlers/image_command.py` (387 lines) - Image processing
- `bot/handlers/dnd_prompts.py` (317 lines) - Do Not Disturb prompts
- `bot/handlers/scheduled_prompts_handler.py` (253 lines) - Scheduled tasks

**Core Commands**:
```
User Commands:
  /start - Initialize bot
  /help - Show help
  /lang - Change language
  /status - System status
  /session - Session management
  /cd <path> - Change directory
  /pwd - Print working directory
  /ls - List files
  /tasks - Task management

MCP Commands:
  /mcpadd - Add MCP server
  /mcplist - List servers
  /mcpselect - Select active context
  /mcpask <query> - Execute with MCP context
  /mcpremove - Remove server
  /mcpstatus - System status

Image Commands:
  /image <prompt> - Generate image with Claude
  /analyze <image> - Analyze uploaded image

DND Commands:
  /dndadd - Add scheduled prompt
  /dndlist - List scheduled prompts
  /dndenable - Enable DND mode
  /dnddisable - Disable DND mode
```

**Message Flow Architecture**:
```
Telegram Update
  ↓
Middleware Chain [
  AuthenticationMiddleware
  RateLimitMiddleware
  ClaudeAvailabilityMiddleware
  SecurityMiddleware
]
  ↓
Router (telegram.ext.Application)
  ├── CommandHandler → command.py
  ├── MessageHandler → message.py
  ├── CallbackQueryHandler → callback.py
  └── ErrorHandler → error_handler.py
  ↓
Feature Services
  ↓
Claude Integration
  ↓
Response Formatting
  ↓
Telegram API
```

**Motia Step Recommendations**:

1. **Command Handlers** → **API Steps**
   - Each command as separate REST endpoint
   - Pattern: Command Pattern
   - HTTP POST `/bot/command/{command_name}`

2. **Message Handler** → **Stream Step**
   - Real-time message processing
   - Pattern: Observer + Mediator
   - WebSocket or SSE for streaming responses

3. **Callback Handlers** → **Event Steps**
   - Async button interaction processing
   - Pattern: Event-Driven + State Machine

**State Management**:
```python
UserState {
  current_directory: Path
  claude_session_id: Optional[str]
  mcp_active_context: Optional[str]
  language: str
  conversation_turn: int
  last_interaction: datetime
}
```

---

### 7. FEATURE MODULES

#### 7.1 Image Processing (`/home/vokov/motia/src.md` lines 27942-28346)

**Files**:
- `bot/features/image_processor.py` (404 lines)
- `bot/handlers/image_command.py` (387 lines)

**Capabilities**:
- Upload image to Telegram
- Process with Claude Vision
- Generate images based on text prompts
- Batch processing (up to 5 images)
- Image optimization and validation

**Image Processing Flow**:
```
User uploads image/photo
  ↓
ImageProcessor.validate_image()
  ├── Check file size (<20MB)
  ├── Check dimensions (32x32 to 4096x4096)
  └── Validate format (JPEG, PNG, WebP, GIF)
  ↓
ImageProcessor.optimize_image()
  ├── Resize if too large
  ├── Compress (JPEG quality 85)
  └── Convert to base64
  ↓
ClaudeIntegration.process_with_image()
  ↓
Parse Claude response
  ↓
Send formatted response to user
```

**Data Structures**:
```python
ProcessedImage {
  original_path: Path
  processed_path: Path
  width: int
  height: int
  format: str
  file_size: int
  base64_data: str
}
```

**Motia Step Recommendation**: **Event Step**
- **Type**: Async File Processing
- **Pattern**: Pipeline + Strategy
- **Justification**: Image processing is compute-intensive and should run asynchronously

---

#### 7.2 DRACON Diagram System (`/home/vokov/motia/src.md` lines 19935-27194)

**Files**:
- `bot/features/dracon_types.py` (315 lines) - Core data types
- `bot/features/dracon_parser.py` (21,499 bytes) - YAML/JSON parsing
- `bot/features/dracon_renderer.py` (23,299 bytes) - SVG/PNG generation
- `bot/features/dracon_generator.py` (15,621 lines) - Code generation
- `bot/features/dracon_storage.py` (14,498 lines) - Schema storage
- `bot/features/dracon_reverse_engineer.py` (12,653 lines) - Reverse engineering
- `bot/features/dracon_enhanced.py` (9,415 lines) - Enhanced features
- `bot/features/dracon_yaml.py` (14,932 lines) - YAML serialization
- `bot/features/demo_dracon_system.py` (234 lines) - Demo workflows

**DRACON Architecture**:
```
DRACON System
  ├── Types Layer (Node, Edge, Schema definitions)
  ├── Parser Layer (YAML → AST)
  ├── Renderer Layer (AST → SVG/PNG)
  ├── Generator Layer (AST → Python/Telegram code)
  ├── Storage Layer (Schema persistence)
  ├── Reverse Engineer (Python → DRACON schema)
  └── Enhanced Features (AI-powered suggestions)
```

**Node Types**:
```python
NodeType:
  - TITLE: Workflow title/header
  - ACTION: Executable action/command
  - QUESTION: Decision point (if/else)
  - CASE: Multi-way branch (switch/case)
  - LOOP_START: Loop beginning
  - LOOP_END: Loop termination
  - ADDRESS: Jump target/label
  - END: Workflow endpoint
  - PARALLEL_START: Concurrent execution start
  - PARALLEL_END: Concurrent execution join
```

**DRACON Schema Format**:
```yaml
version: "1.0"
name: "Bot Main Menu Flow"
metadata:
  author: "DRACON Generator"
  created: "2024-01-01"

nodes:
  - id: "start"
    type: "start"
    position: [0, 0]
    properties:
      text: "Bot Start"

  - id: "main_menu"
    type: "message"
    position: [100, 0]
    properties:
      template: "🏠 **Main Menu**\n\nChoose an action:"

edges:
  - id: "start_to_menu"
    from_node: "start"
    to_node: "main_menu"
    type: "sequence"
```

**Code Generation Capability**:
- Generates Telegram bot handlers from DRACON schemas
- Creates command handlers, callback handlers, message templates
- Produces button configurations and inline keyboards
- Auto-generates state machine logic

**Motia Step Recommendation**: **Noop Step**
- **Type**: Workflow Definition Service
- **Pattern**: Builder + Interpreter
- **Justification**: DRACON is a meta-system for defining workflows, should be external tooling

---

#### 7.3 Scheduled Prompts (`/home/vokov/motia/src.md` lines 18650-19268)

**Files**:
- `bot/features/scheduled_prompts.py` (26,083 bytes)
- `bot/handlers/scheduled_prompts_handler.py` (253 lines)

**Purpose**: Execute Claude commands automatically during DND (Do Not Disturb) periods

**Schedule Types**:
- **Daily**: Run at specific time every day
- **Weekly**: Run on specific day of week
- **Interval**: Run every N hours/minutes

**Prompt Configuration**:
```json
{
  "id": "daily_code_review",
  "title": "Щоденний огляд коду",
  "prompt": "Проаналізуй останні зміни в проекті",
  "enabled": true,
  "schedule": {
    "type": "daily",
    "time": "02:00",
    "timezone": "Europe/Kyiv"
  },
  "conditions": {
    "claude_available": true,
    "dnd_period": true,
    "no_user_activity_hours": 2
  }
}
```

**Auto-Responder**:
```python
AutoResponder {
  response_patterns: Dict[regex, response]

  Patterns:
    "continue?" → "yes"
    "overwrite?" → "yes"
    "commit changes?" → "yes"
    "press enter" → "\n"
}
```

**Motia Step Recommendation**: **Cron Step**
- **Type**: Scheduled Background Tasks
- **Pattern**: Observer + Strategy
- **Justification**: Time-based task execution is core cron functionality

---

#### 7.4 Localization System (`/home/vokov/motia/src.md` lines 5990-7427)

**Files**:
- `localization/manager.py` (201 lines) - Translation manager
- `localization/storage.py` (111 lines) - User language preferences
- `localization/helpers.py` (41 lines) - Helper functions
- `localization/util.py` (90 lines) - Utility functions
- `localization/translations/uk.json` (730 lines) - Ukrainian translations
- `localization/translations/en.json` (251 lines) - English translations

**Supported Languages**:
- Ukrainian (uk) - Primary
- English (en) - Secondary

**Translation Structure**:
```json
{
  "commands": {
    "start": {
      "welcome": "Привіт! 👋",
      "description": "Почати роботу з ботом"
    },
    "help": {
      "title": "📖 Довідка",
      "description": "Показати довідку"
    }
  },
  "errors": {
    "rate_limit": "⏱️ Перевищено ліміт запитів",
    "auth_failed": "🛡️ Помилка автентифікації"
  },
  "mcp": {
    "add": {
      "select_type": "Оберіть тип MCP сервера:",
      "success": "✅ Сервер додано успішно"
    }
  }
}
```

**Motia Step Recommendation**: **Noop Step**
- **Type**: Internationalization Service
- **Pattern**: Strategy + Factory
- **Justification**: i18n is cross-cutting infrastructure concern

---

#### 7.5 Availability Monitor (`/home/vokov/motia/src.md` lines 28347-29239)

**Files**:
- `bot/features/availability_monitor.py` (892 lines)
- `bot/middleware/claude_availability.py` (993 lines)

**Purpose**: Monitor Claude CLI availability and notify users

**Monitoring Flow**:
```
Background Task (every 60s)
  ↓
Check Claude CLI status
  ↓
If unavailable → Track consecutive failures
  ↓
If DND period → Skip notifications
  ↓
If debounce threshold met → Notify users
  ↓
Update cache and metrics
```

**Availability States**:
- **AVAILABLE**: Claude CLI responding normally
- **UNAVAILABLE**: Cannot reach Claude CLI
- **DEGRADED**: Slow response times
- **RECOVERING**: Coming back online

**Motia Step Recommendation**: **Cron Step**
- **Type**: Health Check Service
- **Pattern**: Observer + Circuit Breaker
- **Justification**: Periodic health checks are cron-based monitoring

---

### 8. UTILITY MODULES

#### 8.1 Response Formatting (`/home/vokov/motia/src.md` lines 30121-30836)

**Files**:
- `bot/utils/formatting.py` (25,721 bytes)

**Capabilities**:
- Split long messages (4000 char limit)
- Code block formatting with syntax highlighting
- Semantic chunking (text, code, file operations)
- Progress indicators (bars, spinners, dots)
- Context-aware keyboards

**Formatting Strategies**:
```python
ResponseFormatter:
  ├── _semantic_chunk() - Split by content type
  ├── _format_code_blocks() - Syntax highlighting
  ├── _split_message() - Respect Telegram limits
  ├── _escape_markdown_outside_code() - Safe escaping
  └── _get_contextual_keyboard() - Dynamic buttons
```

**Motia Step Recommendation**: **Noop Step**
- **Type**: Presentation Formatter
- **Pattern**: Strategy + Template Method
- **Justification**: Formatting is presentation layer concern

---

## Design Patterns Identified

### 1. **Facade Pattern**
- **Location**: `claude/facade.py`, `storage/facade.py`
- **Purpose**: Simplify complex subsystem interfaces
- **Motia Equivalent**: Service Interface Layer

### 2. **Strategy Pattern**
- **Location**: `security/auth.py` (AuthProviders)
- **Purpose**: Interchangeable authentication strategies
- **Motia Equivalent**: Plugin Architecture

### 3. **Repository Pattern**
- **Location**: `storage/repositories.py`
- **Purpose**: Abstract data access
- **Motia Equivalent**: Data Access Layer

### 4. **Observer Pattern**
- **Location**: `claude/integration.py` (streaming callbacks)
- **Purpose**: Event-driven architecture
- **Motia Equivalent**: Event Emitters

### 5. **Factory Pattern**
- **Location**: `mcp/server_configs.py` (server templates)
- **Purpose**: Create server configurations
- **Motia Equivalent**: Step Factory

### 6. **Chain of Responsibility**
- **Location**: Middleware chain in bot core
- **Purpose**: Sequential request processing
- **Motia Equivalent**: Middleware Pipeline

### 7. **Command Pattern**
- **Location**: Bot command handlers
- **Purpose**: Encapsulate requests as objects
- **Motia Equivalent**: API Endpoints

### 8. **State Pattern**
- **Location**: Session management
- **Purpose**: Manage user conversation state
- **Motia Equivalent**: State Machine Steps

### 9. **Builder Pattern**
- **Location**: DRACON schema construction
- **Purpose**: Step-by-step object creation
- **Motia Equivalent**: Workflow Builder

### 10. **Mediator Pattern**
- **Location**: `bot/core.py` (central coordination)
- **Purpose**: Coordinate between subsystems
- **Motia Equivalent**: Event Bus

---

## Motia Framework Migration Strategy

### Phase 1: Core Infrastructure (Weeks 1-2)

#### Step 1.1: Configuration Service (Noop Step)
```typescript
// motia-config-service
export default defineNoopStep({
  name: "config-service",
  description: "Centralized configuration management",
  provides: {
    settings: Settings,
    features: FeatureFlags,
  },
  runtime: "nodejs",
});
```

#### Step 1.2: Database Service (Noop Step)
```typescript
// motia-database-service
export default defineNoopStep({
  name: "database-service",
  description: "Storage and persistence layer",
  provides: {
    userRepository: UserRepository,
    sessionRepository: SessionRepository,
    mcpRepository: MCPRepository,
  },
  runtime: "nodejs",
  dependencies: ["config-service"],
});
```

### Phase 2: Authentication & Security (Week 3)

#### Step 2.1: Auth Middleware (API Step)
```typescript
// motia-auth-middleware
export default defineApiStep({
  name: "auth-middleware",
  description: "Multi-provider authentication",
  method: "middleware",
  pattern: "chain-of-responsibility",
  runtime: "nodejs",
  dependencies: ["config-service", "database-service"],

  async handler(req, res, next) {
    const user = await authManager.authenticate(req);
    if (!user) {
      return res.status(401).json({ error: "Unauthorized" });
    }
    req.user = user;
    next();
  }
});
```

#### Step 2.2: Rate Limiter (API Step)
```typescript
// motia-rate-limiter
export default defineApiStep({
  name: "rate-limiter",
  description: "Token bucket rate limiting",
  method: "middleware",
  pattern: "token-bucket",
  runtime: "nodejs",

  async handler(req, res, next) {
    const allowed = await rateLimiter.checkLimit(req.user.id);
    if (!allowed) {
      return res.status(429).json({ error: "Rate limit exceeded" });
    }
    next();
  }
});
```

### Phase 3: Claude Integration (Week 4)

#### Step 3.1: Claude API Service (API Step)
```typescript
// motia-claude-service
export default defineApiStep({
  name: "claude-service",
  description: "Claude AI integration facade",
  method: "POST",
  path: "/api/claude/execute",
  pattern: "facade",
  runtime: "nodejs",
  dependencies: ["config-service", "database-service"],

  async handler(req, res) {
    const { prompt, sessionId } = req.body;
    const response = await claudeIntegration.runCommand({
      prompt,
      userId: req.user.id,
      sessionId,
    });
    return res.json(response);
  }
});
```

#### Step 3.2: Session Manager (Noop Step)
```typescript
// motia-session-manager
export default defineNoopStep({
  name: "session-manager",
  description: "Claude session persistence",
  provides: {
    getSession: Function,
    createSession: Function,
    updateSession: Function,
  },
  runtime: "nodejs",
  dependencies: ["database-service"],
});
```

### Phase 4: MCP Integration (Week 5)

#### Step 4.1: MCP Manager Service (Event Step)
```typescript
// motia-mcp-manager
export default defineEventStep({
  name: "mcp-manager",
  description: "MCP server lifecycle management",
  pattern: "observer",
  runtime: "nodejs",
  dependencies: ["config-service", "database-service"],

  events: {
    "mcp.server.added": async (payload) => {
      await mcpManager.addServer(payload.userId, payload.config);
    },
    "mcp.server.enabled": async (payload) => {
      await mcpManager.enableServer(payload.userId, payload.serverName);
    },
    "mcp.server.status.check": async (payload) => {
      return await mcpManager.getServerStatus(payload.userId, payload.serverName);
    },
  }
});
```

#### Step 4.2: MCP Context Handler (Event Step)
```typescript
// motia-mcp-context
export default defineEventStep({
  name: "mcp-context-handler",
  description: "MCP context-aware query execution",
  pattern: "strategy",
  runtime: "nodejs",
  dependencies: ["mcp-manager", "claude-service"],

  events: {
    "mcp.context.execute": async (payload) => {
      const { userId, query } = payload;
      const context = await mcpContext.getActiveContext(userId);
      return await mcpContext.executeContextualQuery(userId, query, context);
    },
  }
});
```

### Phase 5: Telegram Bot Handlers (Week 6)

#### Step 5.1: Bot Commands (API Steps)
```typescript
// motia-bot-commands
export default defineApiStep({
  name: "bot-command-start",
  description: "/start command handler",
  method: "POST",
  path: "/api/bot/command/start",
  pattern: "command",
  runtime: "nodejs",
  dependencies: ["auth-middleware", "localization-service"],

  async handler(req, res) {
    const { userId, chatId } = req.body;
    const welcome = await t(userId, "commands.start.welcome");
    return res.json({ message: welcome });
  }
});
```

#### Step 5.2: Message Stream (Stream Step)
```typescript
// motia-bot-message-stream
export default defineStreamStep({
  name: "bot-message-stream",
  description: "Real-time message processing",
  pattern: "observer",
  runtime: "nodejs",
  dependencies: ["claude-service", "formatter-service"],

  async* stream(message) {
    const userId = message.from.id;
    const response = await claudeService.runCommand(message.text, userId);

    // Stream chunks as they arrive
    for (const chunk of response.chunks) {
      yield { type: "chunk", data: chunk };
    }

    yield { type: "complete", data: response };
  }
});
```

### Phase 6: Feature Services (Week 7)

#### Step 6.1: Image Processing (Event Step)
```typescript
// motia-image-processor
export default defineEventStep({
  name: "image-processor",
  description: "Async image processing pipeline",
  pattern: "pipeline",
  runtime: "nodejs",
  dependencies: ["claude-service"],

  events: {
    "image.uploaded": async (payload) => {
      const { imageData, userId } = payload;

      // Validate
      await imageProcessor.validate(imageData);

      // Optimize
      const optimized = await imageProcessor.optimize(imageData);

      // Process with Claude
      const result = await claudeService.processWithImage(userId, optimized);

      return result;
    },
  }
});
```

#### Step 6.2: Scheduled Prompts (Cron Steps)
```typescript
// motia-scheduled-prompts
export default defineCronStep({
  name: "daily-code-review",
  description: "Daily code review prompt",
  schedule: "0 2 * * *", // 2 AM daily
  timezone: "Europe/Kyiv",
  pattern: "observer",
  runtime: "nodejs",
  dependencies: ["claude-service", "auto-responder"],

  async handler() {
    const prompt = "Проаналізуй останні зміни в проекті";
    const result = await claudeService.runCommand(prompt, ADMIN_USER_ID);

    // Auto-respond to confirmations
    if (result.needsConfirmation) {
      await autoResponder.respond(result.confirmationType);
    }

    return result;
  }
});
```

#### Step 6.3: Availability Monitor (Cron Step)
```typescript
// motia-availability-monitor
export default defineCronStep({
  name: "claude-availability-check",
  description: "Monitor Claude CLI health",
  schedule: "*/1 * * * *", // Every minute
  pattern: "circuit-breaker",
  runtime: "nodejs",
  dependencies: ["config-service"],

  async handler() {
    const status = await claudeMonitor.checkAvailability();

    if (status.isAvailable) {
      await claudeMonitor.resetCircuitBreaker();
    } else {
      await claudeMonitor.recordFailure();

      if (claudeMonitor.shouldNotify()) {
        await claudeMonitor.notifyUsers(status);
      }
    }

    return status;
  }
});
```

### Phase 7: Utilities & Support Services (Week 8)

#### Step 7.1: Localization Service (Noop Step)
```typescript
// motia-localization-service
export default defineNoopStep({
  name: "localization-service",
  description: "Multi-language support",
  provides: {
    t: TranslateFunction,
    getLanguage: Function,
    setLanguage: Function,
  },
  runtime: "nodejs",
  dependencies: ["database-service"],
});
```

#### Step 7.2: Formatter Service (Noop Step)
```typescript
// motia-formatter-service
export default defineNoopStep({
  name: "formatter-service",
  description: "Response formatting utilities",
  provides: {
    formatResponse: Function,
    splitMessage: Function,
    formatCode: Function,
  },
  runtime: "nodejs",
});
```

---

## Data Flow Diagrams

### 1. User Message Processing Flow

```
┌─────────────┐
│   Telegram  │
│    Update   │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│   Auth Middleware│  ← Check user_id whitelist/token
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  Rate Limiter    │  ← Token bucket check
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│   Bot Router     │  ← Route to handler
└──────┬───────────┘
       │
       ├─→ /command → Command Handler
       ├─→ text → Message Handler → Claude Service
       ├─→ callback → Callback Handler
       └─→ image → Image Handler → Claude Vision
                                      │
                                      ↓
                              ┌───────────────┐
                              │ Claude CLI    │
                              │ Integration   │
                              └───────┬───────┘
                                      │
                                      ↓
                              ┌───────────────┐
                              │  Response     │
                              │  Formatter    │
                              └───────┬───────┘
                                      │
                                      ↓
                              ┌───────────────┐
                              │   Telegram    │
                              │    Reply      │
                              └───────────────┘
```

### 2. MCP Server Execution Flow

```
User: /mcpask "query"
       │
       ↓
┌──────────────────┐
│ MCP Context      │
│ Handler          │
└──────┬───────────┘
       │
       ├─→ Get Active Context
       │   (which server?)
       │
       ↓
┌──────────────────┐
│ MCP Manager      │
│ (check status)   │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Enhance Prompt   │
│ with Context     │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Claude CLI       │
│ with MCP Server  │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Log Usage        │
│ (analytics)      │
└──────┬───────────┘
       │
       ↓
   Response to User
```

### 3. Image Processing Flow

```
User uploads image
       │
       ↓
┌──────────────────┐
│ Telegram         │
│ File Download    │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Image Validator  │
│ - Size check     │
│ - Format check   │
│ - Dimensions     │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Image Optimizer  │
│ - Resize         │
│ - Compress       │
│ - Convert base64 │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Claude Vision    │
│ API Call         │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Response Parser  │
│ & Formatter      │
└──────┬───────────┘
       │
       ↓
   Reply to User
```

### 4. Scheduled Prompt Execution

```
Cron Trigger (2 AM)
       │
       ↓
┌──────────────────┐
│ Check Conditions │
│ - DND period?    │
│ - Claude avail?  │
│ - No activity?   │
└──────┬───────────┘
       │
       ↓ (all pass)
┌──────────────────┐
│ Load Prompt      │
│ Configuration    │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Execute with     │
│ Claude CLI       │
└──────┬───────────┘
       │
       ├─→ Confirmation needed?
       │   ↓
       │   Auto-Responder
       │   ↓
       └─→ Continue
       │
       ↓
┌──────────────────┐
│ Log Execution    │
│ Result           │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Optional: Notify │
│ Admin/Users      │
└──────────────────┘
```

---

## Dependencies Map

### External Dependencies

```yaml
Runtime:
  - python: "3.11+"
  - nodejs: "20+" (for MCP servers)

Core Libraries:
  - python-telegram-bot: ">=21.0" (Telegram API)
  - pydantic: ">=2.0" (config validation)
  - pydantic-settings: ">=2.0" (env vars)
  - structlog: "latest" (structured logging)
  - aiosqlite: "latest" (async SQLite)
  - asyncpg: "latest" (async PostgreSQL)

AI/ML:
  - anthropic: "latest" (Claude SDK - optional)

Image Processing:
  - Pillow: "latest" (image manipulation)

MCP Servers (Node.js):
  - @modelcontextprotocol/server-github
  - @modelcontextprotocol/server-filesystem
  - @modelcontextprotocol/server-postgres
  - @modelcontextprotocol/server-sqlite
  - @modelcontextprotocol/server-playwright
  - mcp-server-git (uvx)

Utilities:
  - PyYAML: "latest" (YAML parsing)
  - python-dotenv: "latest" (.env files)
  - aiofiles: "latest" (async file I/O)
```

### Internal Dependencies

```
Component Dependency Graph:

config-service
  └─→ No dependencies

database-service
  └─→ config-service

auth-middleware
  ├─→ config-service
  └─→ database-service

rate-limiter
  ├─→ config-service
  └─→ database-service

session-manager
  └─→ database-service

claude-service
  ├─→ config-service
  ├─→ session-manager
  └─→ database-service

mcp-manager
  ├─→ config-service
  ├─→ database-service
  └─→ claude-service

mcp-context-handler
  ├─→ mcp-manager
  └─→ claude-service

localization-service
  └─→ database-service

formatter-service
  └─→ localization-service

image-processor
  ├─→ config-service
  └─→ claude-service

bot-core
  ├─→ auth-middleware
  ├─→ rate-limiter
  ├─→ claude-service
  ├─→ mcp-context-handler
  ├─→ localization-service
  ├─→ formatter-service
  ├─→ image-processor
  └─→ database-service
```

---

## Error Handling Patterns

### 1. Exception Hierarchy

```python
ClaudeCodeTelegramError (Base)
  ├─→ ConfigurationError
  │   ├─→ MissingConfigError
  │   └─→ InvalidConfigError
  │
  ├─→ SecurityError
  │   ├─→ AuthenticationError
  │   ├─→ AuthorizationError
  │   └─→ DirectoryTraversalError
  │
  ├─→ ClaudeError
  │   ├─→ ClaudeTimeoutError
  │   ├─→ ClaudeProcessError
  │   ├─→ ClaudeParsingError
  │   └─→ ClaudeToolValidationError
  │
  ├─→ StorageError
  │   ├─→ DatabaseConnectionError
  │   └─→ DataIntegrityError
  │
  ├─→ TelegramError
  │   ├─→ MessageTooLongError
  │   ├─→ RateLimitError
  │   └─→ RateLimitExceeded
  │
  └─→ MCPError
      ├─→ MCPValidationError
      ├─→ MCPServerNotFoundError
      ├─→ MCPContextError
      ├─→ MCPConnectionError
      ├─→ MCPCommandError
      └─→ MCPConfigurationError
```

### 2. Error Recovery Strategies

```python
# Strategy 1: Retry with Exponential Backoff
async def execute_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except TransientError:
            await asyncio.sleep(2 ** attempt)
    raise MaxRetriesExceeded()

# Strategy 2: Circuit Breaker
class CircuitBreaker:
    states = ["CLOSED", "OPEN", "HALF_OPEN"]

    async def call(self, func):
        if self.state == "OPEN":
            if self.should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()

        try:
            result = await func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

# Strategy 3: Graceful Degradation
async def get_with_fallback(primary_func, fallback_func):
    try:
        return await primary_func()
    except PrimaryServiceError:
        logger.warning("Primary service failed, using fallback")
        return await fallback_func()
```

---

## Performance Considerations

### 1. Async/Await Architecture
- All I/O operations are async (database, HTTP, file)
- Connection pooling for database
- Concurrent request handling

### 2. Caching Strategy
```python
# Cache Layers:
1. In-Memory Cache (rate limit buckets)
   - TTL: Variable (based on refill rate)

2. Session Cache (user state)
   - TTL: 2 hours
   - Invalidation: On user action

3. MCP Server Status Cache
   - TTL: 5 minutes
   - Refresh: On status check

4. Translation Cache
   - TTL: Indefinite (only reload on update)
```

### 3. Rate Limiting
```python
Token Bucket Algorithm:
  - Capacity: 10 requests
  - Refill Rate: 5 requests / 60 seconds
  - Burst Capacity: 15 requests

Cost-Based Limiting:
  - Max Cost: $10.00 per user per day
  - Tracked at request level
  - Reset: Daily at midnight UTC
```

### 4. Database Optimization
```sql
-- Indexes:
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_session_id ON user_sessions(session_id);
CREATE INDEX idx_mcp_servers_user_id ON user_mcp_servers(user_id);
CREATE INDEX idx_mcp_usage_user_server ON mcp_usage_log(user_id, server_name);
CREATE INDEX idx_mcp_usage_created ON mcp_usage_log(created_at);

-- Connection Pooling:
min_connections: 2
max_connections: 10
connection_timeout: 30s
```

---

## Security Audit

### 1. Authentication Mechanisms
- **Whitelist**: User ID validation
- **Token-based**: JWT with expiry
- **Multi-factor**: Optional (future)

### 2. Authorization Checks
- Per-command authorization
- Directory traversal prevention
- Tool usage validation

### 3. Input Validation
```python
SecurityValidator:
  - validate_path(path, working_dir)
  - validate_command(command, allowed_commands)
  - validate_tool_call(tool, input, dir)
  - check_dangerous_patterns(text)
```

### 4. Secrets Management
```python
# SecretStr fields:
- telegram_bot_token
- anthropic_api_key
- auth_token_secret
- MCP server API keys (GitHub, etc.)

# Environment variables only, never logged
```

### 5. Audit Logging
```python
AuditLog:
  - user_id
  - action (command, API call, file operation)
  - timestamp
  - success/failure
  - error_details
  - ip_address (if available)
```

---

## Motia Step Type Mapping

### Summary Table

| Component | Lines | Current Pattern | Motia Step Type | Priority | Complexity |
|-----------|-------|-----------------|-----------------|----------|------------|
| **Config System** | 24,529 | Singleton | Noop | High | Low |
| **Database Layer** | 6,420 | Repository | Noop | High | Medium |
| **Authentication** | 5,000+ | Chain | API (Middleware) | High | Medium |
| **Rate Limiter** | 10,493 | Token Bucket | API (Middleware) | High | Low |
| **Claude Integration** | 65,000+ | Facade | API | Critical | High |
| **Session Manager** | 4,000+ | State | Noop | High | Medium |
| **MCP Manager** | 52,059 | Observer | Event | Critical | High |
| **MCP Context** | 12,431 | Strategy | Event | High | Medium |
| **Bot Handlers** | 45,000+ | Command | API | Critical | High |
| **Message Stream** | 1,488 | Observer | Stream | High | Medium |
| **Image Processor** | 5,000+ | Pipeline | Event | Medium | Medium |
| **DRACON System** | 116,000+ | Builder | Noop (Tool) | Low | Very High |
| **Scheduled Prompts** | 26,336 | Cron | Cron | High | Medium |
| **Auto-Responder** | 11,344 | Strategy | Noop | Medium | Low |
| **Availability Monitor** | 9,885 | Circuit Breaker | Cron | Medium | Low |
| **Localization** | 3,000+ | Strategy | Noop | Medium | Low |
| **Formatter** | 25,721 | Template | Noop | Medium | Medium |

### Detailed Recommendations by Category

#### Critical Path (MVP) - 4-6 weeks

1. **API Steps**
   - `/api/bot/command/*` - All bot commands
   - `/api/claude/execute` - Claude execution
   - `/api/claude/stream` - Streaming responses
   - `/api/mcp/server/*` - MCP management

2. **Event Steps**
   - `mcp-server-lifecycle` - Add/remove/enable/disable
   - `mcp-context-execution` - Query with context
   - `image-processing-pipeline` - Async image handling

3. **Cron Steps**
   - `claude-availability-monitor` - Every 1 minute
   - `scheduled-prompts-executor` - User-defined schedules

4. **Stream Steps**
   - `bot-message-stream` - Real-time responses
   - `claude-tool-usage-stream` - Live tool execution

5. **Noop Steps** (Services)
   - `config-service`
   - `database-service`
   - `session-manager`
   - `localization-service`
   - `formatter-service`

#### Phase 2 - Advanced Features (2-3 weeks)

6. **Additional Event Steps**
   - `git-integration` - Git operations
   - `file-handler` - File management
   - `task-scheduler` - Task queue

7. **Additional Cron Steps**
   - `session-cleanup` - Remove old sessions
   - `metrics-aggregation` - Daily stats

8. **Additional API Steps**
   - `/api/session/*` - Session management
   - `/api/tasks/*` - Task CRUD
   - `/api/stats/*` - Analytics

#### Phase 3 - Optional/Future (1-2 weeks)

9. **DRACON System** (External Tool)
   - Not part of core Motia steps
   - Could be standalone workflow designer
   - Integration via API if needed

10. **Advanced Features**
    - Multi-tenant support
    - Webhook integrations
    - Plugin system

---

## Migration Checklist

### Pre-Migration

- [ ] Backup current database
- [ ] Document all environment variables
- [ ] Export user data
- [ ] Test current system thoroughly
- [ ] Freeze feature development

### Migration Process

#### Week 1: Foundation
- [ ] Set up Motia project structure
- [ ] Create config-service Noop step
- [ ] Create database-service Noop step
- [ ] Migrate Settings and FeatureFlags
- [ ] Test configuration loading

#### Week 2: Security Layer
- [ ] Create auth-middleware API step
- [ ] Create rate-limiter API step
- [ ] Migrate AuthenticationManager
- [ ] Migrate RateLimiter
- [ ] Test authentication flow

#### Week 3: Core Services
- [ ] Create session-manager Noop step
- [ ] Create localization-service Noop step
- [ ] Create formatter-service Noop step
- [ ] Migrate session storage
- [ ] Test session persistence

#### Week 4: Claude Integration
- [ ] Create claude-service API step
- [ ] Migrate ClaudeIntegration facade
- [ ] Migrate ClaudeProcessManager
- [ ] Implement streaming response
- [ ] Test Claude execution

#### Week 5: MCP Integration
- [ ] Create mcp-manager Event step
- [ ] Create mcp-context-handler Event step
- [ ] Migrate MCP server configs
- [ ] Migrate context execution
- [ ] Test MCP operations

#### Week 6: Bot Handlers
- [ ] Create bot-command-* API steps
- [ ] Create bot-message-stream Stream step
- [ ] Create bot-callback-* Event steps
- [ ] Migrate all handlers
- [ ] Test end-to-end flow

#### Week 7: Features
- [ ] Create image-processor Event step
- [ ] Create scheduled-prompts-* Cron steps
- [ ] Create availability-monitor Cron step
- [ ] Migrate all features
- [ ] Test feature functionality

#### Week 8: Testing & Deployment
- [ ] Integration testing
- [ ] Performance testing
- [ ] Load testing
- [ ] User acceptance testing
- [ ] Production deployment

### Post-Migration

- [ ] Monitor system health
- [ ] Collect user feedback
- [ ] Performance tuning
- [ ] Documentation updates
- [ ] Training materials

---

## Conclusion

This **Claude Code Telegram Bot** is a sophisticated system with:
- **93 files** across 34,620 lines
- **10+ major subsystems**
- **Complex async architecture**
- **Rich feature set** (MCP, DRACON, image processing, scheduling)

### Migration Effort Estimate
- **Total Time**: 8-10 weeks (1 senior developer)
- **Critical Path**: 4-6 weeks
- **Risk Level**: Medium-High (due to complexity)

### Recommended Approach
1. **Incremental Migration**: Migrate subsystem by subsystem
2. **Parallel Running**: Run old and new systems side-by-side
3. **Feature Parity**: Ensure all features work before cutover
4. **Rollback Plan**: Keep old system available

### Key Benefits After Migration
- **Scalability**: Independent step deployment
- **Maintainability**: Clear separation of concerns
- **Monitoring**: Built-in Motia observability
- **Testing**: Easier unit/integration testing
- **Documentation**: Auto-generated from step definitions

---

**Next Steps**:
1. Review this analysis with stakeholders
2. Prioritize features for MVP
3. Create detailed technical specifications for each Motia step
4. Set up development environment
5. Begin Phase 1 migration

---

**Report Generated**: 2025-10-09
**Analyst**: Claude Code (Sonnet 4.5)
**Project**: Motia Framework Migration
**Status**: Ready for Implementation
