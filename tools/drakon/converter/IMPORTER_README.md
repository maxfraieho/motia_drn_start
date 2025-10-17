# DRAKON JSON Імпортер з Валідацією та Автокорекцією

**Версія:** 1.0
**Дата:** 2025-10-11
**Автор:** Claude Code + Motia AI Pipeline

## Огляд

Інтегрований імпортер DRAKON JSON діаграм з автоматичною валідацією та корекцією помилок. Використовує класи `DrakonValidator` та `DrakonCorrector` з модуля `drakon_tools.py`.

### Основні можливості

- ✅ **Автоматична валідація** діаграм через DrakonValidator
- 🔧 **Автокорекція помилок** через DrakonCorrector
- 💾 **Збереження виправлених діаграм** із суфіксом `_fixed.json`
- 📝 **Генерація лог-файлів** валідації та корекції
- 📦 **Batch-обробка** всіх JSON файлів у директорії
- 🚫 **Строгий режим** - блокування імпорту невалідних діаграм
- 🎯 **CLI-інтерфейс** для зручного використання

---

## Структура модуля

```
/home/vokov/motia/tools/drakon/converter/
├── drakon_json_importer.py     # Основний клас імпортера
├── drakon_import_cli.py        # CLI-інтерфейс
└── IMPORTER_README.md          # Ця документація

/home/vokov/motia/tools/drakon/fix/
├── drakon_tools.py             # Класи валідації та корекції
└── usage_example.py            # Приклади використання
```

---

## Встановлення

### 1. Перевірка залежностей

Модуль вже інтегрований у проєкт Motia. Переконайтесь, що Python 3.8+ встановлений:

```bash
python3 --version
```

### 2. Зробіть CLI виконуваним (опціонально)

```bash
chmod +x /home/vokov/motia/tools/drakon/converter/drakon_import_cli.py
```

### 3. Створіть alias для зручності (опціонально)

Додайте у `~/.bashrc` або `~/.zshrc`:

```bash
alias drakon-import='python3 /home/vokov/motia/tools/drakon/converter/drakon_import_cli.py'
```

Застосуйте зміни:

```bash
source ~/.bashrc
```

---

## Використання

### CLI-інтерфейс (рекомендовано)

#### Базові команди

```bash
# 1. Імпорт одного файлу з валідацією та автокорекцією
python3 drakon_import_cli.py import diagram.json

# 2. Імпорт усіх діаграм у директорії
python3 drakon_import_cli.py import ./diagrams/ --batch

# 3. Валідація без імпорту (швидка перевірка)
python3 drakon_import_cli.py validate diagram.json

# 4. Виправлення діаграми (зберігає _fixed.json)
python3 drakon_import_cli.py fix diagram.json

# 5. Batch-виправлення всіх діаграм
python3 drakon_import_cli.py fix ./diagrams/ --batch
```

#### Додаткові опції

```bash
# Строгий режим (не імпортує невалідні діаграми)
python3 drakon_import_cli.py import diagram.json --strict

# Вимкнути автокорекцію
python3 drakon_import_cli.py import diagram.json --no-fix

# Не зберігати лог-файли
python3 drakon_import_cli.py import diagram.json --no-logs

# Рекурсивний пошук у піддиректоріях
python3 drakon_import_cli.py import ./diagrams/ --batch --recursive

# Детальний вивід (verbose)
python3 drakon_import_cli.py validate diagram.json --verbose
```

### Програмне використання (Python API)

#### Імпорт одного файлу

```python
from pathlib import Path
from drakon_json_importer import DrakonJSONImporter

# Створення імпортера
importer = DrakonJSONImporter(
    strict_mode=False,  # Дозволити імпорт після виправлення
    auto_fix=True       # Автоматично виправляти помилки
)

# Імпорт діаграми
diagram, was_corrected = importer.import_diagram(
    Path("diagram.json"),
    save_logs=True  # Зберегти лог-файли
)

if diagram:
    print(f"✅ Діаграма імпортована успішно")
    if was_corrected:
        print(f"🔧 Діаграма була автоматично виправлена")
else:
    print(f"❌ Імпорт не вдався")
```

#### Batch-обробка директорії

```python
from pathlib import Path
from drakon_json_importer import DrakonJSONImporter

# Створення імпортера
importer = DrakonJSONImporter(auto_fix=True)

# Обробка всіх JSON у директорії
results = importer.import_directory(
    Path("./diagrams"),
    pattern="*.json",      # Патерн пошуку
    recursive=False,       # Не шукати у піддиректоріях
    save_logs=True         # Зберігати лог-файли
)

# Аналіз результатів
for file_path, diagram, was_corrected in results:
    if diagram:
        status = "🔧 виправлена" if was_corrected else "✅ валідна"
        print(f"{file_path.name}: {status}")
    else:
        print(f"{file_path.name}: ❌ помилка")
```

---

## Приклади сценаріїв

### Сценарій 1: Валідація існуючих діаграм

Перевірка всіх діаграм у проєкті без змін:

```bash
cd /home/vokov/motia/tools/drakon/testing
python3 ../converter/drakon_import_cli.py validate . --batch
```

**Вивід:**
```
📋 Валідація директорії: .
Файлів знайдено: 5

✅ initialization.json
❌ error-handling.json
✅ cleanup.json
❌ main-flow.json
✅ sample-initialization.json

Підсумок:
✅ Валідних: 3
❌ Невалідних: 2
```

### Сценарій 2: Виправлення невалідних діаграм

Автоматичне виправлення всіх проблемних діаграм:

```bash
python3 drakon_import_cli.py fix ./testing/ --batch --output ./testing/fixed/
```

**Результат:**
- Створюються файли `*_fixed.json` у директорії `./testing/fixed/`
- Генеруються лог-файли валідації та корекції
- Виводиться підсумкова статистика

### Сценарій 3: Імпорт з строгою валідацією

Імпорт тільки валідних діаграм (для production):

```bash
python3 drakon_import_cli.py import ./diagrams/ --batch --strict
```

**Поведінка:**
- Валідні діаграми імпортуються одразу
- Невалідні діаграми виправляються автоматично
- Якщо виправлення не допомогло → діаграма не імпортується

### Сценарій 4: Швидка перевірка перед комітом

Перевірка діаграм перед Git commit:

```bash
#!/bin/bash
# pre-commit hook

python3 tools/drakon/converter/drakon_import_cli.py validate \
  ./tools/drakon/testing/ --batch

if [ $? -ne 0 ]; then
    echo "❌ Є невалідні DRAKON діаграми. Виправте їх перед комітом."
    exit 1
fi
```

---

## Структура вихідних файлів

### Після імпорту з автокорекцією

```
diagrams/
├── my-diagram.json                    # Оригінальний файл (не змінюється)
├── my-diagram_fixed.json              # Виправлена діаграма
├── my-diagram_validation.log          # Лог валідації
└── my-diagram_correction.log          # Лог корекції
```

### Формат лог-файлів

#### `*_validation.log`

```
=== DRAKON VALIDATION LOG ===
Timestamp: 2025-10-11 15:30:45
File: my-diagram.json
Status: ✅ PASS
Note: Діаграма була автоматично виправлена

=== ПОМИЛКИ ===
(порожньо, якщо успішно)

=== ПОПЕРЕДЖЕННЯ ===
1. Діаграма містить декілька 'end' елементів
```

#### `*_correction.log`

```
=== DRAKON CORRECTION LOG ===
Timestamp: 2025-10-11 15:30:45
File: my-diagram.json
Status: ✅ SUCCESS

=== ВИКОНАНІ КОРЕКЦІЇ ===
1. Додано відсутнє поле 'name'
2. Додано відсутнє поле 'access'
3. Конвертовано 'items' зі списку в словник
4. Додано відсутній 'end' елемент
```

---

## Інтеграція з існуючими інструментами

### Використання разом з drakon_cli.py

```bash
# 1. Конвертація з псевдокоду в JSON
python3 drakon_cli.py --input algorithm.drakon --output algorithm.json

# 2. Валідація згенерованого JSON
python3 drakon_import_cli.py validate algorithm.json

# 3. Виправлення якщо потрібно
python3 drakon_import_cli.py fix algorithm.json
```

### Використання разом з convert_all_drakon.py

Модифікуйте `convert_all_drakon.py` для автоматичної валідації:

```python
from drakon_json_importer import DrakonJSONImporter

# Після конвертації
json_exporter.export_diagram(diagram_json)

# Додайте валідацію
importer = DrakonJSONImporter()
validated_diagram, was_corrected = importer.import_diagram(
    json_path,
    save_logs=True
)

if was_corrected:
    print(f"    ⚠️  Діаграма була автоматично виправлена")
```

---

## Налаштування

### Зміна поведінки валідатора

Модифікуйте `drakon_tools.py` для додавання/зміни правил валідації:

```python
# /home/vokov/motia/tools/drakon/fix/drakon_tools.py

class DrakonValidator:
    VALID_TYPES = {
        'action', 'question', 'branch', 'end', 'header', 'case',
        # Додайте нові типи тут
        'my-custom-type'
    }

    def _validate_items(self, items):
        # Додайте власні правила валідації
        for item_id, item in items.items():
            if item.get('type') == 'my-custom-type':
                # Ваша логіка валідації
                pass
```

### Зміна стратегії корекції

Модифікуйте `DrakonCorrector` для змін в автокорекції:

```python
class DrakonCorrector:
    def _fix_items(self, items):
        # Додайте власну логіку виправлення
        for item_id, item in items.items():
            if item.get('type') == 'action' and not item.get('content'):
                item['content'] = 'TODO: Add action description'
                self.corrections.append(f"Додано placeholder для {item_id}")
```

---

## Розширення функціональності

### Додавання нової команди до CLI

Редагуйте `drakon_import_cli.py`:

```python
def cmd_analyze(args):
    """Нова команда: аналіз складності діаграми"""
    # Ваша логіка
    pass

# У main():
analyze_parser = subparsers.add_parser('analyze', help='Аналіз діаграми')
analyze_parser.add_argument('input', type=str)

# У dispatch:
elif args.command == 'analyze':
    return cmd_analyze(args)
```

### Інтеграція з CI/CD

Приклад GitHub Actions:

```yaml
# .github/workflows/validate-drakon.yml
name: Validate DRAKON Diagrams

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Validate DRAKON diagrams
        run: |
          python3 tools/drakon/converter/drakon_import_cli.py \
            validate tools/drakon/testing/ --batch
```

---

## Troubleshooting

### Проблема: ModuleNotFoundError: No module named 'drakon_tools'

**Рішення:**
Перевірте, що `drakon_tools.py` знаходиться у `../fix/`:

```bash
ls /home/vokov/motia/tools/drakon/fix/drakon_tools.py
```

Або додайте шлях вручну:

```python
import sys
sys.path.insert(0, '/home/vokov/motia/tools/drakon/fix')
```

### Проблема: Діаграма не виправляється автоматично

**Діагностика:**

```bash
# 1. Перевірте помилки валідації
python3 drakon_import_cli.py validate problem.json --verbose

# 2. Подивіться лог корекції
cat problem_correction.log
```

**Можливі причини:**
- Складні структурні помилки (потребують ручного виправлення)
- Відсутні обов'язкові елементи (branch, end)
- Невалідний JSON (синтаксичні помилки)

### Проблема: Batch-обробка пропускає файли

**Перевірте:**
1. Чи правильний glob-патерн: `--pattern "*.json"`
2. Чи не мають файли суфікс `_fixed` (вони ігноруються)
3. Чи є права на читання файлів: `ls -la diagrams/`

---

## Статистика та метрики

Імпортер автоматично збирає статистику:

```python
importer = DrakonJSONImporter()
importer.import_directory(Path("./diagrams"), save_logs=True)

# Доступ до статистики
print(f"Всього: {importer.stats['total']}")
print(f"Валідних: {importer.stats['valid']}")
print(f"Виправлено: {importer.stats['corrected']}")
print(f"Помилок: {importer.stats['failed']}")
```

---

## Подальші кроки

### Заплановані покращення

- [ ] Підтримка виправлення `.drn` формату
- [ ] Інтеграція з DrakonHub API
- [ ] Автоматична конвертація між форматами
- [ ] Візуалізація помилок у термінальному UI
- [ ] Експорт звітів у HTML/PDF
- [ ] Інтеграція з pre-commit hooks

### Внесення змін

Щоб розширити функціональність:

1. **Додайте правила валідації** у `DrakonValidator`
2. **Додайте логіку корекції** у `DrakonCorrector`
3. **Додайте CLI-команди** у `drakon_import_cli.py`
4. **Оновіть документацію** у цьому README

---

## Довідка

### Посилання

- **Основний README проєкту:** `/home/vokov/motia/tools/drakon/README.md`
- **Валідатор та корректор:** `/home/vokov/motia/tools/drakon/fix/drakon_tools.py`
- **Приклади використання:** `/home/vokov/motia/tools/drakon/fix/usage_example.py`
- **Офіційний DRAKON:** [drakonhub.com](https://drakonhub.com)

### Допомога

```bash
# Загальна довідка
python3 drakon_import_cli.py --help

# Довідка по конкретній команді
python3 drakon_import_cli.py import --help
python3 drakon_import_cli.py validate --help
python3 drakon_import_cli.py fix --help
```

---

**Створено:** Claude Code + Motia AI Pipeline
**Версія:** 1.0
**Дата:** 2025-10-11
**Ліцензія:** Частина проєкту Motia
