# DRAKON Testing Plugin - Швидкий старт 🚀

## Що це?

Автоматичне тестування DRAKON діаграм за допомогою DrakonWidget у браузері.

**За 3 хвилини:** Встановлення → Тестування → Звіт ✅

---

## Швидке встановлення

```bash
# 1. Перейти до каталогу
cd /home/vokov/motia/tools/drakon/testing

# 2. Запустити setup
chmod +x setup.sh
./setup.sh

# 3. Готово! 🎉
```

---

## Швидке тестування

### Варіант 1: Ручне тестування (завжди працює)

```bash
python3 drakon_widget_test.py steps/config-service/diagrams
```

Браузер відкриється автоматично. Перевірте візуально та натисніть Enter.

### Варіант 2: Автоматичне тестування (потрібен Playwright)

```bash
python3 drakon_widget_test.py steps/config-service/diagrams --automated
```

Результат у консолі + HTML звіт у `test_results/`

---

## Що встановлюється?

| Компонент | Обов'язковий? | Призначення |
|-----------|---------------|-------------|
| **DrakonWidget** | ✅ Так | Візуалізація діаграм у браузері |
| **Playwright** | ❌ Ні | Автоматичне тестування |
| **jq** | ❌ Ні | Валідація JSON (опціонально) |
| **SQLite** | ❌ Ні | Валідація .drn (опціонально) |

---

## Команди

```bash
# Ручне тестування
python3 drakon_widget_test.py <diagrams-dir>

# Автоматичне тестування
python3 drakon_widget_test.py <diagrams-dir> --automated

# Інтеграційний тест (все)
./integration_test.sh

# Тестувати конкретний Step
python3 drakon_widget_test.py steps/payment-service/diagrams --automated

# Тестувати всі Steps
for step in steps/*/diagrams; do
    python3 drakon_widget_test.py "$step" --automated
done
```

---

## Що тестується?

✅ **Завантаження** - DrakonWidget завантажується коректно  
✅ **Рендеринг** - Діаграма малюється без помилок  
✅ **Структура** - Всі іконки та зв'язки на місці  
✅ **Валідація** - Start/End іконки, цілісність зв'язків  
✅ **Продуктивність** - Час завантаження < 1 секунди

---

## Структура файлів

```
/home/vokov/motia/tools/drakon/testing/
├── setup.sh                    # ← Запустити спочатку
├── drakon_widget_test.py       # ← Основний тестер
├── integration_test.sh         # ← Повний тест
├── drakonwidget.js            # ← Завантажується автоматично
├── test_results/              # ← Результати тестів
│   ├── test_report.html       # ← HTML звіт
│   └── *_screenshot.png       # ← Скріншоти
└── README.md                  # ← Цей файл
```

---

## Приклад виводу

### Ручне тестування
```
============================================================
Testing: initialization.json
============================================================

✓ Created test page: initialization_test.html
✓ HTTP server started on http://localhost:8765
✓ Opening browser: http://localhost:8765/initialization_test.html

Press Enter when test complete...
```

### Автоматичне тестування
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

## Інтеграція з Workflow

Додайте до `unified-motia-workflow.sh`:

```bash
# Після генерації діаграм
./scripts/unified-motia-workflow.sh drakon my-step

# Автоматично протестувати
python3 tools/drakon/testing/drakon_widget_test.py \
    steps/my-step/diagrams \
    --automated
```

---

## Troubleshooting

### "DrakonWidget not found"
```bash
wget https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js
```

### "Playwright not installed"
```bash
pip3 install playwright
python3 -m playwright install chromium
```

### "Port already in use"
```bash
python3 drakon_widget_test.py diagrams/ --port 9000
```

---

## Посилання

📖 **Повна документація**: [DRAKON-WIDGET-TESTING-GUIDE.md](./DRAKON-WIDGET-TESTING-GUIDE.md)  
🔧 **DrakonWidget**: https://github.com/stepan-mitkin/drakonwidget  
🎯 **Motia Project**: `/home/vokov/motia/SESSION-CONTEXT.md`

---

## FAQ

**Q: Чи обов'язковий Playwright?**  
A: Ні. Без нього працює ручне тестування (браузер відкривається).

**Q: Як тестувати .drn файли?**  
A: DrakonWidget працює тільки з JSON. Конвертуйте спочатку:
```bash
python3 tools/drakon/converter/drakon_converter.py file.drn file.json
```

**Q: Чи потрібен інтернет?**  
A: Тільки для setup.sh (завантажує DrakonWidget). Після цього все працює локально.

**Q: Скільки часу займає тестування?**  
A: ~200ms на діаграму (автоматично) або ~30 сек (вручну).

---

## Швидкий старт за 1 хвилину

```bash
cd /home/vokov/motia/tools/drakon/testing
./setup.sh
python3 drakon_widget_test.py ../../steps/config-service/diagrams
```

**Готово!** Браузер відкриється з вашими діаграмами.

---

**Версія:** 1.0  
**Дата:** 2025-10-10  
**Статус:** Production-Ready ✅

Питання? → drakon.editor@gmail.com