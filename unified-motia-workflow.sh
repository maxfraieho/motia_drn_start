#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# Unified Motia Development Pipeline v2.0
# Інтегрує всі 3 підсистеми: Automation + Migration + Markdown Service
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ───────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────

readonly VERSION="2.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directories
readonly PATTERNS_DIR="$SCRIPT_DIR/patterns"
readonly STEPS_DIR="$SCRIPT_DIR/motia-output/steps"
readonly DESCRIPTIONS_DIR="$SCRIPT_DIR/step-descriptions"
readonly OUTPUT_DIR="$SCRIPT_DIR/gen-md-refactor/output"
readonly MD_SERVICE_DIR="$SCRIPT_DIR/gen-md-refactor"

# Scripts
readonly AUTOMATION_SCRIPT="$SCRIPT_DIR/motia-claude-workflow.sh"
readonly MD_SERVICE_SCRIPT="$MD_SERVICE_DIR/motia-md-service.sh"
readonly MD_SERVICE_PY="$MD_SERVICE_DIR/motia-md-service.py"

# Context files
readonly CLAUDE_CORE="$SCRIPT_DIR/CLAUDE-CORE.md"
readonly SESSION_CONTEXT="$SCRIPT_DIR/SESSION-CONTEXT.md"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly MAGENTA='\033[0;35m'
readonly BOLD='\033[1m'
readonly RESET='\033[0m'

# ───────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ───────────────────────────────────────────────────────────────────────────

log_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

log_success() {
    echo -e "${GREEN}✅${RESET} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${RESET}  $1"
}

log_error() {
    echo -e "${RED}❌${RESET} $1"
}

log_step() {
    echo -e "\n${CYAN}${BOLD}▶ $1${RESET}\n"
}

check_dependency() {
    local cmd=$1
    local name=$2
    if ! command -v "$cmd" &> /dev/null; then
        log_error "$name не знайдено. Встановіть: $cmd"
        return 1
    fi
    return 0
}

validate_environment() {
    log_step "Перевірка середовища"

    local all_ok=true

    # Python
    if check_dependency python3 "Python 3"; then
        log_success "Python 3: $(python3 --version)"
    else
        all_ok=false
    fi

    # Claude CLI (optional for some operations)
    if check_dependency claude "Claude CLI"; then
        log_success "Claude CLI: встановлено"
    else
        log_warning "Claude CLI не знайдено (опціонально для деяких операцій)"
    fi

    # Key files
    if [ -f "$CLAUDE_CORE" ]; then
        log_success "CLAUDE-CORE.md знайдено"
    else
        log_warning "CLAUDE-CORE.md не знайдено"
    fi

    if [ -f "$SESSION_CONTEXT" ]; then
        log_success "SESSION-CONTEXT.md знайдено"
    else
        log_warning "SESSION-CONTEXT.md не знайдено"
    fi

    if [ "$all_ok" = false ]; then
        log_error "Деякі залежності відсутні"
        return 1
    fi

    return 0
}

# ───────────────────────────────────────────────────────────────────────────
# MAIN COMMANDS
# ───────────────────────────────────────────────────────────────────────────

cmd_init() {
    local step_name=$1
    local step_type=$2
    local pattern=$3

    log_step "INIT: Ініціалізація нового кроку"

    log_info "Step: $step_name"
    log_info "Type: $step_type"
    log_info "Pattern: $pattern"

    # Create step directory structure
    local step_dir="$STEPS_DIR/$step_name"

    if [ -d "$step_dir" ]; then
        log_warning "Директорія вже існує: $step_dir"
        read -p "Перезаписати? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Скасовано"
            return 0
        fi
        rm -rf "$step_dir"
    fi

    mkdir -p "$step_dir/diagrams"
    log_success "Створено структуру: $step_dir"

    # Create placeholder files
    touch "$step_dir/handler.ts"
    touch "$step_dir/config.json"
    touch "$step_dir/schema.json"
    touch "$step_dir/README.md"

    log_success "Створено файли кроку"

    log_info "Наступний крок: ./unified-motia-workflow.sh describe $step_name"
}

cmd_describe() {
    local step_name=$1
    local step_type=${2:-"event"}
    local pattern=${3:-"observer"}
    local description=${4:-""}
    local language=${5:-"typescript"}

    log_step "DESCRIBE: Створення опису кроку"

    if [ -z "$description" ]; then
        read -p "Введіть опис кроку: " description
    fi

    # Use automation system to create description
    if [ -f "$AUTOMATION_SCRIPT" ]; then
        log_info "Використовується Automation System..."
        "$AUTOMATION_SCRIPT" create-desc "$step_name" "$step_type" "$pattern" "$description" "$language"
    else
        log_error "Automation script не знайдено: $AUTOMATION_SCRIPT"
        return 1
    fi

    log_success "Опис створено: step-descriptions/${step_name}-description.md"
    log_info "Наступний крок: ./unified-motia-workflow.sh aggregate $step_name $pattern"
}

cmd_aggregate() {
    local step_name=$1
    local pattern=${2:-"observer"}

    log_step "AGGREGATE: Агрегація контексту для Claude CLI"

    # Check if we have step directory or description
    local step_dir="$STEPS_DIR/$step_name"
    local step_desc="$DESCRIPTIONS_DIR/${step_name}-description.md"

    if [ ! -d "$step_dir" ] && [ ! -f "$step_desc" ]; then
        log_error "Не знайдено ні директорії, ні опису для кроку: $step_name"
        return 1
    fi

    # Use Markdown Service for 3-level context aggregation
    log_info "Використовується Markdown Service (триступенева агрегація)..."

    # Check if Python service is available
    if [ ! -f "$MD_SERVICE_PY" ]; then
        log_error "Markdown Service не знайдено: $MD_SERVICE_PY"
        return 1
    fi

    # Call Python service directly for aggregation
    python3 "$MD_SERVICE_PY" aggregate-three-level \
        --pattern "$pattern" \
        --step "$step_name" \
        --output-dir "$OUTPUT_DIR"

    log_success "Агреговано 3 рівні контексту:"
    log_info "  • Project Context: $OUTPUT_DIR/motia-project-context.md"
    log_info "  • Pattern Context: $OUTPUT_DIR/motia-pattern-${pattern}.md"
    log_info "  • Step Context: $DESCRIPTIONS_DIR/${step_name}-complete.md"

    log_info "Наступний крок: ./unified-motia-workflow.sh generate $step_name $pattern"
}

cmd_generate() {
    local step_name=$1
    local pattern=${2:-"observer"}
    local task=${3:-"Generate complete implementation"}

    log_step "GENERATE: Генерація коду через Claude CLI"

    # Validate context files exist
    local project_context="$OUTPUT_DIR/motia-project-context.md"
    local pattern_context="$OUTPUT_DIR/motia-pattern-${pattern}.md"
    local step_context="$DESCRIPTIONS_DIR/${step_name}-complete.md"

    if [ ! -f "$step_context" ]; then
        # Fallback to description
        step_context="$DESCRIPTIONS_DIR/${step_name}-description.md"
    fi

    if [ ! -f "$project_context" ] || [ ! -f "$pattern_context" ] || [ ! -f "$step_context" ]; then
        log_error "Контекстні файли не знайдено. Спочатку виконайте aggregate"
        return 1
    fi

    # Check Claude CLI
    if ! check_dependency claude "Claude CLI"; then
        log_error "Claude CLI необхідний для генерації"
        return 1
    fi

    log_info "Генерація з 3 рівнями контексту..."

    # Build Claude command
    local claude_cmd="claude \
        --context-file \"$project_context\" \
        --context-file \"$pattern_context\" \
        --context-file \"$step_context\" \
        -p \"$task\""

    log_info "Команда Claude CLI:"
    echo -e "${CYAN}$claude_cmd${RESET}"
    echo

    read -p "Виконати? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        eval "$claude_cmd"
        log_success "Генерація завершена"
        log_info "Наступний крок: ./unified-motia-workflow.sh docs $step_name"
    else
        log_info "Команду скопійовано в буфер (якщо підтримується)"
        echo "$claude_cmd"
    fi
}

cmd_docs() {
    local step_name=$1

    log_step "DOCS: Генерація документації"

    local step_dir="$STEPS_DIR/$step_name"

    if [ ! -d "$step_dir" ]; then
        log_error "Директорія кроку не знайдена: $step_dir"
        return 1
    fi

    # Check if handler exists
    if [ ! -f "$step_dir/handler.ts" ] || [ ! -s "$step_dir/handler.ts" ]; then
        log_error "handler.ts не знайдено або порожній"
        return 1
    fi

    log_info "Генерація config.json, schema.json, README.md..."

    # Use Claude to generate documentation from handler
    if check_dependency claude "Claude CLI"; then
        local handler_content
        handler_content=$(cat "$step_dir/handler.ts")

        local prompt="Based on the following TypeScript handler, generate:
1. config.json - Step metadata
2. schema.json - Input/output JSON schemas
3. README.md - Comprehensive documentation

Handler code:
\`\`\`typescript
$handler_content
\`\`\`

Generate each file separately."

        claude --context-file "$CLAUDE_CORE" -p "$prompt"

        log_success "Документація згенерована (перевірте вивід Claude)"
        log_info "Наступний крок: ./unified-motia-workflow.sh drakon $step_name"
    else
        log_warning "Claude CLI недоступний, використовуються шаблони"

        # Create basic templates
        cat > "$step_dir/config.json" <<EOF
{
  "name": "$step_name",
  "version": "1.0.0",
  "type": "event",
  "pattern": "observer"
}
EOF

        cat > "$step_dir/schema.json" <<EOF
{
  "input": {},
  "output": {}
}
EOF

        cat > "$step_dir/README.md" <<EOF
# $step_name

## Overview

TODO: Add description

## Usage

TODO: Add usage examples

## Events

TODO: Document events
EOF

        log_success "Базові шаблони створено"
    fi
}

cmd_drakon() {
    local step_name=$1

    log_step "DRAKON: Генерація візуальних діаграм"

    local step_dir="$STEPS_DIR/$step_name"
    local diagrams_dir="$step_dir/diagrams"
    local drakon_tools_dir="$SCRIPT_DIR/tools/drakon/converter"
    local generate_diagrams_script="$drakon_tools_dir/generate_step_diagrams.py"

    if [ ! -d "$step_dir" ]; then
        log_error "Директорія кроку не знайдена: $step_dir"
        return 1
    fi

    if [ ! -f "$generate_diagrams_script" ]; then
        log_error "Основний скрипт генерації ДРАКОН не знайдено: $generate_diagrams_script"
        return 1
    fi

    log_info "Генерація 4-х стандартних діаграм з аналізу метаданих кроку..."
    log_info "Використовується: $generate_diagrams_script"

    python3 "$generate_diagrams_script" \
        --step-name "$step_name" \
        --step-dir "$step_dir" \
        --output-dir "$diagrams_dir" \
        --formats drn,json || {
            log_error "Помилка під час генерації ДРАКОН діаграм"
            return 1
        }

    echo
    log_success "✅ DRAKON діаграми успішно згенеровано!"
    log_info "Створено файли:"
    log_info "  • initialization.drn + initialization.json"
    log_info "  • main-flow.drn + main-flow.json"
    log_info "  • error-handling.drn + error-handling.json"
    log_info "  • cleanup.drn + cleanup.json"
    echo
    log_info "📊 Візуалізація:"
    log_info "  • .drn файли → Відкрийте в DRAKON Editor (desktop)"
    log_info "  • .json файли → Завантажте на https://drakonhub.com/editor або перегляньте локально"
    echo
    log_info "Наступний крок: ./unified-motia-workflow.sh validate $step_name"

    # Оновлюємо індекс для локального переглядача
    local indexer_script="$SCRIPT_DIR/tools/drakon-viewer/generate-diagram-index.sh"
    if [ -f "$indexer_script" ]; then
        log_info "Оновлення індексу для локального переглядача..."
        bash "$indexer_script"
    fi
}

cmd_validate() {
    local step_name=$1

    log_step "VALIDATE: Валідація кроку"

    local step_dir="$STEPS_DIR/$step_name"

    if [ ! -d "$step_dir" ]; then
        log_error "Директорія кроку не знайдена: $step_dir"
        return 1
    fi

    local errors=0

    # Check required files
    log_info "Перевірка обов'язкових файлів..."

    local required_files=(
        "handler.ts"
        "config.json"
        "schema.json"
        "README.md"
    )

    for file in "${required_files[@]}"; do
        if [ -f "$step_dir/$file" ] && [ -s "$step_dir/$file" ]; then
            log_success "$file ✓"
        else
            log_error "$file відсутній або порожній"
            ((errors++))
        fi
    done

    # Check diagrams
    log_info "Перевірка діаграм..."

    local json_diagram_count
    json_diagram_count=$(find "$step_dir/diagrams" -name "*.json" -type f 2>/dev/null | wc -l)

    if [ "$json_diagram_count" -ge 4 ]; then
        log_success "JSON діаграми: $json_diagram_count ✓"
    else
        log_warning "JSON діаграми: $json_diagram_count (рекомендовано 4)"
    fi

    # Validate JSON files
    log_info "Валідація JSON..."

    for json_file in "$step_dir/config.json" "$step_dir/schema.json"; do
        if [ -f "$json_file" ]; then
            if python3 -c "import json; json.load(open('$json_file'))" 2>/dev/null; then
                log_success "$(basename "$json_file") валідний JSON ✓"
            else
                log_error "$(basename "$json_file") невалідний JSON"
                ((errors++))
            fi
        fi
    done

    # Summary
    echo
    if [ $errors -eq 0 ]; then
        log_success "Валідація пройдена успішно!"
        log_info "Наступний крок: ./unified-motia-workflow.sh integrate $step_name"
        return 0
    else
        log_error "Валідація не пройдена: $errors помилок"
        return 1
    fi
}

cmd_integrate() {
    local step_name=$1

    log_step "INTEGRATE: Інтеграція кроку в проєкт"

    # Update motia-config.json
    local config_file="$SCRIPT_DIR/motia-output/motia-config.json"

    if [ -f "$config_file" ]; then
        log_info "Оновлення motia-config.json..."
        log_warning "Автоматичне оновлення поки не реалізовано"
        log_info "Вручну додайте крок до: $config_file"
    fi

    # Update FILE_INDEX.md
    local file_index="$SCRIPT_DIR/motia-output/FILE_INDEX.md"

    if [ -f "$file_index" ]; then
        log_info "Оновлення FILE_INDEX.md..."
        log_warning "Автоматичне оновлення поки не реалізовано"
        log_info "Вручну оновіть статус в: $file_index"
    fi

    log_success "Крок готовий до використання!"
    log_info "Розташування: $STEPS_DIR/$step_name"
}

cmd_full_pipeline() {
    local step_name=$1
    local step_type=$2
    local pattern=$3
    local description=$4
    local language=${5:-"typescript"}

    log_step "FULL PIPELINE: Повний цикл розробки кроку"

    log_info "Step: $step_name"
    log_info "Type: $step_type"
    log_info "Pattern: $pattern"
    log_info "Description: $description"
    log_info "Language: $language"

    echo
    read -p "Продовжити? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        log_info "Скасовано"
        return 0
    fi

    # 1. Init
    cmd_init "$step_name" "$step_type" "$pattern" || return 1

    # 2. Describe
    cmd_describe "$step_name" "$step_type" "$pattern" "$description" "$language" || return 1

    # 3. Aggregate
    cmd_aggregate "$step_name" "$pattern" || return 1

    # 4. Generate
    cmd_generate "$step_name" "$pattern" || return 1

    # 5. Docs
    cmd_docs "$step_name" || return 1

    # 6. DRAKON
    cmd_drakon "$step_name" || return 1

    # 7. Validate
    cmd_validate "$step_name" || return 1

    # 8. Integrate
    cmd_integrate "$step_name" || return 1

    log_success "════════════════════════════════════════════════════════════"
    log_success "FULL PIPELINE ЗАВЕРШЕНО УСПІШНО!"
    log_success "════════════════════════════════════════════════════════════"
}

cmd_status() {
    log_step "STATUS: Статус проєкту"
}

cmd_status() {
    log_step "STATUS: Статус проєкту"

    # Count completed steps
    local total_steps=15
    local completed_steps=0

    if [ -d "$STEPS_DIR" ]; then
        for step_dir in "$STEPS_DIR"/*/; do
            if [ -f "$step_dir/handler.ts" ] && [ -f "$step_dir/config.json" ] && \
               [ -f "$step_dir/schema.json" ] && [ -f "$step_dir/README.md" ]; then
                ((completed_steps++))
            fi
        done
    fi

    local progress=$((completed_steps * 100 / total_steps))

    echo -e "${BOLD}Прогрес проєкту:${RESET}"
    echo -e "  Завершено: ${GREEN}$completed_steps${RESET}/$total_steps steps"
    echo -e "  Прогрес: ${CYAN}$progress%${RESET}"
    echo

    # List completed steps
    if [ $completed_steps -gt 0 ]; then
        echo -e "${BOLD}Завершені кроки:${RESET}"
        for step_dir in "$STEPS_DIR"/*/; do
            local step_name
            step_name=$(basename "$step_dir")
            if [ -f "$step_dir/handler.ts" ] && [ -f "$step_dir/config.json" ]; then
                echo -e "  ${GREEN}✓${RESET} $step_name"
            fi
        done
    fi

    echo

    # Next steps
    echo -e "${BOLD}Рекомендовані наступні кроки:${RESET}"
    if [ $completed_steps -lt $total_steps ]; then
        echo "  1. Завершити залишки steps ($(($total_steps - $completed_steps)) залишилось)"
        echo "  2. Додати integration tests"
        echo "  3. Deploy to Motia Cloud"
    else
        echo "  Всі steps завершено! Готово до deployment"
    fi
}

# ───────────────────────────────────────────────────────────────────────────
# HELP
# ───────────────────────────────────────────────────────────────────────────

show_help() {
    cat <<EOF
${BOLD}Unified Motia Development Pipeline v${VERSION}${RESET}

Інтегрована система для розробки Motia Steps з AI-assisted workflow

${BOLD}USAGE:${RESET}
    $0 <command> [arguments...]

${BOLD}COMMANDS:${RESET}

  ${CYAN}init${RESET} <name> <type> <pattern>
    Ініціалізувати новий крок з структурою директорій

  ${CYAN}describe${RESET} <name> [type] [pattern] [description] [language]
    Створити опис кроку (використовує Automation System)

  ${CYAN}aggregate${RESET} <name> [pattern]
    Агрегувати 3 рівні контексту (використовує Markdown Service)

  ${CYAN}generate${RESET} <name> [pattern] [task]
    Згенерувати код через Claude CLI з контекстом

  ${CYAN}docs${RESET} <name>
    Згенерувати config.json, schema.json, README.md

  ${CYAN}drakon${RESET} <name>
    🔥 Генерувати візуальні DRAKON діаграми (.drn + .json) з аналізу коду

  ${CYAN}validate${RESET} <name>
    Валідувати крок (файли, JSON, діаграми)

  ${CYAN}integrate${RESET} <name>
    Інтегрувати крок в проєкт (оновити конфіги)

  ${CYAN}full-pipeline${RESET} <name> <type> <pattern> <description> [language]
    Виконати повний цикл: init → describe → aggregate → generate → docs → drakon → validate → integrate

  ${CYAN}status${RESET}
    Показати статус проєкту та прогрес

  ${CYAN}help${RESET}
    Показати цю довідку

${BOLD}EXAMPLES:${RESET}

  # Повний цикл для нового кроку
  $0 full-pipeline payment-service event strategy "Payment processing service" typescript

  # Покрокове виконання
  $0 init notification-service event observer
  $0 describe notification-service event observer "Email notifications"
  $0 aggregate notification-service observer
  $0 generate notification-service observer
  $0 docs notification-service
  $0 drakon notification-service
  $0 validate notification-service

  # Статус проєкту
  $0 status

${BOLD}STEP TYPES:${RESET}
  api, event, cron, stream

${BOLD}PATTERNS:${RESET}
  observer, command, strategy, chain-of-responsibility, state, factory, mediator, template-method

${BOLD}SUPPORTED BY:${RESET}
  • Automation System (root): Create descriptions
  • Markdown Service (gen-md-refactor): 3-level context aggregation
  • Migration Project (motia-output): Generated steps storage

${BOLD}VERSION:${RESET} $VERSION
${BOLD}AUTHOR:${RESET} Claude Code + Human Collaboration
EOF
}

# ───────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────

main() {
    local command=${1:-help}
    shift || true

    case $command in
        init)
            validate_environment || exit 1
            cmd_init "$@"
            ;;
        describe)
            validate_environment || exit 1
            cmd_describe "$@"
            ;;
        aggregate)
            validate_environment || exit 1
            cmd_aggregate "$@"
            ;;
        generate)
            validate_environment || exit 1
            cmd_generate "$@"
            ;;
        docs)
            validate_environment || exit 1
            cmd_docs "$@"
            ;;
        drakon)
            validate_environment || exit 1
            cmd_drakon "$@"
            ;;
        validate)
            cmd_validate "$@"
            ;;
        integrate)
            cmd_integrate "$@"
            ;;
        full-pipeline)
            validate_environment || exit 1
            cmd_full_pipeline "$@"
            ;;
        status)
            cmd_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Невідома команда: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

main "$@"
