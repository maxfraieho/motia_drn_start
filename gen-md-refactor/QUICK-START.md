# ⚡ Швидкий старт Motia Markdown Service

## 🚀 Запуск за 30 секунд

```bash
# Крок 1: Перейти в директорію
cd /home/vokov/motia/gen-md-refactor

# Крок 2: Запустити інтерактивне меню
./motia-md-service.sh

# Крок 3: Обрати опцію 5 (Full Pipeline)
# Ввести: factory-pattern, ./steps/my-service

# Крок 4: Виконати згенеровану команду
```

---

## 📋 Основні команди

### Запуск меню

```bash
./motia-md-service.sh
```

### Запуск Python-сервісу напряму

```bash
python3 motia-md-service.py
```

### Конвертація ДРАКОН-схеми

```bash
./motia-drakon-converter.py input.json -o output.md
```

---

## 🎯 Типові сценарії

### Сценарій 1: Перший запуск (новий проєкт)

```bash
./motia-md-service.sh
# 1 - Deploy Structure
# 6 - Show Project Structure
# 9 - Exit
```

### Сценарій 2: Підготовка контексту для існуючого кроку

```bash
./motia-md-service.sh
# 5 - Full Pipeline
# Pattern: strategy-pattern
# Step: ./steps/auth-service
# Копіюємо та виконуємо згенеровану команду
```

### Сценарій 3: Тільки агрегація проєкту

```bash
./motia-md-service.sh
# 2 - Aggregate Project Context
# Результат: output/motia-project-context.md
```

---

## 📚 Корисні посилання

- **Повна документація:** [MOTIA-SERVICE-README.md](MOTIA-SERVICE-README.md)
- **Звіт про генерацію:** [GENERATION-REPORT.md](GENERATION-REPORT.md)
- **Опис ДРАКОН:** [drakon.md](drakon.md)

---

**Готово! 🎉**
