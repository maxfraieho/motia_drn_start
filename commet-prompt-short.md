# Quick Prompt для Commet: DRAKON Viewer Research

Commet, проведи глибоке дослідження та створи детальний план покращення DRAKON діаграм viewer для проєкту Motia.

## Що потрібно дослідити:

### 1. Наш поточний viewer
- URL: http://localhost:8080
- Код: /home/vokov/motia-drn/tools/drakon-viewer/
- Проаналізуй функціонал, обмеження, UX/UI

### 2. DrakonWidget (глибоко!)
- Репозиторій: https://github.com/stepan-mitkin/drakonwidget
- Демо: https://stepan-mitkin.github.io/drakonwidget/
- Вивчи API, методи редагування, можливості, обмеження

### 3. Створи план покращення для:

**Мобільна адаптація:**
- Responsive дизайн 320px-2560px
- Touch-friendly інтерфейс + gestures
- Performance optimization
- PWA features

**Редагування діаграм:**
- Edit mode з drag & drop
- Додавання/редагування елементів (action, question, branch, loop)
- Undo/redo, автозбереження
- Візуальний редактор

**Створення нових діаграм:**
- Wizard з шаблонами
- Code-to-diagram генератор
- Інтеграція з Motia триступеневим підходом
- Експорт у різні формати

**Рефакторинг існуючих:**
- Аналіз /home/vokov/motia-drn/motia-output/steps/*.json
- Оптимізація структури
- Стандартизація формату

## Deliverables:

1. **Звіт:** поточний стан, gap analysis, DrakonWidget можливості
2. **Технічна специфікація:** архітектура, tech stack, API дизайн
3. **Roadmap:** 12-тижневий план з фазами (Foundations → Editor → Mobile → Advanced → Motia Integration)
4. **Code examples:** POC для ключових функцій
5. **UI/UX:** wireframes, user flows, design guidelines

## Критерії успіху:
✅ Повноцінне редагування в браузері
✅ Відмінна робота на мобільних (iOS/Android)
✅ Створення діаграм з нуля/шаблонів
✅ Автогенерація з коду
✅ Інтеграція з Motia workflow
✅ Production-ready рішення

**Досліджуй максимально детально. Особливу увагу - мобільній адаптації та редагуванню!**
