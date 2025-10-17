# Factory Pattern для Motia Steps

## Pattern Overview

Factory Pattern надає інтерфейс для створення об'єктів в суперкласі, але дозволяє підкласам змінювати тип створюваних об'єктів.

## Motia-Specific Implementation

В Motia Factory Pattern використовується для:
1. **Dynamic Event Creation** - створення різних типів подій
2. **Step Configuration** - генерація config на основі параметрів
3. **Response Building** - створення різних response objects

## Key Concepts

1. **Abstraction**: Приховування логіки створення
2. **Flexibility**: Легко додавати нові типи
3. **Consistency**: Єдиний спосіб створення об'єктів
4. **Validation**: Централізована валідація при створенні

## Code Structure

```typescript
// Factory interface
interface EventFactory {
  createEvent(type: string, data: any): Event
}

// Event types
type Event = {
  topic: string
  data: any
  metadata?: any
}

// Factory implementation
class MotiaEventFactory implements EventFactory {
  createEvent(type: string, data: any): Event {
    switch (type) {
      case 'user':
        return this.createUserEvent(data)
      case 'order':
        return this.createOrderEvent(data)
      case 'notification':
        return this.createNotificationEvent(data)
      default:
        throw new Error(`Unknown event type: ${type}`)
    }
  }

  private createUserEvent(data: any): Event {
    return {
      topic: `user.${data.action}`,
      data: {
        userId: data.userId,
        timestamp: Date.now(),
        ...data.payload
      },
      metadata: {
        source: 'user-service',
        version: '1.0'
      }
    }
  }

  private createOrderEvent(data: any): Event {
    return {
      topic: `order.${data.action}`,
      data: {
        orderId: data.orderId,
        userId: data.userId,
        timestamp: Date.now(),
        ...data.payload
      },
      metadata: {
        source: 'order-service',
        version: '1.0',
        priority: 'high'
      }
    }
  }

  private createNotificationEvent(data: any): Event {
    return {
      topic: `notification.${data.channel}`,
      data: {
        recipient: data.recipient,
        message: data.message,
        timestamp: Date.now()
      },
      metadata: {
        source: 'notification-service',
        version: '1.0',
        deliveryMethod: data.channel
      }
    }
  }
}

// Usage in Motia Step
export const config: ApiRouteConfig = {
  type: 'api',
  name: 'EventCreator',
  path: '/events',
  method: 'POST',
  emits: ['*'], // Can emit any event
  bodySchema: z.object({
    type: z.enum(['user', 'order', 'notification']),
    action: z.string(),
    data: z.any()
  })
}

export const handler = async (req, ctx) => {
  const { type, action, data } = req.body

  // Use factory to create event
  const factory = new MotiaEventFactory()
  const event = factory.createEvent(type, { action, ...data })

  ctx.logger.info('Event created via factory', {
    type,
    topic: event.topic
  })

  // Emit created event
  await ctx.emit(event)

  return {
    status: 201,
    body: {
      success: true,
      topic: event.topic
    }
  }
}
```

## Response Factory Pattern

```typescript
// Response factory for consistent API responses
class ApiResponseFactory {
  static success(data: any, message?: string) {
    return {
      status: 200,
      body: {
        success: true,
        message: message || 'Operation successful',
        data,
        timestamp: Date.now()
      }
    }
  }

  static created(data: any, resourceId: string) {
    return {
      status: 201,
      body: {
        success: true,
        message: 'Resource created',
        resourceId,
        data,
        timestamp: Date.now()
      }
    }
  }

  static error(message: string, code?: string) {
    return {
      status: 400,
      body: {
        success: false,
        error: message,
        code: code || 'BAD_REQUEST',
        timestamp: Date.now()
      }
    }
  }

  static notFound(resource: string) {
    return {
      status: 404,
      body: {
        success: false,
        error: `${resource} not found`,
        code: 'NOT_FOUND',
        timestamp: Date.now()
      }
    }
  }

  static serverError(error: Error) {
    return {
      status: 500,
      body: {
        success: false,
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        details: error.message,
        timestamp: Date.now()
      }
    }
  }
}

// Usage
export const handler = async (req, ctx) => {
  try {
    const user = await getUser(req.pathParams.userId)

    if (!user) {
      return ApiResponseFactory.notFound('User')
    }

    return ApiResponseFactory.success(user)

  } catch (error) {
    ctx.logger.error('Failed to get user', { error: error.message })
    return ApiResponseFactory.serverError(error)
  }
}
```

## Best Practices

1. **Single Responsibility**: Factory створює об'єкти, не обробляє логіку
2. **Validation**: Валідуй параметри при створенні
3. **Default Values**: Забезпеч sensible defaults
4. **Error Handling**: Обробляй невалідні типи
5. **Documentation**: Документуй доступні типи

## Common Mistakes

❌ **Factory becomes God Object** - занадто багато типів
❌ **No validation** при створенні
❌ **Inconsistent naming** між типами
❌ **Missing error handling**
❌ **Too complex** creation logic

## Use Cases

- **Event Creation**: Різні типи подій з єдиним interface
- **Response Building**: Консистентні API responses
- **Config Generation**: Динамічна генерація Step configs
- **DTO Creation**: Data Transfer Objects
- **Email Templates**: Різні типи email повідомлень

## Example: Notification Factory

```typescript
// Notification types
interface Notification {
  type: 'email' | 'sms' | 'push' | 'slack'
  recipient: string
  subject?: string
  body: string
  metadata: any
}

// Notification Factory
class NotificationFactory {
  static createEmail(data: {
    to: string
    subject: string
    body: string
    template?: string
  }): Notification {
    return {
      type: 'email',
      recipient: data.to,
      subject: data.subject,
      body: data.template
        ? this.applyTemplate(data.template, data.body)
        : data.body,
      metadata: {
        provider: 'sendgrid',
        timestamp: Date.now()
      }
    }
  }

  static createSMS(data: {
    to: string
    message: string
  }): Notification {
    // SMS has character limit
    const truncatedMessage = data.message.slice(0, 160)

    return {
      type: 'sms',
      recipient: data.to,
      body: truncatedMessage,
      metadata: {
        provider: 'twilio',
        timestamp: Date.now(),
        charCount: truncatedMessage.length
      }
    }
  }

  static createPush(data: {
    deviceToken: string
    title: string
    body: string
    badge?: number
  }): Notification {
    return {
      type: 'push',
      recipient: data.deviceToken,
      subject: data.title,
      body: data.body,
      metadata: {
        provider: 'firebase',
        timestamp: Date.now(),
        badge: data.badge || 0
      }
    }
  }

  static createSlack(data: {
    channel: string
    message: string
    blocks?: any[]
  }): Notification {
    return {
      type: 'slack',
      recipient: data.channel,
      body: data.message,
      metadata: {
        provider: 'slack',
        timestamp: Date.now(),
        blocks: data.blocks || []
      }
    }
  }

  private static applyTemplate(template: string, data: string): string {
    // Simple template engine
    return template.replace(/\{\{(\w+)\}\}/g, (_, key) => {
      return data[key] || ''
    })
  }
}

// Motia Step using Notification Factory
export const sendNotificationConfig: EventConfig = {
  type: 'event',
  name: 'SendNotification',
  subscribes: ['notification.send'],
  emits: ['notification.sent', 'notification.failed']
}

export const sendNotificationHandler = async (input, ctx) => {
  const { notificationType, recipientData, content } = input

  ctx.logger.info('Creating notification', {
    type: notificationType
  })

  try {
    // Use factory to create appropriate notification
    let notification: Notification

    switch (notificationType) {
      case 'email':
        notification = NotificationFactory.createEmail({
          to: recipientData.email,
          subject: content.subject,
          body: content.body,
          template: content.template
        })
        break

      case 'sms':
        notification = NotificationFactory.createSMS({
          to: recipientData.phone,
          message: content.body
        })
        break

      case 'push':
        notification = NotificationFactory.createPush({
          deviceToken: recipientData.deviceToken,
          title: content.subject,
          body: content.body,
          badge: content.badge
        })
        break

      case 'slack':
        notification = NotificationFactory.createSlack({
          channel: recipientData.channel,
          message: content.body,
          blocks: content.blocks
        })
        break

      default:
        throw new Error(`Unknown notification type: ${notificationType}`)
    }

    // Save notification for tracking
    await ctx.state.set(
      `notification_${Date.now()}`,
      'details',
      notification
    )

    // Send notification
    await sendNotification(notification)

    await ctx.emit({
      topic: 'notification.sent',
      data: {
        type: notification.type,
        recipient: notification.recipient
      }
    })

    ctx.logger.info('Notification sent successfully', {
      type: notification.type
    })

  } catch (error) {
    ctx.logger.error('Failed to send notification', {
      error: error.message,
      type: notificationType
    })

    await ctx.emit({
      topic: 'notification.failed',
      data: {
        type: notificationType,
        error: error.message
      }
    })
  }
}

// Helper function to send notification
async function sendNotification(notification: Notification) {
  switch (notification.type) {
    case 'email':
      await sendEmail(notification)
      break
    case 'sms':
      await sendSMS(notification)
      break
    case 'push':
      await sendPushNotification(notification)
      break
    case 'slack':
      await sendSlackMessage(notification)
      break
  }
}
```

## Testing

```bash
# Test notification factory
npx motia emit --topic "notification.send" --message '{
  "notificationType": "email",
  "recipientData": {
    "email": "user@example.com"
  },
  "content": {
    "subject": "Test Email",
    "body": "Hello from Motia!",
    "template": "welcome_email"
  }
}'

# Test SMS
npx motia emit --topic "notification.send" --message '{
  "notificationType": "sms",
  "recipientData": {
    "phone": "+1234567890"
  },
  "content": {
    "body": "Your verification code is: 123456"
  }
}'
```

## Abstract Factory Pattern

```typescript
// Abstract factory for different environments
interface ServiceFactory {
  createLogger(): Logger
  createDatabase(): Database
  createEmailService(): EmailService
}

class ProductionServiceFactory implements ServiceFactory {
  createLogger() {
    return new ProductionLogger()
  }
  createDatabase() {
    return new PostgresDatabase()
  }
  createEmailService() {
    return new SendGridService()
  }
}

class DevelopmentServiceFactory implements ServiceFactory {
  createLogger() {
    return new ConsoleLogger()
  }
  createDatabase() {
    return new InMemoryDatabase()
  }
  createEmailService() {
    return new MockEmailService()
  }
}

// Select factory based on environment
const factory = process.env.NODE_ENV === 'production'
  ? new ProductionServiceFactory()
  : new DevelopmentServiceFactory()

// Use in Motia Step
export const handler = async (req, ctx) => {
  const logger = factory.createLogger()
  const db = factory.createDatabase()
  const email = factory.createEmailService()

  // Use services...
}
```

---

**Pattern Type**: Creational
**Motia Step Type**: Any (utility pattern)
**Complexity**: ⭐⭐⭐☆☆ (Medium)
**Use Frequency**: ⭐⭐⭐⭐☆ (High)
