# State Pattern для Motia Steps

## Pattern Overview

State Pattern дозволяє об'єкту змінювати свою поведінку залежно від внутрішнього стану. Об'єкт виглядає ніби змінив свій клас.

## Motia-Specific Implementation

Використовуй `ctx.state` для збереження поточного стану та різні Event Steps для обробки переходів між станами.

**State Machine Flow:**
```
initial → processing → completed
         ↓
      failed → retry → processing
```

## Key Concepts

1. **State Storage**: Використовуй `ctx.state.set()` для збереження поточного стану
2. **State Transitions**: Кожен перехід = event emission
3. **State-Specific Logic**: Різна логіка для різних станів
4. **Validation**: Валідація дозволених переходів

## Code Structure

```typescript
// State machine definition
const VALID_TRANSITIONS = {
  'initial': ['processing'],
  'processing': ['completed', 'failed'],
  'failed': ['retry', 'cancelled'],
  'retry': ['processing'],
  'completed': [],
  'cancelled': []
}

// Main state handler
export const config: EventConfig = {
  type: 'event',
  name: 'OrderStateMachine',
  subscribes: ['order.state.transition'],
  emits: [
    'order.state.processing',
    'order.state.completed',
    'order.state.failed',
    'order.state.cancelled'
  ],
  input: z.object({
    orderId: z.string(),
    newState: z.string(),
    data: z.any().optional()
  })
}

export const handler = async (input, ctx) => {
  const { orderId, newState, data } = input

  // Get current state
  const currentState = await ctx.state.get(orderId, 'state') || 'initial'

  ctx.logger.info('State transition requested', {
    orderId,
    from: currentState,
    to: newState
  })

  // Validate transition
  if (!VALID_TRANSITIONS[currentState]?.includes(newState)) {
    ctx.logger.error('Invalid state transition', {
      orderId,
      from: currentState,
      to: newState
    })
    throw new Error(`Invalid transition: ${currentState} → ${newState}`)
  }

  // Save new state
  await ctx.state.set(orderId, 'state', newState)
  await ctx.state.set(orderId, 'stateHistory', {
    from: currentState,
    to: newState,
    timestamp: Date.now(),
    data
  })

  // Emit state-specific event
  await ctx.emit({
    topic: `order.state.${newState}`,
    data: { orderId, ...data }
  })

  ctx.logger.info('State transitioned successfully', {
    orderId,
    newState
  })
}
```

## State Handlers

```typescript
// Processing State Handler
export const processingConfig: EventConfig = {
  type: 'event',
  name: 'OrderProcessingState',
  subscribes: ['order.state.processing']
}

export const processingHandler = async (input, ctx) => {
  ctx.logger.info('Order in processing state', { orderId: input.orderId })

  try {
    // State-specific logic
    await processOrder(input.orderId)

    // Transition to completed
    await ctx.emit({
      topic: 'order.state.transition',
      data: {
        orderId: input.orderId,
        newState: 'completed'
      }
    })
  } catch (error) {
    ctx.logger.error('Processing failed', {
      orderId: input.orderId,
      error: error.message
    })

    // Transition to failed
    await ctx.emit({
      topic: 'order.state.transition',
      data: {
        orderId: input.orderId,
        newState: 'failed',
        data: { error: error.message }
      }
    })
  }
}

// Completed State Handler
export const completedConfig: EventConfig = {
  type: 'event',
  name: 'OrderCompletedState',
  subscribes: ['order.state.completed']
}

export const completedHandler = async (input, ctx) => {
  ctx.logger.info('Order completed', { orderId: input.orderId })

  // Final state actions
  await sendConfirmationEmail(input.orderId)
  await updateAnalytics(input.orderId, 'completed')

  // Mark as final
  await ctx.state.set(input.orderId, 'final', true)
}

// Failed State Handler
export const failedConfig: EventConfig = {
  type: 'event',
  name: 'OrderFailedState',
  subscribes: ['order.state.failed']
}

export const failedHandler = async (input, ctx) => {
  ctx.logger.warn('Order failed', { orderId: input.orderId })

  const retryCount = await ctx.state.get(input.orderId, 'retryCount') || 0

  if (retryCount < 3) {
    // Transition to retry
    await ctx.state.set(input.orderId, 'retryCount', retryCount + 1)

    await ctx.emit({
      topic: 'order.state.transition',
      data: {
        orderId: input.orderId,
        newState: 'retry'
      }
    })
  } else {
    // Too many retries, cancel
    await ctx.emit({
      topic: 'order.state.transition',
      data: {
        orderId: input.orderId,
        newState: 'cancelled',
        data: { reason: 'max_retries_exceeded' }
      }
    })
  }
}
```

## Best Practices

1. **Define Valid Transitions**: Явно визначай дозволені переходи
2. **Validate Transitions**: Перевіряй чи можливий перехід
3. **State History**: Зберігай історію переходів
4. **Idempotency**: Повторний перехід в той самий стан = no-op
5. **Final States**: Позначай фінальні стани

## Common Mistakes

❌ **No validation** переходів
❌ **Lost state** через некоректне збереження
❌ **Circular transitions** без exit condition
❌ **Missing error states**
❌ **No state history** для debugging

## Use Cases

- **Order Lifecycle**: pending → confirmed → shipped → delivered
- **User Onboarding**: registered → verified → onboarded → active
- **Document Workflow**: draft → review → approved → published
- **Payment Status**: initiated → processing → succeeded/failed
- **Task Management**: todo → in_progress → review → done

## Example: Document Workflow

```typescript
// Document states
type DocState =
  | 'draft'
  | 'review'
  | 'approved'
  | 'rejected'
  | 'published'
  | 'archived'

const DOC_TRANSITIONS: Record<DocState, DocState[]> = {
  draft: ['review'],
  review: ['approved', 'rejected', 'draft'],
  approved: ['published'],
  rejected: ['draft', 'archived'],
  published: ['archived'],
  archived: []
}

// API to trigger transition
export const transitionConfig: ApiRouteConfig = {
  type: 'api',
  name: 'TransitionDocument',
  path: '/documents/{docId}/transition',
  method: 'POST',
  emits: ['document.transition'],
  bodySchema: z.object({
    newState: z.enum(['draft', 'review', 'approved', 'rejected', 'published', 'archived']),
    comment: z.string().optional()
  })
}

export const transitionHandler = async (req, ctx) => {
  const { docId } = req.pathParams
  const { newState, comment } = req.body

  const currentState = await ctx.state.get(docId, 'state') as DocState || 'draft'

  // Validate transition
  if (!DOC_TRANSITIONS[currentState]?.includes(newState)) {
    return {
      status: 400,
      body: {
        error: 'Invalid transition',
        from: currentState,
        to: newState,
        allowed: DOC_TRANSITIONS[currentState]
      }
    }
  }

  // Emit transition event
  await ctx.emit({
    topic: 'document.transition',
    data: {
      docId,
      fromState: currentState,
      toState: newState,
      comment,
      userId: req.headers['x-user-id'],
      timestamp: Date.now()
    }
  })

  return {
    status: 200,
    body: {
      success: true,
      state: newState
    }
  }
}

// Transition processor
export const processorConfig: EventConfig = {
  type: 'event',
  name: 'DocumentTransitionProcessor',
  subscribes: ['document.transition'],
  emits: [
    'document.review_requested',
    'document.approved',
    'document.rejected',
    'document.published'
  ]
}

export const processorHandler = async (input, ctx) => {
  const { docId, fromState, toState, comment, userId } = input

  ctx.logger.info('Processing document transition', {
    docId,
    from: fromState,
    to: toState
  })

  // Update state
  await ctx.state.set(docId, 'state', toState)

  // Add to history
  const history = await ctx.state.get(docId, 'history') || []
  history.push({
    from: fromState,
    to: toState,
    userId,
    comment,
    timestamp: Date.now()
  })
  await ctx.state.set(docId, 'history', history)

  // State-specific actions
  switch (toState) {
    case 'review':
      await ctx.emit({
        topic: 'document.review_requested',
        data: { docId, reviewerIds: await getReviewers(docId) }
      })
      break

    case 'approved':
      await ctx.emit({
        topic: 'document.approved',
        data: { docId, approvedBy: userId }
      })
      break

    case 'rejected':
      await ctx.emit({
        topic: 'document.rejected',
        data: { docId, rejectedBy: userId, reason: comment }
      })
      break

    case 'published':
      await ctx.emit({
        topic: 'document.published',
        data: { docId, publishedBy: userId }
      })
      break
  }

  ctx.logger.info('Document transition completed', {
    docId,
    newState: toState
  })
}
```

## Testing

```bash
# Create document (initial state: draft)
curl -X POST http://localhost:3000/documents/{docId}/transition \
  -H "Content-Type: application/json" \
  -H "x-user-id: user123" \
  -d '{"newState": "review"}'

# Check current state
npx motia state get "{docId}" "state"

# Check transition history
npx motia state get "{docId}" "history"

# Try invalid transition (should fail)
curl -X POST http://localhost:3000/documents/{docId}/transition \
  -d '{"newState": "published"}' # Can't go draft → published
```

## State Machine Visualization

```typescript
// Generate state diagram
export const diagramConfig: ApiRouteConfig = {
  type: 'api',
  name: 'GetStateDiagram',
  path: '/documents/states/diagram',
  method: 'GET'
}

export const diagramHandler = async (req, ctx) => {
  // Generate Mermaid diagram
  const diagram = `
stateDiagram-v2
    [*] --> draft
    draft --> review
    review --> approved
    review --> rejected
    review --> draft
    approved --> published
    rejected --> draft
    rejected --> archived
    published --> archived
    archived --> [*]
  `

  return {
    status: 200,
    body: { diagram }
  }
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `event` + `api`
**Complexity**: ⭐⭐⭐⭐☆ (Medium-High)
**Use Frequency**: ⭐⭐⭐⭐☆ (High)
