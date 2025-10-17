# Mediator Pattern для Motia Steps

## Pattern Overview

Mediator Pattern визначає об'єкт який інкапсулює взаємодію між групою об'єктів. Це сприяє слабкому зв'язку, не даючи об'єктам посилатися один на одного явно.

## Motia-Specific Implementation

**Motia Event System = Natural Mediator**

Event topics діють як mediator між Steps:
- Steps не знають один про одного
- Комунікація через emit/subscribe
- Mediator (event system) керує розподілом подій

**Explicit Mediator Step:**
```
Step1 → emit → MediatorStep → emit → Step2/Step3/Step4
```

## Key Concepts

1. **Centralized Communication**: Всі взаємодії через mediator
2. **Decoupling**: Steps не залежать один від одного
3. **Complex Routing**: Mediator вирішує куди направити event
4. **State Coordination**: Mediator може координувати state між Steps

## Code Structure

```typescript
// Mediator Step - coordinates interactions
export const mediatorConfig: EventConfig = {
  type: 'event',
  name: 'WorkflowMediator',
  subscribes: [
    'step1.completed',
    'step2.completed',
    'step3.completed'
  ],
  emits: [
    'step1.start',
    'step2.start',
    'step3.start',
    'workflow.completed'
  ]
}

export const mediatorHandler = async (input, ctx) => {
  const { topic, workflowId, data } = input

  ctx.logger.info('Mediator received event', { topic, workflowId })

  // Get workflow state
  const state = await ctx.state.get(workflowId, 'workflow_state') || {
    step1: 'pending',
    step2: 'pending',
    step3: 'pending'
  }

  // Update state based on received event
  if (topic === 'step1.completed') {
    state.step1 = 'completed'

    // Decision: start step2 and step3 in parallel
    await Promise.all([
      ctx.emit({ topic: 'step2.start', data: { workflowId, input: data.step1Result } }),
      ctx.emit({ topic: 'step3.start', data: { workflowId, input: data.step1Result } })
    ])
  }
  else if (topic === 'step2.completed') {
    state.step2 = 'completed'
  }
  else if (topic === 'step3.completed') {
    state.step3 = 'completed'
  }

  // Check if workflow completed
  if (state.step1 === 'completed' &&
      state.step2 === 'completed' &&
      state.step3 === 'completed') {
    ctx.logger.info('Workflow completed', { workflowId })

    await ctx.emit({
      topic: 'workflow.completed',
      data: { workflowId, finalState: state }
    })
  }

  // Save updated state
  await ctx.state.set(workflowId, 'workflow_state', state)
}

// Worker Steps - don't know about each other
export const step1Config: EventConfig = {
  type: 'event',
  name: 'WorkflowStep1',
  subscribes: ['step1.start'],
  emits: ['step1.completed']
}

export const step1Handler = async (input, ctx) => {
  ctx.logger.info('Step 1 executing', { workflowId: input.workflowId })

  const result = await doStep1Work(input)

  await ctx.emit({
    topic: 'step1.completed',
    data: {
      workflowId: input.workflowId,
      step1Result: result
    }
  })
}

// Similar for step2 and step3...
```

## Best Practices

1. **Single Mediator**: Один mediator для related Steps
2. **State Management**: Mediator зберігає coordination state
3. **Clear Events**: Явні назви топіків для communication
4. **Error Handling**: Mediator обробляє errors від всіх Steps
5. **Timeout**: Mediator встановлює timeout для workflows

## Common Mistakes

❌ **Too many mediators** - плутанина
❌ **Mediator becomes God Object** - занадто багато логіки
❌ **No state tracking** - втрата контексту
❌ **Direct communication** між Steps (bypassing mediator)
❌ **Missing error handling** в mediator

## Use Cases

- **Complex Workflows**: Координація багатьох Steps
- **Parallel Execution**: Запуск кількох Steps одночасно
- **Conditional Flows**: Різні шляхи залежно від умов
- **State Coordination**: Синхронізація state між Steps
- **Error Recovery**: Централізована обробка помилок

## Example: Order Fulfillment Mediator

```typescript
// Order Fulfillment Mediator
export const fulfillmentMediatorConfig: EventConfig = {
  type: 'event',
  name: 'OrderFulfillmentMediator',
  subscribes: [
    'order.created',
    'inventory.reserved',
    'payment.processed',
    'shipping.dispatched',
    'inventory.failed',
    'payment.failed',
    'shipping.failed'
  ],
  emits: [
    'inventory.reserve',
    'payment.process',
    'shipping.dispatch',
    'order.completed',
    'order.failed'
  ]
}

export const fulfillmentMediatorHandler = async (input, ctx) => {
  const { topic, orderId, data } = input

  ctx.logger.info('Mediator processing', { topic, orderId })

  // Get order state
  const orderState = await ctx.state.get(orderId, 'fulfillment') || {
    status: 'created',
    inventory: 'pending',
    payment: 'pending',
    shipping: 'pending',
    errors: []
  }

  try {
    switch (topic) {
      case 'order.created':
        // Start: reserve inventory
        await ctx.emit({
          topic: 'inventory.reserve',
          data: { orderId, items: data.items }
        })
        orderState.status = 'processing'
        orderState.inventory = 'processing'
        break

      case 'inventory.reserved':
        // Success: process payment
        orderState.inventory = 'completed'
        await ctx.emit({
          topic: 'payment.process',
          data: { orderId, amount: data.total }
        })
        orderState.payment = 'processing'
        break

      case 'inventory.failed':
        // Failure: cancel order
        orderState.inventory = 'failed'
        orderState.errors.push('Inventory not available')
        await handleOrderFailure(orderId, orderState, ctx)
        break

      case 'payment.processed':
        // Success: dispatch shipping
        orderState.payment = 'completed'
        await ctx.emit({
          topic: 'shipping.dispatch',
          data: { orderId, address: data.shippingAddress }
        })
        orderState.shipping = 'processing'
        break

      case 'payment.failed':
        // Failure: release inventory and cancel
        orderState.payment = 'failed'
        orderState.errors.push('Payment failed')
        await ctx.emit({
          topic: 'inventory.release',
          data: { orderId }
        })
        await handleOrderFailure(orderId, orderState, ctx)
        break

      case 'shipping.dispatched':
        // Success: order completed!
        orderState.shipping = 'completed'
        orderState.status = 'completed'

        await ctx.emit({
          topic: 'order.completed',
          data: {
            orderId,
            trackingNumber: data.trackingNumber
          }
        })

        ctx.logger.info('Order fulfillment completed', { orderId })
        break

      case 'shipping.failed':
        // Failure: refund payment and release inventory
        orderState.shipping = 'failed'
        orderState.errors.push('Shipping failed')

        await Promise.all([
          ctx.emit({ topic: 'payment.refund', data: { orderId } }),
          ctx.emit({ topic: 'inventory.release', data: { orderId } })
        ])

        await handleOrderFailure(orderId, orderState, ctx)
        break
    }

    // Save updated state
    await ctx.state.set(orderId, 'fulfillment', orderState)

  } catch (error) {
    ctx.logger.error('Mediator error', {
      error: error.message,
      orderId,
      topic
    })

    orderState.errors.push(error.message)
    await handleOrderFailure(orderId, orderState, ctx)
  }
}

async function handleOrderFailure(orderId, orderState, ctx) {
  orderState.status = 'failed'
  await ctx.state.set(orderId, 'fulfillment', orderState)

  await ctx.emit({
    topic: 'order.failed',
    data: {
      orderId,
      errors: orderState.errors,
      state: orderState
    }
  })

  ctx.logger.error('Order fulfillment failed', {
    orderId,
    errors: orderState.errors
  })
}

// Worker Steps (simplified)

// Inventory Worker
export const inventoryConfig: EventConfig = {
  type: 'event',
  name: 'InventoryWorker',
  subscribes: ['inventory.reserve'],
  emits: ['inventory.reserved', 'inventory.failed']
}

export const inventoryHandler = async (input, ctx) => {
  const { orderId, items } = input

  try {
    const reserved = await reserveInventory(items)

    await ctx.emit({
      topic: 'inventory.reserved',
      data: { orderId, reserved }
    })
  } catch (error) {
    await ctx.emit({
      topic: 'inventory.failed',
      data: { orderId, error: error.message }
    })
  }
}

// Payment Worker
export const paymentConfig: EventConfig = {
  type: 'event',
  name: 'PaymentWorker',
  subscribes: ['payment.process'],
  emits: ['payment.processed', 'payment.failed']
}

export const paymentHandler = async (input, ctx) => {
  const { orderId, amount } = input

  try {
    const transaction = await processPayment(amount)

    await ctx.emit({
      topic: 'payment.processed',
      data: {
        orderId,
        transactionId: transaction.id,
        total: amount
      }
    })
  } catch (error) {
    await ctx.emit({
      topic: 'payment.failed',
      data: { orderId, error: error.message }
    })
  }
}

// Shipping Worker
export const shippingConfig: EventConfig = {
  type: 'event',
  name: 'ShippingWorker',
  subscribes: ['shipping.dispatch'],
  emits: ['shipping.dispatched', 'shipping.failed']
}

export const shippingHandler = async (input, ctx) => {
  const { orderId, address } = input

  try {
    const shipment = await createShipment(orderId, address)

    await ctx.emit({
      topic: 'shipping.dispatched',
      data: {
        orderId,
        trackingNumber: shipment.trackingNumber
      }
    })
  } catch (error) {
    await ctx.emit({
      topic: 'shipping.failed',
      data: { orderId, error: error.message }
    })
  }
}
```

## Testing

```bash
# Start order fulfillment
npx motia emit --topic "order.created" --message '{
  "orderId": "order123",
  "items": [
    {"sku": "ITEM1", "quantity": 2}
  ],
  "shippingAddress": "123 Main St"
}'

# Monitor mediator state
npx motia state get "order123" "fulfillment"

# Check logs
npx motia logs OrderFulfillmentMediator
npx motia logs InventoryWorker
npx motia logs PaymentWorker
npx motia logs ShippingWorker
```

## Mediator State Visualization

```typescript
// API to visualize workflow state
export const stateConfig: ApiRouteConfig = {
  type: 'api',
  name: 'GetWorkflowState',
  path: '/orders/{orderId}/workflow',
  method: 'GET'
}

export const stateHandler = async (req, ctx) => {
  const { orderId } = req.pathParams

  const state = await ctx.state.get(orderId, 'fulfillment')

  return {
    status: 200,
    body: {
      orderId,
      currentState: state,
      diagram: generateMermaidDiagram(state)
    }
  }
}

function generateMermaidDiagram(state) {
  return `
graph LR
    Created -->|${state.inventory}| Inventory
    Inventory -->|${state.payment}| Payment
    Payment -->|${state.shipping}| Shipping
    Shipping --> Completed
  `
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `event` (coordinator)
**Complexity**: ⭐⭐⭐⭐⭐ (High)
**Use Frequency**: ⭐⭐⭐☆☆ (Medium)
