# Research Prompt Update - 2025-10-19

## ✅ Що додано до RESEARCH_PROMPT_GEMINI.md

### 🔥 Критичне доповнення: Питання 7

**Назва:** DrakonWidget API Integration for Native Diagram Generation

**Чому це найважливіше питання:**
Зараз система генерує JSON діаграм вручну, що призводить до:
- ❌ Ризику несумісності з офіційними редакторами
- ❌ Помилок валідації структури
- ❌ Втрати метаданих (позиції, з'єднання)
- ❌ Відсутності підтримки .drn формату (desktop editor)

**Пропозиція:**
Використовувати API самого drakonWidget для генерації діаграм програмно.

---

## 📊 Порівняння підходів

### Поточний підхід (Ручний JSON)
```python
# tools/drakon/converter/drakon_to_json.py
def generate_diagram_json(function_name, nodes):
    diagram = {
        "name": function_name,
        "access": "write",
        "items": {}
    }
    # Manually build items dict - risky!
    for node in nodes:
        diagram["items"][str(node_id)] = {
            "type": node.type,
            "content": node.content
        }
    return json.dumps(diagram)  # Hope it's valid!
```

**Проблеми:**
- Немає автоматичної валідації
- Можлива несумісність з офіційними інструментами
- Треба вручну підтримувати формат

### Запропонований підхід (DrakonWidget API)
```javascript
// Використання API drakonWidget
const drakonGenerator = require('./drakonwidget-headless');

function generateDiagramViaAPI(functionName, nodes) {
  const diagram = drakonGenerator.createDiagram(functionName);
  
  nodes.forEach((node, index) => {
    drakonGenerator.addNode(diagram, {
      type: node.type,
      content: node.content,
      connectTo: nodes[index + 1]?.id
    });
    // drakonWidget validates automatically!
  });
  
  return drakonGenerator.exportJSON(diagram);
  // Guaranteed compatible with Stepan Mitkin's editors!
}
```

**Переваги:**
- ✅ 100% сумісність з офіційними DRAKON редакторами
- ✅ Автоматична валідація структури
- ✅ Коректні метадані (позиції, розміри, з'єднання)
- ✅ Підтримка всіх типів вузлів
- ✅ Майбутні оновлення drakonWidget автоматично підтягуються

---

## 🔍 Ключові питання для Gemini AI

1. **Headless виконання:**
   - Чи можна запустити drakonWidget в Node.js без DOM?
   - Які залежності треба замокати?
   - Як створити headless wrapper?

2. **API Discovery:**
   - Які функції drakonWidget доступні для програмного використання?
   - Як документувати API (reverse-engineering)?
   - Формат параметрів для `createNode()`, `buildDiagramModel()`?

3. **Інтеграція з Python:**
   - PyExecJS для виклику drakonWidget з Python?
   - Або Node.js мікросервіс для генерації?
   - Який підхід ефективніший?

4. **Сумісність з офіційними редакторами:**
   - Desktop DRAKON Editor (.drn формат)
   - DrakonHub (online editor)
   - Як перевірити сумісність?

5. **Продуктивність:**
   - Швидкість: API vs ручний JSON?
   - Обмеження (пам'ять, concurrency)?
   - Можливість batch generation?

---

## 🎯 Очікувані результати від Gemini

### Якщо API integration можливо:
1. **Архітектура:**
   ```
   Python AST → Semantic Analysis → Node.js Service → DrakonWidget API → Valid JSON
   ```

2. **Proof-of-Concept:**
   ```javascript
   // Headless drakonWidget wrapper
   const { JSDOM } = require('jsdom');
   const drakonWidget = require('./drakonwidget');
   
   function createHeadlessDiagram(name) {
     const dom = new JSDOM();
     global.document = dom.window.document;
     // ... use drakonWidget API
   }
   ```

3. **Міграційний план:**
   - Фаза 1: Headless wrapper (2 тижні)
   - Фаза 2: Node.js microservice (1 тиждень)
   - Фаза 3: Інтеграція з code_to_drakon.py (1 тиждень)
   - Фаза 4: Тестування сумісності (1 тиждень)

### Якщо API integration неможливо:
- Детальний аналіз чому
- Альтернативні підходи
- Як покращити ручний JSON generation
- Як забезпечити валідацію без API

---

## 📈 Вплив на проект

**Пріоритет:** 🔥🔥🔥 КРИТИЧНИЙ (highest impact)

**ROI Analysis:**
- **Вклад роботи:** 4-6 тижнів розробки
- **Вигода:** Назавжди розв'язує проблеми сумісності
- **Ризик:** Середній (залежність від можливості headless запуску)

**Decision Tree:**
```
Can drakonWidget run headless?
  ├─ YES → Implement API integration (high value)
  └─ NO → Can we extract validation logic?
      ├─ YES → Use validation without full API
      └─ NO → Improve manual JSON + testing
```

---

## 📝 Оновлені файли

1. **RESEARCH_PROMPT_GEMINI.md** (~2227 слів)
   - Додано секцію "Question 7: DrakonWidget API Integration"
   - Додано приклади код порівняння (manual vs API)
   - Оновлено Success Criteria
   - Додано пріоритет для Question 7

2. **HOW_TO_USE_RESEARCH.md**
   - Додано секцію "🔥 НАЙВАЖЛИВІШЕ: DrakonWidget API"
   - Оновлено список з 6 до 7 питань
   - Додано очікувані результати для Question 7

3. **SUMMARY.md**
   - Оновлено секцію "AI Research Prompts"
   - Додано інформацію про Question 7
   - Оновлено timestamp

---

## 🚀 Наступні кроки

### Для користувача:
1. **Прочитати оновлений промпт:**
   ```bash
   cat /home/vokov/motia_drn_start/RESEARCH_PROMPT_GEMINI.md
   ```

2. **Запустити в Gemini AI Pro:**
   - Відкрити https://aistudio.google.com/
   - Вставити весь промпт
   - Отримати детальну відповідь

3. **Зосередитись на Question 7:**
   - Gemini має спочатку відповісти на питання про API
   - Це критичний path для архітектури

4. **Зберегти результати:**
   ```bash
   nano /home/vokov/motia_drn_start/GEMINI_RESEARCH_RESULTS.md
   # Вставити відповідь Gemini
   ```

5. **Обговорити імплементацію:**
   - Якщо API можливо → створити Node.js microservice
   - Якщо ні → покращити ручний підхід

---

## 📚 Додаткові ресурси

### Доступні API в drakonWidget.js:
```javascript
// Виявлені функції (reverse-engineering)
createNode(visuals, itemId, type, content, id)
createNewItem(model, type)
buildDiagramModel(widget, diagram)
addItemToModel(model, item)
createParamsNode(visuals, params)
```

### Testing API в app.js:
```javascript
window.DrakonTestAPI = {
  createDiagram: (name) => {...},
  addNode: (type) => {...},
  getDiagram: () => {...},
  saveDiagram: () => {...}
}
```

### Автор DRAKON:
**Stepan Mitkin** - creator of DRAKON visual programming language
- Desktop DRAKON Editor (C#/.NET)
- DrakonHub (online editor)
- drakonWidget.js (JavaScript rendering library)

---

**Створено:** 2025-10-19  
**Автор доповнення:** Користувач запросив додати тему про використання API drakonWidget  
**Статус:** ✅ Готово до запуску в Gemini AI  
**Пріоритет:** 🔥 КРИТИЧНИЙ - Question 7 визначає архітектуру всієї системи
