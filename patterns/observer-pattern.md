# Observer Pattern для Motia Event Steps

## Pattern Overview

Observer Pattern дозволяє об'єктам підписуватися на події та автоматично реагувати на зміни стану. В Motia це природньо реалізується через Event Steps.

## Motia-Specific Implementation

**Event Step = Observer**
- `subscribes` - на які події підписаний (Observable)
- `handler` - що робити при отриманні події (реакція Observer)
- `emits` - може емітувати нові події (каскадні реакції)

## Key Concepts

1. **Decoupling**: Publisher не знає про Subscribers
2. **Async by default**: Events обробляються асинхронно
3. **Scalability**: Багато Observers на одну подію
4. **Resilience**: Auto-retry при failure

## Code Structure

```typescript
export const config: EventConfig = {
  type: 'event',
  name: 'ObserverName',
  subscribes: ['source.event'],  // Observable topic
  emits: ['observer.completed'],  // Опціонально
  input: z.object({
    // Zod validation schema
    data: z.any()
  })
}

export const handler: EventHandler = async (input, ctx) => {
  // 1. Логування
  ctx.logger.info('Event received', { event: input })

  // 2. Бізнес-логіка (реакція Observer)
  const result = await processEvent(input)

  // 3. Збереження стану (опціонально)
  await ctx.state.set(ctx.traceId, 'result', result)

  // 4. Емісія нової події (опціонально)
  await ctx.emit({
    topic: 'observer.completed',
    data: { result }
  })
}
```

## Best Practices

1. **Validate Input**: Завжди використовуй Zod schema
2. **Idempotency**: Observer може отримати одну подію декілька разів
3. **Error Handling**: Логуй помилки, не ігноруй
4. **State Management**: Використовуй `ctx.state` для збереження прогресу
5. **Logging**: Structured logging з metadata

## Common Mistakes

❌ **Blocking operations** без timeout
❌ **Ignoring errors** в handler
❌ **Tight coupling** через direct function calls
❌ **No validation** вхідних даних
❌ **Heavy computation** без chunking

## Use Cases

- **User lifecycle**: created → confirmed → activated
- **Order processing**: placed → paid → shipped → delivered
- **Notification system**: event → notify via email/SMS/push
- **Data pipeline**: raw → validated → transformed → stored
- **Audit logging**: action → log → archive

## Example: User Registration Observer

```typescript
export const config: EventConfig = {
  type: 'event',
  name: 'SendWelcomeEmail',
  subscribes: ['user.registered'],
  emits: ['email.sent'],
  input: z.object({
    userId: z.string(),
    email: z.string().email(),
    name: z.string()
  })
}

export const handler: EventHandler = async (input, ctx) => {
  try {
    ctx.logger.info('Sending welcome email', {
      userId: input.userId,
      email: input.email
    })

    // Відправка email
    await sendEmail({
      to: input.email,
      subject: 'Welcome!',
      body: `Hello ${input.name}!`
    })

    // Збереження статусу
    await ctx.state.set(input.userId, 'welcomeEmailSent', true)

    // Емісія події про успіх
    await ctx.emit({
      topic: 'email.sent',
      data: {
        userId: input.userId,
        emailType: 'welcome'
      }
    })

    ctx.logger.info('Welcome email sent successfully')

  } catch (error) {
    ctx.logger.error('Failed to send welcome email', {
      error: error.message,
      userId: input.userId
    })
    throw error // Auto-retry
  }
}
```

## Testing

```bash
# Емітнути тестову подію
npx motia emit --topic "user.registered" --message '{
  "userId": "123",
  "email": "test@example.com",
  "name": "John Doe"
}'

# Перевірити логи
npx motia logs SendWelcomeEmail

# Перевірити стан
npx motia state get "123" "welcomeEmailSent"
```

## Multiple Observers Pattern

```typescript
// Observer 1: Welcome Email
config = {
  type: 'event',
  name: 'SendWelcomeEmail',
  subscribes: ['user.registered']
}

// Observer 2: Create Profile
config = {
  type: 'event',
  name: 'CreateUserProfile',
  subscribes: ['user.registered']
}

// Observer 3: Analytics
config = {
  type: 'event',
  name: 'TrackUserSignup',
  subscribes: ['user.registered']
}

// Всі 3 Observers обробляють одну подію паралельно
```

---

**Pattern Type**: Behavioral
**Motia Step Type**: `event`
**Complexity**: ⭐⭐☆☆☆ (Easy)
**Use Frequency**: ⭐⭐⭐⭐⭐ (Very High)
