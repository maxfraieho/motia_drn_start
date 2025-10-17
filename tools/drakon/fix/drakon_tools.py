
import json
import os
from typing import Dict, List, Set, Any, Optional
from pathlib import Path

class DrakonValidator:
    """Валідатор для ДРАКОН JSON діаграм"""

    VALID_TYPES = {
        'action', 'question', 'branch', 'end', 'header', 'case', 'select',
        'foreach', 'insertion', 'comment', 'parblock', 'par', 'timer', 
        'pause', 'duration', 'shelf', 'process', 'input', 'output',
        'ctrlstart', 'ctrlend', 'drakon-image'
    }

    REQUIRED_FIELDS = {'name', 'access', 'items'}

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, diagram: Dict[str, Any]) -> bool:
        """Основна функція валідації"""
        self.errors.clear()
        self.warnings.clear()

        # Перевірка структури верхнього рівня
        self._validate_top_level(diagram)

        if 'items' in diagram and isinstance(diagram['items'], dict):
            # Перевірка елементів
            self._validate_items(diagram['items'])

            # Перевірка зв'язків між елементами
            self._validate_connections(diagram['items'])

            # Перевірка семантики діаграми
            self._validate_semantics(diagram['items'])

        return len(self.errors) == 0

    def _validate_top_level(self, diagram: Dict[str, Any]) -> None:
        """Перевірка структури верхнього рівня"""
        # Перевірка обов'язкових полів
        for field in self.REQUIRED_FIELDS:
            if field not in diagram:
                self.errors.append(f"Відсутнє обов'язкове поле '{field}'")

        # Перевірка типів полів
        if 'name' in diagram and not isinstance(diagram['name'], str):
            self.errors.append("Поле 'name' повинно бути рядком")

        if 'access' in diagram and diagram['access'] not in ['read', 'write']:
            self.errors.append("Поле 'access' повинно бути 'read' або 'write'")

        if 'items' in diagram and not isinstance(diagram['items'], dict):
            self.errors.append("Поле 'items' повинно бути словником")

        # Перевірка стилю
        if 'style' in diagram:
            if not isinstance(diagram['style'], str):
                self.errors.append("Поле 'style' повинно бути рядком з JSON")
            else:
                try:
                    json.loads(diagram['style'])
                except json.JSONDecodeError:
                    self.errors.append("Поле 'style' містить невалідний JSON")

    def _validate_items(self, items: Dict[str, Any]) -> None:
        """Перевірка елементів діаграми"""
        if not items:
            self.errors.append("Діаграма не містить елементів")
            return

        for item_id, item in items.items():
            # Перевірка ID
            if not isinstance(item_id, str):
                self.errors.append(f"ID елемента повинен бути рядком: {item_id}")

            # Перевірка структури елемента
            if not isinstance(item, dict):
                self.errors.append(f"Елемент {item_id} повинен бути словником")
                continue

            # Перевірка типу елемента
            if 'type' not in item:
                self.errors.append(f"Елемент {item_id} не має поля 'type'")
                continue

            if item['type'] not in self.VALID_TYPES:
                self.errors.append(f"Невідомий тип елемента '{item['type']}' в {item_id}")

            # Специфічні перевірки для типів
            self._validate_item_specific(item_id, item)

    def _validate_item_specific(self, item_id: str, item: Dict[str, Any]) -> None:
        """Специфічні перевірки для різних типів елементів"""
        item_type = item.get('type')

        # Branch повинен мати branchId
        if item_type == 'branch':
            if 'branchId' not in item:
                self.errors.append(f"Branch елемент {item_id} повинен мати 'branchId'")
            elif not isinstance(item['branchId'], int):
                self.errors.append(f"branchId в {item_id} повинен бути цілим числом")

        # Question повинен мати flag1
        if item_type == 'question':
            if 'flag1' in item and not isinstance(item['flag1'], int):
                self.errors.append(f"flag1 в {item_id} повинен бути цілим числом")

        # Перевірка content
        if 'content' in item and not isinstance(item['content'], str):
            self.errors.append(f"content в {item_id} повинен бути рядком")

        # Перевірка style
        if 'style' in item:
            if not isinstance(item['style'], str):
                self.errors.append(f"style в {item_id} повинен бути рядком з JSON")
            else:
                try:
                    json.loads(item['style'])
                except json.JSONDecodeError:
                    self.errors.append(f"style в {item_id} містить невалідний JSON")

    def _validate_connections(self, items: Dict[str, Any]) -> None:
        """Перевірка зв'язків між елементами"""
        item_ids = set(items.keys())

        for item_id, item in items.items():
            # Перевірка посилань 'one'
            if 'one' in item:
                if item['one'] not in item_ids:
                    self.errors.append(f"Елемент {item_id} посилається на неіснуючий елемент '{item['one']}' в полі 'one'")

            # Перевірка посилань 'two'
            if 'two' in item:
                if item['two'] not in item_ids:
                    self.errors.append(f"Елемент {item_id} посилається на неіснуючий елемент '{item['two']}' в полі 'two'")

            # Перевірка посилань 'side'
            if 'side' in item:
                if item['side'] not in item_ids:
                    self.errors.append(f"Елемент {item_id} посилається на неіснуючий елемент '{item['side']}' в полі 'side'")

    def _validate_semantics(self, items: Dict[str, Any]) -> None:
        """Перевірка семантики діаграми"""
        # Перевірка наявності end елемента
        end_elements = [item_id for item_id, item in items.items() if item.get('type') == 'end']
        if not end_elements:
            self.errors.append("Діаграма повинна містити принаймні один 'end' елемент")
        elif len(end_elements) > 1:
            self.warnings.append("Діаграма містить декілька 'end' елементів")

        # Перевірка наявності branch елемента
        branch_elements = [item_id for item_id, item in items.items() if item.get('type') == 'branch']
        if not branch_elements:
            self.warnings.append("Діаграма не містить 'branch' елементів")

        # Перевірка branchId послідовності
        if branch_elements:
            branch_ids = [item.get('branchId', 0) for item_id, item in items.items() 
                         if item.get('type') == 'branch']
            branch_ids.sort()
            if branch_ids[0] != 0:
                self.errors.append("Перший branch повинен мати branchId = 0")

            for i in range(1, len(branch_ids)):
                if branch_ids[i] != branch_ids[i-1] + 1:
                    self.warnings.append("branchId не утворюють послідовність")
                    break

    def get_report(self) -> str:
        """Отримати звіт валідації"""
        report = []

        if self.errors:
            report.append("=== ПОМИЛКИ ===")
            for i, error in enumerate(self.errors, 1):
                report.append(f"{i}. {error}")

        if self.warnings:
            report.append("\n=== ПОПЕРЕДЖЕННЯ ===")
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"{i}. {warning}")

        if not self.errors and not self.warnings:
            report.append("✅ Діаграма валідна!")

        return "\n".join(report)


class DrakonCorrector:
    """Корректор для автоматичного виправлення поширених помилок у ДРАКОН JSON діаграмах"""

    def __init__(self):
        self.validator = DrakonValidator()
        self.corrections = []

    def correct_diagram(self, diagram: Dict[str, Any]) -> Dict[str, Any]:
        """Автоматично виправляє поширені помилки"""
        self.corrections.clear()
        corrected = dict(diagram)  # Створюємо копію

        # Виправлення структури верхнього рівня
        corrected = self._fix_top_level(corrected)

        # Виправлення елементів
        if 'items' in corrected:
            corrected['items'] = self._fix_items(corrected['items'])

        return corrected

    def _fix_top_level(self, diagram: Dict[str, Any]) -> Dict[str, Any]:
        """Виправлення структури верхнього рівня"""
        # Додаємо обов'язкові поля якщо вони відсутні
        if 'name' not in diagram:
            diagram['name'] = "Unnamed DRAKON Diagram"
            self.corrections.append("Додано відсутнє поле 'name'")

        if 'access' not in diagram:
            diagram['access'] = "write"
            self.corrections.append("Додано відсутнє поле 'access'")

        if 'items' not in diagram:
            diagram['items'] = {}
            self.corrections.append("Додано відсутнє поле 'items'")

        # Конвертуємо items з списку в словник якщо потрібно
        if isinstance(diagram['items'], list):
            items_dict = {}
            for i, item in enumerate(diagram['items']):
                items_dict[str(i + 1)] = item
            diagram['items'] = items_dict
            self.corrections.append("Конвертовано 'items' зі списку в словник")

        # Виправлення style
        if 'style' in diagram and isinstance(diagram['style'], dict):
            diagram['style'] = json.dumps(diagram['style'])
            self.corrections.append("Конвертовано 'style' з об'єкта в JSON рядок")

        return diagram

    def _fix_items(self, items: Any) -> Dict[str, Any]:
        """Виправлення елементів"""
        # Якщо items не словник, конвертуємо
        if not isinstance(items, dict):
            return {}

        fixed_items = {}
        branch_counter = 0

        for item_id, item in items.items():
            if not isinstance(item, dict):
                continue

            fixed_item = dict(item)

            # Конвертуємо числові ID в рядки
            string_id = str(item_id)

            # Додаємо type якщо відсутній
            if 'type' not in fixed_item:
                fixed_item['type'] = 'action'
                self.corrections.append(f"Додано відсутній 'type' для елемента {string_id}")

            # Виправлення для branch елементів
            if fixed_item.get('type') == 'branch':
                if 'branchId' not in fixed_item:
                    fixed_item['branchId'] = branch_counter
                    branch_counter += 1
                    self.corrections.append(f"Додано 'branchId' для branch елемента {string_id}")

            # Виправлення style
            if 'style' in fixed_item and isinstance(fixed_item['style'], dict):
                fixed_item['style'] = json.dumps(fixed_item['style'])
                self.corrections.append(f"Конвертовано 'style' в JSON рядок для елемента {string_id}")

            # Конвертуємо content в рядок
            if 'content' in fixed_item and not isinstance(fixed_item['content'], str):
                fixed_item['content'] = str(fixed_item['content'])
                self.corrections.append(f"Конвертовано 'content' в рядок для елемента {string_id}")

            # Конвертуємо посилання в рядки
            for ref_field in ['one', 'two', 'side']:
                if ref_field in fixed_item and not isinstance(fixed_item[ref_field], str):
                    fixed_item[ref_field] = str(fixed_item[ref_field])
                    self.corrections.append(f"Конвертовано '{ref_field}' в рядок для елемента {string_id}")

            fixed_items[string_id] = fixed_item

        # Додаємо мінімальні обов'язкові елементи якщо їх немає
        has_end = any(item.get('type') == 'end' for item in fixed_items.values())
        has_branch = any(item.get('type') == 'branch' for item in fixed_items.values())

        end_id = None
        if not has_end:
            end_id = str(len(fixed_items) + 1)
            fixed_items[end_id] = {'type': 'end'}
            self.corrections.append("Додано відсутній 'end' елемент")
        else:
            # Знаходимо існуючий end елемент
            end_id = next(id for id, item in fixed_items.items() if item.get('type') == 'end')

        if not has_branch:
            branch_id = str(len(fixed_items) + 1)
            # Знаходимо перший не-end елемент для зв'язку
            first_action = next((id for id, item in fixed_items.items() 
                               if item.get('type') != 'end'), end_id)
            fixed_items[branch_id] = {
                'type': 'branch',
                'branchId': 0,
                'one': first_action
            }
            self.corrections.append("Додано відсутній 'branch' елемент")

        return fixed_items

    def get_corrections_report(self) -> str:
        """Отримати звіт про виконані корекції"""
        if not self.corrections:
            return "Корекції не потрібні"

        report = ["=== ВИКОНАНІ КОРЕКЦІЇ ==="]
        for i, correction in enumerate(self.corrections, 1):
            report.append(f"{i}. {correction}")

        return "\n".join(report)


class DrakonAnalyzer:
    """Аналізатор ДРАКОН JSON файлів"""

    def __init__(self):
        self.validator = DrakonValidator()
        self.corrector = DrakonCorrector()

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Аналізує один файл ДРАКОН діаграми"""
        result = {
            'file_path': file_path,
            'exists': False,
            'readable': False,
            'valid_json': False,
            'content': None,
            'validation_errors': [],
            'validation_warnings': [],
            'corrections_needed': [],
            'is_valid_drakon': False
        }

        try:
            # Перевірка існування файлу
            if not os.path.exists(file_path):
                return result
            result['exists'] = True

            # Спроба читання файлу
            with open(file_path, 'r', encoding='utf-8') as f:
                content_str = f.read()
            result['readable'] = True

            # Спроба парсингу JSON
            content = json.loads(content_str)
            result['valid_json'] = True
            result['content'] = content

            # Валідація як ДРАКОН діаграми
            is_valid = self.validator.validate(content)
            result['is_valid_drakon'] = is_valid
            result['validation_errors'] = list(self.validator.errors)
            result['validation_warnings'] = list(self.validator.warnings)

            # Перевірка можливих корекцій
            corrected = self.corrector.correct_diagram(content)
            if self.corrector.corrections:
                result['corrections_needed'] = list(self.corrector.corrections)

        except FileNotFoundError:
            result['error'] = "Файл не знайдено"
        except PermissionError:
            result['error'] = "Немає дозволу на читання файлу"
        except json.JSONDecodeError as e:
            result['error'] = f"Помилка JSON: {e}"
        except Exception as e:
            result['error'] = f"Неочікувана помилка: {e}"

        return result

    def fix_and_save_file(self, input_path: str, output_path: str = None) -> Dict[str, Any]:
        """Виправляє файл та зберігає результат"""
        if output_path is None:
            output_path = input_path.replace('.json', '_fixed.json')

        result = {'success': False, 'message': '', 'corrections': []}

        try:
            # Аналізуємо файл
            analysis = self.analyze_file(input_path)

            if not analysis.get('valid_json'):
                result['message'] = 'Файл не містить валідний JSON'
                return result

            # Виправляємо діаграму
            corrected = self.corrector.correct_diagram(analysis['content'])

            # Зберігаємо виправлену діаграму
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(corrected, f, ensure_ascii=False, indent=2)

            result['success'] = True
            result['message'] = f'Діаграма виправлена та збережена в {output_path}'
            result['corrections'] = list(self.corrector.corrections)
            result['output_path'] = output_path

        except Exception as e:
            result['message'] = f'Помилка: {e}'

        return result
