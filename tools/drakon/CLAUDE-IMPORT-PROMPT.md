# DRAKON Knowledge Import - Claude CLI Prompt

**Version:** 1.0
**Date:** 2025-10-10
**Purpose:** Інтелектуальний імпорт результатів Perplexity дослідження для валідації та оптимізації DRAKON конвертерів

---

## Інструкція з використання

1. Запустіть Perplexity дослідження: `cd perplexity && ./run_perplexity_lab.sh research`
2. Дочекайтесь завершення та збережіть результат у файл `drndew.md`
3. Відкрийте новий сеанс Claude CLI
4. Скопіюйте цей промпт та замініть `[ВСТАВИТИ ВМІСТ drndew.md]` на реальний вміст
5. Виконайте промпт

---

## 🎯 Промпт для Claude CLI

```markdown
# Аналіз та імпорт результатів DRAKON дослідження

## Контекст проекту

Я працюю над модулем **DRAKON Pipeline** для фреймворку Motia - системи автоматичної генерації візуальних діаграм алгоритмів.

**Розташування:** `/home/vokov/motia/tools/drakon/`

**Поточні компоненти:**
1. `converter/drakon_to_drn.py` - SQLite (.drn) exporter для DRAKON Editor (desktop)
2. `converter/drakon_to_json.py` - JSON exporter для DrakonWidget/DrakonHub (web)
3. `converter/generate_step_diagrams.py` - Генератор діаграм для Motia Steps

**Мета:** Валідація та оптимізація конвертерів на основі глибокого дослідження офіційних специфікацій DRAKON.

---

## 📥 Результати Perplexity дослідження

<details>
<summary>Повний вміст файлу drndew.md (клікніть для розгортання)</summary>

[ВСТАВИТИ ВМІСТ drndew.md]

</details>

---

## 🔍 Завдання

### Phase 1: Валідація поточних конвертерів

**1.1 SQLite Schema Validation**

Порівняй знайдену специфікацію `.drn` формату з поточною реалізацією:

**Поточна схема** (`converter/drakon_to_drn.py`):
```python
CREATE TABLE diagrams (
    diagram_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    origin_x INTEGER DEFAULT 0,
    origin_y INTEGER DEFAULT 0,
    zoom REAL DEFAULT 1.0
);

CREATE TABLE icons (
    icon_id INTEGER PRIMARY KEY,
    diagram_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    w INTEGER NOT NULL,
    h INTEGER NOT NULL,
    text TEXT,
    format TEXT
);

CREATE TABLE links (
    link_id INTEGER PRIMARY KEY,
    diagram_id INTEGER NOT NULL,
    src_icon_id INTEGER NOT NULL,
    dst_icon_id INTEGER NOT NULL,
    vertices TEXT DEFAULT '[]'
);

CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

**Питання для аналізу:**
- ✅ Чи всі таблиці присутні?
- ✅ Чи всі обов'язкові поля є?
- ⚠️ Чи є missing поля, які згадуються в дослідженні?
- ⚠️ Чи типи даних коректні?
- ⚠️ Чи є додаткові таблиці (наприклад, `settings`, `vertices`, `texts`)?

**1.2 JSON Format Validation**

Порівняй JSON структуру з DrakonWidget/DrakonHub специфікацією:

**Поточна структура** (`converter/drakon_to_json.py`):
```json
{
  "diagram": {
    "name": "...",
    "type": "drakon",
    "nodes": [
      {
        "id": 1,
        "type": "action",
        "text": "...",
        "x": 200,
        "y": 100,
        "width": 120,
        "height": 40
      }
    ],
    "links": [
      {
        "id": 1,
        "from": 1,
        "to": 2,
        "points": []
      }
    ],
    "settings": {
      "gridSize": 20,
      "zoom": 1.0,
      "theme": "default"
    }
  }
}
```

**Питання:**
- ✅ Чи структура відповідає офіційній?
- ⚠️ Чи всі optional fields враховані?
- ⚠️ Чи є додаткові metadata поля?

**1.3 Icon Types Coverage**

Поточна підтримка: 12 типів
```
action, question, select, case,
loopbegin, loopend, foreach,
branch, address,
start, end, parameters, comment
```

**Питання:**
- ✅ Чи це повний список?
- ⚠️ Чи є інші типи в офіційній документації?
- ⚠️ Чи правильні string identifiers?

---

### Phase 2: Extraction - Витягнути structured data

**2.1 Icon Types Reference**

Створи JSON файл `knowledge_base/icon_types.json`:

```json
{
  "version": "1.0",
  "source": "Perplexity Research 2025-10-10",
  "icon_types": [
    {
      "id": "action",
      "display_name": "Action",
      "description": "Represents an operation or action",
      "drn_type": "action",
      "json_type": "action",
      "required_links": {
        "min": 1,
        "max": 1,
        "description": "Single input, single output"
      },
      "default_dimensions": {
        "width": 120,
        "height": 40
      },
      "layout_rules": [
        "Can be placed on royal road",
        "Vertical flow preferred"
      ],
      "examples": [
        "Process data",
        "Calculate result",
        "Save to database"
      ]
    },
    {
      "id": "question",
      "display_name": "Question",
      "description": "Decision point (if/then/else)",
      "drn_type": "question",
      "json_type": "question",
      "required_links": {
        "min": 1,
        "max": 2,
        "description": "One input, two outputs (YES down, NO right)"
      },
      "default_dimensions": {
        "width": 120,
        "height": 60
      },
      "layout_rules": [
        "YES branch goes down",
        "NO branch goes right",
        "Must have condition text"
      ],
      "examples": [
        "Is valid?",
        "Has permissions?",
        "Error occurred?"
      ]
    }
    // ... для всіх знайдених типів
  ]
}
```

**2.2 Complete SQLite Schema**

Якщо знайдено додаткові таблиці/поля, створи:
`knowledge_base/drn_complete_schema.sql`

**2.3 Complete JSON Schema**

Створи TypeScript definitions або JSON Schema:
`knowledge_base/json_schema.ts`

**2.4 Validation Rules**

Створи `knowledge_base/validation_rules.json`:

```json
{
  "structural_constraints": [
    {
      "rule": "must_have_start",
      "description": "Every diagram must have at least one start icon",
      "severity": "error"
    },
    {
      "rule": "royal_road_principle",
      "description": "Main execution path must be vertical",
      "severity": "warning"
    },
    {
      "rule": "no_crossing_lines",
      "description": "Links should not cross each other",
      "severity": "warning"
    }
  ],
  "icon_constraints": {
    "question": {
      "required_outgoing_links": 2,
      "required_text": true,
      "description": "Question icon must have condition text and 2 branches"
    },
    "loopbegin": {
      "must_pair_with": "loopend",
      "description": "Loop begin must have matching loop end"
    }
  },
  "layout_constraints": {
    "vertical_spacing": {
      "min": 60,
      "default": 80,
      "description": "Minimum vertical spacing between icons"
    },
    "horizontal_spacing": {
      "min": 40,
      "default": 60,
      "description": "Horizontal spacing for branches"
    }
  }
}
```

**2.5 Code Samples**

Витягни всі code samples з дослідження та збережи в:
- `knowledge_base/code_samples/example_1_*.py`
- `knowledge_base/code_samples/example_2_*.js`
- і т.д.

**2.6 Conversion Guidelines**

Створи `knowledge_base/conversion_guide.md`:

```markdown
# DRAKON Format Conversion Guide

## .drn → .json

### Step 1: Read SQLite database
[конкретні кроки з дослідження]

### Step 2: Map tables to JSON
[mapping rules]

### Step 3: Handle special cases
[edge cases]

## .json → .drn

[зворотний процес]

## Common Pitfalls

1. ...
2. ...
```

---

### Phase 3: Code Optimization

**3.1 Identify Issues**

На основі порівняння, створи:
`VALIDATION-REPORT.md`

```markdown
# DRAKON Converters Validation Report

**Date:** 2025-10-10
**Based on:** Perplexity Deep Research

## Summary

✅ **Correct:** X items
⚠️ **Needs attention:** Y items
❌ **Missing:** Z items

## Detailed Findings

### SQLite Schema

#### ✅ Correct
- Tables: diagrams, icons, links, meta
- Primary keys: correct
- ...

#### ⚠️ Needs Attention
- Field `icons.format` - found additional metadata in research
- Missing table: `settings` (mentioned in official docs)
- ...

#### ❌ Missing
- Field `icons.color` - found in DrakonHub samples
- ...

### JSON Format

[аналогічно]

### Icon Types

[аналогічно]

## Recommendations

1. Add missing fields to SQLite schema
2. Update JSON exporter with optional metadata
3. Implement validation rules
4. ...
```

**3.2 Generate Code Patches**

Створи конкретні patches для виправлення:

**Patch 1: `drakon_to_drn.py` updates**

```python
# ADD: Missing fields to icons table

CREATE TABLE icons (
    icon_id INTEGER PRIMARY KEY,
    diagram_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    w INTEGER NOT NULL,
    h INTEGER NOT NULL,
    text TEXT,
    format TEXT,

    -- NEW FIELDS (if found in research)
    color TEXT,
    selected INTEGER DEFAULT 0,
    -- ... інші знайдені поля
);

# ADD: Missing settings table (if needed)

CREATE TABLE settings (
    diagram_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (diagram_id, key)
);
```

**Patch 2: `drakon_to_json.py` updates**

```python
# ADD: Optional metadata fields

@dataclass
class DrakonNode:
    id: int
    type: str
    text: str
    x: int
    y: int
    width: int
    height: int

    # NEW: Optional fields from research
    color: Optional[str] = None
    selected: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
```

**3.3 Create Updated Versions**

Якщо потрібно, створи повністю оновлені версії:
- `converter/drakon_to_drn_v2.py`
- `converter/drakon_to_json_v2.py`

---

### Phase 4: Testing & Samples

**4.1 Sample Files**

Якщо дослідження містить приклади `.drn` або `.json` файлів:
- Збережи їх у `knowledge_base/samples/`
- Створи тести для їх парсингу

**4.2 Test Cases**

Створи `knowledge_base/test_cases.json`:

```json
{
  "test_cases": [
    {
      "name": "Simple action flow",
      "icons": [
        {"type": "start", "text": "Begin"},
        {"type": "action", "text": "Do something"},
        {"type": "end", "text": "Done"}
      ],
      "expected_links": 2,
      "expected_validation": "pass"
    },
    {
      "name": "Question with branches",
      "icons": [
        {"type": "start", "text": "Start"},
        {"type": "question", "text": "Check condition?"},
        {"type": "action", "text": "YES path"},
        {"type": "action", "text": "NO path"},
        {"type": "end", "text": "End"}
      ],
      "expected_links": 5,
      "expected_validation": "pass"
    }
  ]
}
```

---

## 📊 Deliverables

Після аналізу, створи наступні файли:

### Required (обов'язково)

1. ✅ `knowledge_base/icon_types.json` - Повний довідник icon types
2. ✅ `knowledge_base/validation_rules.json` - Правила валідації
3. ✅ `VALIDATION-REPORT.md` - Звіт про валідацію конвертерів
4. ✅ `knowledge_base/RESEARCH-SUMMARY.md` - Короткий summary ключових findings

### Optional (якщо знайдено в дослідженні)

5. ⭐ `knowledge_base/drn_complete_schema.sql` - Повна SQL схема
6. ⭐ `knowledge_base/json_schema.ts` - TypeScript types
7. ⭐ `knowledge_base/conversion_guide.md` - Гайд з конвертації
8. ⭐ `knowledge_base/code_samples/` - Приклади коду
9. ⭐ `knowledge_base/samples/` - Приклади файлів
10. ⭐ `knowledge_base/test_cases.json` - Test cases

### Code Updates (якщо потрібно)

11. 🔧 `CODE-PATCHES.md` - Конкретні patches для існуючих файлів
12. 🔧 `converter/drakon_to_drn_v2.py` - Оновлена версія (optional)
13. 🔧 `converter/drakon_to_json_v2.py` - Оновлена версія (optional)

---

## 🎯 Формат виводу

### Структура відповіді

```markdown
# DRAKON Knowledge Import - Результати

## Executive Summary

**Дата аналізу:** 2025-10-10
**Джерело:** Perplexity Deep Research
**Якість дослідження:** [Excellent/Good/Fair/Poor]

### Ключові findings

1. [Finding 1]
2. [Finding 2]
3. ...

### Критичні issues

1. [Issue 1]
2. [Issue 2]

---

## Phase 1: Validation Results

### SQLite Schema
✅ Correct: X items
⚠️ Needs update: Y items
❌ Missing: Z items

[детальний розбір]

### JSON Format
[аналогічно]

### Icon Types
[аналогічно]

---

## Phase 2: Extracted Knowledge

[вміст створених JSON файлів]

---

## Phase 3: Code Recommendations

[конкретні patches та рекомендації]

---

## Phase 4: Next Steps

1. [ ] Apply patches to converters
2. [ ] Add validation rules
3. [ ] Create test suite
4. [ ] ...

---

## Appendix: Created Files

[список всіх створених файлів з коротким описом]
```

---

## ✅ Success Criteria

Вважаю завдання виконаним, коли:

1. ✅ **Validation complete** - Порівняно всі аспекти поточних конвертерів з дослідженням
2. ✅ **Knowledge extracted** - Створено structured JSON files з усіма знаннями
3. ✅ **Issues identified** - Чітко визначено, що потрібно виправити
4. ✅ **Code patches ready** - Є конкретні рекомендації з кодом
5. ✅ **Documentation created** - Всі findings задокументовані

---

## 🔍 Особливі запити

### Приділи увагу цим аспектам:

1. **Coordinate systems** - як саме рахуються координати (pixels? grid units?)
2. **Link vertices** - формат масиву `vertices` в links table
3. **Icon dimensions** - default розміри для кожного типу
4. **Branching logic** - як представляються YES/NO гілки
5. **Loop structures** - як парувати loopbegin/loopend
6. **Silhouettes** - якщо згадуються sub-diagrams
7. **Color schemes** - чи є стандартні кольори для типів
8. **Auto-layout** - алгоритми розміщення

### Формат коду

- SQL schemas - чистий SQL DDL
- JSON schemas - валідний JSON
- TypeScript - якщо є type definitions
- Python patches - готові до copy-paste фрагменти

---

## 📝 Notes

- Якщо щось unclear в дослідженні - вкажи це явно
- Якщо дані суперечливі - надай обидва варіанти
- Якщо щось не знайдено - не вигадуй, напиши "Not found in research"
- Пріоритет - точність над повнотою

---

**Готовий до аналізу!** Жду вмісту файлу `drndew.md`.

```

---

## 🎓 Як використовувати цей промпт

### Крок 1: Запустіть дослідження

```bash
cd /home/vokov/motia/tools/drakon/perplexity
export PERPLEXITY_API_KEY='your-key'
./run_perplexity_lab.sh research
```

### Крок 2: Збережіть результат

```bash
# Скопіюйте вміст результату
cat research_output/processed/DRAKON_RESEARCH_*.md > drndew.md

# Або якщо є кілька файлів
cat research_output/processed/*.md > drndew.md
```

### Крок 3: Відкрийте цей файл

```bash
# Відкрийте в редакторі
cat CLAUDE-IMPORT-PROMPT.md
```

### Крок 4: Запустіть Claude CLI

```bash
# Новий сеанс
claude chat

# Скопіюйте весь промпт з секції "🎯 Промпт для Claude CLI"
# Замініть [ВСТАВИТИ ВМІСТ drndew.md] на реальний вміст
# Paste та виконайте
```

### Крок 5: Збережіть результати

Claude створить файли в:
- `knowledge_base/` - structured knowledge
- `VALIDATION-REPORT.md` - звіт валідації
- `CODE-PATCHES.md` - code updates

---

## 📊 Очікувані результати

### Після виконання промпту ви отримаєте:

1. **Validated converters** - розумієте, що працює правильно
2. **Identified gaps** - що missing або incorrect
3. **Structured knowledge** - JSON files з усіма даними
4. **Ready-to-apply patches** - конкретний код для оновлень
5. **Test cases** - приклади для валідації

### Час виконання

- Якщо дослідження коротке (<5000 words): ~5-10 хвилин
- Якщо дослідження середнє (5000-15000 words): ~15-20 хвилин
- Якщо дослідження велике (>15000 words): ~30-40 хвилин

---

## 🚨 Troubleshooting

### "Too much content"

Якщо drndew.md дуже великий (>100KB):

1. Розділіть на частини:
   ```bash
   split -l 500 drndew.md drndew_part_
   ```

2. Запустіть промпт для кожної частини окремо

3. Або використайте summarized version:
   ```bash
   # Витягти тільки ключові секції
   grep -A 50 "File Format" drndew.md > drndew_schemas.md
   grep -A 50 "Icon Types" drndew.md >> drndew_schemas.md
   ```

### "Research incomplete"

Якщо Perplexity не знайшов якусь критичну інформацію:

1. Уточніть промпт у `perplexity_prompt.txt`
2. Запустіть повторно
3. Або запитайте Claude шукати в офіційних репозиторіях

---

## 📚 References

**Project files:**
- `README.md` - Module documentation
- `DRAKON-MODULE-SUMMARY.md` - Implementation summary
- `INTEGRATION-GUIDE.md` - Integration walkthrough
- `converter/drakon_to_drn.py` - Current SQLite exporter
- `converter/drakon_to_json.py` - Current JSON exporter

**Official DRAKON:**
- [DRAKON Editor](https://github.com/stepan-mitkin/drakon_editor)
- [DrakonWidget](https://github.com/stepan-mitkin/drakonwidget)
- [DrakonHub](https://drakonhub.com)

---

**Created:** 2025-10-10 | **Version:** 1.0 | **Status:** Ready to use
