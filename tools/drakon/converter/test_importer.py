#!/usr/bin/env python3
"""
Швидкий тест DRAKON імпортера

Перевірка базової функціональності імпортера з валідацією та автокорекцією.

Використання:
    python3 test_importer.py
"""

import sys
import json
from pathlib import Path

# Імпорт імпортера
from drakon_json_importer import DrakonJSONImporter


def create_test_diagrams():
    """Створює тестові діаграми (валідну та невалідну)"""
    test_dir = Path("./test_diagrams")
    test_dir.mkdir(exist_ok=True)

    # 1. Валідна діаграма
    valid_diagram = {
        "name": "Valid Test Diagram",
        "access": "write",
        "items": {
            "1": {"type": "branch", "branchId": 0, "one": "2"},
            "2": {"type": "action", "content": "Initialize", "one": "3"},
            "3": {"type": "question", "content": "Check status?", "one": "4", "two": "5"},
            "4": {"type": "action", "content": "Process success", "one": "6"},
            "5": {"type": "action", "content": "Handle error", "one": "6"},
            "6": {"type": "end"}
        }
    }

    valid_path = test_dir / "valid_diagram.json"
    with open(valid_path, 'w', encoding='utf-8') as f:
        json.dump(valid_diagram, f, indent=2, ensure_ascii=False)

    # 2. Невалідна діаграма (відсутні обов'язкові поля, неправильна структура)
    invalid_diagram = {
        # Відсутнє 'name'
        # Відсутнє 'access'
        "items": [  # Має бути dict, а не list!
            {"type": "action", "text": "Do something"},
            # Відсутній 'end'
            # Відсутній 'branch'
        ]
    }

    invalid_path = test_dir / "invalid_diagram.json"
    with open(invalid_path, 'w', encoding='utf-8') as f:
        json.dump(invalid_diagram, f, indent=2, ensure_ascii=False)

    # 3. Діаграма з помилками, що можна виправити
    fixable_diagram = {
        "name": "Fixable Diagram",
        # Відсутнє 'access' (буде додано)
        "items": {
            "1": {"type": "action", "content": "Start"},
            "2": {"type": "action", "content": "Process"}
            # Відсутні 'branch' та 'end' (будуть додані)
        }
    }

    fixable_path = test_dir / "fixable_diagram.json"
    with open(fixable_path, 'w', encoding='utf-8') as f:
        json.dump(fixable_diagram, f, indent=2, ensure_ascii=False)

    return test_dir, [valid_path, invalid_path, fixable_path]


def test_single_import():
    """Тест 1: Імпорт одного файлу"""
    print("="*60)
    print("ТЕСТ 1: Імпорт одного валідного файлу")
    print("="*60)

    test_dir, [valid_path, _, _] = create_test_diagrams()

    importer = DrakonJSONImporter(auto_fix=True)
    diagram, was_corrected = importer.import_diagram(valid_path, save_logs=True)

    assert diagram is not None, "Валідна діаграма повинна імпортуватись"
    assert not was_corrected, "Валідна діаграма не повинна виправлятись"

    print("✅ ТЕСТ ПРОЙДЕНО\n")


def test_auto_correction():
    """Тест 2: Автокорекція"""
    print("="*60)
    print("ТЕСТ 2: Автокорекція діаграми з помилками")
    print("="*60)

    test_dir, [_, _, fixable_path] = create_test_diagrams()

    importer = DrakonJSONImporter(auto_fix=True, strict_mode=False)
    diagram, was_corrected = importer.import_diagram(fixable_path, save_logs=True)

    assert diagram is not None, "Діаграма повинна бути виправлена та імпортована"
    assert was_corrected, "Діаграма повинна бути позначена як виправлена"

    # Перевірка що створено _fixed файл
    fixed_path = fixable_path.parent / f"{fixable_path.stem}_fixed.json"
    assert fixed_path.exists(), "Повинен бути створений _fixed файл"

    print("✅ ТЕСТ ПРОЙДЕНО\n")


def test_batch_import():
    """Тест 3: Batch-імпорт"""
    print("="*60)
    print("ТЕСТ 3: Batch-імпорт директорії")
    print("="*60)

    test_dir, _ = create_test_diagrams()

    importer = DrakonJSONImporter(auto_fix=True)
    results = importer.import_directory(test_dir, save_logs=True)

    assert len(results) >= 3, "Повинно бути оброблено мінімум 3 файли"

    valid_count = sum(1 for _, diagram, _ in results if diagram is not None)
    assert valid_count >= 2, "Як мінімум 2 діаграми повинні бути успішно імпортовані"

    print("✅ ТЕСТ ПРОЙДЕНО\n")


def test_strict_mode():
    """Тест 4: Строгий режим"""
    print("="*60)
    print("ТЕСТ 4: Строгий режим (блокування невалідних)")
    print("="*60)

    test_dir, [_, invalid_path, _] = create_test_diagrams()

    importer = DrakonJSONImporter(auto_fix=False, strict_mode=True)
    diagram, _ = importer.import_diagram(invalid_path, save_logs=False)

    assert diagram is None, "У строгому режимі невалідна діаграма не повинна імпортуватись"

    print("✅ ТЕСТ ПРОЙДЕНО\n")


def cleanup():
    """Очищення тестових файлів"""
    import shutil
    test_dir = Path("./test_diagrams")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("🧹 Тестову директорію очищено")


def main():
    """Головна функція тестування"""
    print("\n" + "="*60)
    print("DRAKON ІМПОРТЕР - ШВИДКИЙ ТЕСТ")
    print("="*60 + "\n")

    try:
        test_single_import()
        test_auto_correction()
        test_batch_import()
        test_strict_mode()

        print("="*60)
        print("🎉 ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!")
        print("="*60)

        # Очищення
        cleanup()

        return 0

    except AssertionError as e:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕНО: {e}")
        return 1

    except Exception as e:
        print(f"\n❌ ПОМИЛКА ТЕСТУВАННЯ: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
