# 🎯 Агрегація структури Motia Step для Claude CLI

## Концепція

Для використання повної описової структури кроку як аргументу для Claude CLI, створена система **автоматичної агрегації** всієї інформації з папки кроку в один markdown файл.

```
Існуюча папка кроку:
{step-name}/
├── handler.ts
├── config.json  
├── schema.json
├── README.md
├── diagrams/
│   ├── logic-flow.drakon
│   ├── error-handling.drakon
│   ├── data-processing.drakon
│   └── state-transitions.drakon
├── tests/
└── docs/

        ↓ агрегація ↓

Повний markdown опис:
step-descriptions/{step-name}-complete.md

        ↓ Claude CLI ↓

Оптимізований код
```

---

## 🔧 Автоматизовані скрипти

### **1. Агрегація існуючого кроку**
```bash
# Збирає всю інформацію з папки в один markdown
./aggregate-step-to-md.sh ./existing-user-step user-step-complete
```

**Результат**: `step-descriptions/user-step-complete.md` містить:
- Структуру папки
- Весь код (handler.ts/py)
- Конфігурацію (config.json, schema.json)
- ДРАКОН діаграми
- Тести та документацію
- Інструкції для Claude CLI

### **2. Інтегрований workflow**
```bash
# Агрегація + генерація оптимізованого коду
./motia-claude-workflow.sh aggregate-and-generate ./existing-step observer
```

---

## 🚀 Практичні сценарії використання

### **Сценарій 1: Оптимізація існуючого кроку**
```bash
# У вас є папка з кроком, який потребує покращення
./motia-claude-workflow.sh aggregate-and-generate ./legacy-payment-step command

# Результат:
# 1. step-descriptions/legacy-payment-step-optimized.md
# 2. Оптимізований код від Claude CLI з:
#    - Покращеною структурою
#    - Оновленими ДРАКОН діаграмами  
#    - Сучасними best practices
```

### **Сценарій 2: Аналіз та рефакторинг**
```bash
# Тільки агрегація для детального аналізу
./aggregate-step-to-md.sh ./complex-order-processor analysis-ready

# Потім ручна генерація з додатковими вимогами:
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/chain-responsibility.md)" \
       -p "$(cat step-descriptions/analysis-ready.md)

ДОДАТКОВІ ВИМОГИ:
- Розділи складну логіку на менші кроки
- Додай comprehensive error handling
- Створи Chain of Responsibility для validation"
```

### **Сценарій 3: Міграція між патернами**
```bash
# Агрегувати існуючий крок
./aggregate-step-to-md.sh ./old-notification-step notification-analysis

# Згенерувати з новим патерном
./motia-claude-workflow.sh generate step-descriptions/notification-analysis.md strategy

# Результат: Той же функціонал, але з Strategy pattern замість старого підходу
```

---

## 📋 Структура агрегованого markdown файлу

```markdown
# {step-name} - Повний агрегований опис кроку Motia

## 🏗️ Структура кроку
[Повна структура папки]

## 📋 Конфігурація кроку
### config.json
[Вміст config.json]

### schema.json  
[Вміст schema.json]

## 🔧 Реалізація кроку
### handler.ts/py/rb
[Повний код handler]

## 🎨 ДРАКОН діаграми
### logic-flow.drakon
[Вміст діаграми основної логіки]

### error-handling.drakon
[Вміст діаграми обробки помилок]

### data-processing.drakon
[Вміст діаграми обробки даних]

### state-transitions.drakon
[Вміст діаграми переходів станів]

## 📚 Документація кроку
[Вміст README.md]

## 🧪 Тести
[Всі тестові файли]

## 📖 Додаткова документація
[Файли з папки docs/]

## 🎯 Інструкції для Claude CLI
[Автоматично згенеровані інструкції для оптимізації]
```

---

## 🎛️ Команди Claude CLI

### **Базова команда з агрегованим описом**
```bash
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/observer-pattern.md)" \
       -p "$(cat step-descriptions/user-step-complete.md)"
```

### **Розширена команда з додатковими вимогами**
```bash
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/command-pattern.md)" \
       -p "$(cat step-descriptions/api-step-complete.md)

СПЕЦІАЛЬНІ ВИМОГИ:
- Додай OpenAPI специфікацію
- Включи rate limiting
- Створи comprehensive error responses
- Додай metrics collection"
```

### **Інтерактивний режим для складних змін**
```bash
# Завантаження контексту
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/strategy-pattern.md)" \
       --continue

# В інтерактивному режимі:
> Ось повний опис кроку: $(cat step-descriptions/notification-step-complete.md)
> 
> Потрібно:
> 1. Рефакторинг з Strategy pattern
> 2. Додавання нових каналів сповіщень  
> 3. Покращення error handling
> 4. Створення детальних ДРАКОН діаграм
```

---

## 🔄 Workflow інтеграції

### **Повний цикл розробки**
```bash
# 1. Створення нового кроку
./motia-claude-workflow.sh full-cycle user-manager api command "CRUD API для користувачів"

# 2. Оптимізація існуючого кроку  
./motia-claude-workflow.sh aggregate-and-generate ./legacy-step observer

# 3. Аналіз без змін
./motia-claude-workflow.sh aggregate ./existing-step analysis-only
```

### **Покроковий підхід**
```bash
# Крок 1: Агрегація
./aggregate-step-to-md.sh ./my-step my-step-full

# Крок 2: Ручна генерація з контролем
claude --append-system-prompt "$(cat CLAUDE.md)" \
       --append-system-prompt "$(cat patterns/chain-responsibility.md)" \
       -p "$(cat step-descriptions/my-step-full.md)"
```

---

## 💡 Переваги підходу

### **1. Повна автоматизація**
- Один скрипт збирає всю інформацію з папки
- Автоматичне формування правильної структури markdown

### **2. Збереження контексту**  
- Вся інформація про крок в одному файлі
- ДРАКОН діаграми синхронізовані з кодом
- Тести та документація включені

### **3. Гнучкість використання**
- Можна використовувати як повний workflow
- Або покроково для детального контролю
- Легко додавати додаткові вимоги

### **4. Консистентність результатів**
- Claude отримує повну інформацію
- Генерований код відповідає існуючій структурі  
- ДРАКОН діаграми точно відображають логіку

Цей підхід дозволяє вам ефективно використовувати описову структуру кроку з усіма ДРАКОН схемами та додатковою інформацією як повноцінний аргумент для Claude CLI, забезпечуючи високоякісну генерацію та оптимізацію Motia кроків.