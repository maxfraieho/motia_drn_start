# Command Pattern для Motia API Steps

## Pattern Overview

Command Pattern інкапсулює запит як об'єкт, дозволяючи параметризувати клієнтів різними запитами, створювати черги команд, логувати операції та підтримувати undo.

## Motia-Specific Implementation

**API Step = Command**
- HTTP endpoint - інтерфейс для виклику команди
- `bodySchema` - параметри команди (валідація)
- `handler` - виконання команди
- `emits` - події після виконання (для undo/logging)

## Key Concepts

1. **Encapsulation**: Команда = об'єкт з усією необхідною інформацією
2. **Separation**: Відокремлення виклику від виконання
3. **Queuing**: Події дозволяють створювати черги команд
4. **Logging**: Structured logging всіх команд
5. **Reversibility**: Через events можна реалізувати undo

## Code Structure

```typescript
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'CommandName',
  path: '/resource/{id}',
  method: 'POST',  // або PUT, DELETE
  emits: ['command.executed'],
  bodySchema: z.object({
    // Параметри команди
    action: z.string(),
    params: z.any()
  }),
  responseSchema: {
    200: z.object({ success: z.boolean() }),
    400: z.object({ error: z.string() })
  }
}

export const handler: ApiRouteHandler = async (req, ctx) => {
  // 1. Валідація (автоматична через bodySchema)
  const command = req.body

  // 2. Логування команди
  ctx.logger.info('Executing command', {
    command: command.action,
    params: command.params
  })

  try {
    // 3. Виконання команди
    const result = await executeCommand(command)

    // 4. Збереження результату
    await ctx.state.set(ctx.traceId, 'commandResult', result)

    // 5. Емісія події про виконання
    await ctx.emit({
      topic: 'command.executed',
      data: { command, result, timestamp: Date.now() }
    })

    // 6. Response
    return {
      status: 200,
      body: { success: true, result }
    }

  } catch (error) {
    ctx.logger.error('Command failed', {
      error: error.message,
      command
    })

    return {
      status: 400,
      body: { error: error.message }
    }
  }
}
```

## Best Practices

1. **Validation**: Використовуй `bodySchema` для всіх параметрів
2. **Idempotency**: Команди повинні бути ідемпотентними
3. **Response Schema**: Визначай schema для всіх статусів
4. **Event Emission**: Емітуй події для audit trail
5. **State Persistence**: Зберігай результати для rollback

## Common Mistakes

❌ **No validation** параметрів
❌ **Side effects** без логування
❌ **Missing error handling**
❌ **Synchronous long operations** (використовуй events)
❌ **No idempotency** для критичних команд

## Use Cases

- **CRUD Operations**: Create, Update, Delete resources
- **Payment Commands**: ProcessPayment, RefundPayment
- **User Actions**: ActivateUser, DeactivateUser, ResetPassword
- **System Commands**: BackupDatabase, ClearCache
- **Batch Operations**: BulkUpdate, BulkDelete

## Example: Create Order Command

```typescript
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'CreateOrder',
  path: '/orders',
  method: 'POST',
  emits: ['order.created'],
  bodySchema: z.object({
    userId: z.string(),
    items: z.array(z.object({
      productId: z.string(),
      quantity: z.number().min(1)
    })),
    shippingAddress: z.string()
  }),
  responseSchema: {
    201: z.object({
      orderId: z.string(),
      total: z.number()
    }),
    400: z.object({ error: z.string() })
  }
}

export const handler: ApiRouteHandler = async (req, ctx) => {
  const orderData = req.body

  ctx.logger.info('Creating order', {
    userId: orderData.userId,
    itemCount: orderData.items.length
  })

  try {
    // 1. Валідація наявності товарів
    for (const item of orderData.items) {
      const available = await checkInventory(item.productId, item.quantity)
      if (!available) {
        return {
          status: 400,
          body: { error: `Product ${item.productId} not available` }
        }
      }
    }

    // 2. Розрахунок вартості
    const total = await calculateTotal(orderData.items)

    // 3. Створення замовлення
    const orderId = generateOrderId()
    const order = {
      orderId,
      ...orderData,
      total,
      status: 'pending',
      createdAt: new Date().toISOString()
    }

    // 4. Збереження в state
    await ctx.state.set(orderId, 'order', order)

    // 5. Емісія події для подальшої обробки
    await ctx.emit({
      topic: 'order.created',
      data: order
    })

    ctx.logger.info('Order created successfully', {
      orderId,
      total
    })

    return {
      status: 201,
      body: { orderId, total }
    }

  } catch (error) {
    ctx.logger.error('Failed to create order', {
      error: error.message,
      userId: orderData.userId
    })

    return {
      status: 400,
      body: { error: 'Failed to create order' }
    }
  }
}
```

## Testing

```bash
# Тест команди створення замовлення
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "items": [
      {"productId": "prod1", "quantity": 2},
      {"productId": "prod2", "quantity": 1}
    ],
    "shippingAddress": "123 Main St"
  }'

# Перевірити стан
npx motia state get "ORDER_ID" "order"

# Переглянути логи
npx motia logs CreateOrder
```

## Command History Pattern

```typescript
// API Command емітує події
await ctx.emit({
  topic: 'command.history',
  data: {
    commandType: 'CreateOrder',
    userId: req.body.userId,
    timestamp: Date.now(),
    params: req.body
  }
})

// Event Step логує історію команд
export const config: EventConfig = {
  type: 'event',
  name: 'LogCommandHistory',
  subscribes: ['command.history']
}

export const handler = async (input, ctx) => {
  await ctx.state.set('command-history', input.timestamp, input)
  ctx.logger.info('Command logged', { command: input.commandType })
}
```

## Undo Pattern

```typescript
// Команда емітує події з undo data
await ctx.emit({
  topic: 'command.executed',
  data: {
    commandId: 'cmd123',
    action: 'delete',
    undoData: previousState  // Дані для undo
  }
})

// Undo Command API
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'UndoCommand',
  path: '/commands/{commandId}/undo',
  method: 'POST'
}

export const handler = async (req, ctx) => {
  const commandId = req.pathParams.commandId
  const command = await ctx.state.get('commands', commandId)

  // Відновити попередній стан з undoData
  await restoreState(command.undoData)

  return { status: 200, body: { success: true } }
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `api`
**Complexity**: ⭐⭐⭐☆☆ (Medium)
**Use Frequency**: ⭐⭐⭐⭐⭐ (Very High)
