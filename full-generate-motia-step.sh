#!/bin/bash

# Повна автоматизація створення Motia Step з ДРАКОН діаграмами
# Використання: ./full-generate-motia-step.sh <step-name> <step-type> <pattern> <description> [language]

STEP_NAME=$1
STEP_TYPE=$2
PATTERN=$3
DESCRIPTION=$4
LANGUAGE=${5:-typescript}

if [ -z "$STEP_NAME" ] || [ -z "$STEP_TYPE" ] || [ -z "$PATTERN" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 <step-name> <step-type> <pattern> <description> [language]"
    echo ""
    echo "Цей скрипт виконує повний цикл:"
    echo "1. Створює step-description.md з повною структурою"
    echo "2. Генерує код через Claude CLI з триступеневим промптом"
    echo "3. Створює всі необхідні файли та папки"
    exit 1
fi

echo "🚀 Повна автоматизація створення Motia Step"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Крок: $STEP_NAME"
echo "Тип: $STEP_TYPE" 
echo "Патерн: $PATTERN"
echo "Опис: $DESCRIPTION"
echo "Мова: $LANGUAGE"
echo ""

# Крок 1: Створення опису кроку
echo "📝 Крок 1: Створення опису кроку..."
./create-step-description.sh "$STEP_NAME" "$STEP_TYPE" "$PATTERN" "$DESCRIPTION" "$LANGUAGE"

if [ $? -ne 0 ]; then
    echo "❌ Помилка створення опису кроку"
    exit 1
fi

# Перевірка існування необхідних файлів
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ Помилка: CLAUDE.md не знайдено"
    echo "Створіть базовий Motia контекст файл"
    exit 1
fi

if [ ! -f "patterns/${PATTERN}-pattern.md" ]; then
    echo "❌ Помилка: patterns/${PATTERN}-pattern.md не знайдено"
    echo "Створіть патерн-специфічний промпт файл"
    exit 1
fi

# Крок 2: Генерація коду через Claude CLI
echo "🤖 Крок 2: Генерація коду через Claude CLI..."
echo ""

# Формування триступеневого промпту
FULL_PROMPT="$(cat CLAUDE.md)

━━━ PATTERN SPECIFIC INSTRUCTIONS ━━━
$(cat patterns/${PATTERN}-pattern.md)

━━━ STEP FULL DESCRIPTION ━━━
$(cat step-descriptions/${STEP_NAME}-description.md)

ГЕНЕРУЙ ПОВНУ РЕАЛІЗАЦІЮ КРОКУ ЗГІДНО ОПИСУ ВИЩЕ!"

# Виконання Claude CLI команди
claude -p "$FULL_PROMPT" --output-dir "generated-steps/$STEP_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Генерація завершена успішно!"
    echo ""
    echo "📁 Результати збережено в: generated-steps/$STEP_NAME/"
    echo "📋 Опис кроку: step-descriptions/${STEP_NAME}-description.md"
    echo ""
    echo "🧪 Для тестування використайте:"
    case $STEP_TYPE in
        "api")
            echo "curl -X POST http://localhost:8080/$STEP_NAME -d '{"data": {}}'"
            ;;
        "event") 
            echo "npx motia emit $STEP_NAME.trigger '{"data": {}}'"
            ;;
        "cron")
            echo "npx motia cron trigger $STEP_NAME"
            ;;
        "stream")
            echo "npx motia emit stream.data '{"data": {}}'"
            ;;
    esac
    echo ""
    echo "📊 Моніторинг:"
    echo "npx motia logs $STEP_NAME"
    echo "npx motia dev  # Відкрити Workbench"
else
    echo "❌ Помилка генерації коду"
    exit 1
fi
