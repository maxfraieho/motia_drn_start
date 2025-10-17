# 🤖 Motia Markdown Service v1.0

**CLI-оркестратор для AI-driven генерації коду з Claude CLI**

Автоматична агрегація та підготовка контексту для триступеневого процесу генерації коду через Claude CLI.

---

## 📋 Зміст

- [Огляд](#огляд)
- [Архітектура](#архітектура)
- [Встановлення](#встановлення)
- [Швидкий старт](#швидкий-старт)
- [Використання](#використання)
- [Триступенева підготовка](#триступенева-підготовка)
- [Структура файлів](#структура-файлів)
- [Приклади](#приклади)
- [ДРАКОН-конвертер](#дракон-конвертер)
- [FAQ](#faq)

---

## Огляд

Motia Markdown Service — це набір інструментів для автоматизації підготовки контексту для Claude CLI. Сервіс дозволяє:

✅ **Автоматично агрегувати** всю інформацію з проєкту в структуровані markdown-файли
✅ **Організувати триступеневий контекст**: Project → Pattern → Step
✅ **Конвертувати ДРАКОН-схеми** в псевдокод з повним розумінням мови
✅ **Генерувати команди для Claude CLI** з усім необхідним контекстом
✅ **Оркеструвати весь процес** через зручний CLI-інтерфейс

---

## Архітектура

### Триступенева модель контексту

```
┌─────────────────────────────────────────────────────────┐
│  Рівень 1: PROJECT CONTEXT                              │
│  ├─ motia.md                                            │
│  ├─ README.md                                           │
│  ├─ Структура проєкту                                   │
│  └─ Список доступних патернів                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Рівень 2: PATTERN CONTEXT                              │
│  ├─ Опис патерну (factory-pattern.md)                   │
│  ├─ Приклади використання                               │
│  └─ Best practices                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Рівень 3: STEP CONTEXT                                 │
│  ├─ handler.ts / handler.py                             │
│  ├─ config.json, schema.json                            │
│  ├─ ДРАКОН діаграми (конвертовані в псевдокод)          │
│  ├─ Тести                                               │
│  └─ Документація                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
                  Claude CLI Command
```

### Компоненти системи

#### 1. **motia-md-service.py** — Python-сервіс

Три основні класи:

- **MarkdownAggregator** — Агрегація markdown з файлів та директорій
- **EnvironmentDeployer** — Розгортання структури Motia-проєкту
- **ClaudeStepPreparator** — Підготовка контексту для Claude CLI

#### 2. **motia-md-service.sh** — Bash-оркестратор

Секції:
- **Config** — Налаштування кольорів, шляхів, версій
- **Validation** — Перевірка Python, Claude CLI, файлів
- **Menu** — Інтерактивне меню з опціями
- **Execution** — Виконання команд та обробка помилок

#### 3. **motia-drakon-converter.py** — ДРАКОН-конвертер

Конвертує ДРАКОН-схеми (.json) в структурований псевдокод згідно зі специфікацією мови ДРАКОН.

---

## Встановлення

### Вимоги

- **Python 3.7+**
- **Bash** (Linux/macOS)
- **Claude CLI** (опціонально, для автоматичного виконання)

### Крок 1: Завантаження файлів

```bash
cd /path/to/your/motia-project
# Скопіюйте файли сервісу в директорію проєкту:
# - motia-md-service.py
# - motia-md-service.sh
# - motia-drakon-converter.py
```

### Крок 2: Надання прав виконання

```bash
chmod +x motia-md-service.sh
chmod +x motia-md-service.py
chmod +x motia-drakon-converter.py
```

### Крок 3: Встановлення Claude CLI (опціонально)

```bash
# Для автоматичного виконання команд потрібен Claude CLI
# Інструкції: https://github.com/anthropics/claude-cli

# Після встановлення перевірте:
claude --version
```

---

## Швидкий старт

### Варіант 1: Bash-оркестратор (рекомендовано)

```bash
./motia-md-service.sh
```

Відкриється інтерактивне меню з опціями.

### Варіант 2: Python-сервіс напряму

```bash
python3 motia-md-service.py
```

### Варіант 3: Автоматизація через команди

```bash
# Агрегація контексту проєкту
python3 -c "
from motia_md_service import *
config = MotiaConfig.from_path('.')
aggregator = MarkdownAggregator(config)
aggregator.aggregate_project_context()
"
```

---

## Використання

### Меню Bash-оркестратора

```
======================================================================
    🤖 MOTIA MARKDOWN SERVICE v1.0
    Claude CLI Integration & AI-Powered Code Generation
======================================================================

  [1] 🚀 Deploy Motia Project Structure
  [2] 📋 Aggregate Project Context (Level 1)
  [3] 🎯 Aggregate Pattern Context (Level 2)
  [4] 🔧 Aggregate Step Context (Level 3)
  [5] 🎯 Full Pipeline: Three-Level Claude CLI Preparation
  [6] 🌳 Show Project Structure
  [7] 🐍 Launch Interactive Python Service
  [8] ℹ️  Help & Documentation
  [9] 🚪 Exit
```

### Опція 1: Розгортання структури

Створює базові директорії для Motia-проєкту:

```
motia-project/
├── patterns/           # Патерни проєктування
├── steps/              # Кроки (steps) проєкту
├── output/             # Згенеровані markdown-файли
└── step-descriptions/  # Агреговані описи кроків
```

### Опція 2: Агрегація Project Context

Створює файл `output/motia-project-context.md` з:
- Вмістом motia.md
- README.md
- Структурою проєкту
- Списком доступних патернів

### Опція 3: Агрегація Pattern Context

Створює файл `output/motia-pattern-{name}.md` з:
- Повним описом патерну
- Прикладами використання в існуючих кроках

**Приклад:**

```bash
▶ Your choice: 3
📌 Enter pattern name: factory-pattern

✅ Created: output/motia-pattern-factory-pattern.md
```

### Опція 4: Агрегація Step Context

Створює файл `step-descriptions/{step-name}-complete.md` з:
- Структурою кроку
- README
- config.json, schema.json
- Кодом handler
- ДРАКОН діаграмами (конвертованими в псевдокод)
- Тестами

**Приклад:**

```bash
▶ Your choice: 4
📁 Enter step path: ./steps/auth-middleware

✅ Created: step-descriptions/auth-middleware-complete.md
📊 Processed files: 12
📊 DRAKON diagrams: 4
```

### Опція 5: Повний pipeline ⭐

Найважливіша опція! Виконує всі три рівні агрегації та генерує готову команду для Claude CLI.

**Приклад:**

```bash
▶ Your choice: 5

📌 Enter pattern name: factory-pattern
📁 Enter step path: ./steps/database-service

🎯 Preparing three-level context for Claude CLI...
======================================================================

[1/3] Level 1: Project Context
✅ Created: output/motia-project-context.md (125,467 bytes)

[2/3] Level 2: Pattern Context
✅ Created: output/motia-pattern-factory-pattern.md (45,123 bytes)

[3/3] Level 3: Step Context
✅ Created: step-descriptions/database-service-complete.md (67,890 bytes)

======================================================================
✅ Three-level context prepared!

📋 Generated Claude CLI command:
======================================================================
claude \
  --context-file "output/motia-project-context.md" \
  --context-file "output/motia-pattern-factory-pattern.md" \
  --context-file "step-descriptions/database-service-complete.md" \
  --prompt "Optimize the step code according to the pattern and project architecture"
======================================================================
```

Тепер просто скопіюйте та виконайте згенеровану команду!

---

## Триступенева підготовка

### Навіщо три рівні?

Кожен рівень додає специфічний контекст для Claude:

1. **Project Context** — Claude розуміє загальну архітектуру проєкту
2. **Pattern Context** — Claude знає, який патерн застосовувати
3. **Step Context** — Claude бачить конкретний код для оптимізації

### Workflow для генерації нового кроку

```bash
# 1. Створюємо заготовку кроку
mkdir -p steps/new-feature
cd steps/new-feature

# 2. Створюємо базові файли
touch handler.ts config.json schema.json README.md
mkdir diagrams tests

# 3. Запускаємо повний pipeline
cd ../..
./motia-md-service.sh
# Обираємо опцію 5

# 4. Вводимо дані:
# Pattern: strategy-pattern
# Step path: ./steps/new-feature

# 5. Виконуємо згенеровану команду Claude CLI
claude --context-file ... --prompt "Generate complete implementation"

# 6. Claude генерує оптимальний код згідно з контекстом!
```

---

## Структура файлів

### Вхідні файли

```
motia-project/
├── motia.md                    # Опис проєкту
├── README.md                   # Загальна документація
├── patterns/                   # Патерни
│   ├── factory-pattern.md
│   ├── strategy-pattern.md
│   └── observer-pattern.md
└── steps/                      # Кроки проєкту
    ├── auth-middleware/
    │   ├── handler.ts
    │   ├── config.json
    │   ├── schema.json
    │   ├── README.md
    │   ├── diagrams/
    │   │   ├── logic-flow.json        # ДРАКОН-схема
    │   │   └── error-handling.json
    │   └── tests/
    │       └── handler.test.ts
    └── database-service/
        └── ...
```

### Вихідні файли

```
motia-project/
├── output/                             # Згенеровані контексти
│   ├── motia-project-context.md        # Рівень 1
│   ├── motia-pattern-factory.md        # Рівень 2
│   └── motia-pattern-strategy.md
└── step-descriptions/                  # Агреговані кроки
    ├── auth-middleware-complete.md     # Рівень 3
    └── database-service-complete.md
```

---

## Приклади

### Приклад 1: Створення нового кроку з Factory Pattern

```bash
# Запускаємо сервіс
./motia-md-service.sh

# Обираємо опцію 5 (Full Pipeline)
▶ Your choice: 5

# Вводимо дані
📌 Enter pattern name: factory-pattern
📁 Enter step path: ./steps/notification-service
📝 Task description: Generate notification service with multiple channels

# Отримуємо команду
claude \
  --context-file "output/motia-project-context.md" \
  --context-file "output/motia-pattern-factory-pattern.md" \
  --context-file "step-descriptions/notification-service-complete.md" \
  --prompt "Generate notification service with multiple channels"

# Виконуємо → Claude генерує код!
```

### Приклад 2: Рефакторинг існуючого кроку

```bash
# У вас є крок ./steps/old-service з легасі-кодом
# Хочете рефакторити його згідно з Strategy Pattern

./motia-md-service.sh
▶ Your choice: 5

📌 factory-pattern  → strategy-pattern
📁 ./steps/old-service
📝 Refactor legacy code to use Strategy Pattern with proper dependency injection

# Claude отримає весь контекст і запропонує рефакторинг!
```

### Приклад 3: Конвертація ДРАКОН-схеми окремо

```bash
# Якщо хочете просто конвертувати ДРАКОН в псевдокод
./motia-drakon-converter.py \
  ./steps/auth-middleware/diagrams/logic-flow.json \
  -o output/auth-logic-pseudocode.md

# Результат:
✅ Псевдокод збережено: output/auth-logic-pseudocode.md
📏 Розмір: 12,345 bytes
```

---

## ДРАКОН-конвертер

### Що таке ДРАКОН?

ДРАКОН — візуальна мова алгоритмів, розроблена в російській космічній індустрії. Основні переваги:

- Графічне представлення логіки
- Структурне програмування
- Легке читання алгоритмів
- Чіткі ергономічні правила

### Підтримувані конструкції

✅ **Дія** (action) — Виконання операції
✅ **Вопрос** (question) — Розгалуження if-then-else
✅ **Выбор** (select) — switch-case
✅ **Цикл ДЛЯ** (foreach) — for/foreach цикли
✅ **Цикл зі стрілкою** (loop) — while цикли
✅ **Силует** (branch) — Багатогіллєва структура
✅ **Адрес** (address) — Перехід між гілками

### Приклад конвертації

**Вхід (logic-flow.json):**

```json
{
  "nodes": {
    "1": {"type": "start", "content": {"txt": "Authenticate User"}},
    "2": {"type": "action", "content": {"txt": "Parse credentials"}},
    "3": {"type": "question", "content": {"txt": "Valid format?"}}
  },
  "edges": [
    {"src": "1", "dst": "2"},
    {"src": "2", "dst": "3"},
    {"src": "3", "dst": "4", "label": "да"},
    {"src": "3", "dst": "5", "label": "нет"}
  ]
}
```

**Вихід (pseudocode):**

```
======================================================================
ДРАКОН-СХЕМА: Псевдокод алгоритму
======================================================================

АЛГОРИТМ: Authenticate User

ПОЧАТОК
  ВИКОНАТИ: Parse credentials
  ЯКЩО (Valid format?):
    # [ДА - основний шлях]
    ВИКОНАТИ: Verify credentials
  ІНАКШЕ:
    # [НІ - альтернативний/проблемний шлях]
    ВИКОНАТИ: Return error
  КІНЕЦЬ ЯКЩО
КІНЕЦЬ
```

---

## FAQ

### 1. Чи потрібен Claude CLI для роботи?

Ні, сервіс генерує готові команди, які можна виконати вручну. Claude CLI потрібен тільки для автоматизації виконання.

### 2. Чи можна використовувати з іншими AI-інструментами?

Так! Згенеровані markdown-файли можна використовувати з будь-яким AI-інструментом, що приймає текстовий контекст.

### 3. Скільки часу займає агрегація великого проєкту?

Залежить від розміру:
- Малий проєкт (10 файлів): ~2 секунди
- Середній (100 файлів): ~10 секунд
- Великий (1000+ файлів): ~30-60 секунд

### 4. Чи підтримується Windows?

Python-сервіс працює на Windows. Bash-скрипт потребує WSL або Git Bash.

### 5. Як додати власний патерн?

```bash
# Створіть файл у папці patterns/
echo "# My Custom Pattern\n\nDescription..." > patterns/my-pattern.md

# Використайте його в опції 3 або 5
```

### 6. Що робити, якщо ДРАКОН-схема конвертується некоректно?

Переконайтеся, що JSON містить поля:
- `nodes` з типами: action, question, select, foreach, branch
- `edges` зі зв'язками src → dst

Якщо проблема залишається, конвертуйте схему вручну або надайте issue.

---

## Команди швидкого доступу

```bash
# Запуск інтерактивного меню
./motia-md-service.sh

# Прямий запуск Python-сервісу
python3 motia-md-service.py

# Агрегація проєкту (без меню)
python3 -c "from motia_md_service import *; MarkdownAggregator(MotiaConfig.from_path('.')).aggregate_project_context()"

# Конвертація ДРАКОН
./motia-drakon-converter.py input.json -o output.md

# Перевірка структури
tree -L 3 -I 'node_modules|venv|__pycache__|.git'
```

---

## Ліцензія

MIT License

---

## Автор

**DevOps Engineer**
Версія: 1.0.0
Дата: 2025-10-10

---

## Корисні посилання

- [Claude CLI Documentation](https://github.com/anthropics/claude-cli)
- [Motia Framework](./motia.md)
- [ДРАКОН Specification](./drakon.md)

---

**Happy coding with Motia and Claude! 🚀**
