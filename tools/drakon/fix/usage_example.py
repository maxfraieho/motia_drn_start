
# Приклад використання інструментів для виправлення ДРАКОН конвертера

from drakon_tools import DrakonValidator, DrakonCorrector, DrakonAnalyzer
import json
import os

# 1. ВАЛІДАЦІЯ ІСНУЮЧОГО ФАЙЛУ
def validate_drakon_file(file_path):
    """Валідація одного файлу ДРАКОН діаграми"""
    validator = DrakonValidator()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            diagram = json.load(f)

        is_valid = validator.validate(diagram)

        print(f"Файл: {file_path}")
        print(f"Статус: {'✅ Валідний' if is_valid else '❌ Помилки знайдено'}")
        print(validator.get_report())

        return is_valid

    except Exception as e:
        print(f"Помилка читання файлу {file_path}: {e}")
        return False

# 2. АВТОМАТИЧНЕ ВИПРАВЛЕННЯ ФАЙЛУ
def fix_drakon_file(input_path, output_path=None):
    """Автоматично виправляє ДРАКОН діаграму"""
    corrector = DrakonCorrector()

    if output_path is None:
        output_path = input_path.replace('.json', '_fixed.json')

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            diagram = json.load(f)

        corrected = corrector.correct_diagram(diagram)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(corrected, f, ensure_ascii=False, indent=2)

        print(f"Файл виправлено: {input_path} -> {output_path}")
        print(corrector.get_corrections_report())

        return output_path

    except Exception as e:
        print(f"Помилка виправлення файлу: {e}")
        return None

# 3. МАСОВА ОБРОБКА ДИРЕКТОРІЇ
def process_directory(directory_path):
    """Обробляє всі JSON файли в директорії"""
    analyzer = DrakonAnalyzer()

    results = analyzer.analyze_directory(directory_path)

    print("=== РЕЗУЛЬТАТИ АНАЛІЗУ ===")
    valid_count = 0

    for result in results:
        if result.get('is_valid_drakon'):
            print(f"✅ {result['file_path']}")
            valid_count += 1
        else:
            print(f"❌ {result['file_path']}")

            # Автоматично виправляємо невалідні файли
            if result.get('valid_json') and not result.get('is_valid_drakon'):
                fixed_path = fix_drakon_file(result['file_path'])
                if fixed_path:
                    print(f"   → Створено виправлену версію: {fixed_path}")

    print(f"\nВсього файлів: {len(results)}, валідних: {valid_count}")

# 4. ПОРІВНЯННЯ З ЕТАЛОННОЮ ДІАГРАМОЮ
def compare_with_reference(your_file, reference_file):
    """Порівнює вашу діаграму з еталонною"""
    try:
        with open(your_file, 'r', encoding='utf-8') as f:
            your_diagram = json.load(f)

        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_diagram = json.load(f)

        analyzer = DrakonAnalyzer()
        comparison = analyzer.compare_diagrams(your_diagram, reference_diagram)

        print("=== ПОРІВНЯННЯ ДІАГРАМ ===")
        print(f"Схожість: {comparison['similarity_score']*100:.1f}%")

        if comparison['structure_differences']:
            print("\nВідмінності в структурі:")
            for diff in comparison['structure_differences']:
                print(f"- {diff['field']}: ваше='{diff['value1']}', еталон='{diff['value2']}'")

        if comparison['missing_in_first']:
            print(f"\nВідсутні поля: {comparison['missing_in_first']}")

    except Exception as e:
        print(f"Помилка порівняння: {e}")

# 5. ПРИКЛАД ВИКОРИСТАННЯ
if __name__ == "__main__":
    # Шлях до вашої директорії з діаграмами
    DIAGRAMS_PATH = "/home/vokov/motia/motia-output/steps/config-service/diagrams-corrected"

    print("=== ОБРОБКА ДРАКОН ДІАГРАМ ===")

    # Обробка всіх файлів у директорії
    if os.path.exists(DIAGRAMS_PATH):
        process_directory(DIAGRAMS_PATH)
    else:
        print(f"Директорія не знайдена: {DIAGRAMS_PATH}")
        print("Створіть тестові файли для перевірки")
