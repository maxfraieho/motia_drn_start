#!/bin/bash
###############################################################################
# DRAKON Testing Setup Script
# 
# Автоматично встановлює всі залежності для тестування DRAKON діаграм
#
# Location: /home/vokov/motia/tools/drakon/testing/setup.sh
###############################################################################

set -euo pipefail

# Кольори
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

section() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

###############################################################################
# Головна функція
###############################################################################

main() {
    section "DRAKON Testing Setup"
    
    log_info "This script will install dependencies for DRAKON diagram testing"
    echo ""
    
    # Перевірка Python
    section "Step 1/5: Checking Python"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        log_success "Python found: ${PYTHON_VERSION}"
    else
        log_error "Python 3 not found!"
        log_info "Install Python 3: sudo apt install python3 python3-pip"
        exit 1
    fi
    
    # Перевірка pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3 found"
    else
        log_error "pip3 not found!"
        log_info "Install pip3: sudo apt install python3-pip"
        exit 1
    fi
    
    # Завантаження DrakonWidget
    section "Step 2/5: Downloading DrakonWidget"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    WIDGET_PATH="${SCRIPT_DIR}/drakonwidget.js"
    
    if [[ -f "$WIDGET_PATH" ]]; then
        log_warning "DrakonWidget already exists, skipping download"
    else
        log_info "Downloading DrakonWidget from GitHub..."
        
        if wget -q --show-progress \
            https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js \
            -O "$WIDGET_PATH"; then
            log_success "DrakonWidget downloaded successfully"
        else
            log_error "Failed to download DrakonWidget"
            log_info "You can download it manually from:"
            log_info "https://github.com/stepan-mitkin/drakonwidget"
            exit 1
        fi
    fi
    
    # Встановлення Playwright (опціонально)
    section "Step 3/5: Installing Playwright (Optional)"
    
    echo "Playwright enables automated browser testing."
    echo "Without it, you can only do manual testing."
    echo ""
    read -p "Install Playwright? [y/N]: " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Installing Playwright..."
        
        if pip3 install playwright --user; then
            log_success "Playwright installed"
            
            log_info "Installing Chromium browser..."
            if python3 -m playwright install chromium; then
                log_success "Chromium installed"
            else
                log_warning "Failed to install Chromium"
            fi
        else
            log_warning "Failed to install Playwright"
            log_info "You can install it later with:"
            log_info "  pip3 install playwright"
            log_info "  python3 -m playwright install chromium"
        fi
    else
        log_info "Skipping Playwright installation"
        log_info "Manual testing will still work"
    fi
    
    # Встановлення додаткових інструментів
    section "Step 4/5: Installing Additional Tools"
    
    # jq для JSON
    if command -v jq &> /dev/null; then
        log_success "jq already installed"
    else
        log_info "Installing jq (JSON processor)..."
        
        if sudo apt-get update && sudo apt-get install -y jq 2>/dev/null; then
            log_success "jq installed"
        else
            log_warning "Could not install jq automatically"
            log_info "Install manually: sudo apt install jq"
        fi
    fi
    
    # SQLite
    if command -v sqlite3 &> /dev/null; then
        log_success "SQLite already installed"
    else
        log_info "Installing SQLite..."
        
        if sudo apt-get install -y sqlite3 2>/dev/null; then
            log_success "SQLite installed"
        else
            log_warning "Could not install SQLite automatically"
            log_info "Install manually: sudo apt install sqlite3"
        fi
    fi
    
    # Зробити скрипти виконуваними
    section "Step 5/5: Making Scripts Executable"
    
    chmod +x "${SCRIPT_DIR}/drakon_widget_test.py" 2>/dev/null || true
    log_success "drakon_widget_test.py is executable"
    
    chmod +x "${SCRIPT_DIR}/integration_test.sh" 2>/dev/null || true
    log_success "integration_test.sh is executable"
    
    chmod +x "${SCRIPT_DIR}/setup.sh" 2>/dev/null || true
    log_success "setup.sh is executable"
    
    # Фінальний звіт
    section "Setup Complete!"
    
    echo "✓ DrakonWidget downloaded"
    echo "✓ Scripts configured"
    echo ""
    
    if python3 -c "import playwright" 2>/dev/null; then
        echo "✓ Playwright installed - Automated testing available"
    else
        echo "○ Playwright not installed - Manual testing only"
    fi
    
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Test a single diagram:"
    echo "   cd ${SCRIPT_DIR}"
    echo "   python3 drakon_widget_test.py /path/to/diagrams"
    echo ""
    echo "2. Run automated tests (if Playwright installed):"
    echo "   python3 drakon_widget_test.py /path/to/diagrams --automated"
    echo ""
    echo "3. Run full integration test:"
    echo "   ./integration_test.sh"
    echo ""
    echo "For more info, see README.md"
    echo ""
}

main "$@"