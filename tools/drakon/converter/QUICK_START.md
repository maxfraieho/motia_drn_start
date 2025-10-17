# DRAKON Імпортер - Швидкий Старт

**5 хвилин до першого запуску**

---

## 1️⃣ Перевірка інсталяції

```bash
cd /home/vokov/motia/tools/drakon/converter

# Перевірте що всі файли на місці
ls -la drakon_json_importer.py drakon_import_cli.py

# Перевірте drakon_tools.py
ls -la ../fix/drakon_tools.py
```

---

## 2️⃣ Запуск тесту

```bash
# Швидкий тест функціональності
python3 test_importer.py
```

**Очікуваний результат:**
```
🎉 ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!
```

---

## 3️⃣ Базові команди

### Валідація одного файлу

```bash
python3 drakon_import_cli.py validate diagram.json
```

### Валідація директорії

```bash
python3 drakon_import_cli.py validate ../testing/ --batch
```

### Імпорт з автовиправленням

```bash
python3 drakon_import_cli.py import diagram.json
```

### Виправлення діаграми

```bash
python3 drakon_import_cli.py fix diagram.json
```

---

## 4️⃣ Що робить імпортер?

```
┌─────────────────┐
│  diagram.json   │  ← Вхідна діаграма
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │Валідація│  ✅ Перевірка структури
    └────┬────┘
         │
    [Помилки?]
         │
    ┌────┴─────┐
    Ні        Так
    │           │
    ▼           ▼
[Імпорт]   ┌──────────┐
           │Корекція  │  🔧 Автовиправлення
           └────┬─────┘
                │
                ▼
        ┌────────────────┐
        │ diagram_fixed. │  💾 Виправлена діаграма
        │      json      │
        └────────────────┘
                │
                ▼
        ┌────────────────┐
        │  Лог-файли:    │  📝 Звіти
        │  - validation  │
        │  - correction  │
        └────────────────┘
```

---

## 5️⃣ Приклад використання

```bash
# Створіть тестову діаграму з помилками
cat > test.json << 'EOF'
{
  "items": [
    {"type": "action", "text": "Do something"}
  ]
}
EOF

# Спробуйте валідувати
python3 drakon_import_cli.py validate test.json

# Виведе:
# ❌ Знайдено помилки:
# 1. Відсутнє обов'язкове поле 'name'
# 2. Відсутнє обов'язкове поле 'access'
# 3. Поле 'items' повинно бути словником

# Виправте автоматично
python3 drakon_import_cli.py fix test.json

# Перевірте результат
cat test_fixed.json
cat test_correction.log
```

---

## 6️⃣ Режими роботи

| Режим          | Команда    | Що робить                                    |
|----------------|------------|----------------------------------------------|
| **Валідація**  | `validate` | Перевіряє діаграми (не змінює файли)        |
| **Виправлення**| `fix`      | Створює `_fixed.json` файли                  |
| **Імпорт**     | `import`   | Валідує + виправляє + створює логи          |

---

## 7️⃣ Опції CLI

### Batch-режим
```bash
--batch    # Обробити всю директорію
```

### Строгий режим
```bash
--strict   # Не імпортувати невалідні діаграми
```

### Вимкнути автокорекцію
```bash
--no-fix   # Тільки валідація, без виправлень
```

### Без логів
```bash
--no-logs  # Не створювати лог-файли
```

### Детальний вивід
```bash
--verbose  # Показати всі деталі
```

---

## 8️⃣ Python API

```python
from pathlib import Path
from drakon_json_importer import DrakonJSONImporter

# Створіть імпортер
importer = DrakonJSONImporter(auto_fix=True)

# Імпортуйте діаграму
diagram, was_corrected = importer.import_diagram(
    Path("diagram.json"),
    save_logs=True
)

# Перевірте результат
if diagram:
    print("✅ Успішно!")
    if was_corrected:
        print("🔧 Діаграма була виправлена")
```

---

## 9️⃣ Структура вихідних файлів

```
diagrams/
├── my-diagram.json              # Оригінал (не змінюється)
├── my-diagram_fixed.json        # Виправлена версія
├── my-diagram_validation.log    # Звіт валідації
└── my-diagram_correction.log    # Звіт корекції
```

---

## 🔟 Довідка

```bash
# Загальна довідка
python3 drakon_import_cli.py --help

# Довідка по команді
python3 drakon_import_cli.py import --help
python3 drakon_import_cli.py validate --help
python3 drakon_import_cli.py fix --help
```

---

## 📚 Детальна документація

- **Повна документація:** `IMPORTER_README.md`
- **Звіт інтеграції:** `INTEGRATION_REPORT.md`
- **Тести:** `test_importer.py`

---

## 🐛 Проблеми?

### ModuleNotFoundError: drakon_tools

```bash
# Перевірте що файл існує
ls ../fix/drakon_tools.py

# Якщо потрібно, вкажіть шлях у drakon_json_importer.py:
# sys.path.insert(0, '/повний/шлях/до/fix')
```

### Файли не обробляються в batch

```bash
# Перевірте glob-патерн
ls diagrams/*.json

# _fixed файли ігноруються автоматично
ls diagrams/*_fixed.json
```

---

## ⚡ Швидкі команди

```bash
# Перевірити все в testing/
python3 drakon_import_cli.py validate ../testing/ --batch

# Виправити все в testing/
python3 drakon_import_cli.py fix ../testing/ --batch

# Імпортувати з детальним виводом
python3 drakon_import_cli.py import diagram.json --verbose
```

---

**Готово! Можна працювати! 🚀**

Для детальної інформації дивіться `IMPORTER_README.md`
