# DRAKON Editor - Повнофункціональний Редактор Діаграм

**Версія:** 3.1 (Bugfix Release)
**Статус:** Стабільна версія ✅
**Дата:** 2025-10-17

---

## 🚀 Швидкий Старт

### Запуск
```bash
cd /home/vokov/motia-drn/tools/drakon-viewer/public
python3 -m http.server 8080
```

Відкрийте: http://localhost:8080

### Перші Кроки

1. **Створити діаграму:** `Ctrl+N` → Введіть назву (автоматично зберігається в браузері)
2. **Додати вузли:** Клік на іконки в правій панелі (▭ ◇ ⑂ ●)
3. **Редагувати:** Подвійний клік на вузол або Properties Panel
4. **Зберегти:** Автоматично зберігається в localStorage при кожній зміні
5. **Експорт:** PNG або JSON через Properties Panel

---

## ✨ Основні Можливості

✅ **Повноцінне редагування діаграм**
✅ **Undo/Redo** (історія до 50 станів)
✅ **Properties Panel** з палітрою іконок
✅ **LocalStorage** - автоматичне збереження діаграм у браузері
✅ **Інтерактивний Sidebar** - управління множинними діаграмами
✅ **File Management** (Open/Save/Export JSON/PNG)
✅ **PNG Export** - експорт діаграм як зображень
✅ **Mobile-First** адаптивний дизайн
✅ **Touch gestures** (pinch-to-zoom, swipe)
✅ **Pan/Zoom** навігація
✅ **State Management** система
✅ **Tooltips** на всіх кнопках  

---

## 🎯 Інтерфейс

### Layout
```
┌─────────┬──────────────┬────────────┐
│ Sidebar │   Canvas     │ Properties │
│ (Left)  │   (Center)   │   Panel    │
│         │              │  (Right)   │
│ Діаграми│  DRAKON      │ • Іконки  │
│         │  Diagram     │ • Файли   │
│         │              │ • Форма   │
└─────────┴──────────────┴────────────┘
```

### Properties Panel (Права панель)

**Палітра іконок** (9 типів):
- ▭ Action - Дія
- ◇ Question - Питання
- ⑂ Branch - Розгалуження
- ⬡ Case - Вибір з варіантів
- ⬢ Address - Посилання на іншу діаграму
- ⬓ Header - Заголовок діаграми
- ⥁ Loop Begin - Початок циклу
- ⥀ Loop End - Кінець циклу
- ● End - Кінець

**Файлові операції:**
- 📄 Нова діаграма (`Ctrl+N`)
- 📂 Відкрити файл (JSON)
- 💾 Зберегти (`Ctrl+S`)
- 📥 Експорт JSON
- 🖼️ Експорт PNG

**Властивості вузла** (при виборі):
- ID, Type, Content, Branch ID
- Кнопки: Застосувати / Видалити

### Sidebar (Ліва панель)

**Мої діаграми:**
- Автоматичний список усіх збережених діаграм
- Сортування за датою останньої зміни
- Клік на діаграму для відкриття
- Кнопка 🗑️ для видалення (з'являється при hover)
- Збереження в localStorage браузера

---

## ⌨️ Клавіатурні Скорочення

### Загальні
- `Ctrl+N` - Нова діаграма
- `Ctrl+S` - Зберегти
- `Ctrl+0` - Reset zoom
- `ESC` - Закрити modal

### Редагування
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo  
- `Delete` - Видалити вузол

### Навігація
- `Ctrl++` / `Ctrl+-` - Zoom
- `Ctrl+Wheel` - Zoom (mouse)
- `Drag` - Pan

---

## 📱 Mobile Support

**Touch Gestures:**
- Pinch - Zoom
- 1 палець - Pan
- Swipe вправо - Відкрити sidebar
- 2 пальці - Pinch-to-zoom

**Адаптивний дизайн:**
- Mobile (< 768px): Overlay panels
- Desktop (≥ 768px): Static layout

---

## 📖 Документація

- [IMPROVEMENTS.md](./IMPROVEMENTS.md) - Фаза 1 (Mobile & UX)
- [PHASE2-EDITOR.md](./PHASE2-EDITOR.md) - Фаза 2 (Editor Core)
- [PROPERTIES-PANEL.md](./PROPERTIES-PANEL.md) - Properties Panel

---

## 🏗️ Архітектура

**Компоненти:**
- `state-manager.js` - Централізоване управління станом
- `drakonwidget.js` - DRAKON rendering engine
- `app.js` - UI controller
- `style.css` - Responsive styles

**Data Flow:**
```
User Action → Event Handler → State Manager → 
  → Update UI → Reload Diagram → Render
```

---

## 🛠️ Troubleshooting

**Діаграма не відображається?**
- Ctrl+0 для reset zoom
- F12 console для errors
- Перевірте JSON формат

**Не зберігаються зміни?**
- Увімкніть edit mode (✏️)
- Ctrl+S для збереження

**Mobile gestures не працюють?**
- 2 пальці для pinch
- Swipe з краю екрану

---

## 📊 Формат Діаграми

```json
{
  "name": "Diagram Name",
  "access": "read|write",
  "items": {
    "1": {
      "type": "action",
      "content": "Text",
      "branchId": 1,
      "one": "2"
    }
  }
}
```

**Типи вузлів:** action, question, branch, case, address, header, loopbegin, loopend, end (9 типів)

---

## 📝 Changelog

**v3.1** (2025-10-17) - Bugfix Release
- 🐛 **FIX:** Loader timeout (5 сек) + fallback error
- 🐛 **FIX:** Floating button для повернення Properties Panel
- 🐛 **FIX:** Empty state при старті
- ✨ Розширена палітра іконок (6 → 9 типів): +Case, +Address, +Header
- ✨ Grid палітри (2 → 3 колонки)
- 🔧 Покращена обробка помилок завантаження
- 🔧 UX покращення для зниклих панелей

**v3.0** (2025-10-17) - LocalStorage & PNG Export Edition
- ✨ LocalStorage - автоматичне збереження діаграм у браузері
- ✨ Інтерактивний Sidebar - управління множинними діаграмами
- ✨ PNG Export - експорт діаграм як зображень
- ✨ Auto-save - автоматичне збереження при кожній зміні
- ✨ Delete diagrams - видалення діаграм з sidebar
- ✨ Tooltips - підказки на всіх кнопках
- 🔧 Покращена інтеграція з localStorage
- 🔧 Оптимізація управління станом

**v2.5** (2025-10-17) - Properties Panel Edition
- Properties Panel з палітрою
- File Operations
- Node Properties Form

**v2.0** - Full Editor
- State Management
- Undo/Redo
- CRUD Operations

**v1.0** - Mobile & UX
- Touch support
- Responsive design

---

**Project:** Motia DRAKON Viewer  
**Location:** `/home/vokov/motia-drn/tools/drakon-viewer/`  
**Credits:** [drakonwidget](https://github.com/stepan-mitkin/drakonwidget) | [DRAKON Methodology](https://drakon.tech/)
