#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PUBLIC_DIR="$SCRIPT_DIR/public"
DIAGRAMS_DIR="$PUBLIC_DIR/diagrams"
OUTPUT_FILE="$PUBLIC_DIR/diagrams.json"

echo "🔍 Пошук .json файлів діаграм в $DIAGRAMS_DIR..."

# Створюємо директорію якщо не існує
mkdir -p "$DIAGRAMS_DIR"

# Використовуємо find для пошуку файлів і jq для створення JSON
find "$DIAGRAMS_DIR" -type f -name "*.json" -maxdepth 1 | jq -R -s '
split("\n") |
  map(select(length > 0)) |
  map(
    . as $path |
    ($path | split("/")[-1]) as $filename |
    ($filename | sub(".json$"; "")) as $name |
    # Визначаємо step з назви файлу (prefix до першого дефісу)
    ($name | split("-")[0]) as $step |
    {
      step: $step,
      name: ($name | gsub("-"; " ") | . as $x | ($x[0:1] | ascii_upcase) + $x[1:]),
      path: ("diagrams/" + $filename)
    }
  )
' > "$OUTPUT_FILE"

echo "✅ Створено індексний файл: $OUTPUT_FILE"
echo "📁 Знайдено діаграм: $(find "$DIAGRAMS_DIR" -type f -name "*.json" -maxdepth 1 | wc -l)"
