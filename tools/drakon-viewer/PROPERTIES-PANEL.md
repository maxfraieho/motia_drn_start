# Properties Panel - Повнофункціональний Редактор DRAKON

## Огляд

Створено повнофункціональну правову бокову панель з інструментами для роботи з діаграмами.

## ✅ Реалізовані Компоненти

### 1. **Палітра Іконок** (Icon Palette)

**Розташування:** Верхня секція Properties Panel

**Іконки:**
- **▭** Action - Дія/операція
- **◇** Question - Питання/умова
- **⑂** Branch - Розгалуження
- **⥁** Loop Begin - Початок циклу
- **⥀** Loop End - Кінець циклу
- **●** End - Кінець

**Функціональність:**
- **Клік** на іконку → додає вузол до діаграми
- **Draggable** (готово для drag & drop)
- Hover ефекти та анімації
- Адаптивна сітка (2 колонки на desktop, 3 на mobile)

### 2. **Файлові Операції** (File Operations)

**Кнопки:**

| Кнопка | Функція | Скорочення |
|--------|---------|------------|
| 📄 Нова діаграма | Створити нову | Ctrl+N |
| 📂 Відкрити файл | Завантажити JSON | - |
| 💾 Зберегти | Зберегти як JSON | Ctrl+S |
| 📥 Експорт JSON | Експортувати JSON | - |
| 🖼️ Експорт PNG | (Майбутнє) | - |

**Функціональність:**

#### 📄 Нова діаграма
```javascript
// Створює базову структуру
{
  name: "User Input",
  items: {
    "1": { type: "action", content: "Початок", one: "2" },
    "2": { type: "end" }
  }
}
```
- Prompt для введення назви
- Автоматична базова структура (Start → End)
- Автоматичний edit mode

#### 📂 Відкрити файл
- Клік → file picker для `.json` файлів
- Автоматичний парсинг та валідація
- Завантаження в state manager
- Рендеринг діаграми

#### 💾 Зберегти / 📥 Експорт JSON
- Експорт поточної діаграми як JSON
- Автоматичне ім'я файлу: `{diagram.name}.json`
- Pretty-print з indent=2
- Browser download

### 3. **Властивості Вузла** (Node Properties)

**Показується:** Коли вузол виділено (клік на вузол)

**Поля:**
- **ID** - Унікальний ідентифікатор (readonly)
- **Тип** - Dropdown з типами вузлів
- **Контент** - Textarea для тексту
- **Branch ID** - Номер гілки (silhouette)

**Кнопки:**
- **Застосувати** - Зберегти зміни
- **Видалити** - Видалити вузол

**Функціональність:**
```javascript
// Auto-sync з selected item
stateManager.on('selectionChange', updatePropertiesPanel)

// Apply changes
stateManager.updateItem(id, {
  type: propType.value,
  content: propContent.value,
  branchId: parseInt(propBranch.value)
})
```

### 4. **Інформація про Діаграму** (Diagram Info)

**Відображає:**
- **Діаграма:** Назва поточної діаграми
- **Вузлів:** Кількість вузлів
- **Режим:** Перегляд / Редагування

**Auto-update:** При будь-яких змінах через state manager events

### 5. **Toggle Кнопка**

**Функція:** Згортання/розгортання панелі

**Розташування:** В заголовку панелі (◀)

**Поведінка:**
- Desktop: Slide out вправо
- Mobile: Bottom drawer

## 🎯 Як Використовувати

### Створення Нової Діаграми

**Метод 1: З панелі**
```
1. Клік "📄 Нова діаграма"
2. Введіть назву → "User Login"
3. Панель палітри тепер активна
4. Клік на іконки для додавання вузлів
```

**Метод 2: З toolbar**
```
1. Ctrl+N або кнопка "📄 Нова"
2. Введіть назву
3. Використовуйте toolbar кнопки або панель
```

### Додавання Вузлів

**З палітри іконок:**
```
1. Клік ▭ → Додає Action
2. Клік ◇ → Додає Question
3. Клік ⑂ → Додає Branch
... і т.д.
```

**Результат:**
- Автоматичне позиціонування
- Автоматичне з'єднання з попереднім вузлом
- Placeholder text
- Оновлення діаграми

### Редагування Вузла

**Метод 1: Properties Panel**
```
1. Клік на вузол → виділення
2. Properties Panel показує форму
3. Редагуйте поля
4. "Застосувати" → зберегти
```

**Метод 2: Modal (подвійний клік)**
```
1. Подвійний клік на вузол
2. Modal вікно
3. Редагуйте
4. "Зберегти"
```

### Відкриття Існуючої Діаграми

**З панелі:**
```
1. Клік "📂 Відкрити файл"
2. Виберіть .json файл
3. Діаграма завантажена
```

**З лівого sidebar:**
```
1. Клік на діаграму зі списку
2. Автоматичне завантаження
```

### Експорт/Збереження

**Експорт JSON:**
```
1. Клік "📥 Експорт JSON"
2. Файл завантажується: "diagram-name.json"
```

**Зберегти (з toolbar):**
```
1. Ctrl+S або "💾 Зберегти"
2. Експорт як JSON
```

## 🏗️ Архітектура

### Event Flow

```
User Action (Panel)
    ↓
Event Handler
    ↓
State Manager
    ↓
State Change Event
    ↓
Update UI (Info, Properties)
    ↓
Reload Diagram
```

### State Manager Integration

```javascript
// Listen to changes
stateManager.on('stateChange', updateDiagramInfo)
stateManager.on('selectionChange', updatePropertiesPanel)
stateManager.on('modeChange', updateDiagramInfo)

// Update on any change
function updateDiagramInfo() {
  infoName.textContent = diagram.name
  infoNodes.textContent = itemCount
  infoMode.textContent = editMode ? 'Редагування' : 'Перегляд'
}
```

## 📱 Responsive Design

### Desktop (≥ 768px)
```
┌─────────┬──────────────┬────────────┐
│ Sidebar │   Canvas     │ Properties │
│ (Left)  │   (Center)   │   Panel    │
│         │              │  (Right)   │
│ 300px   │   Flexible   │   320px    │
└─────────┴──────────────┴────────────┘
```

### Mobile (< 768px)
```
┌──────────────────────┐
│      Toolbar         │
├──────────────────────┤
│                      │
│      Canvas          │
│                      │
├──────────────────────┤
│  Properties Panel    │
│  (Bottom Drawer)     │
└──────────────────────┘
```

**Mobile поведінка:**
- Properties Panel як bottom drawer
- Swipe up/down для розгортання/згортання
- Toggle button завжди видимий
- Icon palette: 3 колонки замість 2

## 🎨 UI/UX Features

### Hover Effects
- Icon items: `translateY(-2px)` + border highlight
- Buttons: Background change + border accent
- Smooth transitions: `0.2s`

### Animations
- Panel slide: `transform` transition
- Toggle rotation: `rotate(180deg)`
- Button scale on click: `scale(0.95)`

### Color Scheme
```css
--bg-color: #1a1b26      /* Dark background */
--sidebar-bg: #24283b    /* Panel background */
--text-color: #c0caf5    /* Main text */
--header-color: #a9b1d6  /* Headers */
--accent-color: #7aa2f7  /* Accent/active */
--hover-bg: #414868      /* Hover state */
--border-color: #414868  /* Borders */
```

## 📊 Діаграма Компонентів

```
Properties Panel
├── Panel Header
│   ├── Title: "Інструменти"
│   └── Toggle Button ◀
│
├── Icon Palette Section
│   └── Grid (2x3 icons)
│       ├── Action ▭
│       ├── Question ◇
│       ├── Branch ⑂
│       ├── Loop Begin ⥁
│       ├── Loop End ⥀
│       └── End ●
│
├── File Operations Section
│   ├── 📄 Нова діаграма
│   ├── 📂 Відкрити файл
│   ├── 💾 Зберегти
│   ├── 📥 Експорт JSON
│   └── 🖼️ Експорт PNG (disabled)
│
├── Node Properties Section (conditional)
│   ├── ID (readonly)
│   ├── Type (select)
│   ├── Content (textarea)
│   ├── Branch ID (number)
│   └── Actions
│       ├── Застосувати
│       └── Видалити
│
└── Diagram Info Section
    ├── Діаграма: {name}
    ├── Вузлів: {count}
    └── Режим: {mode}
```

## 🔧 API Reference

### Panel Functions

```javascript
// Toggle panel
togglePropertiesPanel()

// Update info display
updateDiagramInfo()

// Update properties form
updatePropertiesPanel()

// Apply properties changes
applyPropertiesChanges()

// File operations
openFile()
handleFileOpen(event)
exportDiagramAsJson()
```

### Event Handlers

```javascript
// Icon palette
document.querySelectorAll('.icon-item').forEach(item => {
  item.addEventListener('click', () => addNode(type))
})

// Properties panel
panelToggle.addEventListener('click', togglePropertiesPanel)
panelNewBtn.addEventListener('click', createNewDiagram)
panelOpenBtn.addEventListener('click', openFile)
panelSaveBtn.addEventListener('click', saveDiagram)
panelExportJsonBtn.addEventListener('click', exportDiagramAsJson)
fileInput.addEventListener('change', handleFileOpen)
propApply.addEventListener('click', applyPropertiesChanges)
propDelete.addEventListener('click', deleteSelectedNode)
```

## 🚀 Workflow Examples

### Приклад 1: Створення Діаграми з Нуля

```
1. Клік "📄 Нова діаграма" → "Order Processing"
2. Клік ▭ → "Receive order"
3. Клік ◇ → "Is valid?"
4. Клік на "Is valid?" → Properties Panel
5. Редагувати content: "Check inventory"
6. "Застосувати"
7. Клік ▭ → "Process payment"
8. Клік ● → "End"
9. Ctrl+S → Зберегти
```

### Приклад 2: Відкриття та Редагування

```
1. Клік "📂 Відкрити файл"
2. Вибрати "my-flow.json"
3. Діаграма завантажена
4. Клік "✏️ Редагувати"
5. Клік на вузол → Properties Panel
6. Змінити тип: Action → Question
7. "Застосувати"
8. Клік "📥 Експорт JSON"
```

### Приклад 3: Швидке Створення

```
Keyboard-driven workflow:
1. Ctrl+N → Name → Enter
2. Клік ▭ (Action)
3. Подвійний клік → Edit content
4. Клік ◇ (Question)
5. Клік ● (End)
6. Ctrl+S → Save
```

## 💡 Tips & Tricks

### Швидке редагування
- Клік на вузол → Properties Panel (швидко)
- Подвійний клік → Modal (детально)

### Навігація
- `◀` кнопка для більше простору
- Mobile: Swipe для panel

### Workflow
1. Створити базу (Start → End)
2. Додавати вузли між ними
3. Редагувати properties
4. Зберігати часто (Ctrl+S)

## 🐛 Відомі Обмеження

1. **PNG Export** - Поки не реалізовано (requires canvas export)
2. **Drag & Drop** - Іконки draggable, але drop zone не реалізовано
3. **Позиціювання** - Автоматичне, контролюється drakonwidget
4. **Backend** - Тільки local file operations, немає server sync

## 🔜 Майбутні Покращення

1. **LocalStorage** - Auto-save в browser
2. **Recent Files** - Список останніх діаграм
3. **Templates** - Готові шаблони діаграм
4. **PNG Export** - Canvas to image
5. **Drag & Drop** - З палітри на canvas
6. **Context Menu** - Right-click на вузлі
7. **Shortcuts Panel** - Список всіх скорочень

---

**Статус:** Properties Panel завершено ✅
**Файли:**
- `/home/vokov/motia-drn/tools/drakon-viewer/public/index.html`
- `/home/vokov/motia-drn/tools/drakon-viewer/public/css/style.css`
- `/home/vokov/motia-drn/tools/drakon-viewer/public/js/app.js`

**Дата:** 2025-10-17
**Версія:** 2.5 (Properties Panel Edition)
