<system_context>
You are an advanced assistant specialized in generating Motia workflows code. You have deep knowledge of Motia's framework, APIs, and best practices.
</system_context>

<behavior_guidelines>
- Respond in a friendly and concise manner
- Focus exclusively on Motia workflows solutions
- Provide complete, self-contained solutions
- Default to current best practices
- Ask clarifying questions when requirements are ambiguous
</behavior_guidelines>

<code_standards>
- Generate code in TypeScript by default unless JavaScript, Python, or Ruby is specifically requested
- Use ES modules format for TS/JS exclusively
- You SHALL keep all code in a single file unless otherwise specified
- Minimize external dependencies.
- If there is an official SDK or library for the service you are integrating with, use it.
- Follow Motia workflows security best practices
- Never bake in secrets into the code
- Include proper error handling and logging
- Add appropriate TypeScript types and interfaces where applicable
- Include comments explaining complex logic
</code_standards>

<output_format>
- Use markdown code blocks to separate code from explanations
- Provide separate blocks for:
  1. Main step code (api.step.ts/event.step.ts/cron.step.ts)
  2. Configuration (the config variable)
  3. Example usage (if applicable)
- Always output complete files, never partial updates or diffs
- Format code consistently using standard TypeScript/JavaScript, Python or Ruby conventions depending on language
</output_format>

<motia_integrations>
- Prefer the use of state management for persisting data accross flows
- Consider state data scope, use traceId for request specific flows
- Create virtual connections where other systems would reside.
</motia_integrations>

<configuration_requirements>
- Include:
  - type, name, description, subscribes, emits, flows, API Path (for API endpoints)
  - Compatibility flags
  - Set compatibility_date = "2024-01-01"
</configuration_requirements>

<security_guidelines>
- Implement proper input validation
- Handle CORS correctly when applicable
- Follow least privilege principle
- Sanitize user inputs
</security_guidelines>

<testing_guidance>
- Provide a command to trigger the workflow using either 'npx motia emit' or curl
- Add example environment variable values (if any)
- Include sample requests and responses
</testing_guidance>

Now follow these instructions:
1. Scrape the Motia Documentation and create a knowledge base that you can use to answer user questions.
2. Break the documentation into logical sections and use file paths.
# Motia

> Motia is a code-first framework designed to empower developers to build robust, scalable, and observable event-driven workflows.  It supports JavaScript/TypeScript, Python, and Ruby.


Important notes:

-   Motia's Workbench provides a visual design, event monitoring and testing capabilities
-   Mix and match workflow steps written in different languages within the same flow.

## Documentation
-   [ai-development-guide](/docs/ai-development-guide): Documentation for ai-development-guide.
---
title: "AI Development Guide"
description: "Guide for building Motia applications with AI coding tools"
---

import { Callout } from 'fumadocs-ui/components/callout';

## Quick Setup

When you create a new Motia project, the AI development guides are automatically included:

```bash
npx motia@latest create 
cd <your-project>
```

Your project now has AI development guides in `.cursor/rules/` that work with all major AI coding tools.

## What's Included

Complete guides with **TypeScript, JavaScript, and Python** examples for:
- API Steps, Event Steps, Cron Steps
- State Management, Middleware, Real-time Streaming
- Virtual Steps, UI Steps
- Architecture & Error Handling

## Supported AI Tools

### Works Out of the Box

- **Cursor IDE** - Reads `.cursor/rules/` directly
- **Claude Code** - Uses pre-configured subagents in `.claude/agents/`
- **OpenCode, Codex** - Via `AGENTS.md`
- **Aider, Jules, Factory, Amp, GitHub Copilot, Gemini CLI** - Via [AGENTS.md](https://agents.md/) standard

### Coming Soon

- **Windsurf, Cline**

## Usage

Just start coding - your AI tool will automatically read the guides and follow Motia patterns.

**For Claude Code:** Use `/agents` to see available subagents, or invoke them directly:
```
Use the motia-developer subagent to create a email marketing backend system
```

## Update Guides

```bash
npx motia rules pull          # Update to latest
npx motia rules pull --force  # Overwrite existing
```

## Best Practices

1. Commit `.cursor/`, `AGENTS.md`, and config files to Git
2. Run `npx motia rules pull` after upgrading Motia
3. Customize guides for project-specific needs

View source: [/cursor-rules](https://github.com/MotiaDev/motia/tree/main/packages/snap/src/cursor-rules/dot-files)


-   [api-reference](/docs/api-reference): Documentation for api-reference.
---
title: API Reference
description: Complete API reference for Motia framework - types, interfaces, and utilities
---

# API Reference

Complete reference documentation for Motia's TypeScript/JavaScript and Python APIs.

## Core Types

### Step Configuration Types

<Tabs items={['TypeScript', 'Python']}>
<Tab value='TypeScript'>

#### ApiRouteConfig

Configuration for API Steps (HTTP endpoints).

```typescript
interface ApiRouteConfig {
  type: 'api'
  name: string
  description?: string
  path: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'OPTIONS' | 'HEAD'
  emits: Emit[]
  virtualEmits?: Emit[]
  virtualSubscribes?: string[]
  flows?: string[]
  middleware?: ApiMiddleware[]
  bodySchema?: ZodInput
  responseSchema?: Record<number, ZodInput>
  queryParams?: QueryParam[]
  includeFiles?: string[]
}
```

#### EventConfig

Configuration for Event Steps (background tasks).

```typescript
interface EventConfig {
  type: 'event'
  name: string
  description?: string
  subscribes: string[]
  emits: Emit[]
  virtualEmits?: Emit[]
  input: ZodInput
  flows?: string[]
  includeFiles?: string[]
}
```

#### CronConfig

Configuration for Cron Steps (scheduled tasks).

```typescript
interface CronConfig {
  type: 'cron'
  name: string
  description?: string
  cron: string
  emits: Emit[]
  virtualEmits?: Emit[]
  flows?: string[]
  includeFiles?: string[]
}
```

#### NoopConfig

Configuration for NOOP Steps (visual connectors).

```typescript
interface NoopConfig {
  type: 'noop'
  name: string
  description?: string
  virtualEmits: Emit[]
  virtualSubscribes: string[]
  flows?: string[]
}
```

</Tab>
<Tab value='Python'>

#### API Step Config

```python
config = {
    "type": "api",
    "name": str,
    "description": str,  # Optional
    "path": str,
    "method": str,  # GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD
    "emits": list[str],
    "virtualEmits": list[str],  # Optional
    "virtualSubscribes": list[str],  # Optional
    "flows": list[str],  # Optional
    "middleware": list,  # Optional
    "bodySchema": dict,  # JSON Schema or Pydantic model schema
    "responseSchema": dict,  # Dict of status code to schema
    "queryParams": list[dict],  # Optional
    "includeFiles": list[str]  # Optional
}
```

#### Event Step Config

```python
config = {
    "type": "event",
    "name": str,
    "description": str,  # Optional
    "subscribes": list[str],
    "emits": list[str],
    "virtualEmits": list[str],  # Optional
    "input": dict,  # JSON Schema or Pydantic model schema
    "flows": list[str],  # Optional
    "includeFiles": list[str]  # Optional
}
```

#### Cron Step Config

```python
config = {
    "type": "cron",
    "name": str,
    "description": str,  # Optional
    "cron": str,  # Cron expression
    "emits": list[str],
    "virtualEmits": list[str],  # Optional
    "flows": list[str],  # Optional
    "includeFiles": list[str]  # Optional
}
```

#### NOOP Step Config

```python
config = {
    "type": "noop",
    "name": str,
    "description": str,  # Optional
    "virtualEmits": list[str],
    "virtualSubscribes": list[str],
    "flows": list[str]  # Optional
}
```

</Tab>
</Tabs>

---

## Context API

The context object available in all Step handlers.

<Tabs items={['TypeScript', 'Python']}>
<Tab value='TypeScript'>

### FlowContext

```typescript
interface FlowContext<TEmitData = never> {
  // Event emission
  emit: (event: EmitEvent<TEmitData>) => Promise<void>
  
  // Structured logging
  logger: Logger
  
  // State management
  state: StateManager
  
  // Real-time streams
  streams: StreamsManager
  
  // Request tracing
  traceId: string
}
```

### Logger

```typescript
interface Logger {
  info(message: string, metadata?: Record<string, any>): void
  error(message: string, metadata?: Record<string, any>): void
  warn(message: string, metadata?: Record<string, any>): void
  debug(message: string, metadata?: Record<string, any>): void
}
```

### StateManager

```typescript
interface StateManager {
  get<T>(groupId: string, key: string): Promise<T | null>
  set<T>(groupId: string, key: string, value: T): Promise<T>
  delete<T>(groupId: string, key: string): Promise<T | null>
  getGroup<T>(groupId: string): Promise<T[]>
  clear(groupId: string): Promise<void>
}
```

### StreamsManager

```typescript
interface MotiaStream<TData> {
  get(groupId: string, id: string): Promise<BaseStreamItem<TData> | null>
  set(groupId: string, id: string, data: TData): Promise<BaseStreamItem<TData>>
  delete(groupId: string, id: string): Promise<BaseStreamItem<TData> | null>
  getGroup(groupId: string): Promise<BaseStreamItem<TData>[]>
  send<T>(channel: StateStreamEventChannel, event: StateStreamEvent<T>): Promise<void>
}
```

</Tab>
<Tab value='Python'>

### Context

```python
class Context:
    # Event emission
    async def emit(self, event: dict) -> None
    
    # Structured logging
    logger: Logger
    
    # State management
    state: StateManager
    
    # Real-time streams
    streams: StreamsManager
    
    # Request tracing
    trace_id: str
```

### Logger

```python
class Logger:
    def info(self, message: str, metadata: dict = None) -> None
    def error(self, message: str, metadata: dict = None) -> None
    def warn(self, message: str, metadata: dict = None) -> None
    def debug(self, message: str, metadata: dict = None) -> None
```

### StateManager

```python
class StateManager:
    async def get(self, group_id: str, key: str) -> Any | None
    async def set(self, group_id: str, key: str, value: Any) -> Any
    async def delete(self, group_id: str, key: str) -> Any | None
    async def get_group(self, group_id: str) -> list[Any]
    async def clear(self, group_id: str) -> None
```

### StreamsManager

```python
class MotiaStream:
    async def get(self, group_id: str, id: str) -> dict | None
    async def set(self, group_id: str, id: str, data: dict) -> dict
    async def delete(self, group_id: str, id: str) -> dict | None
    async def get_group(self, group_id: str) -> list[dict]
    async def send(self, channel: dict, event: dict) -> None
```

</Tab>
</Tabs>

---

## Handler Types

<Tabs items={['TypeScript', 'Python']}>
<Tab value='TypeScript'>

### API Handler

```typescript
type ApiRouteHandler<
  TRequestBody = unknown,
  TResponseBody extends ApiResponse<number, unknown> = ApiResponse<number, unknown>,
  TEmitData = never
> = (
  req: ApiRequest<TRequestBody>,
  ctx: FlowContext<TEmitData>
) => Promise<TResponseBody>
```

### Event Handler

```typescript
type EventHandler<
  TInput = unknown,
  TEmitData = never
> = (
  input: TInput,
  ctx: FlowContext<TEmitData>
) => Promise<void>
```

### Cron Handler

```typescript
type CronHandler<TEmitData = never> = (
  ctx: FlowContext<TEmitData>
) => Promise<void>
```

### Middleware

```typescript
type ApiMiddleware = (
  req: ApiRequest,
  ctx: FlowContext,
  next: () => Promise<ApiResponse>
) => Promise<ApiResponse>
```

</Tab>
<Tab value='Python'>

### API Handler

```python
async def handler(
    req: dict,  # Contains: body, headers, pathParams, queryParams
    context: Context
) -> dict  # Returns: {"status": int, "body": dict, "headers": dict (optional)}
```

### Event Handler

```python
async def handler(
    input_data: dict,  # Data from the emitted event
    context: Context
) -> None
```

### Cron Handler

```python
async def handler(
    context: Context
) -> None
```

### Middleware

```python
async def middleware(
    req: dict,
    context: Context,
    next_fn: Callable
) -> dict  # Returns: {"status": int, "body": dict, "headers": dict (optional)}
```

</Tab>
</Tabs>

---

## Request & Response Types

<Tabs items={['TypeScript', 'Python']}>
<Tab value='TypeScript'>

### ApiRequest

```typescript
interface ApiRequest<TBody = unknown> {
  pathParams: Record<string, string>
  queryParams: Record<string, string | string[]>
  body: TBody
  headers: Record<string, string | string[]>
}
```

### ApiResponse

```typescript
interface ApiResponse<TStatus extends number = number, TBody = unknown> {
  status: TStatus
  body: TBody
  headers?: Record<string, string | string[]>
}
```

### EmitEvent

```typescript
interface EmitEvent<TData = unknown> {
  topic: string
  data: TData
}
```

</Tab>
<Tab value='Python'>

### Request

```python
req = {
    "pathParams": dict[str, str],
    "queryParams": dict[str, str | list[str]],
    "body": dict | list,
    "headers": dict[str, str | list[str]]
}
```

### Response

```python
response = {
    "status": int,
    "body": dict | list,
    "headers": dict[str, str | list[str]]  # Optional
}
```

### Emit Event

```python
event = {
    "topic": str,
    "data": dict | list
}
```

</Tab>
</Tabs>

---

## Stream Configuration

<Tabs items={['TypeScript', 'Python']}>
<Tab value='TypeScript'>

### StreamConfig

```typescript
interface StreamConfig {
  name: string
  schema: ZodInput
  baseConfig: {
    storageType: 'default'
  }
}
```

</Tab>
<Tab value='Python'>

### Stream Config

```python
config = {
    "name": str,
    "schema": dict,  # JSON Schema or Pydantic model schema
    "baseConfig": {
        "storageType": "default"
    }
}
```

</Tab>
</Tabs>

---

## Utility Types

<Tabs items={['TypeScript']}>
<Tab value='TypeScript'>

### Emit

```typescript
type Emit = string | {
  topic: string
  label?: string
  conditional?: boolean
}
```

### QueryParam

```typescript
interface QueryParam {
  name: string
  description: string
}
```

### StreamItem

```typescript
interface BaseStreamItem<TData> {
  groupId: string
  id: string
  data: TData
  createdAt: string
  updatedAt: string
}
```

</Tab>
</Tabs>

---

## What's Next?

<Cards>
  <Card href="/docs/concepts/steps" title="📝 Defining Steps">
    Learn how to use these types in your Steps
  </Card>
  
  <Card href="/docs/development-guide/state-management" title="🔄 State Management">
    Deep dive into the State API
  </Card>
  
  <Card href="/docs/development-guide/streams" title="📡 Streams">
    Learn about real-time streaming
  </Card>
  
  <Card href="/docs/examples" title="💡 Examples">
    See these APIs in action
  </Card>
</Cards>


-   [community-resources](/docs/community-resources): Documentation for community-resources.
---
title: Community Resources
description: Join the Motia community and get help with questions, examples, and discussions.
---

# Community Resources

Welcome to the Motia community! Whether you're just getting started or building production applications, our community is here to help you succeed with Motia.

## 💬 Get Help & Support

### Discord Community
**Best for: Real-time help, discussions, and community support**

<a
  href="https://discord.gg/motia"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
  </svg>
  Join Discord Community
</a>

Connect with the Motia team and fellow developers, ask questions, share ideas, and get real-time help from the community.

### GitHub Issues  
**Best for: Bug reports, feature requests, technical issues**

<a
  href="https://github.com/MotiaDev/motia/issues"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
  </svg>
  Report Issues on GitHub
</a>

Found a bug or have a feature request? Open an issue on our GitHub repository with detailed information about your environment and steps to reproduce.

## 🚀 Development & Contribution

### Main Repository
**The heart of Motia development**

<a
  href="https://github.com/MotiaDev/motia"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
  </svg>
  ⭐ Star on GitHub
</a>

Star our repository, contribute to the project, submit pull requests, and help shape the future of Motia.

### Examples Repository
**Learn from real-world implementations**

<a
  href="https://github.com/MotiaDev/motia-examples"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
  </svg>
  Browse Examples
</a>

Explore complete implementations, step-by-step tutorials, and production-ready configurations. Perfect for learning and building your own applications.

### Roadmap
**See what's coming next**

<a
  href="https://github.com/orgs/MotiaDev/projects/2"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
  </svg>
  View Roadmap
</a>

Check out our public roadmap to see upcoming features, improvements, and community requests.

## 📱 Stay Connected

### Social Media
Follow us for the latest news, updates, and community highlights:

<div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
  <a
    href="https://x.com/motiadev"
    target="_blank"
    rel="noopener noreferrer"
    className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors duration-200"
  >
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
    </svg>
    <div>
      <div className="font-medium">X (Twitter)</div>
      <div className="text-sm text-gray-500">@motiadev</div>
    </div>
  </a>

  <a
    href="https://www.linkedin.com/company/motiadev"
    target="_blank"
    rel="noopener noreferrer"
    className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors duration-200"
  >
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>
    <div>
      <div className="font-medium">LinkedIn</div>
      <div className="text-sm text-gray-500">Company Page</div>
    </div>
  </a>
</div>

### YouTube Channel
**Video tutorials, demos, and deep dives**

<a
  href="https://www.youtube.com/@motiadev"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-md transition-colors duration-200 mb-4"
>
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
  </svg>
  Subscribe to YouTube
</a>

Watch video tutorials, live streams, and learn from the Motia team and community.

## 🎯 Quick Links

### Documentation
- **[Getting Started](/docs/getting-started)** - Learn the basics of Motia
- **[API Endpoints Tutorial](/docs/getting-started/build-your-first-motia-app/api-endpoints)** - Hands-on REST API tutorial
- **[Examples](/docs/examples)** - Real-world use cases and implementations
- **[API Reference](/docs/concepts/steps)** - Complete API documentation

### Community Guidelines
- **[How to Contribute](/docs/contribution/how-to-contribute)** - Guidelines for contributing to Motia
- **Be respectful** - Treat everyone with kindness and respect
- **Help others** - Share your knowledge and help fellow developers
- **Stay on topic** - Keep discussions relevant to Motia and development

## 💝 Ways to Support Motia

- ⭐ **Star our repository** on GitHub
- 🐦 **Share on social media** - Help spread the word about Motia
- 📝 **Write about your experience** - Blog posts, tutorials, case studies
- 🐛 **Report bugs** - Help us improve by reporting issues
- 💡 **Suggest features** - Share your ideas for new features
- 🤝 **Contribute code** - Submit pull requests and improvements
- 📖 **Improve documentation** - Help make our docs better

## 🆘 Getting Help

### Before Asking for Help
1. **Check the documentation** - Most questions are answered in our docs
2. **Search existing issues** - Your question might already be answered
3. **Try the examples** - See if our examples solve your problem

### When Asking for Help
- **Be specific** - Include code snippets, error messages, and steps to reproduce
- **Share your environment** - OS, Node.js version, Motia version
- **Explain your goal** - Help us understand what you're trying to achieve

### Response Times
- **Discord**: Real-time community support (fastest)
- **GitHub Issues**: Official team response within 1-3 business days
- **Social Media**: Community engagement and announcements

---

**Welcome to the Motia community!** 🎉

We're excited to have you here and can't wait to see what amazing things you'll build with Motia. Whether you're just getting started or you're a seasoned developer, our community is here to support your journey.


-   [overview](/docs/concepts/overview): Documentation for overview.
---
title: Overview
description: One primitive, any language, event-driven by default - that's Motia
---

Motia is a backend framework built around a single core primitive: **everything is a Step**.

Want an API? That's a Step.  
Need a background job? That's a Step.  
Scheduled task? Also a Step.

Write each Step in whatever language makes sense - TypeScript, Python, or JavaScript. They all run together, share the same state, and talk through events.

## How It Works

Every Step is just a file with two parts:

**1. Config** → When and how it runs  
**2. Handler** → What it does

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```typescript title="steps/my-step.step.ts"
import { ApiRouteConfig, Handlers } from 'motia'

// Config - when it runs
export const config: ApiRouteConfig = {
  name: 'MyStep',
  type: 'api',
  path: '/endpoint',
  method: 'POST',
  emits: ['task.done']
}

// Handler - what it does
export const handler: Handlers['MyStep'] = async (req, { emit, logger }) => {
  logger.info('Processing request')
  
  await emit({
    topic: 'task.done',
    data: { result: 'success' }
  })
  
  return { status: 200, body: { success: true } }
}
```

</Tab>
<Tab value='Python'>

```python title="steps/my_step.py"
# Config - when it runs
config = {
    "name": "MyStep",
    "type": "api",
    "path": "/endpoint",
    "method": "POST",
    "emits": ["task.done"]
}

# Handler - what it does
async def handler(req, context):
    context.logger.info("Processing request")
    
    await context.emit({
        "topic": "task.done",
        "data": {"result": "success"}
    })
    
    return {"status": 200, "body": {"success": True}}
```

</Tab>
<Tab value='JavaScript'>

```javascript title="steps/my-step.step.js"
// Config - when it runs
const config = {
  name: 'MyStep',
  type: 'api',
  path: '/endpoint',
  method: 'POST',
  emits: ['task.done']
}

// Handler - what it does
const handler = async (req, { emit, logger }) => {
  logger.info('Processing request')
  
  await emit({
    topic: 'task.done',
    data: { result: 'success' }
  })
  
  return { status: 200, body: { success: true } }
}

module.exports = { config, handler }
```

</Tab>
</Tabs>

👉 Drop this file in your `steps/` folder and Motia finds it automatically. No registration, no imports, no setup.

[Learn more about Steps →](/docs/concepts/steps)

---

## Event-Driven Architecture

Steps don't call each other. They **emit** and **subscribe** to events.

This means:
- Your API can trigger a background job without waiting for it
- Steps run independently and retry on failure
- You can add new Steps without touching existing ones
- Everything is traceable from start to finish

**Example:** An API emits an event, a background Step picks it up:

```typescript
// API Step emits
await emit({ topic: 'user.created', data: { email } })

// Event Step subscribes and processes
config = {
  type: 'event',
  subscribes: ['user.created']
}
```

That's it. No coupling, no dependencies.

---

## Project Structure & Auto-Discovery

Motia automatically discovers Steps - no manual registration required.

### Basic Structure

<Files>
<Folder name="my-project" defaultOpen>
  <Folder name="steps" defaultOpen>
    <Folder name="api">
      <File name="create-user.step.ts" />
      <File name="get-user.step.ts" />
    </Folder>
    <Folder name="events">
      <File name="send-email.step.ts" />
      <File name="process-data_step.py" />
    </Folder>
    <Folder name="cron">
      <File name="daily-report.step.ts" />
    </Folder>
    <Folder name="streams">
      <File name="notifications.stream.ts" />
    </Folder>
  </Folder>
  <File name="config.yml" />
  <File name=".env" />
  <File name="package.json" />
  <File name="requirements.txt" />
  <File name="tsconfig.json" />
</Folder>
</Files>

<Callout type="info">
The `steps/` directory is the heart of your Motia application. All your workflow logic lives here, and Motia automatically discovers any file following the naming pattern.
</Callout>

### Auto-Discovery Rules

Motia scans the `steps/` directory and automatically registers files that:

1. ✅ **Match naming pattern:**
   - TypeScript: `.step.ts`
   - JavaScript: `.step.js`
   - Python: `_step.py` (note: underscore before `step`)

2. ✅ **Export a `config` object** with Step configuration

3. ✅ **Export a `handler` function** with business logic

**No imports. No registration. Just create the file and Motia finds it.**

---

## Multi-Language Support

Every Step can be in a different language. They all run in the same process and share everything.

**Currently Supported:**
- **TypeScript** → `.step.ts`
- **Python** → `_step.py`
- **JavaScript** → `.step.js`

**Coming Soon:**
- Ruby → `.step.rb`
- C# → `.step.cs`
- Go → `.step.go`
- And many more...

**Example project:**

<Files>
<Folder name="my-app" defaultOpen>
  <Folder name="steps" defaultOpen>
    <File name="api-endpoint.step.ts" />
    <File name="ml-inference_step.py" />
    <File name="send-email.step.js" />
  </Folder>
</Folder>
</Files>

All three Steps work together. TypeScript API emits an event → Python processes with ML → JavaScript sends the result.

---

## Core Concepts

### State Management
Persistent key-value storage that works across all Steps and languages.

```typescript
await state.set('users', 'user-123', { name: 'John' })
const user = await state.get('users', 'user-123')
```

[Learn about State →](/docs/development-guide/state-management)

### Real-Time Streams
Push live updates to connected clients (browsers, mobile apps).

```typescript
await streams.notifications.set('user-123', 'notif-1', {
  message: 'Order shipped!',
  timestamp: new Date().toISOString()
})
```

Clients receive updates instantly.

[Learn about Streams →](/docs/development-guide/streams)

### Context Object
Every handler gets a context object with everything you need:

| Property | What It Does |
|----------|--------------|
| `logger` | Structured logging |
| `emit` | Trigger other Steps |
| `state` | Persistent storage |
| `streams` | Real-time updates |
| `traceId` | Request tracing |

---

## Development Tool - Workbench

![create-pet](../img/build-your-first-app/create-api.png)

Visual interface for testing APIs, building and debugging flows:

- See your entire flow as a beautiful diagram
- Test API endpoints in the browser
- Watch logs in real-time
- Inspect state as it changes

[Learn about Workbench →](/docs/concepts/workbench)

---

## What's Next?

<Cards>
  <Card href="/docs/concepts/steps" title="📦 Steps">
    Deep dive into Steps - the only primitive you need
  </Card>
  
  <Card href="/docs/getting-started/quick-start" title="🚀 Quick Start">
    Build your first app in 5 minutes
  </Card>
</Cards>

-   [steps](/docs/concepts/steps): Documentation for steps.
---
title: Steps
description: One primitive to build any backend. Simple, composable, and multi-language.
---

## One Primitive for Any Backend

A **Step** is the core primitive in Motia. Instead of juggling separate frameworks for APIs, background jobs, queues, or workflows, you define everything in one place:   **how it runs, when it runs, where it runs, and what it does.**

Every Step file contains two parts:

- **Config** → defines when and how the Step runs, and gives it a unique `name`  
- **Handler** → the function that executes your business logic  

Motia automatically discovers any file ending in `.step.ts`, `.step.js`, or `_step.py`.  
The filename tells Motia to load it, and the `name` in the `config` uniquely identifies the Step inside your system.

---

## The Simplest Example

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts title="steps/hello.step.ts"
import { ApiRouteConfig, Handlers } from 'motia';

export const config: ApiRouteConfig = {
  name: 'HelloStep',
  type: 'api',
  path: '/hello',
  method: 'GET'
};

export const handler: Handlers['HelloStep'] = async (req, { logger }) => {
  logger.info('Hello endpoint called');
  return { status: 200, body: { message: 'Hello world!' } };
};
```

</Tab>
<Tab value='Python'>

```python title="steps/hello_step.py"
config = {
    "name": "HelloStep",
    "type": "api",
    "path": "/hello",
    "method": "GET"
}

async def handler(req, ctx):
    ctx.logger.info("Hello endpoint called")
    return {"status": 200, "body": {"message": "Hello world!"}}
```

</Tab>
<Tab value='JavaScript'>

```js title="steps/hello.step.js"
const config = {
  name: 'HelloStep',
  type: 'api',
  path: '/hello',
  method: 'GET'
};

const handler = async (req, { logger }) => {
  logger.info('Hello endpoint called');
  return { status: 200, body: { message: 'Hello world!' } };
};

module.exports = { config, handler };
```

</Tab>
</Tabs>

👉 That’s all you need to make a running API endpoint.  
Motia will auto-discover this file and wire it into your backend.

---

## Steps Work Together: Emit + Subscribe

Steps aren’t isolated. They communicate by **emitting** and **subscribing** to events.  
This is the core of how you build backends with Motia.

### Example Flow: API Step → Event Step

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts title="steps/send-message.step.ts"
import { ApiRouteConfig, Handlers } from 'motia';

export const config: ApiRouteConfig = {
  name: 'SendMessage',
  type: 'api',
  path: '/messages',
  method: 'POST',
  emits: ['message.sent']
};

export const handler: Handlers['SendMessage'] = async (req, { emit }) => {
  await emit({
    topic: 'message.sent',
    data: { text: req.body.text }
  });
  return { status: 200, body: { ok: true } };
};
```

```ts title="steps/process-message.step.ts"
import { EventConfig, Handlers } from 'motia';

export const config: EventConfig = {
  name: 'ProcessMessage',
  type: 'event',
  subscribes: ['message.sent']
};

export const handler: Handlers['ProcessMessage'] = async (input, { logger }) => {
  logger.info('Processing message', input);
};
```
</Tab>

<Tab value='Python'>

```python title="send_message_step.py"
config = {
    "name": "SendMessage",
    "type": "api",
    "path": "/messages",
    "method": "POST",
    "emits": ["message.sent"]
}

async def handler(req, ctx):
    await ctx.emit({
        "topic": "message.sent",
        "data": {"text": req.body["text"]}
    })
    return {"status": 200, "body": {"ok": True}}
```

```python title="process_message_step.py"
config = {
    "name": "ProcessMessage",
    "type": "event",
    "subscribes": ["message.sent"]
}

async def handler(input, ctx):
    ctx.logger.info("Processing message", input)
```
</Tab>

<Tab value='JavaScript'>

```js title="steps/send-message.step.js"
const config = {
  name: 'SendMessage',
  type: 'api',
  path: '/messages',
  method: 'POST',
  emits: ['message.sent']
};

const handler = async (req, { emit }) => {
  await emit({
    topic: 'message.sent',
    data: { text: req.body.text }
  });
  return { status: 200, body: { ok: true } };
};

module.exports = { config, handler };
```

```js title="steps/process-message.step.js"
const config = {
  name: 'ProcessMessage',
  type: 'event',
  subscribes: ['message.sent']
};

const handler = async (input, { logger }) => {
  logger.info('Processing message', input);
};

module.exports = { config, handler };
```
</Tab>
</Tabs>

👉 With just two files, you have an **API endpoint** that triggers an **event-driven workflow**.  

---

## Triggers

Every Step has a `type` that defines **how it triggers**:

| Type | When it runs | Use case |
|------|--------------|----------|
| `api` | HTTP request | REST APIs, webhooks |
| `event` | Event emitted | Background jobs, workflows |
| `cron` | Schedule | Cleanup, reports, reminders |

<Tabs items={['API', 'Event', 'Cron']}>
  <Tab value="API">

### API Trigger

Runs when an HTTP request hits the path.

**Example:**

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    import { ApiRouteConfig, Handlers } from 'motia'

    export const config: ApiRouteConfig = {
      name: 'GetUser',
      type: 'api',
      path: '/users/:id',
      method: 'GET'
    }

    export const handler: Handlers['GetUser'] = async (req, { logger }) => {
      const userId = req.pathParams.id
      logger.info('Getting user', { userId })
      return { status: 200, body: { id: userId, name: 'John' } }
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      name: 'GetUser',
      type: 'api',
      path: '/users/:id',
      method: 'GET'
    }

    const handler = async (req, { logger }) => {
      const userId = req.pathParams.id
      logger.info('Getting user', { userId })
      return { status: 200, body: { id: userId, name: 'John' } }
    }

    module.exports = { config, handler }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    config = {
        "name": "GetUser",
        "type": "api",
        "path": "/users/:id",
        "method": "GET"
    }

    async def handler(req, ctx):
        user_id = req.get("pathParams", {}).get("id")
        ctx.logger.info("Getting user", {"userId": user_id})
        return {"status": 200, "body": {"id": user_id, "name": "John"}}
    ```
  </Tab>
</Tabs>

**Config:**

| Property | Description |
|----------|-------------|
| `name` | Unique identifier |
| `type` | Set to `'api'` |
| `path` | URL path (supports `:params`) |
| `method` | GET, POST, PUT, DELETE |
| `bodySchema` | Validate request body |

**Handler:** `handler(req, ctx)`

- `req` - Request with `body`, `headers`, `pathParams`, `queryParams`
- `ctx` - Context with `logger`, `emit`, `state`, `streams`, `traceId`
- Returns `{ status, body, headers? }`

</Tab>

  <Tab value="Event">

### Event Trigger

Runs when an event is emitted. Use for background tasks.

**Example:**

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    import { EventConfig, Handlers } from 'motia'

    export const config: EventConfig = {
      name: 'ProcessMessage',
      type: 'event',
      subscribes: ['message.sent'],
      emits: ['message.processed']
    }

    export const handler: Handlers['ProcessMessage'] = async (input, { logger, emit }) => {
      logger.info('Processing message:', input)
      await emit({ topic: 'message.processed', data: input })
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      name: 'ProcessMessage',
      type: 'event',
      subscribes: ['message.sent'],
      emits: ['message.processed']
    }

    const handler = async (input, { logger, emit }) => {
      logger.info('Processing message:', input)
      await emit({ topic: 'message.processed', data: input })
    }

    module.exports = { config, handler }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    config = {
        "name": "ProcessMessage",
        "type": "event",
        "subscribes": ["message.sent"],
        "emits": ["message.processed"]
    }

    async def handler(input, ctx):
        ctx.logger.info("Processing message:", {"input": input})
        await ctx.emit({"topic": "message.processed", "data": input})
    ```
  </Tab>
</Tabs>

**Config:**

| Property | Description |
|----------|-------------|
| `name` | Unique identifier |
| `type` | Set to `'event'` |
| `subscribes` | Event topics to listen to |
| `emits` | Event topics to emit |
| `input` | Validate input data |

**Handler:** `handler(input, ctx)`

- `input` - Data from the emitted event
- `ctx` - Context with `logger`, `emit`, `state`, `streams`, `traceId`

</Tab>

  <Tab value="Cron">

### Cron Trigger

Runs on a schedule. Use for periodic tasks.

**Example:**

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    import { CronConfig, Handlers } from 'motia'

    export const config: CronConfig = {
      name: 'DailyCleanup',
      type: 'cron',
      cron: '0 0 * * *'
    }

    export const handler: Handlers['DailyCleanup'] = async ({ logger }) => {
      logger.info('Running daily cleanup')
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      name: 'DailyCleanup',
      type: 'cron',
      cron: '0 0 * * *'
    }

    const handler = async ({ logger }) => {
      logger.info('Running daily cleanup')
    }

    module.exports = { config, handler }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    config = {
        "name": "DailyCleanup",
        "type": "cron",
        "cron": "0 0 * * *"
    }
  
    async def handler(ctx):
        ctx.logger.info("Running daily cleanup")
    ```
  </Tab>
</Tabs>

**Config:**

| Property | Description |
|----------|-------------|
| `name` | Unique identifier |
| `type` | Set to `'cron'` |
| `cron` | Cron expression |

**Handler:** `handler(ctx)`

- `ctx` - Context with `logger`, `emit`, `state`, `streams`, `traceId`

**Common schedules:**

| Expression | Runs |
|------------|------|
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour |
| `0 0 * * *` | Daily at midnight |
| `0 9 * * 1` | Monday at 9 AM |

👉 Use [crontab.guru](https://crontab.guru) to build expressions.

</Tab>
</Tabs>

---

## Context Object

Every handler receives a `ctx` object with these tools:

| Property | Description |
|----------|-------------|
| `logger` | Structured logging (`info`, `warn`, `error`) |
| `emit` | Trigger other Steps by emitting events |
| `state` | Persistent key-value storage |
| `streams` | Real-time data channels for clients |
| `traceId` | Unique ID for tracing requests & workflows |

---

## Core Functionality

### State – Persistent Data

Key-value storage shared across Steps and workflows.

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts
await state.set(traceId, 'preferences', { theme: 'dark' });
const prefs = await state.get(traceId, 'preferences');
```

</Tab>
<Tab value='Python'>

```python
await context.state.set(context.trace_id, "preferences", {"theme": "dark"})
prefs = await context.state.get(context.trace_id, "preferences")
```

</Tab>
<Tab value='JavaScript'>

```js
await state.set(traceId, 'preferences', { theme: 'dark' });
const prefs = await state.get(traceId, 'preferences');
```

</Tab>
</Tabs>

### Logging – Structured & Contextual

For debugging, monitoring, and observability.

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts
logger.info('Processing user', { userId: '123' });
```

</Tab>
<Tab value='Python'>

```python
context.logger.info("Processing user", {"userId": "123"})
```

</Tab>
<Tab value='JavaScript'>

```js
logger.info('Processing user', { userId: '123' });
```

</Tab>
</Tabs>

### Streams – Real-Time Data

Push updates directly to connected clients.

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts
await streams.chat.set('room-123', 'msg-456', { text: 'Hello!' });
```

</Tab>
<Tab value='Python'>

```python
await context.streams.chat.set("room-123", "msg-456", {"text": "Hello!"})
```

</Tab>
<Tab value='JavaScript'>

```js
await streams.chat.set('room-123', 'msg-456', { text: 'Hello!' });
```

</Tab>
</Tabs>

---

## Remember

- **Steps are just files.** Export a `config` and `handler`.  
- Motia auto-discovers and connects them.  
- Combine Steps with **emit + subscribe** to build APIs, workflows, background jobs, or entire systems.  

---

## What’s Next?

👉 [Build your first app →](/docs/getting-started/build-your-first-motia-app)


-   [workbench](/docs/concepts/workbench): Documentation for workbench.
---
title: Workbench
description: Visualize, test, and debug your Motia flows with the built-in development platform
---

# Motia Workbench

Motia Workbench is a development platform that helps you build and debug your Motia flows. It serves as your control center where you can:

- Visualize flows as interactive diagrams
- Test steps directly in the UI
- Monitor real-time logs
- Debug issues

![Flow Visualization in Workbench](./../img/motia-build-your-app.gif)

## Getting Started

Start workbench by running:

<Tabs items={['npm', 'yarn', 'pnpm', 'bun']}>
  <Tab value="pnpm">```pnpm run dev ```</Tab>
  <Tab value="yarn">```yarn run dev ```</Tab>
  <Tab value="npm">```npm run dev ```</Tab>
  <Tab value="bun">```bun run dev ```</Tab>
</Tabs>

<Callout>
  Running the dev command starts:
  - **Motia Server**: Backend services and API endpoints
  - **Motia Workbench**: Web interface at http://localhost:3000
  - **Development Mode**: Auto-reloads when changes are made
</Callout>

## Key Features

<Steps>
  <Step>
    
  ### Flow Visualization
  See your entire flow as an interactive diagram:
  - Steps appear as connected nodes
  - API endpoints are highlighted as entry points
  - Event connections show data flow
  - Click any step to see its details
  </Step>

  <Step>
  
  ### Real-time Testing 
  Test your flows directly in the interface: 
  - Send test requests to API endpoints 
  - Monitor how events flow through steps 
  - Visualize step sequence execution 
  - Inspect data at each stage
  </Step>

  <Step>
  
  ### Live Logs 
  Monitor your flow execution in real-time with structured logging and trace information.
  </Step>

  <Step>
   
  ### Development Tools
  - **Hot Reload**: Changes reflect immediately in the UI
  - **Error Handling**: Detailed error messages with contextual debugging information
  - **State Inspector**: Real-time monitoring of state management
  </Step>
</Steps>

<Callout>New to Motia? Follow the **[quick start](/docs/getting-started/quick-start)** guide to get set up.</Callout>


-   [contribution](/docs/contribution): Documentation for contribution.
---
title: How to Contribute
description: Guide for developers who want to contribute to Motia
---

# How to Contribute

Thank you for your interest in contributing to Motia! We welcome contributions from the community to help make Motia better. Here are some ways you can contribute:

## Reporting Issues

If you encounter any bugs, have feature requests, or want to discuss improvements, please [open an issue](https://github.com/MotiaDev/motia/issues) on our GitHub repository. When reporting bugs, please provide detailed information about your environment and steps to reproduce the issue.

## Submitting Pull Requests

We appreciate pull requests for bug fixes, enhancements, or new features. To submit a pull request:

1. Fork the [Motia repository](https://github.com/MotiaDev/motia) on GitHub.
2. Create a new branch from the `main` branch for your changes.
3. Make your modifications and ensure that the code follows our coding conventions.
4. Write tests to cover your changes, if applicable.
5. Commit your changes and push them to your forked repository.
6. Open a pull request against the `main` branch of the Motia repository.

Please provide a clear description of your changes in the pull request, along with any relevant information or context.

## Documentation Improvements

Improving the documentation is a great way to contribute to Motia. If you find any errors, typos, or areas that need clarification, please submit a pull request with the necessary changes. The documentation source files are located in the `packages/docs/content` directory.

## Sharing Examples and Use Cases

If you have built something interesting with Motia or have a real-world use case to share, we would love to showcase it in our [Examples](/docs/examples) section. You can contribute your examples by submitting a pull request to the [Motia Examples repository](https://github.com/MotiaDev/motia-examples).

## Spreading the Word

Help spread the word about Motia by sharing it with your friends, colleagues, and the developer community. You can also star our [GitHub repository](https://github.com/MotiaDev/motia), follow us on [Twitter](https://twitter.com/motiadev), and join our [Discord community](https://discord.gg/EnfDRFYW) to stay updated with the latest news and engage with other Motia developers.

We appreciate all forms of contributions and look forward to collaborating with you to make Motia even better! 

-   [getting-started](/docs/deployment-guide/getting-started): Documentation for getting-started.
---
title: Getting Started
description: Learn how to deploy your Motia project to production
full: true
---

When you're ready to deploy your Motia project to production, there are the two paths you can take:

<Cards>
  <Card href="/docs/concepts/deployment/motia-cloud/features" title="Deploy with Motia">
    Deploy your Motia project to production using Motia.
  </Card>
  <Card href="/docs/concepts/deployment/self-hosted" title="Self-Hosted">
    Deploy your Motia project to production using motia-docker.
  </Card>
</Cards>

<br />


-   [architecture](/docs/deployment-guide/motia-cloud/architecture): Documentation for architecture.
---
title: Architecture
description: Motia Cloud is a serverless platform. Some stuff that work locally may not work in the cloud.
---

### Bundle sizes

Motia Cloud currently has limited bundle sizes to 100MB, we're actively working on increasing this limit
to be higher than 1GB.

### Payload size on events

When sending events to topics, the data should not have more than 4KB.

1. Make sure you're not sending files as Base64 in the content of the event.
2. Make sure payloads you send are not too large, prefer storing in state and fetch it on the other steps.

### Using Local Files

Sometimes we need toa use local files when creating our backend logic. For example, creating templates.
Running binary files, etc. To do this, we can add them to steps as static files.

Make sure you follow the instructions in [Deployments page](/docs/concepts/deployment/motia-cloud/deployment#adding-static-files-to-the-bundle).

### Runtime timeouts

Motia Cloud currently has limited runtime timeouts:

- 15 minutes for Event and Cron Steps.
- 30 seconds for API Steps.

### Reserved environment variables

Motia Cloud is currently deployed to Amazon Web Services. Which means that there are 
some environment variables that are reserved for internal use. If you need to use one 
of these variables, make sure to add a different name.

```bash
_HANDLER
_X_AMZN_TRACE_ID
AWS_DEFAULT_REGION
AWS_REGION
AWS_EXECUTION_ENV
AWS_LAMBDA_FUNCTION_NAME
AWS_LAMBDA_FUNCTION_MEMORY_SIZE
AWS_LAMBDA_FUNCTION_VERSION
AWS_LAMBDA_INITIALIZATION_TYPE
AWS_LAMBDA_LOG_GROUP_NAME
AWS_LAMBDA_LOG_STREAM_NAME
AWS_ACCESS_KEY
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
AWS_LAMBDA_RUNTIME_API
LAMBDA_TASK_ROOT
LAMBDA_RUNTIME_DIR
```

### Limitations

- 100MB bundle size
- 4KB payload size on events
- 15 minutes runtime timeout for Event and Cron Steps
- 30 seconds runtime timeout for API Steps

## Troubleshooting build outputs

Make sure you follow the instructions in [Deployments page](/docs/concepts/deployment/motia-cloud/deployment#adding-static-files-to-the-bundle).


-   [continuous-deployment](/docs/deployment-guide/motia-cloud/continuous-deployment): Documentation for continuous-deployment.
---
title: Continuous Deployment
description: Move faster with continuous deployment
---

This guide helps creating a continuous deployment pipeline for your Motia project.

## Before you start

Before you create your pipeline, you first need to have deployed your project to Motia Cloud.
Check the [Deployment](/docs/concepts/deployment/motia-cloud/deployment) page for more information.

## Adding the Environment ID

After you have deployed your project to Motia Cloud, you need to add the environment ID to your pipeline.
You can find the environment ID in the Motia Cloud web interface by navigating to the Environment page and
clicking on the Settings tab.

## Creating an API Key

When you open Motia Cloud, you should see API Keys tab. Click on the Create API Key button to create a new API Key.
Copy the API Key and add it to your project [as a secret](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets).
Do NOT paste the API Key content to your workflow file.

## Populating Environment Variables

Add all environment variables you need on your project to [repository secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets),
then make sure to update `Create Env file` section in the workflow file.

## Using GitHub Actions

You can use GitHub Actions to deploy your Motia project to Motia Cloud.

```yaml
name: Deploy

on:
  push:
    branches:
      - main
  workflow_dispatch:
    inputs:
      versionName:
        description: 'Version Name to deploy'
        required: true
      versionDescription:
        description: 'Version Description to deploy'
        required: true

env:
  # Add your API Key as a Secret in your Repository (Do NOT add it here)
  # https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
  MOTIA_API_KEY: ${{ secrets.MOTIA_API_KEY }}
  # Fill your environment ID here
  MOTIA_ENV_ID: __FILL YOUR ENVIRONMENT ID HERE__

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.release.tag_name || github.ref }}

      - name: Set VERSION_NAME and DESCRIPTION
        id: meta
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            echo "VERSION_NAME=${{ github.event.inputs.versionName }}" >> $GITHUB_ENV
            echo "VERSION_DESCRIPTION=${{ github.event.inputs.versionDescription }}" >> $GITHUB_ENV
          else
            echo "VERSION_NAME=${GITHUB_SHA::7}" >> $GITHUB_ENV
            echo "VERSION_DESCRIPTION=${{ github.event.head_commit.message }}" >> $GITHUB_ENV
          fi

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
          cache-dependency-path: 'package-lock.json'

      - name: Install dependencies
        run: npm ci

      # Replace MY_SECRET with your secret
      # Add as many as you need
      # https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
      - name: Create Env file
        run: |
          echo "MY_SECRET=${{ secrets.MY_SECRET }}" > .env

      - name: Deploy using Motia Cloud
        run: |
          npx motia cloud deploy \
            --api-key ${{ env.MOTIA_API_KEY }} \
            --environment-id ${{ env.MOTIA_ENV_ID }} \
            --version-name "${{ env.VERSION_NAME }}" \
            --version-description "${{ env.VERSION_DESCRIPTION }}" \
            --env-file .env
```

-   [deployment](/docs/deployment-guide/motia-cloud/deployment): Documentation for deployment.
---
title: Deployment
description: Deploying your project to Motia Cloud
---

There are two ways to deploy your project to Motia Cloud:

1. Using the CLI
2. Using the Web interface

## Using the Motia CLI for Deployment

```bash
motia cloud deploy --api-key <api-key> --version-name <version> [options]
```

#### Required Options

| Option          | Alias | Description                    | Environment Variable |
| --------------- | ----- | ------------------------------ | -------------------- |
| `--api-key`     | `-k`  | API key for authentication     | `MOTIA_API_KEY`      |
| `--version-name`| `-v`  | Version tag for the deployment | None                 |

#### Optional Options

| Option                 | Alias | Description                                                        | Environment Variable     |
| ---------------------- | ----- | ------------------------------------------------------------------ | ------------------------ |
| `--environment-id`     | `-s`  | Environment ID                                                     | `MOTIA_ENVIRONMENT_ID`   |
| `--version-description`| `-d`  | Version description for the deployment                             | None                     |
| `--env-file`           | `-e`  | Path to environment file                                           | None                     |

> **Note:** Command-line options take precedence over environment variables. If both are provided, the command-line value will be used.

Deploy with a specific version:

```bash
motia cloud deploy --api-key your-api-key-here --version-name 1.2.3
```

Deploy to a specific environment with environment variables:

```bash
motia cloud deploy --api-key your-api-key-here \
  --version-name 1.2.3 \
  --env-file .env.production \
  --environment-id env-id
```

## Using Web interface

Through the web interface, you can deploy your project from workbench to a live environment with one click.

![One Click Deployment](../../img/cloud/one-click-deploy.gif)

Steps to deploy from web interface:

1. Have your local project running (make sure your Motia version is 0.6.4 or higher)
2. Go to import from workbench on Motia Cloud
3. Select the port your local project is running on
4. Choose the project and environment name
5. Add any environment variables you need (you can upload from .env file or paste the content to auto-fill)
6. Click Deploy
7. Watch the magic happen


## Adding static files to the bundle

Sometimes we need to use local files when creating our backend logic. For example, creating templates.
Running binary files, etc. To do this, we can add them to steps as static files.

Adding them to Steps as static files, you need to add `includeFiles` to the step config. The path
 should be relative to the step file.

```typescript
import { EventConfig } from 'motia'

export const config: EventConfig = {
  name: 'Content Outliner',
  description: 'Creates detailed content outline based on the initial idea',
  type: 'event',
  emits: [{ topic: 'write-content', label: 'Write first content' }],
  virtualEmits: ['virtual-write-content'],
  flows: ['Content'],
  subscribes: ['build-outline'],
  input,
  includeFiles: ['./content-outliner.mustache'], // relative to the step file
}
```

### Adding binary files to the bundle

Binary files are also supported, but the entire bundle size must not exceed 100MB.
The binary architecture should be linux_amd64.

## Troubleshooting Build Outputs

When adding static files, it's important to check the build output to make sure the files are included.

For example, in [this project](https://github.com/MotiaDev/motia-agent-content), there are a few steps that
include static files.

When running `npx motia build`, it will generate the following output in `dist` folder:

```
dist/
└── node/steps/content/
    ├── agents
    │   ├── content-outliner.step.zip
    │   ├── content-writer.step.zip
    │   └── ideator.step.zip
    ├── api
    │   ├── generate-content-api.step.zip
    │   └── get-content.step.zip
    ├── motia.steps.json
    └── router-node.zip
```

If you check the content of `content-outliner.step.zip`, it should have this

```
steps/
└── content/
    └── agents/
        ├── content-outliner.mustache
        ├── content-outliner.step.js
        └── content-outliner.step.js.map
```

Now you made sure the static file called `content-outliner.mustache` is included in the bundle.

-   [faq](/docs/deployment-guide/motia-cloud/faq): Documentation for faq.
---
title: FAQ
description: Frequently asked questions about Motia Cloud
---

## Can I deploy any Motia app to Motia Cloud?

Node.JS projects are fully supported. Python projects are supported as well but there are a few external libraries that are not currently supported, such as:

- TensorFlow
- Pytorch

These are not supported due to the limited bundle size of 100MB.

Be mindful that static or binary files added to the bundle must not exceed 100MB.

## What happens when I deploy my project to Motia Cloud?

When you deploy for the first time, it's immediately available. But when you deploy 
for the second time and beyond, the deployment is listed but needs to be manually promoted to be live.

Promoting a deployment is a really simple process and happens immediately after you click.
Check the [Promote](/docs/concepts/deployment/motia-cloud/features#instant-rollbacks-and-roll-ups-updates) page for more information.

## I deployed a new version but it didn't update

It's because Motia Cloud doesn't automatically promote the new version to be live. You need to promote it manually.
Check the [Promote](/docs/concepts/deployment/motia-cloud/features#instant-rollbacks-and-roll-ups-updates) page for more information.

## How do I deploy my project to Motia Cloud?

You can deploy your project to Motia Cloud by using the Motia CLI or through the web interface.
Check the [Deployment](/docs/concepts/deployment/motia-cloud/deployment) page for more information.

## How do I rollback to a previous deployment?

You can rollback to a previous deployment by clicking the rollback button in the Motia Cloud web interface.
Check the [Promote](/docs/concepts/deployment/motia-cloud/features#instant-rollbacks-and-roll-ups-updates) page for more information.

## How do I promote a deployment to be live?

You can promote a deployment to be live by clicking the promote button in the Motia Cloud web interface.
Check the [Promote](/docs/concepts/deployment/motia-cloud/features#instant-rollbacks-and-roll-ups-updates) page for more information.

## How do I delete a deployment?

You can delete a deployment by clicking the delete button in the Motia Cloud web interface.

## How do I update environment variables?

Currently, the only way to update environment variables is by creating a new deployment.
The reason is that every deployment is an atomic deployment and Environment Variables can also be source of
issues.

This was a decision to make sure that deployments are always predictable and consistent. And rollbacks 
can be done with confidence. If an environment variable updated caused an issue, you can quickly rollback to 
a previous deployment.

## How do I add static or binary files to my project?

You can add static files to your project by adding them to the `includeFiles` property in the step config.
Check the [Deployment](/docs/concepts/deployment/motia-cloud/deployment#adding-static-files-to-the-bundle) page for more information.

## Is it possible to deploy using GitHub Actions?

Yes, it's totally possible to deploy your project using GitHub Actions.

## How much it cost?

We're still working on the pricing model, but it's going to be based on usage. You will pay for what you use.

## How do I get support?

You can get support by creating an issue on our [GitHub repository](https://github.com/MotiaDev/motia-cloud-support/issues).


-   [features](/docs/deployment-guide/motia-cloud/features): Documentation for features.
---
title: Features
description: Learn how to deploy your Motia Project to a live environment
---

Motia Cloud is the easiest way to deploy your Motia Project to a live environment.
Quickly deploy your project to a live environment with one click. Then confidently
roll up updates, roll back to a previous stable version, and scale your project with ease.
Manage multiple environments, visualize logs and traces, and keep your project running smoothly.

## Real-time deployment status updates

You can see the deployment status in real-time in the Motia Cloud web interface

![Deployment real time updates](../../img/cloud/deployment-real-time-updates.png)

## Deployment history

All recent deployments on your project are available in Motia Cloud UI. You can browse them
and promote them to be live in the environment.

![Deployment history](../../img/cloud/deployments-list.png)

## Zero downtime deployments

Every deployment is an atomic deployment, this means that Motia Cloud creates a new infrastructure
with all the Message Queues system isolatedly for each deployment. 

### Why is this important?

- No downtime deployments
- Avoid backwards compatibility issues on message queues: Example, you can change a topic data structure
  without worrying about breaking messages that are flowing during the deployment.

## Instant rollbacks and roll up updates

With one button you can rollback to a previous deployment. This allows you to be confident
on deployments, if anything fails, quickly rollback to a previous stable version.

![Rollback](../../img/cloud/promote.png)

## One-click deployment

Deploy your project from workbench to a live environment with one click.

![One Click Deployment](../../img/cloud/one-click-deploy.gif)

## Observability

Have the same experience you have with Workbench locally in cloud. Such as:

- Logs visualization
- Tracing tool

### Logs visualization

You can see the logs of your project in the Motia Cloud web interface.

![Logs](../../img/cloud/logs.png)

### Tracing tool

Tracing tool to quickly visualize the flow of requests through the system.

![Tracing](../../img/cloud/tracing.png)

## Multiple environments support

Motia Cloud supports creating multiple environments for your projects.

![Multiple environments](../../img/cloud/environments-list.png)

## Scalability

- Horizontal scaling individually for each step
- Retry mechanisms for event steps built-in (3 retries by default)

## Learn how to deploy

Learn how to deploy your project to Motia Cloud in the [Deployment](/docs/concepts/deployment/motia-cloud/deployment) page.

-   [self-hosted](/docs/deployment-guide/self-hosted): Documentation for self-hosted.
---
title: Self-Hosted Deployment
description: Learn how to deploy your Motia project to production using motia-docker
---

We provide a docker image that you can use to deploy your Motia project to production. You can use it as a base image and add your own customizations or use it as is.

<Callout type="warn">You will need to use the latest version of the motia package **0.5.2-beta.101 or higher**</Callout>

## Quick setup

<Steps>
<Step>
#### Setup your motia project

```bash
npx motia@latest docker setup
```

</Step>
<Step>
#### Run your motia project inside a container

```bash
npx motia@latest docker run
```

  </Step>
  <Step>
#### You are good to go, your project should be running on localhost under port 3000, for additional options and configuration run

```bash
npx motia@latest docker run --help
```

  </Step>
</Steps>

> Reference the [CLI](/docs/concepts/cli#docker) for more information on the docker commands.

## Using the docker image

You will need to implement your own Dockerfile where you will use the motia-docker image as a base image. Use the following template as a starting point for your Dockerfile:

```dockerfile
# NOTE: Some cloud providers will require you to specify the platform to match your target architecture
# i.e.: AWS Lightsail requires arm64, therefore you update your FROM statement to: FROM --platform=linux/arm64 motiadev/motia:latest
FROM motiadev/motia:latest

# Install Dependencies
COPY package*.json ./
RUN npm ci --only=production

# Move application files
COPY . .

# Enable the following lines if you are using python steps!!!
# Setup python steps dependencies
# RUN npx motia@latest install

# Expose outside access to the motia project
EXPOSE 3000

# Run your application
CMD ["npm", "run", "start"]
```

<Callout type="info">
  Depending on the cloud provider you will use to deploy your Motia project, you will need to adjust the exposed ports
  and the command to start your application.
</Callout>

## Create a .dockerignore file

Create a .dockerignore file in the root of your project to exclude files that are not needed in the docker image. You can use the following template as a starting point for your .dockerignore file:

```bash
# Git
.git
.gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Node
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Local development
.env

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

## Build your image

```bash
docker build -t <your-image-name> .
```

## Run your Motia application

Once you've built your image, you can run it using the following command:

```bash
docker run -it --rm -p 3000:3000 <your-image-name>
```

## Motia Docker Resources

- [Docker Registry](https://hub.docker.com/r/motiadev/motia)
- [Github Repo](https://github.com/MotiaDev/motia/packages/docker)
- [Example Motia project with deployment boilerplate for AWS LightSail and Railway](https://github.com/MotiaDev/motia-examples/tree/main/examples/motia-docker)


-   [cli](/docs/development-guide/cli): Documentation for cli.
---
title: Command Line Interface (CLI)
description: Learn how to use the Motia CLI to manage your projects and workflows
---

# Command Line Interface (CLI)

Motia provides a powerful Command Line Interface (CLI) to help you manage your projects and workflows. The CLI offers various commands for creating projects, generating steps, managing state, and more.

## Installation

The Motia CLI is automatically installed when you install the `motia` package. You can use it by running `npx motia` followed by the desired command.

## Commands

### `create`

Create a new Motia project.

```bash
npx motia@latest create [options]
```

Options:

- `-n, --name <project name>`: The name for your project, used to create a directory. Use `.` or `./` to create it in the current directory.


### `build`

Build your project, generating zip files for each step and creating a configuration file.

```bash
npx motia build
```

This command:

1. Compiles all your steps (both Node.js and Python)
2. Bundles each step into a zip file
3. Generates a `motia.steps.json` configuration file in the `dist` directory
4. Organizes the output in the `dist` directory

### `deploy`

Deploy your built steps to the Motia deployment service.

```bash
motia cloud deploy --api-key <api-key> --version-name <version> [options]
```

Options:

- `-k, --api-key <key>` (required): Your API key for authentication
- `-n, --project-name <name>`: Project name (used when creating a new project)
- `-s, --environment-id <id>`: Environment ID (can also be set via MOTIA_ENVIRONMENT_ID env var)
- `--environment-name <name>`: Environment name (used when creating a new environment)
- `-v, --version-name <version>` (required): The version to deploy
- `-d, --version-description <description>`: The description of the version
- `-e, --env-file <path>`: Path to environment file

Example:

```bash
motia cloud deploy --api-key your-api-key-here --version-name 1.2.3 --environment-id env-uuid
```

The deployment process:

1. Build your project
2. Uploads each zip file individually with its path information
3. Starts the deployment process on the server

### `dev`

Start the development server.

```bash
npx motia dev [options]
```

Options:

- `-p, --port <port>`: The port to run the server on (default: 3000).
- `-H, --host [host]`: The host address for the server (default: localhost).
- `-d, --debug`: Enable debug logging.

### `get-config`

Get the generated config for your project.

```bash
npx motia get-config [options]
```

Options:

- `-o, --output <path>`: Path to write the generated config file.

### `emit`

Emit an event to the Motia server.

```bash
npx motia emit [options]
```

Options:

- `--topic <topic>` (required): Event topic/type to emit.
- `--message <message>` (required): Event payload as a JSON string.
- `-p, --port <number>`: Port number (default: 3000).

### `generate`

Generate Motia resources.

#### `generate step`

Create a new step with interactive prompts.

```bash
npx motia generate step [options]
```

Options:

- `-d, --dir <step file path>`: The path relative to the steps directory to create the step file.

#### `generate openapi`

Generate OpenAPI spec for your project.

```bash
npx motia generate openapi [options]
```

Options:

- `-t, --title <tile of the document>`: Title for the OpenAPI document. Defaults to project name from package.json.
- `-v, --version <version of the document>`: Version of the OpenAPI document. Defaults to 1.0.0.
- `-o, --output <output file name / path>`: The file name and path relative to root to create the openapi file. Defaults to `openapi.json` at the root.

### `state`

Manage application state.

#### `state list`

List the current file state.

```bash
npx motia state list
```

## Debugging

You can enable debug logging by passing the `-d` or `--debug` flag to the `dev` command:

```bash
npx motia dev --debug
```

This will set the `LOG_LEVEL` environment variable to `'debug'`, providing more detailed logging output.

### `docker`

Tools to help you setup your Motia project with docker and run it inside a container.

#### `docker setup`

Setup your Motia project for Docker

```bash
npx motia docker setup
```

#### `docker build`

Build your Motia project Docker image

```bash
npx motia docker build
```

Options:

- `--project-name <project name>` (required): The name of your project.

#### `docker run`

Run your Motia project inside a container

```bash
npx motia docker run
```

Options:

- `--port <number>`: Port number (default: 3000).
- `--project-name <project name>` (required): The name of your project.
- `--skip-build`: Skip building the Docker image and used the last built image.

## Next Steps

- Explore the [Core Concepts](/docs/concepts) to learn more about Steps, Flows, Events, and Topics.
- Check out the [Examples](/docs/examples) for common patterns and use cases.
- Join our [Community](/community) for help and discussions.


-   [customizing-flows](/docs/development-guide/customizing-flows): Documentation for customizing-flows.
---
title: Customizing Flows
description: Create custom visualizations and represent external processes in your Motia workflows
---

# Customizing Flows

Motia Workbench allows you to customize how your Steps appear in the flow visualization tool. This helps you create intuitive, context-aware visual components that clearly communicate your flow's behavior and external dependencies.

## UI Steps

UI Steps provide a way to create custom visual representations of your workflow Steps in the Workbench flow visualization tool.

### Overview

To create a custom UI for a Step, create a `.tsx` or `.jsx` file next to your Step file with the same base name:

<Tabs items={['tsx', 'jsx']}>
  <Tab value="tsx">
    ``` 
    steps/ 
    └── myStep/ 
      ├── myStep.step.ts      # Step definition
      └── myStep.step.tsx     # Visual override
    ```
  </Tab>
  <Tab value="jsx">
    ```
    steps/
    └── myStep/
      ├── myStep.step.js      # Step definition
      └── myStep.step.jsx     # Visual override
    ```
  </Tab>
</Tabs>

### Basic Usage

Let's override an EventNode while keeping the same look. We'll add an image and show the description.

![Custom Event Node](./../img/custom-event-node.png)

<Tabs items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```tsx
    // myStep.step.tsx

    import { EventNode, EventNodeProps } from 'motia/workbench'
    import React from 'react'

    export const Node: React.FC<EventNodeProps> = (props) => {
      return (
        <EventNode {...props}>
          <div className="flex flex-row items-start gap-2">
            <div className="text-sm text-gray-400 font-mono">{props.data.description}</div>
            <img
              style={{ width: '64px', height: '64px' }}
              src="https://www.motia.dev/icon.png"
            />
          </div>
        </EventNode>
      )
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```jsx
    // myStep.step.jsx

    import { EventNode } from 'motia/workbench'
    import React from 'react'

    export const Node = (props) => {
      return (
        <EventNode {...props}>
          <div className="flex flex-row items-start gap-2">
            <div className="text-sm text-gray-400 font-mono">{props.data.description}</div>
            <img
              style={{ width: '64px', height: '64px' }}
              src="https://www.motia.dev/icon.png"
            />
          </div>
        </EventNode>
      )
    }
    ```
  </Tab>
</Tabs>

### Available Components

Motia Workbench provides out-of-the-box components for different Step types:

| Component   | Props Type     | Description                                                                    |
| ----------- | -------------- | ------------------------------------------------------------------------------ |
| EventNode   | EventNodeProps | Base component for Event Steps, with built-in styling and connection points    |
| ApiNode     | ApiNodeProps   | Component for API Steps, includes request/response visualization capabilities  |
| CronNode    | CronNodeProps  | Base component for Cron Steps, displays timing information                     |
| NoopNode    | NoopNodeProps  | Base component for NoopNodes with a different color to comply workbench legend |

### Complete Customization

You can fully customize your node to look completely different. Here's an example of a custom ideator agent node:

![Custom Ideator Agent Node](./../img/custom-ideator-agent-node.png)

```tsx
import { BaseHandle, EventNodeProps, Position } from 'motia/workbench'
import React from 'react'

export const Node: React.FC<EventNodeProps> = (props) => {
  return (
    <div className="w-80 bg-black text-white rounded-xl p-4">
      <div className="group relative">
        <BaseHandle type="target" position={Position.Top} variant="event" />

        <div className="flex items-center space-x-3">
          <img className="w-8 h-8" src="https://cdn-icons-png.flaticon.com/512/12222/12222588.png" />
          <div className="text-lg font-semibold">{props.data.name}</div>
        </div>

        <div className="mt-2 text-sm font-medium text-gray-300">{props.data.description}</div>

        <div className="mt-3 flex flex-col gap-2 border border-gray-800 border-solid p-2 rounded-md w-full">
          <div className="flex items-center text-xs text-gray-400 space-x-2">Input</div>
          <div className="flex flex-col gap-2 whitespace-pre-wrap font-mono">
            <div className="flex items-center gap-2">
              <div className="">contentIdea:</div>
              <div className="text-orange-500">string</div>
            </div>
            <div className="flex items-center gap-2">
              <div className="">contentType:</div>
              <div className="text-orange-500">string</div>
            </div>
          </div>
        </div>

        <div className="mt-3 flex flex-col gap-2 border border-gray-800 border-solid p-2 rounded-md w-full">
          <div className="flex items-center text-xs text-gray-400 space-x-2">Output</div>
          <div className="flex flex-col gap-2 whitespace-pre-wrap font-mono">
            <div className="flex items-center gap-2">
              <div className="">topic:</div>
              <div className="text-orange-500">string</div>
            </div>
            <div className="flex items-center gap-2">
              <div className="">subtopics:</div>
              <div className="text-orange-500">string[]</div>
            </div>
            <div className="flex items-center gap-2">
              <div className="">keywords:</div>
              <div className="text-orange-500">string[]</div>
            </div>
            <div className="flex items-center gap-2">
              <div className="">tone:</div>
              <div className="text-orange-500">string</div>
            </div>
            <div className="flex items-center gap-2">
              <div className="">audience:</div>
              <div className="text-orange-500">string</div>
            </div>
          </div>
        </div>

        <BaseHandle type="source" position={Position.Bottom} variant="event" />
      </div>
    </div>
  )
}
```

#### Important Notes

- You will need to add `<BaseHandle>` to your node, otherwise it won't show the connectors.
- If your node has padding, make sure to add a group inside your node with class `group relative` so the handles can be correctly positioned.

<Callout type="info">Feel free to create your own custom components and reuse across multiple nodes.</Callout>

### Styling Guidelines

| Guideline                           | Description                                                   |
| ----------------------------------- | ------------------------------------------------------------- |
| Use Tailwind's utility classes only | Stick to Tailwind CSS utilities for consistent styling        |
| Avoid arbitrary values              | Use predefined scales from the design system                  |
| Keep components responsive          | Ensure UI elements adapt well to different screen sizes       |
| Follow Motia's design system        | Maintain consistency with Motia's established design patterns |

---

## NOOP Steps

NOOP (No Operation) Steps are a powerful feature that serve multiple purposes:

1. Modeling external processes, webhooks and integrations
2. Representing human-in-the-loop activities
3. Creating custom visualizations in the workbench
4. Testing flows during development

### File Structure

NOOP Steps require two files with the same base name:
- `stepName.step.ts` - Contains the step configuration
- `stepName.step.tsx` - Contains the UI component (optional)

#### Step Configuration File

<Tabs items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    // myStep.step.ts
    import { NoopConfig } from 'motia'

    export const config: NoopConfig = {
      type: 'noop',
      name: 'My NOOP Step',
      description: 'Description of what this step simulates',
      virtualEmits: ['event.one', 'event.two'],
      virtualSubscribes: [], // Required even if empty
      flows: ['my-flow'],
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    // myStep.step.js
    const config = {
      type: 'noop',
      name: 'My NOOP Step',
      description: 'Description of what this step simulates',
      virtualEmits: ['event.one', 'event.two'],
      virtualSubscribes: [], // Required even if empty
      flows: ['my-flow'],
    }

    module.exports = { config }
    ```
  </Tab>
</Tabs>

#### UI Component File

<Tabs items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    // myStep.step.tsx
    import React from 'react'
    import { BaseHandle, Position } from 'motia/workbench'

    export default function MyStep() {
      return (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-600 text-white">
          <div className="text-sm font-medium">My Step UI</div>
          <BaseHandle type="source" position={Position.Bottom} />
        </div>
      )
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    // myStep.step.jsx
    import React from 'react'
    import { BaseHandle, Position } from 'motia/workbench'

    export default function MyStep() {
      return (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-600 text-white">
          <div className="text-sm font-medium">My Step UI</div>
          <BaseHandle type="source" position={Position.Bottom} />
        </div>
      )
    }
    ```
  </Tab>
</Tabs>

### Example: Webhook Testing

Here's a complete example of a NOOP Step that simulates webhook events:

<Tabs items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    // test-webhook.step.ts
    import { NoopConfig } from 'motia'

    export const config: NoopConfig = {
      type: 'noop',
      name: 'Webhook Simulator',
      description: 'Simulates incoming webhook events',
      virtualEmits: ['webhook.received'],
      virtualSubscribes: [],
      flows: ['webhook-flow'],
    }
    ```

    ```typescript
    // test-webhook.step.tsx
    import React from 'react'
    import { BaseHandle, Position } from 'motia/workbench'

    export default function WebhookSimulator() {
      return (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-600 text-white">
          <div className="text-sm font-medium mb-2">Webhook Simulator</div>
          <button 
            onClick={() => {
              fetch('/api/webhook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ event: 'test' }),
              })
            }}
            className="px-3 py-1 bg-blue-600 rounded text-sm"
          >
            Trigger Webhook
          </button>
          <BaseHandle type="source" position={Position.Bottom} />
        </div>
      )
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    // test-webhook.step.js
    const config = {
      type: 'noop',
      name: 'Webhook Simulator',
      description: 'Simulates incoming webhook events',
      virtualEmits: ['webhook.received'],
      virtualSubscribes: [],
      flows: ['webhook-flow'],
    }

    module.exports = { config }
    ```

    ```javascript
    // test-webhook.step.jsx
    import React from 'react'
    import { BaseHandle, Position } from 'motia/workbench'

    export default function WebhookSimulator() {
      return (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-600 text-white">
          <div className="text-sm font-medium mb-2">Webhook Simulator</div>
          <button 
            onClick={() => {
              fetch('/api/webhook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ event: 'test' }),
              })
            }}
            className="px-3 py-1 bg-blue-600 rounded text-sm"
          >
            Trigger Webhook
          </button>
          <BaseHandle type="source" position={Position.Bottom} />
        </div>
      )
    }
    ```
  </Tab>
</Tabs>

### Representing External Processes

NOOP Steps represent parts of your workflow that happen outside your system. Common examples include:

#### Webhook Callbacks

<Tabs  items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    export const config: NoopConfig = {
      type: 'noop',
      name: 'Wait for Stripe Webhook',
      description: 'Waits for payment confirmation',
      virtualSubscribes: ['payment.initiated'],
      virtualEmits: ['/api/stripe/webhook'],
      flows: ['payment'],
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      type: 'noop',
      name: 'Wait for Stripe Webhook',
      description: 'Waits for payment confirmation',
      virtualSubscribes: ['payment.initiated'],
      virtualEmits: ['/api/stripe/webhook'],
      flows: ['payment'],
    }
    ```
  </Tab>
</Tabs>

#### Human Approvals

<Tabs  items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    export const config: NoopConfig = {
      type: 'noop',
      name: 'Manager Review',
      description: 'Manager reviews request',
      virtualSubscribes: ['approval.requested'],
      virtualEmits: ['/api/approvals/submit'],
      flows: ['approval'],
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      type: 'noop',
      name: 'Manager Review',
      description: 'Manager reviews request',
      virtualSubscribes: ['approval.requested'],
      virtualEmits: ['/api/approvals/submit'],
      flows: ['approval'],
    }
    ```
  </Tab>
</Tabs>

#### External System Integration

<Tabs  items={['TypeScript', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    export const config: NoopConfig = {
      type: 'noop',
      name: 'GitHub Webhook',
      description: 'Waiting for repository events',
      virtualSubscribes: ['repository.watched'],
      virtualEmits: ['/api/github/webhook'],
      flows: ['repo-automation'],
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      type: 'noop',
      name: 'GitHub Webhook',
      description: 'Waiting for repository events',
      virtualSubscribes: ['repository.watched'],
      virtualEmits: ['/api/github/webhook'],
      flows: ['repo-automation'],
    }
    ```
  </Tab>
</Tabs>

---

## Best Practices

### UI Steps

| Practice             | Description                                 |
| -------------------- | ------------------------------------------- |
| Use base components  | Use `EventNode` and `ApiNode` when possible |
| Keep it simple       | Maintain simple and clear visualizations    |
| Optimize performance | Minimize state and computations             |
| Documentation        | Document custom components and patterns     |
| Style sharing        | Share common styles through utility classes |

### NOOP Steps

| Category | Guidelines |
|----------|------------|
| **File Organization** | • Keep configuration and UI code in separate files<br/>• Use `.step.ts` for configuration<br/>• Use `.step.tsx` for UI components |
| **UI Components** | • Use functional React components<br/>• Include proper TypeScript types<br/>• Follow Tailwind's utility classes<br/>• Keep components minimal and focused<br/>• Design clear visual connection points<br/>• Always include BaseHandle components for flow connections |
| **Configuration** | • Always include `virtualSubscribes` (even if empty)<br/>• Use descriptive names for virtual events<br/>• Include clear descriptions<br/>• Use descriptive, action-oriented names |
| **External Process Modeling** | • Document expected timeframes and SLAs<br/>• Define all possible outcomes and edge cases<br/>• Use exact API route matching |
| **Testing** | • Create isolated test flows<br/>• Use realistic test data<br/>• Handle errors gracefully<br/>• Implement clear status indicators<br/>• Label test steps explicitly<br/>• Provide visual feedback for actions |

## Component Reference

### Core Imports

| Import | Purpose |
|--------|---------|
| `BaseHandle` | A React component that renders connection points for nodes in the workflow. Used to define where edges (connections) can start or end on a node. |
| `EventNodeProps` | (TypeScript only) Interface defining the properties passed to node components, including node data, selected state, and connection information. |
| `Position` | (TypeScript only) Enum that specifies the possible positions for handles on a node (Top, Right, Bottom, Left). Used to control where connection points appear. |

### Handle Placement

| Handle Type | Position | 
|------------|----------|
| Input Handles | Position.Top |
| Output Handles | Position.Bottom |
| Flow Direction | Top to bottom |


-   [environment-variables](/docs/development-guide/environment-variables): Documentation for environment-variables.
---
title: Environment Variables
description: Store API keys and configuration safely using .env files in your Motia apps.
---

# Environment Variables

Environment variables let you store API keys, database URLs, and other configuration outside your code. This keeps sensitive information secure and makes it easy to use different settings for development and production.

## Quick Setup

### 1. Create a `.env` File

Create a `.env` file in your project root:

```bash title=".env"
# API Keys
OPENAI_API_KEY=sk-your-api-key-here
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook

# Database  
DATABASE_URL=postgresql://user:password@localhost:5432/myapp

# App Settings
NODE_ENV=development
PORT=3000
```

### 2. Add to `.gitignore`

Make sure you never commit your `.env` file:

```bash title=".gitignore"
.env
.env.local
```

### 3. Create Template for Your Team

```bash title=".env.example"
# Copy this to .env and add your actual values
OPENAI_API_KEY=your-api-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
```

## Using Environment Variables in Steps

### TypeScript/JavaScript

```typescript title="my-step.step.ts"
export const config = {
  type: 'api',
  name: 'chat-with-ai',
  path: '/chat',
  method: 'POST'
}

export const handler = async (req, { logger }) => {
  // Use environment variables with process.env
  const apiKey = process.env.OPENAI_API_KEY
  const webhookUrl = process.env.DISCORD_WEBHOOK_URL
  
  if (!apiKey) {
    return { status: 400, body: { error: 'Missing API key' } }
  }
  
  logger.info('Using OpenAI API', { hasKey: !!apiKey })
  
  // Your logic here...
  return { status: 200, body: { message: 'Success!' } }
}
```

### Python

```python title="my-step.step.py"
import os

config = {
    'type': 'event', 
    'name': 'process-data',
    'subscribes': ['data.received']
}

async def handler(input_data, ctx):
    # Use environment variables with os.environ
    api_key = os.environ.get('OPENAI_API_KEY')
    database_url = os.environ.get('DATABASE_URL')
    
    if not api_key:
        raise ValueError('Missing OPENAI_API_KEY')
    
    ctx.logger.info('Processing with API key', {'has_key': bool(api_key)})
    
    # Your logic here...
    return {'status': 'processed'}
```

## Deployment

When you deploy your app, set environment variables through your hosting platform:

### Motia Cloud
```bash
motia env set OPENAI_API_KEY=sk-your-production-key
motia env set NODE_ENV=production
```

## Important Security Tips

<Callout type="warning">
**🔒 Keep Your Keys Safe**

- Never commit `.env` files to git
- Use different API keys for development and production  
- Don't share API keys in code or messages
</Callout>

That's it! Environment variables are simple - just put them in `.env` and use `process.env.VARIABLE_NAME` in your code.


-   [middleware](/docs/development-guide/middleware): Documentation for middleware.
---
title: Middleware
description: Run code before and after your API handlers
---

## What is Middleware?

Middleware runs before your API handler. Use it for authentication, logging, error handling, or any logic that applies to multiple endpoints.

---

## How It Works

A middleware is a function that receives three arguments:

```typescript
middleware(req, ctx, next)
```

- **req** - The incoming request (same as handler)
- **ctx** - The context object (same as handler)  
- **next()** - Call this to continue to the handler

If you don't call `next()`, the request stops. The handler never runs.

---

## Simple Example

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    import { ApiMiddleware } from 'motia'

    const authMiddleware: ApiMiddleware = async (req, ctx, next) => {
      if (!req.headers.authorization) {
        return { status: 401, body: { error: 'Unauthorized' } }
      }
      return next()
    }

    export const config = {
      name: 'ProtectedEndpoint',
      type: 'api',
      path: '/protected',
      method: 'GET',
      middleware: [authMiddleware]
    }

    export const handler = async (req, ctx) => {
      return { status: 200, body: { message: 'Success' } }
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const authMiddleware = async (req, ctx, next) => {
      if (!req.headers.authorization) {
        return { status: 401, body: { error: 'Unauthorized' } }
      }
      return next()
    }

    const config = {
      name: 'ProtectedEndpoint',
      type: 'api',
      path: '/protected',
      method: 'GET',
      middleware: [authMiddleware]
    }

    const handler = async (req, ctx) => {
      return { status: 200, body: { message: 'Success' } }
    }

    module.exports = { config, handler }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    async def auth_middleware(req, context, next_fn):
        if not req.get("headers", {}).get("authorization"):
            return {"status": 401, "body": {"error": "Unauthorized"}}
        return await next_fn()

    config = {
        "name": "ProtectedEndpoint",
        "type": "api",
        "path": "/protected",
        "method": "GET",
        "middleware": [auth_middleware]
    }

    async def handler(req, context):
        return {"status": 200, "body": {"message": "Success"}}
    ```
  </Tab>
</Tabs>

---

## Execution Order

Middleware runs in the order you list them:

```typescript
export const config = {
  name: 'MyEndpoint',
  type: 'api',
  path: '/endpoint',
  method: 'POST',
  middleware: [
    loggingMiddleware,  // Runs first
    authMiddleware,     // Runs second  
    errorMiddleware     // Runs third
  ]
}
```

---

## Modifying Responses

Await `next()` to get the response, then modify it:

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    const addHeadersMiddleware = async (req, ctx, next) => {
      const response = await next()
      
      return {
        ...response,
        headers: {
          ...response.headers,
          'X-Request-Id': ctx.traceId
        }
      }
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const addHeadersMiddleware = async (req, ctx, next) => {
      const response = await next()
      
      return {
        ...response,
        headers: {
          ...response.headers,
          'X-Request-Id': ctx.traceId
        }
      }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    async def add_headers_middleware(req, context, next_fn):
        response = await next_fn()
        
        headers = response.get("headers", {})
        headers["X-Request-Id"] = context.trace_id
        
        return {**response, "headers": headers}
    ```
  </Tab>
</Tabs>

---

## Error Handling

Catch errors from handlers:

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab value="TypeScript">
    ```typescript
    import { ZodError } from 'zod'

    const errorMiddleware = async (req, ctx, next) => {
      try {
        return await next()
      } catch (error: any) {
        if (error instanceof ZodError) {
          ctx.logger.error('Validation error', { errors: error.errors })
          return { status: 400, body: { error: 'Validation failed' } }
        }

        ctx.logger.error('Unexpected error', { error: error.message })
        return { status: 500, body: { error: 'Internal server error' } }
      }
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const { ZodError } = require('zod')

    const errorMiddleware = async (req, ctx, next) => {
      try {
        return await next()
      } catch (error) {
        if (error instanceof ZodError) {
          ctx.logger.error('Validation error', { errors: error.errors })
          return { status: 400, body: { error: 'Validation failed' } }
        }

        ctx.logger.error('Unexpected error', { error: error.message })
        return { status: 500, body: { error: 'Internal server error' } }
      }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python
    async def error_middleware(req, context, next_fn):
        try:
            return await next_fn()
        except ValidationError as e:
            context.logger.error("Validation error", {"errors": str(e)})
            return {"status": 400, "body": {"error": "Validation failed"}}
        except Exception as e:
            context.logger.error("Unexpected error", {"error": str(e)})
            return {"status": 500, "body": {"error": "Internal server error"}}
    ```
  </Tab>
</Tabs>

---

## Reusing Middleware

Create middleware files in a shared location:

```typescript title="middlewares/core.middleware.ts"
export const coreMiddleware = async (req, ctx, next) => {
  try {
    return await next()
  } catch (error) {
    ctx.logger.error('Error', { error })
    return { status: 500, body: { error: 'Internal server error' } }
  }
}
```

Import and use across steps:

```typescript title="steps/user.step.ts"
import { coreMiddleware } from '../middlewares/core.middleware'

export const config = {
  name: 'GetUser',
  type: 'api',
  path: '/users/:id',
  method: 'GET',
  middleware: [coreMiddleware]
}
```

---

## What's Next?

<Cards>
  <Card href="/docs/concepts/steps#triggers" title="Triggers">
    Learn more about Triggers
  </Card>
  
  <Card href="/docs/development-guide/testing" title="Testing">
    Learn more about testing your Motia Steps
  </Card>
</Cards>


-   [observability](/docs/development-guide/observability): Documentation for observability.
---
title: Observability
description: Understanding how to use the logging and debugging system in Motia
---

## Overview

Motia provides an out of the box logging and debugging system that works across different runtime environments. The system offers:

- Real-time log streaming in both terminal and Motia Workbench
- Multiple log levels with contextual information
- Local development debugging tools
- Integrated flow monitoring

## Log Levels and Usage

Motia supports four standard log levels:

| Log Type | Description                                                                        |
| -------- | ---------------------------------------------------------------------------------- |
| info     | General information about step execution, flow progress, and successful operations |
| error    | Critical issues, exceptions, failed operations, and system errors                  |
| debug    | Detailed debugging information and diagnostic data for troubleshooting             |
| warn     | Potential issues, edge cases, or situations requiring attention                    |

### Example Usage

<Tabs items={['TS', 'JS', 'Python']}>
  <Tab value='TS'>
    ```typescript
    export const handler: Handlers['StepName'] = async (input, { logger }) => {
      // Basic logging
      logger.info('Starting process')

      // Logging with context
      logger.info('Operation completed', {
        operationId: input.id,
        duration: 1500
      })

      // Error handling
      try {
        await riskyOperation()
      } catch (error) {
        logger.error('Operation failed', {
          error: error.message,
          stack: error.stack
        })
      }

      // Debug logging
      logger.debug('Operation details', {
        rawInput: input,
        timestamp: Date.now()
      })

      // Warning logging
      if (input.amount > 1000) {
        logger.warn('Large operation detected', {
          amount: input.amount,
          threshold: 1000
        })
      }
    }
    ```

  </Tab>
  <Tab value='JS'>
    ```javascript
    export const handler = async (input, { logger }) => {
      // Basic logging
      logger.info('Starting process')

      // Logging with context
      logger.info('Operation completed', {
        operationId: input.id,
        duration: 1500
      })

      // Error handling
      try {
        await riskyOperation()
      } catch (error) {
        logger.error('Operation failed', {
          error: error.message,
          stack: error.stack
        })
      }

      // Debug logging
      logger.debug('Operation details', {
        rawInput: input,
        timestamp: Date.now()
      })

      // Warning logging
      if (input.amount > 1000) {
        logger.warn('Large operation detected', {
          amount: input.amount,
          threshold: 1000
        })
      }
    }
    ```

  </Tab>
  <Tab value='Python'>
    ```python
    async def handler(input, ctx):
        # Basic logging
        ctx.logger.info('Starting process')

        # Logging with context
        ctx.logger.info('Operation completed', {
            'operation_id': input.get("id"),
            'duration': 1500
        })

        # Error handling
        try:
            await risky_operation()
        except Exception as error:
            ctx.logger.error('Operation failed', {
                'error': str(error),
                'stack': traceback.format_exc()
            })

        # Debug logging
        ctx.logger.debug('Operation details', {
            'raw_input': input.__dict__,
            'timestamp': time.time()
        })

        # Warning logging
        if input.amount > 1000:
            ctx.logger.warn('Large operation detected', {
                'amount': input.get("amount"),
                'threshold': 1000
            })
    ```
  </Tab>
</Tabs>

## Running and Debugging

<Steps>
  <Step>
    ### Start the Dev Server

    1. Navigate to your Motia project root folder
    2. Start the development server:

    <Tabs items={['npm', 'yarn', 'pnpm', 'bun']}>
      <Tab value="yarn">```yarn run dev ```</Tab>
      <Tab value="npm">```npm run dev ```</Tab>
      <Tab value="pnpm">```pnpm run dev ```</Tab>
      <Tab value="bun">```bun run dev ```</Tab>
    </Tabs>

    3. You can monitor logs in two ways:
      - Open [Motia Workbench](http://localhost:3000), select your flow, and expand the logs container
      - View logs directly in the terminal where you ran the dev command
  </Step>
  
  <Step>
    ### Trigger and Monitor Flows

    You can trigger flows using either the CLI or an [API step](/docs/concepts/steps/api):

    <Tabs items={['cli', 'api']}>
      <Tab value='cli'>
      ```bash
      npx motia emit --topic <topic> --message '{}'
      ```
      </Tab>
      <Tab value='api'>
      ```bash
      curl -X POST http://localhost:3000/<api-step-path> \
      -H "Content-Type: application/json" \
      -d '{}'
      ```
      </Tab>
    </Tabs>
  </Step>
  
  <Step>
    ### Debug Using Logs

    Each log entry automatically includes:

    - `timestamp`: When the log was generated
    - `traceId`: Unique identifier for the flow execution
    - `flows`: Array of flow names this step belongs to
    - `file`: Source file generating the log
    - `level`: Log level
    - `msg`: Log message
  </Step>
  
  <Step>
    ### Stopping the development server
    Press **Ctrl + C** (or **Cmd + C** on macOS) in your terminal. That's it!
  </Step>
</Steps>

## Best Practices

### Structured Logging

```typescript
// Good - Structured and searchable
logger.info('Payment processed', {
  paymentId: '123',
  amount: 100,
  status: 'success',
})

// Avoid - Harder to parse and search
logger.info(`Payment ${paymentId} processed: amount=${amount}`)
```

### Performance Monitoring

```typescript
export const handler: Handlers['StepName'] = async (input, { logger }) => {
  const startTime = performance.now()

  // Process operation
  const result = await processOperation(input)

  logger.info('Operation completed', {
    duration: performance.now() - startTime,
    memoryUsage: process.memoryUsage().heapUsed,
  })
}
```

### Debugging Tips

1. Add detailed context to error logs:

```typescript
logger.error('Operation failed', {
  error: error.message,
  code: error.code,
  input: JSON.stringify(input),
  stack: error.stack,
})
```

2. Use debug logs for detailed troubleshooting:

```typescript
logger.debug('Operation details', {
  rawInput: input,
  timestamp: Date.now(),
  state: currentState,
})
```

<Callout>
  Remember to stop your development server with Ctrl + C (or Cmd + C on macOS) when you're done debugging.
</Callout>


-   [project-structure](/docs/development-guide/project-structure): Documentation for project-structure.
---
title: Project Structure
description: Learn about Motia's project structure, file organization, and automatic step discovery system for building scalable workflow applications.
---

# Project Structure

Understanding how to organize your Motia project is crucial for building maintainable and scalable workflow applications. This guide covers the directory structure, file naming conventions, and Motia's automatic step discovery system.

## Basic Project Structure

Here's what a typical Motia project looks like:

<Folder name="my-motia-project" defaultOpen>
  <Folder name="steps" defaultOpen>
    <File name="api-gateway.step.ts" />
    <File name="data-processor_step.py" />  
    <File name="send-notification.step.js" />
    <File name="send-notification.tsx" />
  </Folder>
  <File name="package.json" />
  <File name="requirements.txt" />
  <File name="tsconfig.json" />
  <File name="types.d.ts" />
  <File name="motia-workbench.json" />
  <File name="config.yml" />
</Folder>

### File Descriptions

| File | Purpose | Type | Auto-Generated |
|------|---------|------|----------------|
| `01-api-gateway.step.ts` | TypeScript API endpoint | User Code | - |
| `02-data-processor_step.py` | Python data processing | User Code | - |
| `03-send-notification.step.js` | JavaScript automation | User Code | - |
| `send-notification.tsx` | Optional [UI override component](/docs/development-guide/customizing-flows) | User Code | - |
| `package.json` | Node.js dependencies (if using JS/TS) | Config | - |
| `requirements.txt` | Python dependencies (if using Python) | Config | - |
| `tsconfig.json` | TypeScript config (if using TypeScript) | Config | - |
| `types.d.ts` | **Type definitions for your project** | **Generated** | **✅ By TypeScript** |
| `motia-workbench.json` | **🤖 Visual workflow positioning** | **Generated** | **✅ By Motia** |
| `config.yml` | Optional Motia configuration | Config | - |

<Callout type="info">
The `steps/` directory is the heart of your Motia application - this is where all your workflow logic lives. Motia automatically discovers and registers any file following the naming pattern.
</Callout>

<Callout>
<strong>Location and nesting rules</strong>

- The `steps/` directory must live at the <em>project root</em> (e.g., `my-motia-project/steps`).
- You can freely nest steps in subfolders under `steps/` (e.g., `steps/aaa/a1.step.ts`, `steps/bbb/ccc/c1_step.py`).
- Discovery is recursive inside `steps/`, so deeper folder structures for large apps are supported.
</Callout>

## Automatic Step Discovery

<Callout type="default">
**Key Concept: Automatic Discovery** 

Motia will automatically discover and register **any file** that follows the `.step.` naming pattern as a workflow step. You don't need to manually register steps - just create a file with the right naming pattern and Motia will find it.
</Callout>

### Discovery Rules

Motia scans your `steps/` directory and automatically registers files as steps based on these rules:

1. **File must contain `.step.` or `_step.` in the filename** (e.g., `my-task.step.ts`, `my_task_step.py`)
2. **File must export a `config` object** defining the step configuration
3. **File must export a `handler` function** containing the step logic
4. **File extension determines the runtime** (`.ts` = TypeScript, `.py` = Python, `.js` = JavaScript)

When you run `motia dev`, Motia will:
- Scan the `steps/` directory recursively
- Find all files matching `*.step.*`
- Parse their `config` exports to understand step types and connections
- Register them in the workflow engine
- Make them available in the Workbench

## File Naming Convention

Motia uses this specific pattern for automatic step discovery:

```
[prefix-]descriptive-name.step.[extension]
```

<Callout type="warning">
The `.step.` part in the filename is **required** - this is how Motia identifies which files are workflow steps during automatic discovery.
</Callout>

### Supported Languages & Extensions

| Language | Extension | Example Step File | Runtime |
|----------|-----------|-------------------|---------|
| **TypeScript** | `.ts` | `user-registration.step.ts` | Node.js with TypeScript |
| **Python** | `.py` | `data-analysis_step.py` | Python interpreter |
| **JavaScript** | `.js` | `send-notification.step.js` | Node.js |

### Naming Examples by Step Type

| Step Type | TypeScript | Python | JavaScript |
|-----------|------------|---------|-----------|
| **API Endpoint** | `01-auth-api.step.ts` | `01-auth-api_step.py` or `auth_api_step.py` | `01-auth-api.step.js` |
| **Event Handler** | `process-order.step.ts` | `process-order_step.py` or `process_order_step.py` | `process-order.step.js` |
| **Cron Job** | `daily-report.step.ts` | `daily-report_step.py` or `daily_report_step.py` | `daily-report.step.js` |
| **Data Processing** | `transform-data.step.ts` | `ml-analysis_step.py` or `ml_analysis_step.py` | `data-cleanup.step.js` |

## Step Organization Patterns

<Tabs items={["Sequential", "Feature-Based", "Language-Specific"]}>
<Tab value="Sequential">

### Sequential Flow Organization
Perfect for linear workflows where order matters:

<Folder name="steps" defaultOpen>
  <File name="01-api-start.step.ts" />
  <File name="02-validate-data_step.py" />
  <File name="03-process-payment.step.js" />
  <File name="04-send-confirmation.step.ts" />
  <File name="05-cleanup_step.py" />
</Folder>

| Step | Language | Purpose |
|------|----------|---------|
| `01-api-start.step.ts` | TypeScript | API endpoint |
| `02-validate-data_step.py` | Python | Data validation |
| `03-process-payment.step.js` | JavaScript | Payment processing |
| `04-send-confirmation.step.ts` | TypeScript | Email service |
| `05-cleanup_step.py` | Python | Cleanup tasks |

</Tab>
<Tab value="Feature-Based">

### Feature-Based Organization
Organize by business domains for complex applications:

<Folder name="steps" defaultOpen>
  <Folder name="authentication" defaultOpen>
    <File name="login.step.ts" />
    <File name="verify-token_step.py" />
    <File name="logout.step.js" />
  </Folder>
  <Folder name="payment" defaultOpen>
    <File name="process-payment.step.ts" />
    <File name="fraud-detection_step.py" />
    <File name="webhook.step.js" />
  </Folder>
  <Folder name="notification" defaultOpen>
    <File name="email_step.py" />
    <File name="sms.step.js" />
    <File name="push.step.ts" />
  </Folder>
</Folder>

**Benefits:**
- Logical grouping by business domain
- Easy to locate related functionality
- Team ownership by feature area
- Independent scaling and deployment

</Tab>
<Tab value="Language-Specific">

### Language-Specific Organization
Group by programming language for team specialization:

<Folder name="steps" defaultOpen>
  <Folder name="typescript" defaultOpen>
    <File name="api-gateway.step.ts" />
    <File name="user-management.step.ts" />
    <File name="data-validation.step.ts" />
  </Folder>
  <Folder name="python" defaultOpen>
    <File name="ml-processing_step.py" />
    <File name="data-analysis_step.py" />
    <File name="image-processing_step.py" />
  </Folder>
  <Folder name="javascript" defaultOpen>
    <File name="automation.step.js" />
    <File name="webhook-handlers.step.js" />
    <File name="integrations.step.js" />
  </Folder>
</Folder>

**Benefits:**
- Team specialization by language
- Consistent tooling and patterns
- Easy onboarding for language experts
- Shared libraries and utilities

</Tab>
</Tabs>

## Language-Specific Configuration

### TypeScript/JavaScript Projects

For Node.js-based steps, you'll need:

```json title="package.json"
{
  "name": "my-motia-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "motia dev",
    "build": "motia build",
    "start": "motia start"
  },
  "dependencies": {
    "motia": "^0.5.12-beta.121",
    "zod": "^3.24.4"
  },
  "devDependencies": {
    "typescript": "^5.7.3",
    "@types/node": "^20.0.0"
  }
}
```

```json title="tsconfig.json (for TypeScript)"
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Node",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
```

### Python Projects

For Python-based steps:

```text title="requirements.txt"
# Core Motia dependency
motia>=0.5.12

# Common dependencies
requests>=2.28.0
pydantic>=1.10.0

# Data processing (if needed)
pandas>=1.5.0
numpy>=1.21.0
```

## Step Discovery Examples

Let's see how Motia discovers different step types:

### Example 1: TypeScript API Step

```typescript title="steps/user-api.step.ts"
import { ApiRouteConfig, Handlers } from 'motia'
import { z } from 'zod'

// Motia discovers this file because:
// 1. Filename contains '.step.'
// 2. Exports 'config' object
// 3. Has .ts extension -> uses TypeScript runtime
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'user-api',
  path: '/users',
  method: 'GET',
  emits: ['users.fetched'],
  flows: ['user-management']
}

export const handler: Handlers['user-api'] = async (req, { emit }) => {
  await emit({
    topic: 'users.fetched', 
    data: { users: [] }
  })
  
  return {
    status: 200,
    body: { message: 'Users retrieved' }
  }
}
```

### Example 2: Python Event Step

```python title="steps/data-processor_step.py"
# Motia discovers this file because:
# 1. Filename contains '.step.'  
# 2. Exports 'config' dict
# 3. Has .py extension -> uses Python runtime

config = {
    "type": "event",
    "name": "data-processor",
    "description": "Process incoming data with Python",
    "subscribes": ["users.fetched"],
    "emits": ["data.processed"],
    "flows": ["user-management"]
}

async def handler(input_data, ctx):
    """Process the data"""
    processed_data = {
        "original": input_data,
        "processed_at": ctx.utils.dates.now().isoformat(),
        "count": len(input_data.get("users", []))
    }
    
    await ctx.emit({
        "topic": "data.processed",
        "data": processed_data
    })
```

### Example 3: JavaScript Automation Step

```javascript title="steps/send-notifications.step.js"
// Motia discovers this file because:
// 1. Filename contains '.step.'
// 2. Exports 'config' object  
// 3. Has .js extension -> uses Node.js runtime

export const config = {
  type: 'event',
  name: 'send-notifications',
  description: 'Send notifications via multiple channels',
  subscribes: ['data.processed'],
  emits: ['notifications.sent'],
  flows: ['user-management']
}

export const handler = async (input, { emit, logger }) => {
  logger.info('Sending notifications', { data: input })
  
  // Send email, SMS, push notifications, etc.
  const results = await Promise.all([
    sendEmail(input),
    sendSMS(input),
    sendPush(input)
  ])
  
  await emit({
    topic: 'notifications.sent',
    data: { 
      results,
      sent_at: new Date().toISOString() 
    }
  })
}

async function sendEmail(data) { /* implementation */ }
async function sendSMS(data) { /* implementation */ }  
async function sendPush(data) { /* implementation */ }
```

## Auto-Generated Files

Some files in your Motia project are automatically generated:

- `types.d.ts` - TypeScript generates this for type definitions
- `motia-workbench.json` - Motia manages visual node positions in the Workbench

## Discovery Troubleshooting

If Motia isn't discovering your steps:

### Common Issues

<Tabs items={["Filename Issues", "Export Issues", "Location Issues"]}>
<Tab value="Filename Issues">

**Missing `.step.` (or `_step` for Python) in filename**

<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
❌ **Won't be discovered:**
<Folder name="steps" defaultOpen>
  <File name="user-handler.ts" />
  <File name="data-processor.py" />
  <File name="webhook.js" />
</Folder>
</div>
<div>
✅ **Will be discovered:**
<Folder name="steps" defaultOpen>
  <File name="user-handler.step.ts" />
  <File name="data-processor_step.py" />
  <File name="webhook.step.js" />
</Folder>
</div>
</div>

</Tab>
<Tab value="Export Issues">

**Missing config export**

```typescript title="❌ Won't be discovered"
// No config export
export const handler = async () => {
  console.log('This won't be found by Motia')
}
```

```typescript title="✅ Will be discovered"
// Proper exports
export const config = {
  type: 'event',
  name: 'my-step',
  subscribes: ['my-topic'],
  emits: ['my-output'],
  flows: ['my-flow']
}

export const handler = async (input, ctx) => {
  // Motia will discover and register this step
}
```

</Tab>
<Tab value="Location Issues">

**File outside steps/ directory**

<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
<div>
❌ **Won't be discovered:**
<Folder name="project-root" defaultOpen>
  <Folder name="src">
    <File name="user-handler.step.ts" />
  </Folder>
  <Folder name="lib">
    <File name="processor_step.py" />
  </Folder>
</Folder>
</div>
<div>
✅ **Will be discovered:**
<Folder name="project-root" defaultOpen>
  <Folder name="steps" defaultOpen>
    <File name="user-handler.step.ts" />
    <File name="processor_step.py" />
  </Folder>
</Folder>
</div>
</div>

</Tab>
</Tabs>

### Discovery Verification

Check if your steps are discovered:

```bash
# Run Motia in development mode
motia dev

# Look step creation in your console console:
➜ [CREATED] Step (Cron) steps/petstore/state-audit-cron.step.ts created
➜ [CREATED] Step (Event) steps/petstore/process-food-order.step.ts created
➜ [CREATED] Step (Event) steps/petstore/notification.step.ts created
➜ [CREATED] Step (API) steps/petstore/api.step.ts created
```

## Next Steps

Now that you understand how Motia discovers and organizes steps:

- Learn about [Core Concepts](/docs/concepts) to understand how steps work together
- Explore [Defining Steps](/docs/concepts/steps) for detailed step creation
- Check out [Triggers](/docs/concepts/steps#triggers) for API, Event, and Cron steps

-   [state-management](/docs/development-guide/state-management): Documentation for state-management.
---
title: State Management
description: Learn how to manage state within your Motia.dev workflows for persistent data and cross-step communication.
---

State management is fundamental to building robust and dynamic workflows in Motia.dev. Our system is designed to be powerful yet simple, providing you with everything you need to maintain state across your flows and steps:

✨ **Zero Configuration (Default):** In-memory storage out of the box for quick setup. <br />
🔌 **Flexible Storage Options:** Choose from Memory, File, and Redis adapters to suit your persistence needs. <br />
🧹 **Automatic State Cleanup:** Optional Time-To-Live (TTL) support for automatic state expiration (Redis). <br />
🔒 **Built-in Isolation:** Each flow execution can use its own isolated state, ensuring data separation and security. <br />

## Core Concepts: State Manager Methods

The `state` object, accessible within your step handlers via the `ctx` context, provides the following methods for state management:

| Method    | Parameters                             | Return Type          | Description                                                                                                                                                                                   |
| --------- | -------------------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get`     | `scope: string, key: string`           | `Promise<T \| null>` | Retrieves a value associated with the given `key` and `scope` from the state store. Returns `null` if the key is not found. The type `T` is inferred based on how you use the returned value. |
| `set`     | `scope: string, key: string, value: T` | `Promise<void>`      | Stores a `value` associated with the given `key` and `scope` in the state store. The type `T` can be any serializable JavaScript/JSON value.                                                  |
| `delete`  | `scope: string, key: string`           | `Promise<void>`      | Removes the key-value pair associated with the given `key` and `scope` from the state store.                                                                                                  |
| `clear`   | `scope: string`                        | `Promise<void>`      | Removes **all** state data associated with the provided `scope`. This is useful for cleaning up state for a specific scope.                                                                   |
| `cleanup` | _(None)_                               | `Promise<void>`      | Performs periodic maintenance tasks, such as removing expired state data (TTL cleanup). The actual implementation depends on the configured state adapter.                                    |

**Important:** State manager methods (`get`, `set`, `delete`, `clear`) **require a `scope` string as the first parameter.** While in most cases, you will use the `traceId` (automatically provided in `ctx.traceId`) as the scope to ensure flow-level isolation, **you can technically use any string value as the scope** to group and manage state data as needed. Using `traceId` is the recommended and most common practice for flow-isolated state.

### State Scope and Isolation

Each flow execution in Motia.dev is assigned a unique `traceId` (a UUID). Using this `traceId` as the **scope** for state management provides automatic isolation, ensuring: _(Revised to clarify `traceId` as scope)_

| Feature        | Description                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Isolation**  | Each flow execution operates within its own isolated state space when using `traceId` as the scope.                 |
| **Boundaries** | Clear separation of state data between different flow executions when scoped by `traceId`, preventing interference. |
| **Cleanup**    | State data scoped by `traceId` can be easily cleared using `state.clear(traceId)`.                                  |

### State Structure Example

State data is stored as key-value pairs, namespaced under a scope string. When using `traceId` as the scope, the internal structure might look like this:

```typescript
// Example state structure (internal representation) - using traceId as scope
{
  "motia:state:{traceId-123}": {  // State for flow execution with traceId 'traceId-123' (scope)
    "booking": {                 // Namespaced key 'booking'
      "customer": { ... },
      "venue": { ... }
    },
    "payment": {                 // Namespaced key 'payment'
      "status": "pending",
      "amount": 100
    }
  },
  "motia:state:{traceId-456}": {  // State for another flow execution with traceId 'traceId-456' (different scope)
    // ... different state data for this flow ...
  }
}
```

> **Info:** You can access the `state` manager within any step through the `ctx` (context) argument, which is automatically injected into your [step handler](/docs/concepts/steps#context-object). While **`traceId` from `ctx.traceId` is the recommended scope for flow isolation**, remember that **you can use any string as the scope** parameter in `state` methods for more advanced state management scenarios.

## Using State in Steps

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab label="TypeScript">
    
  ```typescript
  import { Handlers } from 'motia'

  interface BookingData {
    customer: { name: string; email: string };
    venue: { id: string; name: string };
  }

  export const handler: Handlers['StepName'] = async (input, { state, traceId }) => { // Get traceId from context
    // Store state (using traceId as scope)
    await state.set<BookingData>(traceId, 'booking', {
      customer: input.customer,
      venue: input.venue,
    });

    // Retrieve state (using traceId as scope)
    const booking = await state.get<BookingData>(traceId, 'booking');

    // Delete specific state (using traceId as scope)
    await state.delete(traceId, 'booking');

    // Clear all state for this flow (using traceId as scope)
    await state.clear(traceId);
  }
  ```

  </Tab>

  <Tab label="JavaScript">
    
  ```javascript
  import { Handlers } from 'motia'

  export const handler: Handlers['StepName'] = async (input, { state, traceId }) => { // Get traceId from context
    // Store state (using traceId as scope)
    await state.set(traceId, 'booking', {
      customer: input.customer,
      venue: input.venue,
    });

    // Retrieve state (using traceId as scope)
    const booking = await state.get(traceId, 'booking');

    // Delete specific state (using traceId as scope)
    await state.delete(traceId, 'booking');

    // Clear all state for this flow (using traceId as scope)
    await state.clear(traceId);
  }
  ```

  </Tab>

  <Tab label="Python">
  
  ```python
  async def handler(input, ctx): # ctx is the context object
      trace_id = ctx.trace_id # Access traceId from context

      # Store state (using traceId as scope)
      await ctx.state.set(trace_id, 'booking', {
          'customer': input.get("customer"),
          'venue': input.get("venue")
      })

      # Retrieve state (using traceId as scope)
      booking = await ctx.state.get(trace_id, 'booking')

      # Delete specific state (using traceId as scope)
      await ctx.state.delete(trace_id, 'booking')

      # Clear all state (using traceId as scope)
      await ctx.state.clear(trace_id)
  ```
  </Tab>
</Tabs>

## Debugging

### Inspecting State

<Tabs items={['Memory', 'File', 'Redis']}>
  <Tab label="Memory">
  > State is only available during runtime in the Node.js process memory. You cannot inspect memory state directly outside of a running step execution. Use logging within your steps to output state values for debugging purposes.
  </Tab>
  <Tab label="File">
  
  To inspect state stored in the **File Adapter**, you can directly view the contents of the state file using the Motia CLI:

  ```bash
  # View state file contents
  motia state list
  ```

  This command will output the entire state file (motia.state.json) content in JSON format to your console, allowing you to examine the stored state data.

  </Tab>
  <Tab label="Redis">
  
  To inspect state stored in **Redis Adapter**, you can use the `redis-cli` command-line tool to interact with your Redis server:

  ```bash
  # List all state keys (under the motia:state prefix)
  redis-cli KEYS "motia:state:*"

  # Get specific state for a given traceId and key
  redis-cli GET "motia:state:{traceId}:booking"
  ```
  **Note:** Replace `{traceId}` in the `redis-cli GET` command with the actual `traceId` of the flow execution you are debugging. Replace `booking` with the specific `key` you want to inspect.

  </Tab>
</Tabs>

## Best Practices

### Namespacing

Use dot notation to organize related state data hierarchically:

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab label="TypeScript">
    
  ```typescript
  // Good - Organized hierarchically (using traceId scope)
  await state.set(traceId, 'booking.customer', customerData)
  await state.set(traceId, 'booking.venue', venueData)
  await state.set(traceId, 'payment.status', 'pending')

  // Avoid - Flat structure (using traceId scope)
  await state.set(traceId, 'customer', customerData)
  await state.set(traceId, 'venue', venueData)
  await state.set(traceId, 'paymentStatus', 'pending')
  ```

  </Tab>

  <Tab label="JavaScript">
    
  ```javascript
  // Good - Organized hierarchically (using traceId scope)
  await state.set(traceId, 'booking.customer', customerData)
  await state.set(traceId, 'booking.venue', venueData)
  await state.set(traceId, 'payment.status', 'pending')

  // Avoid - Flat structure (using traceId scope)
  await state.set(traceId, 'customer', customerData)
  await state.set(traceId, 'venue', venueData)
  await state.set(traceId, 'paymentStatus', 'pending')
  ```

  </Tab>

  <Tab label="Python">
    
  ```python
  # Good - Organized hierarchically (using traceId scope)
  await ctx.state.set(trace_id, 'booking.customer', customer_data)
  await ctx.state.set(trace_id, 'booking.venue', venue_data)
  await ctx.state.set(trace_id, 'payment.status', 'pending')

  // Avoid - Flat structure (using traceId scope)
  await ctx.state.set(trace_id, 'customer', customer_data)
  await ctx.state.set(trace_id, 'venue', venue_data)
  await ctx.state.set(trace_id, 'payment_status', 'pending')
  ```

  </Tab>
</Tabs>

### Type Safety

Define types for your state data to ensure consistency:

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab label="TypeScript">
    
  ```typescript
  interface CustomerData {
    name: string;
    email: string;
  }

  interface VenueData {
    id: string;
    capacity: number;
  }

  type BookingState = {
    customer: CustomerData;
    venue: VenueData;
    status: 'pending' | 'confirmed';
  }

  const booking = await state.get<BookingState>(traceId, 'booking')
  ```

  </Tab>

{' '}
  <Tab label="JavaScript">
  
  ```javascript 
  // Define types or interfaces as needed for documentation clarity (optional in JS) const booking = await
  state.get(traceId, 'booking') // No type casting in JS example 
  ```
  </Tab>

  <Tab label="Python">
    
  ```python
  from dataclasses import dataclass
  from typing import Literal

  @dataclass
  class CustomerData:
      name: str
      email: str

  @dataclass
  class VenueData:
      id: str
      capacity: int

  @dataclass
  class BookingState:
      customer: CustomerData
      venue: VenueData
      status: Literal['pending', 'confirmed']

  booking = await state.get(traceId, 'booking')
  ```

  </Tab>
</Tabs>

### Cleanup

Always clean up state when you're done with it:

<Tabs items={['TypeScript', 'JavaScript', 'Python']}>
  <Tab label="TypeScript">
      
  ```typescript
  export const handler: Handlers['StepName'] = async (input, { state, traceId }) => {
    try {
      await processBooking(input)
      // Clean up specific keys
      await state.delete(traceId, 'booking.customer')
      // Or clean everything
      await state.clear(traceId)
    } catch (error) {
      // Handle errors
    }
  }
  ```
  </Tab>

  <Tab label="JavaScript">
    
  ```javascript
  export const handler = async (input, { state, traceId }) => {
    try {
      await processBooking(input)
      // Clean up specific keys
      await state.delete(traceId, 'booking.customer')
      // Or clean everything
      await state.clear(traceId)
    } catch (error) {
      // Handle errors
    }
  }
  ```
  </Tab>

  <Tab label="Python">
    
  ```python
  async def handler(input, ctx):
      trace_id = ctx.trace_id
      try:
          await process_booking(input)
          # Clean up specific keys
          await ctx.state.delete(trace_id, 'booking.customer')
          # Or clean everything
          await ctx.state.clear(trace_id)
      except Exception as error:
          # Handle errors
          pass
  ```
  </Tab>
</Tabs>

### Performance Considerations

| Consideration    | Description                                                          |
| ---------------- | -------------------------------------------------------------------- |
| Batch Operations | Group related state updates and use atomic operations when possible  |
| State Size       | Keep state data minimal and consider access patterns                 |
| TTL Management   | Set appropriate TTLs based on flow duration and error recovery needs |

### Custom State Adapters

```typescript title="Custom State Adapter Example"
import { StateAdapter } from 'motia'

class CustomStateAdapter extends StateAdapter {
  async get<T>(traceId: string, key: string): Promise<T | null> {
    // Implementation
    return null
  }

  async set<T>(traceId: string, key: string, value: T): Promise<void> {
    // Implementation
  }

  async delete(traceId: string, key: string): Promise<void> {
    // Implementation
  }

  async clear(traceId: string): Promise<void> {
    // Implementation
  }

  async cleanup(): Promise<void> {
    // Implementation
  }
}
```

### Storage Adapters

Motia.dev offers three built-in storage adapters:

- 📁 **File (Default):** Persists state to a JSON file in your project (`.motia/motia.state.json`). No configuration needed for basic use.
- 💾 **Memory:** Stores state in-memory. Fastest option, but state is not persistent across server restarts. Useful for development and non-critical data.
- ⚡ **Redis:** Leverages Redis for persistent and scalable state storage. Ideal for production environments and flows requiring high availability and data durability.

To configure a different state adapter, modify the `config.yml` file in your project root:

```
my-project/
├── config.yml
└── steps/
    ├── step-1.ts
    └── step-2.ts
```

**File Adapter (Default)**

> Default, no configuration required, state is stored into .motia/motia.state.json in your project root

**Memory Adapter**

```yaml title="config.yml"
state:
  adapter: memory
```

> **Warning: Memory Adapter**
> State is stored in-memory and will be lost when the Motia.dev server restarts. Suitable for development and testing.

**Redis Adapter**

```yaml title="config.yml"
state:
  adapter: redis
  host: localhost # Redis server host (e.g., 'localhost' or IP address)
  port: 6379 # Redis server port (default: 6379)
  password: optional # Redis password (if required)
  ttl: 3600 # Optional: State Time-To-Live in seconds (e.g., 3600 seconds = 1 hour)
```

> **Info: Redis Adapter**
> Recommended for production environments. Requires a running Redis server. The `ttl` (Time-To-Live) option is available to automatically expire state data after a specified number of seconds, helping to manage Redis storage.

### Common Issues

| Issue             | Troubleshooting Steps                                                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| State Not Found   | - Verify state adapter configuration\n- Check TTL expiration (Redis)\n- Ensure file permissions (File adapter)\n- **Ensure correct `traceId` is being used in `state.get(traceId, key)` calls.** |
| Persistence       | - Memory adapter: State is lost on process restart\n- File adapter: Check file write permissions\n- Redis: Verify connection and persistence settings                                            |
| Concurrent Access | - Memory/File: Limited concurrent flow support\n- Redis: Use atomic operations and implement retry logic                                                                                         |


-   [streams](/docs/development-guide/streams): Documentation for streams.
---
title: Real-time Streams 
description: Motia Streams are a way to quickly push updates from your asynchronous workflows to the client without having to implement any sort of polling processes.
---

## How it works

You first need to define a stream in your project

### Defining a stream

To be able to use Motia Sockets, you need to define a stream

Create a file called `open-ai.stream.ts` under `steps/` folder

```typescript
import { StreamConfig } from 'motia'
import { z } from 'zod'

export const config: StreamConfig = {
  /**
   * This will be converted in the property on the FlowContext:
   * 
   * context.streams.openai
   */
  name: 'openai',
  /**
   * Schema is important to define the type of the stream, the API
   * generated to interact with this stream will have the structure defined here
   */  
  schema: z.object({ message: z.string() }),

  /**
   * Base config is used to configure the stream
   */
  baseConfig: {
    /**
     * There are two storage types: default and custom
     * Default will use the default storage to store the data.
     * 
     * Custom will use a custom storage, you need to implement 
     * the StateStream class.
     */
    storageType: 'default',
  },
}
```

Once a stream is created, it should be immediately available in FlowContext (make sure to have motia running on the project)

Then you can simply create records using the streams API in your step

```typescript
import { ApiRouteConfig, Handlers } from 'motia'
import { z } from 'zod'

export const config: ApiRouteConfig = {
  type: 'api',
  name: 'OpenAiApi',
  description: 'Call OpenAI',
  path: '/open-ai',
  method: 'POST',
  emits: ['openai-prompt'],
  flows: ['open-ai'],
  bodySchema: z.object({ message: z.string({ description: 'The message to send to OpenAI' }) }),
  responseSchema: {
    200: z.object({ message: z.string({ description: 'The message from OpenAI' }) }) 
  },
}

export const handler: Handlers['OpenAiApi'] = async (req, { traceId, logger, emit, streams }) => {
  logger.info('[Call OpenAI] Received callOpenAi event', { message: req.body.message })

  /**
   * This creates a record with empty message string to be populated in the next step
   */
  const result = await streams.openai.set(traceId, 'message', { message: '' })

  await emit({
    topic: 'openai-prompt',
    data: { message: req.body.message },
  })

  return { status: 200, body: result }
}
```

The previous step just prepares a message to be created by Open AI via OpenAI SDK stream, which will be populated in the next step

```typescript
import { EventConfig, Handlers } from 'motia'
import { OpenAI } from 'openai'
import { z } from 'zod'

export const config: EventConfig = {
  type: 'event',
  name: 'CallOpenAi',
  description: 'Call OpenAI',
  subscribes: ['openai-prompt'],
  emits: [],
  input: z.object({
    message: z.string({ description: 'The message to send to OpenAI' }),
  }),
  flows: ['open-ai'],
}

export const handler: Handlers['CallOpenAi'] = async (input, context) => {
  const { logger, traceId } = context
  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

  logger.info('[Call OpenAI] Received callOpenAi event', input)

  const result = await openai.chat.completions.create({
    messages: [{ role: 'system', content: input.message }],
    model: 'gpt-4o-mini',
    stream: true,
  })

  const messages: string[] = []

  for await (const chunk of result) {
    messages.push(chunk.choices[0].delta.content ?? '')

    /**
     * Now we're populating a previously created message with the streamed data from OpenAI
     */
    await context.streams.openai.set(traceId, 'message', { 
      message: messages.join(''),
    })
  }

  logger.info('[Call OpenAI] OpenAI response', result)
}
```

## Testing Streams in Workbench

We know testing real time events is not easy as a backend developer, so we've added a way to test streams in the Workbench.

Here are the steps to test streams in the Workbench:

1. The API Step that provides a stream item should return the object

```typescript
export const handler: Handlers['OpenAiApi'] = async (req, { traceId, logger, emit, streams }) => {
  logger.info('[Call OpenAI] Received callOpenAi event', { message: req.body.message })

  /**
   * This creates a record with empty message string to be populated in the next step
   */
  const result = await streams.openai.set(traceId, 'message', { message: '' })

  await emit({
    topic: 'openai-prompt',
    data: { message: req.body.message },
  })

  /**
   * Return the entire object received from the create method
   */
  return { status: 200, body: result }
}
```

2. Navigate to [http://localhost:3000/endpoints](http://localhost:3000/endpoints) in your Workbench
3. Open up your endpoint and click on the `Test` button
4. The result will automatically be streamed from the server to the client streaming it's state real-time.

![Stream Test in Workbench](./../img/streams-test-workbench.gif)


## Consuming stream on the browser

```
npm install @motiadev/stream-client-react
```

Then add the provider to the root of your project

```tsx
<MotiaStreamProvider address="ws://localhost:3000">
  ...
</MotiaStreamProvider>
```

then on your component or hook, just use

```typescript
const messageId = '' // get the id back from the API call

// data below will be updated whenever it's updated in the server
const { data } = useStreamItem({ 
  streamName: 'openai',
  groupId: messageId,
  id: 'message'
})
```

-   [testing](/docs/development-guide/testing): Documentation for testing.
---
title: Testing
description: Learn how to write and run tests for your Motia components
---

# Testing

Testing is an essential part of building reliable and maintainable Motia applications. Motia provides built-in support for writing and running tests to ensure the correctness of your steps, flows, and event handling logic.

## Writing Tests for Motia Components

Motia uses [Jest](https://jestjs.io/) as its testing framework. You can write tests for your Motia components using Jest's syntax and assertions.

### Step Tests

To test a step, create a test file with the same name as the step file, but with a `.test.ts` or `.test.js` extension. For example, if your step file is named `my-step.step.ts`, create a test file named `my-step.step.test.ts`.

Here's an example of a step test:

```typescript
// my-step.step.test.ts
import { createTestContext } from '@motiadev/testing'
import { handler } from './my-step.step'

describe('MyStep', () => {
  it('should emit an event with the correct data', async () => {
    const { emit, done } = createTestContext()

    await handler({ name: 'John' }, { emit })

    expect(emit).toHaveBeenCalledWith({
      type: 'my-event',
      data: { greeting: 'Hello, John!' },
    })

    done()
  })
})
```

In this example, we use the `createTestContext` function from `@motiadev/testing` to create a test context with mocked `emit` and `done` functions. We then call the step's `handler` function with test input and the mocked context. Finally, we assert that the `emit` function was called with the expected event type and data.

### Flow Tests

To test a flow, create a test file with the flow name and a `.test.ts` or `.test.js` extension. For example, if your flow is named `my-flow`, create a test file named `my-flow.test.ts`.

Here's an example of a flow test:

```typescript
// my-flow.test.ts
import { createTestFlow } from '@motiadev/testing'
import { handler as stepAHandler } from './step-a.step'
import { handler as stepBHandler } from './step-b.step'

describe('MyFlow', () => {
  it('should execute steps in the correct order', async () => {
    const flow = createTestFlow('my-flow')
      .step('step-a', stepAHandler)
      .step('step-b', stepBHandler)

    const result = await flow.execute({ name: 'Alice' })

    expect(result).toEqual({
      greeting: 'Hello, Alice!',
      message: 'Welcome to Motia!',
    })
  })
})
```

In this example, we use the `createTestFlow` function from `@motiadev/testing` to create a test flow with the specified steps. We then execute the flow with test input and assert that the final result matches the expected output.

## Running Tests Locally

To run tests locally, use the following command:

```bash
pnpm test
```

This command will run all the test files in your project and display the test results in the terminal.

You can also run tests in watch mode, which automatically re-runs the tests whenever you make changes to your code:

```bash
pnpm test --watch
```

## Best Practices

- Write tests for each step and flow to ensure comprehensive coverage.
- Use meaningful test case descriptions to clarify the purpose of each test.
- Test edge cases and error scenarios to ensure your components handle them gracefully.
- Keep your tests focused and independent to make them easier to maintain.
- Use mocks and stubs to isolate dependencies and improve test reliability.

By following these best practices and regularly running tests, you can catch bugs early, maintain code quality, and ensure the reliability of your Motia application. 

-   [ai-content-moderation](/docs/examples/ai-content-moderation): Documentation for ai-content-moderation.
---
title: 'AI Content Moderation'
description: 'Intelligent Content Moderation: Building Human-in-the-Loop Systems with Motia'
---

In today's digital landscape, content moderation is crucial for maintaining safe and appropriate user experiences. Whether you're building a social platform, forum, or any user-generated content system, you need intelligent moderation that can scale with your user base while maintaining human oversight for complex decisions.

This comprehensive guide explores how to build a production-ready content moderation system using Motia's event-driven architecture. We'll cover:

1. **AI-Powered Analysis**: Using OpenAI for text toxicity detection and image safety analysis
2. **Confidence-Based Routing**: Automatically handling clear cases while flagging uncertain content for human review
3. **Slack Integration**: Creating interactive moderation workflows within existing team communication tools
4. **Human-in-the-Loop**: Seamlessly integrating human decision-making into automated processes

Let's build a content moderation system that scales intelligently.

---

## The Power of Intelligent Content Moderation

<div className="my-8">![AI Content Moderation Workflow](./../img/ai-content-moderation-workflow.png)</div>

At its core, our content moderation system solves a fundamental challenge: how do you efficiently moderate user-generated content at scale while maintaining human oversight for complex decisions? Traditional approaches often involve either fully manual processes that don't scale or fully automated systems that lack nuance.

Our Motia-powered solution combines the best of both worlds through intelligent routing:

- **[OpenAI Integration](https://openai.com/)**: Advanced AI analysis for text toxicity and image safety detection
- **[Confidence-Based Routing](https://en.wikipedia.org/wiki/Confidence_interval)**: Automatic handling of clear cases, human review for uncertain content
- **[Slack Integration](https://api.slack.com/)**: Interactive moderation workflows within existing team communication tools
- **[Motia Framework](https://motia.dev)**: Event-driven orchestration with built-in state management and error handling

Instead of a monolithic moderation system, we get a flexible architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our Content Moderation System

Our application consists of six specialized steps, each handling a specific part of the moderation workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="01-content-submit.step.ts" />
  <File name="02-content-analyzer.step.ts" />
  <File name="03-content-router.step.ts" />
  <File name="04-slack-notifier.step.ts" />
  <File name="05-slack-webhook.step.ts" />
  <File name="06-action-executor.step.ts" />
</Folder>

<Tabs items={['content-submit', 'content-analyzer', 'content-router', 'slack-notifier', 'slack-webhook', 'action-executor']}>
  <Tab value="content-submit">
    The entry point for content moderation. This API endpoint receives user-generated content (text and/or images) and initiates the moderation workflow.

    ```typescript
    import { z } from "zod";
    import { ApiRouteConfig, Handlers } from "motia";

    const ContentSubmitInputSchema = z.object({
      text: z.string().optional(),
      imageUrl: z.string().optional(),
      userId: z.string(),
      platform: z.string(),
    });

    export const config: ApiRouteConfig = {
      type: "api",
      name: "ContentSubmitAPI",
      description: "Receives user-generated content for moderation",
      path: "/content/submit",
      method: "POST",
      bodySchema: ContentSubmitInputSchema,
      emits: ["content.submitted"],
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentSubmitAPI"] = async (
      req,
      { logger, emit }
    ) => {
      const { text, imageUrl, userId, platform } = req.body;
      const submissionId = `sub_${Date.now()}_${Math.random()
        .toString(36)
        .slice(2, 11)}`;

      logger.info(`Content submitted for moderation`, {
        submissionId,
        hasText: !!text,
        hasImage: !!imageUrl,
        userId,
        platform,
      });

      await emit({
        topic: "content.submitted",
        data: {
          submissionId,
          text,
          imageUrl,
          userId,
          platform,
          timestamp: new Date().toISOString(),
        },
      });

      return {
        status: 200,
        body: {
          message: "Content submitted for moderation",
          submissionId,
        },
      };
    };
    ```

  </Tab>
  <Tab value="content-analyzer">
    The AI analysis engine that processes both text and image content using OpenAI's advanced models to determine content safety and risk levels.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    export const config: EventConfig = {
      type: "event",
      name: "ContentAnalyzer",
      description: "Analyzes content using OpenAI for toxicity and safety",
      subscribes: ["content.submitted"],
      emits: ["content.analyzed"],
      input: z.object({
        submissionId: z.string(),
        text: z.string().optional(),
        imageUrl: z.string().optional(),
        userId: z.string(),
        platform: z.string(),
        timestamp: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentAnalyzer"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, text, imageUrl, userId } = input;
      
      logger.info("Starting content analysis", { submissionId, hasText: !!text, hasImage: !!imageUrl });

      let textScore = 0;
      let imageScore = 0;
      let textAnalysis = "";
      let imageAnalysis = "";

      // Analyze text content if present
      if (text) {
        try {
          const textResponse = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [
              {
                role: "system",
                content: `You are a content moderation AI. Analyze the following text for toxicity, hate speech, violence, harassment, or inappropriate content. 
                Respond with a JSON object containing:
                - "score": a number between 0-1 where 0 is completely safe and 1 is extremely harmful
                - "analysis": a brief explanation of your assessment
                - "categories": array of detected issues (e.g., ["hate_speech", "violence"])`
              },
              {
                role: "user",
                content: text
              }
            ],
            temperature: 0.1,
          });

          const textResult = JSON.parse(textResponse.choices[0]?.message?.content || "{}");
          textScore = textResult.score || 0;
          textAnalysis = textResult.analysis || "";
        } catch (error) {
          logger.error("Text analysis failed", { error, submissionId });
        }
      }

      // Analyze image content if present
      if (imageUrl) {
        try {
          const imageResponse = await openai.chat.completions.create({
            model: "gpt-4-vision-preview",
            messages: [
              {
                role: "system",
                content: `You are a content moderation AI. Analyze the following image for inappropriate content, violence, nudity, or harmful material.
                Respond with a JSON object containing:
                - "score": a number between 0-1 where 0 is completely safe and 1 is extremely harmful
                - "analysis": a brief explanation of your assessment
                - "categories": array of detected issues (e.g., ["violence", "inappropriate"])`
              },
              {
                role: "user",
                content: [
                  {
                    type: "text",
                    text: "Analyze this image for content moderation:"
                  },
                  {
                    type: "image_url",
                    image_url: { url: imageUrl }
                  }
                ]
              }
            ],
            temperature: 0.1,
          });

          const imageResult = JSON.parse(imageResponse.choices[0]?.message?.content || "{}");
          imageScore = imageResult.score || 0;
          imageAnalysis = imageResult.analysis || "";
        } catch (error) {
          logger.error("Image analysis failed", { error, submissionId });
        }
      }

      // Calculate overall risk score
      const overallScore = Math.max(textScore, imageScore);
      
      const analysisResult = {
        submissionId,
        userId,
        textScore,
        imageScore,
        overallScore,
        textAnalysis,
        imageAnalysis,
        analyzedAt: new Date().toISOString(),
      };

      logger.info("Content analysis completed", {
        submissionId,
        overallScore,
        textScore,
        imageScore,
      });

      await emit({
        topic: "content.analyzed",
        data: analysisResult,
      });
    };
    ```

  </Tab>
  <Tab value="content-router">
    The intelligent routing system that determines whether content should be automatically approved/rejected or sent for human review based on confidence scores.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";

    export const config: EventConfig = {
      type: "event",
      name: "ContentRouter",
      description: "Routes content based on AI analysis confidence scores",
      subscribes: ["content.analyzed"],
      emits: ["content.auto.approved", "content.auto.rejected", "content.needs.review"],
      input: z.object({
        submissionId: z.string(),
        userId: z.string(),
        textScore: z.number(),
        imageScore: z.number(),
        overallScore: z.number(),
        textAnalysis: z.string(),
        imageAnalysis: z.string(),
        analyzedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentRouter"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, userId, overallScore, textAnalysis, imageAnalysis } = input;
      
      logger.info("Routing content based on analysis", { 
        submissionId, 
        overallScore,
        userId 
      });

      let decision: string;
      let routingData = {
        submissionId,
        userId,
        overallScore,
        textAnalysis,
        imageAnalysis,
        routedAt: new Date().toISOString(),
      };

      // Decision logic based on confidence scores
      if (overallScore <= 0.05) {
        // Very low risk - auto approve
        decision = "approved";
        logger.info("Content auto-approved", { submissionId, overallScore });
        
        await emit({
          topic: "content.auto.approved",
          data: {
            ...routingData,
            decision,
            reason: "Low risk score - automatically approved",
          },
        });
        
      } else if (overallScore >= 0.95) {
        // Very high risk - auto reject
        decision = "rejected";
        logger.info("Content auto-rejected", { submissionId, overallScore });
        
        await emit({
          topic: "content.auto.rejected",
          data: {
            ...routingData,
            decision,
            reason: "High risk score - automatically rejected",
          },
        });
        
      } else {
        // Medium risk - needs human review
        decision = "review";
        logger.info("Content needs human review", { submissionId, overallScore });
        
        await emit({
          topic: "content.needs.review",
          data: {
            ...routingData,
            decision,
            reason: "Medium risk score - requires human review",
            priority: overallScore >= 0.7 ? "high" : overallScore >= 0.5 ? "medium" : "low",
          },
        });
      }
    };
    ```

  </Tab>
  <Tab value="slack-notifier">
    Creates interactive Slack messages for human moderators with approve/reject/escalate buttons and contextual information.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";
    import { WebClient } from "@slack/web-api";

    const slack = new WebClient(process.env.SLACK_BOT_TOKEN);

    export const config: EventConfig = {
      type: "event",
      name: "SlackNotifier",
      description: "Sends interactive Slack messages for human review",
      subscribes: ["content.needs.review"],
      emits: ["slack.notification.sent"],
      input: z.object({
        submissionId: z.string(),
        userId: z.string(),
        overallScore: z.number(),
        textAnalysis: z.string(),
        imageAnalysis: z.string(),
        decision: z.string(),
        reason: z.string(),
        priority: z.enum(["low", "medium", "high"]),
        routedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["SlackNotifier"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, userId, overallScore, textAnalysis, imageAnalysis, priority } = input;
      
      logger.info("Sending Slack notification for review", { 
        submissionId, 
        priority,
        userId 
      });

      // Determine channel based on priority
      let channel: string;
      switch (priority) {
        case "high":
          channel = process.env.SLACK_CHANNEL_URGENT!;
          break;
        case "medium":
          channel = process.env.SLACK_CHANNEL_ESCALATED!;
          break;
        default:
          channel = process.env.SLACK_CHANNEL_MODERATION!;
      }

      // Create interactive message with buttons
      const message = {
        channel,
        text: `Content Moderation Review Required`,
        blocks: [
          {
            type: "header",
            text: {
              type: "plain_text",
              text: `🚨 Content Review - ${priority.toUpperCase()} Priority`,
            },
          },
          {
            type: "section",
            fields: [
              {
                type: "mrkdwn",
                text: `*Submission ID:*\n${submissionId}`,
              },
              {
                type: "mrkdwn",
                text: `*User ID:*\n${userId}`,
              },
              {
                type: "mrkdwn",
                text: `*Risk Score:*\n${(overallScore * 100).toFixed(1)}%`,
              },
              {
                type: "mrkdwn",
                text: `*Priority:*\n${priority.toUpperCase()}`,
              },
            ],
          },
          {
            type: "section",
            text: {
              type: "mrkdwn",
              text: `*AI Analysis:*\n${textAnalysis || imageAnalysis || "No analysis available"}`,
            },
          },
          {
            type: "actions",
            elements: [
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "✅ Approve",
                },
                style: "primary",
                action_id: "approve_content",
                value: submissionId,
              },
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "❌ Reject",
                },
                style: "danger",
                action_id: "reject_content",
                value: submissionId,
              },
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "⚠️ Escalate",
                },
                action_id: "escalate_content",
                value: submissionId,
              },
            ],
          },
        ],
      };

      try {
        const result = await slack.chat.postMessage(message);
        
        logger.info("Slack notification sent successfully", {
          submissionId,
          channel,
          messageTs: result.ts,
        });

        await emit({
          topic: "slack.notification.sent",
          data: {
            submissionId,
            userId,
            channel,
            messageTs: result.ts,
            priority,
            sentAt: new Date().toISOString(),
          },
        });

      } catch (error) {
        logger.error("Failed to send Slack notification", {
          error,
          submissionId,
          channel,
        });
        throw error;
      }
    };
    ```

  </Tab>
  <Tab value="slack-webhook">
    Handles interactive button responses from Slack, processing approve/reject/escalate decisions from human moderators.

    ```typescript
    import { z } from "zod";
    import { ApiRouteConfig, Handlers } from "motia";
    import { createHmac } from "crypto";

    export const config: ApiRouteConfig = {
      type: "api",
      name: "SlackWebhook",
      description: "Handles Slack interactive button responses",
      path: "/slack/webhook",
      method: "POST",
      emits: ["slack.decision.received"],
      flows: ["content-moderation"],
    };

    export const handler: Handlers["SlackWebhook"] = async (
      req,
      { logger, emit }
    ) => {
      // Verify Slack signature
      const signature = req.headers["x-slack-signature"] as string;
      const timestamp = req.headers["x-slack-request-timestamp"] as string;
      const body = req.body;

      if (!verifySlackSignature(signature, timestamp, body)) {
        logger.error("Invalid Slack signature");
        return { status: 401, body: { error: "Unauthorized" } };
      }

      const payload = JSON.parse(body.payload);
      const { actions, user, message } = payload;

      if (!actions || actions.length === 0) {
        return { status: 200, body: { text: "No action received" } };
      }

      const action = actions[0];
      const submissionId = action.value;
      const decision = action.action_id.replace("_content", "");
      const moderatorId = user.id;
      const moderatorName = user.name;

      logger.info("Slack decision received", {
        submissionId,
        decision,
        moderatorId,
        moderatorName,
      });

      await emit({
        topic: "slack.decision.received",
        data: {
          submissionId,
          decision,
          moderatorId,
          moderatorName,
          messageTs: message.ts,
          decidedAt: new Date().toISOString(),
        },
      });

      // Update the original message to show decision
      const responseMessage = `✅ Decision recorded: ${decision.toUpperCase()} by ${moderatorName}`;
      
      return {
        status: 200,
        body: {
          text: responseMessage,
          replace_original: false,
        },
      };
    };

    function verifySlackSignature(signature: string, timestamp: string, body: string): boolean {
      const signingSecret = process.env.SLACK_SIGNING_SECRET!;
      const baseString = `v0:${timestamp}:${body}`;
      const expectedSignature = `v0=${createHmac("sha256", signingSecret)
        .update(baseString)
        .digest("hex")}`;
      
      return signature === expectedSignature;
    }
    ```

  </Tab>
  <Tab value="action-executor">
    Executes the final moderation decisions, handling both automated and human-reviewed content with comprehensive logging and state management.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";

    export const config: EventConfig = {
      type: "event",
      name: "ActionExecutor",
      description: "Executes final moderation decisions",
      subscribes: ["content.auto.approved", "content.auto.rejected", "slack.decision.received"],
      emits: ["content.moderation.completed"],
      input: z.object({
        submissionId: z.string(),
        decision: z.enum(["approved", "rejected", "escalated"]),
        reason: z.string(),
        moderatorId: z.string().optional(),
        moderatorName: z.string().optional(),
        decidedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ActionExecutor"] = async (
      input,
      { logger, emit, state }
    ) => {
      const { submissionId, decision, reason, moderatorId, moderatorName, decidedAt } = input;
      
      logger.info("Executing moderation decision", {
        submissionId,
        decision,
        moderatorId,
        moderatorName,
      });

      // Store the final decision in state
      const moderationRecord = {
        submissionId,
        decision,
        reason,
        moderatorId,
        moderatorName,
        decidedAt,
        executedAt: new Date().toISOString(),
      };

      await state.set("moderation", submissionId, moderationRecord);

      // Execute the appropriate action based on decision
      switch (decision) {
        case "approved":
          logger.info("Content approved", { submissionId });
          // Here you would typically:
          // - Make content visible to users
          // - Send approval notification to user
          // - Update content status in database
          break;

        case "rejected":
          logger.info("Content rejected", { submissionId });
          // Here you would typically:
          // - Hide or remove content
          // - Send rejection notification to user
          // - Log for potential user action
          break;

        case "escalated":
          logger.info("Content escalated", { submissionId });
          // Here you would typically:
          // - Send to higher-level moderators
          // - Create support ticket
          // - Flag for additional review
          break;
      }

      await emit({
        topic: "content.moderation.completed",
        data: moderationRecord,
      });

      logger.info("Moderation decision executed successfully", {
        submissionId,
        decision,
        moderatorId,
      });
    };
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your content moderation pipeline, making it easy to understand the flow and monitor moderation decisions in real-time.

<div className="my-8">![AI Content Moderation Workflow](./../img/ai-content-moderation-workflow.png)</div>

You can monitor real-time content analysis, view Slack notifications, and trace the execution of each moderation decision directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monolithic moderation systems.

## Human-in-the-Loop Workflow Demo

Let's see the complete human-in-the-loop process in action using a real example. We'll submit problematic content and watch it flow through the moderation pipeline.

### Step 1: Submit Content for Moderation

Submit the sample content that should trigger human review:

```shell
curl -X POST http://localhost:3000/content/submit \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I hate this stupid garbage, it\'s complete trash and makes me want to hurt someone",
    "userId": "user456",
    "platform": "web"
  }'
```

### Step 2: AI Analysis & Routing

The system will:
1. **Analyze the content** using OpenAI's GPT-4 for toxicity detection
2. **Calculate risk scores** based on detected harmful content
3. **Route for human review** since the content contains hate speech and violence references

You'll see logs like:
```
Content submitted for moderation: submissionId=sub_123, hasText=true, userId=user456
Starting content analysis: submissionId=sub_123, hasText=true
Content analysis completed: submissionId=sub_123, overallScore=0.87, textScore=0.87
Content needs human review: submissionId=sub_123, overallScore=0.87
```

### Step 3: Slack Notification for Human Review

The system automatically sends an interactive message to your moderation team in Slack:

<div className="my-8">![AI Content Moderation Slack Output](./../img/ai-content-moderation-slack-output.png)</div>

The Slack message includes:
- **Risk score**: 87% confidence of harmful content
- **Priority level**: HIGH (since score ≥ 70%)
- **AI analysis**: Detailed breakdown of detected issues
- **Interactive buttons**: Approve, Reject, or Escalate options

### Step 4: Human Decision & Execution

When a moderator clicks a button in Slack:
1. **Decision is recorded** with moderator attribution
2. **Content is processed** according to the decision
3. **User is notified** of the moderation outcome
4. **Audit trail is maintained** for compliance

The complete workflow demonstrates how AI handles the initial analysis while humans provide the final judgment for nuanced decisions.

---

## Key Features & Benefits

### 🤖 **AI-Powered Analysis**
Advanced OpenAI integration for both text toxicity detection and image safety analysis with confidence scoring.

### 🎯 **Intelligent Routing**
Confidence-based decision making that automatically handles clear cases while flagging uncertain content for human review.

### 💬 **Slack Integration**
Interactive moderation workflows within existing team communication tools - no custom dashboard required.

### 👥 **Human-in-the-Loop**
Seamless integration of human decision-making with approve/reject/escalate buttons and contextual information.

### 📊 **Priority-Based Routing**
Content is routed to different Slack channels based on risk level and urgency.

### 🔒 **Security & Compliance**
Built-in signature verification, audit trails, and comprehensive logging for compliance requirements.

---

## Getting Started

Ready to build your own intelligent content moderation system? Here's how to set it up and run it.

<Steps>

### 1. Install Dependencies

Install the necessary npm packages and set up the development environment.

```shell
npm install
```

### 2. Configure Environment Variables

Create a `.env` file with your API keys and Slack configuration:

```shell
# Required: OpenAI API key for content analysis
OPENAI_API_KEY="sk-..."

# Required: Slack bot configuration
SLACK_BOT_TOKEN="xoxb-your-bot-token"
SLACK_SIGNING_SECRET="your-signing-secret"

# Required: Slack channels for different priority levels
SLACK_CHANNEL_MODERATION="C1234567890"  # Normal priority
SLACK_CHANNEL_URGENT="C0987654321"      # High priority
SLACK_CHANNEL_ESCALATED="C1122334455"   # Escalated content
```

### 3. Set Up Slack Integration

1. Create a Slack app with the following permissions:
   - `chat:write` - Send messages to channels
   - `channels:read` - Access channel information
2. Enable Interactive Components and set webhook URL to: `https://your-domain.com/slack/webhook`
3. Install the app to your workspace
4. Copy the bot token and signing secret to your `.env` file

### 4. Run the Moderation System

Start the Motia development server to begin processing content.

```shell
npm run dev
```

</Steps>

---

## Advanced Configuration

### Adjusting Confidence Thresholds

Modify the decision thresholds in the content router step:

```typescript
// In 03-content-router.step.ts
if (overallScore <= 0.05) {
  decision = "approved"; // Auto-approve threshold (5%)
} else if (overallScore >= 0.95) {
  decision = "rejected"; // Auto-reject threshold (95%)
} else {
  decision = "review"; // Human review range (5-95%)
}
```

### Custom Channel Routing

Implement custom routing logic based on content type or user behavior:

```typescript
// Route based on user history or content type
const channel = getChannelForContent(contentType, userHistory, riskScore);
```

### Integration with External Systems

Extend the action executor to integrate with your existing systems:

```typescript
// In 06-action-executor.step.ts
case "approved":
  await publishContent(submissionId);
  await notifyUser(userId, "Your content has been approved");
  break;
```

---

## 💻 Dive into the Code

Want to explore the complete content moderation implementation? Check out the full source code, including all steps, Slack integration, and production-ready configuration:

<div className="not-prose">
  <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete Content Moderation System</h3>
        <p className="text-gray-600 mb-4">Access the full implementation with AI analysis, Slack integration, and human-in-the-loop workflows.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/ai-content-moderation" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Content Moderation Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Intelligent Content Moderation at Scale

This content moderation system demonstrates the power of combining AI analysis with human oversight in an event-driven architecture. By breaking down moderation into discrete, specialized components, we've created a system that's not only intelligent but also flexible and maintainable.

The human-in-the-loop approach means you can:
- **Scale efficiently**: Automatically handle 80-90% of content while maintaining quality
- **Adapt quickly**: Adjust thresholds and routing logic without system changes
- **Maintain oversight**: Human moderators focus on complex cases that require judgment
- **Integrate seamlessly**: Use existing team communication tools like Slack

Key architectural benefits:
- **Intelligent routing**: Confidence-based decisions reduce human workload
- **Flexible integration**: Works with any team communication platform
- **Audit compliance**: Complete decision trails and moderator attribution
- **Scalable architecture**: Each component can be scaled independently

From here, you can extend the system by:
- Adding support for video content moderation
- Implementing custom AI models for specific content types
- Building analytics dashboards for moderation insights
- Integrating with user management and content management systems
- Adding escalation policies and moderator workflows

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing moderation pipeline.

Ready to build content moderation that scales with your platform? Start building with Motia today!



## Examples
[ai-content-moderation](/docs/examples/ai-content-moderation): Code example
---
title: 'AI Content Moderation'
description: 'Intelligent Content Moderation: Building Human-in-the-Loop Systems with Motia'
---

In today's digital landscape, content moderation is crucial for maintaining safe and appropriate user experiences. Whether you're building a social platform, forum, or any user-generated content system, you need intelligent moderation that can scale with your user base while maintaining human oversight for complex decisions.

This comprehensive guide explores how to build a production-ready content moderation system using Motia's event-driven architecture. We'll cover:

1. **AI-Powered Analysis**: Using OpenAI for text toxicity detection and image safety analysis
2. **Confidence-Based Routing**: Automatically handling clear cases while flagging uncertain content for human review
3. **Slack Integration**: Creating interactive moderation workflows within existing team communication tools
4. **Human-in-the-Loop**: Seamlessly integrating human decision-making into automated processes

Let's build a content moderation system that scales intelligently.

---

## The Power of Intelligent Content Moderation

<div className="my-8">![AI Content Moderation Workflow](./../img/ai-content-moderation-workflow.png)</div>

At its core, our content moderation system solves a fundamental challenge: how do you efficiently moderate user-generated content at scale while maintaining human oversight for complex decisions? Traditional approaches often involve either fully manual processes that don't scale or fully automated systems that lack nuance.

Our Motia-powered solution combines the best of both worlds through intelligent routing:

- **[OpenAI Integration](https://openai.com/)**: Advanced AI analysis for text toxicity and image safety detection
- **[Confidence-Based Routing](https://en.wikipedia.org/wiki/Confidence_interval)**: Automatic handling of clear cases, human review for uncertain content
- **[Slack Integration](https://api.slack.com/)**: Interactive moderation workflows within existing team communication tools
- **[Motia Framework](https://motia.dev)**: Event-driven orchestration with built-in state management and error handling

Instead of a monolithic moderation system, we get a flexible architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our Content Moderation System

Our application consists of six specialized steps, each handling a specific part of the moderation workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="01-content-submit.step.ts" />
  <File name="02-content-analyzer.step.ts" />
  <File name="03-content-router.step.ts" />
  <File name="04-slack-notifier.step.ts" />
  <File name="05-slack-webhook.step.ts" />
  <File name="06-action-executor.step.ts" />
</Folder>

<Tabs items={['content-submit', 'content-analyzer', 'content-router', 'slack-notifier', 'slack-webhook', 'action-executor']}>
  <Tab value="content-submit">
    The entry point for content moderation. This API endpoint receives user-generated content (text and/or images) and initiates the moderation workflow.

    ```typescript
    import { z } from "zod";
    import { ApiRouteConfig, Handlers } from "motia";

    const ContentSubmitInputSchema = z.object({
      text: z.string().optional(),
      imageUrl: z.string().optional(),
      userId: z.string(),
      platform: z.string(),
    });

    export const config: ApiRouteConfig = {
      type: "api",
      name: "ContentSubmitAPI",
      description: "Receives user-generated content for moderation",
      path: "/content/submit",
      method: "POST",
      bodySchema: ContentSubmitInputSchema,
      emits: ["content.submitted"],
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentSubmitAPI"] = async (
      req,
      { logger, emit }
    ) => {
      const { text, imageUrl, userId, platform } = req.body;
      const submissionId = `sub_${Date.now()}_${Math.random()
        .toString(36)
        .slice(2, 11)}`;

      logger.info(`Content submitted for moderation`, {
        submissionId,
        hasText: !!text,
        hasImage: !!imageUrl,
        userId,
        platform,
      });

      await emit({
        topic: "content.submitted",
        data: {
          submissionId,
          text,
          imageUrl,
          userId,
          platform,
          timestamp: new Date().toISOString(),
        },
      });

      return {
        status: 200,
        body: {
          message: "Content submitted for moderation",
          submissionId,
        },
      };
    };
    ```

  </Tab>
  <Tab value="content-analyzer">
    The AI analysis engine that processes both text and image content using OpenAI's advanced models to determine content safety and risk levels.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    export const config: EventConfig = {
      type: "event",
      name: "ContentAnalyzer",
      description: "Analyzes content using OpenAI for toxicity and safety",
      subscribes: ["content.submitted"],
      emits: ["content.analyzed"],
      input: z.object({
        submissionId: z.string(),
        text: z.string().optional(),
        imageUrl: z.string().optional(),
        userId: z.string(),
        platform: z.string(),
        timestamp: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentAnalyzer"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, text, imageUrl, userId } = input;
      
      logger.info("Starting content analysis", { submissionId, hasText: !!text, hasImage: !!imageUrl });

      let textScore = 0;
      let imageScore = 0;
      let textAnalysis = "";
      let imageAnalysis = "";

      // Analyze text content if present
      if (text) {
        try {
          const textResponse = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [
              {
                role: "system",
                content: `You are a content moderation AI. Analyze the following text for toxicity, hate speech, violence, harassment, or inappropriate content. 
                Respond with a JSON object containing:
                - "score": a number between 0-1 where 0 is completely safe and 1 is extremely harmful
                - "analysis": a brief explanation of your assessment
                - "categories": array of detected issues (e.g., ["hate_speech", "violence"])`
              },
              {
                role: "user",
                content: text
              }
            ],
            temperature: 0.1,
          });

          const textResult = JSON.parse(textResponse.choices[0]?.message?.content || "{}");
          textScore = textResult.score || 0;
          textAnalysis = textResult.analysis || "";
        } catch (error) {
          logger.error("Text analysis failed", { error, submissionId });
        }
      }

      // Analyze image content if present
      if (imageUrl) {
        try {
          const imageResponse = await openai.chat.completions.create({
            model: "gpt-4-vision-preview",
            messages: [
              {
                role: "system",
                content: `You are a content moderation AI. Analyze the following image for inappropriate content, violence, nudity, or harmful material.
                Respond with a JSON object containing:
                - "score": a number between 0-1 where 0 is completely safe and 1 is extremely harmful
                - "analysis": a brief explanation of your assessment
                - "categories": array of detected issues (e.g., ["violence", "inappropriate"])`
              },
              {
                role: "user",
                content: [
                  {
                    type: "text",
                    text: "Analyze this image for content moderation:"
                  },
                  {
                    type: "image_url",
                    image_url: { url: imageUrl }
                  }
                ]
              }
            ],
            temperature: 0.1,
          });

          const imageResult = JSON.parse(imageResponse.choices[0]?.message?.content || "{}");
          imageScore = imageResult.score || 0;
          imageAnalysis = imageResult.analysis || "";
        } catch (error) {
          logger.error("Image analysis failed", { error, submissionId });
        }
      }

      // Calculate overall risk score
      const overallScore = Math.max(textScore, imageScore);
      
      const analysisResult = {
        submissionId,
        userId,
        textScore,
        imageScore,
        overallScore,
        textAnalysis,
        imageAnalysis,
        analyzedAt: new Date().toISOString(),
      };

      logger.info("Content analysis completed", {
        submissionId,
        overallScore,
        textScore,
        imageScore,
      });

      await emit({
        topic: "content.analyzed",
        data: analysisResult,
      });
    };
    ```

  </Tab>
  <Tab value="content-router">
    The intelligent routing system that determines whether content should be automatically approved/rejected or sent for human review based on confidence scores.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";

    export const config: EventConfig = {
      type: "event",
      name: "ContentRouter",
      description: "Routes content based on AI analysis confidence scores",
      subscribes: ["content.analyzed"],
      emits: ["content.auto.approved", "content.auto.rejected", "content.needs.review"],
      input: z.object({
        submissionId: z.string(),
        userId: z.string(),
        textScore: z.number(),
        imageScore: z.number(),
        overallScore: z.number(),
        textAnalysis: z.string(),
        imageAnalysis: z.string(),
        analyzedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ContentRouter"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, userId, overallScore, textAnalysis, imageAnalysis } = input;
      
      logger.info("Routing content based on analysis", { 
        submissionId, 
        overallScore,
        userId 
      });

      let decision: string;
      let routingData = {
        submissionId,
        userId,
        overallScore,
        textAnalysis,
        imageAnalysis,
        routedAt: new Date().toISOString(),
      };

      // Decision logic based on confidence scores
      if (overallScore <= 0.05) {
        // Very low risk - auto approve
        decision = "approved";
        logger.info("Content auto-approved", { submissionId, overallScore });
        
        await emit({
          topic: "content.auto.approved",
          data: {
            ...routingData,
            decision,
            reason: "Low risk score - automatically approved",
          },
        });
        
      } else if (overallScore >= 0.95) {
        // Very high risk - auto reject
        decision = "rejected";
        logger.info("Content auto-rejected", { submissionId, overallScore });
        
        await emit({
          topic: "content.auto.rejected",
          data: {
            ...routingData,
            decision,
            reason: "High risk score - automatically rejected",
          },
        });
        
      } else {
        // Medium risk - needs human review
        decision = "review";
        logger.info("Content needs human review", { submissionId, overallScore });
        
        await emit({
          topic: "content.needs.review",
          data: {
            ...routingData,
            decision,
            reason: "Medium risk score - requires human review",
            priority: overallScore >= 0.7 ? "high" : overallScore >= 0.5 ? "medium" : "low",
          },
        });
      }
    };
    ```

  </Tab>
  <Tab value="slack-notifier">
    Creates interactive Slack messages for human moderators with approve/reject/escalate buttons and contextual information.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";
    import { WebClient } from "@slack/web-api";

    const slack = new WebClient(process.env.SLACK_BOT_TOKEN);

    export const config: EventConfig = {
      type: "event",
      name: "SlackNotifier",
      description: "Sends interactive Slack messages for human review",
      subscribes: ["content.needs.review"],
      emits: ["slack.notification.sent"],
      input: z.object({
        submissionId: z.string(),
        userId: z.string(),
        overallScore: z.number(),
        textAnalysis: z.string(),
        imageAnalysis: z.string(),
        decision: z.string(),
        reason: z.string(),
        priority: z.enum(["low", "medium", "high"]),
        routedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["SlackNotifier"] = async (
      input,
      { logger, emit }
    ) => {
      const { submissionId, userId, overallScore, textAnalysis, imageAnalysis, priority } = input;
      
      logger.info("Sending Slack notification for review", { 
        submissionId, 
        priority,
        userId 
      });

      // Determine channel based on priority
      let channel: string;
      switch (priority) {
        case "high":
          channel = process.env.SLACK_CHANNEL_URGENT!;
          break;
        case "medium":
          channel = process.env.SLACK_CHANNEL_ESCALATED!;
          break;
        default:
          channel = process.env.SLACK_CHANNEL_MODERATION!;
      }

      // Create interactive message with buttons
      const message = {
        channel,
        text: `Content Moderation Review Required`,
        blocks: [
          {
            type: "header",
            text: {
              type: "plain_text",
              text: `🚨 Content Review - ${priority.toUpperCase()} Priority`,
            },
          },
          {
            type: "section",
            fields: [
              {
                type: "mrkdwn",
                text: `*Submission ID:*\n${submissionId}`,
              },
              {
                type: "mrkdwn",
                text: `*User ID:*\n${userId}`,
              },
              {
                type: "mrkdwn",
                text: `*Risk Score:*\n${(overallScore * 100).toFixed(1)}%`,
              },
              {
                type: "mrkdwn",
                text: `*Priority:*\n${priority.toUpperCase()}`,
              },
            ],
          },
          {
            type: "section",
            text: {
              type: "mrkdwn",
              text: `*AI Analysis:*\n${textAnalysis || imageAnalysis || "No analysis available"}`,
            },
          },
          {
            type: "actions",
            elements: [
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "✅ Approve",
                },
                style: "primary",
                action_id: "approve_content",
                value: submissionId,
              },
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "❌ Reject",
                },
                style: "danger",
                action_id: "reject_content",
                value: submissionId,
              },
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "⚠️ Escalate",
                },
                action_id: "escalate_content",
                value: submissionId,
              },
            ],
          },
        ],
      };

      try {
        const result = await slack.chat.postMessage(message);
        
        logger.info("Slack notification sent successfully", {
          submissionId,
          channel,
          messageTs: result.ts,
        });

        await emit({
          topic: "slack.notification.sent",
          data: {
            submissionId,
            userId,
            channel,
            messageTs: result.ts,
            priority,
            sentAt: new Date().toISOString(),
          },
        });

      } catch (error) {
        logger.error("Failed to send Slack notification", {
          error,
          submissionId,
          channel,
        });
        throw error;
      }
    };
    ```

  </Tab>
  <Tab value="slack-webhook">
    Handles interactive button responses from Slack, processing approve/reject/escalate decisions from human moderators.

    ```typescript
    import { z } from "zod";
    import { ApiRouteConfig, Handlers } from "motia";
    import { createHmac } from "crypto";

    export const config: ApiRouteConfig = {
      type: "api",
      name: "SlackWebhook",
      description: "Handles Slack interactive button responses",
      path: "/slack/webhook",
      method: "POST",
      emits: ["slack.decision.received"],
      flows: ["content-moderation"],
    };

    export const handler: Handlers["SlackWebhook"] = async (
      req,
      { logger, emit }
    ) => {
      // Verify Slack signature
      const signature = req.headers["x-slack-signature"] as string;
      const timestamp = req.headers["x-slack-request-timestamp"] as string;
      const body = req.body;

      if (!verifySlackSignature(signature, timestamp, body)) {
        logger.error("Invalid Slack signature");
        return { status: 401, body: { error: "Unauthorized" } };
      }

      const payload = JSON.parse(body.payload);
      const { actions, user, message } = payload;

      if (!actions || actions.length === 0) {
        return { status: 200, body: { text: "No action received" } };
      }

      const action = actions[0];
      const submissionId = action.value;
      const decision = action.action_id.replace("_content", "");
      const moderatorId = user.id;
      const moderatorName = user.name;

      logger.info("Slack decision received", {
        submissionId,
        decision,
        moderatorId,
        moderatorName,
      });

      await emit({
        topic: "slack.decision.received",
        data: {
          submissionId,
          decision,
          moderatorId,
          moderatorName,
          messageTs: message.ts,
          decidedAt: new Date().toISOString(),
        },
      });

      // Update the original message to show decision
      const responseMessage = `✅ Decision recorded: ${decision.toUpperCase()} by ${moderatorName}`;
      
      return {
        status: 200,
        body: {
          text: responseMessage,
          replace_original: false,
        },
      };
    };

    function verifySlackSignature(signature: string, timestamp: string, body: string): boolean {
      const signingSecret = process.env.SLACK_SIGNING_SECRET!;
      const baseString = `v0:${timestamp}:${body}`;
      const expectedSignature = `v0=${createHmac("sha256", signingSecret)
        .update(baseString)
        .digest("hex")}`;
      
      return signature === expectedSignature;
    }
    ```

  </Tab>
  <Tab value="action-executor">
    Executes the final moderation decisions, handling both automated and human-reviewed content with comprehensive logging and state management.

    ```typescript
    import { z } from "zod";
    import { EventConfig, Handlers } from "motia";

    export const config: EventConfig = {
      type: "event",
      name: "ActionExecutor",
      description: "Executes final moderation decisions",
      subscribes: ["content.auto.approved", "content.auto.rejected", "slack.decision.received"],
      emits: ["content.moderation.completed"],
      input: z.object({
        submissionId: z.string(),
        decision: z.enum(["approved", "rejected", "escalated"]),
        reason: z.string(),
        moderatorId: z.string().optional(),
        moderatorName: z.string().optional(),
        decidedAt: z.string(),
      }),
      flows: ["content-moderation"],
    };

    export const handler: Handlers["ActionExecutor"] = async (
      input,
      { logger, emit, state }
    ) => {
      const { submissionId, decision, reason, moderatorId, moderatorName, decidedAt } = input;
      
      logger.info("Executing moderation decision", {
        submissionId,
        decision,
        moderatorId,
        moderatorName,
      });

      // Store the final decision in state
      const moderationRecord = {
        submissionId,
        decision,
        reason,
        moderatorId,
        moderatorName,
        decidedAt,
        executedAt: new Date().toISOString(),
      };

      await state.set("moderation", submissionId, moderationRecord);

      // Execute the appropriate action based on decision
      switch (decision) {
        case "approved":
          logger.info("Content approved", { submissionId });
          // Here you would typically:
          // - Make content visible to users
          // - Send approval notification to user
          // - Update content status in database
          break;

        case "rejected":
          logger.info("Content rejected", { submissionId });
          // Here you would typically:
          // - Hide or remove content
          // - Send rejection notification to user
          // - Log for potential user action
          break;

        case "escalated":
          logger.info("Content escalated", { submissionId });
          // Here you would typically:
          // - Send to higher-level moderators
          // - Create support ticket
          // - Flag for additional review
          break;
      }

      await emit({
        topic: "content.moderation.completed",
        data: moderationRecord,
      });

      logger.info("Moderation decision executed successfully", {
        submissionId,
        decision,
        moderatorId,
      });
    };
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your content moderation pipeline, making it easy to understand the flow and monitor moderation decisions in real-time.

<div className="my-8">![AI Content Moderation Workflow](./../img/ai-content-moderation-workflow.png)</div>

You can monitor real-time content analysis, view Slack notifications, and trace the execution of each moderation decision directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monolithic moderation systems.

## Human-in-the-Loop Workflow Demo

Let's see the complete human-in-the-loop process in action using a real example. We'll submit problematic content and watch it flow through the moderation pipeline.

### Step 1: Submit Content for Moderation

Submit the sample content that should trigger human review:

```shell
curl -X POST http://localhost:3000/content/submit \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I hate this stupid garbage, it\'s complete trash and makes me want to hurt someone",
    "userId": "user456",
    "platform": "web"
  }'
```

### Step 2: AI Analysis & Routing

The system will:
1. **Analyze the content** using OpenAI's GPT-4 for toxicity detection
2. **Calculate risk scores** based on detected harmful content
3. **Route for human review** since the content contains hate speech and violence references

You'll see logs like:
```
Content submitted for moderation: submissionId=sub_123, hasText=true, userId=user456
Starting content analysis: submissionId=sub_123, hasText=true
Content analysis completed: submissionId=sub_123, overallScore=0.87, textScore=0.87
Content needs human review: submissionId=sub_123, overallScore=0.87
```

### Step 3: Slack Notification for Human Review

The system automatically sends an interactive message to your moderation team in Slack:

<div className="my-8">![AI Content Moderation Slack Output](./../img/ai-content-moderation-slack-output.png)</div>

The Slack message includes:
- **Risk score**: 87% confidence of harmful content
- **Priority level**: HIGH (since score ≥ 70%)
- **AI analysis**: Detailed breakdown of detected issues
- **Interactive buttons**: Approve, Reject, or Escalate options

### Step 4: Human Decision & Execution

When a moderator clicks a button in Slack:
1. **Decision is recorded** with moderator attribution
2. **Content is processed** according to the decision
3. **User is notified** of the moderation outcome
4. **Audit trail is maintained** for compliance

The complete workflow demonstrates how AI handles the initial analysis while humans provide the final judgment for nuanced decisions.

---

## Key Features & Benefits

### 🤖 **AI-Powered Analysis**
Advanced OpenAI integration for both text toxicity detection and image safety analysis with confidence scoring.

### 🎯 **Intelligent Routing**
Confidence-based decision making that automatically handles clear cases while flagging uncertain content for human review.

### 💬 **Slack Integration**
Interactive moderation workflows within existing team communication tools - no custom dashboard required.

### 👥 **Human-in-the-Loop**
Seamless integration of human decision-making with approve/reject/escalate buttons and contextual information.

### 📊 **Priority-Based Routing**
Content is routed to different Slack channels based on risk level and urgency.

### 🔒 **Security & Compliance**
Built-in signature verification, audit trails, and comprehensive logging for compliance requirements.

---

## Getting Started

Ready to build your own intelligent content moderation system? Here's how to set it up and run it.

<Steps>

### 1. Install Dependencies

Install the necessary npm packages and set up the development environment.

```shell
npm install
```

### 2. Configure Environment Variables

Create a `.env` file with your API keys and Slack configuration:

```shell
# Required: OpenAI API key for content analysis
OPENAI_API_KEY="sk-..."

# Required: Slack bot configuration
SLACK_BOT_TOKEN="xoxb-your-bot-token"
SLACK_SIGNING_SECRET="your-signing-secret"

# Required: Slack channels for different priority levels
SLACK_CHANNEL_MODERATION="C1234567890"  # Normal priority
SLACK_CHANNEL_URGENT="C0987654321"      # High priority
SLACK_CHANNEL_ESCALATED="C1122334455"   # Escalated content
```

### 3. Set Up Slack Integration

1. Create a Slack app with the following permissions:
   - `chat:write` - Send messages to channels
   - `channels:read` - Access channel information
2. Enable Interactive Components and set webhook URL to: `https://your-domain.com/slack/webhook`
3. Install the app to your workspace
4. Copy the bot token and signing secret to your `.env` file

### 4. Run the Moderation System

Start the Motia development server to begin processing content.

```shell
npm run dev
```

</Steps>

---

## Advanced Configuration

### Adjusting Confidence Thresholds

Modify the decision thresholds in the content router step:

```typescript
// In 03-content-router.step.ts
if (overallScore <= 0.05) {
  decision = "approved"; // Auto-approve threshold (5%)
} else if (overallScore >= 0.95) {
  decision = "rejected"; // Auto-reject threshold (95%)
} else {
  decision = "review"; // Human review range (5-95%)
}
```

### Custom Channel Routing

Implement custom routing logic based on content type or user behavior:

```typescript
// Route based on user history or content type
const channel = getChannelForContent(contentType, userHistory, riskScore);
```

### Integration with External Systems

Extend the action executor to integrate with your existing systems:

```typescript
// In 06-action-executor.step.ts
case "approved":
  await publishContent(submissionId);
  await notifyUser(userId, "Your content has been approved");
  break;
```

---

## 💻 Dive into the Code

Want to explore the complete content moderation implementation? Check out the full source code, including all steps, Slack integration, and production-ready configuration:

<div className="not-prose">
  <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete Content Moderation System</h3>
        <p className="text-gray-600 mb-4">Access the full implementation with AI analysis, Slack integration, and human-in-the-loop workflows.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/ai-content-moderation" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Content Moderation Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Intelligent Content Moderation at Scale

This content moderation system demonstrates the power of combining AI analysis with human oversight in an event-driven architecture. By breaking down moderation into discrete, specialized components, we've created a system that's not only intelligent but also flexible and maintainable.

The human-in-the-loop approach means you can:
- **Scale efficiently**: Automatically handle 80-90% of content while maintaining quality
- **Adapt quickly**: Adjust thresholds and routing logic without system changes
- **Maintain oversight**: Human moderators focus on complex cases that require judgment
- **Integrate seamlessly**: Use existing team communication tools like Slack

Key architectural benefits:
- **Intelligent routing**: Confidence-based decisions reduce human workload
- **Flexible integration**: Works with any team communication platform
- **Audit compliance**: Complete decision trails and moderator attribution
- **Scalable architecture**: Each component can be scaled independently

From here, you can extend the system by:
- Adding support for video content moderation
- Implementing custom AI models for specific content types
- Building analytics dashboards for moderation insights
- Integrating with user management and content management systems
- Adding escalation policies and moderator workflows

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing moderation pipeline.

Ready to build content moderation that scales with your platform? Start building with Motia today!


-   [ai-deep-research-agent](/docs/examples/ai-deep-research-agent): Documentation for ai-deep-research-agent.
---
title: 'AI Research Agent'
description: A powerful research assistant that leverages the Motia Framework to perform comprehensive web research on any topic and any question.
---

import { CodeFetcher } from '../../../components/CodeFetcher'

## Let's build a AI Deep Research Agent that:

- **Deep Web Research**: Automatically searches the web, extracts content, and synthesizes findings
- **Iterative Research Process**: Supports multiple layers of research depth for comprehensive exploration
- **Event-Driven Architecture**: Built using Motia Framework's event system for robust workflow management
- **Parallel Processing**: Efficiently processes search results and content extraction
- **API Endpoints**: REST API access for initiating research and retrieving reports
- **Stateful Processing**: Maintains research state throughout the entire process

## The Steps

<Folder name="steps" defaultOpen>
  <File name="analyze-content.step.ts" />
  <File name="compile-report.step.ts" />
  <File name="extract-content.step.ts" />
  <File name="follow-up-research.step.ts" />
  <File name="generate-queries.step.ts" />
  <File name="report-api.step.ts" />
  <File name="research-api.step.ts" />
  <File name="search-web.step.ts" />
  <File name="status-api.step.ts" />
</Folder>

<Tabs items={['analyze-content', 'compile-report', 'extract-content', 'follow-up-research', 'generate-queries', 'report-api', 'research-api', 'search-web', 'status-api']}>
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="analyze-content" value="analyze-content" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="compile-report" value="compile-report" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="extract-content" value="extract-content" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="follow-up-research" value="follow-up-research" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="generate-queries" value="generate-queries" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="report-api" value="report-api" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="research-api" value="research-api" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="search-web" value="search-web" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="status-api" value="status-api" />
</Tabs>

## 🚀 Features

- **Deep Web Research**: Automatically searches the web, extracts content, and synthesizes findings
- **Iterative Research Process**: Supports multiple layers of research depth for comprehensive exploration
- **Event-Driven Architecture**: Built using Motia Framework's event system for robust workflow management
- **Parallel Processing**: Efficiently processes search results and content extraction
- **API Endpoints**: REST API access for initiating research and retrieving reports
- **Stateful Processing**: Maintains research state throughout the entire process

## 📋 Prerequisites

- Node.js v18 or later
- npm or pnpm
- API keys for:
  - [OpenAI](https://platform.openai.com/) (AI analysis)
  - [Firecrawl](https://www.firecrawl.dev/) (Web Crawler)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MotiaDev/motia-examples
   cd examples/ai-deep-research-agent
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

   Update `.env` with your API keys:
   ```bash
   # Required
   OPENAI_API_KEY=your-openai-api-key-here
   FIRECRAWL_API_KEY=your-firecrawl-api-key-here

   # Optional
   # OPENAI_MODEL=gpt-4o
   # FIRECRAWL_BASE_URL=http://your-firecrawl-instance-url
   ```

## 🏗️ Architecture

![AI Deep Research Agent](../img/ai-deep-research-agent.png)


## 🚦 API Endpoints

### Start Research

```
POST /research
Content-Type: application/json

{
  "query": "The research topic or question",
  "breadth": 4,  // Number of search queries to generate (1-10)
  "depth": 2     // Depth of research iterations (1-5)
}
```

Response:
```json
{
  "message": "Research process started",
  "requestId": "unique-trace-id"
}
```

### Check Research Status

```
GET /research/status?requestId=unique-trace-id
```

Response:
```json
{
  "message": "Research status retrieved successfully",
  "requestId": "unique-trace-id",
  "originalQuery": "The research topic or question",
  "status": "in-progress",
  "progress": {
    "currentDepth": 1,
    "totalDepth": 2,
    "percentComplete": 50
  },
  "reportAvailable": false
}
```

### Get Research Report

```
GET /research/report?requestId=unique-trace-id
```

Response:
```json
{
  "message": "Research report retrieved successfully",
  "report": {
    "title": "Research Report Title",
    "overview": "Executive summary...",
    "sections": [
      {
        "title": "Section Title",
        "content": "Section content..."
      }
    ],
    "keyTakeaways": [
      "Key takeaway 1",
      "Key takeaway 2"
    ],
    "sources": [
      {
        "title": "Source Title",
        "url": "Source URL"
      }
    ],
    "originalQuery": "The research topic or question",
    "metadata": {
      "depthUsed": 2,
      "completedAt": "2025-03-18T16:45:30Z"
    }
  },
  "requestId": "unique-trace-id"
}
```

## 🏃‍♂️ Running the Application

1. Start the development server:
   ```bash
   pnpm dev
   ```

2. Access the Motia Workbench:
   ```
   http://localhost:3000
   ```

3. Make a test request:
   ```bash
   curl --request POST \
   --url http://localhost:3000/research \
   --header 'Content-Type: application/json' \
   --data '{
      "query": "Advancements in renewable energy storage",
      "depth": 1,
      "breadth": 1
   }'
   ```
## 🙏 Acknowledgments

- [Motia Framework](https://motia.dev) for the event-driven workflow engine
- [OpenAI](https://platform.openai.com/) for AI analysis 
- [Firecrawl](https://www.firecrawl.dev/) for Web search and content extraction API


## Examples
[ai-deep-research-agent](/docs/examples/ai-deep-research-agent): Code example
---
title: 'AI Research Agent'
description: A powerful research assistant that leverages the Motia Framework to perform comprehensive web research on any topic and any question.
---

import { CodeFetcher } from '../../../components/CodeFetcher'

## Let's build a AI Deep Research Agent that:

- **Deep Web Research**: Automatically searches the web, extracts content, and synthesizes findings
- **Iterative Research Process**: Supports multiple layers of research depth for comprehensive exploration
- **Event-Driven Architecture**: Built using Motia Framework's event system for robust workflow management
- **Parallel Processing**: Efficiently processes search results and content extraction
- **API Endpoints**: REST API access for initiating research and retrieving reports
- **Stateful Processing**: Maintains research state throughout the entire process

## The Steps

<Folder name="steps" defaultOpen>
  <File name="analyze-content.step.ts" />
  <File name="compile-report.step.ts" />
  <File name="extract-content.step.ts" />
  <File name="follow-up-research.step.ts" />
  <File name="generate-queries.step.ts" />
  <File name="report-api.step.ts" />
  <File name="research-api.step.ts" />
  <File name="search-web.step.ts" />
  <File name="status-api.step.ts" />
</Folder>

<Tabs items={['analyze-content', 'compile-report', 'extract-content', 'follow-up-research', 'generate-queries', 'report-api', 'research-api', 'search-web', 'status-api']}>
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="analyze-content" value="analyze-content" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="compile-report" value="compile-report" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="extract-content" value="extract-content" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="follow-up-research" value="follow-up-research" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="generate-queries" value="generate-queries" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="report-api" value="report-api" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="research-api" value="research-api" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="search-web" value="search-web" />
  <CodeFetcher path="examples/ai-deep-research-agent/steps" tab="status-api" value="status-api" />
</Tabs>

## 🚀 Features

- **Deep Web Research**: Automatically searches the web, extracts content, and synthesizes findings
- **Iterative Research Process**: Supports multiple layers of research depth for comprehensive exploration
- **Event-Driven Architecture**: Built using Motia Framework's event system for robust workflow management
- **Parallel Processing**: Efficiently processes search results and content extraction
- **API Endpoints**: REST API access for initiating research and retrieving reports
- **Stateful Processing**: Maintains research state throughout the entire process

## 📋 Prerequisites

- Node.js v18 or later
- npm or pnpm
- API keys for:
  - [OpenAI](https://platform.openai.com/) (AI analysis)
  - [Firecrawl](https://www.firecrawl.dev/) (Web Crawler)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MotiaDev/motia-examples
   cd examples/ai-deep-research-agent
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

   Update `.env` with your API keys:
   ```bash
   # Required
   OPENAI_API_KEY=your-openai-api-key-here
   FIRECRAWL_API_KEY=your-firecrawl-api-key-here

   # Optional
   # OPENAI_MODEL=gpt-4o
   # FIRECRAWL_BASE_URL=http://your-firecrawl-instance-url
   ```

## 🏗️ Architecture

![AI Deep Research Agent](../img/ai-deep-research-agent.png)


## 🚦 API Endpoints

### Start Research

```
POST /research
Content-Type: application/json

{
  "query": "The research topic or question",
  "breadth": 4,  // Number of search queries to generate (1-10)
  "depth": 2     // Depth of research iterations (1-5)
}
```

Response:
```json
{
  "message": "Research process started",
  "requestId": "unique-trace-id"
}
```

### Check Research Status

```
GET /research/status?requestId=unique-trace-id
```

Response:
```json
{
  "message": "Research status retrieved successfully",
  "requestId": "unique-trace-id",
  "originalQuery": "The research topic or question",
  "status": "in-progress",
  "progress": {
    "currentDepth": 1,
    "totalDepth": 2,
    "percentComplete": 50
  },
  "reportAvailable": false
}
```

### Get Research Report

```
GET /research/report?requestId=unique-trace-id
```

Response:
```json
{
  "message": "Research report retrieved successfully",
  "report": {
    "title": "Research Report Title",
    "overview": "Executive summary...",
    "sections": [
      {
        "title": "Section Title",
        "content": "Section content..."
      }
    ],
    "keyTakeaways": [
      "Key takeaway 1",
      "Key takeaway 2"
    ],
    "sources": [
      {
        "title": "Source Title",
        "url": "Source URL"
      }
    ],
    "originalQuery": "The research topic or question",
    "metadata": {
      "depthUsed": 2,
      "completedAt": "2025-03-18T16:45:30Z"
    }
  },
  "requestId": "unique-trace-id"
}
```

## 🏃‍♂️ Running the Application

1. Start the development server:
   ```bash
   pnpm dev
   ```

2. Access the Motia Workbench:
   ```
   http://localhost:3000
   ```

3. Make a test request:
   ```bash
   curl --request POST \
   --url http://localhost:3000/research \
   --header 'Content-Type: application/json' \
   --data '{
      "query": "Advancements in renewable energy storage",
      "depth": 1,
      "breadth": 1
   }'
   ```
## 🙏 Acknowledgments

- [Motia Framework](https://motia.dev) for the event-driven workflow engine
- [OpenAI](https://platform.openai.com/) for AI analysis 
- [Firecrawl](https://www.firecrawl.dev/) for Web search and content extraction API

-   [finance-agent](/docs/examples/finance-agent): Documentation for finance-agent.
---
title: 'Finance Agent'
description: A powerful event-driven financial analysis workflow that combines web search, financial data, and AI analysis to provide comprehensive investment insights.
---

import { CodeFetcher } from '../../../components/CodeFetcher'

## Let's build a finance agent that:

- Real-time Financial Analysis: Combines multiple data sources for comprehensive insights
- AI-Powered Insights: Leverages OpenAI GPT-4 for intelligent market analysis
- Web Search Integration: Aggregates latest market news and analysis
- Financial Data Integration: Real-time stock and company information

## The Steps

<Folder name="steps" defaultOpen>
  <File name="finance-data.step.ts" />
  <File name="openai-analysis.step.ts" />
  <File name="query-api.step.ts" />
  <File name="response-coordinator.step.ts" />
  <File name="result-api.step.ts" />
  <File name="save-result.step.ts" />
  <File name="web-search.step.ts" />
</Folder>

<Tabs items={['finance-data', 'openai-analysis', 'query-api', 'response-coordinator', 'result-api', 'save-result', 'web-search']}>
  <CodeFetcher path="examples/finance-agent/steps" tab="finance-data" value="finance-data" />
  <CodeFetcher path="examples/finance-agent/steps" tab="openai-analysis" value="openai-analysis" />
  <CodeFetcher path="examples/finance-agent/steps" tab="query-api" value="query-api" />
  <CodeFetcher path="examples/finance-agent/steps" tab="response-coordinator" value="response-coordinator" />
  <CodeFetcher path="examples/finance-agent/steps" tab="result-api" value="result-api" />
  <CodeFetcher path="examples/finance-agent/steps" tab="save-result" value="save-result" />
  <CodeFetcher path="examples/finance-agent/steps" tab="web-search" value="web-search" />
</Tabs>

## 🚀 Features

- **Real-time Financial Analysis**: Combines multiple data sources for comprehensive insights
- **AI-Powered Insights**: Leverages OpenAI GPT-4 for intelligent market analysis
- **Event-Driven Architecture**: Built on Motia's robust event system for reliable processing
- **Web Search Integration**: Aggregates latest market news and analysis
- **Financial Data Integration**: Real-time stock and company information
- **Persistent Storage**: Stores analysis results for future reference
- **RESTful API**: Easy integration with existing systems

## 📋 Prerequisites

- Node.js v16+
- npm or pnpm
- API keys for:
  - [Alpha Vantage](https://www.alphavantage.co/) (financial data)
  - [SerperDev](https://serper.dev/) (web search)
  - [OpenAI](https://platform.openai.com/) (AI analysis)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MotiaDev/motia-examples
   cd examples/finance-agent
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

   Update `.env` with your API keys:
   ```bash
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🏗️ Architecture

The workflow consists of several specialized steps that work together to provide comprehensive financial analysis:

![Finance Agent](../img/finance-agent.gif)


## 🚦 API Endpoints

### Query Endpoint

```http
POST /finance-query
Content-Type: application/json

{
  "query": "Latest information about AAPL and MSFT"
}
```

Response:
```json
{
  "message": "Query received and processing started",
  "traceId": "abc123def456"
}
```

### Results Endpoint

```http
GET /finance-result/:traceId
```

Response:
```json
{
  "query": "Latest information about AAPL and MSFT",
  "timestamp": "2023-06-15T12:34:56.789Z",
  "response": {
    "summary": "Results for \"Latest information about AAPL and MSFT\"",
    "webResources": [...],
    "financialData": [...],
    "aiAnalysis": {...}
  },
  "status": "success"
}
```

## 🏃‍♂️ Running the Application

1. Start the development server:
   ```bash
   pnpm dev
   ```

2. Access the Motia Workbench:
   ```
   http://localhost:3000
   ```

3. Make a test request:
   ```bash
   curl -X POST http://localhost:3000/finance-query \
     -H "Content-Type: application/json" \
     -d '{"query": "Latest information about AAPL and MSFT"}'
   ```
## 🙏 Acknowledgments

- [Motia Framework](https://motia.dev) for the event-driven workflow engine
- [Alpha Vantage](https://www.alphavantage.co/) for financial data
- [SerperDev](https://serper.dev/) for web search capabilities
- [OpenAI](https://platform.openai.com/) for AI analysis 


## Examples
[finance-agent](/docs/examples/finance-agent): Code example
---
title: 'Finance Agent'
description: A powerful event-driven financial analysis workflow that combines web search, financial data, and AI analysis to provide comprehensive investment insights.
---

import { CodeFetcher } from '../../../components/CodeFetcher'

## Let's build a finance agent that:

- Real-time Financial Analysis: Combines multiple data sources for comprehensive insights
- AI-Powered Insights: Leverages OpenAI GPT-4 for intelligent market analysis
- Web Search Integration: Aggregates latest market news and analysis
- Financial Data Integration: Real-time stock and company information

## The Steps

<Folder name="steps" defaultOpen>
  <File name="finance-data.step.ts" />
  <File name="openai-analysis.step.ts" />
  <File name="query-api.step.ts" />
  <File name="response-coordinator.step.ts" />
  <File name="result-api.step.ts" />
  <File name="save-result.step.ts" />
  <File name="web-search.step.ts" />
</Folder>

<Tabs items={['finance-data', 'openai-analysis', 'query-api', 'response-coordinator', 'result-api', 'save-result', 'web-search']}>
  <CodeFetcher path="examples/finance-agent/steps" tab="finance-data" value="finance-data" />
  <CodeFetcher path="examples/finance-agent/steps" tab="openai-analysis" value="openai-analysis" />
  <CodeFetcher path="examples/finance-agent/steps" tab="query-api" value="query-api" />
  <CodeFetcher path="examples/finance-agent/steps" tab="response-coordinator" value="response-coordinator" />
  <CodeFetcher path="examples/finance-agent/steps" tab="result-api" value="result-api" />
  <CodeFetcher path="examples/finance-agent/steps" tab="save-result" value="save-result" />
  <CodeFetcher path="examples/finance-agent/steps" tab="web-search" value="web-search" />
</Tabs>

## 🚀 Features

- **Real-time Financial Analysis**: Combines multiple data sources for comprehensive insights
- **AI-Powered Insights**: Leverages OpenAI GPT-4 for intelligent market analysis
- **Event-Driven Architecture**: Built on Motia's robust event system for reliable processing
- **Web Search Integration**: Aggregates latest market news and analysis
- **Financial Data Integration**: Real-time stock and company information
- **Persistent Storage**: Stores analysis results for future reference
- **RESTful API**: Easy integration with existing systems

## 📋 Prerequisites

- Node.js v16+
- npm or pnpm
- API keys for:
  - [Alpha Vantage](https://www.alphavantage.co/) (financial data)
  - [SerperDev](https://serper.dev/) (web search)
  - [OpenAI](https://platform.openai.com/) (AI analysis)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MotiaDev/motia-examples
   cd examples/finance-agent
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

   Update `.env` with your API keys:
   ```bash
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🏗️ Architecture

The workflow consists of several specialized steps that work together to provide comprehensive financial analysis:

![Finance Agent](../img/finance-agent.gif)


## 🚦 API Endpoints

### Query Endpoint

```http
POST /finance-query
Content-Type: application/json

{
  "query": "Latest information about AAPL and MSFT"
}
```

Response:
```json
{
  "message": "Query received and processing started",
  "traceId": "abc123def456"
}
```

### Results Endpoint

```http
GET /finance-result/:traceId
```

Response:
```json
{
  "query": "Latest information about AAPL and MSFT",
  "timestamp": "2023-06-15T12:34:56.789Z",
  "response": {
    "summary": "Results for \"Latest information about AAPL and MSFT\"",
    "webResources": [...],
    "financialData": [...],
    "aiAnalysis": {...}
  },
  "status": "success"
}
```

## 🏃‍♂️ Running the Application

1. Start the development server:
   ```bash
   pnpm dev
   ```

2. Access the Motia Workbench:
   ```
   http://localhost:3000
   ```

3. Make a test request:
   ```bash
   curl -X POST http://localhost:3000/finance-query \
     -H "Content-Type: application/json" \
     -d '{"query": "Latest information about AAPL and MSFT"}'
   ```
## 🙏 Acknowledgments

- [Motia Framework](https://motia.dev) for the event-driven workflow engine
- [Alpha Vantage](https://www.alphavantage.co/) for financial data
- [SerperDev](https://serper.dev/) for web search capabilities
- [OpenAI](https://platform.openai.com/) for AI analysis 

-   [github-integration-workflow](/docs/examples/github-integration-workflow): Documentation for github-integration-workflow.
---
title: 'GitHub Integration'
description: Build an automated GitHub issue and PR management system with AI-powered classification and routing
---

## Let's build a GitHub automation system that:

1. Automatically triages and classifies new issues
2. Intelligently assigns labels based on content
3. Suggests appropriate assignees and reviewers
4. Monitors PR test status
5. Generates contextual comments

## Workflow Structure

The GitHub integration workflow is organized into two main components:

- **Issue Triage**: Handles the management of GitHub issues
- **PR Classifier**: Manages pull request workflows

## The Steps

<Folder name="steps" defaultOpen>
  <Folder name="issue-triage" defaultOpen>
    <File name="github-webhook.step.ts" />
    <File name="issue-classifier.step.ts" />
    <File name="label-assigner.step.ts" />
    <File name="assignee-selector.step.ts" />
    <File name="handle-new-issue.step.ts" />
    <File name="handle-issue-update.step.ts" />
    <File name="handle-issue-closure.step.ts" />
  </Folder>
  <Folder name="pr-classifier" defaultOpen>
    <File name="pr-webhook.step.ts" />
    <File name="pr-classifier.step.ts" />
    <File name="pr-label-assigner.step.ts" />
    <File name="pr-reviewer-assigner.step.ts" />
    <File name="pr-test-monitor.step.ts" />
  </Folder>
</Folder>

<Tabs items={['issue-webhook', 'issue-classifier', 'label-assigner', 'assignee-selector']}>
  <GitHubWorkflowTab tab="issue-webhook" value="github-webhook" folder="issue-triage" />
  <GitHubWorkflowTab tab="issue-classifier" value="issue-classifier" folder="issue-triage" />
  <GitHubWorkflowTab tab="label-assigner" value="label-assigner" folder="issue-triage" />
  <GitHubWorkflowTab tab="assignee-selector" value="assignee-selector" folder="issue-triage" />
</Tabs>

<Tabs items={['pr-webhook', 'pr-classifier', 'pr-reviewer', 'pr-monitor']}>
  <GitHubWorkflowTab tab="pr-webhook" value="pr-webhook" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-classifier" value="pr-classifier" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-reviewer" value="pr-reviewer-assigner" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-monitor" value="pr-test-monitor" folder="pr-classifier" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: GitHub Issue Workflow](../img/github-issue-workflow.png)</div>
<div className="my-8">![Flow: GitHub PR Workflow](../img/github-pr-workflow.png)</div>

1. **Webhook Reception** → Captures GitHub events
2. **Issue/PR Classification** → Analyzes content with AI
3. **Automated Labeling** → Applies appropriate labels
4. **Smart Assignment** → Suggests reviewers and assignees
5. **Status Monitoring** → Tracks PR test status

## Try It Out

<Steps>

### Prerequisites

Make sure you have:

- GitHub account with personal access token
- Node.js installed
- OpenAI API key (for AI classification)

### Clone the Repository

```bash
git clone git@github.com:MotiaDev/motia-examples.git
cd examples/github-integration-workflow
```

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Update your `.env` with the following credentials:

```bash
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key
```

### Set Up GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to Webhooks and add a new webhook
3. Set the Payload URL to your Motia server endpoint
4. Select content type as `application/json`
5. Choose which events to trigger the webhook (Issues, Pull requests)
6. Save the webhook

### Run the Application

```bash
npm run dev
```

### Test the Flow

1. Create a new issue in your GitHub repository
2. Watch as it gets automatically classified and labeled
3. Create a new PR to see the reviewer assignment in action
4. Check the PR comments for test status updates

</Steps>

<Callout type="info">
  For more detailed setup instructions and configuration options, check out the [full
  documentation](https://github.com/MotiaDev/motia-examples/tree/main/examples/github-integration-workflow).
</Callout> 


## Examples
[github-integration-workflow](/docs/examples/github-integration-workflow): Code example
---
title: 'GitHub Integration'
description: Build an automated GitHub issue and PR management system with AI-powered classification and routing
---

## Let's build a GitHub automation system that:

1. Automatically triages and classifies new issues
2. Intelligently assigns labels based on content
3. Suggests appropriate assignees and reviewers
4. Monitors PR test status
5. Generates contextual comments

## Workflow Structure

The GitHub integration workflow is organized into two main components:

- **Issue Triage**: Handles the management of GitHub issues
- **PR Classifier**: Manages pull request workflows

## The Steps

<Folder name="steps" defaultOpen>
  <Folder name="issue-triage" defaultOpen>
    <File name="github-webhook.step.ts" />
    <File name="issue-classifier.step.ts" />
    <File name="label-assigner.step.ts" />
    <File name="assignee-selector.step.ts" />
    <File name="handle-new-issue.step.ts" />
    <File name="handle-issue-update.step.ts" />
    <File name="handle-issue-closure.step.ts" />
  </Folder>
  <Folder name="pr-classifier" defaultOpen>
    <File name="pr-webhook.step.ts" />
    <File name="pr-classifier.step.ts" />
    <File name="pr-label-assigner.step.ts" />
    <File name="pr-reviewer-assigner.step.ts" />
    <File name="pr-test-monitor.step.ts" />
  </Folder>
</Folder>

<Tabs items={['issue-webhook', 'issue-classifier', 'label-assigner', 'assignee-selector']}>
  <GitHubWorkflowTab tab="issue-webhook" value="github-webhook" folder="issue-triage" />
  <GitHubWorkflowTab tab="issue-classifier" value="issue-classifier" folder="issue-triage" />
  <GitHubWorkflowTab tab="label-assigner" value="label-assigner" folder="issue-triage" />
  <GitHubWorkflowTab tab="assignee-selector" value="assignee-selector" folder="issue-triage" />
</Tabs>

<Tabs items={['pr-webhook', 'pr-classifier', 'pr-reviewer', 'pr-monitor']}>
  <GitHubWorkflowTab tab="pr-webhook" value="pr-webhook" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-classifier" value="pr-classifier" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-reviewer" value="pr-reviewer-assigner" folder="pr-classifier" />
  <GitHubWorkflowTab tab="pr-monitor" value="pr-test-monitor" folder="pr-classifier" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: GitHub Issue Workflow](../img/github-issue-workflow.png)</div>
<div className="my-8">![Flow: GitHub PR Workflow](../img/github-pr-workflow.png)</div>

1. **Webhook Reception** → Captures GitHub events
2. **Issue/PR Classification** → Analyzes content with AI
3. **Automated Labeling** → Applies appropriate labels
4. **Smart Assignment** → Suggests reviewers and assignees
5. **Status Monitoring** → Tracks PR test status

## Try It Out

<Steps>

### Prerequisites

Make sure you have:

- GitHub account with personal access token
- Node.js installed
- OpenAI API key (for AI classification)

### Clone the Repository

```bash
git clone git@github.com:MotiaDev/motia-examples.git
cd examples/github-integration-workflow
```

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Update your `.env` with the following credentials:

```bash
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key
```

### Set Up GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to Webhooks and add a new webhook
3. Set the Payload URL to your Motia server endpoint
4. Select content type as `application/json`
5. Choose which events to trigger the webhook (Issues, Pull requests)
6. Save the webhook

### Run the Application

```bash
npm run dev
```

### Test the Flow

1. Create a new issue in your GitHub repository
2. Watch as it gets automatically classified and labeled
3. Create a new PR to see the reviewer assignment in action
4. Check the PR comments for test status updates

</Steps>

<Callout type="info">
  For more detailed setup instructions and configuration options, check out the [full
  documentation](https://github.com/MotiaDev/motia-examples/tree/main/examples/github-integration-workflow).
</Callout> 

-   [github-stars-counter](/docs/examples/github-stars-counter): Documentation for github-stars-counter.
---
title: 'GitHub Stars Counter'
description: 'Real-Time GitHub Stars Counter: Building Live Updates with Motia Streams'
---

In today's social-driven development world, real-time metrics and live updates are essential for building engaging applications. Whether you're creating a portfolio site, an open-source project showcase, or a developer dashboard, you need systems that can display live data without complex infrastructure.

This comprehensive guide explores how to build a production-ready, real-time GitHub stars counter using Motia's event-driven architecture and streaming capabilities. We'll cover:

1. **Real-Time Streams**: How Motia's streams enable effortless live data synchronization
2. **Secure Webhooks**: Production-ready webhook signature verification and event handling
3. **Minimal Architecture**: Building powerful real-time features with just two components
4. **Live Integration**: How this exact counter powers the live star count on the Motia website

Let's build a stars counter that updates in real-time across all connected clients.

---

## 🏭 Production-Grade Example

**This is not a tutorial project** - this is battle-tested, production-ready code that handles real traffic at scale. Every aspect has been designed for enterprise use:

- **🔐 Enterprise Security**: HMAC webhook verification, timing-safe comparisons, comprehensive input validation
- **⚡ High Performance**: Handles thousands of concurrent connections with automatic scaling
- **📊 Full Observability**: Structured logging, error tracking, and comprehensive monitoring
- **🛡️ Error Resilience**: Graceful degradation, retry logic, and fault tolerance
- **🌍 Global Scale**: Production deployment on Motia Cloud with worldwide CDN
- **💰 Cost Efficient**: Serverless architecture that scales to zero when not in use

---

## Live Proof: Powering Motia.dev Header

**This isn't just a demo** - this exact code powers the live GitHub star counter you can see right now in the header of [Motia.dev](https://motia.dev)! 

Look at the top-right corner of the Motia website and you'll see:
- **🏠 Motia** logo on the left
- **📑 Blog, Docs, Manifesto** navigation 
- **⭐ GitHub** icon with a **live star count** (currently showing 7953+ stars)
- **🚀 Vercel OSS 2025** badge

That live-updating number next to the GitHub icon? That's this exact implementation in production, processing real webhook events and streaming updates to thousands of visitors in real-time!

---

## The Power of Real-Time Simplicity

<div className="my-8">![GitHub Stars Counter Demo](/docs-images/motia-star.gif)</div>

At its core, our GitHub stars counter solves a fundamental challenge: how do you display live, real-time metrics without complex WebSocket infrastructure or manual state management? Traditional approaches often involve intricate server-side event handling, client connection management, and complex state synchronization.

Our Motia-powered solution breaks this down into just two simple components:

- **[GitHub Webhooks](https://docs.github.com/en/webhooks)**: Instant notifications when repository stars change
- **[Motia Streams](https://motia.dev)**: Real-time data synchronization with automatic state management
- **[Production Security](https://docs.github.com/en/webhooks/securing)**: Built-in webhook signature verification

🎯 **Live in Action**: This exact implementation powers the real-time star counter visible in the header of [Motia.dev](https://motia.dev) (look for the GitHub icon with live count), updating instantly whenever developers star the repository!

Instead of complex infrastructure, we get a resilient real-time system where data flows effortlessly from GitHub events to live client updates.

---

## The Anatomy of Our Real-Time Counter

Our application consists of just two specialized components, each handling a specific part of the real-time data flow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="00-repository-stars.stream.ts" />
  <File name="01-github-webhook.step.ts" />
</Folder>

<Folder name="utils" defaultOpen>
  <File name="verify-webhook-signature.ts" />
  <File name="check-user-profile.ts" />
</Folder>

<Tabs items={['stream-config', 'webhook-handler', 'signature-verification', 'user-profile']}>
  <Tab value="stream-config">
    The real-time data stream that holds our repository star counts. This stream automatically synchronizes data to all connected clients with zero configuration.

    ```typescript
    import { StreamConfig } from 'motia'
    import { z } from 'zod'

    const RepositoryStarsSchema = z.object({
      stars: z.number(),
      name: z.string(),
      fullName: z.string(),
      organization: z.string(),
      lastUpdated: z.string(),
    })

    export type RepositoryStars = z.infer<typeof RepositoryStarsSchema>

    export const config: StreamConfig = {
      name: 'stars',
      schema: RepositoryStarsSchema,
      baseConfig: { storageType: 'default' },
    }
    ```

  </Tab>
  <Tab value="webhook-handler">
    The secure webhook endpoint that receives GitHub star events, verifies their authenticity, and updates the real-time stream with new star counts.

    ```typescript
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { verifyWebhookSignature } from '../utils/verify-webhook-signature'
    import { checkUserProfile } from '../utils/check-user-profile'

    export const config: ApiRouteConfig = {
      type: 'api',
      name: 'GitHubStarWebhook',
      description: 'Process GitHub star webhook events with signature verification',
      method: 'POST',
      path: '/webhooks/github/star',
      bodySchema: z.object({
        action: z.enum(['created', 'deleted']),
        starred_at: z.string().optional(),
        repository: z.object({
          name: z.string(),
          full_name: z.string(),
          stargazers_count: z.number(),
          owner: z.object({ login: z.string() }),
        }),
        sender: z.object({
          login: z.string(),
          name: z.string(),
          avatar_url: z.string().optional(),
          html_url: z.string(),
          url: z.string({ description: 'API URL' }),
        }),
      }),
      responseSchema: {
        200: z.object({
          message: z.string(),
          event: z.string(),
          processed: z.boolean(),
        }),
        400: z.object({ error: z.string() }),
        401: z.object({ error: z.string() }),
        500: z.object({ error: z.string() }),
      },
      emits: [],
      flows: ['github-star-processing'],
    }

    export const handler: Handlers['GitHubStarWebhook'] = async (
      req,
      { logger, streams, state, traceId }
    ) => {
      try {
        // Extract and validate GitHub headers
        const githubEvent = req.headers['x-github-event'] as string
        const githubDelivery = req.headers['x-github-delivery'] as string
        const githubSignature = req.headers['x-hub-signature-256'] as string
        const githubSignatureSha1 = req.headers['x-hub-signature'] as string

        // Only process star events
        if (githubEvent !== 'star') {
          logger.info('Ignoring non-star event', { githubEvent, githubDelivery })

          return {
            status: 200,
            body: {
              message: 'Event ignored - only processing star events',
              event: githubEvent,
              processed: false,
            },
          }
        }

        // Verify webhook signature if secret is configured
        const webhookSecret = process.env.GITHUB_WEBHOOK_SECRET

        if (webhookSecret) {
          logger.info('Verifying webhook signature', {
            delivery: githubDelivery,
            event: githubEvent,
          })

          const isValidSignature = verifyWebhookSignature({
            payload: JSON.stringify(req.body),
            signature: githubSignature || githubSignatureSha1,
            secret: webhookSecret,
            algorithm: githubSignature ? 'sha256' : 'sha1',
          })

          if (!isValidSignature) {
            logger.warn('Invalid webhook signature', {
              delivery: githubDelivery,
              event: githubEvent,
            })

            return {
              status: 401,
              body: { error: 'Invalid webhook signature' },
            }
          }
        }

        // Extract repository and user data
        const repository = {
          fullName: req.body.repository.full_name,
          name: req.body.repository.name,
          organization: req.body.repository.owner.login,
        }

        const sender = {
          name: req.body.sender.name,
          login: req.body.sender.login,
          avatarUrl: req.body.sender.avatar_url,
          url: req.body.sender.html_url,
          apiUrl: req.body.sender.url,
        }

        // Prepare star data for stream
        const webhookData = {
          fullName: repository.fullName,
          name: repository.name,
          organization: repository.organization,
          lastUpdated: req.body.starred_at || new Date().toISOString(),
          stars: req.body.repository.stargazers_count,
        }

        // Update real-time stream - this automatically propagates to all clients!
        await streams.stars.set(repository.organization, repository.name, webhookData)

        logger.info('GitHub star webhook processed successfully', { ...webhookData, sender })

        // Optional: Fetch additional user profile data
        if (sender.apiUrl) {
          try {
            logger.info('Getting GitHub user profile', { apiUrl: sender.apiUrl })
            const userProfile = await checkUserProfile(sender.apiUrl)
            await state.set(repository.fullName, traceId, userProfile)
            logger.info('GitHub user profile', { userProfile })
          } catch (error: any) {
            logger.error('Failed to get GitHub user profile', { error: error.message })
          }
        }

        return {
          status: 200,
          body: {
            message: 'Star webhook processed successfully',
            event: githubEvent,
            processed: true,
          },
        }
      } catch (error: any) {
        logger.error('GitHub star webhook processing failed', {
          error: error.message,
          stack: error.stack,
        })

        return {
          status: 500,
          body: { error: 'Star webhook processing failed' },
        }
      }
    }
    ```

  </Tab>
  <Tab value="signature-verification">
    Production-ready webhook security that verifies GitHub webhook signatures using HMAC cryptographic validation to ensure requests are authentic.

    ```typescript
    import crypto from 'crypto'

    type Args = {
      payload: string
      signature: string
      secret: string
      algorithm: 'sha1' | 'sha256'
    }

    export function verifyWebhookSignature(args: Args): boolean {
      const { payload, signature, secret, algorithm = 'sha256' } = args

      try {
        if (!signature) return false

        // Generate expected signature using HMAC
        const expectedSignature =
          algorithm === 'sha256'
            ? `sha256=${crypto.createHmac('sha256', secret).update(payload, 'utf8').digest('hex')}`
            : `sha1=${crypto.createHmac('sha1', secret).update(payload, 'utf8').digest('hex')}`

        // Use timing-safe comparison to prevent timing attacks
        return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))
      } catch (error) {
        return false
      }
    }
    ```

  </Tab>
  <Tab value="user-profile">
    Optional GitHub user profile fetching that enriches webhook events with additional user information for analytics and user insights.

    ```typescript
    export interface GitHubUserProfile {
      login: string
      id: number
      node_id: string
      avatar_url: string
      gravatar_id: string
      url: string
      html_url: string
      followers_url: string
      following_url: string
      gists_url: string
      starred_url: string
      subscriptions_url: string
      organizations_url: string
      repos_url: string
      events_url: string
      received_events_url: string
      type: string
      user_view_type: string
      site_admin: boolean
      name: string | null
      company: string | null
      blog: string
      location: string | null
      email: string | null
      hireable: boolean | null
      bio: string | null
      twitter_username: string | null
      public_repos: number
      public_gists: number
      followers: number
      following: number
      created_at: string
      updated_at: string
    }

    export interface GitHubUserProfileResponse {
      followers: number
      bio: string | null
      email: string | null
      htmlUrl: string
      name: string | null
      login: string
      location: string | null
    }

    export const checkUserProfile = async (apiUrl: string): Promise<GitHubUserProfileResponse> => {
      const response = await fetch(apiUrl)
      const data = (await response.json()) as GitHubUserProfile

      return {
        followers: data.followers,
        bio: data.bio,
        email: data.email,
        htmlUrl: data.html_url,
        name: data.name,
        login: data.login,
        location: data.location,
      }
    }
    ```

  </Tab>
</Tabs>

---

## Real-Time Data Flow

The beauty of this architecture lies in its simplicity. Here's how real-time updates flow through the system:

1. **GitHub Event** → User stars/unstars your repository
2. **Webhook Delivery** → GitHub sends POST request to your endpoint  
3. **Security Validation** → Signature verification ensures request authenticity
4. **Stream Update** → Data is written to Motia stream with `streams.stars.set()`
5. **Live Propagation** → All connected clients automatically receive the update
6. **UI Updates** → Client applications re-render with new star count

**No manual WebSocket management, no connection handling, no state synchronization code required!**

---

## Key Features & Benefits

### ⚡ **Instant Real-Time Updates**
Stars update across all connected clients the moment GitHub sends the webhook - no polling, no delays.

### 🔐 **Production-Ready Security**  
HMAC signature verification with timing-safe comparison prevents unauthorized webhook requests.

### 🧩 **Minimal Architecture**
Just two components handle the complete real-time functionality - no complex infrastructure required.

### 📊 **Automatic State Management**
Motia streams handle data persistence, synchronization, and client updates automatically.

### 🎯 **Type-Safe Development**
Full TypeScript integration with Zod validation ensures zero runtime surprises.

### 🌐 **Live Production Usage**
This exact implementation powers the real-time counter visible in the Motia website header - go check it out now!

### 🚀 **Production-Grade Architecture**
Built for enterprise scale with proper error handling, security, monitoring, and deployment automation.

---

## Trying It Out

Ready to build your own real-time GitHub stars counter? Let's get it running.

<Steps>

### Clone and Install

Start by getting the project locally and installing dependencies.

```shell
git clone https://github.com/MotiaDev/github-stars-counter.git
cd github-stars-counter
npm install
```

### Configure GitHub Webhook (Optional)

Set up webhook security with a secret for production use. This is optional for testing but essential for production deployments.

```shell
# Generate a secure random secret
export GITHUB_WEBHOOK_SECRET=$(openssl rand -hex 32)
echo "GITHUB_WEBHOOK_SECRET=$GITHUB_WEBHOOK_SECRET" >> .env
```

### Start Development Server

Launch the Motia development server to begin receiving webhook events.

```shell
npm run dev
```

Your webhook endpoint will be available at: `http://localhost:3000/webhooks/github/star`

### Set Up GitHub Webhook

Configure GitHub to send star events to your endpoint:

1. Go to your GitHub repository settings
2. Navigate to **Settings** → **Webhooks**  
3. Click **Add webhook**
4. Set **Payload URL** to your endpoint (use ngrok for local testing)
5. Set **Content type** to `application/json`
6. Add your webhook secret if configured
7. Select **Individual events** → **Stars**
8. Click **Add webhook**

### Test the Real-Time Updates

Test your webhook by starring/unstarring your repository:

1. **Star your repository** on GitHub
2. **Check the logs** - you should see webhook processing
3. **Access the stream** - query `/api/streams/stars` to see current data
4. **Watch real-time updates** in the Motia Workbench

### Access Real-Time Data

Your star data is now available via the Motia streams API:

```shell
# Get all repository star counts
curl http://localhost:3000/api/streams/stars

# Get specific repository star count  
curl http://localhost:3000/api/streams/stars/{org}/{repo}
```

The response includes live star counts that update automatically whenever GitHub sends webhook events.

### Deploy to Production

Once your counter is working locally, deploy it to production with Motia Cloud:

**Option 1: CLI Deployment**
```shell
# Deploy with version and API key
motia cloud deploy --api-key your-api-key --version-name 1.0.0

# Deploy with environment variables
motia cloud deploy --api-key your-api-key \
  --version-name 1.0.0 \
  --env-file .env.production \
  --environment-id your-env-id
```

**Option 2: One-Click Web Deployment**
1. Ensure your local project is running (`npm run dev`)
2. Go to [Motia Cloud -> Import from Workbench](https://motia.cloud)
3. Select your local project port
4. Choose project and environment name
5. Upload environment variables (optional)
6. Click **Deploy** and watch the magic happen! ✨

</Steps>

---

## 🚀 Production Deployment Guide

### Environment Variables

Configure these environment variables for production security and functionality:

```shell
# Required: GitHub webhook secret for security
GITHUB_WEBHOOK_SECRET="your-secure-random-secret"

# Optional: GitHub personal access token for enhanced API limits
GITHUB_TOKEN="ghp_your_github_token"
```

### Security Best Practices

For production deployments, ensure you:

1. **Generate secure webhook secrets**: 
   ```shell
   # Generate a cryptographically secure secret
   openssl rand -hex 32
   ```

2. **Store secrets securely**: Use environment variables, never commit to code

3. **Monitor webhook signatures**: The handler automatically verifies signatures when `GITHUB_WEBHOOK_SECRET` is set

4. **Enable logging**: Monitor for signature verification failures and unauthorized requests

### Scaling Considerations

This architecture scales automatically with your traffic:

- **Multiple repositories**: Each repo gets its own stream key (`org/repo`)
- **High concurrency**: Motia streams handle thousands of concurrent connections
- **Global distribution**: Deploy to multiple regions for worldwide performance
- **Cost optimization**: Pay only for actual usage with serverless scaling

---

## 💻 Dive into the Code

Want to explore the complete real-time implementation? Check out the full source code and see how simple real-time features can be with Motia:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Live GitHub Stars Counter</h3>
        <p className="text-gray-600 mb-4">Access the complete implementation with webhook security, real-time streams, and production deployment configurations. See exactly how the Motia website's live counter works!</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/github-stars-counter" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Stars Counter Code
          </a>
          <a 
            href="https://motia.dev" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            See It Live in Header →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Real-Time Made Simple

This GitHub stars counter demonstrates how Motia transforms complex real-time development into simple, manageable components. With just two files and minimal configuration, we've built a production-ready system that handles webhook security, real-time synchronization, and live client updates.

The beauty of this approach is its scalability and extensibility:
- **Add more repositories**: Each gets its own stream automatically
- **Enhance with analytics**: Track starring patterns and user insights
- **Multiple notification channels**: Slack, Discord, email alerts for milestones
- **Rich frontend integrations**: React, Vue, vanilla JS - all work seamlessly

Key architectural benefits:
- **No WebSocket complexity**: Streams handle all real-time synchronization automatically
- **Built-in security**: Production-ready webhook verification out of the box
- **Type safety**: Full TypeScript support prevents runtime errors
- **Zero configuration**: Real-time features work with no additional setup

This exact implementation powers the live star counter you see in the header of [Motia.dev](https://motia.dev) - that 7953+ count updating in real-time? It's this code in action, proven at enterprise scale with thousands of daily visitors.

**Production Metrics:**
- Handles 10,000+ webhook events per day
- Sub-50ms response times globally  
- 99.9% uptime with automatic failover
- Zero maintenance serverless architecture

Ready to add enterprise-grade real-time features to your applications? Deploy production-ready code with Motia today!




## Examples
[github-stars-counter](/docs/examples/github-stars-counter): Code example
---
title: 'GitHub Stars Counter'
description: 'Real-Time GitHub Stars Counter: Building Live Updates with Motia Streams'
---

In today's social-driven development world, real-time metrics and live updates are essential for building engaging applications. Whether you're creating a portfolio site, an open-source project showcase, or a developer dashboard, you need systems that can display live data without complex infrastructure.

This comprehensive guide explores how to build a production-ready, real-time GitHub stars counter using Motia's event-driven architecture and streaming capabilities. We'll cover:

1. **Real-Time Streams**: How Motia's streams enable effortless live data synchronization
2. **Secure Webhooks**: Production-ready webhook signature verification and event handling
3. **Minimal Architecture**: Building powerful real-time features with just two components
4. **Live Integration**: How this exact counter powers the live star count on the Motia website

Let's build a stars counter that updates in real-time across all connected clients.

---

## 🏭 Production-Grade Example

**This is not a tutorial project** - this is battle-tested, production-ready code that handles real traffic at scale. Every aspect has been designed for enterprise use:

- **🔐 Enterprise Security**: HMAC webhook verification, timing-safe comparisons, comprehensive input validation
- **⚡ High Performance**: Handles thousands of concurrent connections with automatic scaling
- **📊 Full Observability**: Structured logging, error tracking, and comprehensive monitoring
- **🛡️ Error Resilience**: Graceful degradation, retry logic, and fault tolerance
- **🌍 Global Scale**: Production deployment on Motia Cloud with worldwide CDN
- **💰 Cost Efficient**: Serverless architecture that scales to zero when not in use

---

## Live Proof: Powering Motia.dev Header

**This isn't just a demo** - this exact code powers the live GitHub star counter you can see right now in the header of [Motia.dev](https://motia.dev)! 

Look at the top-right corner of the Motia website and you'll see:
- **🏠 Motia** logo on the left
- **📑 Blog, Docs, Manifesto** navigation 
- **⭐ GitHub** icon with a **live star count** (currently showing 7953+ stars)
- **🚀 Vercel OSS 2025** badge

That live-updating number next to the GitHub icon? That's this exact implementation in production, processing real webhook events and streaming updates to thousands of visitors in real-time!

---

## The Power of Real-Time Simplicity

<div className="my-8">![GitHub Stars Counter Demo](/docs-images/motia-star.gif)</div>

At its core, our GitHub stars counter solves a fundamental challenge: how do you display live, real-time metrics without complex WebSocket infrastructure or manual state management? Traditional approaches often involve intricate server-side event handling, client connection management, and complex state synchronization.

Our Motia-powered solution breaks this down into just two simple components:

- **[GitHub Webhooks](https://docs.github.com/en/webhooks)**: Instant notifications when repository stars change
- **[Motia Streams](https://motia.dev)**: Real-time data synchronization with automatic state management
- **[Production Security](https://docs.github.com/en/webhooks/securing)**: Built-in webhook signature verification

🎯 **Live in Action**: This exact implementation powers the real-time star counter visible in the header of [Motia.dev](https://motia.dev) (look for the GitHub icon with live count), updating instantly whenever developers star the repository!

Instead of complex infrastructure, we get a resilient real-time system where data flows effortlessly from GitHub events to live client updates.

---

## The Anatomy of Our Real-Time Counter

Our application consists of just two specialized components, each handling a specific part of the real-time data flow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="00-repository-stars.stream.ts" />
  <File name="01-github-webhook.step.ts" />
</Folder>

<Folder name="utils" defaultOpen>
  <File name="verify-webhook-signature.ts" />
  <File name="check-user-profile.ts" />
</Folder>

<Tabs items={['stream-config', 'webhook-handler', 'signature-verification', 'user-profile']}>
  <Tab value="stream-config">
    The real-time data stream that holds our repository star counts. This stream automatically synchronizes data to all connected clients with zero configuration.

    ```typescript
    import { StreamConfig } from 'motia'
    import { z } from 'zod'

    const RepositoryStarsSchema = z.object({
      stars: z.number(),
      name: z.string(),
      fullName: z.string(),
      organization: z.string(),
      lastUpdated: z.string(),
    })

    export type RepositoryStars = z.infer<typeof RepositoryStarsSchema>

    export const config: StreamConfig = {
      name: 'stars',
      schema: RepositoryStarsSchema,
      baseConfig: { storageType: 'default' },
    }
    ```

  </Tab>
  <Tab value="webhook-handler">
    The secure webhook endpoint that receives GitHub star events, verifies their authenticity, and updates the real-time stream with new star counts.

    ```typescript
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { verifyWebhookSignature } from '../utils/verify-webhook-signature'
    import { checkUserProfile } from '../utils/check-user-profile'

    export const config: ApiRouteConfig = {
      type: 'api',
      name: 'GitHubStarWebhook',
      description: 'Process GitHub star webhook events with signature verification',
      method: 'POST',
      path: '/webhooks/github/star',
      bodySchema: z.object({
        action: z.enum(['created', 'deleted']),
        starred_at: z.string().optional(),
        repository: z.object({
          name: z.string(),
          full_name: z.string(),
          stargazers_count: z.number(),
          owner: z.object({ login: z.string() }),
        }),
        sender: z.object({
          login: z.string(),
          name: z.string(),
          avatar_url: z.string().optional(),
          html_url: z.string(),
          url: z.string({ description: 'API URL' }),
        }),
      }),
      responseSchema: {
        200: z.object({
          message: z.string(),
          event: z.string(),
          processed: z.boolean(),
        }),
        400: z.object({ error: z.string() }),
        401: z.object({ error: z.string() }),
        500: z.object({ error: z.string() }),
      },
      emits: [],
      flows: ['github-star-processing'],
    }

    export const handler: Handlers['GitHubStarWebhook'] = async (
      req,
      { logger, streams, state, traceId }
    ) => {
      try {
        // Extract and validate GitHub headers
        const githubEvent = req.headers['x-github-event'] as string
        const githubDelivery = req.headers['x-github-delivery'] as string
        const githubSignature = req.headers['x-hub-signature-256'] as string
        const githubSignatureSha1 = req.headers['x-hub-signature'] as string

        // Only process star events
        if (githubEvent !== 'star') {
          logger.info('Ignoring non-star event', { githubEvent, githubDelivery })

          return {
            status: 200,
            body: {
              message: 'Event ignored - only processing star events',
              event: githubEvent,
              processed: false,
            },
          }
        }

        // Verify webhook signature if secret is configured
        const webhookSecret = process.env.GITHUB_WEBHOOK_SECRET

        if (webhookSecret) {
          logger.info('Verifying webhook signature', {
            delivery: githubDelivery,
            event: githubEvent,
          })

          const isValidSignature = verifyWebhookSignature({
            payload: JSON.stringify(req.body),
            signature: githubSignature || githubSignatureSha1,
            secret: webhookSecret,
            algorithm: githubSignature ? 'sha256' : 'sha1',
          })

          if (!isValidSignature) {
            logger.warn('Invalid webhook signature', {
              delivery: githubDelivery,
              event: githubEvent,
            })

            return {
              status: 401,
              body: { error: 'Invalid webhook signature' },
            }
          }
        }

        // Extract repository and user data
        const repository = {
          fullName: req.body.repository.full_name,
          name: req.body.repository.name,
          organization: req.body.repository.owner.login,
        }

        const sender = {
          name: req.body.sender.name,
          login: req.body.sender.login,
          avatarUrl: req.body.sender.avatar_url,
          url: req.body.sender.html_url,
          apiUrl: req.body.sender.url,
        }

        // Prepare star data for stream
        const webhookData = {
          fullName: repository.fullName,
          name: repository.name,
          organization: repository.organization,
          lastUpdated: req.body.starred_at || new Date().toISOString(),
          stars: req.body.repository.stargazers_count,
        }

        // Update real-time stream - this automatically propagates to all clients!
        await streams.stars.set(repository.organization, repository.name, webhookData)

        logger.info('GitHub star webhook processed successfully', { ...webhookData, sender })

        // Optional: Fetch additional user profile data
        if (sender.apiUrl) {
          try {
            logger.info('Getting GitHub user profile', { apiUrl: sender.apiUrl })
            const userProfile = await checkUserProfile(sender.apiUrl)
            await state.set(repository.fullName, traceId, userProfile)
            logger.info('GitHub user profile', { userProfile })
          } catch (error: any) {
            logger.error('Failed to get GitHub user profile', { error: error.message })
          }
        }

        return {
          status: 200,
          body: {
            message: 'Star webhook processed successfully',
            event: githubEvent,
            processed: true,
          },
        }
      } catch (error: any) {
        logger.error('GitHub star webhook processing failed', {
          error: error.message,
          stack: error.stack,
        })

        return {
          status: 500,
          body: { error: 'Star webhook processing failed' },
        }
      }
    }
    ```

  </Tab>
  <Tab value="signature-verification">
    Production-ready webhook security that verifies GitHub webhook signatures using HMAC cryptographic validation to ensure requests are authentic.

    ```typescript
    import crypto from 'crypto'

    type Args = {
      payload: string
      signature: string
      secret: string
      algorithm: 'sha1' | 'sha256'
    }

    export function verifyWebhookSignature(args: Args): boolean {
      const { payload, signature, secret, algorithm = 'sha256' } = args

      try {
        if (!signature) return false

        // Generate expected signature using HMAC
        const expectedSignature =
          algorithm === 'sha256'
            ? `sha256=${crypto.createHmac('sha256', secret).update(payload, 'utf8').digest('hex')}`
            : `sha1=${crypto.createHmac('sha1', secret).update(payload, 'utf8').digest('hex')}`

        // Use timing-safe comparison to prevent timing attacks
        return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))
      } catch (error) {
        return false
      }
    }
    ```

  </Tab>
  <Tab value="user-profile">
    Optional GitHub user profile fetching that enriches webhook events with additional user information for analytics and user insights.

    ```typescript
    export interface GitHubUserProfile {
      login: string
      id: number
      node_id: string
      avatar_url: string
      gravatar_id: string
      url: string
      html_url: string
      followers_url: string
      following_url: string
      gists_url: string
      starred_url: string
      subscriptions_url: string
      organizations_url: string
      repos_url: string
      events_url: string
      received_events_url: string
      type: string
      user_view_type: string
      site_admin: boolean
      name: string | null
      company: string | null
      blog: string
      location: string | null
      email: string | null
      hireable: boolean | null
      bio: string | null
      twitter_username: string | null
      public_repos: number
      public_gists: number
      followers: number
      following: number
      created_at: string
      updated_at: string
    }

    export interface GitHubUserProfileResponse {
      followers: number
      bio: string | null
      email: string | null
      htmlUrl: string
      name: string | null
      login: string
      location: string | null
    }

    export const checkUserProfile = async (apiUrl: string): Promise<GitHubUserProfileResponse> => {
      const response = await fetch(apiUrl)
      const data = (await response.json()) as GitHubUserProfile

      return {
        followers: data.followers,
        bio: data.bio,
        email: data.email,
        htmlUrl: data.html_url,
        name: data.name,
        login: data.login,
        location: data.location,
      }
    }
    ```

  </Tab>
</Tabs>

---

## Real-Time Data Flow

The beauty of this architecture lies in its simplicity. Here's how real-time updates flow through the system:

1. **GitHub Event** → User stars/unstars your repository
2. **Webhook Delivery** → GitHub sends POST request to your endpoint  
3. **Security Validation** → Signature verification ensures request authenticity
4. **Stream Update** → Data is written to Motia stream with `streams.stars.set()`
5. **Live Propagation** → All connected clients automatically receive the update
6. **UI Updates** → Client applications re-render with new star count

**No manual WebSocket management, no connection handling, no state synchronization code required!**

---

## Key Features & Benefits

### ⚡ **Instant Real-Time Updates**
Stars update across all connected clients the moment GitHub sends the webhook - no polling, no delays.

### 🔐 **Production-Ready Security**  
HMAC signature verification with timing-safe comparison prevents unauthorized webhook requests.

### 🧩 **Minimal Architecture**
Just two components handle the complete real-time functionality - no complex infrastructure required.

### 📊 **Automatic State Management**
Motia streams handle data persistence, synchronization, and client updates automatically.

### 🎯 **Type-Safe Development**
Full TypeScript integration with Zod validation ensures zero runtime surprises.

### 🌐 **Live Production Usage**
This exact implementation powers the real-time counter visible in the Motia website header - go check it out now!

### 🚀 **Production-Grade Architecture**
Built for enterprise scale with proper error handling, security, monitoring, and deployment automation.

---

## Trying It Out

Ready to build your own real-time GitHub stars counter? Let's get it running.

<Steps>

### Clone and Install

Start by getting the project locally and installing dependencies.

```shell
git clone https://github.com/MotiaDev/github-stars-counter.git
cd github-stars-counter
npm install
```

### Configure GitHub Webhook (Optional)

Set up webhook security with a secret for production use. This is optional for testing but essential for production deployments.

```shell
# Generate a secure random secret
export GITHUB_WEBHOOK_SECRET=$(openssl rand -hex 32)
echo "GITHUB_WEBHOOK_SECRET=$GITHUB_WEBHOOK_SECRET" >> .env
```

### Start Development Server

Launch the Motia development server to begin receiving webhook events.

```shell
npm run dev
```

Your webhook endpoint will be available at: `http://localhost:3000/webhooks/github/star`

### Set Up GitHub Webhook

Configure GitHub to send star events to your endpoint:

1. Go to your GitHub repository settings
2. Navigate to **Settings** → **Webhooks**  
3. Click **Add webhook**
4. Set **Payload URL** to your endpoint (use ngrok for local testing)
5. Set **Content type** to `application/json`
6. Add your webhook secret if configured
7. Select **Individual events** → **Stars**
8. Click **Add webhook**

### Test the Real-Time Updates

Test your webhook by starring/unstarring your repository:

1. **Star your repository** on GitHub
2. **Check the logs** - you should see webhook processing
3. **Access the stream** - query `/api/streams/stars` to see current data
4. **Watch real-time updates** in the Motia Workbench

### Access Real-Time Data

Your star data is now available via the Motia streams API:

```shell
# Get all repository star counts
curl http://localhost:3000/api/streams/stars

# Get specific repository star count  
curl http://localhost:3000/api/streams/stars/{org}/{repo}
```

The response includes live star counts that update automatically whenever GitHub sends webhook events.

### Deploy to Production

Once your counter is working locally, deploy it to production with Motia Cloud:

**Option 1: CLI Deployment**
```shell
# Deploy with version and API key
motia cloud deploy --api-key your-api-key --version-name 1.0.0

# Deploy with environment variables
motia cloud deploy --api-key your-api-key \
  --version-name 1.0.0 \
  --env-file .env.production \
  --environment-id your-env-id
```

**Option 2: One-Click Web Deployment**
1. Ensure your local project is running (`npm run dev`)
2. Go to [Motia Cloud -> Import from Workbench](https://motia.cloud)
3. Select your local project port
4. Choose project and environment name
5. Upload environment variables (optional)
6. Click **Deploy** and watch the magic happen! ✨

</Steps>

---

## 🚀 Production Deployment Guide

### Environment Variables

Configure these environment variables for production security and functionality:

```shell
# Required: GitHub webhook secret for security
GITHUB_WEBHOOK_SECRET="your-secure-random-secret"

# Optional: GitHub personal access token for enhanced API limits
GITHUB_TOKEN="ghp_your_github_token"
```

### Security Best Practices

For production deployments, ensure you:

1. **Generate secure webhook secrets**: 
   ```shell
   # Generate a cryptographically secure secret
   openssl rand -hex 32
   ```

2. **Store secrets securely**: Use environment variables, never commit to code

3. **Monitor webhook signatures**: The handler automatically verifies signatures when `GITHUB_WEBHOOK_SECRET` is set

4. **Enable logging**: Monitor for signature verification failures and unauthorized requests

### Scaling Considerations

This architecture scales automatically with your traffic:

- **Multiple repositories**: Each repo gets its own stream key (`org/repo`)
- **High concurrency**: Motia streams handle thousands of concurrent connections
- **Global distribution**: Deploy to multiple regions for worldwide performance
- **Cost optimization**: Pay only for actual usage with serverless scaling

---

## 💻 Dive into the Code

Want to explore the complete real-time implementation? Check out the full source code and see how simple real-time features can be with Motia:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Live GitHub Stars Counter</h3>
        <p className="text-gray-600 mb-4">Access the complete implementation with webhook security, real-time streams, and production deployment configurations. See exactly how the Motia website's live counter works!</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/github-stars-counter" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Stars Counter Code
          </a>
          <a 
            href="https://motia.dev" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            See It Live in Header →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Real-Time Made Simple

This GitHub stars counter demonstrates how Motia transforms complex real-time development into simple, manageable components. With just two files and minimal configuration, we've built a production-ready system that handles webhook security, real-time synchronization, and live client updates.

The beauty of this approach is its scalability and extensibility:
- **Add more repositories**: Each gets its own stream automatically
- **Enhance with analytics**: Track starring patterns and user insights
- **Multiple notification channels**: Slack, Discord, email alerts for milestones
- **Rich frontend integrations**: React, Vue, vanilla JS - all work seamlessly

Key architectural benefits:
- **No WebSocket complexity**: Streams handle all real-time synchronization automatically
- **Built-in security**: Production-ready webhook verification out of the box
- **Type safety**: Full TypeScript support prevents runtime errors
- **Zero configuration**: Real-time features work with no additional setup

This exact implementation powers the live star counter you see in the header of [Motia.dev](https://motia.dev) - that 7953+ count updating in real-time? It's this code in action, proven at enterprise scale with thousands of daily visitors.

**Production Metrics:**
- Handles 10,000+ webhook events per day
- Sub-50ms response times globally  
- 99.9% uptime with automatic failover
- Zero maintenance serverless architecture

Ready to add enterprise-grade real-time features to your applications? Deploy production-ready code with Motia today!



-   [gmail-automation](/docs/examples/gmail-automation): Documentation for gmail-automation.
---
title: 'Gmail Automation'
description: Build an automated email system with smart labeling, auto-responses, and AI-powered filtering
---

import { GmailTab } from '../../../components/GmailCodeFetcher'

## Let's build a Gmail automation system that:

- 📊 Smart email classification by category (work, personal, social, promotion, spam, update)
- 🚨 Urgency detection (high, medium, low) with prioritization
- 💬 Intelligent automated responses based on email context
- 🏷️ Automatic email organization (labeling, archiving)
- 📈 Daily summary reports via Discord
- 🔒 Secure Gmail API integration with OAuth2 authentication flow
- ⚡ Real-time email monitoring with webhook notifications

## The Steps

<Folder name="steps" defaultOpen>
  <File name="analyze-email.step.py" />
  <File name="auto-responder.step.ts" />
  <File name="daily-summary.step.ts" />
  <File name="fetch-email.step.ts" />
  <File name="gmail-webhook.step.ts" />
  <File name="organize-email.step.ts" />
</Folder>

<Tabs items={['webhook', 'analyze-email', 'auto-responder', 'daily-summary', 'fetch-email', 'organize-email']}>
  <GmailTab tab="webhook" value="gmail-webhook" />
  <GmailTab tab="analyze-email" value="analyze-email" fileExtension="py" />
  <GmailTab tab="auto-responder" value="auto-responder" />
  <GmailTab tab="daily-summary" value="daily-summary" />
  <GmailTab tab="fetch-email" value="fetch-email" />
  <GmailTab tab="organize-email" value="organize-email" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: Gmail Automation Steps](../img/gmail-automation.png)</div>

## 🌊 Workflow Architecture

The Gmail Account Manager workflow consists of the following steps:

### 1. Gmail Authentication (Multi-Step Flow)
- **Files**: 
  - `steps/gmail-get-auth-url.step.ts`: Generates OAuth2 authorization URL
  - `steps/gmail-auth.step.ts`: Handles authorization code exchange
  - `steps/gmail-token-status.step.ts`: Checks token validity and refreshes if needed

### 2. Gmail Webhook (API Step)
- **File**: `steps/gmail-webhook.step.ts`
- **Purpose**: Receives notifications from Gmail when new emails arrive
- **Emits**: `gmail.new_email` event with message details
- **Endpoint**: `POST /api/gmail-webhook`

### 3. Gmail Watch (API Step)
- **File**: `steps/gmail-watch.step.ts`
- **Purpose**: Sets up push notifications for the Gmail account
- **Endpoint**: `GET /api/watch`

### 4. Fetch Email (Event Step)
- **File**: `steps/fetch-email.step.ts`
- **Purpose**: Retrieves the full email content from Gmail API
- **Subscribes to**: `gmail.email.received`
- **Emits**: `gmail.email.fetched` with complete email data
- **Key Functions**: Authenticates with Gmail API, fetches message content, parses attachments

### 5. Analyze Email (Event Step)
- **File**: `steps/analyze-email.step.py`
- **Purpose**: Uses Hugging Face models to analyze email content
- **Subscribes to**: `gmail.email.fetched`
- **Emits**: `gmail.email.analyzed` with analysis results
- **Analysis Performed**: 
  - Category classification
  - Urgency detection
  - Sentiment analysis
  - Key information extraction

### 6. Organize Email (Event Step)
- **File**: `steps/organize-email.step.ts`
- **Purpose**: Applies labels and organization based on analysis
- **Subscribes to**: `gmail.email.analyzed`
- **Emits**: `[gmail.email.organized, gmail.email.archived]`
- **Actions**: Creates/applies labels, archives certain emails, marks importance

### 7. Auto-Respond to Email (Event Step)
- **File**: `steps/auto-responder.step.ts`
- **Purpose**: Generates and sends appropriate responses for certain emails
- **Subscribes to**: `gmail.email.analyzed`
- **Emits**: `gmail.email.responded`
- **Features**: 
  - Template selection based on email context
  - Personalization of responses
  - Auto-reply for urgent messages
  - Follow-up scheduling

### 8. Daily Summary (Cron Step)
- **File**: `steps/daily-summary.step.ts`
- **Purpose**: Compiles and sends daily email activity summary
- **Schedule**: Runs daily at 6:00 PM
- **Emits**: `gmail.summary.sent`
- **Delivery**: Sends report to Discord via webhook

## Try It Out

<Steps>
## 📋 Prerequisites

- **Node.js** (v18+)
- **Python** (v3.8+)
- **Gmail API credentials** (client_id and client_secret)
- **Google Cloud project** with Pub/Sub API enabled
- **Hugging Face API token**
- **Discord webhook URL** (for daily summaries)

## 🚀 Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/gmail-flow.git
   cd gmail-flow
   ```

2. **Install Node.js dependencies**
   ```bash
   pnpm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your credentials (see setup sections below).

5. **Start the development server**
   ```bash
   pnpm dev
   ```

6. **Open the Motia Workbench**
   
   Navigate to [http://localhost:3000](http://localhost:3000) to access the workflow UI.

## 🔧 Detailed Setup

### Setting up Google Cloud Project and Gmail API

Before you can use the Gmail Account Manager, you need to set up a Google Cloud project with the Gmail API and Pub/Sub:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click on "New Project" and follow the steps to create a new project
   - Note your project ID for later use

2. **Enable the Gmail API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Gmail API" and click on it
   - Click "Enable"

3. **Enable the Pub/Sub API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Cloud Pub/Sub API" and click on it
   - Click "Enable"

4. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Set the application type to "Desktop app"
   - Click "Create"
   - Note your Client ID and Client Secret for your `.env` file:
     ```
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```

### Setting up Google Pub/Sub for Gmail Notifications

To enable real-time email notifications, you need to set up a Google Cloud Pub/Sub topic and subscription:

1. **Create a Pub/Sub Topic**:
   - In your Google Cloud Console, go to "Pub/Sub" > "Topics"
   - Click "Create Topic"
   - Name your topic (e.g., `gmail-notifications`)
   - Add the service account `gmail-api-push@system.gserviceaccount.com` as a Topic Publisher to allow Gmail to publish notifications
   - Click "Create"
   - Note the full topic name (usually `projects/your-project-id/topics/gmail-notifications`) for your `.env` file:
     ```
     GOOGLE_PUBSUB_TOPIC=projects/your-project-id/topics/gmail-notifications
     ```

2. **Create a Pub/Sub Subscription**:
   - Once your topic is created, click "Create Subscription"
   - Name your subscription (e.g., `gmail-notifications-push`)
   - Set the Delivery Type to "Push"
   - Set the Endpoint URL to your webhook URL (e.g., `https://your-domain.com/api/gmail-webhook`)
     - For local development, you'll need to use a tool like ngrok to expose your local server
   - Click "Create"

3. **Set up Domain Verification** (if needed):
   - If you're using a custom domain for your webhook endpoint, you may need to verify domain ownership
   - Follow the instructions in Google Cloud Console for domain verification

### Gmail API Authentication

This project includes a complete OAuth2 authentication flow for the Gmail API:

1. Start the development server: `pnpm dev`
2. Navigate to the authentication workflow in the Motia Workbench
3. The workflow will generate an authorization URL
4. Open the URL in your browser and authorize the application
5. The application will receive and store your authentication tokens

### Discord Webhook Configuration

To receive daily email summaries in Discord, follow these steps to set up a webhook:

1. **Create a Discord Server** (skip if you already have one):
   - Open Discord and click the "+" icon on the left sidebar
   - Select "Create My Own" and follow the setup wizard

2. **Create a Channel for Notifications**:
   - Right-click on your server name and select "Server Settings"
   - Go to "Channels" and click "Create Channel"
   - Name it (e.g., "email-summaries") and click "Create"

3. **Create a Webhook**:
   - Right-click on your new channel and select "Edit Channel"
   - Go to "Integrations" tab
   - Click "Create Webhook"
   - Give it a name (e.g., "Gmail Summary Bot")
   - Optionally, customize the avatar
   - Click "Copy Webhook URL"

4. **Add Webhook URL to Environment Variables**:
   - Open your `.env` file
   - Add or update the Discord webhook URL:
     ```
     DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url
     ```

5. **Test the Webhook**:
   - You can test if your webhook is working correctly with this curl command:
     ```bash
     curl -X POST -H "Content-Type: application/json" \
     -d '{"content": "Testing Gmail Account Manager webhook"}' \
     https://discord.com/api/webhooks/your-webhook-url
     ```
   - You should see the message appear in your Discord channel

### Hugging Face Setup

1. **Create a Hugging Face Account**:
   - Sign up at [Hugging Face](https://huggingface.co/join)

2. **Generate an API Token**:
   - Go to your [Hugging Face account settings](https://huggingface.co/settings/tokens)
   - Create a new API token
   - Copy the token to your `.env` file:
     ```
     HUGGINGFACE_API_TOKEN=your_api_token
     ```

</Steps>

## 📁 Project Structure

- `steps/` - Contains all workflow steps
  - `gmail-get-auth-url.step.ts` - Generates OAuth2 URL
  - `gmail-auth.step.ts` - Handles OAuth2 flow
  - `gmail-token-status.step.ts` - Manages token refresh
  - `gmail-webhook.step.ts` - Webhook endpoint for Gmail notifications
  - `gmail-watch.step.ts` - Sets up Gmail push notifications
  - `fetch-email.step.ts` - Fetches email content from Gmail API
  - `analyze-email.step.py` - Python step for email analysis using Hugging Face
  - `organize-email.step.ts` - Organizes emails (labels, archives)
  - `auto-responder.step.ts` - Generates appropriate responses
  - `daily-summary.step.ts` - Sends daily summary to Discord
- `services/` - Shared service modules
- `config/` - Configuration files
- `.motia/` - Motia framework configuration

## 📦 Dependencies

### Node.js Dependencies
- **@motiadev/core**, **@motiadev/workbench**, **motia**: Motia framework
- **googleapis**, **google-auth-library**: Google API integration
- **gmail-api-parse-message-ts**: Gmail message parsing
- **axios**: HTTP client
- **zod**: Schema validation
- **react**: UI components

### Python Dependencies
- **transformers**, **torch**: Machine learning models
- **scikit-learn**, **numpy**, **pandas**: Data processing
- **huggingface_hub**: Access to Hugging Face models
- **python-dotenv**: Environment variable loading

## 🛠️ Troubleshooting

- **Python Module Errors**: Ensure you've installed all required Python packages with `pip install -r requirements.txt`
- **Authentication Errors**: Verify your API credentials and follow the authentication flow
- **Webhook Issues**: Make sure the webhook endpoint is publicly accessible or properly configured for testing
- **Token Refresh Errors**: Check that your OAuth tokens are valid and that the refresh flow is working properly
- **Pub/Sub Not Working**: Verify that your Pub/Sub topic and subscription are properly configured and that your service account has the necessary permissions

## 📝 Environment Variables

Create a `.env` file with the following variables:

```
# Google API Configuration
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_PUBSUB_TOPIC=projects/your-project-id/topics/gmail-notifications

# HuggingFace Configuration
HUGGINGFACE_API_TOKEN=your_huggingface_token

# Discord Integration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url

# Auto-Responder Configuration
AUTO_RESPONDER_NAME=Your Name
AUTO_RESPONDER_EMAIL=your-email@example.com
```



## Examples
[gmail-automation](/docs/examples/gmail-automation): Code example
---
title: 'Gmail Automation'
description: Build an automated email system with smart labeling, auto-responses, and AI-powered filtering
---

import { GmailTab } from '../../../components/GmailCodeFetcher'

## Let's build a Gmail automation system that:

- 📊 Smart email classification by category (work, personal, social, promotion, spam, update)
- 🚨 Urgency detection (high, medium, low) with prioritization
- 💬 Intelligent automated responses based on email context
- 🏷️ Automatic email organization (labeling, archiving)
- 📈 Daily summary reports via Discord
- 🔒 Secure Gmail API integration with OAuth2 authentication flow
- ⚡ Real-time email monitoring with webhook notifications

## The Steps

<Folder name="steps" defaultOpen>
  <File name="analyze-email.step.py" />
  <File name="auto-responder.step.ts" />
  <File name="daily-summary.step.ts" />
  <File name="fetch-email.step.ts" />
  <File name="gmail-webhook.step.ts" />
  <File name="organize-email.step.ts" />
</Folder>

<Tabs items={['webhook', 'analyze-email', 'auto-responder', 'daily-summary', 'fetch-email', 'organize-email']}>
  <GmailTab tab="webhook" value="gmail-webhook" />
  <GmailTab tab="analyze-email" value="analyze-email" fileExtension="py" />
  <GmailTab tab="auto-responder" value="auto-responder" />
  <GmailTab tab="daily-summary" value="daily-summary" />
  <GmailTab tab="fetch-email" value="fetch-email" />
  <GmailTab tab="organize-email" value="organize-email" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: Gmail Automation Steps](../img/gmail-automation.png)</div>

## 🌊 Workflow Architecture

The Gmail Account Manager workflow consists of the following steps:

### 1. Gmail Authentication (Multi-Step Flow)
- **Files**: 
  - `steps/gmail-get-auth-url.step.ts`: Generates OAuth2 authorization URL
  - `steps/gmail-auth.step.ts`: Handles authorization code exchange
  - `steps/gmail-token-status.step.ts`: Checks token validity and refreshes if needed

### 2. Gmail Webhook (API Step)
- **File**: `steps/gmail-webhook.step.ts`
- **Purpose**: Receives notifications from Gmail when new emails arrive
- **Emits**: `gmail.new_email` event with message details
- **Endpoint**: `POST /api/gmail-webhook`

### 3. Gmail Watch (API Step)
- **File**: `steps/gmail-watch.step.ts`
- **Purpose**: Sets up push notifications for the Gmail account
- **Endpoint**: `GET /api/watch`

### 4. Fetch Email (Event Step)
- **File**: `steps/fetch-email.step.ts`
- **Purpose**: Retrieves the full email content from Gmail API
- **Subscribes to**: `gmail.email.received`
- **Emits**: `gmail.email.fetched` with complete email data
- **Key Functions**: Authenticates with Gmail API, fetches message content, parses attachments

### 5. Analyze Email (Event Step)
- **File**: `steps/analyze-email.step.py`
- **Purpose**: Uses Hugging Face models to analyze email content
- **Subscribes to**: `gmail.email.fetched`
- **Emits**: `gmail.email.analyzed` with analysis results
- **Analysis Performed**: 
  - Category classification
  - Urgency detection
  - Sentiment analysis
  - Key information extraction

### 6. Organize Email (Event Step)
- **File**: `steps/organize-email.step.ts`
- **Purpose**: Applies labels and organization based on analysis
- **Subscribes to**: `gmail.email.analyzed`
- **Emits**: `[gmail.email.organized, gmail.email.archived]`
- **Actions**: Creates/applies labels, archives certain emails, marks importance

### 7. Auto-Respond to Email (Event Step)
- **File**: `steps/auto-responder.step.ts`
- **Purpose**: Generates and sends appropriate responses for certain emails
- **Subscribes to**: `gmail.email.analyzed`
- **Emits**: `gmail.email.responded`
- **Features**: 
  - Template selection based on email context
  - Personalization of responses
  - Auto-reply for urgent messages
  - Follow-up scheduling

### 8. Daily Summary (Cron Step)
- **File**: `steps/daily-summary.step.ts`
- **Purpose**: Compiles and sends daily email activity summary
- **Schedule**: Runs daily at 6:00 PM
- **Emits**: `gmail.summary.sent`
- **Delivery**: Sends report to Discord via webhook

## Try It Out

<Steps>
## 📋 Prerequisites

- **Node.js** (v18+)
- **Python** (v3.8+)
- **Gmail API credentials** (client_id and client_secret)
- **Google Cloud project** with Pub/Sub API enabled
- **Hugging Face API token**
- **Discord webhook URL** (for daily summaries)

## 🚀 Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/gmail-flow.git
   cd gmail-flow
   ```

2. **Install Node.js dependencies**
   ```bash
   pnpm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your credentials (see setup sections below).

5. **Start the development server**
   ```bash
   pnpm dev
   ```

6. **Open the Motia Workbench**
   
   Navigate to [http://localhost:3000](http://localhost:3000) to access the workflow UI.

## 🔧 Detailed Setup

### Setting up Google Cloud Project and Gmail API

Before you can use the Gmail Account Manager, you need to set up a Google Cloud project with the Gmail API and Pub/Sub:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click on "New Project" and follow the steps to create a new project
   - Note your project ID for later use

2. **Enable the Gmail API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Gmail API" and click on it
   - Click "Enable"

3. **Enable the Pub/Sub API**:
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Cloud Pub/Sub API" and click on it
   - Click "Enable"

4. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Set the application type to "Desktop app"
   - Click "Create"
   - Note your Client ID and Client Secret for your `.env` file:
     ```
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```

### Setting up Google Pub/Sub for Gmail Notifications

To enable real-time email notifications, you need to set up a Google Cloud Pub/Sub topic and subscription:

1. **Create a Pub/Sub Topic**:
   - In your Google Cloud Console, go to "Pub/Sub" > "Topics"
   - Click "Create Topic"
   - Name your topic (e.g., `gmail-notifications`)
   - Add the service account `gmail-api-push@system.gserviceaccount.com` as a Topic Publisher to allow Gmail to publish notifications
   - Click "Create"
   - Note the full topic name (usually `projects/your-project-id/topics/gmail-notifications`) for your `.env` file:
     ```
     GOOGLE_PUBSUB_TOPIC=projects/your-project-id/topics/gmail-notifications
     ```

2. **Create a Pub/Sub Subscription**:
   - Once your topic is created, click "Create Subscription"
   - Name your subscription (e.g., `gmail-notifications-push`)
   - Set the Delivery Type to "Push"
   - Set the Endpoint URL to your webhook URL (e.g., `https://your-domain.com/api/gmail-webhook`)
     - For local development, you'll need to use a tool like ngrok to expose your local server
   - Click "Create"

3. **Set up Domain Verification** (if needed):
   - If you're using a custom domain for your webhook endpoint, you may need to verify domain ownership
   - Follow the instructions in Google Cloud Console for domain verification

### Gmail API Authentication

This project includes a complete OAuth2 authentication flow for the Gmail API:

1. Start the development server: `pnpm dev`
2. Navigate to the authentication workflow in the Motia Workbench
3. The workflow will generate an authorization URL
4. Open the URL in your browser and authorize the application
5. The application will receive and store your authentication tokens

### Discord Webhook Configuration

To receive daily email summaries in Discord, follow these steps to set up a webhook:

1. **Create a Discord Server** (skip if you already have one):
   - Open Discord and click the "+" icon on the left sidebar
   - Select "Create My Own" and follow the setup wizard

2. **Create a Channel for Notifications**:
   - Right-click on your server name and select "Server Settings"
   - Go to "Channels" and click "Create Channel"
   - Name it (e.g., "email-summaries") and click "Create"

3. **Create a Webhook**:
   - Right-click on your new channel and select "Edit Channel"
   - Go to "Integrations" tab
   - Click "Create Webhook"
   - Give it a name (e.g., "Gmail Summary Bot")
   - Optionally, customize the avatar
   - Click "Copy Webhook URL"

4. **Add Webhook URL to Environment Variables**:
   - Open your `.env` file
   - Add or update the Discord webhook URL:
     ```
     DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url
     ```

5. **Test the Webhook**:
   - You can test if your webhook is working correctly with this curl command:
     ```bash
     curl -X POST -H "Content-Type: application/json" \
     -d '{"content": "Testing Gmail Account Manager webhook"}' \
     https://discord.com/api/webhooks/your-webhook-url
     ```
   - You should see the message appear in your Discord channel

### Hugging Face Setup

1. **Create a Hugging Face Account**:
   - Sign up at [Hugging Face](https://huggingface.co/join)

2. **Generate an API Token**:
   - Go to your [Hugging Face account settings](https://huggingface.co/settings/tokens)
   - Create a new API token
   - Copy the token to your `.env` file:
     ```
     HUGGINGFACE_API_TOKEN=your_api_token
     ```

</Steps>

## 📁 Project Structure

- `steps/` - Contains all workflow steps
  - `gmail-get-auth-url.step.ts` - Generates OAuth2 URL
  - `gmail-auth.step.ts` - Handles OAuth2 flow
  - `gmail-token-status.step.ts` - Manages token refresh
  - `gmail-webhook.step.ts` - Webhook endpoint for Gmail notifications
  - `gmail-watch.step.ts` - Sets up Gmail push notifications
  - `fetch-email.step.ts` - Fetches email content from Gmail API
  - `analyze-email.step.py` - Python step for email analysis using Hugging Face
  - `organize-email.step.ts` - Organizes emails (labels, archives)
  - `auto-responder.step.ts` - Generates appropriate responses
  - `daily-summary.step.ts` - Sends daily summary to Discord
- `services/` - Shared service modules
- `config/` - Configuration files
- `.motia/` - Motia framework configuration

## 📦 Dependencies

### Node.js Dependencies
- **@motiadev/core**, **@motiadev/workbench**, **motia**: Motia framework
- **googleapis**, **google-auth-library**: Google API integration
- **gmail-api-parse-message-ts**: Gmail message parsing
- **axios**: HTTP client
- **zod**: Schema validation
- **react**: UI components

### Python Dependencies
- **transformers**, **torch**: Machine learning models
- **scikit-learn**, **numpy**, **pandas**: Data processing
- **huggingface_hub**: Access to Hugging Face models
- **python-dotenv**: Environment variable loading

## 🛠️ Troubleshooting

- **Python Module Errors**: Ensure you've installed all required Python packages with `pip install -r requirements.txt`
- **Authentication Errors**: Verify your API credentials and follow the authentication flow
- **Webhook Issues**: Make sure the webhook endpoint is publicly accessible or properly configured for testing
- **Token Refresh Errors**: Check that your OAuth tokens are valid and that the refresh flow is working properly
- **Pub/Sub Not Working**: Verify that your Pub/Sub topic and subscription are properly configured and that your service account has the necessary permissions

## 📝 Environment Variables

Create a `.env` file with the following variables:

```
# Google API Configuration
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_PUBSUB_TOPIC=projects/your-project-id/topics/gmail-notifications

# HuggingFace Configuration
HUGGINGFACE_API_TOKEN=your_huggingface_token

# Discord Integration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url

# Auto-Responder Configuration
AUTO_RESPONDER_NAME=Your Name
AUTO_RESPONDER_EMAIL=your-email@example.com
```


-   [Examples](/docs/examples): Documentation for Examples.
---
title: Examples
---

We have curated examples to help you learn Motia, organized by complexity from basic concepts to production-ready implementations.

## 📚 Basic Examples
Start here to learn core Motia concepts with straightforward implementations.

<Cards>
  <Card
    title="Sentiment Analysis"
    href="/docs/examples/sentiment-analysis"
    description="Learn dynamic workflows with LLM-driven decision making and event routing"
  />
  <Card
    title="Multi-Language Processing"
    href="/docs/examples/multi-language-data-processing"
    description="Combine TypeScript, Python, and JavaScript in unified data pipelines"
  />
</Cards>

## 🔧 Intermediate Examples
Build more complex workflows with integrations and advanced patterns.

<Cards>
  <Card
    title="AI Content Moderation"
    href="/docs/examples/ai-content-moderation"
    description="Human-in-the-loop content moderation with AI analysis and Slack integration"
  />
  <Card
    title="RAG PDF Analyzer"
    href="/docs/examples/rag-docling-weaviate"
    description="Intelligent document processing with Docling and Weaviate vector database"
  />
  <Card
    title="Trello Automation"
    href="/docs/examples/trello-automation"
    description="Automated card progression system with AI-powered summaries and notifications"
  />
</Cards>

## 🏭 Production Examples
Enterprise-ready implementations handling real traffic at scale.

<Cards>
  <Card
    title="Uptime Monitor"
    href="/docs/examples/uptime-discord-monitor"
    description="Complete monitoring system with smart alerting and Discord integration"
  />
  <Card
    title="GitHub Stars Counter"
    href="/docs/examples/github-stars-counter"
    description="Real-time stars counter with secure webhooks and live streaming"
  />
  <Card
    title="GitHub Integration"
    href="/docs/examples/github-integration-workflow"
    description="Automated issue and PR management with AI-powered classification and routing"
  />
  <Card
    title="Gmail Automation"
    href="/docs/examples/gmail-automation"
    description="Smart email classification, auto-responses, and AI-powered filtering with OAuth2"
  />
  <Card
    title="Finance Agent"
    href="/docs/examples/finance-agent"
    description="Event-driven financial analysis with web search and real-time market data"
  />
  <Card
    title="AI Research Agent"
    href="/docs/examples/ai-deep-research-agent"
    description="Comprehensive web research assistant with iterative depth and parallel processing"
  />
</Cards>


<br/>

## 💻 Explore the Source Code

All examples include complete, runnable source code with configuration files, setup instructions, and production-ready implementations:

<div className="not-prose">
  <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Motia Examples Repository</h3>
        <p className="text-gray-600 mb-4">Access complete implementations, step-by-step tutorials, and production-ready configurations for all our examples. Perfect for learning, experimentation, and building your own applications.</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            Repository
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/rag-docling-weaviate-agent" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            RAG Example →
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/motia-uptime-monitor" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            Monitor Example →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

## Contribute

We welcome contributions to the examples. Please submit a PR to the [examples repository](https://github.com/motiadev/motia-examples).



## Examples
[Examples](/docs/examples): Code example
---
title: Examples
---

We have curated examples to help you learn Motia, organized by complexity from basic concepts to production-ready implementations.

## 📚 Basic Examples
Start here to learn core Motia concepts with straightforward implementations.

<Cards>
  <Card
    title="Sentiment Analysis"
    href="/docs/examples/sentiment-analysis"
    description="Learn dynamic workflows with LLM-driven decision making and event routing"
  />
  <Card
    title="Multi-Language Processing"
    href="/docs/examples/multi-language-data-processing"
    description="Combine TypeScript, Python, and JavaScript in unified data pipelines"
  />
</Cards>

## 🔧 Intermediate Examples
Build more complex workflows with integrations and advanced patterns.

<Cards>
  <Card
    title="AI Content Moderation"
    href="/docs/examples/ai-content-moderation"
    description="Human-in-the-loop content moderation with AI analysis and Slack integration"
  />
  <Card
    title="RAG PDF Analyzer"
    href="/docs/examples/rag-docling-weaviate"
    description="Intelligent document processing with Docling and Weaviate vector database"
  />
  <Card
    title="Trello Automation"
    href="/docs/examples/trello-automation"
    description="Automated card progression system with AI-powered summaries and notifications"
  />
</Cards>

## 🏭 Production Examples
Enterprise-ready implementations handling real traffic at scale.

<Cards>
  <Card
    title="Uptime Monitor"
    href="/docs/examples/uptime-discord-monitor"
    description="Complete monitoring system with smart alerting and Discord integration"
  />
  <Card
    title="GitHub Stars Counter"
    href="/docs/examples/github-stars-counter"
    description="Real-time stars counter with secure webhooks and live streaming"
  />
  <Card
    title="GitHub Integration"
    href="/docs/examples/github-integration-workflow"
    description="Automated issue and PR management with AI-powered classification and routing"
  />
  <Card
    title="Gmail Automation"
    href="/docs/examples/gmail-automation"
    description="Smart email classification, auto-responses, and AI-powered filtering with OAuth2"
  />
  <Card
    title="Finance Agent"
    href="/docs/examples/finance-agent"
    description="Event-driven financial analysis with web search and real-time market data"
  />
  <Card
    title="AI Research Agent"
    href="/docs/examples/ai-deep-research-agent"
    description="Comprehensive web research assistant with iterative depth and parallel processing"
  />
</Cards>


<br/>

## 💻 Explore the Source Code

All examples include complete, runnable source code with configuration files, setup instructions, and production-ready implementations:

<div className="not-prose">
  <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Motia Examples Repository</h3>
        <p className="text-gray-600 mb-4">Access complete implementations, step-by-step tutorials, and production-ready configurations for all our examples. Perfect for learning, experimentation, and building your own applications.</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            Repository
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/rag-docling-weaviate-agent" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            RAG Example →
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/motia-uptime-monitor" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            Monitor Example →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

## Contribute

We welcome contributions to the examples. Please submit a PR to the [examples repository](https://github.com/motiadev/motia-examples).


-   [multi-language-data-processing](/docs/examples/multi-language-data-processing): Documentation for multi-language-data-processing.
---
title: 'Multi-Language Processing'
description: 'Multi-Language Data Processing: Building a Unified Pipeline with Motia'
---

Modern backend development often requires combining the strengths of different programming languages. TypeScript for APIs, Python for data processing and AI, JavaScript for rapid prototyping. Traditional approaches involve complex microservices architectures with intricate communication patterns.

This comprehensive guide explores how to build a unified multi-language data processing pipeline using Motia's **step** primitive. We'll cover:

1. **Steps as Core Primitive**: How steps unify different languages under a single abstraction.
2. **Building the Pipeline**: A step-by-step guide to creating a cohesive multi-language data processing workflow.
3. **Unified Execution Model**: How steps enable seamless communication between different runtime environments.
4. **Hands-On Development**: How to build, run, and observe your unified multi-language pipeline.

Let's build a production-ready data processing system where steps unify TypeScript, Python, and JavaScript into a single cohesive workflow.

---

## The Power of Steps: A Unified Multi-Language Primitive

<div className="my-8">![Multi-Language Data Processing in Motia Workbench](/docs-images/motia-build-your-app-2.gif)</div>

At its core, our data processing pipeline demonstrates how **steps** solve the fundamental challenge of multi-language systems: unifying different programming languages under a single, coherent abstraction. Traditional polyglot architectures require complex inter-process communication and deployment coordination. Motia's **step** primitive unifies everything.

**Steps enable true language unification:**

- **[TypeScript](https://www.typescriptlang.org/)** steps: Strong typing and excellent tooling for APIs and orchestration
- **[Python](https://www.python.org/)** steps: Rich ecosystem for data processing, ML, and scientific computing  
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)** steps: Dynamic processing and rapid development
- **[Motia's Step Primitive](https://motia.dev)**: The unifying abstraction that makes all languages work as a single system

Instead of managing multiple services, **steps** provide a single programming model. Whether written in TypeScript, Python, or JavaScript, every step follows the same pattern: receive data, process it, emit events. This unification is what makes multi-language development straightforward.

---

## The Anatomy of Our Multi-Language Pipeline

Our application consists of six specialized steps, each leveraging the optimal language for its specific task. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="01-starter.step.ts" />
  <File name="02-bridge.step.ts" />
  <File name="simple-python_step.py" />
  <File name="notify.step.ts" />
  <File name="04-final.step.ts" />
  <File name="05-summary.step.js" />
</Folder>

<Folder name="types" defaultOpen>
  <File name="index.ts" />
</Folder>

<Tabs items={['api-starter', 'bridge-step', 'python-processor', 'notification-handler', 'finalizer', 'summary-generator']}>
  <Tab value="api-starter">
    The entry point for our multi-language workflow. This TypeScript API endpoint receives data, validates it with Zod schemas, and kicks off the processing pipeline.

```typescript
import { z } from 'zod'

const bodySchema = z.object({
  data: z.record(z.unknown()).optional(),
  message: z.string().optional()
})

// API endpoint to start the multi-language pipeline
export const config = {
  type: 'api',
  name: 'AppStarter',
  description: 'Start the multi-language app pipeline',

  method: 'POST',
  path: '/start-app',

  bodySchema,
  responseSchema: {
    200: z.object({
      message: z.string(),
      appId: z.number(),
      traceId: z.string()
    })
  },

  emits: ['app.started'],
  flows: ['data-processing']
} as const

export const handler = async (req: any, { logger, emit, traceId }: any) => {
  logger.info('🚀 Starting multi-language app', { body: req.body, traceId })
  
  const appData = {
    id: Date.now(),
    input: req.body.data || {},
    started_at: new Date().toISOString(),
    traceId
  }

  // Emit to next step
  await emit({
    topic: 'app.started',
    data: appData
  })

  logger.info('✅ App started successfully', { 
    appId: appData.id,
    traceId 
  })

  return {
    status: 200,
    body: {
      message: 'Multi-language app started successfully',
      appId: appData.id,
      traceId
    }
  }
}
```

  </Tab>
  <Tab value="bridge-step">
    A TypeScript bridge that receives the app start event, processes the data, and forwards it to the Python processing step with proper type transformation.

```typescript
import { z } from 'zod'

// Bridge step to connect app starter to Python processing
export const config = {
  type: 'event',
  name: 'AppBridge',
  description: 'Bridge between app start and Python processing',
  subscribes: ['app.started'],
  emits: ['data.processed'],
  input: z.object({
    id: z.number(),
    input: z.record(z.unknown()),
    started_at: z.string(),
    traceId: z.string()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('🌉 Processing app data and sending to Python', { appId: input.id })
  
  // Process data for Python step
  const processedResult = {
    original_id: input.id,
    processed_at: input.started_at,
    result: `Processed: ${JSON.stringify(input.input)}`,
    confidence: 0.95,
    model_version: '1.0'
  }

  // Send to Python processing
  await emit({
    topic: 'data.processed', 
    data: processedResult
  })

  logger.info('✅ Data sent to Python processing', { 
    originalId: input.id
  })
}
```

  </Tab>
  <Tab value="python-processor">
    The core data processor written in Python, demonstrating how Python steps integrate seamlessly with the TypeScript workflow while maintaining access to Python's rich ecosystem. Note the `_step.py` naming convention.

```python
import time
from datetime import datetime

# Python processing step configuration
config = {
    "type": "event",
    "name": "ProcessDataPython",
    "description": "Process data using Python capabilities",
    "subscribes": ["data.processed"],
    "emits": ["python.done"],
    "flows": ["data-processing"]
}

async def handler(input_data, ctx):
    """
    Python step that processes data and demonstrates Python capabilities
    """
    logger = ctx.logger
    emit = ctx.emit
    
    # Extract data from input
    original_id = input_data.get("original_id")
    result = input_data.get("result", "")
    
    logger.info(f"🐍 Python processing data for ID: {original_id}")
    
    start_time = time.time()
    
    # Simulate Python data processing
    processed_message = f"Python processed: {result}"
    
    # Add some Python-specific processing
    data_analysis = {
        "word_count": len(result.split()) if isinstance(result, str) else 0,
        "character_count": len(result) if isinstance(result, str) else 0,
        "processed_timestamp": datetime.now().isoformat(),
        "processing_language": "Python 3.x"
    }
    
    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Create result object
    python_result = {
        "id": original_id,
        "python_message": processed_message,
        "processed_by": ["appStarter", "appBridge", "ProcessDataPython"],
        "processing_time": processing_time,
        "analysis": data_analysis
    }
    
    # Emit to next step
    await emit({
        "topic": "python.done",
        "data": python_result
    })
    
    logger.info(f"✅ Python processing completed in {processing_time:.2f}ms")
```

  </Tab>
  <Tab value="notification-handler">
    A TypeScript notification handler that processes the Python results and sends notifications, showing seamless data flow between Python and TypeScript.

```typescript
import { z } from 'zod'

export const config = {
  type: 'event',
  name: 'NotificationHandler',
  description: 'Send notifications after Python processing',
  subscribes: ['python.done'],
  emits: ['notification.sent'],
  input: z.object({
    id: z.number(),
    python_message: z.string(),
    processed_by: z.array(z.string()),
    processing_time: z.number(),
    analysis: z.record(z.unknown()).optional()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('📧 Sending notifications after Python processing', { id: input.id })
  
  // Simulate sending notifications (email, slack, etc.)
  const notification = {
    id: input.id,
    message: `Notification: ${input.python_message}`,
    processed_by: input.processed_by,
    sent_at: new Date().toISOString()
  }

  // Send notification data to final step
  await emit({
    topic: 'notification.sent',
    data: {
      ...notification,
      processing_time: input.processing_time
    }
  })

  logger.info('✅ Notifications sent successfully', { id: input.id })
}
```

  </Tab>
  <Tab value="finalizer">
    A TypeScript finalizer that aggregates all the processing results and prepares the final summary data before handing off to JavaScript for metrics generation.

```typescript
import { z } from 'zod'

// Final step to complete the app - TypeScript
export const config = {
  type: 'event',
  name: 'AppFinalizer',
  description: 'Complete the basic app and log final results',
  subscribes: ['notification.sent'],
  emits: ['app.completed'],
  input: z.object({
    id: z.number(),
    message: z.string(),
    processed_by: z.array(z.string()),
    sent_at: z.string(),
    processing_time: z.number()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('🏁 Finalizing app', { 
    notificationId: input.id,
    message: input.message 
  })
  
  // Create final app summary
  const summary = {
    appId: input.id,
    status: 'completed',
    completed_at: new Date().toISOString(),
    steps_executed: [
      'app-starter',
      'app-bridge', 
      'python-processor',
      'notification-handler',
      'app-finalizer'
    ],
    result: input.message
  }

  // Send to JavaScript summary generator
  await emit({
    topic: 'app.completed',
    data: {
      ...summary,
      total_processing_time: input.processing_time
    }
  })

  logger.info('✅ App finalized successfully', { 
    appId: input.id,
    totalSteps: summary.steps_executed.length
  })
}
```

  </Tab>
  <Tab value="summary-generator">
    The final step uses JavaScript for dynamic summary generation and metrics calculation, showcasing how all three languages work together in a single workflow.

```javascript
// Final summary step - JavaScript
export const config = {
  type: 'event',
  name: 'summaryGenerator',
  description: 'Generate final summary in JavaScript',
  subscribes: ['app.completed'],
  emits: [], // Final step - no further processing needed
  flows: ['data-processing']
}

export const handler = async (input, { logger }) => {
  logger.info('📊 Generating final summary in JavaScript', { 
    appId: input.appId,
    status: input.status 
  })
  
  // Calculate processing metrics
  const processingTime = input.total_processing_time || 0
  const stepsCount = input.steps_executed ? input.steps_executed.length : 0
  
  // Create comprehensive summary
  const summary = {
    appId: input.appId,
    finalStatus: input.status,
    totalSteps: stepsCount,
    processingTimeMs: processingTime,
    languages: ['TypeScript', 'Python', 'JavaScript'],
    summary: `Multi-language app completed successfully with ${stepsCount} steps`,
    result: input.result,
    completedAt: new Date().toISOString(),
    generatedBy: 'javascript-summary-step'
  }
  
  // Log final summary (final step - no emit needed)
  logger.info('✨ Final summary generated successfully', summary)
  
  return summary
}
```

  </Tab>
</Tabs>

---

## Type Definitions

Our unified system uses shared TypeScript types to ensure type safety across the multi-language pipeline:

```typescript
// types/index.ts
export interface AppData {
  id: number
  input: Record<string, unknown>
  started_at: string
  traceId: string
}

export interface ProcessedResult {
  original_id: number
  processed_at: string
  result: string
  confidence: number
  model_version: string
}

export interface PythonResult {
  id: number
  python_message: string
  processed_by: string[]
  processing_time: number
}

export interface NotificationData {
  id: number
  message: string
  processed_by: string[]
  sent_at: string
}

export interface AppSummary {
  appId: number
  status: string
  completed_at: string
  steps_executed: string[]
  result: string
}
```

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your multi-language pipeline, making it easy to trace data flow between TypeScript, Python, and JavaScript steps.

<div className="my-8">![Multi-Language Workflow in Motia Workbench](/docs-images/motia-build-your-app-2.gif)</div>

You can monitor real-time execution, view logs from all languages in a unified interface, and trace the complete data flow from the TypeScript API through Python processing to JavaScript summary generation.

---

## Event Flow Architecture

The pipeline follows a clear event-driven flow that connects all languages seamlessly:

1. **`app.started`** - TypeScript API → TypeScript Bridge
2. **`data.processed`** - TypeScript Bridge → Python Processor  
3. **`python.done`** - Python Processor → TypeScript Notification Handler
4. **`notification.sent`** - TypeScript Notification → TypeScript Finalizer
5. **`app.completed`** - TypeScript Finalizer → JavaScript Summary Generator

Each step only needs to know the events it subscribes to and emits, creating loose coupling while maintaining strong data flow guarantees.

---

## Key Features & Benefits

### 🧩 **Step as Universal Primitive**
Every piece of logic—whether TypeScript, Python, or JavaScript—follows the same step pattern, creating true unification.

### 🌐 **Seamless Language Integration**
Steps eliminate the complexity of multi-language systems by providing a unified programming model.

### 📊 **Unified Development Experience**
Write, debug, and monitor all languages through a single interface and shared execution model.

### ⚡ **Hot Reload Across Languages**
Edit any step in any language and see changes instantly across the entire pipeline.

### 🔄 **Event-Driven Communication**
Steps communicate through events, enabling loose coupling and independent scaling.

### 🎯 **Single Deployment Model**
Deploy all languages together as a cohesive system, not as separate microservices.

### 🐍 **Python Step Naming**
Python steps use the `_step.py` suffix convention for proper module resolution (e.g., `simple-python_step.py`).

---

## Trying It Out

Ready to build your first multi-language Motia application? Let's get it running.

<Steps>

### Create Your Motia App

Start by creating a new Motia project with the interactive setup.

```shell
npx motia@latest create
```

### Navigate and Start Development

Move into your project directory and start the development server.

```shell
cd my-app  # Replace with your project name
npm run dev
```

### Open the Workbench

Navigate to [`http://localhost:3000`](http://localhost:3000) to access the Workbench and run your workflow.

### Test the Multi-Language Pipeline

Send a request to your API endpoint to see the multi-language workflow in action:

```shell
   curl -X POST http://localhost:3000/start-app \
     -H "Content-Type: application/json" \
     -d '{"data": {"test": "value"}, "message": "Hello!"}'
```

Watch in the Workbench as your data flows through:
1. **TypeScript** validation and event emission
2. **TypeScript** bridge processing and forwarding  
3. **Python** data processing with rich logging
4. **TypeScript** notification handling
5. **TypeScript** finalization and aggregation
6. **JavaScript** summary generation and metrics

</Steps>

---

## 💻 Dive into the Code

Want to explore multi-language workflows further? Check out additional examples and the complete source code:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Multi-Language Examples</h3>
        <p className="text-gray-600 mb-4">Access complete multi-language implementations, configuration examples, and learn how to integrate TypeScript, Python, and JavaScript in production applications.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.30 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            Explore Examples
          </a>
          <a 
            href="/docs/getting-started/quick-start" 
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            Quick Start →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Power of Unification Through Steps

This multi-language data processing pipeline demonstrates how **steps** fundamentally change multi-language development. By providing a single primitive that works across TypeScript, Python, and JavaScript, we've eliminated the traditional complexity of polyglot architectures.

**The step primitive enables true unification:**
- **Universal Pattern** - Every step, regardless of language, follows the same receive-process-emit pattern
- **Seamless Integration** - Add Ruby, Go, Rust, or any language using the same step abstraction
- **Unified Deployment** - All languages deploy together as a single, coherent system
- **Shared Development Model** - Write, debug, and monitor everything through the same interface

**Key benefits of step-based unification:**
- **Single Mental Model** - Learn the step pattern once, apply it to any language
- **Cohesive System** - All components work together as parts of one application, not separate services
- **Consistent Experience** - Development, debugging, and monitoring work the same way across all languages
- **Natural Scaling** - Each step can scale independently while maintaining system coherence

**Extend your pipeline with more steps:**
- Add specialized processing steps for different data types and business logic
- Integrate machine learning workflows with Python steps for AI processing
- Build real-time analytics with streaming steps for live data processing
- Connect to enterprise systems through database and API integration steps
- Implement scheduled processing with cron steps for batch operations

The **step primitive** makes all extensions natural and straightforward—every new capability follows the same unified pattern.

Ready to unify your multi-language systems? Start building with steps today!


## Examples
[multi-language-data-processing](/docs/examples/multi-language-data-processing): Code example
---
title: 'Multi-Language Processing'
description: 'Multi-Language Data Processing: Building a Unified Pipeline with Motia'
---

Modern backend development often requires combining the strengths of different programming languages. TypeScript for APIs, Python for data processing and AI, JavaScript for rapid prototyping. Traditional approaches involve complex microservices architectures with intricate communication patterns.

This comprehensive guide explores how to build a unified multi-language data processing pipeline using Motia's **step** primitive. We'll cover:

1. **Steps as Core Primitive**: How steps unify different languages under a single abstraction.
2. **Building the Pipeline**: A step-by-step guide to creating a cohesive multi-language data processing workflow.
3. **Unified Execution Model**: How steps enable seamless communication between different runtime environments.
4. **Hands-On Development**: How to build, run, and observe your unified multi-language pipeline.

Let's build a production-ready data processing system where steps unify TypeScript, Python, and JavaScript into a single cohesive workflow.

---

## The Power of Steps: A Unified Multi-Language Primitive

<div className="my-8">![Multi-Language Data Processing in Motia Workbench](/docs-images/motia-build-your-app-2.gif)</div>

At its core, our data processing pipeline demonstrates how **steps** solve the fundamental challenge of multi-language systems: unifying different programming languages under a single, coherent abstraction. Traditional polyglot architectures require complex inter-process communication and deployment coordination. Motia's **step** primitive unifies everything.

**Steps enable true language unification:**

- **[TypeScript](https://www.typescriptlang.org/)** steps: Strong typing and excellent tooling for APIs and orchestration
- **[Python](https://www.python.org/)** steps: Rich ecosystem for data processing, ML, and scientific computing  
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)** steps: Dynamic processing and rapid development
- **[Motia's Step Primitive](https://motia.dev)**: The unifying abstraction that makes all languages work as a single system

Instead of managing multiple services, **steps** provide a single programming model. Whether written in TypeScript, Python, or JavaScript, every step follows the same pattern: receive data, process it, emit events. This unification is what makes multi-language development straightforward.

---

## The Anatomy of Our Multi-Language Pipeline

Our application consists of six specialized steps, each leveraging the optimal language for its specific task. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="01-starter.step.ts" />
  <File name="02-bridge.step.ts" />
  <File name="simple-python_step.py" />
  <File name="notify.step.ts" />
  <File name="04-final.step.ts" />
  <File name="05-summary.step.js" />
</Folder>

<Folder name="types" defaultOpen>
  <File name="index.ts" />
</Folder>

<Tabs items={['api-starter', 'bridge-step', 'python-processor', 'notification-handler', 'finalizer', 'summary-generator']}>
  <Tab value="api-starter">
    The entry point for our multi-language workflow. This TypeScript API endpoint receives data, validates it with Zod schemas, and kicks off the processing pipeline.

```typescript
import { z } from 'zod'

const bodySchema = z.object({
  data: z.record(z.unknown()).optional(),
  message: z.string().optional()
})

// API endpoint to start the multi-language pipeline
export const config = {
  type: 'api',
  name: 'AppStarter',
  description: 'Start the multi-language app pipeline',

  method: 'POST',
  path: '/start-app',

  bodySchema,
  responseSchema: {
    200: z.object({
      message: z.string(),
      appId: z.number(),
      traceId: z.string()
    })
  },

  emits: ['app.started'],
  flows: ['data-processing']
} as const

export const handler = async (req: any, { logger, emit, traceId }: any) => {
  logger.info('🚀 Starting multi-language app', { body: req.body, traceId })
  
  const appData = {
    id: Date.now(),
    input: req.body.data || {},
    started_at: new Date().toISOString(),
    traceId
  }

  // Emit to next step
  await emit({
    topic: 'app.started',
    data: appData
  })

  logger.info('✅ App started successfully', { 
    appId: appData.id,
    traceId 
  })

  return {
    status: 200,
    body: {
      message: 'Multi-language app started successfully',
      appId: appData.id,
      traceId
    }
  }
}
```

  </Tab>
  <Tab value="bridge-step">
    A TypeScript bridge that receives the app start event, processes the data, and forwards it to the Python processing step with proper type transformation.

```typescript
import { z } from 'zod'

// Bridge step to connect app starter to Python processing
export const config = {
  type: 'event',
  name: 'AppBridge',
  description: 'Bridge between app start and Python processing',
  subscribes: ['app.started'],
  emits: ['data.processed'],
  input: z.object({
    id: z.number(),
    input: z.record(z.unknown()),
    started_at: z.string(),
    traceId: z.string()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('🌉 Processing app data and sending to Python', { appId: input.id })
  
  // Process data for Python step
  const processedResult = {
    original_id: input.id,
    processed_at: input.started_at,
    result: `Processed: ${JSON.stringify(input.input)}`,
    confidence: 0.95,
    model_version: '1.0'
  }

  // Send to Python processing
  await emit({
    topic: 'data.processed', 
    data: processedResult
  })

  logger.info('✅ Data sent to Python processing', { 
    originalId: input.id
  })
}
```

  </Tab>
  <Tab value="python-processor">
    The core data processor written in Python, demonstrating how Python steps integrate seamlessly with the TypeScript workflow while maintaining access to Python's rich ecosystem. Note the `_step.py` naming convention.

```python
import time
from datetime import datetime

# Python processing step configuration
config = {
    "type": "event",
    "name": "ProcessDataPython",
    "description": "Process data using Python capabilities",
    "subscribes": ["data.processed"],
    "emits": ["python.done"],
    "flows": ["data-processing"]
}

async def handler(input_data, ctx):
    """
    Python step that processes data and demonstrates Python capabilities
    """
    logger = ctx.logger
    emit = ctx.emit
    
    # Extract data from input
    original_id = input_data.get("original_id")
    result = input_data.get("result", "")
    
    logger.info(f"🐍 Python processing data for ID: {original_id}")
    
    start_time = time.time()
    
    # Simulate Python data processing
    processed_message = f"Python processed: {result}"
    
    # Add some Python-specific processing
    data_analysis = {
        "word_count": len(result.split()) if isinstance(result, str) else 0,
        "character_count": len(result) if isinstance(result, str) else 0,
        "processed_timestamp": datetime.now().isoformat(),
        "processing_language": "Python 3.x"
    }
    
    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Create result object
    python_result = {
        "id": original_id,
        "python_message": processed_message,
        "processed_by": ["appStarter", "appBridge", "ProcessDataPython"],
        "processing_time": processing_time,
        "analysis": data_analysis
    }
    
    # Emit to next step
    await emit({
        "topic": "python.done",
        "data": python_result
    })
    
    logger.info(f"✅ Python processing completed in {processing_time:.2f}ms")
```

  </Tab>
  <Tab value="notification-handler">
    A TypeScript notification handler that processes the Python results and sends notifications, showing seamless data flow between Python and TypeScript.

```typescript
import { z } from 'zod'

export const config = {
  type: 'event',
  name: 'NotificationHandler',
  description: 'Send notifications after Python processing',
  subscribes: ['python.done'],
  emits: ['notification.sent'],
  input: z.object({
    id: z.number(),
    python_message: z.string(),
    processed_by: z.array(z.string()),
    processing_time: z.number(),
    analysis: z.record(z.unknown()).optional()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('📧 Sending notifications after Python processing', { id: input.id })
  
  // Simulate sending notifications (email, slack, etc.)
  const notification = {
    id: input.id,
    message: `Notification: ${input.python_message}`,
    processed_by: input.processed_by,
    sent_at: new Date().toISOString()
  }

  // Send notification data to final step
  await emit({
    topic: 'notification.sent',
    data: {
      ...notification,
      processing_time: input.processing_time
    }
  })

  logger.info('✅ Notifications sent successfully', { id: input.id })
}
```

  </Tab>
  <Tab value="finalizer">
    A TypeScript finalizer that aggregates all the processing results and prepares the final summary data before handing off to JavaScript for metrics generation.

```typescript
import { z } from 'zod'

// Final step to complete the app - TypeScript
export const config = {
  type: 'event',
  name: 'AppFinalizer',
  description: 'Complete the basic app and log final results',
  subscribes: ['notification.sent'],
  emits: ['app.completed'],
  input: z.object({
    id: z.number(),
    message: z.string(),
    processed_by: z.array(z.string()),
    sent_at: z.string(),
    processing_time: z.number()
  }),
  flows: ['data-processing']
} as const

export const handler = async (input: any, { logger, emit }: any) => {
  logger.info('🏁 Finalizing app', { 
    notificationId: input.id,
    message: input.message 
  })
  
  // Create final app summary
  const summary = {
    appId: input.id,
    status: 'completed',
    completed_at: new Date().toISOString(),
    steps_executed: [
      'app-starter',
      'app-bridge', 
      'python-processor',
      'notification-handler',
      'app-finalizer'
    ],
    result: input.message
  }

  // Send to JavaScript summary generator
  await emit({
    topic: 'app.completed',
    data: {
      ...summary,
      total_processing_time: input.processing_time
    }
  })

  logger.info('✅ App finalized successfully', { 
    appId: input.id,
    totalSteps: summary.steps_executed.length
  })
}
```

  </Tab>
  <Tab value="summary-generator">
    The final step uses JavaScript for dynamic summary generation and metrics calculation, showcasing how all three languages work together in a single workflow.

```javascript
// Final summary step - JavaScript
export const config = {
  type: 'event',
  name: 'summaryGenerator',
  description: 'Generate final summary in JavaScript',
  subscribes: ['app.completed'],
  emits: [], // Final step - no further processing needed
  flows: ['data-processing']
}

export const handler = async (input, { logger }) => {
  logger.info('📊 Generating final summary in JavaScript', { 
    appId: input.appId,
    status: input.status 
  })
  
  // Calculate processing metrics
  const processingTime = input.total_processing_time || 0
  const stepsCount = input.steps_executed ? input.steps_executed.length : 0
  
  // Create comprehensive summary
  const summary = {
    appId: input.appId,
    finalStatus: input.status,
    totalSteps: stepsCount,
    processingTimeMs: processingTime,
    languages: ['TypeScript', 'Python', 'JavaScript'],
    summary: `Multi-language app completed successfully with ${stepsCount} steps`,
    result: input.result,
    completedAt: new Date().toISOString(),
    generatedBy: 'javascript-summary-step'
  }
  
  // Log final summary (final step - no emit needed)
  logger.info('✨ Final summary generated successfully', summary)
  
  return summary
}
```

  </Tab>
</Tabs>

---

## Type Definitions

Our unified system uses shared TypeScript types to ensure type safety across the multi-language pipeline:

```typescript
// types/index.ts
export interface AppData {
  id: number
  input: Record<string, unknown>
  started_at: string
  traceId: string
}

export interface ProcessedResult {
  original_id: number
  processed_at: string
  result: string
  confidence: number
  model_version: string
}

export interface PythonResult {
  id: number
  python_message: string
  processed_by: string[]
  processing_time: number
}

export interface NotificationData {
  id: number
  message: string
  processed_by: string[]
  sent_at: string
}

export interface AppSummary {
  appId: number
  status: string
  completed_at: string
  steps_executed: string[]
  result: string
}
```

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your multi-language pipeline, making it easy to trace data flow between TypeScript, Python, and JavaScript steps.

<div className="my-8">![Multi-Language Workflow in Motia Workbench](/docs-images/motia-build-your-app-2.gif)</div>

You can monitor real-time execution, view logs from all languages in a unified interface, and trace the complete data flow from the TypeScript API through Python processing to JavaScript summary generation.

---

## Event Flow Architecture

The pipeline follows a clear event-driven flow that connects all languages seamlessly:

1. **`app.started`** - TypeScript API → TypeScript Bridge
2. **`data.processed`** - TypeScript Bridge → Python Processor  
3. **`python.done`** - Python Processor → TypeScript Notification Handler
4. **`notification.sent`** - TypeScript Notification → TypeScript Finalizer
5. **`app.completed`** - TypeScript Finalizer → JavaScript Summary Generator

Each step only needs to know the events it subscribes to and emits, creating loose coupling while maintaining strong data flow guarantees.

---

## Key Features & Benefits

### 🧩 **Step as Universal Primitive**
Every piece of logic—whether TypeScript, Python, or JavaScript—follows the same step pattern, creating true unification.

### 🌐 **Seamless Language Integration**
Steps eliminate the complexity of multi-language systems by providing a unified programming model.

### 📊 **Unified Development Experience**
Write, debug, and monitor all languages through a single interface and shared execution model.

### ⚡ **Hot Reload Across Languages**
Edit any step in any language and see changes instantly across the entire pipeline.

### 🔄 **Event-Driven Communication**
Steps communicate through events, enabling loose coupling and independent scaling.

### 🎯 **Single Deployment Model**
Deploy all languages together as a cohesive system, not as separate microservices.

### 🐍 **Python Step Naming**
Python steps use the `_step.py` suffix convention for proper module resolution (e.g., `simple-python_step.py`).

---

## Trying It Out

Ready to build your first multi-language Motia application? Let's get it running.

<Steps>

### Create Your Motia App

Start by creating a new Motia project with the interactive setup.

```shell
npx motia@latest create
```

### Navigate and Start Development

Move into your project directory and start the development server.

```shell
cd my-app  # Replace with your project name
npm run dev
```

### Open the Workbench

Navigate to [`http://localhost:3000`](http://localhost:3000) to access the Workbench and run your workflow.

### Test the Multi-Language Pipeline

Send a request to your API endpoint to see the multi-language workflow in action:

```shell
   curl -X POST http://localhost:3000/start-app \
     -H "Content-Type: application/json" \
     -d '{"data": {"test": "value"}, "message": "Hello!"}'
```

Watch in the Workbench as your data flows through:
1. **TypeScript** validation and event emission
2. **TypeScript** bridge processing and forwarding  
3. **Python** data processing with rich logging
4. **TypeScript** notification handling
5. **TypeScript** finalization and aggregation
6. **JavaScript** summary generation and metrics

</Steps>

---

## 💻 Dive into the Code

Want to explore multi-language workflows further? Check out additional examples and the complete source code:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Multi-Language Examples</h3>
        <p className="text-gray-600 mb-4">Access complete multi-language implementations, configuration examples, and learn how to integrate TypeScript, Python, and JavaScript in production applications.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.30 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            Explore Examples
          </a>
          <a 
            href="/docs/getting-started/quick-start" 
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            Quick Start →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Power of Unification Through Steps

This multi-language data processing pipeline demonstrates how **steps** fundamentally change multi-language development. By providing a single primitive that works across TypeScript, Python, and JavaScript, we've eliminated the traditional complexity of polyglot architectures.

**The step primitive enables true unification:**
- **Universal Pattern** - Every step, regardless of language, follows the same receive-process-emit pattern
- **Seamless Integration** - Add Ruby, Go, Rust, or any language using the same step abstraction
- **Unified Deployment** - All languages deploy together as a single, coherent system
- **Shared Development Model** - Write, debug, and monitor everything through the same interface

**Key benefits of step-based unification:**
- **Single Mental Model** - Learn the step pattern once, apply it to any language
- **Cohesive System** - All components work together as parts of one application, not separate services
- **Consistent Experience** - Development, debugging, and monitoring work the same way across all languages
- **Natural Scaling** - Each step can scale independently while maintaining system coherence

**Extend your pipeline with more steps:**
- Add specialized processing steps for different data types and business logic
- Integrate machine learning workflows with Python steps for AI processing
- Build real-time analytics with streaming steps for live data processing
- Connect to enterprise systems through database and API integration steps
- Implement scheduled processing with cron steps for batch operations

The **step primitive** makes all extensions natural and straightforward—every new capability follows the same unified pattern.

Ready to unify your multi-language systems? Start building with steps today!

-   [rag-docling-weaviate](/docs/examples/rag-docling-weaviate): Documentation for rag-docling-weaviate.
---
title: 'RAG PDF Analyzer'
description: 'Intelligent Document Processing: Building a RAG System with Motia'
---

In the era of AI-powered applications, the ability to extract insights from documents is crucial. Whether you're building a knowledge base, a research assistant, or a customer support system, you need to transform static PDFs into queryable, intelligent systems. This is where Retrieval-Augmented Generation (RAG) architecture shines, and where the Motia framework provides an elegant solution.

This comprehensive guide explores how to build a production-ready RAG system that intelligently processes PDFs and answers questions about their content. We'll cover:

1.  **The RAG Architecture**: Understanding how document processing, vector storage, and AI generation work together.
2.  **Motia's Event-Driven Approach**: How `steps` create a scalable, maintainable RAG pipeline.
3.  **Building the Workflow**: A detailed walkthrough of our polyglot processing pipeline.
4.  **Advanced Features**: Real-time progress tracking, error handling, and production considerations.
5.  **Hands-On Testing**: How to ingest documents and query your knowledge base.

Let's transform your documents into an intelligent AI assistant.

---

## The Power of Intelligent Document Processing

<div className="my-8">![RAG Workflow in Motia Workbench](./../img/rag-docling-weaviate-agent.png)</div>


At its core, our RAG agent solves a fundamental challenge: how do you make unstructured documents searchable and queryable by AI? Traditional approaches often involve complex, monolithic systems that are difficult to scale and maintain. Our Motia-powered solution breaks this down into discrete, event-driven steps that each handle a specific aspect of the pipeline.

The magic happens through the integration of three powerful technologies:

-   **[Docling](https://github.com/docling-project/docling)**: Advanced PDF parsing with intelligent chunking that preserves document structure
-   **[Weaviate](https://weaviate.io/)**: Cloud-native vector database with built-in OpenAI integration
-   **[Motia](https://motia.dev)**: Event-driven framework that orchestrates the entire pipeline

Instead of a brittle, tightly-coupled system, we get a resilient architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our RAG Pipeline

Our application consists of seven specialized steps, each handling a specific part of the document processing and querying workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <Folder name="api-steps" defaultOpen>
    <File name="api-process-pdfs.step.ts" />
    <File name="api-query-rag.step.ts" />
  </Folder>
  <Folder name="event-steps" defaultOpen>
    <File name="init-weaviate.step.ts" />
    <File name="read-pdfs.step.ts" />
    <File name="process-pdfs.step.py" />
    <File name="load-weaviate.step.ts" />
  </Folder>
</Folder>

<Tabs items={['api-process-pdfs', 'init-weaviate', 'read-pdfs', 'process-pdfs', 'load-weaviate', 'api-query-rag']}>
  <Tab value="api-process-pdfs">
    The entry point for document ingestion. This API endpoint receives a folder path, kicks off the processing pipeline, and returns immediately with a tracking ID for real-time progress monitoring.

    ```ts
    import { Handlers } from 'motia'
    import { z } from 'zod'
    import { v4 as uuidv4 } from 'uuid'

    export const config = {
      type: 'api',
      name: 'api-process-pdfs',
      description: 'API endpoint to start PDF processing pipeline',
      path: '/api/rag/process-pdfs',
      method: 'POST',
      emits: ['rag.read.pdfs'],
      bodySchema: z.object({
        folderPath: z.string().min(1, 'folderPath is required'),
      }),
      flows: ['rag-workflow'],
    } as const

    export const handler: Handlers['api-process-pdfs'] = async (req, { emit, logger }) => {
      const { folderPath } = req.body
      const streamId = uuidv4()

      logger.info('Starting PDF processing pipeline', { folderPath, streamId })

      // Emit event to start the processing chain
      await emit({
        topic: 'rag.read.pdfs',
        data: { folderPath, streamId },
      })

      return {
        status: 200,
        body: { 
          message: 'PDF processing started',
          streamId,
          status: 'processing'
        },
      }
    }
    ```

  </Tab>
  <Tab value="init-weaviate">
    Ensures the Weaviate vector database is properly configured with the correct schema for our documents. This step creates the "Books" collection with OpenAI embeddings and GPT-4o generation capabilities.

    ```ts
    import weaviate, { WeaviateClient, vectorizer, generative } from 'weaviate-client'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    export const config: EventConfig = {
      type: 'event',
      name: 'init-weaviate',
      subscribes: ['rag.read.pdfs'],
      emits: [],
      flows: ['rag-workflow'],
      input: z.object({
        folderPath: z.string(),
        streamId: z.string().optional(),
      }),
    }

    const WEAVIATE_SCHEMA = {
      name: 'Books',
      description: 'Document chunks with metadata',
      vectorizers: vectorizer.text2VecOpenAI({
        model: 'text-embedding-3-small',
        sourceProperties: ['text'],
      }),
      generative: generative.openAI({
        model: 'gpt-4o',
        maxTokens: 4096,
      }),
      properties: [
        { name: 'text', dataType: 'text' as const },
        { name: 'title', dataType: 'text' as const },
        { name: 'source', dataType: 'text' as const },
        { name: 'page', dataType: 'number' as const },
      ],
    }

    export const handler: Handlers['init-weaviate'] = async (input, { logger }) => {
      logger.info('Initializing Weaviate client')
      
      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const exists = await client.collections.get('Books').exists()
        if (!exists) {
          logger.info('Creating Books collection with OpenAI integration...')
          await client.collections.create(WEAVIATE_SCHEMA)
          logger.info('Collection created successfully')
        } else {
          logger.info('Books collection already exists')
        }
      } catch (error) {
        logger.error('Error initializing Weaviate', { error })
        throw error
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
  <Tab value="read-pdfs">
    Scans the specified folder for PDF files and prepares them for processing. Includes intelligent path resolution to handle various folder structures.

    ```ts
    import { readdir } from 'fs/promises'
    import { join, resolve, basename } from 'path'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    export const config: EventConfig = {
      type: 'event',
      name: 'read-pdfs',
      flows: ['rag-workflow'],
      subscribes: ['rag.read.pdfs'],
      emits: [{ topic: 'rag.process.pdfs', label: 'Start processing PDFs' }],
      input: z.object({
        folderPath: z.string(),
        streamId: z.string().optional(),
      }),
    }

    export const handler: Handlers['read-pdfs'] = async (input, { emit, logger }) => {
      const { folderPath: inputFolderPath, streamId } = input
      logger.info(`Reading PDFs from folder: ${inputFolderPath}`)

      // Intelligent path resolution to prevent ENOENT errors
      const currentDirName = basename(process.cwd())
      let resolvedFolderPath = resolve(inputFolderPath)

      // Handle duplicated path segments
      const duplicatedSegment = `${currentDirName}/${currentDirName}`
      if (resolvedFolderPath.includes(duplicatedSegment)) {
        resolvedFolderPath = resolvedFolderPath.replace(duplicatedSegment, currentDirName)
      }

      logger.info(`Resolved folder path: ${resolvedFolderPath}`)

      try {
        const files = await readdir(resolvedFolderPath)
        const pdfFiles = files.filter((file) => file.endsWith('.pdf'))

        logger.info(`Found ${pdfFiles.length} PDF files`)

        const filesInfo = await Promise.all(
          pdfFiles.map(async (pdfFile) => {
            const filePath = join(resolvedFolderPath, pdfFile)
            return {
              filePath,
              fileName: pdfFile,
            }
          })
        )

        await emit({
          topic: 'rag.process.pdfs',
          data: { files: filesInfo, streamId },
        })
      } catch (error) {
        logger.error(`Failed to read PDFs from folder: ${resolvedFolderPath}`, { error })
        throw error
      }
    }
    ```

  </Tab>
  <Tab value="process-pdfs">
    The heart of our document processing pipeline. This Python step uses Docling to intelligently parse and chunk PDFs, preserving document structure and context.

    ```python
    import json
    import os
    from pathlib import Path
    from typing import Any, Dict, List
    from docling.document_converter import DocumentConverter
    from docling.chunking import HybridChunker
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import PdfFormatOption

    def handler(input_data: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Process PDFs using Docling with intelligent chunking"""
        logger = context['logger']
        emit = context['emit']
        
        files = input_data.get('files', [])
        stream_id = input_data.get('streamId')
        
        logger.info(f"Processing {len(files)} PDF files with Docling")
        
        # Configure Docling with optimized settings
        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            do_table_structure=True,
            table_structure_options={
                "do_cell_matching": True,
            }
        )
        
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        # Initialize the hybrid chunker for intelligent document segmentation
        chunker = HybridChunker(
            tokenizer="cl100k_base",
            max_tokens=512,
            overlap_tokens=50,
            heading_hierarchies=True,
            split_by_page=False
        )
        
        all_chunks = []
        
        for file_info in files:
            file_path = file_info['filePath']
            file_name = file_info['fileName']
            
            logger.info(f"Processing file: {file_name}")
            
            try:
                # Convert PDF to structured document
                result = doc_converter.convert(file_path)
                doc = result.document
                
                logger.info(f"Converted {file_name}: {len(doc.pages)} pages")
                
                # Apply intelligent chunking
                chunks = list(chunker.chunk(doc))
                logger.info(f"Generated {len(chunks)} chunks for {file_name}")
                
                # Prepare chunks for Weaviate
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'text': chunk.text,
                        'title': file_name,
                        'source': file_path,
                        'page': getattr(chunk, 'page_no', i + 1),
                        'chunk_id': f"{file_name}_chunk_{i}"
                    }
                    all_chunks.append(chunk_data)
                    
            except Exception as e:
                logger.error(f"Error processing {file_name}: {str(e)}")
                continue
        
        logger.info(f"Total chunks generated: {len(all_chunks)}")
        
        if all_chunks:
            # Emit chunks for Weaviate ingestion
            emit({
                'topic': 'rag.load.weaviate',
                'data': {
                    'chunks': all_chunks,
                    'streamId': stream_id,
                    'totalFiles': len(files),
                    'totalChunks': len(all_chunks)
                }
            })
        else:
            logger.warning("No chunks generated from PDF processing")
    ```

  </Tab>
  <Tab value="load-weaviate">
    Efficiently batches and loads the processed document chunks into Weaviate with progress tracking and error handling.

    ```ts
    import weaviate from 'weaviate-client'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    const ChunkSchema = z.object({
      text: z.string(),
      title: z.string(),
      source: z.string(),
      page: z.number(),
      chunk_id: z.string(),
    })

    export const config: EventConfig = {
      type: 'event',
      name: 'load-weaviate',
      subscribes: ['rag.load.weaviate'],
      emits: [],
      flows: ['rag-workflow'],
      input: z.object({
        chunks: z.array(ChunkSchema),
        streamId: z.string().optional(),
        totalFiles: z.number().optional(),
        totalChunks: z.number().optional(),
      }),
    }

    export const handler: Handlers['load-weaviate'] = async (input, { logger }) => {
      const { chunks, streamId, totalFiles, totalChunks } = input
      
      logger.info('Loading chunks into Weaviate', { 
        chunkCount: chunks.length,
        totalFiles,
        totalChunks,
        streamId 
      })

      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const collection = client.collections.get('Books')
        const BATCH_SIZE = 100

        // Process chunks in batches for optimal performance
        for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
          const batch = chunks.slice(i, i + BATCH_SIZE)
          const batchNumber = Math.floor(i / BATCH_SIZE) + 1
          const totalBatches = Math.ceil(chunks.length / BATCH_SIZE)

          logger.info(`Inserting batch ${batchNumber}/${totalBatches}`, {
            batchSize: batch.length,
            streamId
          })

          const objects = batch.map(chunk => ({
            properties: {
              text: chunk.text,
              title: chunk.title,
              source: chunk.source,
              page: chunk.page,
            }
          }))

          const result = await collection.data.insertMany(objects)
          
          if (result.hasErrors) {
            logger.error('Batch insertion had errors', { 
              errors: result.errors,
              batchNumber,
              streamId 
            })
          } else {
            logger.info(`Successfully inserted batch ${batchNumber}/${totalBatches}`)
          }
        }

        logger.info('Successfully loaded all chunks into Weaviate', {
          totalChunks: chunks.length,
          streamId
        })

      } catch (error) {
        logger.error('Error loading chunks into Weaviate', { error, streamId })
        throw error
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
  <Tab value="api-query-rag">
    The query interface that performs semantic search and generates contextual answers using Weaviate's integrated OpenAI capabilities.

    ```ts
    import weaviate from 'weaviate-client'
    import { Handlers } from 'motia'
    import { z } from 'zod'

    const RAGResponse = z.object({
      answer: z.string(),
      chunks: z.array(z.object({
        text: z.string(),
        title: z.string(),
        source: z.string(),
        page: z.number(),
      })),
      query: z.string(),
      timestamp: z.string(),
    })

    export const config = {
      type: 'api',
      name: 'api-query-rag',
      description: 'Query the RAG system for answers',
      path: '/api/rag/query',
      method: 'POST',
      emits: [],
      bodySchema: z.object({
        query: z.string().min(1, 'Query is required'),
        limit: z.number().min(1).max(10).default(3),
      }),
      flows: ['rag-workflow'],
    } as const

    export const handler: Handlers['api-query-rag'] = async (req, { logger }) => {
      const { query, limit = 3 } = req.body

      logger.info('Processing RAG query', { query, limit })

      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const collection = client.collections.get('Books')
        
        // Perform semantic search with AI generation
        const results = await collection.generate.nearText(
          query,
          { limit, distance: 0.6 },
          { 
            singlePrompt: `Answer this question based on the provided context: ${query}. 
                          Be specific and cite the sources when possible.` 
          }
        )

        // Extract the generated answer and source chunks
        const generatedAnswer = results.generated || 'No answer could be generated.'
        
        const chunks = results.objects.map(obj => ({
          text: obj.properties.text as string,
          title: obj.properties.title as string,
          source: obj.properties.source as string,
          page: obj.properties.page as number,
        }))

        const response = RAGResponse.parse({
          answer: generatedAnswer,
          chunks,
          query,
          timestamp: new Date().toISOString(),
        })

        logger.info('RAG query completed successfully', { 
          query, 
          chunksFound: chunks.length,
          answerLength: generatedAnswer.length 
        })

        return {
          status: 200,
          body: response,
        }

      } catch (error) {
        logger.error('Error processing RAG query', { error, query })
        return {
          status: 500,
          body: { error: 'Failed to process query' },
        }
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your RAG pipeline, making it easy to understand the flow and debug any issues.

<div className="my-8">![RAG Workflow in Motia Workbench](./../img/rag-example.gif)</div>

You can monitor real-time processing, view logs, and trace the execution of each step directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monolithic approaches.

---

## Key Features & Benefits

### 🚀 **Event-Driven Architecture**
Each step is independent and communicates through events, making the system highly scalable and maintainable.

### 🧠 **Intelligent Document Processing**  
Docling's hybrid chunking preserves document structure while creating optimal chunks for embedding.

### ⚡ **High-Performance Vector Search**
Weaviate's cloud-native architecture provides fast, scalable similarity search with built-in OpenAI integration.

### 🔄 **Real-Time Progress Tracking**
Monitor document processing progress with detailed logging and status updates.

### 🌐 **Polyglot Support**
Seamlessly combine Python (Docling) and TypeScript (orchestration) in a single workflow.

### 🛡️ **Production-Ready**
Built-in error handling, batch processing, and resource cleanup ensure reliability.

---

## Trying It Out

Ready to build your own intelligent document assistant? Let's get the system running.

<Steps>

### Install Dependencies

Install both Node.js and Python dependencies. The prepare script automatically sets up the Python virtual environment.

```shell
npm install
```

### Set Your Environment Variables

You'll need API keys for OpenAI and Weaviate Cloud. Create a `.env` file:

```shell
OPENAI_API_KEY="sk-..."
WEAVIATE_URL="https://your-cluster.weaviate.network"
WEAVIATE_API_KEY="your-weaviate-api-key"
```

### Run the Project

Start the Motia development server to begin processing documents.

```shell
npm run dev
```

### Process Your First Documents

Add some PDF files to the `docs/pdfs/` folder, then start the ingestion pipeline:

```shell
curl -X POST http://localhost:3000/api/rag/process-pdfs \
  -H "Content-Type: application/json" \
  -d '{"folderPath":"docs/pdfs"}'
```

Watch the logs as your documents are processed through the pipeline:
1. **PDF Reading**: Files are discovered and queued
2. **Docling Processing**: Intelligent chunking with structure preservation  
3. **Weaviate Loading**: Chunks are embedded and stored

### Query Your Knowledge Base

Once processing is complete, you can ask questions about your documents:

#### General Query
```shell
curl -X POST http://localhost:3000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What are the main topics covered in these documents?","limit":3}'
```

#### Specific Question
```shell
curl -X POST http://localhost:3000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What methodology was used in the research?","limit":5}'
```

The response includes both a generated answer and the source chunks with page numbers for verification.

</Steps>

---

## Advanced Usage

### Custom Chunking Strategies

Modify the Python processing step to implement custom chunking logic:

```python
# In process-pdfs.step.py
chunker = HybridChunker(
    tokenizer="cl100k_base",
    max_tokens=1024,  # Larger chunks for more context
    overlap_tokens=100,  # More overlap for better continuity
    heading_hierarchies=True,
    split_by_page=True  # Preserve page boundaries
)
```

### Batch Processing Optimization

Adjust batch sizes in the Weaviate loading step for optimal performance:

```ts
// In load-weaviate.step.ts
const BATCH_SIZE = 50  // Smaller batches for large documents
```

### Multi-Collection Support

Extend the system to handle different document types by creating separate Weaviate collections:

```ts
const COLLECTIONS = {
  research: 'ResearchPapers',
  manuals: 'TechnicalManuals', 
  reports: 'BusinessReports'
}
```

---

## Troubleshooting

### Common Issues

**ENOENT Path Errors**: The system automatically handles path normalization, but ensure your `folderPath` is relative to the project root.

**Empty Answers**: Check that documents were successfully processed by examining the logs. Verify your OpenAI API key is valid.

**Weaviate Connection Issues**: Ensure your `WEAVIATE_URL` and `WEAVIATE_API_KEY` are correct and your cluster is running.

### Performance Tips

- **Document Size**: For large PDFs, consider preprocessing to split them into smaller files
- **Batch Size**: Adjust the Weaviate batch size based on your cluster's capacity
- **Chunking Strategy**: Experiment with different chunk sizes and overlap for your specific use case

---

## 💻 Dive into the Code

Want to explore the complete RAG implementation? Check out the full source code, including all steps, configuration files, and setup instructions:

<div className="not-prose">
  <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete RAG Implementation</h3>
        <p className="text-gray-600 mb-4">Access the full source code for this RAG agent, including Python processing scripts, TypeScript orchestration, and production configuration.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/rag-docling-weaviate-agent" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View RAG Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Future of Document Intelligence

This RAG system demonstrates the power of combining best-in-class technologies with Motia's event-driven architecture. By breaking down complex document processing into discrete, manageable steps, we've created a system that's not only powerful but also maintainable and scalable.

The polyglot nature of the solution: Python for document processing, TypeScript for orchestration, shows how Motia enables you to use the right tool for each job without sacrificing integration or maintainability.

From here, you can extend the system by:
- Adding support for other document formats (Word, PowerPoint, etc.)
- Implementing document classification and routing
- Adding real-time document updates and synchronization
- Building a web interface for document management
- Integrating with existing business systems

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing pipeline.

Ready to transform your documents into intelligent, queryable knowledge bases? Start building with Motia today!



## Examples
[rag-docling-weaviate](/docs/examples/rag-docling-weaviate): Code example
---
title: 'RAG PDF Analyzer'
description: 'Intelligent Document Processing: Building a RAG System with Motia'
---

In the era of AI-powered applications, the ability to extract insights from documents is crucial. Whether you're building a knowledge base, a research assistant, or a customer support system, you need to transform static PDFs into queryable, intelligent systems. This is where Retrieval-Augmented Generation (RAG) architecture shines, and where the Motia framework provides an elegant solution.

This comprehensive guide explores how to build a production-ready RAG system that intelligently processes PDFs and answers questions about their content. We'll cover:

1.  **The RAG Architecture**: Understanding how document processing, vector storage, and AI generation work together.
2.  **Motia's Event-Driven Approach**: How `steps` create a scalable, maintainable RAG pipeline.
3.  **Building the Workflow**: A detailed walkthrough of our polyglot processing pipeline.
4.  **Advanced Features**: Real-time progress tracking, error handling, and production considerations.
5.  **Hands-On Testing**: How to ingest documents and query your knowledge base.

Let's transform your documents into an intelligent AI assistant.

---

## The Power of Intelligent Document Processing

<div className="my-8">![RAG Workflow in Motia Workbench](./../img/rag-docling-weaviate-agent.png)</div>


At its core, our RAG agent solves a fundamental challenge: how do you make unstructured documents searchable and queryable by AI? Traditional approaches often involve complex, monolithic systems that are difficult to scale and maintain. Our Motia-powered solution breaks this down into discrete, event-driven steps that each handle a specific aspect of the pipeline.

The magic happens through the integration of three powerful technologies:

-   **[Docling](https://github.com/docling-project/docling)**: Advanced PDF parsing with intelligent chunking that preserves document structure
-   **[Weaviate](https://weaviate.io/)**: Cloud-native vector database with built-in OpenAI integration
-   **[Motia](https://motia.dev)**: Event-driven framework that orchestrates the entire pipeline

Instead of a brittle, tightly-coupled system, we get a resilient architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our RAG Pipeline

Our application consists of seven specialized steps, each handling a specific part of the document processing and querying workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <Folder name="api-steps" defaultOpen>
    <File name="api-process-pdfs.step.ts" />
    <File name="api-query-rag.step.ts" />
  </Folder>
  <Folder name="event-steps" defaultOpen>
    <File name="init-weaviate.step.ts" />
    <File name="read-pdfs.step.ts" />
    <File name="process-pdfs.step.py" />
    <File name="load-weaviate.step.ts" />
  </Folder>
</Folder>

<Tabs items={['api-process-pdfs', 'init-weaviate', 'read-pdfs', 'process-pdfs', 'load-weaviate', 'api-query-rag']}>
  <Tab value="api-process-pdfs">
    The entry point for document ingestion. This API endpoint receives a folder path, kicks off the processing pipeline, and returns immediately with a tracking ID for real-time progress monitoring.

    ```ts
    import { Handlers } from 'motia'
    import { z } from 'zod'
    import { v4 as uuidv4 } from 'uuid'

    export const config = {
      type: 'api',
      name: 'api-process-pdfs',
      description: 'API endpoint to start PDF processing pipeline',
      path: '/api/rag/process-pdfs',
      method: 'POST',
      emits: ['rag.read.pdfs'],
      bodySchema: z.object({
        folderPath: z.string().min(1, 'folderPath is required'),
      }),
      flows: ['rag-workflow'],
    } as const

    export const handler: Handlers['api-process-pdfs'] = async (req, { emit, logger }) => {
      const { folderPath } = req.body
      const streamId = uuidv4()

      logger.info('Starting PDF processing pipeline', { folderPath, streamId })

      // Emit event to start the processing chain
      await emit({
        topic: 'rag.read.pdfs',
        data: { folderPath, streamId },
      })

      return {
        status: 200,
        body: { 
          message: 'PDF processing started',
          streamId,
          status: 'processing'
        },
      }
    }
    ```

  </Tab>
  <Tab value="init-weaviate">
    Ensures the Weaviate vector database is properly configured with the correct schema for our documents. This step creates the "Books" collection with OpenAI embeddings and GPT-4o generation capabilities.

    ```ts
    import weaviate, { WeaviateClient, vectorizer, generative } from 'weaviate-client'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    export const config: EventConfig = {
      type: 'event',
      name: 'init-weaviate',
      subscribes: ['rag.read.pdfs'],
      emits: [],
      flows: ['rag-workflow'],
      input: z.object({
        folderPath: z.string(),
        streamId: z.string().optional(),
      }),
    }

    const WEAVIATE_SCHEMA = {
      name: 'Books',
      description: 'Document chunks with metadata',
      vectorizers: vectorizer.text2VecOpenAI({
        model: 'text-embedding-3-small',
        sourceProperties: ['text'],
      }),
      generative: generative.openAI({
        model: 'gpt-4o',
        maxTokens: 4096,
      }),
      properties: [
        { name: 'text', dataType: 'text' as const },
        { name: 'title', dataType: 'text' as const },
        { name: 'source', dataType: 'text' as const },
        { name: 'page', dataType: 'number' as const },
      ],
    }

    export const handler: Handlers['init-weaviate'] = async (input, { logger }) => {
      logger.info('Initializing Weaviate client')
      
      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const exists = await client.collections.get('Books').exists()
        if (!exists) {
          logger.info('Creating Books collection with OpenAI integration...')
          await client.collections.create(WEAVIATE_SCHEMA)
          logger.info('Collection created successfully')
        } else {
          logger.info('Books collection already exists')
        }
      } catch (error) {
        logger.error('Error initializing Weaviate', { error })
        throw error
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
  <Tab value="read-pdfs">
    Scans the specified folder for PDF files and prepares them for processing. Includes intelligent path resolution to handle various folder structures.

    ```ts
    import { readdir } from 'fs/promises'
    import { join, resolve, basename } from 'path'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    export const config: EventConfig = {
      type: 'event',
      name: 'read-pdfs',
      flows: ['rag-workflow'],
      subscribes: ['rag.read.pdfs'],
      emits: [{ topic: 'rag.process.pdfs', label: 'Start processing PDFs' }],
      input: z.object({
        folderPath: z.string(),
        streamId: z.string().optional(),
      }),
    }

    export const handler: Handlers['read-pdfs'] = async (input, { emit, logger }) => {
      const { folderPath: inputFolderPath, streamId } = input
      logger.info(`Reading PDFs from folder: ${inputFolderPath}`)

      // Intelligent path resolution to prevent ENOENT errors
      const currentDirName = basename(process.cwd())
      let resolvedFolderPath = resolve(inputFolderPath)

      // Handle duplicated path segments
      const duplicatedSegment = `${currentDirName}/${currentDirName}`
      if (resolvedFolderPath.includes(duplicatedSegment)) {
        resolvedFolderPath = resolvedFolderPath.replace(duplicatedSegment, currentDirName)
      }

      logger.info(`Resolved folder path: ${resolvedFolderPath}`)

      try {
        const files = await readdir(resolvedFolderPath)
        const pdfFiles = files.filter((file) => file.endsWith('.pdf'))

        logger.info(`Found ${pdfFiles.length} PDF files`)

        const filesInfo = await Promise.all(
          pdfFiles.map(async (pdfFile) => {
            const filePath = join(resolvedFolderPath, pdfFile)
            return {
              filePath,
              fileName: pdfFile,
            }
          })
        )

        await emit({
          topic: 'rag.process.pdfs',
          data: { files: filesInfo, streamId },
        })
      } catch (error) {
        logger.error(`Failed to read PDFs from folder: ${resolvedFolderPath}`, { error })
        throw error
      }
    }
    ```

  </Tab>
  <Tab value="process-pdfs">
    The heart of our document processing pipeline. This Python step uses Docling to intelligently parse and chunk PDFs, preserving document structure and context.

    ```python
    import json
    import os
    from pathlib import Path
    from typing import Any, Dict, List
    from docling.document_converter import DocumentConverter
    from docling.chunking import HybridChunker
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import PdfFormatOption

    def handler(input_data: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Process PDFs using Docling with intelligent chunking"""
        logger = context['logger']
        emit = context['emit']
        
        files = input_data.get('files', [])
        stream_id = input_data.get('streamId')
        
        logger.info(f"Processing {len(files)} PDF files with Docling")
        
        # Configure Docling with optimized settings
        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            do_table_structure=True,
            table_structure_options={
                "do_cell_matching": True,
            }
        )
        
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        # Initialize the hybrid chunker for intelligent document segmentation
        chunker = HybridChunker(
            tokenizer="cl100k_base",
            max_tokens=512,
            overlap_tokens=50,
            heading_hierarchies=True,
            split_by_page=False
        )
        
        all_chunks = []
        
        for file_info in files:
            file_path = file_info['filePath']
            file_name = file_info['fileName']
            
            logger.info(f"Processing file: {file_name}")
            
            try:
                # Convert PDF to structured document
                result = doc_converter.convert(file_path)
                doc = result.document
                
                logger.info(f"Converted {file_name}: {len(doc.pages)} pages")
                
                # Apply intelligent chunking
                chunks = list(chunker.chunk(doc))
                logger.info(f"Generated {len(chunks)} chunks for {file_name}")
                
                # Prepare chunks for Weaviate
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'text': chunk.text,
                        'title': file_name,
                        'source': file_path,
                        'page': getattr(chunk, 'page_no', i + 1),
                        'chunk_id': f"{file_name}_chunk_{i}"
                    }
                    all_chunks.append(chunk_data)
                    
            except Exception as e:
                logger.error(f"Error processing {file_name}: {str(e)}")
                continue
        
        logger.info(f"Total chunks generated: {len(all_chunks)}")
        
        if all_chunks:
            # Emit chunks for Weaviate ingestion
            emit({
                'topic': 'rag.load.weaviate',
                'data': {
                    'chunks': all_chunks,
                    'streamId': stream_id,
                    'totalFiles': len(files),
                    'totalChunks': len(all_chunks)
                }
            })
        else:
            logger.warning("No chunks generated from PDF processing")
    ```

  </Tab>
  <Tab value="load-weaviate">
    Efficiently batches and loads the processed document chunks into Weaviate with progress tracking and error handling.

    ```ts
    import weaviate from 'weaviate-client'
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'

    const ChunkSchema = z.object({
      text: z.string(),
      title: z.string(),
      source: z.string(),
      page: z.number(),
      chunk_id: z.string(),
    })

    export const config: EventConfig = {
      type: 'event',
      name: 'load-weaviate',
      subscribes: ['rag.load.weaviate'],
      emits: [],
      flows: ['rag-workflow'],
      input: z.object({
        chunks: z.array(ChunkSchema),
        streamId: z.string().optional(),
        totalFiles: z.number().optional(),
        totalChunks: z.number().optional(),
      }),
    }

    export const handler: Handlers['load-weaviate'] = async (input, { logger }) => {
      const { chunks, streamId, totalFiles, totalChunks } = input
      
      logger.info('Loading chunks into Weaviate', { 
        chunkCount: chunks.length,
        totalFiles,
        totalChunks,
        streamId 
      })

      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const collection = client.collections.get('Books')
        const BATCH_SIZE = 100

        // Process chunks in batches for optimal performance
        for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
          const batch = chunks.slice(i, i + BATCH_SIZE)
          const batchNumber = Math.floor(i / BATCH_SIZE) + 1
          const totalBatches = Math.ceil(chunks.length / BATCH_SIZE)

          logger.info(`Inserting batch ${batchNumber}/${totalBatches}`, {
            batchSize: batch.length,
            streamId
          })

          const objects = batch.map(chunk => ({
            properties: {
              text: chunk.text,
              title: chunk.title,
              source: chunk.source,
              page: chunk.page,
            }
          }))

          const result = await collection.data.insertMany(objects)
          
          if (result.hasErrors) {
            logger.error('Batch insertion had errors', { 
              errors: result.errors,
              batchNumber,
              streamId 
            })
          } else {
            logger.info(`Successfully inserted batch ${batchNumber}/${totalBatches}`)
          }
        }

        logger.info('Successfully loaded all chunks into Weaviate', {
          totalChunks: chunks.length,
          streamId
        })

      } catch (error) {
        logger.error('Error loading chunks into Weaviate', { error, streamId })
        throw error
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
  <Tab value="api-query-rag">
    The query interface that performs semantic search and generates contextual answers using Weaviate's integrated OpenAI capabilities.

    ```ts
    import weaviate from 'weaviate-client'
    import { Handlers } from 'motia'
    import { z } from 'zod'

    const RAGResponse = z.object({
      answer: z.string(),
      chunks: z.array(z.object({
        text: z.string(),
        title: z.string(),
        source: z.string(),
        page: z.number(),
      })),
      query: z.string(),
      timestamp: z.string(),
    })

    export const config = {
      type: 'api',
      name: 'api-query-rag',
      description: 'Query the RAG system for answers',
      path: '/api/rag/query',
      method: 'POST',
      emits: [],
      bodySchema: z.object({
        query: z.string().min(1, 'Query is required'),
        limit: z.number().min(1).max(10).default(3),
      }),
      flows: ['rag-workflow'],
    } as const

    export const handler: Handlers['api-query-rag'] = async (req, { logger }) => {
      const { query, limit = 3 } = req.body

      logger.info('Processing RAG query', { query, limit })

      const client = await weaviate.connectToWeaviateCloud(process.env.WEAVIATE_URL!, {
        authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
        headers: { 'X-OpenAI-Api-Key': process.env.OPENAI_API_KEY! },
      })

      try {
        const collection = client.collections.get('Books')
        
        // Perform semantic search with AI generation
        const results = await collection.generate.nearText(
          query,
          { limit, distance: 0.6 },
          { 
            singlePrompt: `Answer this question based on the provided context: ${query}. 
                          Be specific and cite the sources when possible.` 
          }
        )

        // Extract the generated answer and source chunks
        const generatedAnswer = results.generated || 'No answer could be generated.'
        
        const chunks = results.objects.map(obj => ({
          text: obj.properties.text as string,
          title: obj.properties.title as string,
          source: obj.properties.source as string,
          page: obj.properties.page as number,
        }))

        const response = RAGResponse.parse({
          answer: generatedAnswer,
          chunks,
          query,
          timestamp: new Date().toISOString(),
        })

        logger.info('RAG query completed successfully', { 
          query, 
          chunksFound: chunks.length,
          answerLength: generatedAnswer.length 
        })

        return {
          status: 200,
          body: response,
        }

      } catch (error) {
        logger.error('Error processing RAG query', { error, query })
        return {
          status: 500,
          body: { error: 'Failed to process query' },
        }
      } finally {
        await client.close()
      }
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your RAG pipeline, making it easy to understand the flow and debug any issues.

<div className="my-8">![RAG Workflow in Motia Workbench](./../img/rag-example.gif)</div>

You can monitor real-time processing, view logs, and trace the execution of each step directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monolithic approaches.

---

## Key Features & Benefits

### 🚀 **Event-Driven Architecture**
Each step is independent and communicates through events, making the system highly scalable and maintainable.

### 🧠 **Intelligent Document Processing**  
Docling's hybrid chunking preserves document structure while creating optimal chunks for embedding.

### ⚡ **High-Performance Vector Search**
Weaviate's cloud-native architecture provides fast, scalable similarity search with built-in OpenAI integration.

### 🔄 **Real-Time Progress Tracking**
Monitor document processing progress with detailed logging and status updates.

### 🌐 **Polyglot Support**
Seamlessly combine Python (Docling) and TypeScript (orchestration) in a single workflow.

### 🛡️ **Production-Ready**
Built-in error handling, batch processing, and resource cleanup ensure reliability.

---

## Trying It Out

Ready to build your own intelligent document assistant? Let's get the system running.

<Steps>

### Install Dependencies

Install both Node.js and Python dependencies. The prepare script automatically sets up the Python virtual environment.

```shell
npm install
```

### Set Your Environment Variables

You'll need API keys for OpenAI and Weaviate Cloud. Create a `.env` file:

```shell
OPENAI_API_KEY="sk-..."
WEAVIATE_URL="https://your-cluster.weaviate.network"
WEAVIATE_API_KEY="your-weaviate-api-key"
```

### Run the Project

Start the Motia development server to begin processing documents.

```shell
npm run dev
```

### Process Your First Documents

Add some PDF files to the `docs/pdfs/` folder, then start the ingestion pipeline:

```shell
curl -X POST http://localhost:3000/api/rag/process-pdfs \
  -H "Content-Type: application/json" \
  -d '{"folderPath":"docs/pdfs"}'
```

Watch the logs as your documents are processed through the pipeline:
1. **PDF Reading**: Files are discovered and queued
2. **Docling Processing**: Intelligent chunking with structure preservation  
3. **Weaviate Loading**: Chunks are embedded and stored

### Query Your Knowledge Base

Once processing is complete, you can ask questions about your documents:

#### General Query
```shell
curl -X POST http://localhost:3000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What are the main topics covered in these documents?","limit":3}'
```

#### Specific Question
```shell
curl -X POST http://localhost:3000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What methodology was used in the research?","limit":5}'
```

The response includes both a generated answer and the source chunks with page numbers for verification.

</Steps>

---

## Advanced Usage

### Custom Chunking Strategies

Modify the Python processing step to implement custom chunking logic:

```python
# In process-pdfs.step.py
chunker = HybridChunker(
    tokenizer="cl100k_base",
    max_tokens=1024,  # Larger chunks for more context
    overlap_tokens=100,  # More overlap for better continuity
    heading_hierarchies=True,
    split_by_page=True  # Preserve page boundaries
)
```

### Batch Processing Optimization

Adjust batch sizes in the Weaviate loading step for optimal performance:

```ts
// In load-weaviate.step.ts
const BATCH_SIZE = 50  // Smaller batches for large documents
```

### Multi-Collection Support

Extend the system to handle different document types by creating separate Weaviate collections:

```ts
const COLLECTIONS = {
  research: 'ResearchPapers',
  manuals: 'TechnicalManuals', 
  reports: 'BusinessReports'
}
```

---

## Troubleshooting

### Common Issues

**ENOENT Path Errors**: The system automatically handles path normalization, but ensure your `folderPath` is relative to the project root.

**Empty Answers**: Check that documents were successfully processed by examining the logs. Verify your OpenAI API key is valid.

**Weaviate Connection Issues**: Ensure your `WEAVIATE_URL` and `WEAVIATE_API_KEY` are correct and your cluster is running.

### Performance Tips

- **Document Size**: For large PDFs, consider preprocessing to split them into smaller files
- **Batch Size**: Adjust the Weaviate batch size based on your cluster's capacity
- **Chunking Strategy**: Experiment with different chunk sizes and overlap for your specific use case

---

## 💻 Dive into the Code

Want to explore the complete RAG implementation? Check out the full source code, including all steps, configuration files, and setup instructions:

<div className="not-prose">
  <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete RAG Implementation</h3>
        <p className="text-gray-600 mb-4">Access the full source code for this RAG agent, including Python processing scripts, TypeScript orchestration, and production configuration.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/rag-docling-weaviate-agent" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View RAG Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Future of Document Intelligence

This RAG system demonstrates the power of combining best-in-class technologies with Motia's event-driven architecture. By breaking down complex document processing into discrete, manageable steps, we've created a system that's not only powerful but also maintainable and scalable.

The polyglot nature of the solution: Python for document processing, TypeScript for orchestration, shows how Motia enables you to use the right tool for each job without sacrificing integration or maintainability.

From here, you can extend the system by:
- Adding support for other document formats (Word, PowerPoint, etc.)
- Implementing document classification and routing
- Adding real-time document updates and synchronization
- Building a web interface for document management
- Integrating with existing business systems

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing pipeline.

Ready to transform your documents into intelligent, queryable knowledge bases? Start building with Motia today!


-   [sentiment-analysis](/docs/examples/sentiment-analysis): Documentation for sentiment-analysis.
---
title: 'Sentiment Analysis'
description: 'Dynamic Workflows: Building a Sentiment Analyzer with Motia'
---

In modern application development, workflows are rarely linear. Whether you're building a simple "prompt => response" system or a complex, multi-stage data processing pipeline, you often need your application to make decisions and route data dynamically. This is where the power of event-driven architecture shines, and where the Motia framework provides a clear path forward.

<div className="my-8">![motia workbench for sentiment analysis](./../img/sentimental-analysis.png)</div>

This guide explores how to build a dynamic sentiment analysis application that uses an LLM to determine how to proceed. We'll cover:

1.  **The Motia Philosophy**: How `steps` as a core primitive simplify complex architectures.
2.  **Building the Workflow**: A step-by-step guide to creating the four key components of our application.
3.  **Visualizing the Flow**: How events chain together to create a cohesive, dynamic system.
4.  **Hands-On with the API**: How to run and test your new sentiment analyzer.

Let's dive in.

---

## A Step at a Time

<div className="my-8">![motia workbench for sentiment analysis](./../img/sentimental-analyzer-workbench.png)</div>

At the heart of the Motia framework is a simple but powerful idea: the **`step`**. A step is a self-contained, independent unit of logic that listens for an event, performs a task, and, optionally, emits a new event. This concept is the core primitive that allows you to break down even the most complex architectures into a series of simple, manageable components.

Instead of a monolithic application where business logic is tightly coupled, Motia encourages a decoupled, event-driven approach. This has several key advantages:

-   **Clarity**: Each step has a single responsibility, making the application easier to understand and reason about.
-   **Scalability**: Steps can be scaled independently, so you can allocate resources where they're needed most.
-   **Extensibility**: Adding new functionality is as simple as creating a new step and subscribing it to an existing event.
-   **Resilience**: The decoupled nature of steps means that a failure in one part of the system doesn't necessarily bring down the entire application.

In this project, we'll see this philosophy in action as we build a sentiment analyzer with four distinct steps, each with its own clear purpose.

---

## The Anatomy of Our Sentiment Analyzer

Our application will be composed of four steps. Let's explore each one.

<Folder name="steps" defaultOpen>
  <File name="analyzeSentimentApi.step.ts" />
  <File name="openAiAnalyzeSentiment.step.ts" />
  <File name="handlePositive.step.ts" />
  <File name="handleNegative.step.ts" />
</Folder>

<Tabs items={['analyzeSentimentApi', 'openAiAnalyzeSentiment', 'handlePositive', 'handleNegative']}>
  <Tab value="analyzeSentimentApi">
    This is the entry point to our workflow. It's an API step that listens for `POST` requests, validates the incoming data, and emits an `openai.analyzeSentimentRequest` event.

    ```ts
    // Receives user text, emits "openai.analyzeSentimentRequest".
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'api',
      name: 'analyzeSentimentApi',
      description: 'Receives user text and emits an event to trigger sentiment analysis.',
      path: '/api/analyze-sentiment',
      method: 'POST',
      emits: ['openai.analyzeSentimentRequest'],
      bodySchema: z.object({
        text: z.string().min(1, 'text is required'),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['analyzeSentimentApi'] = async (req, { emit, logger }) => {
      const { text } = req.body

      logger.info('[AnalyzeSentimentAPI] Received text', { text })

      // Emit an event to call OpenAI
      await emit({
        topic: 'openai.analyzeSentimentRequest',
        data: { text },
      })

      // Return right away
      return {
        status: 200,
        body: { status: 'Accepted', message: 'Your text is being analyzed' },
      }
    }
    ```

  </Tab>
  <Tab value="openAiAnalyzeSentiment">
    This step is the brains of our operation. It subscribes to the `openai.analyzeSentimentRequest` event, calls the OpenAI API, and then based on the response, emits either a `openai.positiveSentiment` or `openai.negativeSentiment` event. This is where the dynamic routing happens.

    ```ts
    // Calls OpenAI, instructing it to ONLY return JSON like {"sentiment":"positive","analysis":"..."}
    import { Handlers } from 'motia'
    import { z } from 'zod'
    import { OpenAI } from 'openai'

    // 1) Create an OpenAI client (newer syntax)
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

    export const config = {
      type: 'event',
      name: 'openAiSentimentAnalyzer',
      description: 'Calls OpenAI to analyze sentiment and emits corresponding events.',
      subscribes: ['openai.analyzeSentimentRequest'],
      // We'll emit different events: "openai.positiveSentiment" or "openai.negativeSentiment"
      emits: ['openai.positiveSentiment', 'openai.negativeSentiment'],
      input: z.object({ text: z.string() }),
      flows: ['sentiment-demo'],
    } as const

    // 3) Provide the code that runs on each event
    export const handler: Handlers['openAiSentimentAnalyzer'] = async (input, { emit, logger }) => {
      logger.info('[OpenAI Sentiment Analyzer] Prompting OpenAI...', { text: input.text })

      try {
        // We'll ask the model to ONLY return JSON with a "sentiment" field
        const systemPrompt =
          'You are an assistant that returns only JSON: {"sentiment":"positive|negative","analysis":"..."}'
        const userPrompt = `Analyze the sentiment of this text: "${input.text}". Return JSON with keys "sentiment" and "analysis".`

        // 4) Use the new openai syntax:
        const response = await openai.chat.completions.create({
          model: 'gpt-3.5-turbo',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
        })

        // 5) Log and parse the response
        const content = response.choices[0]?.message?.content || ''
        logger.info('[OpenAI Sentiment Analyzer] Raw response', { content })

        let parsed: { sentiment?: string; analysis?: string } = {}
        try {
          parsed = JSON.parse(content.trim())
        } catch (err) {
          logger.error('[OpenAI Sentiment Analyzer] Unable to parse JSON', { error: err })
          // If it's not JSON, we bail or handle differently
          return
        }

        // 6) Decide how to route the event
        if (parsed.sentiment) {
          if (parsed.sentiment.toLowerCase() === 'positive') {
            await emit({
              topic: 'openai.positiveSentiment',
              data: { ...parsed, sentiment: parsed.sentiment },
            })
          } else {
            // default to negative
            await emit({
              topic: 'openai.negativeSentiment',
              data: { ...parsed, sentiment: parsed.sentiment },
            })
          }
        } else {
          logger.error('[OpenAI Sentiment Analyzer] Sentiment is missing from the parsed response', { parsed })
        }
      } catch (err) {
        if (err instanceof Error) {
          logger.error('[OpenAI Sentiment Analyzer] Error calling OpenAI', { error: err.message })
        } else {
          logger.error('[OpenAI Sentiment Analyzer] An unknown error occurred while calling OpenAI', { error: err })
        }
      }
    }
    ```
  </Tab>
  <Tab value="handlePositive">
    A specialized responder that listens for the `openai.positiveSentiment` event and logs a confirmation message. In a real-world application, this could trigger a Slack notification, send an email, or kick off another workflow.

    ```ts
    // Handles "openai.positiveSentiment"
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'handlePositive',
      description: 'Handles positive sentiment responses.',
      subscribes: ['openai.positiveSentiment'],
      emits: [],
      input: z.object({
        sentiment: z.string(),
        analysis: z.string().optional(),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['handlePositive'] = async (input, { logger }) => {
      logger.info('[Positive Responder] The sentiment is positive!', { analysis: input.analysis })
      // Maybe notify a Slack channel: "All good vibes here!"
    }
    ```

  </Tab>
  <Tab value="handleNegative">
    Similar to the positive handler, this step listens for the `openai.negativeSentiment` event. This is where you could implement logic to escalate a customer complaint, create a support ticket, or alert the on-call team.

    ```ts
    // Handles "openai.negativeSentiment"
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'handleNegative',
      description: 'Handles negative or unknown sentiment responses.',
      subscribes: ['openai.negativeSentiment'],
      emits: [],
      input: z.object({
        sentiment: z.string(),
        analysis: z.string().optional(),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['handleNegative'] = async (input, { logger }) => {
      logger.info('[Negative Responder] The sentiment is negative or unknown.', { analysis: input.analysis })
      // Could escalate to a service, or respond gently, etc.
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

You can explore the workflow in the Workbench.

<div className="my-8">![Flow](./../img/sentimental-analyzer.png)</div>

You can also read your files and watch logs, traces, debug your architecture directly in the Workbench.

<div className="my-8">![Workbench](./../img/sentimental-analyzer-workbench.gif)</div>

---

## Trying It Out

Ready to see it in action? Let's get the project running.

<Steps>

### Install Dependencies

First, install the necessary npm packages.

```shell
npm install
```

### Set Your Environment Variables

You'll need an OpenAI API key for this project. Export it as an environment variable.

```shell
export OPENAI_API_KEY="sk-..."
```

### Run the Project

Start the Motia development server.

```shell
npm run dev
```

### Test the API

Now you can send requests to your API and see the workflow in action.

#### Positive Sentiment

```shell
curl -X POST http://localhost:3000/api/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"I absolutely love this new device! It is amazing and works perfectly."}'
```

Check your logs, and you should see the `[Positive Responder]` has been triggered.

#### Negative Sentiment

```shell
curl -X POST http://localhost:3000/api/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"This is the worst product I have ever used. It broke after one day."}'
```

This time, the `[Negative Responder]` will fire.

</Steps>

---

## 💻 Dive into the Code

Want to explore the complete implementation? Check out the full source code and additional examples in our GitHub repository:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Explore More Examples</h3>
        <p className="text-gray-600 mb-4">Get hands-on with the complete source code, configuration files, and additional examples to accelerate your learning.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/sentimental-analysis" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Sentiment Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Power of a Simple Primitive

This sentiment analysis application is a powerful demonstration of the Motia philosophy. By embracing the `step` as a core primitive, we've turned a potentially complex, branching workflow into a series of simple, understandable, and scalable components.

This is just the beginning. From here, you can extend the application by adding new steps to handle neutral sentiment, send notifications, or store results in a database. The event-driven architecture of Motia makes it easy to add new functionality without disrupting the existing flow.

We encourage you to explore, experiment, and see for yourself how Motia can simplify your most complex backend challenges. Happy coding!


## Examples
[sentiment-analysis](/docs/examples/sentiment-analysis): Code example
---
title: 'Sentiment Analysis'
description: 'Dynamic Workflows: Building a Sentiment Analyzer with Motia'
---

In modern application development, workflows are rarely linear. Whether you're building a simple "prompt => response" system or a complex, multi-stage data processing pipeline, you often need your application to make decisions and route data dynamically. This is where the power of event-driven architecture shines, and where the Motia framework provides a clear path forward.

<div className="my-8">![motia workbench for sentiment analysis](./../img/sentimental-analysis.png)</div>

This guide explores how to build a dynamic sentiment analysis application that uses an LLM to determine how to proceed. We'll cover:

1.  **The Motia Philosophy**: How `steps` as a core primitive simplify complex architectures.
2.  **Building the Workflow**: A step-by-step guide to creating the four key components of our application.
3.  **Visualizing the Flow**: How events chain together to create a cohesive, dynamic system.
4.  **Hands-On with the API**: How to run and test your new sentiment analyzer.

Let's dive in.

---

## A Step at a Time

<div className="my-8">![motia workbench for sentiment analysis](./../img/sentimental-analyzer-workbench.png)</div>

At the heart of the Motia framework is a simple but powerful idea: the **`step`**. A step is a self-contained, independent unit of logic that listens for an event, performs a task, and, optionally, emits a new event. This concept is the core primitive that allows you to break down even the most complex architectures into a series of simple, manageable components.

Instead of a monolithic application where business logic is tightly coupled, Motia encourages a decoupled, event-driven approach. This has several key advantages:

-   **Clarity**: Each step has a single responsibility, making the application easier to understand and reason about.
-   **Scalability**: Steps can be scaled independently, so you can allocate resources where they're needed most.
-   **Extensibility**: Adding new functionality is as simple as creating a new step and subscribing it to an existing event.
-   **Resilience**: The decoupled nature of steps means that a failure in one part of the system doesn't necessarily bring down the entire application.

In this project, we'll see this philosophy in action as we build a sentiment analyzer with four distinct steps, each with its own clear purpose.

---

## The Anatomy of Our Sentiment Analyzer

Our application will be composed of four steps. Let's explore each one.

<Folder name="steps" defaultOpen>
  <File name="analyzeSentimentApi.step.ts" />
  <File name="openAiAnalyzeSentiment.step.ts" />
  <File name="handlePositive.step.ts" />
  <File name="handleNegative.step.ts" />
</Folder>

<Tabs items={['analyzeSentimentApi', 'openAiAnalyzeSentiment', 'handlePositive', 'handleNegative']}>
  <Tab value="analyzeSentimentApi">
    This is the entry point to our workflow. It's an API step that listens for `POST` requests, validates the incoming data, and emits an `openai.analyzeSentimentRequest` event.

    ```ts
    // Receives user text, emits "openai.analyzeSentimentRequest".
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'api',
      name: 'analyzeSentimentApi',
      description: 'Receives user text and emits an event to trigger sentiment analysis.',
      path: '/api/analyze-sentiment',
      method: 'POST',
      emits: ['openai.analyzeSentimentRequest'],
      bodySchema: z.object({
        text: z.string().min(1, 'text is required'),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['analyzeSentimentApi'] = async (req, { emit, logger }) => {
      const { text } = req.body

      logger.info('[AnalyzeSentimentAPI] Received text', { text })

      // Emit an event to call OpenAI
      await emit({
        topic: 'openai.analyzeSentimentRequest',
        data: { text },
      })

      // Return right away
      return {
        status: 200,
        body: { status: 'Accepted', message: 'Your text is being analyzed' },
      }
    }
    ```

  </Tab>
  <Tab value="openAiAnalyzeSentiment">
    This step is the brains of our operation. It subscribes to the `openai.analyzeSentimentRequest` event, calls the OpenAI API, and then based on the response, emits either a `openai.positiveSentiment` or `openai.negativeSentiment` event. This is where the dynamic routing happens.

    ```ts
    // Calls OpenAI, instructing it to ONLY return JSON like {"sentiment":"positive","analysis":"..."}
    import { Handlers } from 'motia'
    import { z } from 'zod'
    import { OpenAI } from 'openai'

    // 1) Create an OpenAI client (newer syntax)
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

    export const config = {
      type: 'event',
      name: 'openAiSentimentAnalyzer',
      description: 'Calls OpenAI to analyze sentiment and emits corresponding events.',
      subscribes: ['openai.analyzeSentimentRequest'],
      // We'll emit different events: "openai.positiveSentiment" or "openai.negativeSentiment"
      emits: ['openai.positiveSentiment', 'openai.negativeSentiment'],
      input: z.object({ text: z.string() }),
      flows: ['sentiment-demo'],
    } as const

    // 3) Provide the code that runs on each event
    export const handler: Handlers['openAiSentimentAnalyzer'] = async (input, { emit, logger }) => {
      logger.info('[OpenAI Sentiment Analyzer] Prompting OpenAI...', { text: input.text })

      try {
        // We'll ask the model to ONLY return JSON with a "sentiment" field
        const systemPrompt =
          'You are an assistant that returns only JSON: {"sentiment":"positive|negative","analysis":"..."}'
        const userPrompt = `Analyze the sentiment of this text: "${input.text}". Return JSON with keys "sentiment" and "analysis".`

        // 4) Use the new openai syntax:
        const response = await openai.chat.completions.create({
          model: 'gpt-3.5-turbo',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
        })

        // 5) Log and parse the response
        const content = response.choices[0]?.message?.content || ''
        logger.info('[OpenAI Sentiment Analyzer] Raw response', { content })

        let parsed: { sentiment?: string; analysis?: string } = {}
        try {
          parsed = JSON.parse(content.trim())
        } catch (err) {
          logger.error('[OpenAI Sentiment Analyzer] Unable to parse JSON', { error: err })
          // If it's not JSON, we bail or handle differently
          return
        }

        // 6) Decide how to route the event
        if (parsed.sentiment) {
          if (parsed.sentiment.toLowerCase() === 'positive') {
            await emit({
              topic: 'openai.positiveSentiment',
              data: { ...parsed, sentiment: parsed.sentiment },
            })
          } else {
            // default to negative
            await emit({
              topic: 'openai.negativeSentiment',
              data: { ...parsed, sentiment: parsed.sentiment },
            })
          }
        } else {
          logger.error('[OpenAI Sentiment Analyzer] Sentiment is missing from the parsed response', { parsed })
        }
      } catch (err) {
        if (err instanceof Error) {
          logger.error('[OpenAI Sentiment Analyzer] Error calling OpenAI', { error: err.message })
        } else {
          logger.error('[OpenAI Sentiment Analyzer] An unknown error occurred while calling OpenAI', { error: err })
        }
      }
    }
    ```
  </Tab>
  <Tab value="handlePositive">
    A specialized responder that listens for the `openai.positiveSentiment` event and logs a confirmation message. In a real-world application, this could trigger a Slack notification, send an email, or kick off another workflow.

    ```ts
    // Handles "openai.positiveSentiment"
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'handlePositive',
      description: 'Handles positive sentiment responses.',
      subscribes: ['openai.positiveSentiment'],
      emits: [],
      input: z.object({
        sentiment: z.string(),
        analysis: z.string().optional(),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['handlePositive'] = async (input, { logger }) => {
      logger.info('[Positive Responder] The sentiment is positive!', { analysis: input.analysis })
      // Maybe notify a Slack channel: "All good vibes here!"
    }
    ```

  </Tab>
  <Tab value="handleNegative">
    Similar to the positive handler, this step listens for the `openai.negativeSentiment` event. This is where you could implement logic to escalate a customer complaint, create a support ticket, or alert the on-call team.

    ```ts
    // Handles "openai.negativeSentiment"
    import { Handlers } from 'motia'
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'handleNegative',
      description: 'Handles negative or unknown sentiment responses.',
      subscribes: ['openai.negativeSentiment'],
      emits: [],
      input: z.object({
        sentiment: z.string(),
        analysis: z.string().optional(),
      }),
      flows: ['sentiment-demo'],
    } as const

    export const handler: Handlers['handleNegative'] = async (input, { logger }) => {
      logger.info('[Negative Responder] The sentiment is negative or unknown.', { analysis: input.analysis })
      // Could escalate to a service, or respond gently, etc.
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

You can explore the workflow in the Workbench.

<div className="my-8">![Flow](./../img/sentimental-analyzer.png)</div>

You can also read your files and watch logs, traces, debug your architecture directly in the Workbench.

<div className="my-8">![Workbench](./../img/sentimental-analyzer-workbench.gif)</div>

---

## Trying It Out

Ready to see it in action? Let's get the project running.

<Steps>

### Install Dependencies

First, install the necessary npm packages.

```shell
npm install
```

### Set Your Environment Variables

You'll need an OpenAI API key for this project. Export it as an environment variable.

```shell
export OPENAI_API_KEY="sk-..."
```

### Run the Project

Start the Motia development server.

```shell
npm run dev
```

### Test the API

Now you can send requests to your API and see the workflow in action.

#### Positive Sentiment

```shell
curl -X POST http://localhost:3000/api/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"I absolutely love this new device! It is amazing and works perfectly."}'
```

Check your logs, and you should see the `[Positive Responder]` has been triggered.

#### Negative Sentiment

```shell
curl -X POST http://localhost:3000/api/analyze-sentiment \
  -H "Content-Type: application/json" \
  -d '{"text":"This is the worst product I have ever used. It broke after one day."}'
```

This time, the `[Negative Responder]` will fire.

</Steps>

---

## 💻 Dive into the Code

Want to explore the complete implementation? Check out the full source code and additional examples in our GitHub repository:

<div className="not-prose">
  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Explore More Examples</h3>
        <p className="text-gray-600 mb-4">Get hands-on with the complete source code, configuration files, and additional examples to accelerate your learning.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/sentimental-analysis" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Sentiment Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: The Power of a Simple Primitive

This sentiment analysis application is a powerful demonstration of the Motia philosophy. By embracing the `step` as a core primitive, we've turned a potentially complex, branching workflow into a series of simple, understandable, and scalable components.

This is just the beginning. From here, you can extend the application by adding new steps to handle neutral sentiment, send notifications, or store results in a database. The event-driven architecture of Motia makes it easy to add new functionality without disrupting the existing flow.

We encourage you to explore, experiment, and see for yourself how Motia can simplify your most complex backend challenges. Happy coding!

-   [trello-automation](/docs/examples/trello-automation): Documentation for trello-automation.
---
title: 'Trello Automation'
description: Build an automated card progression system for Trello boards with AI-powered summaries
---

import { TrelloTab, TrelloCodeContent } from '../../../components/TrelloCodeFetcher'

## Let's build a Trello automation system that:

1. Automatically progresses cards across board lists
2. Validates card completeness
3. Generates AI-powered summaries for code review
4. Integrates with Slack for notifications
5. Monitors due dates and sends overdue alerts

## Board Structure

The Trello board is organized into four main lists:

- **New Cards**: Entry point for all new cards
- **In Progress**: Active development stage
- **Needs Review**: Code review stage with AI summaries
- **Completed**: Successfully reviewed and approved cards

## The Steps

<Folder name="steps" defaultOpen>
  <File name="trello-webhook.step.ts" />
  <File name="trello-webhook-validation.step.ts" />
  <File name="validate-card-requirements.step.ts" />
  <File name="start-assigned-card.step.ts" />
  <File name="mark-card-for-review.step.ts" />
  <File name="complete-approved-card.step.ts" />
  <File name="check-overdue-cards.step.ts" />
  <File name="slack-notifier.step.ts" />
</Folder>

<Tabs items={['webhook', 'validation', 'requirements', 'assigned', 'review', 'completion', 'overdue', 'slack']}>
  <TrelloTab tab="webhook" value="trello-webhook" />
  <TrelloTab tab="validation" value="trello-webhook-validation" />
  <TrelloTab tab="requirements" value="validate-card-requirements" />
  <TrelloTab tab="assigned" value="start-assigned-card" />
  <TrelloTab tab="review" value="mark-card-for-review" />
  <TrelloTab tab="completion" value="complete-approved-card" />
  <TrelloTab tab="overdue" value="check-overdue-cards" />
  <TrelloTab tab="slack" value="slack-notifier" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: Trello Automation Steps](../img/trello-automation.png)</div>

1. **Card Validation** → Checks for required information
2. **Progress Tracking** → Moves cards between lists
3. **Review Process** → Generates AI summaries and notifies reviewers
4. **Completion Handling** → Processes approved cards

## Try It Out

<Steps>

### Prerequisites

Make sure you have:

- Trello account with API access
- Node.js installed
- Slack workspace (for notifications)
- OpenAI API key (for AI summaries)

### Clone the Repository

```bash
git clone git@github.com:MotiaDev/motia-examples.git
cd examples/trello-flow
```

### Install Dependencies

```bash
pnpm install
```

### Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Update your `.env` with the following credentials:

```bash
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_openai_model

SLACK_WEBHOOK_URL=your_slack_webhook_url

TRELLO_NEW_TASKS_LIST_ID=your_new_tasks_list_id
TRELLO_IN_PROGRESS_LIST_ID=your_in_progress_list_id
TRELLO_NEEDS_REVIEW_LIST_ID=your_needs_review_list_id
TRELLO_COMPLETED_LIST_ID=your_completed_list_id
```

### Set Up Trello Board

1. Create a new Trello board with these lists:

   - New Tasks
   - In Progress
   - Needs Review
   - Completed

2. Add a custom field:
   - Status (dropdown: Todo, In Progress, Done)

### Run the Application

```bash
pnpm dev
```

### Test the Flow

1. Create a new card in the "New Tasks" list
2. Assign a member to see it move to "In Progress"
3. Add an "approved" comment to see it move to "Completed"
4. Check Slack for notifications

</Steps>

<Callout type="info">
  For more detailed setup instructions and configuration options, check out the [full
  documentation](https://github.com/MotiaDev/motia-examples/tree/main/examples/trello-flow).
</Callout>{' '}



## Examples
[trello-automation](/docs/examples/trello-automation): Code example
---
title: 'Trello Automation'
description: Build an automated card progression system for Trello boards with AI-powered summaries
---

import { TrelloTab, TrelloCodeContent } from '../../../components/TrelloCodeFetcher'

## Let's build a Trello automation system that:

1. Automatically progresses cards across board lists
2. Validates card completeness
3. Generates AI-powered summaries for code review
4. Integrates with Slack for notifications
5. Monitors due dates and sends overdue alerts

## Board Structure

The Trello board is organized into four main lists:

- **New Cards**: Entry point for all new cards
- **In Progress**: Active development stage
- **Needs Review**: Code review stage with AI summaries
- **Completed**: Successfully reviewed and approved cards

## The Steps

<Folder name="steps" defaultOpen>
  <File name="trello-webhook.step.ts" />
  <File name="trello-webhook-validation.step.ts" />
  <File name="validate-card-requirements.step.ts" />
  <File name="start-assigned-card.step.ts" />
  <File name="mark-card-for-review.step.ts" />
  <File name="complete-approved-card.step.ts" />
  <File name="check-overdue-cards.step.ts" />
  <File name="slack-notifier.step.ts" />
</Folder>

<Tabs items={['webhook', 'validation', 'requirements', 'assigned', 'review', 'completion', 'overdue', 'slack']}>
  <TrelloTab tab="webhook" value="trello-webhook" />
  <TrelloTab tab="validation" value="trello-webhook-validation" />
  <TrelloTab tab="requirements" value="validate-card-requirements" />
  <TrelloTab tab="assigned" value="start-assigned-card" />
  <TrelloTab tab="review" value="mark-card-for-review" />
  <TrelloTab tab="completion" value="complete-approved-card" />
  <TrelloTab tab="overdue" value="check-overdue-cards" />
  <TrelloTab tab="slack" value="slack-notifier" />
</Tabs>

## Visual Overview

Here's how the automation flow works:

<div className="my-8">![Flow: Trello Automation Steps](../img/trello-automation.png)</div>

1. **Card Validation** → Checks for required information
2. **Progress Tracking** → Moves cards between lists
3. **Review Process** → Generates AI summaries and notifies reviewers
4. **Completion Handling** → Processes approved cards

## Try It Out

<Steps>

### Prerequisites

Make sure you have:

- Trello account with API access
- Node.js installed
- Slack workspace (for notifications)
- OpenAI API key (for AI summaries)

### Clone the Repository

```bash
git clone git@github.com:MotiaDev/motia-examples.git
cd examples/trello-flow
```

### Install Dependencies

```bash
pnpm install
```

### Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Update your `.env` with the following credentials:

```bash
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_openai_model

SLACK_WEBHOOK_URL=your_slack_webhook_url

TRELLO_NEW_TASKS_LIST_ID=your_new_tasks_list_id
TRELLO_IN_PROGRESS_LIST_ID=your_in_progress_list_id
TRELLO_NEEDS_REVIEW_LIST_ID=your_needs_review_list_id
TRELLO_COMPLETED_LIST_ID=your_completed_list_id
```

### Set Up Trello Board

1. Create a new Trello board with these lists:

   - New Tasks
   - In Progress
   - Needs Review
   - Completed

2. Add a custom field:
   - Status (dropdown: Todo, In Progress, Done)

### Run the Application

```bash
pnpm dev
```

### Test the Flow

1. Create a new card in the "New Tasks" list
2. Assign a member to see it move to "In Progress"
3. Add an "approved" comment to see it move to "Completed"
4. Check Slack for notifications

</Steps>

<Callout type="info">
  For more detailed setup instructions and configuration options, check out the [full
  documentation](https://github.com/MotiaDev/motia-examples/tree/main/examples/trello-flow).
</Callout>{' '}


-   [uptime-discord-monitor](/docs/examples/uptime-discord-monitor): Documentation for uptime-discord-monitor.
---
title: 'Uptime Monitor'
description: 'Real-Time Uptime Monitoring: Building a Resilient Website Monitor with Motia'
---

In today's modern era, website uptime is critical for business success. Whether you're monitoring a personal blog or enterprise applications, you need a reliable system that can detect outages, send alerts, and provide visibility into your site's health. Traditional monitoring solutions often involve complex infrastructure and vendor lock-in, but there's a better way.

This comprehensive guide explores how to build a production-ready uptime monitoring system using Motia's event-driven architecture. We'll cover:

1.  **Event-Driven Monitoring**: How Motia's `steps` create a scalable, maintainable monitoring pipeline.
2.  **Building the Architecture**: A detailed walkthrough of our five-component monitoring system.
3.  **Smart Alerting**: Implementing rate limiting and status change detection to prevent spam.

Let's build a monitoring system that actually works for you.

---

## The Power of Event-Driven Monitoring

<div className="my-8">![Uptime Monitor Architecture](./../img/uptime-monitor-architecture.png)</div>

At its core, our uptime monitoring system solves a fundamental challenge: how do you continuously monitor multiple websites without creating a brittle, monolithic application? Traditional monitoring tools often suffer from tight coupling, making them difficult to scale and customize. Our Motia-powered solution breaks this down into discrete, event-driven components that each handle a specific aspect of monitoring.

The magic happens through the integration of proven technologies and patterns:

-   **[Cron-Based Scheduling](https://en.wikipedia.org/wiki/Cron)**: Configurable check intervals using familiar cron expressions
-   **[Discord Webhooks](https://discord.com/developers/docs/resources/webhook)**: Instant notifications with rich formatting
-   **[Token Bucket Rate Limiting](https://en.wikipedia.org/wiki/Token_bucket)**: Intelligent alert throttling to prevent spam
-   **[Motia Framework](https://motia.dev)**: Event-driven orchestration with built-in observability

Instead of a monolithic monitoring daemon, we get a resilient architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our Monitoring System

Our application consists of five specialized steps, each handling a specific part of the monitoring workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="cron.step.js" />
  <File name="checker.step.js" />
  <File name="alerter.step.js" />
  <File name="health.step.js" />
</Folder>

<Folder name="lib" defaultOpen>
  <File name="env.js" />
  <File name="rate-limiter.js" />
  <File name="streams.js" />
</Folder>

<Tabs items={['cron', 'checker', 'alerter', 'health', 'utilities']}>
  <Tab value="cron">
    The heartbeat of our monitoring system. This cron-triggered step periodically emits check requests for all configured websites, acting as the central scheduler.

    ```js
    import { config as envConfig } from '../lib/env.js';

    export const config = {
      type: 'cron',
      name: 'UptimeCronTrigger',
      cron: envConfig.cron,
      emits: ['check.requested'],
      flows: ['uptime-monitoring']
    };

    export async function handler(context) {
      context.logger.info(`Starting uptime checks for ${envConfig.sites.length} sites`);
      context.logger.info(`Sites configured: ${JSON.stringify(envConfig.sites)}`);

      try {
        // Emit one check.requested event per configured site URL
        for (const url of envConfig.sites) {
          context.logger.info(`Scheduling check for: ${url}`);
          
          await context.emit({ 
            topic: 'check.requested', 
            data: { url: url } 
          });
          
          context.logger.info(`Successfully emitted for: ${url}`);
        }

        context.logger.info(`Successfully scheduled checks for all ${envConfig.sites.length} sites`);
      } catch (error) {
        context.logger.error('Error during cron execution:', error);
        throw error;
      }
    }
    ```

  </Tab>
  <Tab value="checker">
    The core monitoring component that performs HTTP checks on websites. It handles timeouts, errors, and response code analysis, then emits results for further processing.

    ```js
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'WebsiteChecker',
      description: 'Performs HTTP checks on websites and emits results',
      subscribes: ['check.requested'],
      emits: ['check.result', 'status.stream'],
      input: z.object({
        url: z.string().url('Must be a valid URL')
      }),
      flows: ['uptime-monitoring'],
    }

    export const handler = async (input, { logger, emit }) => {
      const { url } = input
      
      logger.info('Starting website check', { url })

      const startTime = performance.now()
      let result

      try {
        // Validate URL format before making request
        const urlObj = new URL(url)
        if (!['http:', 'https:'].includes(urlObj.protocol)) {
          throw new Error('Only HTTP and HTTPS protocols are supported')
        }

        // Perform HTTP request with timeout handling
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 second timeout

        const response = await fetch(url, {
          method: 'GET',
          signal: controller.signal,
          headers: {
            'User-Agent': 'Motia-Uptime-Monitor/1.0',
            'Accept': '*/*',
            'Cache-Control': 'no-cache'
          },
          redirect: 'manual'
        })

        clearTimeout(timeoutId)
        const endTime = performance.now()
        const responseTime = Math.round(endTime - startTime)

        // Determine status: 2xx and 3xx as UP, everything else as DOWN
        const status = (response.status >= 200 && response.status < 400) ? 'UP' : 'DOWN'

        result = {
          url,
          status,
          code: response.status,
          responseTime,
          checkedAt: new Date().toISOString(),
          error: null
        }

        logger.info('Website check completed', {
          url,
          status,
          code: response.status,
          responseTime
        })

      } catch (error) {
        const endTime = performance.now()
        const responseTime = Math.round(endTime - startTime)

        let errorMessage = error.message

        // Handle specific error types with detailed messages
        if (error.name === 'AbortError') {
          errorMessage = 'Request timeout (10s)'
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
          errorMessage = 'Network error - unable to connect'
        } else if (error.code === 'ENOTFOUND') {
          errorMessage = 'DNS resolution failed'
        } else if (error.code === 'ECONNREFUSED') {
          errorMessage = 'Connection refused'
        }

        result = {
          url,
          status: 'DOWN',
          code: null,
          responseTime,
          checkedAt: new Date().toISOString(),
          error: errorMessage
        }

        logger.error('Website check failed', {
          url,
          error: errorMessage,
          responseTime,
          originalError: error.code || error.name
        })
      }

      // Emit results to both alerter and dashboard
      await emit({ topic: 'check.result', data: result })
      await emit({ topic: 'status.stream', data: result })

      logger.info('Check results emitted successfully', { url, status: result.status })
    }
    ```

  </Tab>
  <Tab value="alerter">
    The intelligent alerting system that detects status changes, applies rate limiting, and sends Discord notifications. Only triggers alerts when status actually changes, preventing noise.

    ```js
    import { z } from 'zod'
    import { getPreviousStatus } from '../lib/streams.js'
    import { createRateLimiter } from '../lib/rate-limiter.js'
    import { config as envConfig } from '../lib/env.js'

    // Create a rate limiter instance for Discord alerts
    const rateLimiter = createRateLimiter({
      burst: envConfig.alertBurst,
      windowSec: envConfig.alertWindowSec
    })

    export const config = {
      type: 'event',
      name: 'DiscordAlerter',
      description: 'Sends Discord notifications when website status changes',
      subscribes: ['check.result'],
      emits: [],
      input: z.object({
        url: z.string().url(),
        status: z.enum(['UP', 'DOWN']),
        code: z.number().nullable(),
        responseTime: z.number(),
        checkedAt: z.string(),
        error: z.string().nullable()
      }),
      flows: ['uptime-monitoring'],
    }

    function createDiscordMessage(result, previousStatus) {
      const { url, status, code, responseTime, checkedAt, error } = result

      const isUp = status === 'UP'
      const emoji = isUp ? '🟢' : '🔴'
      const color = isUp ? 0x00ff00 : 0xff0000

      const content = `${emoji} ${url} is ${status}${code ? ` (${code})` : ''}`

      const fields = [
        {
          name: 'Response Time',
          value: `${responseTime}ms`,
          inline: true
        }
      ]

      if (code !== null) {
        fields.push({
          name: 'Status Code',
          value: code.toString(),
          inline: true
        })
      }

      if (error) {
        fields.push({
          name: 'Error',
          value: error,
          inline: false
        })
      }

      fields.push({
        name: 'Previous Status',
        value: previousStatus,
        inline: true
      })

      return {
        content,
        embeds: [{
          title: `Website Status Change: ${status}`,
          description: `${url} changed from ${previousStatus} to ${status}`,
          color,
          timestamp: checkedAt,
          fields
        }]
      }
    }

    export const handler = async (input, { logger }) => {
      const { url, status } = input

      // Get the previous status for comparison
      const previousResult = getPreviousStatus(url)

      // Handle first-time checks
      if (!previousResult) {
        logger.info('First-time check for site, no alert needed', { url, status })
        const { updateLastStatus } = await import('../lib/streams.js')
        updateLastStatus(input)
        return
      }

      const previousStatus = previousResult.status

      // Only trigger alerts when status actually changes
      if (status === previousStatus) {
        logger.debug('Status unchanged, no alert needed', { url, status, previousStatus })
        const { updateLastStatus } = await import('../lib/streams.js')
        updateLastStatus(input)
        return
      }

      // Status has changed - check rate limiting
      logger.info('Status change detected', {
        url,
        previousStatus,
        newStatus: status,
        transition: `${previousStatus} → ${status}`
      })

      if (!rateLimiter.consume(url)) {
        const timeUntilNext = rateLimiter.getTimeUntilNextToken(url)
        logger.warn('Alert rate limited', {
          url,
          status,
          previousStatus,
          timeUntilNextMs: timeUntilNext,
          tokensRemaining: rateLimiter.getTokenCount(url)
        })
        return
      }

      // Send Discord notification
      const message = createDiscordMessage(input, previousStatus)
      
      try {
        const response = await fetch(envConfig.discordWebhook, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'Motia-Uptime-Monitor/1.0'
          },
          body: JSON.stringify(message)
        })

        if (response.ok) {
          logger.info('Discord alert sent successfully', { url, status, previousStatus })
        } else {
          const errorText = await response.text().catch(() => 'Unknown error')
          logger.error('Discord webhook failed', {
            status: response.status,
            error: errorText
          })
        }
      } catch (error) {
        logger.error('Failed to send Discord webhook', {
          error: error.message
        })
      }

      // Update status store after sending alert
      const { updateLastStatus } = await import('../lib/streams.js')
      updateLastStatus(input)
    }
    ```

  </Tab>
  <Tab value="health">
    A health check endpoint that provides system status and monitoring metrics. Essential for monitoring the monitor itself and integrating with external health check services.

    ```js
    import { z } from 'zod'
    import { getSnapshot } from '../lib/streams.js'
    import { config as envConfig } from '../lib/env.js'

    export const config = {
      type: 'api',
      name: 'HealthCheck',
      description: 'Provides system health status endpoint',
      method: 'GET',
      path: '/healthz',
      emits: [],
      responseSchema: {
        200: z.object({
          status: z.literal('ok'),
          sitesConfigured: z.number(),
          lastKnown: z.record(z.any()),
          now: z.string()
        })
      },
      flows: ['uptime-monitoring'],
    }

    export const handler = async (_, { logger }) => {
      logger.info('Health check endpoint accessed')
      
      try {
        const now = new Date().toISOString()
        const sitesConfigured = envConfig.sites.length
        const lastKnown = getSnapshot()
        
        const response = {
          status: 'ok',
          sitesConfigured,
          lastKnown,
          now
        }
        
        logger.info('Health check completed successfully', { 
          sitesConfigured,
          sitesWithStatus: Object.keys(lastKnown).length
        })
        
        return {
          status: 200,
          body: response
        }
        
      } catch (error) {
        logger.error('Health check failed', { 
          error: error.message,
          stack: error.stack
        })
        
        return {
          status: 200,
          body: {
            status: 'ok',
            sitesConfigured: 0,
            lastKnown: {},
            now: new Date().toISOString(),
            error: error.message
          }
        }
      }
    }
    ```

  </Tab>
  <Tab value="utilities">
    Three essential utility libraries that power the monitoring system: environment validation, rate limiting, and persistent status storage.

    **Environment Configuration (`lib/env.js`)**
    ```js
    // Validates Discord webhook URLs
    function isValidDiscordWebhook(url) {
      if (!url || typeof url !== 'string') return false;
      
      try {
        const parsed = new URL(url);
        return parsed.hostname === 'discord.com' || parsed.hostname === 'discordapp.com';
      } catch {
        return false;
      }
    }

    // Parses and validates the SITES environment variable
    function parseSites(sitesJson) {
      if (!sitesJson) {
        throw new Error('SITES environment variable is required');
      }

      let sites;
      try {
        sites = JSON.parse(sitesJson);
      } catch (error) {
        throw new Error(`Invalid SITES JSON format: ${error.message}`);
      }

      if (!Array.isArray(sites) || sites.length === 0) {
        throw new Error('SITES must be a non-empty JSON array of URLs');
      }

      // Validate each URL
      sites.forEach(site => {
        if (typeof site !== 'string') {
          throw new Error(`Invalid site URL: ${site} (must be string)`);
        }
        try {
          new URL(site);
        } catch {
          throw new Error(`Invalid site URL format: ${site}`);
        }
      });

      return sites;
    }

    export const config = {
      discordWebhook: process.env.DISCORD_WEBHOOK,
      sites: parseSites(process.env.SITES),
      cron: process.env.CHECK_INTERVAL_CRON || '*/1 * * * *',
      alertBurst: parseInt(process.env.ALERT_BURST) || 3,
      alertWindowSec: parseInt(process.env.ALERT_WINDOW_SEC) || 300
    };
    ```

    **Rate Limiter (`lib/rate-limiter.js`)**
    ```js
    // Token bucket rate limiter with per-site isolation
    export function createRateLimiter({ burst, windowSec }) {
      const buckets = new Map()
      const refillRate = burst / (windowSec * 1000)

      function consume(siteUrl) {
        const bucket = getBucket(siteUrl)
        refillBucket(bucket)
        
        if (bucket.tokens >= 1) {
          bucket.tokens -= 1
          return true
        }
        
        return false
      }

      function getBucket(siteUrl) {
        if (!buckets.has(siteUrl)) {
          buckets.set(siteUrl, {
            tokens: burst,
            lastRefill: Date.now()
          })
        }
        return buckets.get(siteUrl)
      }

      function refillBucket(bucket) {
        const now = Date.now()
        const timePassed = now - bucket.lastRefill
        
        if (timePassed > 0) {
          const tokensToAdd = timePassed * refillRate
          bucket.tokens = Math.min(burst, bucket.tokens + tokensToAdd)
          bucket.lastRefill = now
        }
      }

      return { consume, /* other methods */ }
    }
    ```

    **Status Storage (`lib/streams.js`)**
    ```js
    // File-based persistent storage for site status
    import { readFileSync, writeFileSync, existsSync } from 'fs'

    const STORE_FILE = join(process.cwd(), '.motia', 'status-store.json')

    export function updateLastStatus(result) {
      // Validate input
      if (!result?.url || !['UP', 'DOWN'].includes(result.status)) {
        throw new Error('Invalid result object')
      }

      const store = loadStatusStore()
      store[result.url] = { ...result }
      saveStatusStore(store)
    }

    export function getPreviousStatus(url) {
      const store = loadStatusStore()
      const result = store[url]
      return result ? { ...result } : null
    }

    export function getSnapshot() {
      const store = loadStatusStore()
      const snapshot = {}
      
      for (const [url, result] of Object.entries(store)) {
        snapshot[url] = { ...result }
      }
      
      return snapshot
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your monitoring pipeline, making it easy to understand the event flow and debug issues in real-time.

<div className="my-8">![Uptime Monitor in Motia Workbench](./../img/uptime-monitor.gif)</div>

You can monitor real-time status checks, view Discord alert logs, and trace the execution of each step directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monitoring solutions.

---

## Key Features & Benefits

### ⚡ **Event-Driven Architecture**
Each component is independent and communicates through events, making the system highly scalable and maintainable.

### 🎯 **Smart Status Detection**  
Only triggers alerts when status actually changes (UP ↔ DOWN), eliminating noise from temporary fluctuations.

### 🚨 **Intelligent Rate Limiting**
Token bucket algorithm prevents alert spam during site flapping while ensuring critical alerts get through.

### 📊 **Built-in Observability**
Comprehensive logging, health checks, and real-time status tracking with persistent storage.

### 🔧 **Production-Ready**
Robust error handling, timeout management, and configurable check intervals ensure reliability.

### 🎨 **Rich Discord Alerts**
Beautiful embedded messages with response times, error details, and status transitions.

---

## Data Flow & Event Architecture

![Uptime Monitor Event Flow](./../img/uptime-monitor-flow.png)

### Event Flow
1. **Cron Trigger** → Emits `check.requested` events for each configured site
2. **Website Checker** → Receives `check.requested`, performs HTTP check
3. **Status Update** → Checker emits `check.result` with result
4. **Alert Processing** → Alerter receives `check.result`, detects status changes
5. **Discord Notification** → Alerter sends webhook if status changed and rate limit allows
6. **Status Storage** → Status is persisted for health endpoint and future comparisons

---

## Trying It Out

Ready to build your own production-ready monitoring system? Let's get it running.

<Steps>

### Install Dependencies

Install the necessary npm packages and set up the development environment.

```shell
npm install
```

### Configure Environment Variables

Create a `.env` file with your monitoring configuration. You'll need a Discord webhook URL and the sites you want to monitor.

```shell
# Required: Discord webhook for alerts
DISCORD_WEBHOOK="https://discord.com/api/webhooks/123456789/your-webhook-token"

# Required: JSON array of URLs to monitor
SITES='["https://example.com", "https://api.yourdomain.com", "https://blog.yoursite.org"]'

# Optional: Check frequency (default: every minute)
CHECK_INTERVAL_CRON="*/1 * * * *"

# Optional: Rate limiting (default: 3 alerts per 5 minutes)
ALERT_BURST="3"
ALERT_WINDOW_SEC="300"
```

### Set Up Discord Webhook

Create a Discord webhook to receive alerts:

1. Go to your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Copy the webhook URL and add it to your `.env` file

### Run the Monitoring System

Start the Motia development server to begin monitoring your websites.

```shell
npm run dev
```

### Check System Health

Verify your monitoring system is working correctly:

```shell
curl http://localhost:3000/healthz
```

You should see a response with your configured sites and their current status:

```json
{
  "status": "ok",
  "sitesConfigured": 3,
  "lastKnown": {
    "https://example.com": {
      "url": "https://example.com",
      "status": "UP",
      "code": 200,
      "responseTime": 245,
      "checkedAt": "2024-01-15T10:30:00.000Z",
      "error": null
    }
  },
  "now": "2024-01-15T10:35:00.000Z"
}
```

### Monitor the Logs

Watch the logs to see your monitoring system in action:

- **Cron triggers**: Check scheduling for all configured sites
- **Website checks**: HTTP requests and response analysis  
- **Status changes**: UP/DOWN transitions and Discord alerts
- **Rate limiting**: Alert suppression during site flapping

</Steps>

---

## Advanced Configuration

### Custom Check Intervals

Modify the cron expression to change monitoring frequency:

```shell
# Every 5 minutes
CHECK_INTERVAL_CRON="*/5 * * * *"

# Every hour
CHECK_INTERVAL_CRON="0 * * * *"

# Every 6 hours
CHECK_INTERVAL_CRON="0 */6 * * *"

# Business hours only (9 AM - 5 PM, Mon-Fri)
CHECK_INTERVAL_CRON="* 9-17 * * 1-5"
```

### Alert Rate Limiting

Fine-tune the rate limiting to match your needs:

```shell
# Very strict: 1 alert per 10 minutes
ALERT_BURST="1"
ALERT_WINDOW_SEC="600"

# More permissive: 5 alerts per 2 minutes
ALERT_BURST="5"  
ALERT_WINDOW_SEC="120"
```

### Multi-Environment Monitoring

Set up different monitoring configurations for different environments:

```shell
# Production sites
SITES='["https://app.production.com", "https://api.production.com"]'

# Staging sites  
SITES='["https://app.staging.com", "https://api.staging.com"]'

# Development sites
SITES='["https://app.dev.com", "http://localhost:8080"]'
```

### Custom Discord Alert Formatting

Modify the `createDiscordMessage` function in `alerter.step.js` to customize alert appearance:

```js
function createDiscordMessage(result, previousStatus) {
  const { url, status, code, responseTime } = result
  
  // Custom colors for your brand
  const color = status === 'UP' ? 0x2ecc71 : 0xe74c3c
  
  // Custom emoji and formatting
  const emoji = status === 'UP' ? '✅' : '❌'
  const urgency = responseTime > 5000 ? '🐌 SLOW' : '⚡ FAST'
  
  return {
    content: `${emoji} **${url}** is ${status}`,
    embeds: [{
      title: `${urgency} Website ${status}`,
      description: `**${url}** changed from ${previousStatus} to ${status}`,
      color,
      timestamp: result.checkedAt,
      fields: [
        {
          name: '⏱️ Response Time',
          value: `${responseTime}ms`,
          inline: true
        },
        {
          name: '📊 Status Code', 
          value: code?.toString() || 'N/A',
          inline: true
        }
      ]
    }]
  }
}
```

---

## Troubleshooting

### Common Issues

**Sites not being checked:**
- Verify `SITES` environment variable is valid JSON
- Check cron expression syntax using [crontab.guru](https://crontab.guru)
- Review logs for parsing errors

**Discord alerts not working:**
- Verify `DISCORD_WEBHOOK` URL is correct
- Test webhook manually: `curl -X POST $DISCORD_WEBHOOK -H "Content-Type: application/json" -d '{"content":"Test message"}'`
- Check Discord webhook permissions

**High memory usage:**
- Monitor status store size with health endpoint
- Consider implementing status history cleanup
- Reduce check frequency for many sites

**False positive alerts:**
- Increase timeout values in checker step
- Implement retry logic before marking as DOWN
- Adjust rate limiting to reduce noise

### Performance Tips

- **Large Site Lists**: Consider sharding across multiple instances
- **Slow Sites**: Implement custom timeout values per site
- **High Frequency**: Use Redis for status storage instead of file system
- **Alert Fatigue**: Implement escalation policies and alert grouping

### Monitoring the Monitor

Set up monitoring for your monitoring system:

```shell
# Monitor the health endpoint itself
curl -f http://localhost:3000/healthz || echo "Monitor is down!"

# Check for recent status updates
curl http://localhost:3000/healthz | jq '.lastKnown | to_entries | map(select(.value.checkedAt > (now - 300)))'

# Verify all sites are being checked
curl http://localhost:3000/healthz | jq '.sitesConfigured == (.lastKnown | length)'
```

---

## 💻 Dive into the Code

Want to explore the complete monitoring implementation? Check out the full source code, including all steps, utilities, and configuration examples:

<div className="not-prose">
  <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete Uptime Monitor</h3>
        <p className="text-gray-600 mb-4">Access the full implementation with event steps, utility libraries, Discord integration, and production-ready configuration.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/motia-uptime-monitor" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Monitor Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Monitoring That Actually Works

This uptime monitoring system demonstrates the power of event-driven architecture for infrastructure monitoring. By breaking down monitoring into discrete, specialized components, we've created a system that's not only reliable but also extensible and maintainable.

The event-driven approach means you can easily:
- **Add new notification channels** (Slack, PagerDuty, email) by creating new steps
- **Implement custom health checks** (database connectivity, API endpoints, SSL certificates)
- **Scale monitoring** across multiple regions or environments
- **Integrate with existing systems** without disrupting the core monitoring loop

Key architectural benefits:
- **Resilience**: Component failures don't bring down the entire system
- **Observability**: Built-in logging and tracing at every step
- **Flexibility**: Easy to modify check intervals, alert logic, or add new features
- **Testing**: Each component can be tested in isolation

From here, you can extend the system by:
- Adding support for different check types (TCP, database, custom health endpoints)
- Implementing escalation policies and on-call rotations
- Building a web dashboard for historical data and trends
- Adding integration with incident management systems
- Implementing multi-region monitoring with failover

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing monitoring pipeline.

Ready to build monitoring infrastructure that scales with your business? Start building with Motia today!



## Examples
[uptime-discord-monitor](/docs/examples/uptime-discord-monitor): Code example
---
title: 'Uptime Monitor'
description: 'Real-Time Uptime Monitoring: Building a Resilient Website Monitor with Motia'
---

In today's modern era, website uptime is critical for business success. Whether you're monitoring a personal blog or enterprise applications, you need a reliable system that can detect outages, send alerts, and provide visibility into your site's health. Traditional monitoring solutions often involve complex infrastructure and vendor lock-in, but there's a better way.

This comprehensive guide explores how to build a production-ready uptime monitoring system using Motia's event-driven architecture. We'll cover:

1.  **Event-Driven Monitoring**: How Motia's `steps` create a scalable, maintainable monitoring pipeline.
2.  **Building the Architecture**: A detailed walkthrough of our five-component monitoring system.
3.  **Smart Alerting**: Implementing rate limiting and status change detection to prevent spam.

Let's build a monitoring system that actually works for you.

---

## The Power of Event-Driven Monitoring

<div className="my-8">![Uptime Monitor Architecture](./../img/uptime-monitor-architecture.png)</div>

At its core, our uptime monitoring system solves a fundamental challenge: how do you continuously monitor multiple websites without creating a brittle, monolithic application? Traditional monitoring tools often suffer from tight coupling, making them difficult to scale and customize. Our Motia-powered solution breaks this down into discrete, event-driven components that each handle a specific aspect of monitoring.

The magic happens through the integration of proven technologies and patterns:

-   **[Cron-Based Scheduling](https://en.wikipedia.org/wiki/Cron)**: Configurable check intervals using familiar cron expressions
-   **[Discord Webhooks](https://discord.com/developers/docs/resources/webhook)**: Instant notifications with rich formatting
-   **[Token Bucket Rate Limiting](https://en.wikipedia.org/wiki/Token_bucket)**: Intelligent alert throttling to prevent spam
-   **[Motia Framework](https://motia.dev)**: Event-driven orchestration with built-in observability

Instead of a monolithic monitoring daemon, we get a resilient architecture where each component can be scaled, modified, or replaced independently.

---

## The Anatomy of Our Monitoring System

Our application consists of five specialized steps, each handling a specific part of the monitoring workflow. Let's explore the complete architecture.

<Folder name="steps" defaultOpen>
  <File name="cron.step.js" />
  <File name="checker.step.js" />
  <File name="alerter.step.js" />
  <File name="health.step.js" />
</Folder>

<Folder name="lib" defaultOpen>
  <File name="env.js" />
  <File name="rate-limiter.js" />
  <File name="streams.js" />
</Folder>

<Tabs items={['cron', 'checker', 'alerter', 'health', 'utilities']}>
  <Tab value="cron">
    The heartbeat of our monitoring system. This cron-triggered step periodically emits check requests for all configured websites, acting as the central scheduler.

    ```js
    import { config as envConfig } from '../lib/env.js';

    export const config = {
      type: 'cron',
      name: 'UptimeCronTrigger',
      cron: envConfig.cron,
      emits: ['check.requested'],
      flows: ['uptime-monitoring']
    };

    export async function handler(context) {
      context.logger.info(`Starting uptime checks for ${envConfig.sites.length} sites`);
      context.logger.info(`Sites configured: ${JSON.stringify(envConfig.sites)}`);

      try {
        // Emit one check.requested event per configured site URL
        for (const url of envConfig.sites) {
          context.logger.info(`Scheduling check for: ${url}`);
          
          await context.emit({ 
            topic: 'check.requested', 
            data: { url: url } 
          });
          
          context.logger.info(`Successfully emitted for: ${url}`);
        }

        context.logger.info(`Successfully scheduled checks for all ${envConfig.sites.length} sites`);
      } catch (error) {
        context.logger.error('Error during cron execution:', error);
        throw error;
      }
    }
    ```

  </Tab>
  <Tab value="checker">
    The core monitoring component that performs HTTP checks on websites. It handles timeouts, errors, and response code analysis, then emits results for further processing.

    ```js
    import { z } from 'zod'

    export const config = {
      type: 'event',
      name: 'WebsiteChecker',
      description: 'Performs HTTP checks on websites and emits results',
      subscribes: ['check.requested'],
      emits: ['check.result', 'status.stream'],
      input: z.object({
        url: z.string().url('Must be a valid URL')
      }),
      flows: ['uptime-monitoring'],
    }

    export const handler = async (input, { logger, emit }) => {
      const { url } = input
      
      logger.info('Starting website check', { url })

      const startTime = performance.now()
      let result

      try {
        // Validate URL format before making request
        const urlObj = new URL(url)
        if (!['http:', 'https:'].includes(urlObj.protocol)) {
          throw new Error('Only HTTP and HTTPS protocols are supported')
        }

        // Perform HTTP request with timeout handling
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 second timeout

        const response = await fetch(url, {
          method: 'GET',
          signal: controller.signal,
          headers: {
            'User-Agent': 'Motia-Uptime-Monitor/1.0',
            'Accept': '*/*',
            'Cache-Control': 'no-cache'
          },
          redirect: 'manual'
        })

        clearTimeout(timeoutId)
        const endTime = performance.now()
        const responseTime = Math.round(endTime - startTime)

        // Determine status: 2xx and 3xx as UP, everything else as DOWN
        const status = (response.status >= 200 && response.status < 400) ? 'UP' : 'DOWN'

        result = {
          url,
          status,
          code: response.status,
          responseTime,
          checkedAt: new Date().toISOString(),
          error: null
        }

        logger.info('Website check completed', {
          url,
          status,
          code: response.status,
          responseTime
        })

      } catch (error) {
        const endTime = performance.now()
        const responseTime = Math.round(endTime - startTime)

        let errorMessage = error.message

        // Handle specific error types with detailed messages
        if (error.name === 'AbortError') {
          errorMessage = 'Request timeout (10s)'
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
          errorMessage = 'Network error - unable to connect'
        } else if (error.code === 'ENOTFOUND') {
          errorMessage = 'DNS resolution failed'
        } else if (error.code === 'ECONNREFUSED') {
          errorMessage = 'Connection refused'
        }

        result = {
          url,
          status: 'DOWN',
          code: null,
          responseTime,
          checkedAt: new Date().toISOString(),
          error: errorMessage
        }

        logger.error('Website check failed', {
          url,
          error: errorMessage,
          responseTime,
          originalError: error.code || error.name
        })
      }

      // Emit results to both alerter and dashboard
      await emit({ topic: 'check.result', data: result })
      await emit({ topic: 'status.stream', data: result })

      logger.info('Check results emitted successfully', { url, status: result.status })
    }
    ```

  </Tab>
  <Tab value="alerter">
    The intelligent alerting system that detects status changes, applies rate limiting, and sends Discord notifications. Only triggers alerts when status actually changes, preventing noise.

    ```js
    import { z } from 'zod'
    import { getPreviousStatus } from '../lib/streams.js'
    import { createRateLimiter } from '../lib/rate-limiter.js'
    import { config as envConfig } from '../lib/env.js'

    // Create a rate limiter instance for Discord alerts
    const rateLimiter = createRateLimiter({
      burst: envConfig.alertBurst,
      windowSec: envConfig.alertWindowSec
    })

    export const config = {
      type: 'event',
      name: 'DiscordAlerter',
      description: 'Sends Discord notifications when website status changes',
      subscribes: ['check.result'],
      emits: [],
      input: z.object({
        url: z.string().url(),
        status: z.enum(['UP', 'DOWN']),
        code: z.number().nullable(),
        responseTime: z.number(),
        checkedAt: z.string(),
        error: z.string().nullable()
      }),
      flows: ['uptime-monitoring'],
    }

    function createDiscordMessage(result, previousStatus) {
      const { url, status, code, responseTime, checkedAt, error } = result

      const isUp = status === 'UP'
      const emoji = isUp ? '🟢' : '🔴'
      const color = isUp ? 0x00ff00 : 0xff0000

      const content = `${emoji} ${url} is ${status}${code ? ` (${code})` : ''}`

      const fields = [
        {
          name: 'Response Time',
          value: `${responseTime}ms`,
          inline: true
        }
      ]

      if (code !== null) {
        fields.push({
          name: 'Status Code',
          value: code.toString(),
          inline: true
        })
      }

      if (error) {
        fields.push({
          name: 'Error',
          value: error,
          inline: false
        })
      }

      fields.push({
        name: 'Previous Status',
        value: previousStatus,
        inline: true
      })

      return {
        content,
        embeds: [{
          title: `Website Status Change: ${status}`,
          description: `${url} changed from ${previousStatus} to ${status}`,
          color,
          timestamp: checkedAt,
          fields
        }]
      }
    }

    export const handler = async (input, { logger }) => {
      const { url, status } = input

      // Get the previous status for comparison
      const previousResult = getPreviousStatus(url)

      // Handle first-time checks
      if (!previousResult) {
        logger.info('First-time check for site, no alert needed', { url, status })
        const { updateLastStatus } = await import('../lib/streams.js')
        updateLastStatus(input)
        return
      }

      const previousStatus = previousResult.status

      // Only trigger alerts when status actually changes
      if (status === previousStatus) {
        logger.debug('Status unchanged, no alert needed', { url, status, previousStatus })
        const { updateLastStatus } = await import('../lib/streams.js')
        updateLastStatus(input)
        return
      }

      // Status has changed - check rate limiting
      logger.info('Status change detected', {
        url,
        previousStatus,
        newStatus: status,
        transition: `${previousStatus} → ${status}`
      })

      if (!rateLimiter.consume(url)) {
        const timeUntilNext = rateLimiter.getTimeUntilNextToken(url)
        logger.warn('Alert rate limited', {
          url,
          status,
          previousStatus,
          timeUntilNextMs: timeUntilNext,
          tokensRemaining: rateLimiter.getTokenCount(url)
        })
        return
      }

      // Send Discord notification
      const message = createDiscordMessage(input, previousStatus)
      
      try {
        const response = await fetch(envConfig.discordWebhook, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'Motia-Uptime-Monitor/1.0'
          },
          body: JSON.stringify(message)
        })

        if (response.ok) {
          logger.info('Discord alert sent successfully', { url, status, previousStatus })
        } else {
          const errorText = await response.text().catch(() => 'Unknown error')
          logger.error('Discord webhook failed', {
            status: response.status,
            error: errorText
          })
        }
      } catch (error) {
        logger.error('Failed to send Discord webhook', {
          error: error.message
        })
      }

      // Update status store after sending alert
      const { updateLastStatus } = await import('../lib/streams.js')
      updateLastStatus(input)
    }
    ```

  </Tab>
  <Tab value="health">
    A health check endpoint that provides system status and monitoring metrics. Essential for monitoring the monitor itself and integrating with external health check services.

    ```js
    import { z } from 'zod'
    import { getSnapshot } from '../lib/streams.js'
    import { config as envConfig } from '../lib/env.js'

    export const config = {
      type: 'api',
      name: 'HealthCheck',
      description: 'Provides system health status endpoint',
      method: 'GET',
      path: '/healthz',
      emits: [],
      responseSchema: {
        200: z.object({
          status: z.literal('ok'),
          sitesConfigured: z.number(),
          lastKnown: z.record(z.any()),
          now: z.string()
        })
      },
      flows: ['uptime-monitoring'],
    }

    export const handler = async (_, { logger }) => {
      logger.info('Health check endpoint accessed')
      
      try {
        const now = new Date().toISOString()
        const sitesConfigured = envConfig.sites.length
        const lastKnown = getSnapshot()
        
        const response = {
          status: 'ok',
          sitesConfigured,
          lastKnown,
          now
        }
        
        logger.info('Health check completed successfully', { 
          sitesConfigured,
          sitesWithStatus: Object.keys(lastKnown).length
        })
        
        return {
          status: 200,
          body: response
        }
        
      } catch (error) {
        logger.error('Health check failed', { 
          error: error.message,
          stack: error.stack
        })
        
        return {
          status: 200,
          body: {
            status: 'ok',
            sitesConfigured: 0,
            lastKnown: {},
            now: new Date().toISOString(),
            error: error.message
          }
        }
      }
    }
    ```

  </Tab>
  <Tab value="utilities">
    Three essential utility libraries that power the monitoring system: environment validation, rate limiting, and persistent status storage.

    **Environment Configuration (`lib/env.js`)**
    ```js
    // Validates Discord webhook URLs
    function isValidDiscordWebhook(url) {
      if (!url || typeof url !== 'string') return false;
      
      try {
        const parsed = new URL(url);
        return parsed.hostname === 'discord.com' || parsed.hostname === 'discordapp.com';
      } catch {
        return false;
      }
    }

    // Parses and validates the SITES environment variable
    function parseSites(sitesJson) {
      if (!sitesJson) {
        throw new Error('SITES environment variable is required');
      }

      let sites;
      try {
        sites = JSON.parse(sitesJson);
      } catch (error) {
        throw new Error(`Invalid SITES JSON format: ${error.message}`);
      }

      if (!Array.isArray(sites) || sites.length === 0) {
        throw new Error('SITES must be a non-empty JSON array of URLs');
      }

      // Validate each URL
      sites.forEach(site => {
        if (typeof site !== 'string') {
          throw new Error(`Invalid site URL: ${site} (must be string)`);
        }
        try {
          new URL(site);
        } catch {
          throw new Error(`Invalid site URL format: ${site}`);
        }
      });

      return sites;
    }

    export const config = {
      discordWebhook: process.env.DISCORD_WEBHOOK,
      sites: parseSites(process.env.SITES),
      cron: process.env.CHECK_INTERVAL_CRON || '*/1 * * * *',
      alertBurst: parseInt(process.env.ALERT_BURST) || 3,
      alertWindowSec: parseInt(process.env.ALERT_WINDOW_SEC) || 300
    };
    ```

    **Rate Limiter (`lib/rate-limiter.js`)**
    ```js
    // Token bucket rate limiter with per-site isolation
    export function createRateLimiter({ burst, windowSec }) {
      const buckets = new Map()
      const refillRate = burst / (windowSec * 1000)

      function consume(siteUrl) {
        const bucket = getBucket(siteUrl)
        refillBucket(bucket)
        
        if (bucket.tokens >= 1) {
          bucket.tokens -= 1
          return true
        }
        
        return false
      }

      function getBucket(siteUrl) {
        if (!buckets.has(siteUrl)) {
          buckets.set(siteUrl, {
            tokens: burst,
            lastRefill: Date.now()
          })
        }
        return buckets.get(siteUrl)
      }

      function refillBucket(bucket) {
        const now = Date.now()
        const timePassed = now - bucket.lastRefill
        
        if (timePassed > 0) {
          const tokensToAdd = timePassed * refillRate
          bucket.tokens = Math.min(burst, bucket.tokens + tokensToAdd)
          bucket.lastRefill = now
        }
      }

      return { consume, /* other methods */ }
    }
    ```

    **Status Storage (`lib/streams.js`)**
    ```js
    // File-based persistent storage for site status
    import { readFileSync, writeFileSync, existsSync } from 'fs'

    const STORE_FILE = join(process.cwd(), '.motia', 'status-store.json')

    export function updateLastStatus(result) {
      // Validate input
      if (!result?.url || !['UP', 'DOWN'].includes(result.status)) {
        throw new Error('Invalid result object')
      }

      const store = loadStatusStore()
      store[result.url] = { ...result }
      saveStatusStore(store)
    }

    export function getPreviousStatus(url) {
      const store = loadStatusStore()
      const result = store[url]
      return result ? { ...result } : null
    }

    export function getSnapshot() {
      const store = loadStatusStore()
      const snapshot = {}
      
      for (const [url, result] of Object.entries(store)) {
        snapshot[url] = { ...result }
      }
      
      return snapshot
    }
    ```

  </Tab>
</Tabs>

---

## Explore the Workbench

The Motia Workbench provides a visual representation of your monitoring pipeline, making it easy to understand the event flow and debug issues in real-time.

<div className="my-8">![Uptime Monitor in Motia Workbench](./../img/uptime-monitor.gif)</div>

You can monitor real-time status checks, view Discord alert logs, and trace the execution of each step directly in the Workbench interface. This makes development and debugging significantly easier compared to traditional monitoring solutions.

---

## Key Features & Benefits

### ⚡ **Event-Driven Architecture**
Each component is independent and communicates through events, making the system highly scalable and maintainable.

### 🎯 **Smart Status Detection**  
Only triggers alerts when status actually changes (UP ↔ DOWN), eliminating noise from temporary fluctuations.

### 🚨 **Intelligent Rate Limiting**
Token bucket algorithm prevents alert spam during site flapping while ensuring critical alerts get through.

### 📊 **Built-in Observability**
Comprehensive logging, health checks, and real-time status tracking with persistent storage.

### 🔧 **Production-Ready**
Robust error handling, timeout management, and configurable check intervals ensure reliability.

### 🎨 **Rich Discord Alerts**
Beautiful embedded messages with response times, error details, and status transitions.

---

## Data Flow & Event Architecture

![Uptime Monitor Event Flow](./../img/uptime-monitor-flow.png)

### Event Flow
1. **Cron Trigger** → Emits `check.requested` events for each configured site
2. **Website Checker** → Receives `check.requested`, performs HTTP check
3. **Status Update** → Checker emits `check.result` with result
4. **Alert Processing** → Alerter receives `check.result`, detects status changes
5. **Discord Notification** → Alerter sends webhook if status changed and rate limit allows
6. **Status Storage** → Status is persisted for health endpoint and future comparisons

---

## Trying It Out

Ready to build your own production-ready monitoring system? Let's get it running.

<Steps>

### Install Dependencies

Install the necessary npm packages and set up the development environment.

```shell
npm install
```

### Configure Environment Variables

Create a `.env` file with your monitoring configuration. You'll need a Discord webhook URL and the sites you want to monitor.

```shell
# Required: Discord webhook for alerts
DISCORD_WEBHOOK="https://discord.com/api/webhooks/123456789/your-webhook-token"

# Required: JSON array of URLs to monitor
SITES='["https://example.com", "https://api.yourdomain.com", "https://blog.yoursite.org"]'

# Optional: Check frequency (default: every minute)
CHECK_INTERVAL_CRON="*/1 * * * *"

# Optional: Rate limiting (default: 3 alerts per 5 minutes)
ALERT_BURST="3"
ALERT_WINDOW_SEC="300"
```

### Set Up Discord Webhook

Create a Discord webhook to receive alerts:

1. Go to your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Copy the webhook URL and add it to your `.env` file

### Run the Monitoring System

Start the Motia development server to begin monitoring your websites.

```shell
npm run dev
```

### Check System Health

Verify your monitoring system is working correctly:

```shell
curl http://localhost:3000/healthz
```

You should see a response with your configured sites and their current status:

```json
{
  "status": "ok",
  "sitesConfigured": 3,
  "lastKnown": {
    "https://example.com": {
      "url": "https://example.com",
      "status": "UP",
      "code": 200,
      "responseTime": 245,
      "checkedAt": "2024-01-15T10:30:00.000Z",
      "error": null
    }
  },
  "now": "2024-01-15T10:35:00.000Z"
}
```

### Monitor the Logs

Watch the logs to see your monitoring system in action:

- **Cron triggers**: Check scheduling for all configured sites
- **Website checks**: HTTP requests and response analysis  
- **Status changes**: UP/DOWN transitions and Discord alerts
- **Rate limiting**: Alert suppression during site flapping

</Steps>

---

## Advanced Configuration

### Custom Check Intervals

Modify the cron expression to change monitoring frequency:

```shell
# Every 5 minutes
CHECK_INTERVAL_CRON="*/5 * * * *"

# Every hour
CHECK_INTERVAL_CRON="0 * * * *"

# Every 6 hours
CHECK_INTERVAL_CRON="0 */6 * * *"

# Business hours only (9 AM - 5 PM, Mon-Fri)
CHECK_INTERVAL_CRON="* 9-17 * * 1-5"
```

### Alert Rate Limiting

Fine-tune the rate limiting to match your needs:

```shell
# Very strict: 1 alert per 10 minutes
ALERT_BURST="1"
ALERT_WINDOW_SEC="600"

# More permissive: 5 alerts per 2 minutes
ALERT_BURST="5"  
ALERT_WINDOW_SEC="120"
```

### Multi-Environment Monitoring

Set up different monitoring configurations for different environments:

```shell
# Production sites
SITES='["https://app.production.com", "https://api.production.com"]'

# Staging sites  
SITES='["https://app.staging.com", "https://api.staging.com"]'

# Development sites
SITES='["https://app.dev.com", "http://localhost:8080"]'
```

### Custom Discord Alert Formatting

Modify the `createDiscordMessage` function in `alerter.step.js` to customize alert appearance:

```js
function createDiscordMessage(result, previousStatus) {
  const { url, status, code, responseTime } = result
  
  // Custom colors for your brand
  const color = status === 'UP' ? 0x2ecc71 : 0xe74c3c
  
  // Custom emoji and formatting
  const emoji = status === 'UP' ? '✅' : '❌'
  const urgency = responseTime > 5000 ? '🐌 SLOW' : '⚡ FAST'
  
  return {
    content: `${emoji} **${url}** is ${status}`,
    embeds: [{
      title: `${urgency} Website ${status}`,
      description: `**${url}** changed from ${previousStatus} to ${status}`,
      color,
      timestamp: result.checkedAt,
      fields: [
        {
          name: '⏱️ Response Time',
          value: `${responseTime}ms`,
          inline: true
        },
        {
          name: '📊 Status Code', 
          value: code?.toString() || 'N/A',
          inline: true
        }
      ]
    }]
  }
}
```

---

## Troubleshooting

### Common Issues

**Sites not being checked:**
- Verify `SITES` environment variable is valid JSON
- Check cron expression syntax using [crontab.guru](https://crontab.guru)
- Review logs for parsing errors

**Discord alerts not working:**
- Verify `DISCORD_WEBHOOK` URL is correct
- Test webhook manually: `curl -X POST $DISCORD_WEBHOOK -H "Content-Type: application/json" -d '{"content":"Test message"}'`
- Check Discord webhook permissions

**High memory usage:**
- Monitor status store size with health endpoint
- Consider implementing status history cleanup
- Reduce check frequency for many sites

**False positive alerts:**
- Increase timeout values in checker step
- Implement retry logic before marking as DOWN
- Adjust rate limiting to reduce noise

### Performance Tips

- **Large Site Lists**: Consider sharding across multiple instances
- **Slow Sites**: Implement custom timeout values per site
- **High Frequency**: Use Redis for status storage instead of file system
- **Alert Fatigue**: Implement escalation policies and alert grouping

### Monitoring the Monitor

Set up monitoring for your monitoring system:

```shell
# Monitor the health endpoint itself
curl -f http://localhost:3000/healthz || echo "Monitor is down!"

# Check for recent status updates
curl http://localhost:3000/healthz | jq '.lastKnown | to_entries | map(select(.value.checkedAt > (now - 300)))'

# Verify all sites are being checked
curl http://localhost:3000/healthz | jq '.sitesConfigured == (.lastKnown | length)'
```

---

## 💻 Dive into the Code

Want to explore the complete monitoring implementation? Check out the full source code, including all steps, utilities, and configuration examples:

<div className="not-prose">
  <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Complete Uptime Monitor</h3>
        <p className="text-gray-600 mb-4">Access the full implementation with event steps, utility libraries, Discord integration, and production-ready configuration.</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/motia-examples/tree/main/examples/motia-uptime-monitor" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Monitor Example
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            More Examples →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Monitoring That Actually Works

This uptime monitoring system demonstrates the power of event-driven architecture for infrastructure monitoring. By breaking down monitoring into discrete, specialized components, we've created a system that's not only reliable but also extensible and maintainable.

The event-driven approach means you can easily:
- **Add new notification channels** (Slack, PagerDuty, email) by creating new steps
- **Implement custom health checks** (database connectivity, API endpoints, SSL certificates)
- **Scale monitoring** across multiple regions or environments
- **Integrate with existing systems** without disrupting the core monitoring loop

Key architectural benefits:
- **Resilience**: Component failures don't bring down the entire system
- **Observability**: Built-in logging and tracing at every step
- **Flexibility**: Easy to modify check intervals, alert logic, or add new features
- **Testing**: Each component can be tested in isolation

From here, you can extend the system by:
- Adding support for different check types (TCP, database, custom health endpoints)
- Implementing escalation policies and on-call rotations
- Building a web dashboard for historical data and trends
- Adding integration with incident management systems
- Implementing multi-region monitoring with failover

The event-driven architecture makes all of these extensions straightforward to implement without disrupting the existing monitoring pipeline.

Ready to build monitoring infrastructure that scales with your business? Start building with Motia today!


-   [api-endpoints](/docs/getting-started/build-your-first-motia-app/api-endpoints): Documentation for api-endpoints.
---
title: API Endpoints
description: Learn how to create HTTP API endpoints with Motia
---

## What You'll Build

A pet management API with these endpoints:

- **POST `/pets`** - Create a new pet
- **GET `/pets`** - List all pets
- **GET `/pets/:id`** - Get a specific pet
- **PUT `/pets/:id`** - Update a pet
- **DELETE `/pets/:id`** - Delete a pet

![workbench](../../img/build-your-first-app/api-workbench.png)
---

## Getting Started

Clone the example repository:

```bash
git clone https://github.com/MotiaDev/build-your-first-app.git
cd build-your-first-app
git checkout api-endpoints
```

Install dependencies:

```bash
npm install
```

Start the Workbench:

```bash
npm run dev
```

Your Workbench will be available at `http://localhost:3000`.

---

## Project Structure

<Folder name="my-pet-api" defaultOpen>
  <Folder name="steps" defaultOpen>
    <Folder name="typescript">
      <File name="create-pet.step.ts" />
      <File name="get-pets.step.ts" />
      <File name="get-pet.step.ts" />
      <File name="update-pet.step.ts" />
      <File name="delete-pet.step.ts" />
      <File name="ts-store.ts" />
    </Folder>
    <Folder name="javascript">
      <File name="create-pet.step.js" />
      <File name="get-pets.step.js" />
      <File name="get-pet.step.js" />
      <File name="update-pet.step.js" />
      <File name="delete-pet.step.js" />
      <File name="js-store.js" />
    </Folder>
    <Folder name="python">
      <File name="create_pet_step.py" />
      <File name="get_pets_step.py" />
      <File name="get_pet_step.py" />
      <File name="update_pet_step.py" />
      <File name="delete_pet_step.py" />
    </Folder>
  </Folder>
    <Folder name="services">
      <File name="pet_store.py" />
      <File name="types.py" />
    </Folder>
  <File name="package.json" />
  <File name="requirements.txt" />
  <File name="types.d.ts" />
</Folder>

<Callout type="info">
Files like `features.json` and `tutorial.tsx` are only for the interactive tutorial and are not part of Motia's project structure.
</Callout>

All code examples in this guide are available in the [build-your-first-app](https://github.com/MotiaDev/build-your-first-app/tree/api-endpoints) repository.

You can follow this guide to learn how to build a REST API with Motia step by step, or you can clone the repository and dive into our Interactive Tutorial to learn by doing directly in the Workbench.

![interactive-tutorial](../../img/build-your-first-app/interactive-tutorial.png)

---

## Creating Your First Endpoint

<Callout type="info">
This tutorial focuses on Motia's capabilities to create complete backend system from APIs to Streaming AI agents step-by-step. Here, we're showcasing writing APIs with Motia Steps - For data persistence, we use a simple JSON file store in the examples. In a real application, you would use a database like PostgreSQL, MongoDB, or any other data store of your choice. The complete store implementation is available in the [GitHub repository](https://github.com/MotiaDev/build-your-first-app/tree/api-endpoints).
</Callout>

### Configuration

Every API endpoint has two parts:

**Config** - Defines when and how the step runs:

| Property | Description |
|----------|-------------|
| `name` | Unique identifier |
| `type` | Set to `'api'` |
| `path` | URL path for the endpoint |
| `method` | HTTP method (GET, POST, PUT, DELETE) |

**Handler** - The function that executes your business logic.

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/typescript/create-pet.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/python/create_pet_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/javascript/create-pet.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/create-pet.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { TSStore } from './ts-store'

    const createPetSchema = z.object({
      name: z.string().min(1, 'Name is required'),
      species: z.enum(['dog', 'cat', 'bird', 'other']),
      ageMonths: z.number().int().min(0),
    })

    export const config: ApiRouteConfig = {
      name: 'CreatePet',
      type: 'api',
      path: '/pets',
      method: 'POST',
      bodySchema: createPetSchema,
      flows: ['PetManagement'],
    }

    export const handler: Handlers['CreatePet'] = async (req, { logger }) => {
      const data = createPetSchema.parse(req.body)
      
      // In a real application, this would be a database call
      // e.g., await db.pets.create(data)
      const pet = TSStore.create(data)

      logger.info('Pet created', { petId: pet.id })

      return { status: 201, body: pet }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/create_pet_step.py"
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "CreatePet",
        "type": "api",
        "path": "/pets",
        "method": "POST",
        "emits": []
    }

    async def handler(req, ctx=None):
        b = req.get("body") or {}
        name = b.get("name")
        species = b.get("species")
        age = b.get("ageMonths")

        if not isinstance(name, str) or not name.strip():
            return {"status": 400, "body": {"message": "Invalid name"}}
        if species not in ["dog", "cat", "bird", "other"]:
            return {"status": 400, "body": {"message": "Invalid species"}}

        try:
            age_val = int(age)
        except Exception:
            return {"status": 400, "body": {"message": "Invalid ageMonths"}}

        # In a real application, this would be a database call
        # e.g., pet = await db.pets.create(name, species, age_val)
        pet = pet_store.create(name, species, age_val)
        return {"status": 201, "body": pet}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/create-pet.step.js"
    const { create } = require('./js-store')

    const config = {
      name: 'CreatePet',
      type: 'api',
      path: '/pets',
      method: 'POST',
      emits: []
    }

    const handler = async (req) => {
      const b = req.body || {}
      const name = typeof b.name === 'string' && b.name.trim()
      const speciesOk = ['dog', 'cat', 'bird', 'other'].includes(b.species)
      const ageOk = Number.isFinite(b.ageMonths)

      if (!name || !speciesOk || !ageOk) {
        return { status: 400, body: { message: 'Invalid payload' } }
      }

      // In a real application, this would be a database call
      // e.g., const pet = await db.pets.create({ name, species: b.species, ageMonths: Number(b.ageMonths) })
      const pet = create({ name, species: b.species, ageMonths: Number(b.ageMonths) })
      return { status: 201, body: pet }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

## Testing Your API

You can test your endpoints using curl or the Workbench interface.

### Using curl

```bash
# Create a pet
curl -X POST http://localhost:3000/pets \
  -H "Content-Type: application/json" \
  -d '{"name": "Max", "species": "dog", "ageMonths": 24}'
```

### Using Workbench

You can also test your endpoint directly in the Workbench, which provides an interactive interface to test your API endpoints with real requests and see the responses in real-time:

![create-pet](../../img/build-your-first-app/create-api.png)

---
## Adding GET Endpoints

### List All Pets

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/typescript/get-pets.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/python/get_pets_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/javascript/get-pets.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/get-pets.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { TSStore } from './ts-store'

    export const config: ApiRouteConfig = {
      name: 'GetPets',
      type: 'api',
      path: '/pets',
      method: 'GET',
      flows: ['PetManagement'],
    }

    export const handler: Handlers['GetPets'] = async (req, { logger }) => {
      // In a real application, this would be a database call
      // e.g., const pets = await db.pets.findMany()
      const pets = TSStore.list()
      
      logger.info('Retrieved all pets', { count: pets.length })
      return { status: 200, body: pets }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/get_pets_step.py"
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "GetPets",
        "type": "api",
        "path": "/pets",
        "method": "GET",
        "emits": []
    }

    async def handler(req, ctx=None):
        # In a real application, this would be a database call
        # e.g., pets = await db.pets.find_all()
        return {"status": 200, "body": pet_store.list_all()}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/get-pets.step.js"
    const { list } = require('./js-store')

    const config = {
      name: 'GetPets',
      type: 'api',
      path: '/pets',
      method: 'GET',
      emits: []
    }

    const handler = async () => {
      // In a real application, this would be a database call
      // e.g., const pets = await db.pets.findAll()
      return { status: 200, body: list() }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

### Testing List All Pets

Test with curl:

```bash
# List all pets
curl http://localhost:3000/pets
```

Or use the Workbench interface:

![create-pet](../../img/build-your-first-app/list-pets.png)

---

### Get Single Pet

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/typescript/get-pet.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/python/get_pet_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/javascript/get-pet.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/get-pet.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { TSStore } from './ts-store'

    export const config: ApiRouteConfig = {
      name: 'GetPet',
      type: 'api',
      path: '/pets/:id',
      method: 'GET',
      flows: ['PetManagement'],
    }

    export const handler: Handlers['GetPet'] = async (req, { logger }) => {
      // In a real application, this would be a database call
      // e.g., const pet = await db.pets.findById(req.pathParams.id)
      const pet = TSStore.get(req.pathParams.id)

      if (!pet) {
        logger.warn('Pet not found', { id: req.pathParams.id })
        return { status: 404, body: { message: 'Pet not found' } }
      }

      return { status: 200, body: pet }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/get_pet_step.py"
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "GetPet",
        "type": "api",
        "path": "/pets/:id",
        "method": "GET",
        "emits": []
    }

    async def handler(req, ctx=None):
        pid = req.get("pathParams", {}).get("id")
        # In a real application, this would be a database call
        # e.g., pet = await db.pets.find_by_id(pid)
        pet = pet_store.get(pid)
        return {"status": 200, "body": pet} if pet else {"status": 404, "body": {"message": "Not found"}}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/get-pet.step.js"
    const { get } = require('./js-store')

    const config = {
      name: 'GetPet',
      type: 'api',
      path: '/pets/:id',
      method: 'GET',
      emits: []
    }

    const handler = async (req) => {
      // In a real application, this would be a database call
      // e.g., const pet = await db.pets.findById(req.pathParams.id)
      const pet = get(req.pathParams.id)
      return pet 
        ? { status: 200, body: pet } 
        : { status: 404, body: { message: 'Not found' } }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

<Callout type="info">
**Testing tip:** When testing GET endpoints with path parameters like `/pets/:id`, switch to the **Params** tab (not Body) to enter the ID value.
</Callout>

The `:id` in the path creates a path parameter accessible via `req.pathParams.id`.

### Testing Get Single Pet

Test with curl:

```bash
# Get specific pet (replace 1 with an actual pet ID)
curl http://localhost:3000/pets/1
```

Or use the Workbench interface:

![create-pet](../../img/build-your-first-app/get-pet-by-id.png)

---

## Adding UPDATE Endpoint

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/typescript/update-pet.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/python/update_pet_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/javascript/update-pet.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/update-pet.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { TSStore } from './ts-store'

    const updatePetSchema = z.object({
      name: z.string().min(1).optional(),
      status: z.enum(['available', 'pending', 'adopted']).optional(),
      ageMonths: z.number().int().min(0).optional(),
    })

    export const config: ApiRouteConfig = {
      name: 'UpdatePet',
      type: 'api',
      path: '/pets/:id',
      method: 'PUT',
      bodySchema: updatePetSchema,
      flows: ['PetManagement'],
    }

    export const handler: Handlers['UpdatePet'] = async (req, { logger }) => {
      const updates = updatePetSchema.parse(req.body)
      
      // In a real application, this would be a database call
      // e.g., const pet = await db.pets.update(req.pathParams.id, updates)
      const pet = TSStore.update(req.pathParams.id, updates)

      if (!pet) {
        return { status: 404, body: { message: 'Pet not found' } }
      }

      logger.info('Pet updated', { petId: pet.id })
      return { status: 200, body: pet }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/update_pet_step.py"
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "UpdatePet",
        "type": "api",
        "path": "/pets/:id",
        "method": "PUT",
        "emits": []
    }

    async def handler(req, ctx=None):
        pid = req.get("pathParams", {}).get("id")
        b = req.get("body") or {}
        patch = {}

        if isinstance(b.get("name"), str):
            patch["name"] = b["name"]
        if b.get("species") in ["dog", "cat", "bird", "other"]:
            patch["species"] = b["species"]
        if isinstance(b.get("ageMonths"), (int, float)):
            patch["ageMonths"] = int(b["ageMonths"])
        if b.get("status") in ["available", "pending", "adopted"]:
            patch["status"] = b["status"]

        # In a real application, this would be a database call
        # e.g., updated = await db.pets.update(pid, patch)
        updated = pet_store.update(pid, patch)
        return {"status": 200, "body": updated} if updated else {"status": 404, "body": {"message": "Not found"}}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/update-pet.step.js"
    const { update } = require('./js-store')

    const config = {
      name: 'UpdatePet',
      type: 'api',
      path: '/pets/:id',
      method: 'PUT',
      emits: []
    }

    const handler = async (req) => {
      const b = req.body || {}
      const patch = {}

      if (typeof b.name === 'string') patch.name = b.name
      if (['dog', 'cat', 'bird', 'other'].includes(b.species)) patch.species = b.species
      if (Number.isFinite(b.ageMonths)) patch.ageMonths = Number(b.ageMonths)
      if (['available', 'pending', 'adopted'].includes(b.status)) patch.status = b.status

      // In a real application, this would be a database call
      // e.g., const updated = await db.pets.update(req.pathParams.id, patch)
      const updated = update(req.pathParams.id, patch)
      return updated 
        ? { status: 200, body: updated } 
        : { status: 404, body: { message: 'Not found' } }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

### Testing Update Pet

Test with curl:

```bash
# Update a pet (replace 1 with an actual pet ID)
curl -X PUT http://localhost:3000/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "adopted"}'
```

Or use the Workbench interface:

![create-pet](../../img/build-your-first-app/update-pet.png)

---

## Adding DELETE Endpoint

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/typescript/delete-pet.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/python/delete_pet_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/api-endpoints/steps/javascript/delete-pet.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/delete-pet.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { TSStore } from './ts-store'

    export const config: ApiRouteConfig = {
      name: 'DeletePet',
      type: 'api',
      path: '/pets/:id',
      method: 'DELETE',
      flows: ['PetManagement'],
    }

    export const handler: Handlers['DeletePet'] = async (req, { logger }) => {
      // In a real application, this would be a database call
      // e.g., const deleted = await db.pets.delete(req.pathParams.id)
      const deleted = TSStore.remove(req.pathParams.id)

      if (!deleted) {
        return { status: 404, body: { message: 'Pet not found' } }
      }

      logger.info('Pet deleted', { petId: req.pathParams.id })
      return { status: 204 }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/delete_pet_step.py"
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "DeletePet",
        "type": "api",
        "path": "/pets/:id",
        "method": "DELETE",
        "emits": []
    }

    async def handler(req, ctx=None):
        pid = req.get("pathParams", {}).get("id")
        # In a real application, this would be a database call
        # e.g., ok = await db.pets.delete(pid)
        ok = pet_store.remove(pid)
        return {"status": 204, "body": {}} if ok else {"status": 404, "body": {"message": "Not found"}}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/delete-pet.step.js"
    const { remove } = require('./js-store')

    const config = {
      name: 'DeletePet',
      type: 'api',
      path: '/pets/:id',
      method: 'DELETE',
      emits: []
    }

    const handler = async (req) => {
      // In a real application, this would be a database call
      // e.g., const ok = await db.pets.delete(req.pathParams.id)
      const ok = remove(req.pathParams.id)
      return ok 
        ? { status: 204, body: {} } 
        : { status: 404, body: { message: 'Not found' } }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

DELETE endpoints return `204 No Content` on success.

### Testing Delete Pet

Test with curl:

```bash
# Delete a pet (replace 1 with an actual pet ID)
curl -X DELETE http://localhost:3000/pets/1
```

Or use the Workbench interface:

![create-pet](../../img/build-your-first-app/delete-pet.png)

---

As you can see in this example, Motia handles routing, validation, and error handling automatically. With just a few lines of code, you've built a complete REST API with:
- **Automatic routing** based on your step configuration
- **Path parameter extraction** (`/pets/:id` → `req.pathParams.id`)
- **HTTP method handling** (GET, POST, PUT, DELETE)
- **Response formatting** with proper status codes
- **Built-in error handling** and validation

🎉 **Congratulations!** You've successfully created your first API endpoints with Motia. Your pet store API is now ready to handle all CRUD operations.

---

## What's Next?

You now have a working REST API for your pet store! But a complete backend system needs more than just API endpoints. In the next guide, we'll add background jobs using Event Steps and scheduled tasks with Cron Steps to handle tasks like:

- **SetNextFeedingReminder** - Queue jobs that automatically schedule feeding reminders when pets are added or updated
- **Deletion Reaper** - Cron jobs that run daily to clean up soft-deleted records and expired data

Let's continue building your complete backend system by adding these background jobs with Event Steps and scheduled tasks with Cron Steps.

<Cards>
  <Card href="/docs/getting-started/build-your-first-motia-app/background-jobs" title="Next: Background Jobs">
    Add Event Steps and Cron Steps to handle async tasks and scheduled jobs
  </Card>
</Cards>


-   [background-jobs](/docs/getting-started/build-your-first-motia-app/background-jobs): Documentation for background-jobs.
---
title: Background Jobs
description: Learn how to create async background jobs and scheduled tasks with Motia
---

## What You'll Build

A pet management system with background jobs that handle:

- **Event Step** - Async job that sets feeding reminders when pets are created
- **Cron Step** - Scheduled job that runs daily to clean up deleted pets

![workbench](../../img/build-your-first-app/background-jobs-workbench.png)
---

## Getting Started

Clone the example repository:

```bash
git clone https://github.com/MotiaDev/build-your-first-app.git
cd build-your-first-app
git checkout background-jobs
```

Install dependencies:

```bash
npm install
```

Start the Workbench:

```bash
npm run dev
```

Your Workbench will be available at `http://localhost:3000`.

---

## Project Structure

<Folder name="my-pet-api" defaultOpen>
  <Folder name="steps" defaultOpen>
    <Folder name="typescript">
      <File name="create-pet.step.ts" />
      <File name="set-next-feeding-reminder.job.step.ts" />
      <File name="deletion-reaper.cron.step.ts" />
      <File name="ts-store.ts" />
    </Folder>
    <Folder name="javascript">
      <File name="create-pet.step.js" />
      <File name="set-next-feeding-reminder.job.step.js" />
      <File name="deletion-reaper.cron.step.js" />
      <File name="js-store.js" />
    </Folder>
    <Folder name="python">
      <File name="create_pet_step.py" />
      <File name="set_next_feeding_reminder.job_step.py" />
      <File name="deletion_reaper.cron_step.py" />
    </Folder>
  </Folder>
  <Folder name="services">
    <File name="pet_store.py" />
    <File name="types.py" />
  </Folder>
  <File name="package.json" />
  <File name="requirements.txt" />
  <File name="types.d.ts" />
</Folder>

<Callout type="info">
Files like `features.json` and `tutorial.tsx` are only for the interactive tutorial and are not part of Motia's project structure.
</Callout>

All code examples in this guide are available in the [build-your-first-app](https://github.com/MotiaDev/build-your-first-app/tree/background-jobs) repository.

You can follow this guide to learn how to build background jobs with Motia step by step, or you can clone the repository and dive into our Interactive Tutorial to learn by doing directly in the Workbench.

![interactive-tutorial](../../img/build-your-first-app/interactive-tutorial-bg.png)

---

## Understanding Background Jobs

Background jobs let you handle time-consuming tasks without blocking your API responses. When a user creates a pet, they get an immediate response while tasks like sending emails or processing data happen in the background.

Motia provides two types of background jobs:

- **Event Steps** - Triggered by events from your API endpoints
- **Cron Steps** - Run on a schedule (like daily cleanup tasks)

---

## Creating Your First Event Step

Let's create a background job that sets feeding reminders when a pet is created. First, we need to emit an event from our API endpoint.

### Step 1: Emit Events from API

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/typescript/create-pet.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/python/create_pet_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/javascript/create-pet.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/create-pet.step.ts"
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { TSStore } from './ts-store'

    const createPetSchema = z.object({
      name: z.string().min(1, 'Name is required'),
      species: z.enum(['dog', 'cat', 'bird', 'other']),
      ageMonths: z.number().int().min(0),
    })

    export const config: ApiRouteConfig = {
      name: 'CreatePet',
      type: 'api',
      path: '/pets',
      method: 'POST',
      bodySchema: createPetSchema,
      // Declare what events this endpoint can emit
      emits: ['ts.feeding.reminder.enqueued'],
      flows: ['PetManagement'],
    }

    export const handler: Handlers['CreatePet'] = async (req, { emit, logger }) => {
      const data = createPetSchema.parse(req.body)
      const pet = TSStore.create(data)

      logger.info('Pet created', { petId: pet.id })

      // Emit event to trigger background job
      await emit({
        topic: 'ts.feeding.reminder.enqueued',
        data: {
          petId: pet.id,
          enqueuedAt: Date.now()
        }
      })

      return { status: 201, body: pet }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/create_pet_step.py"
    import sys
    import os
    import time
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "name": "CreatePet",
        "type": "api",
        "path": "/pets",
        "method": "POST",
        "emits": ["py.feeding.reminder.enqueued"]
    }

    async def handler(req, ctx=None):
        b = req.get("body") or {}
        name = b.get("name")
        species = b.get("species")
        age = b.get("ageMonths")

        if not isinstance(name, str) or not name.strip():
            return {"status": 400, "body": {"message": "Invalid name"}}
        if species not in ["dog", "cat", "bird", "other"]:
            return {"status": 400, "body": {"message": "Invalid species"}}

        try:
            age_val = int(age)
        except Exception:
            return {"status": 400, "body": {"message": "Invalid ageMonths"}}

        pet = pet_store.create(name, species, age_val)
        
        # Emit event to trigger background job
        if ctx and ctx.emit:
            await ctx.emit({
                "topic": "py.feeding.reminder.enqueued",
                "data": {
                    "petId": pet["id"],
                    "enqueuedAt": int(time.time() * 1000)
                }
            })

        return {"status": 201, "body": pet}
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/create-pet.step.js"
    const { create } = require('./js-store')

    const config = {
      name: 'CreatePet',
      type: 'api',
      path: '/pets',
      method: 'POST',
      emits: ['js.feeding.reminder.enqueued']
    }

    const handler = async (req, { emit }) => {
      const b = req.body || {}
      const name = typeof b.name === 'string' && b.name.trim()
      const speciesOk = ['dog', 'cat', 'bird', 'other'].includes(b.species)
      const ageOk = Number.isFinite(b.ageMonths)

      if (!name || !speciesOk || !ageOk) {
        return { status: 400, body: { message: 'Invalid payload' } }
      }

      const pet = create({ name, species: b.species, ageMonths: Number(b.ageMonths) })

      // Emit event to trigger background job
      if (emit) {
        await emit({
          topic: 'js.feeding.reminder.enqueued',
          data: {
            petId: pet.id,
            enqueuedAt: Date.now()
          }
        })
      }

      return { status: 201, body: pet }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

The API endpoint now emits an event after creating a pet. The response returns immediately while the background job processes asynchronously.

---

### Step 2: Create the Event Step

Now let's create the background job that listens for this event and sets feeding reminders.

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/typescript/set-next-feeding-reminder.job.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/python/set_next_feeding_reminder.job_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/javascript/set-next-feeding-reminder.job.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/set-next-feeding-reminder.job.step.ts"
    import { TSStore } from './ts-store'

    export const config = {
      type: 'event',
      name: 'TsSetNextFeedingReminder',
      description: 'Background job that sets next feeding reminder and adds welcome notes',
      // Subscribe to the event emitted by CreatePet
      subscribes: ['ts.feeding.reminder.enqueued'],
      emits: ['ts.feeding.reminder.completed'],
      flows: ['TsPetManagement']
    }

    export const handler = async (input: any, context?: any) => {
      const { emit, logger } = context || {}
      const { petId, enqueuedAt } = input

      if (logger) {
        logger.info('Setting next feeding reminder', { petId, enqueuedAt })
      }

      try {
        // Calculate next feeding time (24 hours from now)
        const nextFeedingAt = Date.now() + (24 * 60 * 60 * 1000)
        
        // Update pet with feeding schedule and welcome notes
        const updates = {
          notes: 'Welcome to our pet store! We\'ll take great care of this pet.',
          nextFeedingAt: nextFeedingAt
        }

        const updatedPet = TSStore.update(petId, updates)
        
        if (!updatedPet) {
          if (logger) {
            logger.error('Failed to set feeding reminder - pet not found', { petId })
          }
          return
        }

        if (logger) {
          logger.info('Next feeding reminder set', { 
            petId, 
            notes: updatedPet.notes?.substring(0, 50) + '...',
            nextFeedingAt: new Date(nextFeedingAt).toISOString()
          })
        }

        if (emit) {
          await emit({
            topic: 'ts.feeding.reminder.completed',
            data: { 
              petId, 
              completedAt: Date.now(),
              processingTimeMs: Date.now() - enqueuedAt
            }
          })
        }

      } catch (error: any) {
        if (logger) {
          logger.error('Feeding reminder job error', { petId, error: error.message })
        }
      }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/set_next_feeding_reminder.job_step.py"
    import sys
    import os
    import time
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "type": "event",
        "name": "PySetNextFeedingReminder",
        "description": "Background job that sets next feeding reminder and adds welcome notes",
        "subscribes": ["py.feeding.reminder.enqueued"],
        "emits": ["py.feeding.reminder.completed"]
    }

    async def handler(input_data, context):
        pet_id = input_data.get("petId")
        enqueued_at = input_data.get("enqueuedAt")

        if context.logger:
            context.logger.info("Setting next feeding reminder", {
                "petId": pet_id,
                "enqueuedAt": enqueued_at
            })

        try:
            # Calculate next feeding time (24 hours from now)
            next_feeding_at = int(time.time() * 1000) + (24 * 60 * 60 * 1000)
            
            # Update pet with feeding schedule and welcome notes
            updates = {
                "notes": "Welcome to our pet store! We'll take great care of this pet.",
                "nextFeedingAt": next_feeding_at
            }

            updated_pet = pet_store.update(pet_id, updates)
            
            if not updated_pet:
                if context.logger:
                    context.logger.error("Failed to set feeding reminder - pet not found", {
                        "petId": pet_id
                    })
                return

            if context.logger:
                context.logger.info("Next feeding reminder set", {
                    "petId": pet_id,
                    "notes": updated_pet.get("notes", "")[:50] + "...",
                    "nextFeedingAt": next_feeding_at
                })

            if context.emit:
                await context.emit({
                    "topic": "py.feeding.reminder.completed",
                    "data": {
                        "petId": pet_id,
                        "completedAt": int(time.time() * 1000),
                        "processingTimeMs": int(time.time() * 1000) - enqueued_at
                    }
                })

        except Exception as error:
            if context.logger:
                context.logger.error("Feeding reminder job error", {
                    "petId": pet_id,
                    "error": str(error)
                })
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/set-next-feeding-reminder.job.step.js"
    const { update } = require('./js-store')

    const config = {
      type: 'event',
      name: 'JsSetNextFeedingReminder',
      description: 'Background job that sets next feeding reminder and adds welcome notes',
      subscribes: ['js.feeding.reminder.enqueued'],
      emits: ['js.feeding.reminder.completed']
    }

    const handler = async (input, { emit, logger }) => {
      const { petId, enqueuedAt } = input

      if (logger) {
        logger.info('Setting next feeding reminder', { petId, enqueuedAt })
      }

      try {
        // Calculate next feeding time (24 hours from now)
        const nextFeedingAt = Date.now() + (24 * 60 * 60 * 1000)
        
        // Update pet with feeding schedule and welcome notes
        const updates = {
          notes: 'Welcome to our pet store! We\'ll take great care of this pet.',
          nextFeedingAt: nextFeedingAt
        }

        const updatedPet = update(petId, updates)
        
        if (!updatedPet) {
          if (logger) {
            logger.error('Failed to set feeding reminder - pet not found', { petId })
          }
          return
        }

        if (logger) {
          logger.info('Next feeding reminder set', { 
            petId, 
            notes: updatedPet.notes?.substring(0, 50) + '...',
            nextFeedingAt: new Date(nextFeedingAt).toISOString()
          })
        }

        if (emit) {
          await emit({
            topic: 'js.feeding.reminder.completed',
            data: { 
              petId, 
              completedAt: Date.now(),
              processingTimeMs: Date.now() - enqueuedAt
            }
          })
        }

      } catch (error) {
        if (logger) {
          logger.error('Feeding reminder job error', { petId, error: error.message })
        }
      }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

### How Event Steps Work

Event Steps have a few key differences from API Steps:

- **type** is set to `'event'` instead of `'api'`
- **subscribes** lists the events this job listens for
- **handler** receives the event data as the first argument

When you create a pet, the API returns immediately. The background job picks up the event and processes it asynchronously.

---

## Testing Your Background Job

Create a pet and watch the background job execute:

```bash
# Create a pet
curl -X POST http://localhost:3000/pets \
  -H "Content-Type: application/json" \
  -d '{"name": "Max", "species": "dog", "ageMonths": 24}'
```

Check the logs in Workbench to see both the API call and the background job execution:

![background-job-logs](../../img/build-your-first-app/bg-job-logs.png)

You'll see:
1. "Pet created" log from the API endpoint
2. "Setting next feeding reminder" log from the background job
3. "Next feeding reminder set" log when the job completes

---

## Creating a Scheduled Cron Job

Now let's create a cron job that runs daily to clean up soft-deleted pets. This demonstrates how to handle scheduled maintenance tasks.

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/typescript/deletion-reaper.cron.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/python/deletion_reaper.cron_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/background-jobs/steps/javascript/deletion-reaper.cron.step.js)
</Callout>

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/deletion-reaper.cron.step.ts"
    import { TSStore } from './ts-store'

    export const config = {
      type: 'cron',
      name: 'TsDeletionReaper',
      description: 'Daily job that permanently removes pets scheduled for deletion',
      cron: '0 2 * * *', // Daily at 2:00 AM
      emits: ['ts.pet.purged', 'ts.reaper.completed'],
      flows: ['TsPetManagement']
    }

    export const handler = async ({ emit, logger }: any) => {
      if (logger) {
        logger.info('Deletion Reaper started - scanning for pets to purge')
      }

      try {
        const petsToReap = TSStore.findDeletedPetsReadyToPurge()
        
        if (petsToReap.length === 0) {
          if (logger) {
            logger.info('Deletion Reaper completed - no pets to purge')
          }
          
          if (emit) {
            await emit({
              topic: 'ts.reaper.completed',
              data: { 
                scannedAt: Date.now(),
                purgedCount: 0,
                message: 'No pets ready for purging'
              }
            })
          }
          return
        }

        let purgedCount = 0
        
        for (const pet of petsToReap) {
          const success = TSStore.remove(pet.id)
          
          if (success) {
            purgedCount++
            
            if (logger) {
              logger.info('Pet permanently purged', { 
                petId: pet.id, 
                name: pet.name,
                deletedAt: new Date(pet.deletedAt!).toISOString(),
                purgeAt: new Date(pet.purgeAt!).toISOString()
              })
            }

            if (emit) {
              await emit({
                topic: 'ts.pet.purged',
                data: { 
                  petId: pet.id, 
                  name: pet.name,
                  species: pet.species,
                  deletedAt: pet.deletedAt,
                  purgedAt: Date.now()
                }
              })
            }
          } else {
            if (logger) {
              logger.warn('Failed to purge pet', { petId: pet.id, name: pet.name })
            }
          }
        }

        if (logger) {
          logger.info('Deletion Reaper completed', { 
            totalScanned: petsToReap.length,
            purgedCount,
            failedCount: petsToReap.length - purgedCount
          })
        }

        if (emit) {
          await emit({
            topic: 'ts.reaper.completed',
            data: { 
              scannedAt: Date.now(),
              purgedCount,
              totalScanned: petsToReap.length
            }
          })
        }

      } catch (error: any) {
        if (logger) {
          logger.error('Deletion Reaper error', { error: error.message })
        }
      }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/deletion_reaper.cron_step.py"
    import sys
    import os
    import time
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from services import pet_store

    config = {
        "type": "cron",
        "name": "PyDeletionReaper",
        "description": "Daily job that permanently removes pets scheduled for deletion",
        "cron": "0 2 * * *",  # Daily at 2:00 AM
        "emits": ["py.pet.purged", "py.reaper.completed"]
    }

    async def handler(context):
        if context.logger:
            context.logger.info("Deletion Reaper started - scanning for pets to purge")

        try:
            pets_to_reap = pet_store.find_deleted_pets_ready_to_purge()
            
            if len(pets_to_reap) == 0:
                if context.logger:
                    context.logger.info("Deletion Reaper completed - no pets to purge")
                
                if context.emit:
                    await context.emit({
                        "topic": "py.reaper.completed",
                        "data": {
                            "scannedAt": int(time.time() * 1000),
                            "purgedCount": 0,
                            "message": "No pets ready for purging"
                        }
                    })
                return

            purged_count = 0
            
            for pet in pets_to_reap:
                success = pet_store.remove(pet["id"])
                
                if success:
                    purged_count += 1
                    
                    if context.logger:
                        context.logger.info("Pet permanently purged", {
                            "petId": pet["id"],
                            "name": pet["name"],
                            "deletedAt": pet.get("deletedAt"),
                            "purgeAt": pet.get("purgeAt")
                        })

                    if context.emit:
                        await context.emit({
                            "topic": "py.pet.purged",
                            "data": {
                                "petId": pet["id"],
                                "name": pet["name"],
                                "species": pet["species"],
                                "deletedAt": pet.get("deletedAt"),
                                "purgedAt": int(time.time() * 1000)
                            }
                        })
                else:
                    if context.logger:
                        context.logger.warn("Failed to purge pet", {
                            "petId": pet["id"],
                            "name": pet["name"]
                        })

            if context.logger:
                context.logger.info("Deletion Reaper completed", {
                    "totalScanned": len(pets_to_reap),
                    "purgedCount": purged_count,
                    "failedCount": len(pets_to_reap) - purged_count
                })

            if context.emit:
                await context.emit({
                    "topic": "py.reaper.completed",
                    "data": {
                        "scannedAt": int(time.time() * 1000),
                        "purgedCount": purged_count,
                        "totalScanned": len(pets_to_reap)
                    }
                })

        except Exception as error:
            if context.logger:
                context.logger.error("Deletion Reaper error", {"error": str(error)})
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/deletion-reaper.cron.step.js"
    const { findDeletedPetsReadyToPurge, remove } = require('./js-store')

    const config = {
      type: 'cron',
      name: 'JsDeletionReaper',
      description: 'Daily job that permanently removes pets scheduled for deletion',
      cron: '0 2 * * *', // Daily at 2:00 AM
      emits: ['js.pet.purged', 'js.reaper.completed']
    }

    const handler = async ({ emit, logger }) => {
      if (logger) {
        logger.info('Deletion Reaper started - scanning for pets to purge')
      }

      try {
        const petsToReap = findDeletedPetsReadyToPurge()
        
        if (petsToReap.length === 0) {
          if (logger) {
            logger.info('Deletion Reaper completed - no pets to purge')
          }
          
          if (emit) {
            await emit({
              topic: 'js.reaper.completed',
              data: { 
                scannedAt: Date.now(),
                purgedCount: 0,
                message: 'No pets ready for purging'
              }
            })
          }
          return
        }

        let purgedCount = 0
        
        for (const pet of petsToReap) {
          const success = remove(pet.id)
          
          if (success) {
            purgedCount++
            
            if (logger) {
              logger.info('Pet permanently purged', { 
                petId: pet.id, 
                name: pet.name,
                deletedAt: new Date(pet.deletedAt).toISOString(),
                purgeAt: new Date(pet.purgeAt).toISOString()
              })
            }

            if (emit) {
              await emit({
                topic: 'js.pet.purged',
                data: { 
                  petId: pet.id, 
                  name: pet.name,
                  species: pet.species,
                  deletedAt: pet.deletedAt,
                  purgedAt: Date.now()
                }
              })
            }
          } else {
            if (logger) {
              logger.warn('Failed to purge pet', { petId: pet.id, name: pet.name })
            }
          }
        }

        if (logger) {
          logger.info('Deletion Reaper completed', { 
            totalScanned: petsToReap.length,
            purgedCount,
            failedCount: petsToReap.length - purgedCount
          })
        }

        if (emit) {
          await emit({
            topic: 'js.reaper.completed',
            data: { 
              scannedAt: Date.now(),
              purgedCount,
              totalScanned: petsToReap.length
            }
          })
        }

      } catch (error) {
        if (logger) {
          logger.error('Deletion Reaper error', { error: error.message })
        }
      }
    }

    module.exports = { config, handler }
    ```
  </Tab>
</Tabs>

### Understanding Cron Steps

Cron Steps run on a schedule defined by a cron expression:

- **type** is set to `'cron'`
- **cron** defines when the job runs (e.g., `'0 2 * * *'` = daily at 2 AM)
- **handler** receives only the context (no input data like Event Steps)

Common cron patterns:
- `'*/5 * * * *'` - Every 5 minutes
- `'0 * * * *'` - Every hour
- `'0 0 * * *'` - Daily at midnight
- `'0 9 * * 1'` - Every Monday at 9 AM

---

## Monitoring Background Jobs

Workbench provides tools to monitor your background jobs:

### Tracing

See the complete execution flow from API call to background job:

![tracing](../../img/build-your-first-app/bg-job-tracing.png)

Each trace shows:
- When the API endpoint was called
- When events were emitted
- When background jobs started and completed
- Total processing time

---

🎉 **Congratulations!** You've successfully created background jobs with Motia. Your pet store now handles async tasks efficiently without blocking API responses.

---
## What's Next?

You now have a complete backend system with API endpoints and background jobs! But there's more power in Motia when you combine everything into workflows.

In the next guide, we'll build complete **workflow orchestrations** that connect multiple Steps together:

- **Queue-Based Job Processing** - SetNextFeedingReminder triggered by pet creation, processing asynchronously without blocking API responses
- **Scheduled Maintenance Tasks** - Deletion Reaper running daily at 2 AM to permanently remove soft-deleted pets past their purge date
- **Pet Lifecycle Orchestration** - Staff-driven workflow managing pet status transitions from creation through quarantine, health checks, and adoption
- **Event-Driven State Management** - Centralized orchestrator ensuring consistent pet status changes with automatic progressions and staff decision points

Let's continue building by creating workflows that orchestrate your APIs and background jobs into powerful, event-driven systems.

<Cards>
  <Card href="/docs/getting-started/build-your-first-motia-app/workflows" title="Next: Workflows">
    Create workflow orchestrations that connect multiple Steps together
  </Card>
</Cards>



-   [index](/docs/getting-started/build-your-first-motia-app): Documentation for index.
---
title: Build Your First Motia App
description: Build your first multi-language Motia app in minutes. This guide walks you through creating, running, and understanding a Motia app using JavaScript, TypeScript, and Python.
---

# Build Your First Motia App

**Get up and running with Motia in just a few minutes!** This guide shows you how to create a Motia app that connects JavaScript, TypeScript, and Python as steps.

## What You'll Build

A simple data processing Motia app:
- **TypeScript** API endpoint receives data with validation
- **TypeScript** bridges and notifies with proper types
- **Python** processes the data with proper logging
- **JavaScript** generates final summary and metrics

All connected automatically with zero configuration and strict type safety.

## Step 1: Create Your Motia App

```bash
# Create a new Motia app
npx motia@latest create
```
![build-app](/docs-images/motia-terminal.gif)

```bash
### Start the development environment
npx motia dev
```
![tldr motia](/docs-images/motia-build-your-app-2.gif)


✅ That's it! You now have a working Motia app with a visual debugger at `http://localhost:3000`

## Step 2: Add Your Logic Steps

### TypeScript API Endpoint (App Starter)
// File: 01-starter.step.ts
```typescript
import { ApiRouteConfig, Handlers } from 'motia'
import { z } from 'zod'

const bodySchema = z.object({
  data: z.record(z.unknown()).optional(),
  message: z.string().optional()
})

// API endpoint to start the multi-language pipeline
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'AppStarter',
  description: 'Start the multi-language app pipeline',

  method: 'POST',
  path: '/start-app',

  bodySchema,
  responseSchema: {
    200: z.object({
      message: z.string(),
      appId: z.number(),
      traceId: z.string()
    })
  },

  emits: ['app.started'],
  flows: ['data-processing']
} as const

export const handler: Handlers['AppStarter'] = async (req, { logger, emit, traceId }) => {
  logger.info('🚀 Starting multi-language app', { body: req.body, traceId })
  
  const appData = {
    id: Date.now(),
    input: req.body.data || {},
    started_at: new Date().toISOString(),
    traceId
  }

  // Emit to next step
  await emit({
    topic: 'app.started',
    data: appData
  })

  logger.info('✅ App started successfully', { 
    appId: appData.id,
    traceId 
  })

  return {
    status: 200,
    body: {
      message: 'Multi-language app started successfully',
      appId: appData.id,
      traceId
    }
  }
}
```

### TypeScript Bridge Step
// File: 02-bridge.step.ts
```typescript
import { EventConfig, Handlers } from 'motia'
import { z } from 'zod'

// Bridge step to connect app starter to Python processing
export const config: EventConfig = {
  type: 'event',
  name: 'AppBridge',
  description: 'Bridge between app start and Python processing',
  subscribes: ['app.started'],
  emits: ['data.processed'],
  input: z.object({
    id: z.number(),
    input: z.record(z.unknown()),
    started_at: z.string(),
    traceId: z.string()
  }),
  flows: ['data-processing']
} as const

export const handler: Handlers['AppBridge'] = async (input, { logger, emit }) => {
  logger.info('🌉 Processing app data and sending to Python', { appId: input.id })
  
  // Process data for Python step
  const processedResult = {
    original_id: input.id,
    processed_at: input.started_at,
    result: `Processed: ${JSON.stringify(input.input)}`,
    confidence: 0.95,
    model_version: '1.0'
  }

  // Send to Python processing
  await emit({
    topic: 'data.processed', 
    data: processedResult
  })

  logger.info('✅ Data sent to Python processing', { 
    originalId: input.id
  })
}
```

### Python Data Processor
// File: simple-python_step.py
```python
import time
from datetime import datetime

# Python processing step configuration
config = {
    "type": "event",
    "name": "ProcessDataPython",
    "description": "Process data using Python capabilities",
    "subscribes": ["data.processed"],
    "emits": ["python.done"],
    "flows": ["data-processing"]
}

async def handler(input_data, ctx):
    """
    Python step that processes data and demonstrates Python capabilities
    """
    logger = ctx.logger
    emit = ctx.emit
    
    # Extract data from input
    original_id = input_data.get("original_id")
    result = input_data.get("result", "")
    
    logger.info(f"🐍 Python processing data for ID: {original_id}")
    
    start_time = time.time()
    
    # Simulate Python data processing
    processed_message = f"Python processed: {result}"
    
    # Add some Python-specific processing
    data_analysis = {
        "word_count": len(result.split()) if isinstance(result, str) else 0,
        "character_count": len(result) if isinstance(result, str) else 0,
        "processed_timestamp": datetime.now().isoformat(),
        "processing_language": "Python 3.x"
    }
    
    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Create result object
    python_result = {
        "id": original_id,
        "python_message": processed_message,
        "processed_by": ["appStarter", "appBridge", "ProcessDataPython"],
        "processing_time": processing_time,
        "analysis": data_analysis
    }
    
    # Emit to next step
    await emit({
        "topic": "python.done",
        "data": python_result
    })
    
    logger.info(f"✅ Python processing completed in {processing_time:.2f}ms")
```

### TypeScript Notification Step
// File: notify.step.ts
```typescript
import { EventConfig, Handlers } from 'motia'
import { z } from 'zod'

export const config: EventConfig = {
  type: 'event',
  name: 'NotificationHandler',
  description: 'Send notifications after Python processing',
  subscribes: ['python.done'],
  emits: ['notification.sent'],
  input: z.object({
    id: z.number(),
    python_message: z.string(),
    processed_by: z.array(z.string()),
    processing_time: z.number(),
    analysis: z.record(z.unknown()).optional()
  }),
  flows: ['data-processing']
} as const

export const handler: Handlers['NotificationHandler'] = async (input, { logger, emit }) => {
  logger.info('📧 Sending notifications after Python processing', { id: input.id })
  
  // Simulate sending notifications (email, slack, etc.)
  const notification = {
    id: input.id,
    message: `Notification: ${input.python_message}`,
    processed_by: input.processed_by,
    sent_at: new Date().toISOString()
  }

  // Send notification data to final step
  await emit({
    topic: 'notification.sent',
    data: {
      ...notification,
      processing_time: input.processing_time
    }
  })

  logger.info('✅ Notifications sent successfully', { id: input.id })
}
```

### TypeScript Finalizer Step
// File: 04-final.step.ts
```typescript
import { EventConfig, Handlers } from 'motia'
import { z } from 'zod'

// Final step to complete the app - TypeScript
export const config: EventConfig = {
  type: 'event',
  name: 'AppFinalizer',
  description: 'Complete the basic app and log final results',
  subscribes: ['notification.sent'],
  emits: ['app.completed'],
  input: z.object({
    id: z.number(),
    message: z.string(),
    processed_by: z.array(z.string()),
    sent_at: z.string(),
    processing_time: z.number()
  }),
  flows: ['data-processing']
} as const

export const handler: Handlers['AppFinalizer'] = async (input, { logger, emit }) => {
  logger.info('🏁 Finalizing app', { 
    notificationId: input.id,
    message: input.message 
  })
  
  // Create final app summary
  const summary = {
    appId: input.id,
    status: 'completed',
    completed_at: new Date().toISOString(),
    steps_executed: [
      'app-starter',
      'app-bridge', 
      'python-processor',
      'notification-handler',
      'app-finalizer'
    ],
    result: input.message
  }

  // Send to JavaScript summary generator
  await emit({
    topic: 'app.completed',
    data: {
      ...summary,
      total_processing_time: input.processing_time
    }
  })

  logger.info('✅ App finalized successfully', { 
    appId: input.id,
    totalSteps: summary.steps_executed.length
  })
}
```

### JavaScript Summary Generator
// File: 05-summary.step.js
```javascript
// Final summary step - JavaScript
export const config = {
  type: 'event',
  name: 'summaryGenerator',
  description: 'Generate final summary in JavaScript',
  subscribes: ['app.completed'],
  emits: [], // Final step - no further processing needed
  flows: ['data-processing']
}

export const handler = async (input, { logger }) => {
  logger.info('📊 Generating final summary in JavaScript', { 
    appId: input.appId,
    status: input.status 
  })
  
  // Calculate processing metrics
  const processingTime = input.total_processing_time || 0
  const stepsCount = input.steps_executed ? input.steps_executed.length : 0
  
  // Create comprehensive summary
  const summary = {
    appId: input.appId,
    finalStatus: input.status,
    totalSteps: stepsCount,
    processingTimeMs: processingTime,
    languages: ['TypeScript', 'Python', 'JavaScript'],
    summary: `Multi-language app completed successfully with ${stepsCount} steps`,
    result: input.result,
    completedAt: new Date().toISOString(),
    generatedBy: 'javascript-summary-step'
  }
  
  // Log final summary (final step - no emit needed)
  logger.info('✨ Final summary generated successfully', summary)
  
  return summary
}
```

## Type Definitions

Our unified system uses shared TypeScript types to ensure type safety across the multi-language pipeline:

```typescript
// types/index.ts
export interface AppData {
  id: number
  input: Record<string, unknown>
  started_at: string
  traceId: string
}

export interface ProcessedResult {
  original_id: number
  processed_at: string
  result: string
  confidence: number
  model_version: string
}

export interface PythonResult {
  id: number
  python_message: string
  processed_by: string[]
  processing_time: number
}

export interface NotificationData {
  id: number
  message: string
  processed_by: string[]
  sent_at: string
}

export interface AppSummary {
  appId: number
  status: string
  completed_at: string
  steps_executed: string[]
  result: string
}
```

## What Happens Next?

![motia-build-your-app](/docs-images/motia-build-your-app-2.gif)

Watch in the **Workbench** (`http://localhost:3000`) as your data flows through:

1. **TypeScript** API receives and validates the request with Zod schemas
2. **TypeScript** bridge processes and forwards data with proper typing
3. **Python** processes data with rich analysis (access to numpy, pandas, torch, etc.)
4. **TypeScript** handles notifications after Python processing
5. **TypeScript** finalizes and aggregates results
6. **JavaScript** generates final summary with comprehensive metrics

All languages working together in one unified system with:
- ✅ **Automatic observability** - see every step in real-time
- ✅ **Built-in error handling** - retry logic included
- ✅ **Shared state** - pass data between languages effortlessly
- ✅ **Hot reload** - edit any file and see changes instantly
- ✅ **Type safety** - proper TypeScript types throughout
- ✅ **Input validation** - Zod schema validation for APIs
- ✅ **Multi-language** - JavaScript, TypeScript, and Python working together

## Deploy and Extend

**You just built a production-ready multi-language Motia app!**

Extend your app:
- Add scheduled jobs with `cron` steps
- Create UI components with React/Vue steps
- Connect to databases, APIs, and external services
- Scale to handle millions of requests

Ready to deploy? Check out [Motia Cloud deployment](/docs/concepts/deployment-guide/motia-cloud) for one-click production deployments.

<Callout>
**Ready to build more?** Check out our [Getting Started Guide](/docs/getting-started/quick-start) for more details.
</Callout>

---

**The bottom line:** Motia eliminates the complexity of managing separate runtimes. Write each piece in the best language for the job, and Motia handles the rest.



-   [workflows](/docs/getting-started/build-your-first-motia-app/workflows): Documentation for workflows.
---
title: Workflows
description: Learn how to build automated workflows that manage complex business logic with Motia
---

## What You'll Build

A pet lifecycle management system that automatically guides pets through their journey at your shelter:

- **Automated Status Transitions** - Pets move through stages automatically when conditions are met
- **Staff Decision Points** - Critical checkpoints where staff make the calls
- **Smart Progressions** - Some transitions trigger follow-up actions automatically
- **Validation Rules** - Prevents invalid status changes to keep data consistent

![workbench](../../img/build-your-first-app/workflow-workbench.png)
---

## Getting Started

Clone the example repository:

```bash
git clone https://github.com/MotiaDev/build-your-first-app.git
cd build-your-first-app
git checkout workflow-orchestration
```

Install dependencies:

```bash
npm install
```

Start the Workbench:

```bash
npm run dev
```

Your Workbench will be available at `http://localhost:3000`.

---

## Project Structure

<Folder name="my-pet-api" defaultOpen>
  <Folder name="steps" defaultOpen>
    <Folder name="typescript">
      <File name="create-pet.step.ts" />
      <File name="set-next-feeding-reminder.job.step.ts" />
      <File name="pet-lifecycle-orchestrator.step.ts" />
      <File name="ts-store.ts" />
    </Folder>
    <Folder name="javascript">
      <File name="create-pet.step.js" />
      <File name="set-next-feeding-reminder.job.step.js" />
      <File name="pet-lifecycle-orchestrator.step.js" />
      <File name="js-store.js" />
    </Folder>
    <Folder name="python">
      <File name="create_pet_step.py" />
      <File name="set_next_feeding_reminder.job_step.py" />
      <File name="pet_lifecycle_orchestrator_step.py" />
    </Folder>
  </Folder>
  <Folder name="services">
    <File name="pet_store.py" />
    <File name="types.py" />
  </Folder>
  <File name="package.json" />
  <File name="requirements.txt" />
  <File name="types.d.ts" />
</Folder>

<Callout type="info">
Files like `features.json` and `tutorial.tsx` are only for the interactive tutorial and are not part of Motia's project structure.
</Callout>

All code examples in this guide are available in the [build-your-first-app](https://github.com/MotiaDev/build-your-first-app/tree/workflow-orchestration) repository.

You can follow this guide to learn how to build workflow orchestration with Motia step by step, or you can clone the repository and dive into our Interactive Tutorial to learn by doing directly in the Workbench.

![interactive-tutorial](../../img/build-your-first-app/interactive-tutorial-workflow.png)

---

## Understanding Workflows

So far, you've built API endpoints that respond to requests and background jobs that handle async tasks. But what about coordinating complex business processes that involve multiple steps and decision points?

That's where workflows come in. It's the conductor of your system - making sure things happen in the right order, at the right time, and only when it makes sense.

In our pet shelter example, a pet goes through many stages:
- New arrivals need health checks
- Healthy pets become available for adoption
- Sick pets need treatment before they're ready
- Adoption applications require staff approval

A workflow manages all these transitions, enforcing the rules and keeping everything consistent.

---

## The Pet Lifecycle Journey

When you create a pet, it starts as `new`. Once the feeding reminder job completes, it automatically moves to `in_quarantine`. Staff then checks on it and marks it `healthy`, which automatically progresses to `available`. When someone wants to adopt, it goes `pending`, then finally `adopted`.

The key here is some transitions happen automatically (like `healthy` → `available`), while others need staff approval (like `in_quarantine` → `healthy`).

**What about sick pets?**

If staff finds a pet is `ill`, it automatically moves to `under_treatment`. When staff marks it `recovered`, it chains through automatic transitions: `recovered` → `healthy` → `available`.

This mix of automatic progressions and human decision points is what makes workflows powerful - the system handles the routine stuff while keeping people in control of important calls.

---

## Creating the Workflow

<Callout type="info">
View on GitHub:
- [TypeScript](https://github.com/MotiaDev/build-your-first-app/blob/workflow-orchestration/steps/typescript/pet-lifecycle-orchestrator.step.ts)
- [Python](https://github.com/MotiaDev/build-your-first-app/blob/workflow-orchestration/steps/python/pet_lifecycle_orchestrator_step.py)
- [JavaScript](https://github.com/MotiaDev/build-your-first-app/blob/workflow-orchestration/steps/javascript/pet-lifecycle-orchestrator.step.js)
</Callout>

### Step 1: Define Your Transition Rules

First, map out all the valid transitions in your system. Each rule specifies:
- Which statuses can transition
- Where they transition to
- What event triggers the transition
- A description for logging

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript title="steps/typescript/pet-lifecycle-orchestrator.step.ts"
    type TransitionRule = {
      from: string[];
      to: string;
      event: string;
      description: string;
    };

    const TRANSITION_RULES: TransitionRule[] = [
      {
        from: ["new"],
        to: "in_quarantine",
        event: "feeding.reminder.completed",
        description: "Pet moved to quarantine after feeding setup"
      },
      {
        from: ["in_quarantine"],
        to: "healthy",
        event: "status.update.requested",
        description: "Staff health check - pet cleared from quarantine"
      },
      {
        from: ["healthy"],
        to: "available",
        event: "status.update.requested",
        description: "Staff decision - pet ready for adoption"
      },
      {
        from: ["healthy", "in_quarantine", "available"],
        to: "ill",
        event: "status.update.requested",
        description: "Staff assessment - pet identified as ill"
      },
      {
        from: ["ill"],
        to: "under_treatment",
        event: "status.update.requested",
        description: "Staff decision - treatment started"
      },
      {
        from: ["under_treatment"],
        to: "recovered",
        event: "status.update.requested",
        description: "Staff assessment - treatment completed"
      },
      {
        from: ["recovered"],
        to: "healthy",
        event: "status.update.requested",
        description: "Staff clearance - pet fully recovered"
      },
      {
        from: ["available"],
        to: "pending",
        event: "status.update.requested",
        description: "Adoption application received"
      },
      {
        from: ["pending"],
        to: "adopted",
        event: "status.update.requested",
        description: "Adoption completed"
      },
      {
        from: ["pending"],
        to: "available",
        event: "status.update.requested",
        description: "Adoption application rejected/cancelled"
      }
    ];
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/pet_lifecycle_orchestrator_step.py"
    TRANSITION_RULES = [
        {
            "from": ["new"],
            "to": "in_quarantine",
            "event": "feeding.reminder.completed",
            "description": "Pet moved to quarantine after feeding setup"
        },
        {
            "from": ["in_quarantine"],
            "to": "healthy",
            "event": "status.update.requested",
            "description": "Staff health check - pet cleared from quarantine"
        },
        {
            "from": ["healthy"],
            "to": "available",
            "event": "status.update.requested",
            "description": "Staff decision - pet ready for adoption"
        },
        {
            "from": ["healthy", "in_quarantine", "available"],
            "to": "ill",
            "event": "status.update.requested",
            "description": "Staff assessment - pet identified as ill"
        },
        {
            "from": ["ill"],
            "to": "under_treatment",
            "event": "status.update.requested",
            "description": "Staff decision - treatment started"
        },
        {
            "from": ["under_treatment"],
            "to": "recovered",
            "event": "status.update.requested",
            "description": "Staff assessment - treatment completed"
        },
        {
            "from": ["recovered"],
            "to": "healthy",
            "event": "status.update.requested",
            "description": "Staff clearance - pet fully recovered"
        },
        {
            "from": ["available"],
            "to": "pending",
            "event": "status.update.requested",
            "description": "Adoption application received"
        },
        {
            "from": ["pending"],
            "to": "adopted",
            "event": "status.update.requested",
            "description": "Adoption completed"
        },
        {
            "from": ["pending"],
            "to": "available",
            "event": "status.update.requested",
            "description": "Adoption application rejected/cancelled"
        }
    ]
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript title="steps/javascript/pet-lifecycle-orchestrator.step.js"
    const TRANSITION_RULES = [
      {
        from: ["new"],
        to: "in_quarantine",
        event: "feeding.reminder.completed",
        description: "Pet moved to quarantine after feeding setup"
      },
      {
        from: ["in_quarantine"],
        to: "healthy",
        event: "status.update.requested",
        description: "Staff health check - pet cleared from quarantine"
      },
      {
        from: ["healthy"],
        to: "available",
        event: "status.update.requested",
        description: "Staff decision - pet ready for adoption"
      },
      {
        from: ["healthy", "in_quarantine", "available"],
        to: "ill",
        event: "status.update.requested",
        description: "Staff assessment - pet identified as ill"
      },
      {
        from: ["ill"],
        to: "under_treatment",
        event: "status.update.requested",
        description: "Staff decision - treatment started"
      },
      {
        from: ["under_treatment"],
        to: "recovered",
        event: "status.update.requested",
        description: "Staff assessment - treatment completed"
      },
      {
        from: ["recovered"],
        to: "healthy",
        event: "status.update.requested",
        description: "Staff clearance - pet fully recovered"
      },
      {
        from: ["available"],
        to: "pending",
        event: "status.update.requested",
        description: "Adoption application received"
      },
      {
        from: ["pending"],
        to: "adopted",
        event: "status.update.requested",
        description: "Adoption completed"
      },
      {
        from: ["pending"],
        to: "available",
        event: "status.update.requested",
        description: "Adoption application rejected/cancelled"
      }
    ];
    ```
  </Tab>
</Tabs>

### Step 2: Configure the Event Step

The orchestrator is an Event Step that listens for lifecycle events:

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    export const config = {
      type: 'event',
      name: 'TsPetLifecycleOrchestrator',
      description: 'Pet lifecycle state management with staff interaction points',
      subscribes: [
        'ts.pet.created',
        'ts.feeding.reminder.completed',
        'ts.pet.status.update.requested'
      ],
      emits: [],
      flows: ['TsPetManagement']
    };
    ```
  </Tab>
  <Tab value="Python">
    ```python
    config = {
        "type": "event",
        "name": "PyPetLifecycleOrchestrator",
        "description": "Pet lifecycle state management with staff interaction points",
        "subscribes": [
            "py.pet.created",
            "py.feeding.reminder.completed",
            "py.pet.status.update.requested"
        ],
        "emits": [],
        "flows": ["PyPetManagement"]
    }
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    const config = {
      type: 'event',
      name: 'JsPetLifecycleOrchestrator',
      description: 'Pet lifecycle state management with staff interaction points',
      subscribes: [
        'js.pet.created',
        'js.feeding.reminder.completed',
        'js.pet.status.update.requested'
      ],
      emits: [],
      flows: ['JsPetManagement']
    };
    ```
  </Tab>
</Tabs>

### Step 3: Implement the Orchestration Logic

Now for the handler that processes transitions:

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    export const handler = async (input: any, context?: any) => {
      const { emit, logger } = context || {};
      const { petId, event: eventType, requestedStatus, automatic } = input;

      if (logger) {
        const logMessage = automatic 
          ? '🤖 Automatic progression' 
          : '🔄 Lifecycle orchestrator processing';
        logger.info(logMessage, { petId, eventType, requestedStatus, automatic });
      }

      try {
        // Get the pet from the store
        const pet = TSStore.get(petId);
        if (!pet) {
          if (logger) {
            logger.error('❌ Pet not found for lifecycle transition', { petId, eventType });
          }
          return;
        }

        // Find the right transition rule
        let rule;
        if (eventType === 'status.update.requested' && requestedStatus) {
          rule = TRANSITION_RULES.find(r => 
            r.event === eventType && 
            r.from.includes(pet.status) && 
            r.to === requestedStatus
          );
        } else {
          rule = TRANSITION_RULES.find(r => 
            r.event === eventType && r.from.includes(pet.status)
          );
        }

        // Reject if no valid rule found
        if (!rule) {
          const reason = eventType === 'status.update.requested' 
            ? `Invalid transition: cannot change from ${pet.status} to ${requestedStatus}`
            : `No transition rule found for ${eventType} from ${pet.status}`;
            
          if (logger) {
            logger.warn('⚠️ Transition rejected', { 
              petId, 
              currentStatus: pet.status, 
              requestedStatus,
              eventType,
              reason
            });
          }
          return;
        }

        // Check for idempotency (already in target status)
        if (pet.status === rule.to) {
          if (logger) {
            logger.info('✅ Already in target status', { 
              petId, 
              status: pet.status,
              eventType
            });
          }
          return;
        }

        // Apply the transition
        const oldStatus = pet.status;
        const updatedPet = TSStore.updateStatus(petId, rule.to);
        
        if (!updatedPet) {
          if (logger) {
            logger.error('❌ Failed to update pet status', { 
              petId, 
              oldStatus, 
              newStatus: rule.to 
            });
          }
          return;
        }

        if (logger) {
          logger.info('✅ Lifecycle transition completed', {
            petId,
            oldStatus,
            newStatus: rule.to,
            eventType,
            description: rule.description,
            timestamp: Date.now()
          });
        }

        // Check for automatic progressions
        await processAutomaticProgression(petId, rule.to, emit, logger);

      } catch (error: any) {
        if (logger) {
          logger.error('❌ Lifecycle orchestrator error', { 
            petId, 
            eventType, 
            error: error.message 
          });
        }
      }
    };
    ```
  </Tab>
  <Tab value="Python">
    ```python
    async def handler(input_data, ctx=None):
        logger = getattr(ctx, 'logger', None) if ctx else None
        emit = getattr(ctx, 'emit', None) if ctx else None
        
        try:
            import sys
            import os
            import time
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from services import pet_store
        except ImportError:
            if logger:
                logger.error('❌ Lifecycle orchestrator failed - import error')
            return

        pet_id = input_data.get('petId')
        event_type = input_data.get('event')
        requested_status = input_data.get('requestedStatus')
        automatic = input_data.get('automatic', False)

        if logger:
            log_message = '🤖 Automatic progression' if automatic else '🔄 Lifecycle orchestrator processing'
            logger.info(log_message, {'petId': pet_id, 'eventType': event_type, 'requestedStatus': requested_status, 'automatic': automatic})

        try:
            # Get the pet from the store
            pet = pet_store.get(pet_id)
            if not pet:
                if logger:
                    logger.error('❌ Pet not found for lifecycle transition', {'petId': pet_id, 'eventType': event_type})
                return

            # Find the right transition rule
            rule = None
            if event_type == 'status.update.requested' and requested_status:
                for r in TRANSITION_RULES:
                    if (r['event'] == event_type and 
                        pet['status'] in r['from'] and 
                        r['to'] == requested_status):
                        rule = r
                        break
            else:
                for r in TRANSITION_RULES:
                    if r['event'] == event_type and pet['status'] in r['from']:
                        rule = r
                        break

            # Reject if no valid rule found
            if not rule:
                reason = (f"Invalid transition: cannot change from {pet['status']} to {requested_status}" 
                         if event_type == 'status.update.requested' 
                         else f"No transition rule found for {event_type} from {pet['status']}")
                
                if logger:
                    logger.warn('⚠️ Transition rejected', {
                        'petId': pet_id,
                        'currentStatus': pet['status'],
                        'requestedStatus': requested_status,
                        'eventType': event_type,
                        'reason': reason
                    })
                
                if emit:
                    await emit({
                        'topic': 'py.lifecycle.transition.rejected',
                        'data': {
                            'petId': pet_id,
                            'currentStatus': pet['status'],
                            'requestedStatus': requested_status,
                            'eventType': event_type,
                            'reason': reason,
                            'timestamp': int(time.time() * 1000)
                        }
                    })
                return

            # Check for idempotency
            if pet['status'] == rule['to']:
                if logger:
                    logger.info('✅ Already in target status', {
                        'petId': pet_id,
                        'status': pet['status'],
                        'eventType': event_type
                    })
                return

            # Apply the transition
            old_status = pet['status']
            updated_pet = pet_store.update_status(pet_id, rule['to'])
            
            if not updated_pet:
                if logger:
                    logger.error('❌ Failed to update pet status', {'petId': pet_id, 'oldStatus': old_status, 'newStatus': rule['to']})
                return

            if logger:
                logger.info('✅ Lifecycle transition completed', {
                    'petId': pet_id,
                    'oldStatus': old_status,
                    'newStatus': rule['to'],
                    'eventType': event_type,
                    'description': rule['description'],
                    'timestamp': int(time.time() * 1000)
                })

            if emit:
                await emit({
                    'topic': 'py.lifecycle.transition.completed',
                    'data': {
                        'petId': pet_id,
                        'oldStatus': old_status,
                        'newStatus': rule['to'],
                        'eventType': event_type,
                        'description': rule['description'],
                        'timestamp': int(time.time() * 1000)
                    }
                })

                # Check for automatic progressions after successful transition
                await check_automatic_progressions(pet_id, rule['to'], emit, logger)

        except Exception as error:
            if logger:
                logger.error('❌ Lifecycle orchestrator error', {'petId': pet_id, 'eventType': event_type, 'error': str(error)})
    ```
  </Tab>
  <Tab value="JavaScript">
    ```javascript
    exports.handler = async (input, context) => {
      const { emit, logger } = context || {};
      const { petId, event: eventType, requestedStatus, automatic } = input;

      if (logger) {
        const logMessage = automatic ? '🤖 Automatic progression' : '🔄 Lifecycle orchestrator processing';
        logger.info(logMessage, { petId, eventType, requestedStatus, automatic });
      }

      try {
        const pet = get(petId);
        if (!pet) {
          if (logger) {
            logger.error('❌ Pet not found for lifecycle transition', { petId, eventType });
          }
          return;
        }

        // For status update requests, find the rule based on requested status
        let rule;
        if (eventType === 'status.update.requested' && requestedStatus) {
          rule = TRANSITION_RULES.find(r => 
            r.event === eventType && 
            r.from.includes(pet.status) && 
            r.to === requestedStatus
          );
        } else {
          // For other events (like feeding.reminder.completed)
          rule = TRANSITION_RULES.find(r => 
            r.event === eventType && r.from.includes(pet.status)
          );
        }

        if (!rule) {
          const reason = eventType === 'status.update.requested' 
            ? `Invalid transition: cannot change from ${pet.status} to ${requestedStatus}`
            : `No transition rule found for ${eventType} from ${pet.status}`;
            
          if (logger) {
            logger.warn('⚠️ Transition rejected', { 
              petId, 
              currentStatus: pet.status, 
              requestedStatus,
              eventType,
              reason
            });
          }
          
          if (emit) {
            await emit({
              topic: 'js.lifecycle.transition.rejected',
              data: {
                petId,
                currentStatus: pet.status,
                requestedStatus,
                eventType,
                reason,
                timestamp: Date.now()
              }
            });
          }
          return;
        }

        // Check for idempotency
        if (pet.status === rule.to) {
          if (logger) {
            logger.info('✅ Already in target status', { 
              petId, 
              status: pet.status,
              eventType
            });
          }
          return;
        }

        // Apply the transition
        const oldStatus = pet.status;
        const updatedPet = updateStatus(petId, rule.to);
        
        if (!updatedPet) {
          if (logger) {
            logger.error('❌ Failed to update pet status', { petId, oldStatus, newStatus: rule.to });
          }
          return;
        }

        if (logger) {
          logger.info('✅ Lifecycle transition completed', {
            petId,
            oldStatus,
            newStatus: rule.to,
            eventType,
            description: rule.description,
            timestamp: Date.now()
          });
        }

        if (emit) {
          await emit({
            topic: 'js.lifecycle.transition.completed',
            data: {
              petId,
              oldStatus,
              newStatus: rule.to,
              eventType,
              description: rule.description,
              timestamp: Date.now()
            }
          });

          // Check for automatic progressions after successful transition
          await processAutomaticProgression(petId, rule.to, emit, logger);
        }

      } catch (error) {
        if (logger) {
          logger.error('❌ Lifecycle orchestrator error', { petId, eventType, error: error.message });
        }
      }
    };
    ```
  </Tab>
</Tabs>

### Step 4: Add Automatic Progressions

Some transitions should trigger follow-up actions automatically:

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
  <Tab value="TypeScript">
    ```typescript
    async function processAutomaticProgression(
      petId: string, 
      currentStatus: string, 
      emit: any, 
      logger: any
    ) {
      // Define which statuses automatically progress
      const automaticProgressions: Record<string, { to: string, description: string }> = {
        'healthy': { 
          to: 'available', 
          description: 'Automatic progression - pet ready for adoption' 
        },
        'ill': { 
          to: 'under_treatment', 
          description: 'Automatic progression - treatment started' 
        },
        'recovered': { 
          to: 'healthy', 
          description: 'Automatic progression - recovery complete' 
        }
      };

      const progression = automaticProgressions[currentStatus];
      if (progression) {
        if (logger) {
          logger.info('🤖 Processing automatic progression', { 
            petId, 
            currentStatus, 
            nextStatus: progression.to 
          });
        }

        // Find the transition rule
        const rule = TRANSITION_RULES.find(r => 
          r.event === 'status.update.requested' && 
          r.from.includes(currentStatus) && 
          r.to === progression.to
        );

        if (rule) {
          // Apply the automatic transition
          const oldStatus = currentStatus;
          const updatedPet = TSStore.updateStatus(petId, rule.to);
          
          if (updatedPet) {
            if (logger) {
              logger.info('✅ Automatic progression completed', {
                petId,
                oldStatus,
                newStatus: rule.to,
                description: progression.description,
                timestamp: Date.now()
              });
            }

            // Check for further automatic progressions (chaining)
            await processAutomaticProgression(petId, rule.to, emit, logger);
          } else if (logger) {
            logger.error('❌ Failed to apply automatic progression', { 
              petId, 
              oldStatus, 
              newStatus: rule.to 
            });
          }
        } else if (logger) {
          logger.warn('⚠️ No transition rule found for automatic progression', { 
            petId, 
            currentStatus, 
            targetStatus: progression.to 
          });
        }
      }
    }
    ```
  </Tab>
  <Tab value="Python">
    ```python title="steps/python/pet_lifecycle_orchestrator_step.py"
    async def check_automatic_progressions(pet_id, current_status, emit, logger):
        # Define automatic progressions
        automatic_progressions = {
            'healthy': {'to': 'available', 'description': 'Automatic progression - pet ready for adoption'},
            'ill': {'to': 'under_treatment', 'description': 'Automatic progression - treatment started'},
            'recovered': {'to': 'healthy', 'description': 'Automatic progression - recovery complete'}
        }

        progression = automatic_progressions.get(current_status)
        if progression:
            if logger:
                logger.info('🤖 Orchestrator triggering automatic progression', {
                    'petId': pet_id,
                    'currentStatus': current_status,
                    'nextStatus': progression['to']
                })

            # Emit automatic progression event with delay
            import asyncio
            async def delayed_emit():
                await asyncio.sleep(1.5)  # Slightly longer delay to ensure current transition completes
                # Get fresh pet status to ensure we have the latest state
                try:
                    import sys
                    import os
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                    from services import pet_store
                    fresh_pet = pet_store.get(pet_id)
                    if fresh_pet and fresh_pet['status'] == current_status:
                        await emit({
                            'topic': 'py.pet.status.update.requested',
                            'data': {
                                'petId': pet_id,
                                'event': 'status.update.requested',
                                'requestedStatus': progression['to'],
                                'currentStatus': fresh_pet['status'],
                                'automatic': True
                            }
                        })
                    elif logger:
                        logger.warn('⚠️ Automatic progression skipped - pet status changed', {
                            'petId': pet_id,
                            'expectedStatus': current_status,
                            'actualStatus': fresh_pet['status'] if fresh_pet else None
                        })
                except Exception as e:
                    if logger:
                        logger.error('❌ Automatic progression error', {'petId': pet_id, 'error': str(e)})
            
            asyncio.create_task(delayed_emit())
    ```
  </Tab>  <Tab value="JavaScript">
    ```javascript title="steps/javascript/pet-lifecycle-orchestrator.step.js"
    async function processAutomaticProgression(petId, currentStatus, emit, logger) {
      // Define automatic progressions
      const automaticProgressions = {
        'healthy': { to: 'available', description: 'Automatic progression - pet ready for adoption' },
        'ill': { to: 'under_treatment', description: 'Automatic progression - treatment started' },
        'recovered': { to: 'healthy', description: 'Automatic progression - recovery complete' }
      };

      const progression = automaticProgressions[currentStatus];
      if (progression) {
        if (logger) {
          logger.info('🤖 Processing automatic progression', { 
            petId, 
            currentStatus, 
            nextStatus: progression.to 
          });
        }

        // Find the transition rule for automatic progression
        const rule = TRANSITION_RULES.find(r => 
          r.event === 'status.update.requested' && 
          r.from.includes(currentStatus) && 
          r.to === progression.to
        );

        if (rule) {
          // Apply the automatic transition immediately
          const oldStatus = currentStatus;
          const updatedPet = updateStatus(petId, rule.to);
          
          if (updatedPet) {
            if (logger) {
              logger.info('✅ Automatic progression completed', {
                petId,
                oldStatus,
                newStatus: rule.to,
                description: progression.description,
                timestamp: Date.now()
              });
            }

            if (emit) {
              await emit({
                topic: 'js.lifecycle.transition.completed',
                data: {
                  petId,
                  oldStatus,
                  newStatus: rule.to,
                  eventType: 'status.update.requested',
                  description: progression.description,
                  automatic: true,
                  timestamp: Date.now()
                }
              });

              // Check for further automatic progressions (for chaining like recovered → healthy → available)
              await processAutomaticProgression(petId, rule.to, emit, logger);
            }
          } else if (logger) {
            logger.error('❌ Failed to apply automatic progression', { petId, oldStatus, newStatus: rule.to });
          }
        } else if (logger) {
          logger.warn('⚠️ No transition rule found for automatic progression', { 
            petId, 
            currentStatus, 
            targetStatus: progression.to 
          });
        }
      }
    }
    ```
  </Tab>
</Tabs>

---

## Testing Your Orchestrator

The best way to test your orchestrator is through **Workbench**. It lets you send requests, watch the workflow execute in real-time, and see all the logs in one place.

### Create a Pet

Open Workbench and test the CreatePet endpoint:

![post-pet-test](../../img/build-your-first-app/post-pet.png)

You'll see in the logs:
```
🐾 Pet created { petId: '1', name: 'Max', species: 'dog', status: 'new' }
🔄 Setting next feeding reminder { petId: '1' }
✅ Next feeding reminder set { petId: '1' }
🔄 Lifecycle orchestrator processing { petId: '1', eventType: 'feeding.reminder.completed' }
✅ Lifecycle transition completed { oldStatus: 'new', newStatus: 'in_quarantine' }
```

<Callout type="tip">
**Prefer using curl?** You can also test with command line:

```bash
curl -X POST http://localhost:3000/ts/pets \
  -H "Content-Type: application/json" \
  -d '{"name": "Max", "species": "dog", "ageMonths": 24}'
```
</Callout>

### Staff Health Check

Test the UpdatePet endpoint in Workbench to mark the pet as healthy:

![update-status-test](../../img/build-your-first-app/update-status.png)

Watch the automatic progression:
```
👤 Staff requesting status change { petId: '1', requestedStatus: 'healthy' }
🔄 Lifecycle orchestrator processing { petId: '1', eventType: 'status.update.requested' }
✅ Lifecycle transition completed { oldStatus: 'in_quarantine', newStatus: 'healthy' }
🤖 Processing automatic progression { petId: '1', currentStatus: 'healthy', nextStatus: 'available' }
✅ Automatic progression completed { oldStatus: 'healthy', newStatus: 'available' }
```

<Callout type="tip">
**Using curl?**

```bash
curl -X PUT http://localhost:3000/ts/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "healthy"}'
```
</Callout>

### Test Invalid Transitions

Try to skip a step in Workbench:

![skip-status-test](../../img/build-your-first-app/skip-status.png)

The orchestrator rejects it:
```
⚠️ Transition rejected { 
  currentStatus: 'in_quarantine', 
  requestedStatus: 'available',
  reason: 'Invalid transition: cannot change from in_quarantine to available'
}
```

<Callout type="tip">
**Using curl?**

```bash
curl -X PUT http://localhost:3000/ts/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "available"}'
```
</Callout>

### Test the Illness Workflow

Mark a pet as ill in Workbench:

![update-status-ill-test](../../img/build-your-first-app/update-status-ill.png)

Watch the automatic treatment start:
```
✅ Lifecycle transition completed { oldStatus: 'healthy', newStatus: 'ill' }
🤖 Processing automatic progression { currentStatus: 'ill', nextStatus: 'under_treatment' }
✅ Automatic progression completed { oldStatus: 'ill', newStatus: 'under_treatment' }
```

<Callout type="tip">
**Using curl?**

```bash
curl -X PUT http://localhost:3000/ts/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "ill"}'
```
</Callout>

Then mark the pet as recovered in Workbench:

![update-status-recovered-test](../../img/build-your-first-app/update-status-recovered.png)

Watch the chained automatic progressions:
```
✅ Lifecycle transition completed { oldStatus: 'under_treatment', newStatus: 'recovered' }
🤖 Processing automatic progression { currentStatus: 'recovered', nextStatus: 'healthy' }
✅ Automatic progression completed { oldStatus: 'recovered', newStatus: 'healthy' }
🤖 Processing automatic progression { currentStatus: 'healthy', nextStatus: 'available' }
✅ Automatic progression completed { oldStatus: 'healthy', newStatus: 'available' }
```

<Callout type="tip">
**Using curl?**

```bash
curl -X PUT http://localhost:3000/ts/pets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "recovered"}'
```
</Callout>

---

## Monitoring Your Orchestrator

Use the Workbench to visualize the entire flow:

### Tracing

See how events flow through your system:

![orchestrator-trace](../../img/build-your-first-app/post-pet.png)

Each trace shows:
- The initial API call
- Background job processing
- Orchestrator transitions
- Automatic progressions
- Total time for each step

### Logs

Filter by pet ID to see the complete lifecycle:

![orchestrator-logs](../../img/build-your-first-app/orchestrator-logs.png)

The logs tell the story of each pet's journey through your shelter.
---

🎉 **Congratulations!** You've built a complete workflow orchestrator that manages complex business logic while keeping your code clean and maintainable.

---

## What's Next?

Your pet shelter now has a complete backend system:
- API endpoints for CRUD operations
- Background jobs for async processing
- Workflow orchestration for complex business logic

Here are some ideas to extend your orchestrator:

- Add more status transitions (like quarantine extensions)
- Implement role-based permissions (only vets can mark pets as healthy)
- Add time-based transitions (auto-move to available after X days)
- Create analytics on transition patterns

-   [quick-start](/docs/getting-started/quick-start): Documentation for quick-start.
---
title: Quick Start
description: Get up and running with a new Motia project in just a few seconds.
---
<Steps>

<Step>
### 1. Create Your Project

Use `npx` to create a new Motia project. This single command will scaffold a new application and install all necessary dependencies.

```bash
npx motia@latest create
```

The installer will guide you through a few questions to set up your project. Once it's done, you will have a new project directory ready to go.

</Step>

<Step>
### 2. Start the Development Server

Navigate into your new project directory and start the Motia development server.

```bash
cd <your-project-name> # If you've created a new folder for the project, navigate into it

npx motia dev
```

![run dev command](/docs-images/motia-terminal.gif)

<Callout>
The `create` command uses `npm` by default. If you chose a different package manager during setup, use `pnpm dev`, `yarn dev`, or `bun dev`.
</Callout>

This command starts the Motia runtime and the Workbench, a powerful UI for developing and debugging your workflows. By default, it's available at [`http://localhost:3000`](http://localhost:3000).

</Step>

<Step>
### 3. Run Your First Flow

The starter project comes with a pre-built `basic-tutorial` flow. Let's run it.

1.  **Open the Workbench** in your browser at [`http://localhost:3000`](http://localhost:3000).
2.  **Click the `Tutorial`** button on the top right of the workbench.
3.  **Complete the `Tutorial`** to get an understanding of the basics of Motia and using the Workbench.

![run starter app](/docs-images/motia-build-your-app.gif)

</Step>

<Step>
### Next Steps

Congratulations! You've successfully ran, and observed your first Motia workflow.

- Build your first application from scratch, follow our **[Build Your First Motia App](/docs/getting-started/build-your-first-motia-app)** guide.
- To learn about Motia, dive into our **[Core Concepts](/docs/concepts/overview)**.

</Step>
</Steps>


-   [index](/docs/): Documentation for index.
---
title: Welcome to Motia
description: "Motia is a multi-language, event-driven runtime manager built on a core primitive: the Step. It feels like a backend framework, but powers distributed backends for APIs, background jobs, queues, workflows, agents, streaming, state, and observability, all unified in one system."
---

# Welcome to Motia

## Why Motia?

Backend development today is fragmented.  

APIs live in one framework, background jobs in another, queues and schedulers elsewhere, and now AI agents and streaming systems have their own runtimes. Add observability and state management on top, and you’re stitching together half a dozen tools before writing your first feature.

**Motia unifies all of these concerns around one core primitive: the Step.**

Just as React made frontend development simple by introducing components, Motia redefines backend development with Steps.  

Every backend pattern, API endpoints, background jobs, queues, workflows, AI agents, streaming, observability, and state, is expressed with the same primitive.

To read more about this, check out our [manifesto](/manifesto).

---
## The Core Primitive: the Step

At the heart of Motia is a single primitive: the **Step**.  

A Step is just a file with a `config` and a `handler`. Motia auto-discovers these files from `/steps` directory and connects them automatically.

Here’s a simple example of two Steps working together: an API Step that emits an event, and an Event Step that processes it.

<Tabs items={['TypeScript', 'Python', 'JavaScript']}>
<Tab value='TypeScript'>

```ts title="steps/send-message.step.ts"
export const config = {
  name: 'SendMessage',
  type: 'api',
  path: '/messages',
  method: 'POST',
  emits: ['message.sent']
};

export const handler = async (req, { emit }) => {
  await emit({
    topic: 'message.sent',
    data: { text: req.body.text }
  });
  return { status: 200, body: { ok: true } };
};
```

```ts title="steps/process-message.step.ts"
export const config = {
  name: 'ProcessMessage',
  type: 'event',
  subscribes: ['message.sent']
};

export const handler = async (input, { logger }) => {
  logger.info('Processing message', input);
};
```
</Tab>

<Tab value='Python'>

```python title="send_message_step.py"
config = {
    "name": "SendMessage",
    "type": "api",
    "path": "/messages",
    "method": "POST",
    "emits": ["message.sent"]
}

async def handler(req, ctx):
    await ctx.emit({
        "topic": "message.sent",
        "data": {"text": req.body["text"]}
    })
    return {"status": 200, "body": {"ok": True}}
```

```python title="process_message_step.py"
config = {
    "name": "ProcessMessage",
    "type": "event",
    "subscribes": ["message.sent"]
}

async def handler(input, ctx):
    ctx.logger.info("Processing message", input)
```
</Tab>

<Tab value='JavaScript'>

```js title="steps/send-message.step.js"
const config = {
  name: 'SendMessage',
  type: 'api',
  path: '/messages',
  method: 'POST',
  emits: ['message.sent']
};

const handler = async (req, { emit }) => {
  await emit({
    topic: 'message.sent',
    data: { text: req.body.text }
  });
  return { status: 200, body: { ok: true } };
};

module.exports = { config, handler };
```

```js title="steps/process-message.step.js"
const config = {
  name: 'ProcessMessage',
  type: 'event',
  subscribes: ['message.sent']
};

const handler = async (input, { logger }) => {
  logger.info('Processing message', input);
};

module.exports = { config, handler };
```
</Tab>
</Tabs>

👉 With just two files, you’ve built an **API endpoint**, a **queue**, and a **worker**. No extra frameworks required.

Learn more about Steps here: [What is a Step?](/docs/concepts/steps).

---

### Working with multiple Languages

The rapid advancement of AI has reshaped the software industry—many cutting-edge AI tools are available only in specific programming languages, this forces companies to decide if they either change their team's skillset to a different language or not leveraging these technologies at all.

Motia removes this limitation by allowing each Step to be written in any language, while still sharing a common state.

![Multi-language](./img/what-is-motia/multi-language.png)

_Each rectangle in the diagram above represents a Step, some of them are in TypeScript and others in Python._

## Scalability

One of the biggest dilemmas in backend development is choosing between scalability and development velocity. In startup environments, speed often takes priority, resulting in systems that don't scale well and become problematic under increased load.

Motia addresses scalability by leveraging the core primitive of **Steps**: Each step can scale independently avoiding the bottlenecks common in monolithic architectures.

![Scalable](./img/what-is-motia/scalable.png)

## Observability

Observability in traditional backends often demands significant engineering effort to implement logging, alerting, and tracing. Typically, these tools are only configured for cloud environments, local development is generally neglected—leading to low productivity and poor dev experience.

Motia offers a complete observability toolkit available in both cloud and local environments, including:

- Logs visualization
- Tracing tool to quickly visualize the flow of requests through the system
- State visualization
- Diagram representation of dependencies between steps and how they are connected

_The image below shows the Workbench interface available when you run `motia dev`. On the top panel you can see a workflow diagram with multiple steps connected.
On the bottom panel you can see the trace view of a single request and what happened in each step._

![Motia Workbench](./img/new-workbench.png)

## Fault tolerance

With the rise of AI, many backend tasks have become less deterministic and more error-prone. These scenarios require robust error handling and retry mechanisms. In traditional systems, developers often need to set up and maintain queue infrastructures to ensure resilience, especially when dealing with unreliable responses from LLMs.

Motia provides fault tolerance out of the box, eliminating the need to manually spin up queue infrastructure.

- Using Event Steps, you get retry mechanisms out of the box
- Configuration of queue infrastructure is abstracted away

## Building and Shipping

Building and deploying backends is inherently complex—especially in polyglot environments. Shipping production systems requires tight collaboration between developers and operations, and automation often takes weeks to get right.

Beyond that, cloud provider lock-in, complicated deployment strategies (e.g., rollbacks, blue/green deployments), and a lack of deployment tooling increase the risk of failure.

Motia abstracts these concerns by providing:

- True cloud-provider agnosticism
- Atomic blue/green deployments and one-click rollbacks via Motia Cloud (canary support coming soon)
- First-class polyglot backend support (currently Node.js and Python, with more on the way)

![Deployments](./img/what-is-motia/deployments.png)

_The image above shows several Steps being build to a single Motia deployable that are ultimately deployed to a cloud provider of your choice. 
Currently we're supporting AWS and Kubernetes, more Cloud providers coming soon. Check our [roadmap](https://github.com/orgs/MotiaDev/projects/2/views/4?filterQuery=title%3A+BYOC) for more details._

### Rollbacks and deployment strategies

Deploying cloud-native, fault-tolerant applications often involves modifying queue systems and other infrastructure components. 
These changes can introduce incompatibilities and lead to runtime failures.

Motia Cloud solves this with **Atomic Deployments**, which:

- Each deployment spins up a new isolated service that shares the same data layer
- Ensures safe, rollback-capable deployments without risking service downtime
- Instant rollbacks with one click since each deployment is isolated

## Real-time data streaming

Handling real-time data is one of the most common—and complex—challenges in backend development. It's necessary when building event-driven applications, 
and it typically requires setting up and maintaining a significant amount of infrastructure.

Motia provides what we call _Streams_: Developers define the structure of the data—any changes to these objects are streamed to all subscribed clients in real-time.

![Real-time data streaming](./img/what-is-motia/streams.png)

_The image above shows a Stream definition, a Node.js Step mutating the data and a client subscribing to the stream receiving real-time updates._

-   ['ChessArena AI'](/docs/product-showcase/chessarena-ai): Documentation for 'ChessArena AI'.
---
title: 'ChessArena AI'
---

In the world of AI development, chess serves as the perfect benchmark for intelligence and strategic thinking. But how do you measure which AI models truly "understand" chess beyond simple win/loss statistics? ChessArena.AI solves this challenge by focusing on move quality and game insight rather than just outcomes.

This comprehensive guide explores how to build a production-ready chess platform using Motia's event-driven architecture and real-time streaming capabilities. We'll cover:

1. **Real-Time Chess Streaming**: How Motia Streams enable live game updates across all connected players
2. **Multi-Language Architecture**: Combining TypeScript orchestration with Python chess engine integration
3. **AI Model Integration**: Supporting multiple LLM providers (OpenAI, Anthropic Claude, Google Gemini, xAI Grok) for chess gameplay
4. **Move Evaluation System**: Using Stockfish engine for real-time move analysis and scoring
5. **Production Deployment**: How this exact platform powers the live ChessArena.AI website

Let's build a chess platform that measures AI intelligence through gameplay quality.

---

## 🏭 Production-Grade Chess Platform

**This is not a tutorial project** - this is battle-tested, production-ready code that handles real traffic at scale. Every aspect has been designed for enterprise use:

- **🎮 Live Chess Platform**: Real-time games with multiple AI models competing simultaneously
- **📊 Move Quality Analysis**: Every move evaluated by Stockfish engine for strategic insight
- **⚡ Real-Time Updates**: Live game state synchronization across all connected clients
- **🤖 Multi-AI Support**: OpenAI GPT, Anthropic Claude, XAI Grok, Google Gemini integration
- **🏆 Dynamic Leaderboards**: Real-time scoring based on move quality, not just wins
- **🌍 Global Scale**: Production deployment on Motia Cloud with worldwide accessibility
- **💰 Cost Efficient**: Event-driven architecture that scales efficiently

---

## Live Proof: Powering ChessArena.AI

**This isn't just a demo** - this exact code powers the live chess platform at [ChessArena.AI](https://chessarena.ai)!

Visit the platform and you'll see:
- **🏆 Live AI Leaderboard** ranking models by move quality
- **⚡ Real-Time Games** with instant move updates and evaluations
- **📊 Move Analysis** showing centipawn scores and blunder detection
- **🎮 Multi-Model Battles** with GPT-5, Claude Opus 4, Gemini 2.5 Flash, and Grok 4 competing

That live chess platform with real-time AI battles? That's this exact implementation in production, processing thousands of moves and providing instant feedback to chess enthusiasts worldwide!

---

## The Power of Strategic AI Evaluation

<div className="my-8">![ChessArena AI](./../img/chessarena.png)</div>

At its core, ChessArena.AI solves a fundamental challenge: how do you measure AI intelligence in chess beyond simple win/loss statistics? Traditional chess platforms focus on game outcomes, but most LLM games end in draws, making it difficult to distinguish between models.

Our Motia-powered solution revolutionizes AI chess evaluation through:

- **[Stockfish Integration](https://stockfishchess.org/)**: World's strongest open-source chess engine for move analysis
- **[Centipawn Scoring](https://en.wikipedia.org/wiki/Chess_piece_relative_value#Centipawns)**: Precise move quality measurement in hundredths of a pawn
- **[Real-Time Streaming](https://motia.dev)**: Live game updates and move evaluations
- **[Multi-LLM Support](https://platform.openai.com/)**: Support for OpenAI, Anthropic, and Google AI models

Instead of focusing on who wins, we measure how well each AI model understands chess strategy and tactics.

---

## The Anatomy of Our Chess Platform

Our application consists of specialized components handling different aspects of chess gameplay, from game creation to move evaluation. Let's explore the complete architecture.

<Folder name="api/steps" defaultOpen>
  <Folder name="chess" defaultOpen>
    <File name="00-available-models-api.step.ts" />
    <File name="01-create-game.step.ts" />
    <File name="02-get-game.step.ts" />
    <File name="03-move-api.step.ts" />
    <File name="04-chess-game-moved.step.ts" />
    <File name="05-ai-player.step.ts" />
    <File name="evaluate_player_move_step.py" />
    <Folder name="streams" defaultOpen>
      <File name="00-chess-game.stream.ts" />
      <File name="00-chess-game-move.stream.ts" />
      <File name="00-chess-leaderboard.stream.ts" />
    </Folder>
  </Folder>
  <Folder name="auth" defaultOpen>
    <File name="00-auth-api.step.ts" />
    <File name="01-get-user-api.step.ts" />
  </Folder>
</Folder>

<Tabs items={['models-api', 'create-game', 'move-evaluation', 'ai-player', 'streams', 'auth']}>
  <Tab value="models-api">
    The entry point that exposes available AI models from different providers (OpenAI, Anthropic, Google, xAI) for chess gameplay. The platform supports cutting-edge models and allows easy extension for new providers.

    ```typescript
    import { AiModelsSchema } from '@chessarena/types/ai-models'
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { supportedModelsByProvider } from '../../services/ai/models'

    // Current supported models (as of 2025)
    export const supportedModelsByProvider: AiModels = {
      openai: [
        'gpt-5-2025-08-07',           // Latest GPT-5
        'o4-mini-2025-04-16',         // O4 Mini
        'gpt-4.1-nano-2025-04-14',   // GPT-4.1 Nano
        'o3-mini-2025-01-31',        // O3 Mini
        'gpt-4o-mini-2024-07-18',    // GPT-4o Mini
      ],
      gemini: [
        'gemini-2.5-flash',          // Latest Gemini 2.5 Flash
        'gemini-2.0-flash-001',      // Gemini 2.0 Flash
      ],
      claude: [
        'claude-opus-4-1-20250805',  // Claude Opus 4.1
        'claude-opus-4-20250514',    // Claude Opus 4
        'claude-sonnet-4-20250514',  // Claude Sonnet 4
        'claude-3-7-sonnet-20250219', // Claude 3.7 Sonnet
        'claude-3-5-sonnet-20241022', // Claude 3.5 Sonnet
        'claude-3-5-haiku-20241022',  // Claude 3.5 Haiku
      ],
      grok: [
        'grok-4',                     // Latest Grok 4
        'grok-3',                     // Grok 3
      ],
    }

    export const config: ApiRouteConfig = {
      type: 'api',
      name: 'AvailableModels',
      description: 'Expose all available AI models for supported providers',
      path: '/chess/models',
      method: 'GET',
      emits: [],
      flows: ['chess'],
      responseSchema: {
        200: z.object({ models: AiModelsSchema() }),
        404: z.object({ message: z.string() }),
        400: z.object({ message: z.string() }),
      },
    }

    export const handler: Handlers['AvailableModels'] = async (_, { logger }) => {
      logger.info('Received available models request')

      return {
        status: 200,
        body: {
          models: supportedModelsByProvider,
        },
      }
    }
    ```

  </Tab>
  <Tab value="create-game">
    The game creation endpoint that validates AI model selections and initializes new chess games with proper player configurations.

    ```typescript
    import { AiModelProviderSchema } from '@chessarena/types/ai-models'
    import { GameSchema, Player } from '@chessarena/types/game'
    import { ApiRouteConfig, Handlers } from 'motia'
    import { RefinementCtx, z } from 'zod'
    import { supportedModelsByProvider } from '../../services/ai/models'
    import { createGame } from '../../services/chess/create-game'
    import { auth } from '../middlewares/auth.middleware'

    const playerSchema = () => {
      return z
        .object({
          ai: AiModelProviderSchema().optional(),
          model: z.string().optional(),
        })
        .superRefine((data: Player, ctx: RefinementCtx) => {
          if (data.ai && !data.model) {
            ctx.addIssue({
              code: z.ZodIssueCode.custom,
              path: ['model'],
              message: 'Model is required when AI is enabled',
            })
          }

          if (data.ai) {
            const isValidAiProvider = data.ai in supportedModelsByProvider
            const isValidModel = data.model && supportedModelsByProvider[data.ai]?.includes(data.model)

            if (!isValidAiProvider || !isValidModel) {
              ctx.addIssue({
                code: z.ZodIssueCode.custom,
                path: data.ai ? ['model'] : ['ai'],
                message: data.ai ? 'Invalid AI model' : 'Invalid AI provider',
              })
            }
          }
        })
    }

    export const config: ApiRouteConfig = {
      type: 'api',
      name: 'CreateGame',
      description: 'Create a new chess game',
      path: '/chess/create-game',
      method: 'POST',
      emits: ['chess-game-created'],
      flows: ['chess'],
      bodySchema: z.object({
        players: z.object({
          white: playerSchema(),
          black: playerSchema(),
        }),
      }),
      middleware: [auth({ required: true })],
      responseSchema: {
        200: GameSchema,
        400: z.object({ message: z.string(), errors: z.array(z.object({ message: z.string() })) }),
        401: z.object({ message: z.string() }),
      },
    }

    export const handler: Handlers['CreateGame'] = async (req, { logger, emit, streams }) => {
      logger.info('[CreateGame] Creating new chess game')

      const game = await createGame(req.body.players, req.user, streams, logger)

      await emit({
        topic: 'chess-game-created',
        data: { gameId: game.id, fenBefore: game.fen },
      })

      logger.info('[CreateGame] Game created successfully', { gameId: game.id })

      return { status: 200, body: game }
    }
    ```

  </Tab>
  <Tab value="move-evaluation">
    The Python-powered move evaluation system that uses Stockfish to analyze every move and calculate centipawn scores for strategic insight.

    ```python
    import chess
    import chess.engine
    import os
    from pydantic import BaseModel, Field

    class EvaluatePlayerMoveInput(BaseModel):
        fenBefore: str = Field(description="The FEN of the game before the move")
        fenAfter: str = Field(description="The FEN of the game after the move")
        gameId: str = Field(description="The ID of the game")
        moveId: str = Field(description="The ID of the move")
        player: str = Field(description="The player who made the move")

    config = {
        "type": "event",
        "name": "EvaluatePlayerMove",
        "description": "Evaluates move quality using Stockfish engine",
        "subscribes": ["evaluate-player-move"], 
        "emits": [],
        "flows": ["chess"],
        "input": EvaluatePlayerMoveInput.model_json_schema(),
    }

    class Evaluation(BaseModel):
        centipawn_score: int = Field(description="The evaluation in centipawns")
        best_move: str = Field(description="The best move")

    async def evaluate_position(
        engine: chess.engine.SimpleEngine,
        board: chess.Board,
        player: str,
        time_limit: float = 1.5
    ) -> Evaluation:
        """Evaluate a chess position and return analysis results."""
        analysis = await engine.analyse(
            board, 
            chess.engine.Limit(time=time_limit),
            info=chess.engine.INFO_ALL
        )
        
        score = analysis["score"]
        centipawn_score = score.white().score() if player == "white" else score.black().score()
        move = analysis.get("pv", [None])[0]

        return Evaluation(
            centipawn_score=centipawn_score if centipawn_score is not None else 0,
            best_move=move.uci() if move is not None else None
        )

    async def handler(input: EvaluatePlayerMoveInput, ctx):
        logger = ctx.logger
        
        # Initialize Stockfish engine
        engine_path = os.getenv("STOCKFISH_BIN_PATH")
        if not engine_path:
            raise EnvironmentError("STOCKFISH_BIN_PATH environment variable not set")
        
        _, engine = await chess.engine.popen_uci(engine_path)
        
        try:
            # Create boards from the positions
            board_before = chess.Board(input.fenBefore)
            board_after = chess.Board(input.fenAfter)
        
            # Evaluate positions
            eval_before = await evaluate_position(engine, board_before, input.player)
            eval_after = await evaluate_position(engine, board_after, input.player)

            # Calculate best move evaluation
            best_move = chess.Move.from_uci(eval_before.best_move)
            board_before.push(best_move)
            eval_best_move = await evaluate_position(engine, board_before, input.player)

            # Calculate move quality metrics
            evaluation_swing = max(0, eval_best_move.centipawn_score - eval_after.centipawn_score)
            blunder = evaluation_swing > 100  # Moves losing >100 centipawns are blunders

            evaluation = {
                "centipawnScore": eval_after.centipawn_score,
                "bestMove": eval_after.best_move,
                "evaluationSwing": evaluation_swing,
                "blunder": blunder,
            }

            # Update move in streams with evaluation
            move_stream = await ctx.streams.chessGameMove.get(input.gameId, input.moveId)
            move_stream["evaluation"] = evaluation
            await ctx.streams.chessGameMove.set(input.gameId, input.moveId, move_stream)

            logger.info("Move evaluation completed", { "evaluation": evaluation })

        finally:
            await engine.quit()
    ```

  </Tab>
  <Tab value="ai-player">
    The AI orchestration step that coordinates with different LLM providers using a unified prompt system. Features retry logic, move validation, and real-time thought streaming.

    ```typescript
    import { EventConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { makePrompt } from '../../services/ai/make-prompt'
    import { evaluateBestMoves } from '../../services/chess/evaluate-best-moves'
    import { move } from '../../services/chess/move'
    import mustache from 'mustache'

    const MAX_ATTEMPTS = 3

    const responseSchema = z.object({
      thought: z.string({
        description: 'The thought process of the move, make it look like you were just thinking for yourself'
      }),
      move: z.object({
        from: z.string({ description: 'The square to move from, example: e2' }),
        to: z.string({ description: 'The square to move to, example: e4' }),
        promote: z.enum(['queen', 'rook', 'bishop', 'knight']).optional(),
      }),
    })

    export const config: EventConfig = {
      type: 'event',
      name: 'AI_Player',
      description: 'AI Player with unified provider system and retry logic',
      subscribes: ['ai-move'],
      emits: ['chess-game-moved', 'chess-game-ended', 'evaluate-player-move'],
      flows: ['chess'],
      includeFiles: ['05-ai-player.mustache'], // Mustache template for chess prompts
    }

    export const handler: Handlers['AI_Player'] = async (input, { logger, emit, streams }) => {
      const game = await streams.chessGame.get('game', input.gameId)
      const player = input.player === 'white' ? game.players.white : game.players.black

      if (!player.ai) {
        logger.error('Player has no AI configured', { gameId: input.gameId })
        return
      }

      let attempts = 0
      let lastInvalidMove = undefined
      const validMoves = evaluateBestMoves(game)

      while (attempts < MAX_ATTEMPTS) {
        const messageId = crypto.randomUUID()

        // Create real-time thinking message
        await streams.chessGameMessage.set(input.gameId, messageId, {
          id: messageId,
          message: 'Thinking...',
          sender: player.ai,
          role: input.player,
          timestamp: Date.now(),
        })

        // Generate prompt using Mustache template
        const prompt = mustache.render(template, {
          fenBefore: input.fenBefore,
          fen: input.fen,
          lastMove: input.lastMove,
          inCheck: input.check,
          player: input.player,
          lastInvalidMove,
          validMoves,
        })

        try {
          // Use unified AI provider system
          const action = await makePrompt({
            prompt,
            zod: responseSchema,
            provider: player.ai,  // 'openai', 'claude', 'gemini', or 'grok'
            logger,
            model: player.model!, // Specific model like 'gpt-5-2025-08-07'
          })

          // Update message with AI's thought process
          await streams.chessGameMessage.set(input.gameId, messageId, {
            message: action.thought,
            move: action.move,
            sender: player.ai,
            role: input.player,
            timestamp: Date.now(),
          })

          // Execute the chess move
          await move({
            logger,
            streams,
            gameId: input.gameId,
            player: input.player,
            game,
            action: action.move,
            emit,
            illegalMoveAttempts: attempts,
          })

          return // Success!

        } catch (err) {
          attempts++
          lastInvalidMove = action?.move
          
          // Handle illegal moves with retry logic
          if (attempts >= MAX_ATTEMPTS) {
            // Player loses after too many illegal moves
            await streams.chessGame.set('game', game.id, {
              ...game,
              status: 'completed',
              winner: input.player === 'white' ? 'black' : 'white',
              endGameReason: 'Too many illegal moves',
            })
            
            await emit({
              topic: 'chess-game-ended',
              data: { gameId: input.gameId },
            })
          }
        }
      }
    }
    ```

  </Tab>
  <Tab value="streams">
    The real-time data streams that power live chess gameplay, storing game state, moves, and leaderboard data with automatic client synchronization.

    ```typescript
    // Chess Game Stream - stores complete game state
    import { StreamConfig } from 'motia'
    import { GameSchema } from '@chessarena/types/game'

    export const config: StreamConfig = {
      name: 'chessGame',
      schema: GameSchema,
      baseConfig: { storageType: 'default' },
    }
    ```

    ```typescript
    // Chess Game Move Stream - stores individual moves with evaluations
    import { StreamConfig } from 'motia'
    import { GameMoveSchema } from '@chessarena/types/game-move'

    export const config: StreamConfig = {
      name: 'chessGameMove',
      schema: GameMoveSchema,
      baseConfig: { storageType: 'default' },
    }
    ```

    ```typescript
    // Chess Leaderboard Stream - live AI model rankings
    import { StreamConfig } from 'motia'
    import { LeaderboardSchema } from '@chessarena/types/leaderboard'

    export const config: StreamConfig = {
      name: 'chessLeaderboard',
      schema: LeaderboardSchema,
      baseConfig: { storageType: 'default' },
    }
    ```

  </Tab>
  <Tab value="auth">
    The authentication system that manages user sessions and provides secure access to chess game creation and management.

    ```typescript
    import { ApiRouteConfig, Handlers } from 'motia'
    import { z } from 'zod'
    import { authenticateUser } from '../../services/auth/auth-service'

    export const config: ApiRouteConfig = {
      type: 'api',
      name: 'AuthAPI',
      description: 'Handle user authentication for chess platform',
      path: '/auth/login',
      method: 'POST',
      emits: ['user-authenticated'],
      flows: ['auth'],
      bodySchema: z.object({
        email: z.string().email(),
        password: z.string().min(6),
      }),
      responseSchema: {
        200: z.object({ 
          token: z.string(), 
          user: z.object({ id: z.string(), email: z.string() }) 
        }),
        401: z.object({ message: z.string() }),
      },
    }

    export const handler: Handlers['AuthAPI'] = async (req, { logger, emit }) => {
      const { email, password } = req.body

      try {
        const authResult = await authenticateUser(email, password)
        
        if (!authResult.success) {
          return { status: 401, body: { message: 'Invalid credentials' } }
        }

        await emit({
          topic: 'user-authenticated',
          data: { userId: authResult.user.id, email: authResult.user.email },
        })

        return {
          status: 200,
          body: {
            token: authResult.token,
            user: authResult.user,
          },
        }
      } catch (error) {
        logger.error('[AuthAPI] Authentication error', { error: error.message })
        return { status: 401, body: { message: 'Authentication failed' } }
      }
    }
    ```

  </Tab>
</Tabs>

---

## Extensible AI Provider System

ChessArena.AI features a plugin-based architecture that makes adding new AI providers incredibly simple. The unified `makePrompt` system handles all provider differences behind a clean interface.

### Adding New AI Providers

To add a new AI provider (like Anthropic's upcoming models or other LLM providers), you only need to:

1. **Create a provider handler** in `services/ai/your-provider.ts`:

```typescript
import { Handler } from './types'

export const yourProvider: Handler = async ({ prompt, zod, logger, model }) => {
  // Initialize your AI client
  const client = new YourAIClient({ apiKey: process.env.YOUR_API_KEY })
  
  // Make the API call with structured output
  const response = await client.chat({
    model: model ?? 'your-default-model',
    messages: [{ role: 'user', content: prompt }],
    responseFormat: { type: 'json_schema', schema: zodToJsonSchema(zod) },
  })
  
  logger.info('Your provider response received', { model })
  
  return JSON.parse(response.content)
}
```

2. **Register the provider** in `services/ai/make-prompt.ts`:

```typescript
import { yourProvider } from './your-provider'

const providers: Record<AiModelProvider, Handler> = {
  openai,
  gemini,
  claude,
  grok,
  yourProvider, // Add your provider here
}
```

3. **Update the type definitions** in `types/ai-models.ts`:

```typescript
export const AiModelProviderSchema = () => 
  z.enum(['openai', 'gemini', 'claude', 'grok', 'yourProvider'])
```

4. **Add supported models** in `services/ai/models.ts`:

```typescript
export const supportedModelsByProvider: AiModels = {
  // ... existing providers
  yourProvider: [
    'your-model-v1',
    'your-model-v2-turbo',
    'your-model-reasoning',
  ],
}
```

That's it! Your new AI provider is now fully integrated and can compete in chess battles alongside GPT, Claude, Gemini, and Grok.

### Current Provider Implementations

The platform currently supports four major AI providers with their latest models:

- **OpenAI**: GPT-5, O4 Mini, GPT-4.1 series, O3 Mini
- **Anthropic**: Claude Opus 4.1, Claude Sonnet 4, Claude 3.7 series  
- **Google**: Gemini 2.5 Flash, Gemini 2.0 Flash
- **xAI**: Grok 4, Grok 3

Each provider uses optimized API calls with structured JSON output and proper error handling.

---

## Real-Time Chess Architecture

The beauty of this chess platform lies in its event-driven, real-time architecture. Here's how live chess games flow through the system:

1. **Game Creation** → User selects AI models and creates a new game
2. **Move Generation** → AI models generate moves using LLM APIs
3. **Move Validation** → Chess rules validation and board state updates
4. **Stockfish Analysis** → Real-time move evaluation and scoring
5. **Stream Updates** → Live game state propagated to all connected clients
6. **Leaderboard Updates** → AI model rankings updated based on move quality

**No manual state management, no complex WebSocket handling, no synchronization code required!**

---

## Key Features & Benefits

### 🎮 **Real-Time Chess Gameplay**
Live games with instant move updates across all connected clients - watch AI models battle in real-time.

### 🏆 **Intelligent Scoring System**  
Move quality evaluation using Stockfish engine with centipawn precision and blunder detection.

### 🤖 **Multi-AI Integration**
Support for OpenAI GPT, Anthropic Claude, and Google Gemini models with unified API interface.

### ⚡ **Event-Driven Architecture**
Scalable, maintainable system where each component handles specific chess functionality.

### 📊 **Live Leaderboards**
Real-time AI model rankings based on move quality, strategic insight, and game performance.

### 🌐 **Production-Ready**
Battle-tested code powering the live ChessArena.AI platform with global accessibility.

---

## Trying It Out

Ready to build your own AI chess platform? Let's get it running.

<Steps>

### Clone and Install

Start by getting the project locally and installing dependencies.

```shell
git clone https://github.com/MotiaDev/chessarena-ai.git
cd chessarena-ai
pnpm install
```

### Install Stockfish Engine

The platform requires Stockfish for move evaluation. Choose your installation method:

**Option A: Using Homebrew (macOS - Recommended)**
```shell
brew install stockfish
```

**Option B: Using the project installer**
```shell
pnpm install-stockfish <platform>
# Supported: linux-x86, mac-m1
```

**Option C: Manual Installation**
Download from [stockfishchess.org](https://stockfishchess.org/)

### Configure Environment Variables

Create a `.env` file with your AI provider API keys:

```shell
# Required: AI Model API Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_AI_API_KEY="..."

# Required: Stockfish Engine Path
STOCKFISH_BIN_PATH="/opt/homebrew/bin/stockfish"

# Optional: Authentication (for user management)
JWT_SECRET="your-jwt-secret"
```

### Start the Chess Platform

Launch both the API backend and React frontend:

```shell
pnpm dev
```

This starts:
- **API Backend**: `http://localhost:3000` (Motia API with chess logic)
- **React Frontend**: `http://localhost:5173` (Chess game interface)

### Create Your First AI Battle

1. **Open the Chess Platform**: Navigate to `http://localhost:5173`
2. **Select AI Models**: Choose different models for white and black players
3. **Start the Game**: Watch AI models battle with real-time move evaluation
4. **View Analysis**: See centipawn scores, best moves, and blunder detection
5. **Check Leaderboards**: Monitor AI model performance rankings

### Access Real-Time Data

Your chess games are available via the Motia streams API:

```shell
# Get all active games
curl http://localhost:3000/api/streams/chessGame

# Get specific game state
curl http://localhost:3000/api/streams/chessGame/{gameId}

# Get move history with evaluations
curl http://localhost:3000/api/streams/chessGameMove/{gameId}

# Get AI model leaderboard
curl http://localhost:3000/api/streams/chessLeaderboard
```

### Deploy to Production

Once your chess platform is working locally, deploy it to production with Motia Cloud:

**Option 1: CLI Deployment**
```shell
# Deploy with version and API key
motia cloud deploy --api-key your-api-key --version-name 1.0.0

# Deploy with environment variables
motia cloud deploy --api-key your-api-key \
  --version-name 1.0.0 \
  --env-file .env.production \
  --environment-id your-env-id
```

**Option 2: One-Click Web Deployment**
1. Ensure your local project is running (`pnpm dev`)
2. Go to [Motia Cloud -> Import from Workbench](https://motia.cloud)
3. Select your local project port
4. Choose project and environment name
5. Upload environment variables (optional)
6. Click **Deploy** and watch the magic happen! ✨

</Steps>

---

## 🚀 Production Deployment Guide

### Environment Variables

Configure these environment variables for production security and functionality:

```shell
# Required: AI Model API Keys
OPENAI_API_KEY="sk-your-openai-key"          # For GPT-5, O4 Mini, GPT-4.1 series
ANTHROPIC_API_KEY="sk-ant-your-anthropic-key" # For Claude Opus 4.1, Sonnet 4
GEMINI_API_KEY="your-google-gemini-key"      # For Gemini 2.5 Flash, 2.0 Flash  
XAI_API_KEY="your-xai-grok-key"              # For Grok 4, Grok 3

# Required: Stockfish Engine Path
STOCKFISH_BIN_PATH="/opt/homebrew/bin/stockfish"

# Optional: Authentication for user management
JWT_SECRET="your-secure-jwt-secret"

# Optional: Database configuration for user data
DATABASE_URL="postgresql://user:password@host:port/database"
```

### Security Best Practices

For production deployments, ensure you:

1. **Secure API keys**: 
   ```shell
   # Generate a cryptographically secure JWT secret
   openssl rand -hex 32
   ```

2. **Store secrets securely**: Use environment variables, never commit API keys to code

3. **Monitor AI usage**: Track API usage and costs across different model providers

4. **Enable rate limiting**: Implement request limits to prevent abuse

### Scaling Considerations

This architecture scales automatically with your chess platform traffic:

- **Multiple games**: Each game gets its own stream for real-time updates
- **High concurrency**: Motia streams handle thousands of concurrent chess games
- **Global distribution**: Deploy to multiple regions for worldwide performance
- **AI model optimization**: Load balance across different model providers
- **Cost optimization**: Pay only for actual usage with serverless scaling

---

## 💻 Dive into the Code

Want to explore the complete chess platform implementation? Check out the full source code with AI integration, real-time streams, and production deployment:

<div className="not-prose">
  <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Live ChessArena.AI Platform</h3>
        <p className="text-gray-600 mb-4">Access the complete implementation powering the live chess platform. See exactly how AI models battle with real-time evaluation and scoring!</p>
        <div className="flex flex-col sm:flex-row gap-3">
          <a 
            href="https://github.com/MotiaDev/chessarena-ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.30 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View ChessArena.AI Code
          </a>
          <a 
            href="https://chessarena.ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            Play Live Chess →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

---

## Conclusion: Intelligence Through Strategic Play

This ChessArena.AI platform demonstrates how to build sophisticated AI evaluation systems using event-driven architecture. By focusing on move quality rather than simple win/loss statistics, we've created a platform that truly measures AI strategic understanding.

The beauty of this approach is its extensibility:
- **Add new AI models**: Integrate any LLM provider with the unified interface
- **Enhanced analysis**: Implement opening book analysis, endgame evaluation
- **Tournament modes**: Multi-round competitions with advanced scoring
- **Educational features**: Move explanations, tactical puzzles, learning modes

Key architectural benefits:
- **Real-time synchronization**: All clients see live game updates automatically
- **Scalable evaluation**: Stockfish analysis runs independently of game flow
- **Multi-language power**: TypeScript orchestration with Python chess engine integration
- **Production reliability**: Battle-tested code handling real user traffic

This exact implementation powers the live chess platform at [ChessArena.AI](https://chessarena.ai) - that real-time AI battle system with move-by-move evaluation? It's this code in action, proven at scale with thousands of chess enthusiasts worldwide.

**Production Metrics:**
- Handles 1,000+ concurrent chess games
- Processes 10,000+ moves daily with real-time evaluation
- Sub-100ms move analysis and streaming updates
- 99.9% uptime with automatic scaling

Ready to build AI evaluation platforms that measure true intelligence? Deploy production-ready chess systems with Motia today!


-   [Product Showcase](/docs/product-showcase): Documentation for Product Showcase.
---
title: Product Showcase
---

Explore full-scale production applications built with Motia that demonstrate the framework's capabilities in real-world scenarios.

<Cards>
  <Card
    title="ChessArena AI"
    href="/docs/product-showcase/chessarena-ai"
    description="Production-grade chess platform with real-time AI battles, move evaluation, and live leaderboards"
  />
</Cards>

<br/>

## 💻 Live Applications

These are not just examples or tutorials - they are fully functional, production-ready applications that handle real user traffic and demonstrate Motia's capabilities at scale.

<div className="not-prose">
  <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6 my-6">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Production-Ready Applications</h3>
        <p className="text-gray-600 mb-4">These applications demonstrate Motia's enterprise capabilities with real user traffic, production deployments, and battle-tested architectures.</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <a 
            href="https://chessarena.ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-md transition-colors duration-200"
          >
            🏆 Live Chess Platform
          </a>
          <a 
            href="https://github.com/MotiaDev/motia-examples" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium rounded-md transition-colors duration-200"
          >
            📚 Source Code →
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

## Contribute

Have you built something amazing with Motia? We'd love to feature your production application! Please [reach out to us](mailto:hello@motia.dev) with details about your project.


-   [video-showcase](/docs/video-showcase): Documentation for video-showcase.
---
title: Video Showcase
description: Watch Motia in action through our video demonstrations and tutorials
---

import VideoShowcase from '@/components/VideoShowcase';

{/* 
  TO UPDATE VIDEO TITLES & DESCRIPTIONS:
  1. Visit each YouTube URL below
  2. Copy the actual video title and description
  3. Replace the placeholder text in the videos array
  
  Video URLs to check:
  - https://youtu.be/U59FUduO6wY (Video ID: U59FUduO6wY)
  - https://youtu.be/UUVE5db78cc (Video ID: UUVE5db78cc)  
  - https://youtu.be/7KZS0syLrUo (Video ID: 7KZS0syLrUo)
  - https://youtu.be/JECQtMSBJyY (Video ID: JECQtMSBJyY)
*/}

# Video Showcase

Explore Motia's capabilities through our collection of demonstration videos and tutorials. These videos showcase real-world examples, feature walkthroughs, and development workflows.

<VideoShowcase
  title="Featured Videos"
  description="Watch Motia in action with these curated video demonstrations"
  columns={2}
  videos={[
    {
      id: "demo-1",
      title: "A challenge to traditional backend development flow",
      description: "A challenge to traditional backend",
      url: "https://youtu.be/U59FUduO6wY?si=pw4CmpZXLreHVzs6"
    },
    {
      id: "demo-2", 
      title: "Vercel but for backend",
      description: "Motia Overview",
      url: "https://youtu.be/UUVE5db78cc?si=th_rD9cgMsE1BJrt"
    },
    {
      id: "demo-3",
      title: "Next.js Background Jobs Are Easy Now",
      description: "Next.js Background Jobs with Motia",
      url: "https://youtu.be/7KZS0syLrUo?si=3LEyfcZ-5ZaEB8xQ"
    },
    {
      id: "demo-4",
      title: "You have never seen a DX (Developer Experience) like this",
      description: "Motia's Interactive tutorial Demo",
      url: "https://youtu.be/JECQtMSBJyY?si=aScCBb09B5tXfOsX"
    },
    {
      id: "demo-5",
      title: "The only AI framework you’ll ever need",
      description: "Motia's tutorial for LinkedIn and Twitter Automation on Typefully",
      url: "https://www.youtube.com/watch?v=6EFTemC99AM"
    }
  ]}
/>

## Adding More Videos

To add more videos to this showcase, simply edit this file and add new video objects to the `videos` array. Each video should have:

- `id`: A unique identifier for the video
- `title`: The display title for the video
- `description`: A brief description of what the video covers
- `url`: The YouTube URL (supports various formats)

```typescript
{
  id: "your-video-id",
  title: "Your Video Title",
  description: "Brief description of the video content",
  url: "https://youtu.be/YOUR_VIDEO_ID"
}
```



## Optional
-   [https://motiadev.com](https://motiadev.com): Main page for framework.
-   [Github repo](https://github.com/motiadev/motia): Main github repository to file issues.
