# 🎯 Триступенева архітектура Claude CLI для Motia Steps

## Концепція

Для повної генерації Motia кроків з ДРАКОН діаграмами та структурою папок використовується **триступенева архітектура промптів**:

```
CLAUDE.md (Базовий контекст)
    ↓
patterns/{pattern}-pattern.md (Патерн-специфічний)
    ↓
step-descriptions/{step}-description.md (Повний опис кроку)
    ↓
Claude CLI генерація → Повна реалізація
```

---

## 📁 Структура файлів проекту

```
motia-project/
├── CLAUDE.md                           # Базовий Motia контекст
├── patterns/                           # Патерн-специфічні промпти
│   ├── observer-pattern.md
│   ├── command-pattern.md
│   ├── strategy-pattern.md
│   └── ...
├── step-descriptions/                  # Повні описи кроків
│   ├── user-processor-description.md
│   ├── order-creator-description.md
│   └── ...
├── generated-steps/                    # Згенеровані кроки
│   ├── user-processor/
│   │   ├── handler.ts
│   │   ├── config.json
│   │   ├── schema.json
│   │   ├── README.md
│   │   ├── diagrams/
│   │   │   ├── logic-flow.drakon
│   │   │   ├── error-handling.drakon
│   │   │   ├── data-processing.drakon
│   │   │   └── state-transitions.drakon
│   │   ├── tests/
│   │   └── docs/
│   └── ...
├── create-step-description.sh          # Генератор описів
└── full-generate-motia-step.sh        # Повна автоматизація
```

---

## 🚀 Використання

### 1. Створення опису кроку

```bash
# Генерація step-description.md файлу
./create-step-description.sh user-processor event observer "Обробляє реєстрацію користувачів та відправляє welcome email" typescript
```

**Результат**: Створюється `step-descriptions/user-processor-description.md` з повною структурою:
- Схеми ДРАКОН діаграм
- Конфігурація Motia
- JSON схеми валідації  
- Структура папок та файлів
- Тестові команди

### 2. Генерація коду через Claude CLI

#### Ручний спосіб (максимальний контроль):
```bash
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/observer-pattern.md)" \
       -p "$(cat step-descriptions/user-processor-description.md)"
```

#### Автоматизований спосіб (рекомендований):
```bash
./full-generate-motia-step.sh user-processor event observer "Обробляє реєстрацію користувачів" typescript
```

---

## 📋 Приклади команд

### Observer Pattern (Event Step)
```bash
# Створення опису
./create-step-description.sh user-lifecycle event observer "Спостерігає за lifecycle подіями користувача" typescript

# Повна генерація
./full-generate-motia-step.sh user-lifecycle event observer "Спостерігає за lifecycle подіями користувача"

# Ручна генерація з додатковими параметрами
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/observer-pattern.md)" \
       --verbose \
       -p "$(cat step-descriptions/user-lifecycle-description.md)

ДОДАТКОВІ ВИМОГИ:
- Включи retry механізм для failed events
- Додай metrics collection для observability
- Створи comprehensive error handling"
```

### Command Pattern (API Step)  
```bash
# Створення CRUD API з валідацією
./full-generate-motia-step.sh order-manager api command "CRUD API для управління замовленнями з повною валідацією" python

# Результат: generated-steps/order-manager/ з усіма файлами
```

### Strategy Pattern (Event Step)
```bash
# Система сповіщень з різними стратегіями
./full-generate-motia-step.sh notification-sender event strategy "Відправляє сповіщення через email, SMS або push" typescript
```

### Chain of Responsibility (Stream Step)
```bash
# Pipeline обробки даних
./full-generate-motia-step.sh data-validator stream chain "Послідовна валідація даних через ланцюг перевірок" typescript
```

---

## 🎨 Структура step-description.md

Кожен згенерований `step-description.md` містить:

### 📋 Специфікацію кроку
- Тип кроку (api/event/cron/stream)
- Патерн проектування
- Мову програмування
- Функціональний опис

### 🎨 ДРАКОН діаграми у текстовому форматі
```
ЗАГОЛОВОК: user-processor - Основний потік
├─ ПОЧАТОК
├─ ДІЯ: Отримати дані користувача
├─ УМОВА: Email валідний?
│  ├─ ТАК → ДІЯ: Створити користувача
│  └─ НІ → ДІЯ: Повернути помилку
├─ ДІЯ: Емітувати user.created
└─ КІНЕЦЬ
```

### 🔧 Шаблони реалізації
- TypeScript/Python handler код
- Motia конфігурація
- JSON схеми валідації
- Тестові команди

### 🚀 Команди для тестування
- Запуск кроку
- Моніторинг логів
- Трейсинг виконання

---

## 🎯 Переваги підходу

### 1. **Повна автоматизація**
Один скрипт створює всю структуру кроку з документацією

### 2. **Консистентність**
Всі кроки дотримуються єдиних стандартів Motia

### 3. **Візуальне моделювання**  
ДРАКОН діаграми забезпечують зрозумілість логіки

### 4. **Модульність**
Кожен рівень промпту можна змінювати незалежно

### 5. **Масштабованість**
Легко додавати нові патерни та типи кроків

---

## 🔧 Налаштування та розширення

### Додавання нового патерну
1. Створіть `patterns/new-pattern.md` з специфічними інструкціями
2. Модифікуйте скрипти для підтримки нового патерну
3. Додайте приклади використання

### Кастомізація шаблонів
Модифікуйте `step-description-template.md` для додавання:
- Специфічних ДРАКОН елементів
- Додаткових файлів в структуру
- Кастомних тестових сценаріїв

### Інтеграція з CI/CD
```bash
# Автоматична генерація в pipeline
./full-generate-motia-step.sh $STEP_NAME $STEP_TYPE $PATTERN "$DESCRIPTION"
npm test generated-steps/$STEP_NAME/
```

---

Цей підхід забезпечує повну автоматизацію створення структурованих, документованих та тестованих Motia кроків з візуальним моделюванням ДРАКОН для кожного патерну проектування.