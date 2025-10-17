#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PUBLIC_DIR="$SCRIPT_DIR/public"
STEPS_DIR="$SCRIPT_DIR/../../motia-output/steps"
OUTPUT_FILE="$PUBLIC_DIR/diagrams.json"

echo "🔍 Пошук .json файлів діаграм в $STEPS_DIR..."

# Використовуємо find для пошуку файлів і jq для створення JSON
find "$STEPS_DIR" -type f -name "*.json" | jq -R -s '
split("\n") |
  map(select(length > 0)) |
  map(
    . as $path |
    ($path | split("/")[-3:]) as $parts |
    {
      step: $parts[0],
      name: ($parts[2] | sub(".json$"; ""))
      path: ("/diagrams/" + $parts[0] + "/" + $parts[2])
    }
  )
' > "$OUTPUT_FILE"

echo "✅ Створено індексний файл: $OUTPUT_FILE"
