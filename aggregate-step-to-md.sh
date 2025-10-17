#!/bin/bash

# Агрегатор папки Motia Step в один markdown файл для Claude CLI
# Використання: ./aggregate-step-to-md.sh <step-folder-path> <output-name>

STEP_FOLDER=$1
OUTPUT_NAME=${2:-"step-complete-description"}

if [ -z "$STEP_FOLDER" ] || [ ! -d "$STEP_FOLDER" ]; then
    echo "Usage: $0 <step-folder-path> [output-name]"
    echo ""
    echo "Приклад:"
    echo "  $0 ./user-processor user-processor-full"
    echo "  $0 ./steps/api/create-order create-order-complete"
    echo ""
    echo "Структура папки має містити:"
    echo "  handler.ts/py         # Логіка кроку"
    echo "  config.json           # Конфігурація Motia"
    echo "  schema.json           # Схема валідації"
    echo "  README.md             # Документація"
    echo "  diagrams/             # ДРАКОН діаграми"
    echo "  tests/                # Тести"
    echo "  docs/                 # Додаткова документація"
    exit 1
fi

# Отримуємо назву кроку з папки
STEP_NAME=$(basename "$STEP_FOLDER")
OUTPUT_FILE="step-descriptions/${OUTPUT_NAME}.md"

# Створюємо папку для результатів
mkdir -p step-descriptions

# Початок markdown файлу
cat > "$OUTPUT_FILE" << EOF
# $STEP_NAME - Повний агрегований опис кроку Motia

> Цей файл містить всю інформацію з папки кроку для передачі в Claude CLI

## 🏗️ Структура кроку
\`\`\`
EOF

# Додаємо структуру папки
echo "$STEP_NAME/" >> "$OUTPUT_FILE"
find "$STEP_FOLDER" -type f -o -type d | sort | sed "s|$STEP_FOLDER|├──|g" | sed 's/├──/├── /' >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'
```

## 📋 Конфігурація кроку

EOF

# Додаємо config.json якщо існує
if [ -f "$STEP_FOLDER/config.json" ]; then
    echo "### config.json" >> "$OUTPUT_FILE"
    echo '```json' >> "$OUTPUT_FILE"
    cat "$STEP_FOLDER/config.json" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Додаємо schema.json якщо існує
if [ -f "$STEP_FOLDER/schema.json" ]; then
    echo "### schema.json" >> "$OUTPUT_FILE"
    echo '```json' >> "$OUTPUT_FILE"
    cat "$STEP_FOLDER/schema.json" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Додаємо основну логіку кроку
echo "## 🔧 Реалізація кроку" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# handler.ts або handler.py
for handler_file in "$STEP_FOLDER/handler.ts" "$STEP_FOLDER/handler.py" "$STEP_FOLDER/handler.rb"; do
    if [ -f "$handler_file" ]; then
        handler_ext="${handler_file##*.}"
        echo "### $(basename $handler_file)" >> "$OUTPUT_FILE"
        echo "\`\`\`$handler_ext" >> "$OUTPUT_FILE"
        cat "$handler_file" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        break
    fi
done

# ДРАКОН діаграми
echo "## 🎨 ДРАКОН діаграми" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

if [ -d "$STEP_FOLDER/diagrams" ]; then
    for diagram in "$STEP_FOLDER/diagrams"/*.drakon; do
        if [ -f "$diagram" ]; then
            diagram_name=$(basename "$diagram" .drakon)
            echo "### $diagram_name.drakon" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
            cat "$diagram" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    done
else
    echo "⚠️ Папка diagrams/ не знайдена" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# README.md
if [ -f "$STEP_FOLDER/README.md" ]; then
    echo "## 📚 Документація кроку" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    cat "$STEP_FOLDER/README.md" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Тести
echo "## 🧪 Тести" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

if [ -d "$STEP_FOLDER/tests" ]; then
    for test_file in "$STEP_FOLDER/tests"/**/*test*; do
        if [ -f "$test_file" ]; then
            test_ext="${test_file##*.}"
            test_name=$(basename "$test_file")
            echo "### $test_name" >> "$OUTPUT_FILE"
            echo "\`\`\`$test_ext" >> "$OUTPUT_FILE"
            cat "$test_file" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    done
else
    echo "⚠️ Папка tests/ не знайдена" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Додаткова документація з папки docs/
if [ -d "$STEP_FOLDER/docs" ]; then
    echo "## 📖 Додаткова документація" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    for doc_file in "$STEP_FOLDER/docs"/*.md; do
        if [ -f "$doc_file" ]; then
            doc_name=$(basename "$doc_file" .md)
            echo "### $doc_name.md" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            cat "$doc_file" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    done
fi

# Заключна секція з інструкціями для Claude
cat >> "$OUTPUT_FILE" << 'EOF'

## 🎯 Інструкції для Claude CLI

### Що потрібно зробити:
1. **Проаналізувати** всю структуру кроку вище
2. **Оптимізувати** код відповідно до best practices Motia
3. **Доповнити** відсутні файли (якщо потрібно)
4. **Перевірити** відповідність ДРАКОН діаграм логіці коду
5. **Створити** повну робочу реалізацію кроку

### Вимоги до результату:
- Всі файли мають бути функціональними
- Код має відповідати Motia стандартам
- ДРАКОН діаграми мають точно відображати логіку
- Тести мають покривати основні сценарії
- Документація має бути повною та зрозумілою

### Структура результату:
Створи всі файли згідно структури кроку з оптимізованим кодом.
EOF

echo "✅ Створено агрегований опис: $OUTPUT_FILE"
echo ""
echo "🚀 Для генерації коду через Claude CLI використайте:"
echo "claude --append-system-prompt "\$(cat CLAUDE.md)" --append-system-prompt "\$(cat patterns/PATTERN-pattern.md)" -p "\$(cat $OUTPUT_FILE)""
