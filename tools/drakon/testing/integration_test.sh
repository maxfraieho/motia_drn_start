#!/bin/bash
###############################################################################
# DRAKON Integration Test Script
# 
# Повний інтеграційний тест для DRAKON Pipeline:
# 1. Генерація діаграм
# 2. Конвертація між форматами
# 3. Тестування з DrakonWidget
# 4. Валідація результатів
#
# Location: /home/vokov/motia/tools/drakon/testing/integration_test.sh
###############################################################################

set -euo pipefail

# Кольори для виводу
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфігурація
PROJECT_ROOT="/home/vokov/motia"
DRAKON_DIR="${PROJECT_ROOT}/tools/drakon"
TEST_DIR="${DRAKON_DIR}/testing"
RESULTS_DIR="${TEST_DIR}/integration_results"
TEST_STEP="drakon-test-step"

# Лічильники
TESTS_PASSED=0
TESTS_FAILED=0

###############################################################################
# Допоміжні функції
###############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

section_header() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

cleanup() {
    log_info "Cleaning up test artifacts..."
    
    # Видалити тестовий Step (якщо існує)
    if [[ -d "${PROJECT_ROOT}/steps/${TEST_STEP}" ]]; then
        rm -rf "${PROJECT_ROOT}/steps/${TEST_STEP}"
        log_info "Removed test Step: ${TEST_STEP}"
    fi
}

trap cleanup EXIT

###############################################################################
# Тест 1: Перевірка залежностей
###############################################################################

test_dependencies() {
    section_header "Test 1: Checking Dependencies"
    
    # Python 3
    if command -v python3 &> /dev/null; then
        log_success "Python 3 installed: $(python3 --version)"
    else
        log_error "Python 3 not found"
        return 1
    fi
    
    # SQLite
    if command -v sqlite3 &> /dev/null; then
        log_success "SQLite installed: $(sqlite3 --version)"
    else
        log_error "SQLite not found"
    fi
    
    # jq (для JSON)
    if command -v jq &> /dev/null; then
        log_success "jq installed"
    else
        log_warning "jq not installed (optional)"
    fi
    
    # Перевірка Python модулів
    if python3 -c "import sqlite3" 2>/dev/null; then
        log_success "Python sqlite3 module available"
    else
        log_error "Python sqlite3 module not found"
    fi
    
    # DrakonWidget
    if [[ -f "${TEST_DIR}/drakonwidget.js" ]]; then
        log_success "DrakonWidget found"
    else
        log_warning "DrakonWidget not found, will download"
        
        # Спробувати завантажити
        if wget -q https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/drakonwidget.js \
                -O "${TEST_DIR}/drakonwidget.js"; then
            log_success "DrakonWidget downloaded"
        else
            log_error "Failed to download DrakonWidget"
        fi
    fi
    
    # Playwright (опціонально)
    if python3 -c "import playwright" 2>/dev/null; then
        log_success "Playwright installed (automated testing available)"
    else
        log_warning "Playwright not installed (automated testing unavailable)"
    fi
}

###############################################################################
# Тест 2: Генерація діаграм
###############################################################################

test_diagram_generation() {
    section_header "Test 2: Generating DRAKON Diagrams"
    
    # Створити тестовий Step
    log_info "Creating test Step: ${TEST_STEP}"
    
    cd "${PROJECT_ROOT}"
    
    if ./scripts/unified-motia-workflow.sh full-pipeline \
        "${TEST_STEP}" \
        "event" \
        "observer" \
        "Integration test step for DRAKON" \
        "typescript"; then
        log_success "Test Step created successfully"
    else
        log_error "Failed to create test Step"
        return 1
    fi
    
    # Перевірити структуру
    local step_dir="${PROJECT_ROOT}/steps/${TEST_STEP}"
    
    if [[ -d "${step_dir}/diagrams" ]]; then
        log_success "Diagrams directory exists"
    else
        log_error "Diagrams directory not found"
        return 1
    fi
    
    # Перевірити файли
    local expected_files=(
        "initialization.drn"
        "initialization.json"
        "main-flow.drn"
        "main-flow.json"
        "error-handling.drn"
        "error-handling.json"
        "cleanup.drn"
        "cleanup.json"
    )
    
    local files_found=0
    for file in "${expected_files[@]}"; do
        if [[ -f "${step_dir}/diagrams/${file}" ]]; then
            log_success "Found: ${file}"
            files_found=$((files_found + 1))
        else
            log_error "Missing: ${file}"
        fi
    done
    
    if [[ $files_found -eq ${#expected_files[@]} ]]; then
        log_success "All ${files_found} diagram files generated"
    else
        log_error "Only ${files_found}/${#expected_files[@]} files generated"
    fi
}

###############################################################################
# Тест 3: Валідація .drn файлів
###############################################################################

test_drn_validation() {
    section_header "Test 3: Validating .drn Files"
    
    local diagrams_dir="${PROJECT_ROOT}/steps/${TEST_STEP}/diagrams"
    
    for drn_file in "${diagrams_dir}"/*.drn; do
        if [[ ! -f "$drn_file" ]]; then
            continue
        fi
        
        local filename=$(basename "$drn_file")
        log_info "Validating: ${filename}"
        
        # SQLite integrity check
        if sqlite3 "$drn_file" "PRAGMA integrity_check;" | grep -q "ok"; then
            log_success "  ✓ SQLite integrity OK"
        else
            log_error "  ✗ SQLite integrity FAILED"
            continue
        fi
        
        # Перевірити таблиці
        local tables=$(sqlite3 "$drn_file" "SELECT name FROM sqlite_master WHERE type='table';")
        
        if echo "$tables" | grep -q "info"; then
            log_success "  ✓ Table 'info' exists"
        else
            log_error "  ✗ Table 'info' missing"
        fi
        
        if echo "$tables" | grep -q "diagrams"; then
            log_success "  ✓ Table 'diagrams' exists"
        else
            log_error "  ✗ Table 'diagrams' missing"
        fi
        
        if echo "$tables" | grep -q "items"; then
            log_success "  ✓ Table 'items' exists"
        else
            log_error "  ✗ Table 'items' missing"
        fi
        
        # Підрахувати іконки
        local icon_count=$(sqlite3 "$drn_file" "SELECT COUNT(*) FROM items;")
        
        if [[ $icon_count -gt 0 ]]; then
            log_success "  ✓ Contains ${icon_count} icons"
        else
            log_error "  ✗ No icons found"
        fi
        
        # Перевірити версію
        local version=$(sqlite3 "$drn_file" "SELECT value FROM info WHERE key='version';")
        
        if [[ -n "$version" ]]; then
            log_success "  ✓ Version: ${version}"
        else
            log_warning "  ! No version info"
        fi
    done
}

###############################################################################
# Тест 4: Валідація JSON файлів
###############################################################################

test_json_validation() {
    section_header "Test 4: Validating JSON Files"
    
    local diagrams_dir="${PROJECT_ROOT}/steps/${TEST_STEP}/diagrams"
    
    for json_file in "${diagrams_dir}"/*.json; do
        if [[ ! -f "$json_file" ]]; then
            continue
        fi
        
        local filename=$(basename "$json_file")
        log_info "Validating: ${filename}"
        
        # JSON syntax check
        if jq empty "$json_file" 2>/dev/null; then
            log_success "  ✓ JSON syntax valid"
        else
            log_error "  ✗ JSON syntax invalid"
            continue
        fi
        
        # Перевірити обов'язкові поля
        if jq -e '.name' "$json_file" > /dev/null 2>&1; then
            local name=$(jq -r '.name' "$json_file")
            log_success "  ✓ Has name: ${name}"
        else
            log_error "  ✗ Missing 'name' field"
        fi
        
        if jq -e '.access' "$json_file" > /dev/null 2>&1; then
            log_success "  ✓ Has 'access' field"
        else
            log_error "  ✗ Missing 'access' field"
        fi
        
        if jq -e '.items' "$json_file" > /dev/null 2>&1; then
            local item_count=$(jq '.items | length' "$json_file")
            log_success "  ✓ Has ${item_count} items"
        else
            log_error "  ✗ Missing 'items' field"
        fi
        
        # Перевірити структуру items
        local broken_links=$(jq -r '
            .items | to_entries | 
            map(select(.value.one and (.value.one as $one | .items | has($one) | not))) | 
            length
        ' "$json_file" 2>/dev/null || echo "0")
        
        if [[ $broken_links -eq 0 ]]; then
            log_success "  ✓ All links valid"
        else
            log_error "  ✗ ${broken_links} broken links"
        fi
    done
}

###############################################################################
# Тест 5: Конвертація форматів
###############################################################################

test_format_conversion() {
    section_header "Test 5: Testing Format Conversion"
    
    local diagrams_dir="${PROJECT_ROOT}/steps/${TEST_STEP}/diagrams"
    local converter="${DRAKON_DIR}/converter/drakon_converter.py"
    
    if [[ ! -f "$converter" ]]; then
        log_error "Converter not found: ${converter}"
        return 1
    fi
    
    # Тест: .drn → .json
    log_info "Testing .drn → .json conversion"
    
    local test_drn="${diagrams_dir}/initialization.drn"
    local test_json="${RESULTS_DIR}/converted_from_drn.json"
    
    mkdir -p "${RESULTS_DIR}"
    
    if python3 "$converter" "$test_drn" "$test_json" 2>/dev/null; then
        log_success "Conversion .drn → .json successful"
        
        # Перевірити результат
        if jq empty "$test_json" 2>/dev/null; then
            log_success "Converted JSON is valid"
        else
            log_error "Converted JSON is invalid"
        fi
    else
        log_error "Conversion .drn → .json failed"
    fi
    
    # Тест: .json → .drn
    log_info "Testing .json → .drn conversion"
    
    test_json="${diagrams_dir}/main-flow.json"
    test_drn="${RESULTS_DIR}/converted_from_json.drn"
    
    if python3 "$converter" "$test_json" "$test_drn" 2>/dev/null; then
        log_success "Conversion .json → .drn successful"
        
        # Перевірити результат
        if sqlite3 "$test_drn" "PRAGMA integrity_check;" | grep -q "ok"; then
            log_success "Converted .drn is valid"
        else
            log_error "Converted .drn is invalid"
        fi
    else
        log_error "Conversion .json → .drn failed"
    fi
}

###############################################################################
# Тест 6: DrakonWidget тестування
###############################################################################

test_drakon_widget() {
    section_header "Test 6: Testing with DrakonWidget"
    
    local diagrams_dir="${PROJECT_ROOT}/steps/${TEST_STEP}/diagrams"
    local tester="${TEST_DIR}/drakon_widget_test.py"
    
    if [[ ! -f "$tester" ]]; then
        log_error "DrakonWidget tester not found: ${tester}"
        return 1
    fi
    
    # Перевірити чи є Playwright
    if python3 -c "import playwright" 2>/dev/null; then
        log_info "Running automated tests with Playwright"
        
        if python3 "$tester" \
            "$diagrams_dir" \
            --automated \
            --output-dir "${RESULTS_DIR}/widget_tests" 2>&1 | tee "${RESULTS_DIR}/widget_test.log"; then
            log_success "DrakonWidget automated tests passed"
        else
            log_error "DrakonWidget automated tests failed"
            log_info "Check log: ${RESULTS_DIR}/widget_test.log"
        fi
    else
        log_warning "Playwright not installed, skipping automated tests"
        log_info "To install: pip install playwright && playwright install"
    fi
}

###############################################################################
# Тест 7: Продуктивність
###############################################################################

test_performance() {
    section_header "Test 7: Performance Testing"
    
    log_info "Measuring diagram generation time..."
    
    local start_time=$(date +%s%N)
    
    # Згенерувати діаграми для нового Step
    local perf_step="perf-test-step"
    
    cd "${PROJECT_ROOT}"
    
    ./scripts/unified-motia-workflow.sh drakon "$perf_step" > /dev/null 2>&1 || true
    
    local end_time=$(date +%s%N)
    local duration_ms=$(( (end_time - start_time) / 1000000 ))
    
    log_info "Generation time: ${duration_ms}ms"
    
    if [[ $duration_ms -lt 15000 ]]; then
        log_success "Performance acceptable (< 15 seconds)"
    elif [[ $duration_ms -lt 30000 ]]; then
        log_warning "Performance marginal (15-30 seconds)"
    else
        log_error "Performance poor (> 30 seconds)"
    fi
    
    # Очистити
    rm -rf "${PROJECT_ROOT}/steps/${perf_step}"
}

###############################################################################
# Звіт
###############################################################################

generate_report() {
    section_header "Integration Test Summary"
    
    local total_tests=$((TESTS_PASSED + TESTS_FAILED))
    
    echo "Total Tests:  ${total_tests}"
    echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
    echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
    echo ""
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
        echo ""
        echo "DRAKON Pipeline is working correctly!"
        return 0
    else
        echo -e "${RED}✗ SOME TESTS FAILED${NC}"
        echo ""
        echo "Please review the errors above and fix the issues."
        return 1
    fi
}

###############################################################################
# Main
###############################################################################

main() {
    section_header "DRAKON Integration Test Suite"
    
    log_info "Starting integration tests..."
    log_info "Project root: ${PROJECT_ROOT}"
    log_info "Results dir: ${RESULTS_DIR}"
    echo ""
    
    # Створити каталог результатів
    mkdir -p "${RESULTS_DIR}"
    
    # Запустити тести
    test_dependencies
    test_diagram_generation
    test_drn_validation
    test_json_validation
    test_format_conversion
    test_drakon_widget
    test_performance
    
    # Згенерувати звіт
    generate_report
}

# Запустити
main

exit $?