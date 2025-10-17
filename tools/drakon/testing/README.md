# DrakonWidget Testing Plugin - Посібник користувача

## Огляд

Плагін для автоматичного тестування DRAKON діаграм за допомогою DrakonWidget у браузері. Перевіряє коректність завантаження, рендерингу та структури діаграм.

## Можливості

✅ **Автоматичне тестування** - Використання Playwright для headless браузера  
✅ **Ручне тестування** - Відкриття в браузері для візуальної перевірки  
✅ **Структурна валідація** - Перевірка зв'язків, іконок, форматування  
✅ **Скріншоти** - Автоматичне створення знімків екрану  
✅ **HTML звіти** - Детальні звіти про тестування  
✅ **Підтримка декількох діаграм** - Тестування цілих каталогів

---

## Встановлення

### 1. Завантажити DrakonWidget

```bash
cd /home/vokov/motia/tools/drakon/testing

# Клонувати репозиторій
git clone https://github.com/stepan-mitkin/drakonwidget.git
cp drakonwidget/drakonwidget.js ./
```

### 2. Встановити залежності (для автоматичного тестування)

```bash
# Встановити Playwright
pip install playwright

# Завантажити браузери
playwright install chromium
```

### 3. Зробити скрипт виконуваним

```bash
chmod +x /home/vokov/motia/tools/drakon/testing/drakon_widget_test.py
```

---

## Використання

### Швидкий старт - Ручне тестування

```bash
cd /home/vokov/motia

# Тестувати всі діаграми в Step
python3 tools/drakon/testing/drakon_widget_test.py \
  steps/config-service/diagrams

# Браузер відкриється автоматично
# Перевірте візуально та натисніть Enter для наступної діаграми
```

### Автоматичне тестування

```bash
# Потрібен Playwright
python3 tools/drakon/testing/drakon_widget_test.py \
  steps/config-service/diagrams \
  --automated

# Результати:
# ✓ PASS | initialization.json | 234ms | All 9 tests passed
# ✓ PASS | main-flow.json | 189ms | All 9 tests passed
# ✗ FAIL | error-handling.json | 156ms | 2 test(s) failed: Link Integrity, End Icon
```

### Тестування конкретного Step

```bash
# Один Step
python3 tools/drakon/testing/drakon_widget_test.py \
  steps/database-service/diagrams \
  --automated \
  --output-dir test_results/database-service

# Всі Steps
for step in steps/*/diagrams; do
  python3 tools/drakon/testing/drakon_widget_test.py "$step" --automated
done
```

---

## Параметри командного рядка

| Параметр | Опис | За замовчуванням |
|----------|------|------------------|
| `diagrams_dir` | Каталог з JSON файлами | (обов'язково) |
| `--widget-path` | Шлях до drakonwidget.js | `./drakonwidget.js` |
| `--output-dir` | Каталог для результатів | `./test_results` |
| `--automated` | Автоматичне тестування | `False` (ручне) |
| `--port` | Порт HTTP сервера | `8765` |

---

## Що тестується?

### 1. Завантаження компонентів
- ✓ DrakonWidget завантажується
- ✓ Конфігурація створюється
- ✓ Widget рендериться в DOM

### 2. Завантаження діаграми
- ✓ Діаграма завантажується з JSON
- ✓ Шрифти завантажуються
- ✓ Діаграма малюється

### 3. Структурна валідація
- ✓ Кількість іконок > 0
- ✓ Наявність start іконки (branch)
- ✓ Наявність end іконки
- ✓ Всі зв'язки (links) валідні

### 4. Цілісність зв'язків
- ✓ Всі `one` посилання існують
- ✓ Всі `two` посилання існують
- ✓ Немає циклічних посилань (якщо не loop)

---

## Приклад виводу

### Консоль

```
============================================================
Testing: initialization.json
============================================================

✓ Created test page: initialization_test.html
✓ HTTP server started on http://localhost:8765
✓ Opening browser: http://localhost:8765/initialization_test.html

============================================================
Manual test instructions:
1. Check that diagram loads without errors
2. Verify all icons are visible
3. Verify lines connect correctly
4. Check test results at bottom of page
5. Close browser when done
============================================================

Press Enter when test complete...
```

### Автоматичний режим

```
Found 4 diagram(s) to test
✓ PASS | initialization.json | 234ms | All 9 tests passed
✓ PASS | main-flow.json | 189ms | All 9 tests passed
✓ PASS | error-handling.json | 203ms | All 9 tests passed
✓ PASS | cleanup.json | 178ms | All 9 tests passed

✓ Test report: test_results/test_report.html

Results: 4/4 passed
```

---

## HTML звіт

Автоматично генерується `test_report.html`:

```
DRAKON Widget Test Report
Generated: 2025-10-10 15:30:45

┌─────────────┬──────┬────────┐
│ Total Tests │ Pass │  Fail  │
│      4      │  4   │   0    │
└─────────────┴──────┴────────┘

Test Results
╔════════════════════════╦═══════╦══════════╦═══════════════════════╗
║ Diagram                ║ Status║ Duration ║ Message               ║
╠════════════════════════╬═══════╬══════════╬═══════════════════════╣
║ initialization.json    ║ ✓ PASS║   234ms  ║ All 9 tests passed    ║
║ main-flow.json         ║ ✓ PASS║   189ms  ║ All 9 tests passed    ║
║ error-handling.json    ║ ✓ PASS║   203ms  ║ All 9 tests passed    ║
║ cleanup.json           ║ ✓ PASS║   178ms  ║ All 9 tests passed    ║
╚════════════════════════╩═══════╩══════════╩═══════════════════════╝
```

---

## Інтеграція з CI/CD

### GitHub Actions

```yaml
name: Test DRAKON Diagrams

on: [push, pull_request]

jobs:
  test-drakon:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install playwright
        playwright install chromium
    
    - name: Download DrakonWidget
      run: |
        wget https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js \
          -O tools/drakon/testing/drakonwidget.js
    
    - name: Test all DRAKON diagrams
      run: |
        python3 tools/drakon/testing/drakon_widget_test.py \
          steps/config-service/diagrams \
          --automated \
          --output-dir test_results
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: drakon-test-results
        path: test_results/
```

### GitLab CI

```yaml
test-drakon:
  image: mcr.microsoft.com/playwright/python:v1.40.0-jammy
  
  script:
    - pip install playwright
    - playwright install chromium
    - wget https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js
    - python3 tools/drakon/testing/drakon_widget_test.py steps/*/diagrams --automated
  
  artifacts:
    when: always
    paths:
      - test_results/
    reports:
      junit: test_results/junit.xml
```

---

## Інтеграція з unified-motia-workflow.sh

Додайте тестування до pipeline:

```bash
# У файлі /home/vokov/motia/scripts/unified-motia-workflow.sh

test_drakon_diagrams() {
    local step_name="$1"
    local diagrams_dir="${STEPS_DIR}/${step_name}/diagrams"
    
    log_step "Testing DRAKON diagrams for ${step_name}..."
    
    if [[ ! -d "$diagrams_dir" ]]; then
        log_error "No diagrams directory found: $diagrams_dir"
        return 1
    fi
    
    # Check if DrakonWidget exists
    local widget_path="${PROJECT_ROOT}/tools/drakon/testing/drakonwidget.js"
    if [[ ! -f "$widget_path" ]]; then
        log_warning "DrakonWidget not found, downloading..."
        wget -q https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js \
             -O "$widget_path"
    fi
    
    # Run automated tests if Playwright available
    if python3 -c "import playwright" 2>/dev/null; then
        log_info "Running automated tests..."
        python3 "${PROJECT_ROOT}/tools/drakon/testing/drakon_widget_test.py" \
            "$diagrams_dir" \
            --automated \
            --output-dir "${PROJECT_ROOT}/test_results/${step_name}"
    else
        log_info "Playwright not installed, skipping automated tests"
        log_info "To install: pip install playwright && playwright install"
    fi
}

# Додати до команди full-pipeline
full_pipeline() {
    # ... existing code ...
    
    # Generate DRAKON diagrams
    log_step "Step 3/6: Generating DRAKON diagrams..."
    generate_drakon_diagrams "$STEP_NAME"
    
    # Test DRAKON diagrams (NEW)
    log_step "Step 4/6: Testing DRAKON diagrams..."
    test_drakon_diagrams "$STEP_NAME"
    
    # Aggregate markdown
    log_step "Step 5/6: Aggregating markdown..."
    aggregate_step "$STEP_NAME"
    
    # ... rest of pipeline ...
}

# Додати команду test-drakon
case "$COMMAND" in
    test-drakon)
        if [[ $# -lt 2 ]]; then
            log_error "Usage: $0 test-drakon <step-name>"
            exit 1
        fi
        test_drakon_diagrams "$2"
        ;;
    # ... existing commands ...
esac
```

---

## Використання з Python API

```python
#!/usr/bin/env python3
"""
Приклад програмного використання тестера
"""

from pathlib import Path
from drakon_widget_test import DrakonWidgetTester, TestResult

# Ініціалізувати тестер
tester = DrakonWidgetTester(
    drakon_widget_path=Path("./drakonwidget.js"),
    test_output_dir=Path("./my_tests"),
    port=8765
)

# Тест 1: Ручний тест однієї діаграми
tester.test_diagram_manual(Path("steps/my-step/diagrams/main-flow.json"))

# Тест 2: Автоматичний тест
result = tester.test_diagram_automated(
    Path("steps/my-step/diagrams/initialization.json")
)

if result.passed:
    print(f"✓ {result.name}: {result.message}")
else:
    print(f"✗ {result.name}: {result.message}")

# Тест 3: Тестувати всі діаграми
results = tester.test_all_diagrams(
    diagrams_dir=Path("steps/my-step/diagrams"),
    automated=True
)

# Згенерувати звіт
report_file = tester.generate_report(results)
print(f"Report: {report_file}")

# Статистика
passed = sum(1 for r in results if r.passed)
print(f"Results: {passed}/{len(results)} passed")
```

---

## Налагодження

### Проблема: "DrakonWidget not found"

**Рішення:**
```bash
cd /home/vokov/motia/tools/drakon/testing
wget https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js
```

### Проблема: "Playwright not installed"

**Рішення:**
```bash
pip install playwright
playwright install chromium
```

### Проблема: "Port already in use"

**Рішення:**
```bash
# Використати інший порт
python3 drakon_widget_test.py diagrams/ --port 9000
```

### Проблема: Браузер не відкривається

**Рішення:**
```bash
# Перевірити HTTP сервер
curl http://localhost:8765/

# Вручну відкрити URL
firefox http://localhost:8765/test_diagram_test.html
```

---

## Розширені можливості

### 1. Кастомна конфігурація DrakonWidget

Редагуйте `create_test_html()` для зміни теми:

```python
config = {
    'theme': {
        'background': '#1e1e1e',  # Темна тема
        'iconBack': '#2d2d2d',
        'iconBorder': '#555',
        'color': '#ffffff'
    }
}
```

### 2. Додаткові тести

Додайте власні перевірки в HTML:

```javascript
// Test 9: Custom validation
var customCheck = myValidationFunction(diagramData);
addResult('Custom Check', customCheck, 'My validation');
```

### 3. Експорт скріншотів

```python
# У automated mode скріншоти створюються автоматично
# Знайти їх у test_results/<diagram>_screenshot.png
```

### 4. Візуальне порівняння (Visual Regression)

```python
# Зберегти базовий скріншот
baseline_screenshot = "baselines/main-flow.png"

# Порівняти з поточним
from PIL import Image
import imagehash

baseline = Image.open(baseline_screenshot)
current = Image.open("test_results/main-flow_screenshot.png")

hash1 = imagehash.average_hash(baseline)
hash2 = imagehash.average_hash(current)

difference = hash1 - hash2
if difference > 5:
    print(f"Visual difference detected: {difference}")
```

---

## Приклади використання

### Приклад 1: CI/CD Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Testing DRAKON diagrams..."

python3 tools/drakon/testing/drakon_widget_test.py \
    steps/*/diagrams \
    --automated

if [ $? -ne 0 ]; then
    echo "DRAKON tests failed. Commit aborted."
    exit 1
fi

echo "✓ All DRAKON tests passed"
```

### Приклад 2: Тестування після генерації

```bash
# Згенерувати діаграми
./scripts/unified-motia-workflow.sh drakon payment-service

# Відразу протестувати
python3 tools/drakon/testing/drakon_widget_test.py \
    steps/payment-service/diagrams \
    --automated
```

### Приклад 3: Batch тестування

```bash
#!/bin/bash
# test_all_steps.sh

FAILED=0

for step_dir in steps/*/diagrams; do
    step_name=$(basename $(dirname "$step_dir"))
    echo "Testing $step_name..."
    
    python3 tools/drakon/testing/drakon_widget_test.py \
        "$step_dir" \
        --automated \
        --output-dir "test_results/$step_name"
    
    if [ $? -ne 0 ]; then
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "============================================"
if [ $FAILED -eq 0 ]; then
    echo "✓ All Steps passed DRAKON tests"
else
    echo "✗ $FAILED Step(s) failed DRAKON tests"
    exit 1
fi
```

---

## Метрики продуктивності

### Типовий час виконання

| Операція | Час (ручний) | Час (автоматичний) |
|----------|--------------|-------------------|
| 1 діаграма | ~30 сек | ~200 мс |
| 4 діаграми (Step) | ~2 хв | ~800 мс |
| 15 Steps (60 діаграм) | ~30 хв | ~12 сек |

### Оптимізація

```python
# Паралельне тестування
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(tester.test_diagram_automated, json_file)
        for json_file in json_files
    ]
    
    results = [f.result() for f in futures]
```

---

## FAQ

**Q: Чи можна тестувати .drn файли?**  
A: Ні, DrakonWidget працює тільки з JSON. Спочатку конвертуйте:
```bash
python3 tools/drakon/converter/drakon_converter.py diagram.drn diagram.json
python3 tools/drakon/testing/drakon_widget_test.py . --automated
```

**Q: Як тестувати без браузера?**  
A: Використовуйте структурний валідатор:
```python
from drakon_widget_test import DiagramValidator
errors = DiagramValidator.validate_json(diagram)
```

**Q: Чи потрібен інтернет?**  
A: Ні, всі компоненти локальні. Але для завантаження DrakonWidget спочатку потрібен інтернет.

**Q: Як інтегрувати з існуючими тестами?**  
A: Додайте до pytest:
```python
def test_drakon_diagrams():
    tester = DrakonWidgetTester(...)
    results = tester.test_all_diagrams(..., automated=True)
    assert all(r.passed for r in results)
```

---

## Структура файлів

```
/home/vokov/motia/tools/drakon/testing/
├── drakon_widget_test.py         # Основний скрипт
├── drakonwidget.js               # DrakonWidget (завантажити)
├── test_results/                 # Результати тестів
│   ├── test_report.html          # HTML звіт
│   ├── initialization_test.html  # Тестові сторінки
│   ├── initialization_screenshot.png
│   ├── main-flow_test.html
│   └── ...
└── README.md                     # Цей файл
```

---

## Швидкий старт (5 хвилин)

```bash
# 1. Перейти до каталогу
cd /home/vokov/motia/tools/drakon/testing

# 2. Завантажити DrakonWidget
wget https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js

# 3. (Опціонально) Встановити Playwright
pip install playwright
playwright install chromium

# 4. Тестувати діаграми
python3 drakon_widget_test.py ../../steps/config-service/diagrams --automated

# 5. Переглянути звіт
firefox test_results/test_report.html
```

**Готово!** Тепер ви можете автоматично тестувати всі DRAKON діаграми.

---

## Контакти

**Питання?** Створіть issue у Motia репозиторії або напишіть:
- Email: drakon.editor@gmail.com (офіційна підтримка DrakonWidget)
- GitHub: https://github.com/stepan-mitkin/drakonwidget

---

**Версія:** 1.0  
**Дата:** 2025-10-10  
**Статус:** Production-Ready ✅