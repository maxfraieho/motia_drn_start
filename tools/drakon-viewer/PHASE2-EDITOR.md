# Фаза 2: DRAKON Editor - Повнофункціональний Редактор

## Огляд

**Фаза 2** успішно завершена! DRAKON Viewer тепер є повнофункціональним редактором з можливістю створення, редагування та збереження діаграм.

## ✅ Реалізовані Можливості

### 1. State Management System
**Файл:** `/home/vokov/motia-drn/tools/drakon-viewer/public/js/state-manager.js`

Повнофункціональний модуль управління станом діаграм:
- **Історія змін**: До 50 станів для undo/redo
- **Event-driven архітектура**: Listeners для stateChange, modeChange, selectionChange, historyChange
- **CRUD операції**: Створення, читання, оновлення, видалення вузлів
- **Іммутабельність**: Deep cloning для безпечних операцій
- **Tracking змін**: isDirty flag для незбережених змін

**API:**
```javascript
// Load diagram
stateManager.loadDiagram(diagramData)

// Update item
stateManager.updateItem(itemId, { content: 'New text', type: 'action' })

// Add item
const newId = stateManager.addItem({ type: 'action', content: 'New node' })

// Delete item
stateManager.deleteItem(itemId)

// Undo/Redo
stateManager.undo()
stateManager.redo()

// Listen to changes
stateManager.on('stateChange', (manager) => { /* handle change */ })
```

### 2. Режим Редагування

**Toggle кнопка:**
- **✏️ Редагувати** → увімкнути edit mode
- **👁️ Перегляд** → вимкнути edit mode

**Індикатори:**
- 📝 Режим редагування (в toolbar)
- ● Незбережені зміни (червоний індикатор)

**Поведінка:**
- В read-only mode: тільки перегляд та zoom/pan
- В edit mode: можливість редагувати, додавати, видаляти вузли

### 3. Undo/Redo

**Кнопки в Toolbar:**
- ↶ Скасувати (undo)
- ↷ Повторити (redo)

**Клавіатурні скорочення:**
- `Ctrl+Z` / `Cmd+Z` - Undo
- `Ctrl+Shift+Z` / `Ctrl+Y` / `Cmd+Shift+Z` - Redo

**Функціональність:**
- Автоматичне збереження кожної зміни в історію
- Динамічне оновлення стану кнопок (enabled/disabled)
- Максимум 50 станів в історії

### 4. Створення Нової Діаграми

**Кнопка:** 📄 Нова

**Клавіатурне скорочення:** `Ctrl+N` / `Cmd+N`

**Функціональність:**
- Prompt для введення назви діаграми
- Автоматичне створення базової структури:
  - Початковий вузол (Action: "Початок")
  - Кінцевий вузол (End)
  - З'єднання між ними
- Автоматичне увімкнення edit mode
- Готовність до додавання нових вузлів

### 5. Додавання Вузлів (Іконок)

**Панель кнопок в Toolbar** (показується тільки в edit mode):

| Іконка | Тип | Опис |
|--------|-----|------|
| ▭ | Action | Дія/операція |
| ◇ | Question | Питання/умова |
| ⑂ | Branch | Розгалуження |
| ● | End | Кінець |

**Функціональність:**
- Клік на іконку → додає новий вузол
- Автоматичне позиціонування (нижче існуючих вузлів)
- Автоматичне з'єднання з останнім вузлом (якщо можливо)
- Placeholder text: "New {type}"
- Автоматичне оновлення діаграми

### 6. Редагування Вузлів

**Модальне вікно:**
- Подвійний клік на вузол → відкриває modal
- Редагування контенту (textarea)
- Вибір типу вузла (dropdown)
- Кнопки: Зберегти / Скасувати

**Закриття modal:**
- Кнопка × (закрити)
- Кнопка "Скасувати"
- Клік на backdrop
- Клавіша `ESC`

**Типи вузлів:**
- Action (Дія)
- Question (Питання)
- Branch (Розгалуження)
- End (Кінець)
- Loop Begin (Початок циклу)
- Loop End (Кінець циклу)

### 7. Видалення Вузлів

**Кнопка:** 🗑️ (в панелі додавання вузлів)

**Клавіатурне скорочення:** `Delete`

**Функціональність:**
- Спочатку виберіть вузол (клік)
- Натисніть Delete або кнопку 🗑️
- Підтвердження через confirm dialog
- Автоматичне видалення всіх посилань на вузол
- Оновлення діаграми

### 8. Збереження Змін

**Кнопка:** 💾 Зберегти (показується тільки в edit mode)

**Клавіатурне скорочення:** `Ctrl+S` / `Cmd+S`

**Функціональність:**
- Експорт діаграми як JSON файл
- Завантаження через браузер
- Автоматичне ім'я файлу з path діаграми
- Скидання isDirty flag після збереження

**Майбутнє покращення:** Backend API для збереження на сервері

### 9. Selection Management

**Вибір вузлів:**
- Клік на вузол → виділяє його
- stateManager.selectItem(itemId) → зберігає виділення
- Використовується для операцій (видалення, редагування)

## 📋 Повний Список Клавіатурних Скорочень

### Загальні
- `Ctrl+N` / `Cmd+N` - Нова діаграма
- `Ctrl+0` / `Cmd+0` - Скинути zoom

### Zoom
- `Ctrl++` / `Cmd++` - Збільшити
- `Ctrl+-` / `Cmd+-` - Зменшити
- `Ctrl+Wheel` / `Cmd+Wheel` - Zoom

### Edit Mode
- `Ctrl+Z` / `Cmd+Z` - Undo
- `Ctrl+Shift+Z` / `Ctrl+Y` - Redo
- `Ctrl+S` / `Cmd+S` - Зберегти
- `Delete` - Видалити виділений вузол
- `ESC` - Закрити modal

## 🎯 Як Використовувати

### Створення Нової Діаграми

1. **Натисніть "📄 Нова"** або `Ctrl+N`
2. **Введіть назву** діаграми
3. **Додайте вузли** з панелі іконок:
   - ▭ Action
   - ◇ Question
   - ⑂ Branch
   - ● End
4. **Редагуйте вузли** подвійним кліком
5. **Збережіть** `Ctrl+S`

### Редагування Існуючої Діаграми

1. **Відкрийте діаграму** з бічного меню
2. **Увімкніть edit mode** - "✏️ Редагувати"
3. **Редагуйте:**
   - Подвійний клік → редагувати контент
   - Drag & drop → переміщення (підтримується drakonwidget)
   - Delete → видалити вузол
4. **Використовуйте Undo/Redo** за потреби
5. **Збережіть зміни** `Ctrl+S`

### Типовий Workflow

```
1. Ctrl+N → Нова діаграма "User Login Flow"
2. Клік ▭ → Додати Action "Check credentials"
3. Клік ◇ → Додати Question "Valid?"
4. Подвійний клік → Редагувати контент
5. Клік ● → Додати End
6. Ctrl+S → Зберегти
```

## 🏗️ Архітектура

### Компоненти

```
┌─────────────────────────────────────┐
│         DRAKON Editor               │
├─────────────────────────────────────┤
│                                     │
│  ┌────────────────────────────┐    │
│  │   DiagramStateManager       │    │
│  │   - loadDiagram()           │    │
│  │   - updateItem()            │    │
│  │   - addItem()               │    │
│  │   - deleteItem()            │    │
│  │   - undo() / redo()         │    │
│  └────────────────────────────┘    │
│            ▲                        │
│            │                        │
│  ┌─────────┴──────────────────┐    │
│  │      App.js (Controller)    │    │
│  │   - Event handlers          │    │
│  │   - UI updates              │    │
│  │   - Keyboard shortcuts      │    │
│  └─────────┬──────────────────┘    │
│            │                        │
│            ▼                        │
│  ┌────────────────────────────┐    │
│  │    DrakonWidget.js          │    │
│  │   - render()                │    │
│  │   - setDiagram()            │    │
│  │   - callbacks               │    │
│  └────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### Data Flow

```
User Action → Event Handler → State Manager → Update Diagram → Reload Widget → Render
              ↓
         History Save
              ↓
        Enable Undo/Redo
```

## 📊 Структура Даних Діаграми

```json
{
  "name": "Example Flow",
  "access": "write",
  "params": [],
  "items": {
    "1": {
      "id": "1",
      "type": "action",
      "content": "Start process",
      "branchId": 1,
      "one": "2"
    },
    "2": {
      "id": "2",
      "type": "question",
      "content": "Is valid?",
      "branchId": 1,
      "yes": "3",
      "no": "4"
    },
    "3": {
      "id": "3",
      "type": "action",
      "content": "Process data",
      "branchId": 1,
      "one": "5"
    },
    "4": {
      "id": "4",
      "type": "action",
      "content": "Handle error",
      "branchId": 2,
      "one": "5"
    },
    "5": {
      "id": "5",
      "type": "end",
      "content": "",
      "branchId": 1
    }
  }
}
```

## 🚀 Що Далі (Фаза 3-5)

### Фаза 3: Mobile Optimization (вже завершена)
- ✅ Touch gestures
- ✅ Responsive design
- ✅ Pan/zoom

### Фаза 4: Розширені Функції
- [ ] Properties Panel (боковий)
- [ ] Шаблони діаграм
- [ ] Експорт у PNG/SVG
- [ ] **Code-to-Diagram генератор** (AST parser)

### Фаза 5: Інтеграція
- [ ] Backend API для збереження
- [ ] Інтеграція з unified-motia-workflow.sh
- [ ] Docker production build
- [ ] CI/CD

## 📝 Примітки

### Обмеження drakonwidget.js
- Автоматичне компонування вузлів контролюється бібліотекою
- Позиції x, y можуть ігноруватися (залежить від drakonwidget)
- branchId визначає вертикальну лінію ("силует")

### Майбутні Покращення
1. **Context Menu:** Правий клік на вузлі → меню (Edit, Delete, Duplicate)
2. **Copy/Paste:** Копіювання вузлів
3. **Multi-select:** Виділення кількох вузлів
4. **Properties Panel:** Детальне редагування всіх властивостей
5. **Templates:** Готові шаблони діаграм
6. **Backend Integration:** Збереження на сервері, колаборація

---

**Статус:** Фаза 2 завершена ✅
**Дата:** 2025-10-17
**Наступна фаза:** Properties Panel + Code-to-Diagram
**Базис:** /home/vokov/motia-drn/promt/plan.md
