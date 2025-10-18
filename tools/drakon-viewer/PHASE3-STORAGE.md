# Phase 3: LocalStorage & Export Features

**Дата:** 2025-10-17
**Версія:** 3.0
**Статус:** ✅ Completed

---

## Огляд

Фаза 3 додала критичні функції управління діаграмами:
- LocalStorage для збереження діаграм у браузері
- Інтерактивний Sidebar з управлінням діаграмами
- PNG Export функціональність
- Auto-save при змінах

---

## ✨ Реалізовані Функції

### 1. LocalStorage Management

**Ключові компоненти:**

```javascript
// Storage keys
const STORAGE_KEY = 'drakon_diagrams';
const STORAGE_META_KEY = 'drakon_diagrams_meta';

// Core functions
function saveDiagramToStorage(diagram)
function loadDiagramsFromStorage()
function getDiagramFromStorage(id)
function deleteDiagramFromStorage(id)
function generateDiagramId(name)
```

**Особливості:**

#### Auto-Save
- Автоматичне збереження при кожній зміні діаграми
- Інтеграція з State Manager через events
- Timestamp для відстеження останньої зміни

```javascript
stateManager.on('stateChange', () => {
    updateHistoryButtons();
    updateDiagramInfo();

    // Auto-save to localStorage
    const diagram = stateManager.getDiagram();
    if (diagram && diagram.id) {
        saveDiagramToStorage(diagram);
    }
});
```

#### Diagram ID Generation
- Унікальний ID для кожної діаграми
- Формат: `{safeName}_{timestamp}_{random}`
- Приклад: `My_Flow_1729184520123_a7f3k2m`

#### Data Structure
```json
{
  "My_Flow_1729184520123_a7f3k2m": {
    "id": "My_Flow_1729184520123_a7f3k2m",
    "name": "My Flow",
    "lastModified": "2025-10-17T10:30:00.000Z",
    "items": { ... },
    "access": "write",
    "params": []
  },
  "Another_Diagram_1729184530456_b8g4l3n": { ... }
}
```

---

### 2. Interactive Sidebar

**Функції:**

#### Dynamic Diagram List
- Автоматичне популювання з localStorage
- Сортування за датою останньої зміни (newest first)
- Empty state коли немає діаграм

```javascript
function populateDiagramsList() {
    const diagrams = loadDiagramsFromStorage();
    const diagramIds = Object.keys(diagrams);

    if (diagramIds.length === 0) {
        diagramNav.innerHTML = '<p>Немає збережених діаграм...</p>';
        return;
    }

    // Sort by lastModified
    diagramIds.sort((a, b) => {
        const dateA = new Date(diagrams[a].lastModified || 0);
        const dateB = new Date(diagrams[b].lastModified || 0);
        return dateB - dateA;
    });

    // Render list...
}
```

#### Click to Load
- Клік на діаграму → завантаження
- Highlight активної діаграми (`.active` class)
- Auto-close sidebar на mobile після вибору

#### Delete Functionality
- Кнопка 🗑️ для кожної діаграми
- Показується при hover
- Confirmation dialog перед видаленням
- Автоматичне оновлення списку після видалення

```javascript
deleteBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    e.preventDefault();
    if (confirm(`Видалити діаграму "${diagram.name}"?`)) {
        deleteDiagramFromStorage(id);
        populateDiagramsList();

        // Clear canvas if active
        const currentDiagram = stateManager.getDiagram();
        if (currentDiagram && currentDiagram.id === id) {
            drakonContainer.innerHTML = '<p>Оберіть діаграму...</p>';
            stateManager.loadDiagram(null);
        }
    }
});
```

#### Hover Effects
- Delete button з'являється при hover
- Smooth opacity transition (0.2s)
- Visual feedback

---

### 3. PNG Export

**Реалізація:**

```javascript
function exportDiagramAsPng() {
    const diagram = stateManager.getDiagramCopy();
    if (!diagram) {
        alert('Немає діаграми для експорту');
        return;
    }

    if (!currentCanvas) {
        alert('Canvas не знайдено.');
        return;
    }

    try {
        // Convert canvas to PNG
        const dataURL = currentCanvas.toDataURL('image/png');

        // Download
        const a = document.createElement('a');
        a.href = dataURL;
        a.download = (diagram.name || 'diagram') + '.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        console.log('PNG exported successfully');
    } catch (error) {
        console.error('Error exporting PNG:', error);
        alert('Помилка експорту PNG: ' + error.message);
    }
}
```

**Особливості:**
- Експорт поточного canvas в PNG формат
- Назва файлу з назви діаграми
- Error handling для CORS/tainted canvas issues

**Активація кнопки:**
```javascript
if (panelExportPngBtn) {
    panelExportPngBtn.disabled = false;
    panelExportPngBtn.title = 'Експортувати діаграму як PNG зображення';
}
```

---

### 4. Enhanced File Operations

#### New Diagram
- Автоматичне збереження в localStorage
- Генерація унікального ID
- Оновлення sidebar списку

```javascript
function createNewDiagram() {
    const diagramName = prompt('Назва нової діаграми:', 'New Diagram');
    if (!diagramName) return;

    const newDiagram = { ... };

    // Save to storage
    const diagramId = saveDiagramToStorage(newDiagram);
    if (diagramId) {
        newDiagram.id = diagramId;
    }

    // Load and refresh
    stateManager.loadDiagram(newDiagram);
    populateDiagramsList();
    closeSidebarOnMobile();
}
```

#### Open File
- Імпорт JSON файлу
- Автоматичне збереження в localStorage
- Додавання до sidebar списку

```javascript
function handleFileOpen(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const diagramData = JSON.parse(e.target.result);

        // Save to localStorage
        const diagramId = saveDiagramToStorage(diagramData);
        if (diagramId) {
            diagramData.id = diagramId;
        }

        stateManager.loadDiagram(diagramData);
        populateDiagramsList();
    };
    reader.readAsText(file);
}
```

#### Save/Export
- JSON export (existing functionality)
- PNG export (new!)
- Зберігання назви діаграми для filename

---

### 5. Tooltips

**Додані tooltips для всіх кнопок:**

#### Toolbar
- ☰ "Відкрити меню"
- ✏️ "Увімкнути режим редагування"
- 📄 "Створити нову діаграму"
- ▭ ◇ ⑂ "Додати [тип] вузол"
- 🗑️ "Видалити виділений вузол (Delete)"
- ↶ "Скасувати (Ctrl+Z)"
- ↷ "Повторити (Ctrl+Y)"
- 🔍+ "Збільшити"
- 🔍− "Зменшити"
- ↺ "Скинути масштаб"
- 💾 "Зберегти зміни"
- ⛶ "Повноекранний режим"

#### Properties Panel
- 📄 "Створити нову діаграму (Ctrl+N)"
- 📂 "Відкрити діаграму з JSON файлу"
- 💾 "Зберегти діаграму як JSON (Ctrl+S)"
- 📥 "Експортувати діаграму в JSON формат"
- 🖼️ "Експортувати діаграму як PNG зображення"
- "Застосувати" → "Застосувати зміни до виділеного вузла"
- "Видалити" → "Видалити виділений вузол (Delete)"

#### Icon Palette
- ▭ "Action - Дія"
- ◇ "Question - Питання"
- ⑂ "Branch - Розгалуження"
- ⥁ "Loop Begin - Початок циклу"
- ⥀ "Loop End - Кінець циклу"
- ● "End - Кінець"

---

## 🎯 Workflow Examples

### Приклад 1: Створення та Автоматичне Збереження

```
1. Ctrl+N або клік "📄 Нова діаграма"
2. Введіть назву: "User Authentication Flow"
3. Діаграма автоматично зберігається в localStorage
4. З'являється в sidebar списку
5. Кожна зміна автоматично зберігається
6. Не потрібно вручну зберігати!
```

### Приклад 2: Робота з Множинними Діаграмами

```
1. Створити "Login Flow" → автоматично в sidebar
2. Створити "Registration Flow" → автоматично в sidebar
3. Створити "Password Reset Flow" → автоматично в sidebar
4. Sidebar показує всі 3 діаграми, sorted by lastModified
5. Клік на будь-яку → миттєве завантаження
6. Hover → кнопка 🗑️ для видалення
```

### Приклад 3: Експорт Діаграми

```
1. Відкрити діаграму зі sidebar
2. Експорт JSON: клік "📥 Експорт JSON" → завантажується файл
3. Експорт PNG: клік "🖼️ Експорт PNG" → завантажується зображення
4. Використати в документації, презентаціях, тощо
```

### Приклад 4: Імпорт та Збереження

```
1. Клік "📂 Відкрити файл"
2. Вибрати JSON файл з комп'ютера
3. Діаграма завантажується
4. Автоматично зберігається в localStorage
5. Додається до sidebar списку
6. Доступна для редагування
```

---

## 🏗️ Архітектура

### Data Flow

```
User Action (Create/Edit/Delete)
    ↓
Event Handler
    ↓
State Manager (updateDiagram)
    ↓
State Change Event
    ↓
Auto-save to LocalStorage
    ↓
Update Sidebar List
    ↓
UI Refresh
```

### Storage Integration

```
app.js
├── LocalStorage Functions
│   ├── saveDiagramToStorage()
│   ├── loadDiagramsFromStorage()
│   ├── getDiagramFromStorage()
│   ├── deleteDiagramFromStorage()
│   └── generateDiagramId()
│
├── Sidebar Management
│   ├── populateDiagramsList()
│   └── Diagram click handler
│
├── Export Functions
│   ├── exportDiagramAsJson()
│   └── exportDiagramAsPng()
│
└── State Manager Integration
    └── Auto-save on stateChange
```

---

## 📊 Покращення Порівняно з v2.5

| Функція | v2.5 | v3.0 |
|---------|------|------|
| Збереження діаграм | ❌ Тільки download JSON | ✅ Auto-save в localStorage |
| Управління діаграмами | ❌ Немає списку | ✅ Інтерактивний sidebar |
| Видалення діаграм | ❌ Вручну видаляти файли | ✅ Кнопка в UI |
| PNG Export | ❌ Disabled | ✅ Працює |
| Auto-save | ❌ Вручну Ctrl+S | ✅ Автоматично |
| Tooltips | 🟡 Частково | ✅ На всіх кнопках |
| Сортування діаграм | ❌ Немає | ✅ By lastModified |
| Empty state | ❌ Порожній список | ✅ Friendly message |

---

## 🔧 Технічні Деталі

### LocalStorage Limits
- Типовий ліміт: 5-10MB per domain
- Діаграми зберігаються як JSON strings
- Automatic cleanup не реалізовано (може бути в майбутньому)

### Browser Compatibility
- localStorage підтримується всіма сучасними браузерами
- Canvas.toDataURL() підтримується всіма сучасними браузерами
- CORS issues можливі при завантаженні зовнішніх resources

### Error Handling
- Try-catch блоки для localStorage operations
- User-friendly alert messages
- Console logging для debugging

---

## 🐛 Відомі Обмеження

1. **Storage Quota**
   - LocalStorage має ліміт розміру (~5MB)
   - Великі діаграми (1000+ вузлів) можуть досягти ліміту
   - Немає попередження про наближення до ліміту

2. **PNG Export Quality**
   - Залежить від resolution canvas
   - Може бути pixelated на великих діаграмах
   - Не підтримує векторний експорт (SVG)

3. **No Cloud Sync**
   - Діаграми зберігаються тільки локально
   - Не синхронізуються між пристроями
   - Clearing browser data видалить діаграми

4. **No Version Control**
   - Немає історії версій діаграм
   - Undo/Redo тільки в межах сесії
   - Неможливо відновити старі версії

---

## 🔜 Майбутні Покращення

### Short-term (Етап 4)
- [ ] Storage quota warning
- [ ] Export to SVG
- [ ] Duplicate diagram функція
- [ ] Rename diagram in sidebar
- [ ] Theme support (dark/light)

### Medium-term
- [ ] Diagram templates
- [ ] Import/Export всіх діаграм
- [ ] Search/Filter в sidebar
- [ ] Tags для діаграм
- [ ] Diagram preview thumbnails

### Long-term
- [ ] Cloud sync (backend)
- [ ] Collaboration features
- [ ] Version control
- [ ] Comments on nodes
- [ ] Diagram sharing (public links)

---

## 📖 API Reference

### Storage Functions

```javascript
/**
 * Save diagram to localStorage
 * @param {Object} diagram - Diagram data object
 * @returns {string|null} - Diagram ID or null on error
 */
function saveDiagramToStorage(diagram)

/**
 * Load all diagrams from localStorage
 * @returns {Object} - Object with diagram IDs as keys
 */
function loadDiagramsFromStorage()

/**
 * Get specific diagram from storage
 * @param {string} id - Diagram ID
 * @returns {Object|null} - Diagram object or null if not found
 */
function getDiagramFromStorage(id)

/**
 * Delete diagram from localStorage
 * @param {string} id - Diagram ID
 * @returns {boolean} - Success status
 */
function deleteDiagramFromStorage(id)

/**
 * Generate unique diagram ID
 * @param {string} name - Diagram name
 * @returns {string} - Unique ID
 */
function generateDiagramId(name)

/**
 * Populate sidebar with diagrams list
 */
function populateDiagramsList()

/**
 * Export current diagram as PNG
 */
function exportDiagramAsPng()
```

---

## 🎉 Висновок

**Фаза 3 успішно завершена!**

Додані критичні функції для production-ready редактора:
- ✅ LocalStorage з auto-save
- ✅ Інтерактивний sidebar
- ✅ PNG Export
- ✅ Tooltips на всіх кнопках

**Редактор тепер готовий до реального використання!**

Наступні кроки - Етап 4: UX/UI покращення та додаткові features з comparison analysis.

---

**Файли змінені:**
- `/home/vokov/motia-drn/tools/drakon-viewer/public/js/app.js` - +150 lines (storage, sidebar, PNG export)
- `/home/vokov/motia-drn/tools/drakon-viewer/public/index.html` - tooltips додані
- `/home/vokov/motia-drn/tools/drakon-viewer/README.md` - оновлено до v3.0

**Статус:** ✅ Production Ready
**Дата:** 2025-10-17
**Версія:** 3.0
