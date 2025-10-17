#!/bin/bash

# ============================================================================
# MOTIA MARKDOWN SERVICE v1.0 - CLI Orchestrator
# ============================================================================
# Bash-оркестратор для Motia-проєкту та інтеграції з Claude CLI
#
# Автор: DevOps Engineer
# Версія: 1.0.0
# Сумісність: Linux, macOS
# ============================================================================

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# ============================================================================
# CONFIGURATION
# ============================================================================

# Кольорові коди для CLI
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly MAGENTA='\033[0;35m'
readonly BOLD='\033[1m'
readonly NC='\033[0m' # No Color

# Назва Python-сервісу
readonly PYTHON_SERVICE="motia-md-service.py"

# Версія
readonly VERSION="1.0.0"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

print_header() {
    echo -e "${BLUE}${BOLD}"
    echo "========================================================================"
    echo "    🤖 MOTIA MARKDOWN SERVICE v${VERSION}"
    echo "    Claude CLI Integration & AI-Powered Code Generation"
    echo "========================================================================"
    echo -e "${NC}"
}

print_section() {
    echo -e "\n${CYAN}${BOLD}▶ $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${MAGENTA}  ➜ $1${NC}"
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

check_python() {
    print_section "Validation: Checking Python Installation"

    if command -v python3 &> /dev/null; then
        local py_version=$(python3 --version 2>&1)
        print_success "Python3 found: $py_version"
        PY_CMD="python3"
        return 0
    elif command -v python &> /dev/null; then
        local py_version=$(python --version 2>&1)
        print_success "Python found: $py_version"
        PY_CMD="python"
        return 0
    else
        print_error "Python not found!"
        echo ""
        print_info "Please install Python3:"
        echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  - CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "  - Fedora:        sudo dnf install python3 python3-pip"
        echo "  - Arch:          sudo pacman -S python python-pip"
        echo "  - macOS:         brew install python3"
        echo ""
        return 1
    fi
}

check_python_service() {
    print_section "Validation: Checking Python Service"

    if [[ -f "$PYTHON_SERVICE" ]]; then
        local file_size=$(stat -f%z "$PYTHON_SERVICE" 2>/dev/null || stat -c%s "$PYTHON_SERVICE" 2>/dev/null)
        print_success "Service found: $PYTHON_SERVICE (${file_size} bytes)"
        return 0
    else
        print_error "$PYTHON_SERVICE not found in current directory!"
        print_info "Current directory: $(pwd)"
        print_info "Make sure the Python service is in the same folder as this script."
        return 1
    fi
}

check_claude_cli() {
    print_section "Validation: Checking Claude CLI (optional)"

    if command -v claude &> /dev/null; then
        local claude_version=$(claude --version 2>&1 || echo "version unknown")
        print_success "Claude CLI found: $claude_version"
        CLAUDE_AVAILABLE=true
    else
        print_warning "Claude CLI not found (optional for manual workflow)"
        print_info "Install from: https://github.com/anthropics/claude-cli"
        CLAUDE_AVAILABLE=false
    fi
}

# ============================================================================
# MENU FUNCTIONS
# ============================================================================

show_main_menu() {
    clear
    print_header

    echo -e "${BOLD}Current Directory:${NC} $(pwd)"
    echo -e "${BOLD}Python Command:${NC} $PY_CMD"
    echo -e "${BOLD}Claude CLI:${NC} $(if $CLAUDE_AVAILABLE; then echo '✅ Available'; else echo '❌ Not installed'; fi)"
    echo ""

    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}${BOLD}                         MAIN MENU${NC}"
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  ${GREEN}${BOLD}[1]${NC} 🚀 Deploy Motia Project Structure"
    echo "  ${GREEN}${BOLD}[2]${NC} 📋 Aggregate Project Context (Level 1)"
    echo "  ${GREEN}${BOLD}[3]${NC} 🎯 Aggregate Pattern Context (Level 2)"
    echo "  ${GREEN}${BOLD}[4]${NC} 🔧 Aggregate Step Context (Level 3)"
    echo "  ${GREEN}${BOLD}[5]${NC} 🎯 ${BOLD}Full Pipeline: Three-Level Claude CLI Preparation${NC}"
    echo "  ${GREEN}${BOLD}[6]${NC} 🌳 Show Project Structure"
    echo "  ${GREEN}${BOLD}[7]${NC} 🐍 Launch Interactive Python Service"
    echo "  ${GREEN}${BOLD}[8]${NC} ℹ️  Help & Documentation"
    echo "  ${GREEN}${BOLD}[9]${NC} 🚪 Exit"
    echo ""
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# ============================================================================
# EXECUTION FUNCTIONS
# ============================================================================

launch_python_service() {
    print_section "Launching Interactive Python Service"

    print_step "Executing: $PY_CMD $PYTHON_SERVICE"
    echo ""

    $PY_CMD "$PYTHON_SERVICE"
    local exit_code=$?

    echo ""
    if [[ $exit_code -eq 0 ]]; then
        print_success "Python service completed successfully"
    else
        print_error "Python service exited with code: $exit_code"
    fi

    return $exit_code
}

quick_deploy_structure() {
    print_section "Quick Deploy: Motia Project Structure"

    print_info "This will create the base Motia directory structure"
    echo ""

    # Використовуємо Python для створення структури
    $PY_CMD -c "
import sys
sys.path.insert(0, '.')
from pathlib import Path

# Створюємо директорії
dirs = ['patterns', 'steps', 'output', 'step-descriptions']
for d in dirs:
    Path(d).mkdir(exist_ok=True)
    print(f'  ✅ Created: {d}/')

print('\n✅ Project structure deployed successfully!')
"

    if [[ $? -eq 0 ]]; then
        print_success "Deployment completed"
    else
        print_error "Deployment failed"
        return 1
    fi
}

aggregate_project_context() {
    print_section "Aggregating Project Context (Level 1)"

    print_info "This will create motia-project-context.md with full project overview"
    echo ""

    $PY_CMD -c "
import asyncio
import sys
sys.path.insert(0, '.')

async def run():
    # Імпорт після додавання шляху
    exec(open('$PYTHON_SERVICE').read(), globals())

    config = MotiaConfig.from_path('.')
    aggregator = MarkdownAggregator(config)
    result = aggregator.aggregate_project_context()
    print(f'\n✅ Created: {result}')

asyncio.run(run())
"

    if [[ $? -eq 0 ]]; then
        print_success "Project context aggregated"
    else
        print_error "Aggregation failed"
        return 1
    fi
}

quick_full_pipeline() {
    print_section "Full Pipeline: Three-Level Preparation"

    echo -e "${YELLOW}${BOLD}This will prepare complete context for Claude CLI:${NC}"
    echo "  1️⃣  Project Context"
    echo "  2️⃣  Pattern Context"
    echo "  3️⃣  Step Context"
    echo ""

    read -p "$(echo -e ${CYAN}📌 Enter pattern name \(e.g., factory-pattern\): ${NC})" pattern_name
    read -p "$(echo -e ${CYAN}📁 Enter step path \(e.g., ./steps/my-step\): ${NC})" step_path

    if [[ -z "$pattern_name" ]] || [[ -z "$step_path" ]]; then
        print_error "Pattern name and step path are required!"
        return 1
    fi

    print_info "Preparing three-level context..."
    echo ""

    $PY_CMD <<EOF
import asyncio
import sys
sys.path.insert(0, '.')

async def run():
    # Імпорт після додавання шляху
    exec(open('$PYTHON_SERVICE').read(), globals())

    config = MotiaConfig.from_path('.')
    aggregator = MarkdownAggregator(config)
    preparator = ClaudeStepPreparator(config, aggregator)

    await preparator.execute_claude_pipeline(
        pattern_name='$pattern_name',
        step_path='$step_path',
        auto_execute=False
    )

asyncio.run(run())
EOF

    if [[ $? -eq 0 ]]; then
        print_success "Pipeline completed successfully"

        if $CLAUDE_AVAILABLE; then
            echo ""
            print_info "Claude CLI is available. You can now execute the generated command."
        else
            echo ""
            print_warning "Claude CLI not installed. Install it to execute generated commands."
        fi
    else
        print_error "Pipeline failed"
        return 1
    fi
}

show_help() {
    clear
    print_header

    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}${BOLD}                    HELP & DOCUMENTATION${NC}"
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "${BOLD}OVERVIEW:${NC}"
    echo "  Motia Markdown Service integrates with Claude CLI to enable"
    echo "  AI-powered code generation using a three-level context approach:"
    echo ""
    echo "    Level 1: Project Context   → motia.md, README, overall structure"
    echo "    Level 2: Pattern Context   → Design pattern documentation"
    echo "    Level 3: Step Context      → Specific implementation details"
    echo ""

    echo -e "${BOLD}WORKFLOW:${NC}"
    echo "  1. Deploy project structure (Option 1)"
    echo "  2. Create/populate patterns and steps directories"
    echo "  3. Run full pipeline (Option 5) to generate Claude CLI commands"
    echo "  4. Execute generated commands with Claude CLI"
    echo ""

    echo -e "${BOLD}QUICK START:${NC}"
    echo "  $ ./motia-md-service.sh        # Launch menu"
    echo "  $ python3 motia-md-service.py  # Direct Python access"
    echo ""

    echo -e "${BOLD}REQUIREMENTS:${NC}"
    echo "  - Python 3.7+"
    echo "  - Claude CLI (optional, for auto-execution)"
    echo ""

    echo -e "${BOLD}FILES GENERATED:${NC}"
    echo "  - output/motia-project-context.md    (Level 1)"
    echo "  - output/motia-pattern-*.md          (Level 2)"
    echo "  - step-descriptions/*-complete.md    (Level 3)"
    echo ""

    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    read -p "$(echo -e ${YELLOW}Press Enter to return to menu...${NC})"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    # Change to script directory
    cd "$(dirname "$0")" || exit 1

    # Run validations
    check_python || exit 1
    check_python_service || exit 1
    check_claude_cli

    # Main loop
    while true; do
        show_main_menu

        read -p "$(echo -e ${YELLOW}${BOLD}▶ Your choice \(1-9\): ${NC})" choice

        case $choice in
            1)
                quick_deploy_structure
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            2)
                aggregate_project_context
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            3)
                print_section "Aggregate Pattern Context"
                read -p "$(echo -e ${CYAN}📌 Enter pattern name: ${NC})" pattern
                if [[ -n "$pattern" ]]; then
                    $PY_CMD -c "
import sys
sys.path.insert(0, '.')
exec(open('$PYTHON_SERVICE').read(), globals())
config = MotiaConfig.from_path('.')
aggregator = MarkdownAggregator(config)
aggregator.aggregate_pattern_context('$pattern')
"
                fi
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            4)
                print_section "Aggregate Step Context"
                read -p "$(echo -e ${CYAN}📁 Enter step path: ${NC})" step
                if [[ -n "$step" ]]; then
                    $PY_CMD -c "
import sys
sys.path.insert(0, '.')
exec(open('$PYTHON_SERVICE').read(), globals())
config = MotiaConfig.from_path('.')
aggregator = MarkdownAggregator(config)
aggregator.aggregate_step_context('$step')
"
                fi
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            5)
                quick_full_pipeline
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            6)
                print_section "Project Structure"
                tree -L 3 -I 'node_modules|venv|__pycache__|.git' 2>/dev/null || find . -maxdepth 3 -not -path '*/\.*' -not -path '*/node_modules/*' -not -path '*/venv/*' | head -50
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            7)
                launch_python_service
                read -p "$(echo -e ${YELLOW}\nPress Enter to continue...${NC})"
                ;;
            8)
                show_help
                ;;
            9)
                clear
                print_header
                echo -e "${GREEN}${BOLD}"
                echo "  👋 Thank you for using Motia Markdown Service!"
                echo "  🚀 Happy coding with Claude CLI!"
                echo -e "${NC}\n"
                exit 0
                ;;
            *)
                print_error "Invalid choice! Please select 1-9."
                sleep 2
                ;;
        esac
    done
}

# Trap для красивого виходу при Ctrl+C
trap 'echo -e "\n\n${YELLOW}⚠️  Interrupted by user. Goodbye!${NC}\n"; exit 130' INT

# Запуск
main "$@"
