#!/usr/bin/env bash
#
# DRAKON Research Pipeline - Perplexity Labs Integration
#
# Purpose: Orchestrate deep research on DRAKON ecosystem using Perplexity Labs API
# Author: Motia DRAKON Pipeline Module
# Version: 1.0
# Date: 2025-10-10
#
# Usage:
#   ./run_perplexity_lab.sh [command]
#
# Commands:
#   research     - Execute full research pipeline
#   status       - Check job status
#   process      - Process existing research results
#   validate     - Validate research against success criteria
#   help         - Show this help message

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CONFIG_FILE="${SCRIPT_DIR}/perplexity_config.json"
readonly PROMPT_FILE="${SCRIPT_DIR}/perplexity_prompt.txt"
readonly TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

# Output directories
readonly OUTPUT_DIR="${SCRIPT_DIR}/research_output"
readonly RAW_DIR="${OUTPUT_DIR}/raw"
readonly PROCESSED_DIR="${OUTPUT_DIR}/processed"
readonly KNOWLEDGE_DIR="${SCRIPT_DIR}/knowledge_base"
readonly SCHEMAS_DIR="${OUTPUT_DIR}/schemas"
readonly SAMPLES_DIR="${OUTPUT_DIR}/code_samples"
readonly LOGS_DIR="${SCRIPT_DIR}/logs"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly MAGENTA='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color
readonly BOLD='\033[1m'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${CYAN}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

log_error() {
    echo -e "${RED}❌${NC} $*" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}

log_step() {
    echo -e "${MAGENTA}▶${NC} ${BOLD}$*${NC}"
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

validate_environment() {
    log_step "Validating environment..."

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        log_error "jq is not installed. Please install it: sudo apt install jq"
        exit 1
    fi

    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        log_error "curl is not installed. Please install it: sudo apt install curl"
        exit 1
    fi

    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log_error "python3 is not installed"
        exit 1
    fi

    # Check for Perplexity API key
    if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
        log_error "PERPLEXITY_API_KEY environment variable is not set"
        log_info "Set it with: export PERPLEXITY_API_KEY='your-api-key'"
        exit 1
    fi

    # Check if config file exists
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_error "Config file not found: $CONFIG_FILE"
        exit 1
    fi

    # Check if prompt file exists
    if [[ ! -f "$PROMPT_FILE" ]]; then
        log_error "Prompt file not found: $PROMPT_FILE"
        exit 1
    fi

    log_success "Environment validation passed"
}

create_directory_structure() {
    log_step "Creating directory structure..."

    mkdir -p "$RAW_DIR" "$PROCESSED_DIR" "$KNOWLEDGE_DIR" \
             "$SCHEMAS_DIR" "$SAMPLES_DIR" "$LOGS_DIR"

    log_success "Directory structure created"
}

# ============================================================================
# PERPLEXITY API FUNCTIONS
# ============================================================================

submit_research_job() {
    log_step "Submitting research job to Perplexity Labs..."

    local endpoint model api_key temperature max_tokens
    endpoint=$(jq -r '.perplexity_api.endpoint' "$CONFIG_FILE")
    model=$(jq -r '.perplexity_api.model' "$CONFIG_FILE")
    api_key="$PERPLEXITY_API_KEY"
    temperature=$(jq -r '.request_parameters.temperature' "$CONFIG_FILE")
    max_tokens=$(jq -r '.request_parameters.max_tokens' "$CONFIG_FILE")

    # Read prompt
    local prompt
    prompt=$(<"$PROMPT_FILE")

    # Build request payload
    local request_payload
    request_payload=$(jq -n \
        --arg model "$model" \
        --arg prompt "$prompt" \
        --argjson temp "$temperature" \
        --argjson max_tok "$max_tokens" \
        '{
            model: $model,
            messages: [
                {
                    role: "system",
                    content: "You are a deep research assistant specializing in technical documentation, file formats, and software ecosystems. Provide comprehensive, well-cited research with code examples and references to official sources."
                },
                {
                    role: "user",
                    content: $prompt
                }
            ],
            temperature: $temp,
            max_tokens: $max_tok,
            return_citations: true,
            return_related_questions: true,
            search_recency_filter: "month"
        }')

    # Submit request
    local response_file="${RAW_DIR}/perplexity_response_${TIMESTAMP}.json"
    local http_code

    log_info "Sending request to Perplexity API..."
    log_info "Model: $model"
    log_info "Max tokens: $max_tokens"

    http_code=$(curl -s -w "%{http_code}" -o "$response_file" \
        -X POST "$endpoint" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "$request_payload")

    if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
        log_success "Research job submitted successfully (HTTP $http_code)"
        log_info "Raw response saved to: $response_file"
        echo "$response_file"
    else
        log_error "API request failed with HTTP $http_code"
        cat "$response_file"
        exit 1
    fi
}

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

process_research_results() {
    local response_file="$1"

    log_step "Processing research results..."

    # Check if response is valid JSON
    if ! jq empty "$response_file" 2>/dev/null; then
        log_error "Invalid JSON response"
        exit 1
    fi

    # Extract content
    local content
    content=$(jq -r '.choices[0].message.content // .message.content // .content // ""' "$response_file")

    if [[ -z "$content" ]]; then
        log_error "No content found in response"
        exit 1
    fi

    # Save processed markdown
    local processed_file="${PROCESSED_DIR}/DRAKON_RESEARCH_${TIMESTAMP}.md"
    cat > "$processed_file" <<EOF
# DRAKON Visual Programming Language - Deep Research Results

**Research Date:** $(date +%Y-%m-%d\ %H:%M:%S)
**Source:** Perplexity Labs (sonar-research)
**Generated by:** Motia DRAKON Pipeline Module

---

$content

---

## Research Metadata

**Raw Response:** ${response_file}
**Processed:** $(date +%Y-%m-%d\ %H:%M:%S)
**Pipeline Version:** 1.0

EOF

    log_success "Processed results saved to: $processed_file"

    # Extract citations if available
    local citations
    citations=$(jq -r '.citations // []' "$response_file")
    if [[ "$citations" != "[]" ]]; then
        local citations_file="${OUTPUT_DIR}/citations.json"
        echo "$citations" | jq '.' > "$citations_file"
        log_success "Citations extracted to: $citations_file"
    fi

    # Extract structured data
    extract_structured_data "$processed_file"

    echo "$processed_file"
}

extract_structured_data() {
    local markdown_file="$1"

    log_step "Extracting structured data from research..."

    # Python script to extract schemas, code samples, and icon types
    python3 <<'PYTHON_SCRIPT'
import re
import json
import sys
from pathlib import Path

def extract_sql_schemas(content):
    """Extract SQL CREATE TABLE statements"""
    sql_pattern = r'```sql\n(CREATE TABLE.*?)\n```'
    schemas = re.findall(sql_pattern, content, re.DOTALL | re.IGNORECASE)
    return schemas

def extract_json_schemas(content):
    """Extract JSON schemas and structures"""
    json_pattern = r'```json\n(\{.*?\})\n```'
    schemas = []
    for match in re.findall(json_pattern, content, re.DOTALL):
        try:
            schemas.append(json.loads(match))
        except:
            pass
    return schemas

def extract_code_samples(content):
    """Extract code samples (Python, JavaScript, etc.)"""
    code_pattern = r'```(python|javascript|typescript|js|ts|py)\n(.*?)\n```'
    samples = {}
    for lang, code in re.findall(code_pattern, content, re.DOTALL):
        if lang not in samples:
            samples[lang] = []
        samples[lang].append(code)
    return samples

def extract_icon_types(content):
    """Extract DRAKON icon type information"""
    icon_pattern = r'(?:icon.*?type|type.*?identifier).*?[:=]\s*["\']?(\w+)["\']?'
    icons = list(set(re.findall(icon_pattern, content, re.IGNORECASE)))
    return icons

# Read markdown
markdown_file = sys.argv[1]
content = Path(markdown_file).read_text()

# Extract data
sql_schemas = extract_sql_schemas(content)
json_schemas = extract_json_schemas(content)
code_samples = extract_code_samples(content)
icon_types = extract_icon_types(content)

# Save results
output_dir = Path(markdown_file).parent.parent

if sql_schemas:
    schemas_dir = output_dir / 'schemas'
    schemas_dir.mkdir(exist_ok=True)
    (schemas_dir / 'drn_sql_schema.sql').write_text('\n\n'.join(sql_schemas))
    print(f"✅ Extracted {len(sql_schemas)} SQL schemas")

if json_schemas:
    schemas_dir = output_dir / 'schemas'
    schemas_dir.mkdir(exist_ok=True)
    (schemas_dir / 'json_schemas.json').write_text(json.dumps(json_schemas, indent=2))
    print(f"✅ Extracted {len(json_schemas)} JSON schemas")

if code_samples:
    samples_dir = output_dir / 'code_samples'
    samples_dir.mkdir(exist_ok=True)
    for lang, samples in code_samples.items():
        for i, sample in enumerate(samples):
            ext = 'py' if lang == 'python' else lang.replace('typescript', 'ts').replace('javascript', 'js')
            (samples_dir / f'sample_{i+1}.{ext}').write_text(sample)
    print(f"✅ Extracted {sum(len(s) for s in code_samples.values())} code samples")

if icon_types:
    kb_dir = output_dir.parent / 'knowledge_base'
    kb_dir.mkdir(exist_ok=True)
    icon_data = {
        'icon_types': icon_types,
        'extracted_from': str(markdown_file),
        'count': len(icon_types)
    }
    (kb_dir / 'drakon_icon_types.json').write_text(json.dumps(icon_data, indent=2))
    print(f"✅ Extracted {len(icon_types)} icon types")

PYTHON_SCRIPT

    log_success "Structured data extraction complete"
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

validate_research_quality() {
    local processed_file="$1"

    log_step "Validating research quality against success criteria..."

    local required_sections min_length
    required_sections=$(jq -r '.success_criteria.required_sections[]' "$CONFIG_FILE")

    local missing_sections=()
    while IFS= read -r section; do
        if ! grep -q "$section" "$processed_file"; then
            missing_sections+=("$section")
        fi
    done <<< "$required_sections"

    if [[ ${#missing_sections[@]} -gt 0 ]]; then
        log_warning "Missing required sections:"
        printf '%s\n' "${missing_sections[@]}" | sed 's/^/  - /'
    else
        log_success "All required sections present"
    fi

    # Check file size (should be substantial)
    local file_size
    file_size=$(wc -c < "$processed_file")
    if [[ $file_size -lt 10000 ]]; then
        log_warning "Research output seems small ($file_size bytes)"
    else
        log_success "Research output size: $file_size bytes"
    fi

    # Check for citations
    if [[ -f "${OUTPUT_DIR}/citations.json" ]]; then
        local citation_count
        citation_count=$(jq 'length' "${OUTPUT_DIR}/citations.json")
        log_success "Citations found: $citation_count"
    else
        log_warning "No citations file found"
    fi

    # Check extracted artifacts
    local schemas_count samples_count
    schemas_count=$(find "$SCHEMAS_DIR" -type f 2>/dev/null | wc -l)
    samples_count=$(find "$SAMPLES_DIR" -type f 2>/dev/null | wc -l)

    log_info "Extracted artifacts:"
    log_info "  - SQL/JSON schemas: $schemas_count"
    log_info "  - Code samples: $samples_count"

    log_success "Quality validation complete"
}

# ============================================================================
# MAIN PIPELINE
# ============================================================================

run_full_pipeline() {
    log_step "Starting DRAKON Deep Research Pipeline"
    echo

    # Step 1: Validate environment
    validate_environment
    echo

    # Step 2: Create directory structure
    create_directory_structure
    echo

    # Step 3: Submit research job
    local response_file
    response_file=$(submit_research_job)
    echo

    # Step 4: Process results
    local processed_file
    processed_file=$(process_research_results "$response_file")
    echo

    # Step 5: Validate quality
    validate_research_quality "$processed_file"
    echo

    # Step 6: Generate summary report
    generate_summary_report "$response_file" "$processed_file"
    echo

    log_success "Pipeline completed successfully!"
    log_info "Results available at: $OUTPUT_DIR"
}

generate_summary_report() {
    local response_file="$1"
    local processed_file="$2"

    log_step "Generating summary report..."

    local summary_file="${SCRIPT_DIR}/RESEARCH_SUMMARY.md"

    cat > "$summary_file" <<EOF
# DRAKON Research Pipeline - Summary Report

**Execution Date:** $(date +%Y-%m-%d\ %H:%M:%S)
**Pipeline Version:** 1.0

## Research Status

✅ Research completed successfully

## Output Files

### Primary Results
- **Processed Markdown:** \`${processed_file#$SCRIPT_DIR/}\`
- **Raw API Response:** \`${response_file#$SCRIPT_DIR/}\`

### Extracted Artifacts
- **SQL Schemas:** \`research_output/schemas/*.sql\`
- **JSON Schemas:** \`research_output/schemas/*.json\`
- **Code Samples:** \`research_output/code_samples/*.{py,js,ts}\`
- **Icon Types:** \`knowledge_base/drakon_icon_types.json\`

### Citations
- **Citations Index:** \`research_output/citations.json\`

## Next Steps

1. **Review research results:**
   \`\`\`bash
   cat "$processed_file"
   \`\`\`

2. **Update DRAKON converters** based on findings:
   - Review \`research_output/schemas/drn_sql_schema.sql\`
   - Check \`research_output/schemas/json_schemas.json\`
   - Compare with current implementation in \`../converter/\`

3. **Validate compatibility:**
   \`\`\`bash
   ./run_perplexity_lab.sh validate
   \`\`\`

4. **Update knowledge base:**
   - Merge findings into \`../converter/README.md\`
   - Update icon type mappings in converter code
   - Add validation rules based on discovered specifications

## Integration with Motia

To integrate research findings into Motia workflow:

\`\`\`bash
# From project root
./scripts/unified-motia-workflow.sh drakon <step-name>
\`\`\`

Converters now have access to:
- Complete .drn SQLite schema
- Full JSON format specification
- All DRAKON icon types
- Validation rules from official tools

---

**Generated by:** Motia DRAKON Pipeline Module
**Config:** \`perplexity_config.json\`
**Logs:** \`logs/perplexity_research_${TIMESTAMP}.log\`
EOF

    log_success "Summary report saved to: $summary_file"
}

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

cmd_research() {
    run_full_pipeline
}

cmd_status() {
    log_info "Checking research pipeline status..."
    echo

    if [[ -d "$OUTPUT_DIR" ]]; then
        log_info "Output directory: $OUTPUT_DIR"

        local research_count
        research_count=$(find "$PROCESSED_DIR" -name "DRAKON_RESEARCH_*.md" 2>/dev/null | wc -l)
        log_info "Research outputs: $research_count"

        if [[ $research_count -gt 0 ]]; then
            log_info "Latest research:"
            find "$PROCESSED_DIR" -name "DRAKON_RESEARCH_*.md" -exec ls -lh {} \; | tail -1
        fi

        local schemas_count samples_count
        schemas_count=$(find "$SCHEMAS_DIR" -type f 2>/dev/null | wc -l)
        samples_count=$(find "$SAMPLES_DIR" -type f 2>/dev/null | wc -l)

        log_info "Extracted schemas: $schemas_count"
        log_info "Code samples: $samples_count"
    else
        log_warning "No research outputs found. Run: ./run_perplexity_lab.sh research"
    fi
}

cmd_process() {
    log_info "Processing existing research results..."

    local latest_raw
    latest_raw=$(find "$RAW_DIR" -name "perplexity_response_*.json" -type f 2>/dev/null | sort | tail -1)

    if [[ -z "$latest_raw" ]]; then
        log_error "No raw research files found in $RAW_DIR"
        exit 1
    fi

    log_info "Processing: $latest_raw"
    local processed_file
    processed_file=$(process_research_results "$latest_raw")
    validate_research_quality "$processed_file"
}

cmd_validate() {
    log_info "Validating latest research..."

    local latest_processed
    latest_processed=$(find "$PROCESSED_DIR" -name "DRAKON_RESEARCH_*.md" -type f 2>/dev/null | sort | tail -1)

    if [[ -z "$latest_processed" ]]; then
        log_error "No processed research files found"
        exit 1
    fi

    validate_research_quality "$latest_processed"
}

cmd_help() {
    cat <<EOF
${BOLD}DRAKON Research Pipeline - Perplexity Labs Integration${NC}

${BOLD}USAGE:${NC}
  ./run_perplexity_lab.sh [command]

${BOLD}COMMANDS:${NC}
  ${GREEN}research${NC}     Execute full research pipeline (submit + process + validate)
  ${GREEN}status${NC}       Check research pipeline status and outputs
  ${GREEN}process${NC}      Reprocess existing raw research results
  ${GREEN}validate${NC}     Validate latest research against quality criteria
  ${GREEN}help${NC}         Show this help message

${BOLD}EXAMPLES:${NC}
  # Run full research pipeline
  export PERPLEXITY_API_KEY='your-api-key'
  ./run_perplexity_lab.sh research

  # Check status
  ./run_perplexity_lab.sh status

  # Reprocess existing results
  ./run_perplexity_lab.sh process

${BOLD}PREREQUISITES:${NC}
  - PERPLEXITY_API_KEY environment variable set
  - jq, curl, python3 installed
  - perplexity_config.json and perplexity_prompt.txt present

${BOLD}OUTPUT STRUCTURE:${NC}
  research_output/
  ├── raw/                    # Raw API responses (JSON)
  ├── processed/              # Processed markdown research
  ├── schemas/                # Extracted SQL/JSON schemas
  ├── code_samples/           # Extracted code snippets
  └── citations.json          # Source citations

  knowledge_base/
  └── drakon_icon_types.json  # DRAKON icon reference

  logs/
  └── perplexity_research_*.log

${BOLD}CONFIGURATION:${NC}
  Edit perplexity_config.json to customize:
  - API parameters (model, temperature, max_tokens)
  - Processing pipeline steps
  - Success criteria
  - Output paths

${BOLD}MORE INFO:${NC}
  See: perplexity_config.json
       perplexity_prompt.txt
       ../converter/README.md

EOF
}

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

main() {
    local command="${1:-help}"

    case "$command" in
        research)
            cmd_research
            ;;
        status)
            cmd_status
            ;;
        process)
            cmd_process
            ;;
        validate)
            cmd_validate
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            log_error "Unknown command: $command"
            echo
            cmd_help
            exit 1
            ;;
    esac
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
