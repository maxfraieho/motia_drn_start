#!/bin/bash

# Інтегрований workflow для роботи з Motia Steps через Claude CLI
# Використання: ./motia-claude-workflow.sh <action> [parameters...]

ACTION=$1

show_help() {
    echo "Motia Claude CLI Workflow - Інтегрована система для роботи з кроками"
    echo ""
    echo "Usage: $0 <action> [parameters...]"
    echo ""
    echo "Actions:"
    echo "  create-desc <name> <type> <pattern> <description> [lang]"
    echo "    Створити новий опис кроку"
    echo ""
    echo "  aggregate <step-folder> [output-name]"
    echo "    Агрегувати існуючу папку кроку в markdown"
    echo ""
    echo "  generate <step-description-file> [pattern]"
    echo "    Згенерувати код через Claude CLI"
    echo ""
    echo "  full-cycle <name> <type> <pattern> <description> [lang]"
    echo "    Повний цикл: створити опис + згенерувати код"
    echo ""
    echo "  aggregate-and-generate <step-folder> [pattern]"
    echo "    Агрегувати існуючу папку + згенерувати оптимізований код"
    echo ""
    echo "Examples:"
    echo "  $0 create-desc user-processor event observer 'Обробляє користувачів'"
    echo "  $0 aggregate ./existing-step user-step-full"
    echo "  $0 generate step-descriptions/user-processor-description.md observer"
    echo "  $0 full-cycle order-api api command 'CRUD API для замовлень'"
    echo "  $0 aggregate-and-generate ./legacy-step command"
}

case $ACTION in
    "create-desc")
        STEP_NAME=$2
        STEP_TYPE=$3
        PATTERN=$4
        DESCRIPTION=$5
        LANGUAGE=${6:-typescript}

        if [ -z "$STEP_NAME" ] || [ -z "$STEP_TYPE" ] || [ -z "$PATTERN" ] || [ -z "$DESCRIPTION" ]; then
            echo "❌ Недостатньо аргументів для create-desc"
            show_help
            exit 1
        fi

        echo "📝 Створення опису кроку..."
        ./create-step-description.sh "$STEP_NAME" "$STEP_TYPE" "$PATTERN" "$DESCRIPTION" "$LANGUAGE"
        ;;

    "aggregate")
        STEP_FOLDER=$2
        OUTPUT_NAME=${3:-"$(basename $STEP_FOLDER)-complete"}

        if [ -z "$STEP_FOLDER" ] || [ ! -d "$STEP_FOLDER" ]; then
            echo "❌ Невалідна папка кроку: $STEP_FOLDER"
            show_help
            exit 1
        fi

        echo "📦 Агрегація папки кроку..."
        ./aggregate-step-to-md.sh "$STEP_FOLDER" "$OUTPUT_NAME"
        ;;

    "generate")
        DESCRIPTION_FILE=$2
        PATTERN=${3:-"observer"}

        if [ -z "$DESCRIPTION_FILE" ] || [ ! -f "$DESCRIPTION_FILE" ]; then
            echo "❌ Файл опису не знайдено: $DESCRIPTION_FILE"
            show_help
            exit 1
        fi

        # Перевірка наявності компактного промпту (пріоритет) або повного
        if [ -f "CLAUDE-CORE.md" ]; then
            CONTEXT_FILE="CLAUDE-CORE.md"
            echo "✅ Використовується компактний контекст: CLAUDE-CORE.md"
        elif [ -f "CLAUDE.md" ]; then
            CONTEXT_FILE="CLAUDE.md"
            echo "⚠️  Використовується повний контекст: CLAUDE.md (рекомендується CLAUDE-CORE.md)"
        else
            echo "❌ Файл контексту не знайдено. Потрібен CLAUDE-CORE.md або CLAUDE.md"
            exit 1
        fi

        if [ ! -f "patterns/$PATTERN-pattern.md" ]; then
            echo "❌ patterns/$PATTERN-pattern.md не знайдено."
            echo "Доступні patterns:"
            ls patterns/*.md 2>/dev/null | sed 's/patterns\///g' | sed 's/-pattern.md//g' || echo "  (папка patterns/ порожня)"
            exit 1
        fi

        echo "🤖 Генерація коду через Claude CLI..."
        echo "   Контекст: $CONTEXT_FILE"
        echo "   Pattern: patterns/$PATTERN-pattern.md"
        claude --append-system-prompt "$(cat $CONTEXT_FILE)" \
               --append-system-prompt "$(cat patterns/$PATTERN-pattern.md)" \
               -p "$(cat $DESCRIPTION_FILE)"
        ;;

    "full-cycle")
        STEP_NAME=$2
        STEP_TYPE=$3
        PATTERN=$4
        DESCRIPTION=$5
        LANGUAGE=${6:-typescript}

        if [ -z "$STEP_NAME" ] || [ -z "$STEP_TYPE" ] || [ -z "$PATTERN" ] || [ -z "$DESCRIPTION" ]; then
            echo "❌ Недостатньо аргументів для full-cycle"
            show_help
            exit 1
        fi

        echo "🔄 Повний цикл створення кроку..."
        echo "1️⃣ Створення опису..."
        ./create-step-description.sh "$STEP_NAME" "$STEP_TYPE" "$PATTERN" "$DESCRIPTION" "$LANGUAGE"

        echo "2️⃣ Генерація коду..."
        ./motia-claude-workflow.sh generate "step-descriptions/${STEP_NAME}-description.md" "$PATTERN"
        ;;

    "aggregate-and-generate")
        STEP_FOLDER=$2
        PATTERN=${3:-"observer"}

        if [ -z "$STEP_FOLDER" ] || [ ! -d "$STEP_FOLDER" ]; then
            echo "❌ Невалідна папка кроку: $STEP_FOLDER"
            show_help
            exit 1
        fi

        STEP_NAME=$(basename "$STEP_FOLDER")
        OUTPUT_NAME="${STEP_NAME}-optimized"

        echo "🔄 Агрегація + оптимізація існуючого кроку..."
        echo "1️⃣ Агрегація папки..."
        ./aggregate-step-to-md.sh "$STEP_FOLDER" "$OUTPUT_NAME"

        echo "2️⃣ Генерація оптимізованого коду..."
        ./motia-claude-workflow.sh generate "step-descriptions/${OUTPUT_NAME}.md" "$PATTERN"
        ;;

    *)
        echo "❌ Невідома дія: $ACTION"
        show_help
        exit 1
        ;;
esac
