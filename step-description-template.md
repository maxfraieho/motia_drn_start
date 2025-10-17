# Генератор опису кроку Motia для Claude CLI

## 🎯 Концепція тристороннього промпту

Для створення повного опису кроку з ДРАКОН діаграмами та структурою папок, використовується **триступенева архітектура**:

1. **CLAUDE.md** - Базовий Motia context (загальні знання)
2. **pattern-specific.md** - Патерн-специфічний промпт (Observer, Command, тощо)
3. **step-description.md** - Повний опис конкретного кроку з структурою

---

## 📁 Шаблон step-description.md

```markdown
# {step-name} - Повний опис кроку Motia

## 🏗️ Структура кроку
```
{step-name}/
├── handler.ts                   # Логіка кроку
├── config.json                  # Конфігурація Motia
├── schema.json                  # Схема валідації
├── README.md                    # Документація
├── diagrams/                    # ДРАКОН діаграми кроку
│   ├── logic-flow.drakon        # Основна логіка
│   ├── error-handling.drakon    # Обробка помилок
│   ├── data-processing.drakon   # Обробка даних
│   └── state-transitions.drakon # Переходи станів
├── tests/                       # Unit та integration тести
│   ├── unit/
│   │   └── handler.test.ts
│   └── integration/
│       └── flow.test.ts
└── docs/                        # Додаткова документація
    ├── api.md                   # API документація
    ├── examples.md              # Приклади використання
    └── troubleshooting.md       # Розв'язання проблем
```

## 📋 Специфікація кроку

### Базова інформація
- **Тип кроку**: {api|event|cron|stream}
- **Патерн проектування**: {observer|command|strategy|chain|template|state|mediator|factory}
- **Мова програмування**: {typescript|python|ruby}
- **Основна функція**: {описати що робить крок}

### Конфігурація (config.json)
```json
{
  "type": "{step-type}",
  "name": "{step-name}",
  "description": "{опис функціональності}",
  "subscribes": ["{event-topics}"],
  "emits": ["{emitted-events}"],
  "path": "{api-path}",
  "method": "{http-method}",
  "flows": ["{flow-names}"],
  "compatibility_date": "2024-01-01"
}
```

### Схема валідації (schema.json)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "{input-field}": {
      "type": "{type}",
      "description": "{опис поля}"
    }
  },
  "required": ["{required-fields}"]
}
```

## 🎨 ДРАКОН діаграми

### logic-flow.drakon - Основна логіка
```
ЗАГОЛОВОК: {step-name} - Основний потік
├─ ПОЧАТОК
├─ ДІЯ: Отримати вхідні дані
├─ УМОВА: Дані валідні?
│  ├─ ТАК → ДІЯ: Обробити дані
│  └─ НІ → ДІЯ: Повернути помилку валідації
├─ ДІЯ: Виконати бізнес-логіку
├─ ДІЯ: Емітувати події
└─ КІНЕЦЬ
```

### error-handling.drakon - Обробка помилок
```
ЗАГОЛОВОК: {step-name} - Обробка помилок
├─ ПОЧАТОК
├─ УМОВА: Тип помилки?
│  ├─ Валідація → ДІЯ: Логувати як WARNING
│  ├─ Бізнес-логіка → ДІЯ: Логувати як ERROR
│  └─ Система → ДІЯ: Логувати як CRITICAL
├─ ДІЯ: Сформувати response
└─ КІНЕЦЬ
```

### data-processing.drakon - Обробка даних
```
ЗАГОЛОВОК: {step-name} - Обробка даних
├─ ПОЧАТОК
├─ ДІЯ: Парсинг вхідних даних
├─ ДІЯ: Трансформація даних
├─ УМОВА: Потрібно зберегти стан?
│  ├─ ТАК → ДІЯ: ctx.state.set()
│  └─ НІ → Продовжити
├─ ДІЯ: Підготувати вихідні дані
└─ КІНЕЦЬ
```

### state-transitions.drakon - Переходи станів
```
ЗАГОЛОВОК: {step-name} - Стани
├─ ПОЧАТОК
├─ УМОВА: Поточний стан?
│  ├─ INITIAL → ДІЯ: Встановити PROCESSING
│  ├─ PROCESSING → ДІЯ: Встановити COMPLETED/FAILED
│  └─ COMPLETED → ДІЯ: Встановити ARCHIVED
└─ КІНЕЦЬ
```

## 🔧 Реалізація

### handler.ts
```typescript
import { {HandlerType}, FlowContext } from "motia";

export const config = {
  // конфігурація з config.json
};

export const handler: {HandlerType}<{InputType}, {EmitType}> = async (
  {input-params}, 
  ctx: FlowContext<{EmitType}>
) => {
  // Реалізація відповідно до ДРАКОН діаграм
  
  // 1. Валідація (logic-flow.drakon)
  // 2. Обробка даних (data-processing.drakon)  
  // 3. Обробка помилок (error-handling.drakon)
  // 4. Управління станом (state-transitions.drakon)
  
  // Емітування подій
  await ctx.emit({ topic: "{emit-topic}", data: result });
};
```

### Тести
```typescript
// tests/unit/handler.test.ts
describe("{step-name} handler", () => {
  test("should process valid input", async () => {
    // Unit test implementation
  });
  
  test("should handle validation errors", async () => {
    // Error handling test
  });
});

// tests/integration/flow.test.ts
describe("{step-name} integration", () => {
  test("should complete full flow", async () => {
    // Integration test implementation
  });
});
```

## 🚀 Команди для тестування

### Запуск кроку
```bash
# Event Step
npx motia emit {event-topic} '{{input-data}}'

# API Step  
curl -X {METHOD} http://localhost:8080{api-path} -d '{{request-body}}'

# Cron Step
npx motia cron trigger {cron-step-name}
```

### Моніторинг
```bash
# Перегляд логів
npx motia logs {step-name}

# Перегляд стану
npx motia state get {group-id} {key}

# Трейсинг
npx motia trace {trace-id}
```

## 📚 Документація

### README.md
```markdown
# {step-name}

{Опис функціональності кроку}

## Використання
{Приклади використання}

## Конфігурація
{Опис налаштувань}

## API Reference
{Документація API якщо є}
```

### docs/examples.md
```markdown
# Приклади використання {step-name}

## Базовий приклад
{Приклад коду}

## Розширений приклад
{Складніший приклад}
```

## 🎯 Вимоги до генерації

1. **Всі файли мають бути згенеровані** згідно структури
2. **ДРАКОН діаграми мають відповідати** логіці handler.ts
3. **Тести мають покривати** основні сценарії та edge cases
4. **Документація має бути повною** з прикладами
5. **Схеми валідації мають бути коректними** JSON Schema
6. **Конфігурація має відповідати** типу кроку та патерну
```