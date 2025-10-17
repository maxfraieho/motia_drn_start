# Motia Core Concepts - AI Assistant Guide

> Компактна версія для AI асистентів. Повна документація: Claude.md

## System Context

Ви - AI асистент, що спеціалізується на створенні Motia workflows. Motia - це code-first framework для побудови event-driven backend систем.

**Ключові принципи:**
- Все є Step (API, Event, Cron)
- Event-driven архітектура за замовчуванням
- Підтримка TypeScript, Python, JavaScript
- Автоматичне відкриття Steps у папці `steps/`

## Core Primitive: Steps

### Анатомія Step

Кожен Step = 2 частини:

1. **Config** - коли і як він запускається
2. **Handler** - що він робить

```typescript
// config - визначає тип, ім'я, тригери
export const config: ApiRouteConfig = {
  name: 'StepName',      // унікальний ідентифікатор
  type: 'api',           // api | event | cron | noop
  path: '/endpoint',     // для API
  method: 'POST',        // для API
  emits: ['topic.name'], // події які емітить
  subscribes: []         // події на які підписаний (для event)
}

// handler - бізнес-логіка
export const handler: Handlers['StepName'] = async (req, ctx) => {
  // ctx: { logger, emit, state, streams, traceId }
  return { status: 200, body: { success: true } }
}
```

### Types Steps

| Type | Тригер | Використання |
|------|--------|--------------|
| `api` | HTTP request | REST API, webhooks |
| `event` | Event emission | Background jobs, async workflows |
| `cron` | Schedule | Періодичні задачі |
| `noop` | Virtual | Візуалізація зовнішніх систем |

### File Naming

- TypeScript: `*.step.ts`
- Python: `*_step.py` (underscore!)
- JavaScript: `*.step.js`

**Auto-discovery:** Motia сканує `steps/` і автоматично знаходить всі файли з `.step.` або `_step.`

## Event-Driven Architecture

Steps не викликають один одного напряму - вони використовують **emit** та **subscribe**:

```typescript
// Step 1: емітить подію
await ctx.emit({
  topic: 'user.created',
  data: { userId: '123' }
})

// Step 2: підписаний на подію
config = {
  type: 'event',
  subscribes: ['user.created']
}
```

**Переваги:**
- Decoupling - steps незалежні
- Resilience - auto-retry на failures
- Scalability - паралельна обробка
- Observability - повна трасуємість

## Context API

Кожен handler отримує `ctx` об'єкт:

| Property | Опис |
|----------|------|
| `logger` | Structured logging (info, warn, error, debug) |
| `emit` | Емісія подій для тригеру інших Steps |
| `state` | Persistent key-value storage |
| `streams` | Real-time data channels |
| `traceId` | Унікальний ID для трасування запитів |

### Logger

```typescript
ctx.logger.info('Message', { metadata })
ctx.logger.error('Error', { error: e.message })
ctx.logger.warn('Warning', { context })
ctx.logger.debug('Debug info', { details })
```

### State Management

```typescript
// Scope: groupId (наприклад traceId, userId)
await ctx.state.set(groupId, 'key', value)
const data = await ctx.state.get(groupId, 'key')
await ctx.state.delete(groupId, 'key')
await ctx.state.clear(groupId)
```

### Streams (Real-time)

```typescript
// Push updates до клієнтів
await ctx.streams.notifications.set(groupId, itemId, data)
await ctx.streams.notifications.delete(groupId, itemId)
```

## Step Types Details

### API Step

```typescript
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'CreateUser',
  path: '/users',
  method: 'POST',
  emits: ['user.created'],
  bodySchema: z.object({ email: z.string() }) // validation
}

export const handler = async (req, ctx) => {
  // req: { body, headers, pathParams, queryParams }
  await ctx.emit({ topic: 'user.created', data: req.body })
  return { status: 201, body: { id: '123' } }
}
```

### Event Step

```typescript
export const config: EventConfig = {
  type: 'event',
  name: 'SendWelcomeEmail',
  subscribes: ['user.created'],
  emits: ['email.sent']
}

export const handler = async (input, ctx) => {
  // input - data з емітованої події
  ctx.logger.info('Sending email', { to: input.email })
  await sendEmail(input.email)
}
```

### Cron Step

```typescript
export const config: CronConfig = {
  type: 'cron',
  name: 'DailyCleanup',
  cron: '0 0 * * *', // щоденно о півночі
  emits: ['cleanup.completed']
}

export const handler = async (ctx) => {
  ctx.logger.info('Running cleanup')
  await cleanupOldData()
}
```

## Best Practices

### 1. Security

- ✅ Використовуй environment variables для secrets
- ✅ Валідуй inputs з `bodySchema` або Pydantic
- ✅ Sanitize user inputs
- ❌ НІКОЛИ не хардкодь API keys у коді

### 2. Error Handling

```typescript
try {
  await riskyOperation()
} catch (error) {
  ctx.logger.error('Operation failed', {
    error: error.message,
    stack: error.stack
  })
  throw error // або повернути error response
}
```

### 3. State Management

- Використовуй `traceId` для request-specific data
- Використовуй `userId` для user-specific data
- Очищуй state після завершення flow

### 4. Logging

```typescript
// ✅ Structured logging
ctx.logger.info('Payment processed', {
  paymentId, amount, status
})

// ❌ Уникай
ctx.logger.info(`Payment ${paymentId} processed`)
```

### 5. Middleware (API only)

```typescript
const authMiddleware = async (req, ctx, next) => {
  if (!req.headers.authorization) {
    return { status: 401, body: { error: 'Unauthorized' } }
  }
  return next() // продовжити до handler
}

export const config = {
  type: 'api',
  middleware: [authMiddleware]
}
```

## Common Patterns

### 1. Request-Response with Background Processing

```typescript
// API: прийняти request, емітнути подію, повернути response
export const handler = async (req, ctx) => {
  await ctx.emit({ topic: 'process.data', data: req.body })
  return { status: 202, body: { message: 'Processing started' } }
}

// Event: обробити в background
config = { type: 'event', subscribes: ['process.data'] }
```

### 2. Multi-step Workflow

```
API → emit('step1') → Event1 → emit('step2') → Event2 → emit('done')
```

### 3. Human-in-the-Loop

```typescript
// Використовуй NOOP steps для моделювання зовнішніх процесів
export const config: NoopConfig = {
  type: 'noop',
  virtualSubscribes: ['approval.requested'],
  virtualEmits: ['/api/approval/callback']
}
```

## Testing & Development

### Start Dev Server

```bash
npm run dev  # http://localhost:3000
```

### Trigger Event

```bash
npx motia emit --topic "test.event" --message '{"key":"value"}'
```

### Test API

```bash
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"data":"test"}'
```

### Workbench

- Відкрий http://localhost:3000
- Візуалізуй flows
- Тестуй API endpoints
- Переглядай logs в real-time

## Project Structure

```
my-project/
├── steps/              # Всі Steps тут (авто-discovery)
│   ├── api/
│   │   └── create-user.step.ts
│   ├── events/
│   │   └── send-email_step.py
│   └── cron/
│       └── cleanup.step.js
├── config.yml          # Motia config (опціонально)
├── .env               # Environment variables (НЕ commitити!)
├── package.json       # Node.js dependencies
└── requirements.txt   # Python dependencies
```

## Multi-Language Support

**В одному проекті:**
- TypeScript API endpoint
- Python ML processing
- JavaScript email sender

Всі Steps діляться state, events, logging.

## Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
```

```typescript
const apiKey = process.env.OPENAI_API_KEY
```

```python
import os
api_key = os.environ.get('OPENAI_API_KEY')
```

## Code Standards

- ✅ TypeScript за замовчуванням (якщо не вказано інше)
- ✅ ES modules (`import/export`)
- ✅ Всі Steps у одному файлі (якщо не вказано інше)
- ✅ Proper error handling
- ✅ Structured logging
- ✅ Type annotations (TS/Python)
- ❌ No hardcoded secrets

## Output Format

При створенні Steps:

1. **Config block** - з коментарями
2. **Handler block** - з error handling
3. **Usage example** - як тестувати

Завжди надавай **повні файли**, не partial updates.

## Deployment

### Motia Cloud
```bash
motia cloud deploy --api-key KEY --version-name v1.0.0
```

### Self-Hosted
```bash
motia docker setup
motia docker run
```

## Quick Reference

| Потрібно | Використовуй |
|----------|--------------|
| HTTP endpoint | `type: 'api'` |
| Background job | `type: 'event'` |
| Scheduled task | `type: 'cron'` |
| Зберегти дані | `ctx.state.set()` |
| Логування | `ctx.logger.info()` |
| Емітнути подію | `ctx.emit()` |
| Real-time update | `ctx.streams` |
| Track request | `ctx.traceId` |

## Для деталей

Повна документація, приклади, API reference → **Claude.md**

---

**Version:** Core v1.0
**Full docs:** Claude.md (678KB)
**Updated:** 2025-10-09
