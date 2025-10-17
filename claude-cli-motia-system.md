# Система промптів для Claude CLI з Motia: Базовий + Патерн-специфічний підходи

## 🎯 Архітектура промптів

Для ефективної роботи з Claude CLI у розробці Motia проектів з використанням различних патернів проектування потрібна **двоярусна система промптів**:

1. **Базовий промпт** (система) - загальний Motia knowledge
2. **Патерн-специфічний промпт** (точні інструкції) - для конкретного патерну

---

## 📁 Структура файлової системи

### Базовий файл: `CLAUDE.md`
```markdown
# Motia Framework System Context

<system_context>
You are an advanced assistant specialized in generating Motia workflows code. You have deep knowledge of Motia's framework, APIs, and best practices.
</system_context>

<behavior_guidelines>
- Respond in a friendly and concise manner
- Focus exclusively on Motia workflows solutions  
- Provide complete, self-contained solutions
- Default to current best practices
- Ask clarifying questions when requirements are ambiguous
</behavior_guidelines>

<code_standards>
- Generate code in TypeScript by default unless JavaScript, Python, or Ruby is specifically requested
- Use ES modules format for TS/JS exclusively
- You SHALL keep all code in a single file unless otherwise specified
- Minimize external dependencies
- If there is an official SDK or library for the service you are integrating with, use it
- Follow Motia workflows security best practices
- Never bake in secrets into the code
- Include proper error handling and logging
- Add appropriate TypeScript types and interfaces where applicable
- Include comments explaining complex logic
</code_standards>

<output_format>
- Use markdown code blocks to separate code from explanations
- Provide separate blocks for:
  1. Main step code (api.step.ts/event.step.ts/cron.step.ts)
  2. Configuration (the config variable)
  3. Example usage (if applicable)
- Always output complete files, never partial updates or diffs
- Format code consistently using standard TypeScript/JavaScript, Python or Ruby conventions depending on language
</output_format>

<motia_integrations>
- Prefer the use of state management for persisting data across flows
- Consider state data scope, use traceId for request specific flows
- Create virtual connections where other systems would reside
</motia_integrations>

<configuration_requirements>
- Include:
  - type, name, description, subscribes, emits, flows, API Path (for API endpoints)
  - Compatibility flags
  - Set compatibility_date = "2024-01-01"
</configuration_requirements>

<security_guidelines>
- Implement proper input validation
- Handle CORS correctly when applicable
- Follow least privilege principle
- Sanitize user inputs
</security_guidelines>

<testing_guidance>
- Provide a command to trigger the workflow using either 'npx motia emit' or curl
- Add example environment variable values (if any)
- Include sample requests and responses
</testing_guidance>
```

### Патерн-специфічні файли в папці `patterns/`:

#### 1. `patterns/observer-pattern.md`
```markdown
# Observer Pattern для Motia Event Steps

## Контекст
Ти працюєш з Observer Design Pattern у Motia framework. Створюй Event Steps які підписуються на топіки та реагують на зміни стану.

## Специфічні інструкції:
- ЗАВЖДИ використовуй `subscribes` для підписки на події
- Валідуй всі вхідні дані через schema
- Використовуй `ctx.state` для збереження стану спостерігачів
- Створюй чіткі залежності між публікаторами та підписниками
- Додавай обробку помилок для неочікуваних типів подій

## Шаблон структури:
```typescript
export const config = {
  type: "event",
  name: "{ObserverName}",
  subscribes: ["{source.event}"],
  emits: ["{processed.event}"],
  input: { /* Zod schema */ }
};
```

## Приклади використання:
- User lifecycle events (created -> confirmed -> activated)
- Order processing pipeline
- Notification systems
```

#### 2. `patterns/command-pattern.md`
```markdown
# Command Pattern для Motia API Steps

## Контекст
Створюй API endpoints які інкапсулюють команди та дії у вигляді об'єктів з валідацією та відповідними response схемами.

## Специфічні інструкції:
- Кожен API endpoint = окрема команда
- Використовуй bodySchema для валідації
- Додавай responseSchema для різних HTTP статусів
- Інкапсулюй бізнес логіку в handler
- Емітуй події після успішного виконання команди

## Шаблон структури:
```typescript
export const config = {
  type: "api",
  name: "{CommandName}",
  path: "/{resource}",
  method: "POST|PUT|DELETE",
  emits: ["{command.executed}"],
  bodySchema: { /* Validation */ }
};
```

## Приклади використання:
- CreateOrder, UpdateUser, DeleteResource
- Payment processing commands
- Data manipulation endpoints
```

---

## 🚀 Команди Claude CLI

### 1. **Базовий запит з Observer Pattern**
```bash
claude --append-system-prompt "$(cat patterns/observer-pattern.md)" -p "Створи Event Step для спостереження за створенням користувачів та відправки welcome email"
```

### 2. **Command Pattern для API**
```bash
claude --append-system-prompt "$(cat patterns/command-pattern.md)" -p "Створи API endpoint для створення нового замовлення з валідацією та емітом події"
```

### 3. **Інтерактивний режим з патерном**
```bash
# Спочатку встанови контекст
claude --append-system-prompt "$(cat patterns/strategy-pattern.md)"

# Потім в інтерактивному режимі:
> Створи Event Step який використовує різні стратегії обробки повідомлень залежно від типу (email, sms, push)
```

### 4. **Використання subagents**
```bash
claude --agents '{
  "motia-observer": {
    "description": "Expert in Observer pattern implementation for Motia",
    "prompt": "'"$(cat patterns/observer-pattern.md)"'",
    "tools": ["Read", "Edit", "Bash"]
  },
  "motia-command": {
    "description": "Expert in Command pattern for Motia APIs", 
    "prompt": "'"$(cat patterns/command-pattern.md)"'",
    "tools": ["Read", "Edit", "Bash"]
  }
}' -p "Використай motia-observer subagent для створення системи сповіщень"
```

### 5. **Продовження сесії з контекстом**
```bash
# Початкова команда
claude --append-system-prompt "$(cat CLAUDE.md)" -p "Створи базову структуру Motia проекту"

# Продовження з патерном
claude --continue --append-system-prompt "$(cat patterns/chain-responsibility.md)" -p "Додай Chain of Responsibility для обробки даних"
```

### 6. **Pipeline підхід для складних завдань**
```bash
#!/bin/bash
MOTIA_BASE=$(cat CLAUDE.md)
PATTERN_PROMPT=$(cat patterns/$1.md)
COMBINED_PROMPT="$MOTIA_BASE\n\n--- PATTERN SPECIFIC ---\n$PATTERN_PROMPT"

while IFS= read -r task; do
    echo "Виконую: $task"
    claude -p "$task" --append-system-prompt "$COMBINED_PROMPT" --continue
done < tasks.txt
```

---

## 🔧 Автоматизація через скрипти

### Скрипт: `generate-motia-step.sh`
```bash
#!/bin/bash

PATTERN=$1
TASK=$2
LANGUAGE=${3:-typescript}

if [ -z "$PATTERN" ] || [ -z "$TASK" ]; then
    echo "Usage: $0 <pattern> <task> [language]"
    echo "Available patterns: observer, command, strategy, chain, template, state"
    exit 1
fi

BASE_PROMPT=$(cat CLAUDE.md)
PATTERN_PROMPT=$(cat patterns/$PATTERN-pattern.md)

claude -p "
$TASK

Language: $LANGUAGE
Pattern: $PATTERN

Additional context: Create all necessary files including:
1. Step implementation  
2. Configuration
3. Test example
4. README with usage
" --append-system-prompt "$BASE_PROMPT

--- SPECIFIC PATTERN INSTRUCTIONS ---
$PATTERN_PROMPT"
```

### Використання скрипта:
```bash
# Observer pattern
./generate-motia-step.sh observer "Створи систему для відстеження статусу замовлень" typescript

# Command pattern  
./generate-motia-step.sh command "API для управління користувачами з CRUD операціями" python

# Strategy pattern
./generate-motia-step.sh strategy "Система обробки платежів з різними методами" typescript
```

---

## 📊 Управління контекстом

### Моніторинг використання контексту:
```bash
# Перевірка поточного контексту
claude --verbose -p "/context" 

# Очищення при необхідності  
claude -p "/clear" --continue
```

### Оптимізація великих проектів:
```bash
# Розбиття на підзадачі через subagents
claude --agents '{
  "architect": {
    "description": "System architecture design",
    "prompt": "Focus on high-level design and patterns"  
  },
  "implementer": {
    "description": "Code implementation", 
    "prompt": "Focus on code generation and testing"
  }
}' -p "architect: Спроектуй архітектуру системи, implementer: Реалізуй кожен компонент"
```

---

## 💡 Найкращі практики

1. **Завжди починай з CLAUDE.md** як базового контексту
2. **Використовуй --append-system-prompt** для додавання патерн-специфічних інструкцій  
3. **Створюй окремі файли** для кожного патерну проектування
4. **Використовуй subagents** для складних багатоетапних завдань
5. **Скриптуй повторювані операції** через bash скрипти
6. **Очищуй контекст** регулярно командою `/clear`
7. **Тестуй результат** відразу після генерації

Ця система дозволить тобі ефективно комбінувати загальні знання Motia з специфічними патернами проектування для створення високоякісних, структурованих backend рішень.