# Motia Design Patterns

Колекція design patterns оптимізованих для Motia framework.

## Доступні Patterns

### Behavioral Patterns

| Pattern | File | Difficulty | Use Frequency | Step Type |
|---------|------|------------|---------------|-----------|
| **Observer** | [observer-pattern.md](observer-pattern.md) | ⭐⭐☆☆☆ Easy | ⭐⭐⭐⭐⭐ Very High | `event` |
| **Command** | [command-pattern.md](command-pattern.md) | ⭐⭐⭐☆☆ Medium | ⭐⭐⭐⭐⭐ Very High | `api` |
| **Strategy** | [strategy-pattern.md](strategy-pattern.md) | ⭐⭐⭐☆☆ Medium | ⭐⭐⭐⭐☆ High | `event`/`api` |
| **Chain of Responsibility** | [chain-of-responsibility-pattern.md](chain-of-responsibility-pattern.md) | ⭐⭐⭐⭐☆ Medium-High | ⭐⭐⭐⭐☆ High | `event` |
| **State** | [state-pattern.md](state-pattern.md) | ⭐⭐⭐⭐☆ Medium-High | ⭐⭐⭐⭐☆ High | `event`+`api` |
| **Template Method** | [template-method-pattern.md](template-method-pattern.md) | ⭐⭐⭐☆☆ Medium | ⭐⭐⭐☆☆ Medium | Any |
| **Mediator** | [mediator-pattern.md](mediator-pattern.md) | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐☆☆ Medium | `event` |

### Creational Patterns

| Pattern | File | Difficulty | Use Frequency | Step Type |
|---------|------|------------|---------------|-----------|
| **Factory** | [factory-pattern.md](factory-pattern.md) | ⭐⭐⭐☆☆ Medium | ⭐⭐⭐⭐☆ High | Any |

## Швидкий старт

### Використання pattern з Claude CLI

```bash
# Базовий промпт + pattern
claude --append-system-prompt "$(cat CLAUDE-CORE.md)" \
       --append-system-prompt "$(cat patterns/observer-pattern.md)" \
       -p "Створи Event Step для обробки реєстрації користувачів"
```

### Повний workflow

```bash
# 1. Створити опис кроку з pattern
./create-step-description.sh user-registration event observer \
  "Обробляє реєстрацію користувачів та відправляє welcome email"

# 2. Згенерувати код
./motia-claude-workflow.sh generate \
  step-descriptions/user-registration-description.md \
  observer
```

## Pattern Selection Guide

### За типом завдання:

- **Background processing** → Observer Pattern
- **API endpoints** → Command Pattern
- **Multiple algorithms** → Strategy Pattern
- **Sequential processing** → Chain of Responsibility
- **State machines** → State Pattern
- **Complex coordination** → Mediator Pattern
- **Object creation** → Factory Pattern
- **Code reuse** → Template Method Pattern

### За складністю проекту:

**Простий проект** (1-5 Steps):
- Observer
- Command
- Factory

**Середній проект** (5-15 Steps):
- + Strategy
- + Chain of Responsibility
- + Template Method

**Складний проект** (15+ Steps):
- + State
- + Mediator

## Best Practices

1. **Один Pattern на Step**: Не mix кілька patterns в одному Step
2. **Почни з простого**: Observer та Command для більшості випадків
3. **Документуй вибір**: Чому обрано цей pattern
4. **Тестуй окремо**: Кожен pattern має свої test cases
5. **Використовуй приклади**: Кожен pattern має робочий приклад

## Структура Pattern файлу

Кожен pattern файл містить:

```markdown
# Pattern Name

## Pattern Overview
- Загальний опис pattern

## Motia-Specific Implementation
- Як реалізувати в Motia

## Key Concepts
- Ключові концепції

## Code Structure
- Шаблон коду

## Best Practices
- Рекомендації

## Common Mistakes
- Поширені помилки

## Use Cases
- Типові випадки використання

## Example
- Повний робочий приклад

## Testing
- Як тестувати

---
Pattern Type: [Behavioral/Creational/Structural]
Step Type: [api/event/cron]
Complexity: ⭐⭐⭐☆☆
Use Frequency: ⭐⭐⭐⭐☆
```

## Комбінування Patterns

Деякі patterns добре працюють разом:

### Observer + Factory
```typescript
// Factory створює різні типи подій
// Observer обробляє створені події
```

### Command + Chain of Responsibility
```typescript
// Command створює запит
// Chain обробляє через кілька Steps
```

### State + Mediator
```typescript
// State управляє станами
// Mediator координує переходи
```

### Strategy + Template Method
```typescript
// Template визначає структуру
// Strategy реалізує варіації
```

## Додаткові ресурси

- **CLAUDE-CORE.md** - Базові концепції Motia
- **Claude.md** - Повна документація Motia (678KB)
- **usage-examples.md** - Приклади використання
- **motia-claude-workflow.sh** - Скрипт автоматизації

## Contributing

Якщо ви створили новий pattern:

1. Використовуйте шаблон structure вище
2. Додайте робочий приклад
3. Додайте тести
4. Оновіть цей README
5. Додайте до списку patterns в скриптах

## License

Ці patterns створені для використання з Motia framework.

---

**Version**: 1.0
**Created**: 2025-10-09
**Last Updated**: 2025-10-09
