# Приклади використання Motia Claude Workflow

## 1. Створення нового кроку з нуля
```bash
# Повний цикл: опис + генерація
./motia-claude-workflow.sh full-cycle user-processor event observer "Обробляє реєстрацію користувачів та відправляє welcome email"

# Результат: 
# - step-descriptions/user-processor-description.md
# - Згенерований код через Claude CLI
```

## 2. Оптимізація існуючого кроку
```bash
# У вас є папка з існуючим кроком
ls ./existing-user-step/
# handler.ts  config.json  schema.json  diagrams/  tests/  docs/

# Агрегація + оптимізація
./motia-claude-workflow.sh aggregate-and-generate ./existing-user-step observer

# Результат:
# - step-descriptions/existing-user-step-optimized.md
# - Оптимізований код через Claude CLI
```

## 3. Покроковий підхід
```bash
# Крок 1: Створити опис
./motia-claude-workflow.sh create-desc payment-processor api command "API для обробки платежів" python

# Крок 2: Згенерувати код
./motia-claude-workflow.sh generate step-descriptions/payment-processor-description.md command

# Результат: Максимальний контроль над процесом
```

## 4. Агрегація без генерації (для аналізу)
```bash
# Тільки агрегація існуючого кроку в markdown
./motia-claude-workflow.sh aggregate ./my-complex-step analysis-ready

# Результат: step-descriptions/analysis-ready.md для ручного аналізу
```

## 5. Ручна генерація з триступеневим промптом
```bash
# Після агрегації можна використовувати ручно
claude --append-system-prompt "$(cat CLAUDE.md)"        --append-system-prompt "$(cat patterns/strategy-pattern.md)"        -p "$(cat step-descriptions/my-step-complete.md)

ДОДАТКОВІ ВИМОГИ:
- Додай comprehensive error handling
- Включи retry механізм
- Створи детальну документацію"
```
