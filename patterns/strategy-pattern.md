# Strategy Pattern для Motia Steps

## Pattern Overview

Strategy Pattern визначає сімейство алгоритмів, інкапсулює кожен з них і робить їх взаємозамінними. Стратегію можна змінити незалежно від клієнтів, які її використовують.

## Motia-Specific Implementation

**Варіанти реалізації:**
1. **Conditional Logic** - вибір стратегії в handler
2. **Multiple Event Steps** - різні Steps для різних стратегій
3. **Dynamic Emit** - емісія різних топіків залежно від стратегії

## Key Concepts

1. **Flexibility**: Легко додавати нові стратегії
2. **Isolation**: Кожна стратегія незалежна
3. **Runtime Selection**: Вибір стратегії під час виконання
4. **Testability**: Легко тестувати кожну стратегію окремо

## Code Structure - Variant 1: Conditional

```typescript
export const config: EventConfig = {
  type: 'event',
  name: 'ProcessPayment',
  subscribes: ['payment.requested'],
  emits: ['payment.processed'],
  input: z.object({
    amount: z.number(),
    paymentMethod: z.enum(['credit_card', 'paypal', 'crypto'])
  })
}

export const handler: EventHandler = async (input, ctx) => {
  ctx.logger.info('Processing payment', {
    method: input.paymentMethod,
    amount: input.amount
  })

  // Strategy Selection
  let result
  switch (input.paymentMethod) {
    case 'credit_card':
      result = await processCreditCard(input, ctx)
      break
    case 'paypal':
      result = await processPayPal(input, ctx)
      break
    case 'crypto':
      result = await processCrypto(input, ctx)
      break
    default:
      throw new Error(`Unknown payment method: ${input.paymentMethod}`)
  }

  await ctx.emit({
    topic: 'payment.processed',
    data: result
  })
}

// Strategy Implementations
async function processCreditCard(input, ctx) {
  ctx.logger.info('Using credit card strategy')
  // Credit card specific logic
  return { status: 'success', transactionId: 'cc_123' }
}

async function processPayPal(input, ctx) {
  ctx.logger.info('Using PayPal strategy')
  // PayPal specific logic
  return { status: 'success', transactionId: 'pp_456' }
}

async function processCrypto(input, ctx) {
  ctx.logger.info('Using crypto strategy')
  // Crypto specific logic
  return { status: 'success', transactionId: 'crypto_789' }
}
```

## Code Structure - Variant 2: Separate Steps

```typescript
// Main Step: Route to strategy
export const config: EventConfig = {
  type: 'event',
  name: 'PaymentRouter',
  subscribes: ['payment.requested'],
  emits: [
    'payment.creditcard',
    'payment.paypal',
    'payment.crypto'
  ]
}

export const handler = async (input, ctx) => {
  // Emit to specific strategy based on payment method
  const topic = `payment.${input.paymentMethod}`

  await ctx.emit({
    topic,
    data: input
  })
}

// Strategy 1: Credit Card Step
export const creditCardConfig: EventConfig = {
  type: 'event',
  name: 'ProcessCreditCard',
  subscribes: ['payment.creditcard'],
  emits: ['payment.processed']
}

export const creditCardHandler = async (input, ctx) => {
  // Credit card specific implementation
  ctx.logger.info('Processing credit card payment')
  const result = await chargeCreditCard(input)

  await ctx.emit({
    topic: 'payment.processed',
    data: result
  })
}

// Strategy 2: PayPal Step
export const paypalConfig: EventConfig = {
  type: 'event',
  name: 'ProcessPayPal',
  subscribes: ['payment.paypal'],
  emits: ['payment.processed']
}

export const paypalHandler = async (input, ctx) => {
  // PayPal specific implementation
  ctx.logger.info('Processing PayPal payment')
  const result = await chargePayPal(input)

  await ctx.emit({
    topic: 'payment.processed',
    data: result
  })
}
```

## Best Practices

1. **Validation**: Валідуй strategy type в schema
2. **Error Handling**: Обробляй помилки для кожної стратегії
3. **Logging**: Логуй яка стратегія використовується
4. **Fallback**: Мій fallback стратегію для unknown types
5. **State**: Зберігай вибрану стратегію в state

## Common Mistakes

❌ **Tight coupling** між стратегіями
❌ **Missing validation** для strategy type
❌ **No default strategy** для невідомих типів
❌ **Duplicate logic** між стратегіями
❌ **Hard to add new strategies** через жорстку структуру

## Use Cases

- **Payment Processing**: Різні методи оплати
- **Notification Delivery**: Email, SMS, Push, Slack
- **Data Export**: CSV, JSON, XML, PDF
- **Authentication**: OAuth, JWT, API Key, Basic Auth
- **Compression**: ZIP, GZIP, BROTLI
- **Storage**: S3, GCS, Azure Blob, Local FS

## Example: Notification Strategy

```typescript
export const config: EventConfig = {
  type: 'event',
  name: 'SendNotification',
  subscribes: ['notification.send'],
  emits: ['notification.sent'],
  input: z.object({
    userId: z.string(),
    message: z.string(),
    channel: z.enum(['email', 'sms', 'push', 'slack'])
  })
}

export const handler: EventHandler = async (input, ctx) => {
  ctx.logger.info('Sending notification', {
    userId: input.userId,
    channel: input.channel
  })

  // Get user preferences
  const userPrefs = await ctx.state.get(input.userId, 'preferences')

  // Strategy Selection
  try {
    let result
    switch (input.channel) {
      case 'email':
        result = await sendEmailStrategy(input, userPrefs, ctx)
        break
      case 'sms':
        result = await sendSMSStrategy(input, userPrefs, ctx)
        break
      case 'push':
        result = await sendPushStrategy(input, userPrefs, ctx)
        break
      case 'slack':
        result = await sendSlackStrategy(input, userPrefs, ctx)
        break
      default:
        // Fallback to email
        ctx.logger.warn('Unknown channel, using email fallback', {
          channel: input.channel
        })
        result = await sendEmailStrategy(input, userPrefs, ctx)
    }

    // Log success
    await ctx.state.set(input.userId, `last_notification_${input.channel}`, {
      timestamp: Date.now(),
      message: input.message
    })

    await ctx.emit({
      topic: 'notification.sent',
      data: { userId: input.userId, channel: input.channel, result }
    })

    ctx.logger.info('Notification sent successfully', {
      userId: input.userId,
      channel: input.channel
    })

  } catch (error) {
    ctx.logger.error('Failed to send notification', {
      error: error.message,
      userId: input.userId,
      channel: input.channel
    })
    throw error
  }
}

// Email Strategy
async function sendEmailStrategy(input, userPrefs, ctx) {
  const emailAddress = userPrefs?.email || input.userId
  ctx.logger.info('Using email strategy', { to: emailAddress })

  // Send email via service
  await emailService.send({
    to: emailAddress,
    subject: 'Notification',
    body: input.message
  })

  return { method: 'email', sent: true }
}

// SMS Strategy
async function sendSMSStrategy(input, userPrefs, ctx) {
  const phoneNumber = userPrefs?.phone
  if (!phoneNumber) {
    throw new Error('Phone number not available')
  }

  ctx.logger.info('Using SMS strategy', { to: phoneNumber })

  await smsService.send({
    to: phoneNumber,
    message: input.message
  })

  return { method: 'sms', sent: true }
}

// Push Strategy
async function sendPushStrategy(input, userPrefs, ctx) {
  const deviceTokens = userPrefs?.deviceTokens || []
  if (deviceTokens.length === 0) {
    throw new Error('No device tokens available')
  }

  ctx.logger.info('Using push strategy', { tokens: deviceTokens.length })

  await pushService.send({
    tokens: deviceTokens,
    title: 'Notification',
    body: input.message
  })

  return { method: 'push', sent: true }
}

// Slack Strategy
async function sendSlackStrategy(input, userPrefs, ctx) {
  const slackChannel = userPrefs?.slackChannel || '#general'

  ctx.logger.info('Using Slack strategy', { channel: slackChannel })

  await slackService.send({
    channel: slackChannel,
    text: input.message
  })

  return { method: 'slack', sent: true }
}
```

## Testing

```bash
# Тест email strategy
npx motia emit --topic "notification.send" --message '{
  "userId": "user123",
  "message": "Hello World",
  "channel": "email"
}'

# Тест SMS strategy
npx motia emit --topic "notification.send" --message '{
  "userId": "user123",
  "message": "Hello World",
  "channel": "sms"
}'

# Перевірити логи
npx motia logs SendNotification
```

## Dynamic Strategy Loading

```typescript
// Strategy registry
const strategies = {
  email: sendEmailStrategy,
  sms: sendSMSStrategy,
  push: sendPushStrategy,
  slack: sendSlackStrategy
}

export const handler = async (input, ctx) => {
  // Get strategy function dynamically
  const strategyFn = strategies[input.channel]

  if (!strategyFn) {
    ctx.logger.warn('Strategy not found, using default')
    strategyFn = strategies.email // default
  }

  // Execute strategy
  const result = await strategyFn(input, ctx)

  return result
}
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `event` or `api`
**Complexity**: ⭐⭐⭐☆☆ (Medium)
**Use Frequency**: ⭐⭐⭐⭐☆ (High)
