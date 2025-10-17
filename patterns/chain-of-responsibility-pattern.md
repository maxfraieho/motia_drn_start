# Chain of Responsibility Pattern для Motia Steps

## Pattern Overview

Chain of Responsibility дозволяє передавати запити вздовж ланцюжка обробників. Кожен обробник вирішує чи обробляти запит самому або передати його наступному в ланцюжку.

## Motia-Specific Implementation

**Event Chain:**
```
Step1 → emit(next) → Step2 → emit(next) → Step3 → emit(done)
```

Кожен Step в ланцюжку:
1. Обробляє частину запиту
2. Вирішує чи передавати далі
3. Емітує подію для наступного кроку

## Key Concepts

1. **Sequential Processing**: Обробка в певній послідовності
2. **Early Exit**: Ланцюжок може зупинитися на будь-якому кроці
3. **Responsibility**: Кожен Step відповідає за свою частину
4. **Flexibility**: Легко додавати/видаляти кроки

## Code Structure

```typescript
// Step 1: Start of chain
export const config1: EventConfig = {
  type: 'event',
  name: 'ChainStep1',
  subscribes: ['chain.start'],
  emits: ['chain.step2', 'chain.rejected']
}

export const handler1 = async (input, ctx) => {
  ctx.logger.info('Chain Step 1: Validation')

  // Process and decide
  if (!validate(input)) {
    ctx.logger.warn('Validation failed, stopping chain')
    await ctx.emit({
      topic: 'chain.rejected',
      data: { reason: 'validation_failed', step: 1 }
    })
    return
  }

  // Pass to next step
  await ctx.emit({
    topic: 'chain.step2',
    data: { ...input, step1Complete: true }
  })
}

// Step 2: Middle of chain
export const config2: EventConfig = {
  type: 'event',
  name: 'ChainStep2',
  subscribes: ['chain.step2'],
  emits: ['chain.step3', 'chain.rejected']
}

export const handler2 = async (input, ctx) => {
  ctx.logger.info('Chain Step 2: Enrichment')

  // Process
  const enrichedData = await enrichData(input)

  if (!enrichedData.canProceed) {
    await ctx.emit({
      topic: 'chain.rejected',
      data: { reason: 'enrichment_failed', step: 2 }
    })
    return
  }

  // Pass to next
  await ctx.emit({
    topic: 'chain.step3',
    data: { ...enrichedData, step2Complete: true }
  })
}

// Step 3: End of chain
export const config3: EventConfig = {
  type: 'event',
  name: 'ChainStep3',
  subscribes: ['chain.step3'],
  emits: ['chain.completed']
}

export const handler3 = async (input, ctx) => {
  ctx.logger.info('Chain Step 3: Final processing')

  // Final processing
  const result = await finalProcess(input)

  // Complete chain
  await ctx.emit({
    topic: 'chain.completed',
    data: { ...result, allStepsComplete: true }
  })
}
```

## Best Practices

1. **State Tracking**: Зберігай прогрес у `ctx.state`
2. **Error Propagation**: Емітуй error events для failed chains
3. **Logging**: Логуй кожен крок у ланцюжку
4. **Timeout**: Встановлюй timeout для всього ланцюжка
5. **Idempotency**: Кожен крок повинен бути ідемпотентним

## Common Mistakes

❌ **Circular chains** (Step1 → Step2 → Step1)
❌ **No termination** condition
❌ **Missing error handling** в ланцюжку
❌ **Lost context** між кроками
❌ **Too long chains** (>5-7 steps)

## Use Cases

- **Data Pipeline**: Extract → Transform → Load
- **Request Processing**: Validate → Authenticate → Authorize → Process
- **Content Moderation**: PreCheck → AIAnalysis → HumanReview → Publish
- **Order Fulfillment**: Validate → Reserve → Charge → Ship → Confirm
- **Middleware Pipeline**: Logging → Auth → RateLimit → Business Logic

## Example: Content Moderation Chain

```typescript
// Step 1: Pre-check (быстрая проверка)
export const preCheckConfig: EventConfig = {
  type: 'event',
  name: 'ContentPreCheck',
  subscribes: ['content.submitted'],
  emits: ['content.aicheck', 'content.rejected']
}

export const preCheckHandler = async (input, ctx) => {
  ctx.logger.info('Pre-checking content', { contentId: input.contentId })

  // Save to state for tracking
  await ctx.state.set(input.contentId, 'status', 'pre_check')

  // Quick checks
  const hasProhibitedWords = checkProhibitedWords(input.text)
  const isTooShort = input.text.length < 10

  if (hasProhibitedWords || isTooShort) {
    ctx.logger.warn('Content rejected in pre-check', {
      contentId: input.contentId,
      reason: hasProhibitedWords ? 'prohibited_words' : 'too_short'
    })

    await ctx.state.set(input.contentId, 'status', 'rejected')

    await ctx.emit({
      topic: 'content.rejected',
      data: {
        contentId: input.contentId,
        reason: hasProhibitedWords ? 'prohibited_words' : 'too_short',
        step: 'pre_check'
      }
    })
    return
  }

  // Pass to AI check
  ctx.logger.info('Pre-check passed, sending to AI', {
    contentId: input.contentId
  })

  await ctx.emit({
    topic: 'content.aicheck',
    data: { ...input, preCheckPassed: true }
  })
}

// Step 2: AI Analysis
export const aiCheckConfig: EventConfig = {
  type: 'event',
  name: 'ContentAICheck',
  subscribes: ['content.aicheck'],
  emits: ['content.humanreview', 'content.approved', 'content.rejected']
}

export const aiCheckHandler = async (input, ctx) => {
  ctx.logger.info('AI analyzing content', { contentId: input.contentId })

  await ctx.state.set(input.contentId, 'status', 'ai_check')

  // AI analysis
  const analysis = await analyzeWithAI(input.text)

  // Save analysis
  await ctx.state.set(input.contentId, 'ai_analysis', analysis)

  if (analysis.score < 0.3) {
    // Clearly bad content
    ctx.logger.warn('AI rejected content', {
      contentId: input.contentId,
      score: analysis.score
    })

    await ctx.state.set(input.contentId, 'status', 'rejected')

    await ctx.emit({
      topic: 'content.rejected',
      data: {
        contentId: input.contentId,
        reason: 'ai_rejected',
        score: analysis.score,
        step: 'ai_check'
      }
    })
    return
  }

  if (analysis.score > 0.8) {
    // Clearly good content - auto approve
    ctx.logger.info('AI approved content', {
      contentId: input.contentId,
      score: analysis.score
    })

    await ctx.state.set(input.contentId, 'status', 'approved')

    await ctx.emit({
      topic: 'content.approved',
      data: {
        contentId: input.contentId,
        approvedBy: 'ai',
        score: analysis.score
      }
    })
    return
  }

  // Uncertain - send to human review
  ctx.logger.info('Sending to human review', {
    contentId: input.contentId,
    score: analysis.score
  })

  await ctx.emit({
    topic: 'content.humanreview',
    data: {
      ...input,
      aiAnalysis: analysis,
      aiCheckPassed: true
    }
  })
}

// Step 3: Human Review (NOOP - external system)
export const humanReviewConfig: NoopConfig = {
  type: 'noop',
  name: 'ContentHumanReview',
  virtualSubscribes: ['content.humanreview'],
  virtualEmits: ['/api/content/review/callback']
}

// Step 4: Review Callback
export const reviewCallbackConfig: ApiRouteConfig = {
  type: 'api',
  name: 'ReviewCallback',
  path: '/content/review/callback',
  method: 'POST',
  emits: ['content.approved', 'content.rejected'],
  bodySchema: z.object({
    contentId: z.string(),
    decision: z.enum(['approve', 'reject']),
    reviewerId: z.string()
  })
}

export const reviewCallbackHandler = async (req, ctx) => {
  const { contentId, decision, reviewerId } = req.body

  ctx.logger.info('Human review completed', {
    contentId,
    decision,
    reviewerId
  })

  await ctx.state.set(contentId, 'status', decision === 'approve' ? 'approved' : 'rejected')

  const topic = decision === 'approve' ? 'content.approved' : 'content.rejected'

  await ctx.emit({
    topic,
    data: {
      contentId,
      approvedBy: 'human',
      reviewerId,
      reason: decision === 'reject' ? 'human_review' : undefined
    }
  })

  return { status: 200, body: { success: true } }
}
```

## Testing Chain

```bash
# Запуск ланцюжка
npx motia emit --topic "content.submitted" --message '{
  "contentId": "content123",
  "text": "This is test content for moderation",
  "userId": "user456"
}'

# Перевірити прогрес
npx motia state get "content123" "status"

# Переглянути логи всього ланцюжка
npx motia logs ContentPreCheck
npx motia logs ContentAICheck

# Симулювати human review callback
curl -X POST http://localhost:3000/content/review/callback \
  -H "Content-Type: application/json" \
  -d '{
    "contentId": "content123",
    "decision": "approve",
    "reviewerId": "reviewer789"
  }'
```

## Chain State Tracking

```typescript
// Utility для tracking chain progress
async function trackChainProgress(contentId, step, ctx) {
  const progress = await ctx.state.get(contentId, 'chain_progress') || []

  progress.push({
    step,
    timestamp: Date.now(),
    traceId: ctx.traceId
  })

  await ctx.state.set(contentId, 'chain_progress', progress)
}

// Use in each handler
export const handler = async (input, ctx) => {
  await trackChainProgress(input.contentId, 'pre_check', ctx)
  // ... rest of handler
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `event` (primarily)
**Complexity**: ⭐⭐⭐⭐☆ (Medium-High)
**Use Frequency**: ⭐⭐⭐⭐☆ (High)
