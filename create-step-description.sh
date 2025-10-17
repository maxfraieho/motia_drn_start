#!/bin/bash

# Генератор повних описів Motia Steps з ДРАКОН діаграмами
# Використання: ./create-step-description.sh <step-name> <step-type> <pattern> <description>

STEP_NAME=$1
STEP_TYPE=$2  # api, event, cron, stream
PATTERN=$3    # observer, command, strategy, chain, template, state, mediator, factory
DESCRIPTION=$4
LANGUAGE=${5:-typescript}

# Перевірка аргументів
if [ -z "$STEP_NAME" ] || [ -z "$STEP_TYPE" ] || [ -z "$PATTERN" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 <step-name> <step-type> <pattern> <description> [language]"
    echo ""
    echo "Arguments:"
    echo "  step-name     - Назва кроку (наприклад: user-processor)"
    echo "  step-type     - Тип кроку: api | event | cron | stream"
    echo "  pattern       - Патерн: observer | command | strategy | chain | template | state | mediator | factory"
    echo "  description   - Опис функціональності кроку"
    echo "  language      - Мова програмування: typescript | python | ruby (за замовчуванням: typescript)"
    echo ""
    echo "Приклади:"
    echo "  $0 user-processor event observer 'Обробляє реєстрацію користувачів та відправляє welcome email'"
    echo "  $0 create-order api command 'API для створення нових замовлень з валідацією' python"
    echo "  $0 notification-sender event strategy 'Відправляє сповіщення через різні канали'"
    exit 1
fi

# Створення папок
mkdir -p step-descriptions
mkdir -p generated-steps

# Визначення обробників подій залежно від типу кроку
case $STEP_TYPE in
    "api")
        HANDLER_TYPE="ApiRouteHandler"
        INPUT_PARAMS="req, ctx"
        CONFIG_EXTRA='"path": "/'"$STEP_NAME"'", "method": "POST",'
        ;;
    "event") 
        HANDLER_TYPE="EventHandler"
        INPUT_PARAMS="input, ctx"
        CONFIG_EXTRA='"subscribes": ["'"$STEP_NAME"'.trigger"],'
        ;;
    "cron")
        HANDLER_TYPE="CronHandler" 
        INPUT_PARAMS="ctx"
        CONFIG_EXTRA='"cron": "0 */6 * * *",'
        ;;
    "stream")
        HANDLER_TYPE="EventHandler"
        INPUT_PARAMS="input, ctx"
        CONFIG_EXTRA='"subscribes": ["stream.data"],'
        ;;
    *)
        echo "Помилка: Непідтримуваний тип кроку: $STEP_TYPE"
        exit 1
        ;;
esac

# Створення step-description.md файлу
cat > "step-descriptions/${STEP_NAME}-description.md" << EOF
# $STEP_NAME - Повний опис кроку Motia

## 🏗️ Структура кроку
\`\`\`
$STEP_NAME/
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
\`\`\`

## 📋 Специфікація кроку

### Базова інформація
- **Тип кроку**: $STEP_TYPE
- **Патерн проектування**: $PATTERN
- **Мова програмування**: $LANGUAGE
- **Основна функція**: $DESCRIPTION

### Конфігурація (config.json)
\`\`\`json
{
  "type": "$STEP_TYPE",
  "name": "$STEP_NAME",
  "description": "$DESCRIPTION",
  $CONFIG_EXTRA
  "emits": ["$STEP_NAME.completed"],
  "flows": ["$STEP_NAME-flow"],
  "compatibility_date": "2024-01-01"
}
\`\`\`

### Схема валідації (schema.json)
\`\`\`json
{
  "\$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "data": {
      "type": "object",
      "description": "Вхідні дані для кроку"
    }
  },
  "required": ["data"]
}
\`\`\`

## 🎨 ДРАКОН діаграми

### logic-flow.drakon - Основна логіка
\`\`\`
ЗАГОЛОВОК: $STEP_NAME - Основний потік
├─ ПОЧАТОК
├─ ДІЯ: Отримати вхідні дані
├─ УМОВА: Дані валідні?
│  ├─ ТАК → ДІЯ: Обробити дані
│  └─ НІ → ДІЯ: Повернути помилку валідації
├─ ДІЯ: Виконати бізнес-логіку
├─ ДІЯ: Емітувати події
└─ КІНЕЦЬ
\`\`\`

### error-handling.drakon - Обробка помилок
\`\`\`
ЗАГОЛОВОК: $STEP_NAME - Обробка помилок
├─ ПОЧАТОК
├─ УМОВА: Тип помилки?
│  ├─ Валідація → ДІЯ: Логувати як WARNING
│  ├─ Бізнес-логіка → ДІЯ: Логувати як ERROR
│  └─ Система → ДІЯ: Логувати як CRITICAL
├─ ДІЯ: Сформувати response
└─ КІНЕЦЬ
\`\`\`

### data-processing.drakon - Обробка даних
\`\`\`
ЗАГОЛОВОК: $STEP_NAME - Обробка даних
├─ ПОЧАТОК
├─ ДІЯ: Парсинг вхідних даних
├─ ДІЯ: Трансформація даних
├─ УМОВА: Потрібно зберегти стан?
│  ├─ ТАК → ДІЯ: ctx.state.set()
│  └─ НІ → Продовжити
├─ ДІЯ: Підготувати вихідні дані
└─ КІНЕЦЬ
\`\`\`

### state-transitions.drakon - Переходи станів
\`\`\`
ЗАГОЛОВОК: $STEP_NAME - Стани
├─ ПОЧАТОК
├─ УМОВА: Поточний стан?
│  ├─ INITIAL → ДІЯ: Встановити PROCESSING
│  ├─ PROCESSING → ДІЯ: Встановити COMPLETED/FAILED
│  └─ COMPLETED → ДІЯ: Встановити ARCHIVED
└─ КІНЕЦЬ
\`\`\`

## 🔧 Реалізація

### handler.ts
\`\`\`typescript
import { $HANDLER_TYPE, FlowContext } from "motia";

export const config = {
  type: "$STEP_TYPE",
  name: "$STEP_NAME",
  description: "$DESCRIPTION",
  $CONFIG_EXTRA
  emits: ["$STEP_NAME.completed"],
  compatibility_date: "2024-01-01"
};

export const handler: $HANDLER_TYPE = async (
  $INPUT_PARAMS
) => {
  // Реалізація відповідно до ДРАКОН діаграм

  // 1. Валідація (logic-flow.drakon)
  ctx.logger.info("Starting $STEP_NAME processing");

  // 2. Обробка даних (data-processing.drakon)

  // 3. Обробка помилок (error-handling.drakon)

  // 4. Управління станом (state-transitions.drakon)

  // Емітування подій
  await ctx.emit({ 
    topic: "$STEP_NAME.completed", 
    data: { status: "success" } 
  });
};
\`\`\`

## 🚀 Команди для тестування

### Запуск кроку
\`\`\`bash
EOF

# Додаємо специфічні команди залежно від типу кроку
case $STEP_TYPE in
    "api")
        echo "# API Step" >> "step-descriptions/${STEP_NAME}-description.md"
        echo "curl -X POST http://localhost:8080/$STEP_NAME -d '{"data": {}}'" >> "step-descriptions/${STEP_NAME}-description.md"
        ;;
    "event") 
        echo "# Event Step" >> "step-descriptions/${STEP_NAME}-description.md"
        echo "npx motia emit $STEP_NAME.trigger '{"data": {}}'" >> "step-descriptions/${STEP_NAME}-description.md"
        ;;
    "cron")
        echo "# Cron Step" >> "step-descriptions/${STEP_NAME}-description.md"
        echo "npx motia cron trigger $STEP_NAME" >> "step-descriptions/${STEP_NAME}-description.md"
        ;;
    "stream")
        echo "# Stream Step" >> "step-descriptions/${STEP_NAME}-description.md"
        echo "npx motia emit stream.data '{"data": {}}'" >> "step-descriptions/${STEP_NAME}-description.md"
        ;;
esac

cat >> "step-descriptions/${STEP_NAME}-description.md" << 'EOF'
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

## 🎯 Вимоги до генерації

1. **Всі файли мають бути згенеровані** згідно структури
2. **ДРАКОН діаграми мають відповідати** логіці handler.ts
3. **Тести мають покривати** основні сценарії та edge cases
4. **Документація має бути повною** з прикладами
5. **Схеми валідації мають бути коректними** JSON Schema
6. **Конфігурація має відповідати** типу кроку та патерну
EOF

echo "✅ Створено опис кроку: step-descriptions/${STEP_NAME}-description.md"
echo ""
echo "🚀 Для генерації коду використайте:"
echo "claude --append-system-prompt "\$(cat CLAUDE.md)" --append-system-prompt "\$(cat patterns/${PATTERN}-pattern.md)" -p "\$(cat step-descriptions/${STEP_NAME}-description.md)""
