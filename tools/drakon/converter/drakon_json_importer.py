#!/usr/bin/env python3
"""
DRAKON JSON Імпортер з Валідацією та Автокорекцією

Інтегрований імпортер DRAKON JSON діаграм з:
- Автоматичною валідацією через DrakonValidator
- Автокорекцією помилок через DrakonCorrector
- Збереженням виправлених діаграм із суфіксом _fixed
- Генерацією лог-файлів біля діаграм
- Batch-обробкою всіх JSON файлів у директорії

Автор: Claude Code + Motia AI Pipeline
Дата: 2025-10-11
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging

# Імпорт класів валідації та корекції
# INTEGRATION POINT: Додайте sys.path якщо drakon_tools.py в іншій директорії
sys.path.insert(0, str(Path(__file__).parent.parent / 'fix'))
from drakon_tools import DrakonValidator, DrakonCorrector, DrakonAnalyzer


# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DrakonJSONImporter:
    """
    Імпортер DRAKON JSON діаграм з валідацією та автокорекцією

    Функціональність:
    - Читання JSON файлів діаграм
    - Валідація структури через DrakonValidator
    - Автоматичне виправлення помилок через DrakonCorrector
    - Збереження виправлених діаграм (_fixed.json)
    - Генерація лог-файлів валідації та корекції
    - Batch-обробка директорій
    """

    def __init__(self, strict_mode: bool = False, auto_fix: bool = True):
        """
        Ініціалізація імпортера

        Args:
            strict_mode: Якщо True, не імпортує діаграми з помилками без виправлення
            auto_fix: Якщо True, автоматично виправляє діаграми з помилками
        """
        self.validator = DrakonValidator()
        self.corrector = DrakonCorrector()
        self.analyzer = DrakonAnalyzer()
        self.strict_mode = strict_mode
        self.auto_fix = auto_fix

        self.stats = {
            'total': 0,
            'valid': 0,
            'corrected': 0,
            'failed': 0
        }

    def import_diagram(
        self,
        file_path: Path,
        save_logs: bool = True
    ) -> Tuple[Optional[Dict[str, Any]], bool]:
        """
        Імпорт одного файлу DRAKON діаграми

        Процес:
        1. Читання JSON файлу
        2. Валідація структури
        3. Якщо є помилки → автокорекція (якщо увімкнено)
        4. Збереження виправленої діаграми (_fixed.json)
        5. Генерація лог-файлів

        Args:
            file_path: Шлях до JSON файлу діаграми
            save_logs: Чи зберігати лог-файли

        Returns:
            Tuple[діаграма, чи була виправлена]
            - діаграма: Dict з даними діаграми або None якщо імпорт не вдався
            - була_виправлена: True якщо діаграма була автоматично виправлена
        """
        file_path = Path(file_path)
        self.stats['total'] += 1

        logger.info(f"📥 Імпорт діаграми: {file_path.name}")

        # Крок 1: Читання JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                diagram = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Помилка JSON: {e}")
            self.stats['failed'] += 1
            return None, False
        except FileNotFoundError:
            logger.error(f"❌ Файл не знайдено: {file_path}")
            self.stats['failed'] += 1
            return None, False

        # Крок 2: Валідація
        is_valid = self.validator.validate(diagram)

        if is_valid:
            logger.info(f"✅ Діаграма валідна: {file_path.name}")
            self.stats['valid'] += 1

            # Збереження лог-файлу (опціонально)
            if save_logs:
                self._save_validation_log(file_path, success=True)

            return diagram, False

        # Діаграма має помилки
        logger.warning(f"⚠️  Знайдено помилки валідації:")
        for error in self.validator.errors:
            logger.warning(f"   - {error}")

        # Крок 3: Автокорекція (якщо увімкнено)
        if not self.auto_fix:
            logger.error(f"❌ Автокорекція вимкнена, діаграма не імпортована")
            self.stats['failed'] += 1

            if save_logs:
                self._save_validation_log(file_path, success=False)

            return None, False

        # Виправлення діаграми
        logger.info(f"🔧 Виконую автокорекцію...")
        corrected_diagram = self.corrector.correct_diagram(diagram)

        # Крок 4: Повторна валідація
        is_fixed = self.validator.validate(corrected_diagram)

        if not is_fixed:
            logger.error(f"❌ Не вдалося виправити діаграму автоматично")
            logger.error(f"   Залишилися помилки:")
            for error in self.validator.errors:
                logger.error(f"   - {error}")

            self.stats['failed'] += 1

            if save_logs:
                self._save_validation_log(file_path, success=False)
                self._save_correction_log(file_path, success=False)

            if self.strict_mode:
                return None, False
            else:
                # У нестрогому режимі повертаємо виправлену (але не валідну) діаграму
                return corrected_diagram, True

        # Діаграма успішно виправлена
        logger.info(f"✅ Діаграма виправлена успішно")
        logger.info(f"   Виконано корекцій: {len(self.corrector.corrections)}")
        for correction in self.corrector.corrections:
            logger.info(f"   - {correction}")

        self.stats['corrected'] += 1

        # Крок 5: Збереження виправленої діаграми
        fixed_path = self._save_fixed_diagram(file_path, corrected_diagram)
        logger.info(f"💾 Збережено виправлену діаграму: {fixed_path.name}")

        # Крок 6: Збереження лог-файлів
        if save_logs:
            self._save_validation_log(file_path, success=True, was_corrected=True)
            self._save_correction_log(file_path, success=True)

        return corrected_diagram, True

    def import_directory(
        self,
        directory: Path,
        pattern: str = "*.json",
        recursive: bool = False,
        save_logs: bool = True
    ) -> List[Tuple[Path, Optional[Dict[str, Any]], bool]]:
        """
        Batch-обробка всіх JSON файлів у директорії

        Args:
            directory: Директорія для сканування
            pattern: Glob-патерн для пошуку файлів (за замовчуванням "*.json")
            recursive: Чи шукати рекурсивно в піддиректоріях
            save_logs: Чи зберігати лог-файли для кожної діаграми

        Returns:
            Список кортежів (шлях, діаграма, чи_була_виправлена)
        """
        directory = Path(directory)

        if not directory.exists():
            logger.error(f"❌ Директорія не існує: {directory}")
            return []

        # Пошук JSON файлів
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))

        # Фільтрація: не обробляємо _fixed файли
        files = [f for f in files if not f.stem.endswith('_fixed')]

        logger.info(f"📂 Batch-обробка директорії: {directory}")
        logger.info(f"   Знайдено файлів: {len(files)}")

        results = []

        for file_path in files:
            diagram, was_corrected = self.import_diagram(file_path, save_logs=save_logs)
            results.append((file_path, diagram, was_corrected))
            print()  # Розділювач між файлами

        # Виведення підсумкової статистики
        self._print_summary()

        return results

    def _save_fixed_diagram(
        self,
        original_path: Path,
        diagram: Dict[str, Any]
    ) -> Path:
        """
        Збереження виправленої діаграми з суфіксом _fixed

        Args:
            original_path: Шлях до оригінального файлу
            diagram: Виправлена діаграма

        Returns:
            Шлях до збереженого файлу
        """
        fixed_path = original_path.parent / f"{original_path.stem}_fixed.json"

        with open(fixed_path, 'w', encoding='utf-8') as f:
            json.dump(diagram, f, ensure_ascii=False, indent=2)

        return fixed_path

    def _save_validation_log(
        self,
        diagram_path: Path,
        success: bool,
        was_corrected: bool = False
    ):
        """
        Збереження лог-файлу валідації біля діаграми

        Args:
            diagram_path: Шлях до діаграми
            success: Чи пройшла валідація
            was_corrected: Чи була діаграма виправлена
        """
        log_path = diagram_path.parent / f"{diagram_path.stem}_validation.log"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== DRAKON VALIDATION LOG ===\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"File: {diagram_path.name}\n")
            f.write(f"Status: {'✅ PASS' if success else '❌ FAIL'}\n")

            if was_corrected:
                f.write(f"Note: Діаграма була автоматично виправлена\n")

            f.write(f"\n{self.validator.get_report()}\n")

    def _save_correction_log(
        self,
        diagram_path: Path,
        success: bool
    ):
        """
        Збереження лог-файлу корекції біля діаграми

        Args:
            diagram_path: Шлях до діаграми
            success: Чи успішна була корекція
        """
        log_path = diagram_path.parent / f"{diagram_path.stem}_correction.log"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== DRAKON CORRECTION LOG ===\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"File: {diagram_path.name}\n")
            f.write(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}\n\n")
            f.write(f"{self.corrector.get_corrections_report()}\n")

    def _print_summary(self):
        """Виведення підсумкової статистики обробки"""
        logger.info("=" * 60)
        logger.info("📊 ПІДСУМКОВА СТАТИСТИКА")
        logger.info("=" * 60)
        logger.info(f"Всього оброблено:        {self.stats['total']}")
        logger.info(f"✅ Валідних:              {self.stats['valid']}")
        logger.info(f"🔧 Виправлено:            {self.stats['corrected']}")
        logger.info(f"❌ Помилок:               {self.stats['failed']}")
        logger.info("=" * 60)


def main():
    """
    CLI Entry Point (базовий приклад)

    Повний CLI буде реалізовано окремо через drakon_import_cli.py
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='DRAKON JSON Імпортер з валідацією та автокорекцією',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Шлях до JSON файлу або директорії'
    )

    parser.add_argument(
        '--batch',
        action='store_true',
        help='Обробити всі JSON файли в директорії'
    )

    parser.add_argument(
        '--no-fix',
        action='store_true',
        help='Вимкнути автокорекцію'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Строгий режим: не імпортувати невалідні діаграми'
    )

    parser.add_argument(
        '--no-logs',
        action='store_true',
        help='Не зберігати лог-файли'
    )

    args = parser.parse_args()

    # Створення імпортера
    importer = DrakonJSONImporter(
        strict_mode=args.strict,
        auto_fix=not args.no_fix
    )

    # Обробка
    if args.batch:
        if not args.input.is_dir():
            logger.error(f"❌ Для --batch потрібна директорія, отримано: {args.input}")
            return 1

        importer.import_directory(
            args.input,
            save_logs=not args.no_logs
        )
    else:
        if not args.input.is_file():
            logger.error(f"❌ Файл не знайдено: {args.input}")
            return 1

        diagram, was_corrected = importer.import_diagram(
            args.input,
            save_logs=not args.no_logs
        )

        if diagram is None:
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
