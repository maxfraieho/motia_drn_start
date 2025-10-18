# 🤖 Claude Prompt for DRAKON Editor Development

## 🎯 Мета
Claude використовується як технічний асистент для **розробки, налагодження та розширення функціональності редактора DRAKON**, який базується на проєкті [stepan-mitkin/drakonwidget](https://github.com/stepan-mitkin/drakonwidget).

## 🧭 Основне Правило Роботи

### ⚠️ КРИТИЧНО ВАЖЛИВО

**Перш ніж пропонувати БУДЬ-ЯКІ зміни або новий функціонал — ОБОВ'ЯЗКОВО:**

#### 1️⃣ Дослідити DrakonWidget API (в такому порядку)

**Крок A: Локальний drakonwidget.js**
```bash
# Пошук методу в локальному файлі
grep -n "function.*methodName" /home/vokov/motia-drn/tools/drakon-viewer/public/js/drakonwidget.js

# Перегляд імплементації
# Read file at found line number ±100 lines
```

**Крок B: Офіційний репозиторій**
```
1. WebFetch: https://github.com/stepan-mitkin/drakonwidget
   - Знайти структуру проєкту

2. WebFetch: https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/master/js/main.js
   - Переглянути як використовується API в демо

3. WebFetch: https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/master/libs/drakonwidget.js
   - Вивчити імплементацію методу
```

**Крок C: Live Demo**
```
WebFetch: https://stepan-mitkin.github.io/drakonwidget/
- Проаналізувати як працює фіча в оригіналі
- Зрозуміти user workflow
```

**Крок D: Наша реалізація**
```
Read: public/js/app.js
Read: public/js/state-manager.js
- Зрозуміти як інтегровано в наш проект
```

#### 2️⃣ Тільки ПІСЛЯ цього пропонуй рішення

Рішення має:
- ✅ **Використовувати існуючі DrakonWidget API методи** (не реімплементувати!)
- ✅ **Адаптувати офіційні паттерни** з main.js
- ✅ **Інтегруватися з існуючим workflow** (state manager, editSender)
- ✅ **Не ламати структуру** drakonWidget або його внутрішні механізми
- ❌ **НЕ винаходити з нуля** те що вже є в DrakonWidget

---

## ⚙️ Контекст Проєкту

**Проєкт:** `/home/vokov/motia-drn/tools/drakon-viewer`
**Поточна версія:** v3.2 (Insertion Sockets via DrakonWidget API)
**Live:** https://dangerboys.exodus.pp.ua/
**Git:** https://github.com/maxfraieho/motia_drn_start

**Основні файли:**
- `public/js/drakonwidget.js` (35k рядків) — ядро візуалізації та API від stepan-mitkin
- `public/js/app.js` (1200+ рядків) — логіка інтерфейсу, контролер
- `public/js/state-manager.js` — централізоване управління станом (undo/redo)
- `public/index.html` — UI структура (sidebar, canvas, properties panel)
- `public/css/style.css` — адаптивні стилі (dark theme)

**Документація:**
- `README.md` — основна документація, changelog
- `PHASE2-EDITOR.md` — план розвитку editor core
- `PHASE3-STORAGE.md` — localStorage integration
- `PROPERTIES-PANEL.md` — properties panel специфікація
- `IMPROVEMENTS.md` — mobile & UX покращення
- `Claude.md` (цей файл) — методологія роботи для Claude

---

## 💬 Робочий Контекст для Нових Сесій

**Prompt:**

> Ти — технічний асистент для розробки редактора DRAKON.
> Перед кожною зміною спочатку:
> 1. Переглянь API `drakonWidget` і код поточної реалізації.
> 2. Проаналізуй як подібна функція вже реалізована.
> 3. Лише після цього запропонуй спосіб інтеграції нового функціоналу.
>
> Твоя мета — **адаптувати, не ламати** існуючий код.
> Пропонуючи зміни, завжди вказуй:
> - де саме в коді їх реалізувати (файл + функція);
> - як це узгоджується з архітектурою;
> - чи потребує оновлення UI або state manager.
>
> Після кожного успішного оновлення додавай короткий changelog у форматі:
> ```
> ✅ {Назва фічі або виправлення}
> - {Що зроблено, які функції змінено}
> - {Тестування або приклад використання}
> ```
>
> Додатково:
> - Використовуй існуючі події (`stateChange`, `modeChange`, `selectionChange`).
> - При потребі створення нових API — інтегруй через `drakonWidget` (а не напряму в DOM).
> - Код має бути зрозумілий, з коментарями і у стилі проєкту.

---

## 📚 Додаткові Ресурси

**Тестові промпти:**
- `/home/vokov/motia-drn/promt/browser-testing-prompt.md` - тестування через Commet браузер
- `/home/vokov/motia-drn/promt/bugfix-summary-v3.1.md` - історія виправлень
- `/home/vokov/motia-drn/promt/node-insertion-analysis-prompt.md` - аналіз insertion механізму

**Deployment:**
```bash
# Автоматичний деплой
/home/vokov/motia-drn/tools/drakon-viewer/deploy.sh "Commit message"

# Або manual
docker restart motia_drakon_viewer
```

**Live сайт:** https://dangerboys.exodus.pp.ua/

---

## 🎓 Кейс: Insertion Sockets (ПРАВИЛЬНИЙ ПРИКЛАД)

### ❌ Неправильний Підхід (Спроба 1-2)

```javascript
// Спроба реімплементувати самостійно
function calculateInsertionSockets() {
  const items = diagram.items;
  // Проблема: items НЕ мають координат x, y!
  // DrakonWidget розраховує їх після рендерингу
  for (const id in items) {
    const item = items[id];
    const x = item.x || 0;  // ❌ undefined!
    const y = item.y || 0;  // ❌ undefined!
  }
}
```

**Результат:** Діаграми ламаються, координати неправильні ❌

### ✅ Правильний Підхід (Спроба 3)

**Крок 1: Дослідження**
```bash
# Пошук в локальному файлі
grep -n "showInsertionSockets" public/js/drakonwidget.js
# Знайдено: line 4058

# Перегляд імплементації
Read: drakonwidget.js lines 4058-4113
```

**Крок 2: Аналіз офіційного main.js**
```javascript
// WebFetch: https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/master/js/main.js
function insertIcon(type) {
  drakon.showInsertionSockets(type);  // ✅ Вбудований API!
}
```

**Крок 3: Імплементація**
```javascript
// Використати вбудований метод замість реімплементації
function addNode(type) {
  drakonWidget.showInsertionSockets(type, null);
  // DrakonWidget САМ:
  // - знаходить edges з координатами (після рендерингу)
  // - створює sockets: x=(x1+x2)/2, y=(y1+y2)/2
  // - відображає на canvas
  // - обробляє кліки
}
```

**Крок 4: Адаптація editSender**
```javascript
// З офіційного main.js: підтримка changes array
pushEdit: function(edit) {
  if (edit.changes && Array.isArray(edit.changes)) {
    for (const change of edit.changes) {
      switch (change.op) {
        case 'insert':  // ✅ Додано підтримку insert
          currentDiagram.items[change.id] = change.fields;
          break;
        // ...
      }
    }
  }
}
```

**Результат:** Працює ідеально! ✅
- Insertion sockets з'являються на правильних координатах
- Кліки обробляються DrakonWidget
- Діаграми не ламаються
- Код простіший (10 рядків замість 200)

### 📖 Висновок з Кейсу

**Правило:** Якщо щось здається складним - скоріш за все воно **вже реалізоване в DrakonWidget**.

**Алгоритм:**
1. grep → знайти метод
2. WebFetch → подивитись як використовується
3. Read → вивчити імплементацію
4. Адаптувати (не переписувати!)

---

## 📖 Quick Reference

### DrakonWidget Core API

**Основні методи (які маєш використовувати):**

```javascript
// Рендеринг
drakonWidget.render(width, height, config)
drakonWidget.redraw()
drakonWidget.setDiagram(name, diagram, editSender)

// Insertion sockets
drakonWidget.showInsertionSockets(type, imageData)  // ✅ Використовувати!
drakonWidget.showPasteSockets(type)

// Інші корисні
drakonWidget.getImageData()
drakonWidget.undo()
drakonWidget.redo()
```

**Пошук методів:**
```bash
# Шукати конкретний метод
grep -n "function.*showInsertionSockets" /home/vokov/motia-drn/tools/drakon-viewer/public/js/drakonwidget.js

# Шукати всі публічні методи widget
grep -n "self\..*= function" /home/vokov/motia-drn/tools/drakon-viewer/public/js/drakonwidget.js | tail -100
```

### State Manager API

```javascript
// Діаграма
stateManager.loadDiagram(diagram)
stateManager.getDiagram()
stateManager.getDiagramCopy()
stateManager.updateDiagram(diagram, skipHistory)

// Items (вузли)
stateManager.addItem(item)  // повертає новий ID
stateManager.updateItem(id, fields)
stateManager.deleteItem(id)

// Режими і стан
stateManager.isEditMode()
stateManager.setEditMode(bool)
stateManager.getSelectedItem()
stateManager.selectItem(id)

// Undo/Redo
stateManager.undo()
stateManager.redo()
stateManager.getHistoryInfo()
stateManager.hasUnsavedChanges()
stateManager.markAsSaved()

// Події
stateManager.on('stateChange', callback)
stateManager.on('modeChange', callback)
stateManager.on('selectionChange', callback)
stateManager.on('historyChange', callback)
```

### EditSender Pattern

```javascript
// Формат який очікує DrakonWidget
const editSender = {
  stop: function() {},
  pushEdit: function(edit) {
    // edit.changes = [{op: 'insert'|'update'|'delete', id, fields}]
    for (const change of edit.changes) {
      switch (change.op) {
        case 'insert':
          diagram.items[change.id] = change.fields;
          break;
        case 'update':
          Object.assign(diagram.items[change.id], change.fields);
          break;
        case 'delete':
          delete diagram.items[change.id];
          break;
      }
    }
  }
};
```

### Діаграма Structure

```javascript
{
  "name": "Diagram Name",
  "access": "read" | "write",
  "params": [],
  "items": {
    "1": {
      "id": "1",
      "type": "header" | "action" | "question" | "end" | ...,
      "content": "Text",
      "branchId": 1,
      "one": "2",    // ID наступного вузла вниз
      "two": "3"     // ID наступного вузла вправо (для question/branch)
    }
  }
}
```

**ВАЖЛИВО:** Items НЕ мають `x, y` координат! DrakonWidget розраховує їх при рендерингу в `visuals` структурі.

### Deployment

```bash
# Швидкий деплой (рекомендовано)
cd /home/vokov/motia-drn/tools/drakon-viewer
./deploy.sh "Your commit message"

# Manual
git add .
git commit -m "message"
git push origin main
docker restart motia_drakon_viewer
```

### Testing

```bash
# Local
cd /home/vokov/motia-drn/tools/drakon-viewer/public
python3 -m http.server 8080

# Production
https://dangerboys.exodus.pp.ua/
# Ctrl+Shift+R - hard reload
```

---

## 🧩 Приклад Сесії