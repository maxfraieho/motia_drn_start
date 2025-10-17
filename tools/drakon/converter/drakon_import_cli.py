#!/usr/bin/env python3
"""
DRAKON JSON Import CLI

Повноцінний CLI-інтерфейс для імпорту та валідації DRAKON JSON діаграм.

Використання:
    # Імпорт одного файлу
    python drakon_import_cli.py import diagram.json

    # Імпорт директорії (batch)
    python drakon_import_cli.py import ./diagrams/ --batch

    # Валідація без імпорту
    python drakon_import_cli.py validate diagram.json

    # Виправлення діаграми
    python drakon_import_cli.py fix diagram.json

    # Виправлення всіх діаграм у директорії
    python drakon_import_cli.py fix ./diagrams/ --batch

Автор: Claude Code + Motia AI Pipeline
Дата: 2025-10-11
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import logging

# Імпорт основного імпортера
from drakon_json_importer import DrakonJSONImporter

# Імпорт інструментів валідації (для окремих команд)
sys.path.insert(0, str(Path(__file__).parent.parent / 'fix'))
from drakon_tools import DrakonValidator, DrakonCorrector
import json


# Налаштування кольорового виводу (опціонально)
class Colors:
    """ANSI color codes для термінального виводу"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def setup_logging(verbose: bool = False):
    """Налаштування логування"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(message)s'  # Спрощений формат для CLI
    )


def cmd_import(args):
    """
    Команда: import
    Імпорт DRAKON діаграм з валідацією та автокорекцією
    """
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.FAIL}❌ Шлях не існує: {input_path}{Colors.ENDC}")
        return 1

    # Створення імпортера
    importer = DrakonJSONImporter(
        strict_mode=args.strict,
        auto_fix=not args.no_fix
    )

    # Batch або одиночний імпорт
    if args.batch:
        if not input_path.is_dir():
            print(f"{Colors.FAIL}❌ Для --batch потрібна директорія{Colors.ENDC}")
            return 1

        results = importer.import_directory(
            input_path,
            pattern=args.pattern,
            recursive=args.recursive,
            save_logs=not args.no_logs
        )

        # Повернення коду помилки якщо були невдалі імпорти
        failed = sum(1 for _, diagram, _ in results if diagram is None)
        return 1 if failed > 0 else 0

    else:
        if not input_path.is_file():
            print(f"{Colors.FAIL}❌ Файл не знайдено: {input_path}{Colors.ENDC}")
            return 1

        diagram, was_corrected = importer.import_diagram(
            input_path,
            save_logs=not args.no_logs
        )

        return 0 if diagram is not None else 1


def cmd_validate(args):
    """
    Команда: validate
    Валідація діаграм без імпорту (швидка перевірка)
    """
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.FAIL}❌ Шлях не існує: {input_path}{Colors.ENDC}")
        return 1

    validator = DrakonValidator()

    # Batch або одиночна валідація
    if args.batch:
        if not input_path.is_dir():
            print(f"{Colors.FAIL}❌ Для --batch потрібна директорія{Colors.ENDC}")
            return 1

        files = list(input_path.glob(args.pattern))
        files = [f for f in files if not f.stem.endswith('_fixed')]

        print(f"{Colors.HEADER}📋 Валідація директорії: {input_path}{Colors.ENDC}")
        print(f"Файлів знайдено: {len(files)}\n")

        results = {'valid': 0, 'invalid': 0}

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    diagram = json.load(f)

                is_valid = validator.validate(diagram)

                if is_valid:
                    print(f"{Colors.OKGREEN}✅ {file_path.name}{Colors.ENDC}")
                    results['valid'] += 1
                else:
                    print(f"{Colors.FAIL}❌ {file_path.name}{Colors.ENDC}")
                    if args.verbose:
                        for error in validator.errors:
                            print(f"   - {error}")
                    results['invalid'] += 1

            except Exception as e:
                print(f"{Colors.FAIL}❌ {file_path.name} (помилка: {e}){Colors.ENDC}")
                results['invalid'] += 1

        print(f"\n{Colors.HEADER}Підсумок:{Colors.ENDC}")
        print(f"✅ Валідних: {results['valid']}")
        print(f"❌ Невалідних: {results['invalid']}")

        return 0 if results['invalid'] == 0 else 1

    else:
        # Одиночна валідація
        if not input_path.is_file():
            print(f"{Colors.FAIL}❌ Файл не знайдено: {input_path}{Colors.ENDC}")
            return 1

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                diagram = json.load(f)

            is_valid = validator.validate(diagram)

            print(f"{Colors.HEADER}📋 Валідація: {input_path.name}{Colors.ENDC}\n")

            if is_valid:
                print(f"{Colors.OKGREEN}✅ Діаграма валідна{Colors.ENDC}")
                return 0
            else:
                print(f"{Colors.FAIL}❌ Знайдено помилки:{Colors.ENDC}")
                print(validator.get_report())
                return 1

        except json.JSONDecodeError as e:
            print(f"{Colors.FAIL}❌ Помилка JSON: {e}{Colors.ENDC}")
            return 1
        except Exception as e:
            print(f"{Colors.FAIL}❌ Помилка: {e}{Colors.ENDC}")
            return 1


def cmd_fix(args):
    """
    Команда: fix
    Виправлення діаграм (без імпорту, тільки збереження виправлених)
    """
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"{Colors.FAIL}❌ Шлях не існує: {input_path}{Colors.ENDC}")
        return 1

    corrector = DrakonCorrector()
    validator = DrakonValidator()

    # Batch або одиночне виправлення
    if args.batch:
        if not input_path.is_dir():
            print(f"{Colors.FAIL}❌ Для --batch потрібна директорія{Colors.ENDC}")
            return 1

        files = list(input_path.glob(args.pattern))
        files = [f for f in files if not f.stem.endswith('_fixed')]

        print(f"{Colors.HEADER}🔧 Виправлення діаграм у: {input_path}{Colors.ENDC}")
        print(f"Файлів знайдено: {len(files)}\n")

        results = {'fixed': 0, 'failed': 0, 'valid': 0}

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    diagram = json.load(f)

                # Перевірка чи потрібне виправлення
                if validator.validate(diagram):
                    print(f"{Colors.OKGREEN}✅ {file_path.name} (вже валідна){Colors.ENDC}")
                    results['valid'] += 1
                    continue

                # Виправлення
                corrected = corrector.correct_diagram(diagram)

                # Повторна валідація
                if validator.validate(corrected):
                    # Збереження
                    output_path = args.output or file_path.parent / f"{file_path.stem}_fixed.json"
                    output_path = Path(output_path)

                    if args.batch and args.output:
                        output_path = Path(args.output) / f"{file_path.stem}_fixed.json"

                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(corrected, f, ensure_ascii=False, indent=2)

                    print(f"{Colors.OKGREEN}🔧 {file_path.name} → {output_path.name}{Colors.ENDC}")
                    results['fixed'] += 1
                else:
                    print(f"{Colors.FAIL}❌ {file_path.name} (не вдалося виправити){Colors.ENDC}")
                    results['failed'] += 1

            except Exception as e:
                print(f"{Colors.FAIL}❌ {file_path.name} (помилка: {e}){Colors.ENDC}")
                results['failed'] += 1

        print(f"\n{Colors.HEADER}Підсумок:{Colors.ENDC}")
        print(f"🔧 Виправлено: {results['fixed']}")
        print(f"✅ Були валідні: {results['valid']}")
        print(f"❌ Помилок: {results['failed']}")

        return 0 if results['failed'] == 0 else 1

    else:
        # Одиночне виправлення
        if not input_path.is_file():
            print(f"{Colors.FAIL}❌ Файл не знайдено: {input_path}{Colors.ENDC}")
            return 1

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                diagram = json.load(f)

            print(f"{Colors.HEADER}🔧 Виправлення: {input_path.name}{Colors.ENDC}\n")

            # Перевірка чи потрібне виправлення
            if validator.validate(diagram):
                print(f"{Colors.OKGREEN}✅ Діаграма вже валідна{Colors.ENDC}")
                return 0

            # Виправлення
            corrected = corrector.correct_diagram(diagram)

            # Повторна валідація
            if not validator.validate(corrected):
                print(f"{Colors.FAIL}❌ Не вдалося виправити діаграму{Colors.ENDC}")
                print(f"\nЗалишилися помилки:")
                for error in validator.errors:
                    print(f"  - {error}")
                return 1

            # Збереження
            output_path = args.output or input_path.parent / f"{input_path.stem}_fixed.json"
            output_path = Path(output_path)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(corrected, f, ensure_ascii=False, indent=2)

            print(f"{Colors.OKGREEN}✅ Діаграма виправлена{Colors.ENDC}")
            print(f"💾 Збережено: {output_path}")
            print(f"\nВиконані корекції:")
            for correction in corrector.corrections:
                print(f"  - {correction}")

            return 0

        except json.JSONDecodeError as e:
            print(f"{Colors.FAIL}❌ Помилка JSON: {e}{Colors.ENDC}")
            return 1
        except Exception as e:
            print(f"{Colors.FAIL}❌ Помилка: {e}{Colors.ENDC}")
            return 1


def main():
    """Головна функція CLI"""

    parser = argparse.ArgumentParser(
        prog='drakon-import',
        description='DRAKON JSON імпортер з валідацією та автокорекцією',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:

  # Імпорт одного файлу
  %(prog)s import diagram.json

  # Імпорт директорії
  %(prog)s import ./diagrams/ --batch

  # Валідація без імпорту
  %(prog)s validate diagram.json

  # Валідація директорії
  %(prog)s validate ./diagrams/ --batch

  # Виправлення одного файлу
  %(prog)s fix diagram.json

  # Виправлення директорії
  %(prog)s fix ./diagrams/ --batch --output ./fixed/

  # Строгий режим (не імпортувати невалідні)
  %(prog)s import diagram.json --strict

  # Вимкнути автокорекцію
  %(prog)s import diagram.json --no-fix

Для детальної інформації про команду:
  %(prog)s <команда> --help
        """
    )

    # Підкоманди
    subparsers = parser.add_subparsers(dest='command', help='Доступні команди')

    # === КОМАНДА: import ===
    import_parser = subparsers.add_parser(
        'import',
        help='Імпорт DRAKON діаграм з валідацією та автокорекцією'
    )
    import_parser.add_argument('input', type=str, help='Файл або директорія')
    import_parser.add_argument('--batch', action='store_true', help='Обробити всі файли в директорії')
    import_parser.add_argument('--pattern', default='*.json', help='Glob-патерн (за замовчуванням: *.json)')
    import_parser.add_argument('--recursive', '-r', action='store_true', help='Рекурсивний пошук')
    import_parser.add_argument('--no-fix', action='store_true', help='Вимкнути автокорекцію')
    import_parser.add_argument('--strict', action='store_true', help='Не імпортувати невалідні діаграми')
    import_parser.add_argument('--no-logs', action='store_true', help='Не зберігати лог-файли')
    import_parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')

    # === КОМАНДА: validate ===
    validate_parser = subparsers.add_parser(
        'validate',
        help='Валідація діаграм без імпорту (швидка перевірка)'
    )
    validate_parser.add_argument('input', type=str, help='Файл або директорія')
    validate_parser.add_argument('--batch', action='store_true', help='Перевірити всі файли в директорії')
    validate_parser.add_argument('--pattern', default='*.json', help='Glob-патерн (за замовчуванням: *.json)')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Показати всі помилки')

    # === КОМАНДА: fix ===
    fix_parser = subparsers.add_parser(
        'fix',
        help='Виправлення діаграм (збереження _fixed файлів)'
    )
    fix_parser.add_argument('input', type=str, help='Файл або директорія')
    fix_parser.add_argument('--batch', action='store_true', help='Виправити всі файли в директорії')
    fix_parser.add_argument('--pattern', default='*.json', help='Glob-патерн (за замовчуванням: *.json)')
    fix_parser.add_argument('--output', '-o', type=str, help='Вихідна директорія (для batch)')
    fix_parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')

    # Парсинг аргументів
    args = parser.parse_args()

    # Перевірка чи вказана команда
    if not args.command:
        parser.print_help()
        return 1

    # Налаштування логування
    setup_logging(getattr(args, 'verbose', False))

    # Виконання команди
    if args.command == 'import':
        return cmd_import(args)
    elif args.command == 'validate':
        return cmd_validate(args)
    elif args.command == 'fix':
        return cmd_fix(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
