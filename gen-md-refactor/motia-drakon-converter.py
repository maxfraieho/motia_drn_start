#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced DRAKON to Pseudocode Converter
========================================
Покращений конвертер ДРАКОН-схем в псевдокод з повним розумінням мови.

Базується на статті про мову ДРАКОН (drakon.md):
- Ікони: Вопрос, Выбор, Цикл ДЛЯ, Действие
- Візуальні логічні формули
- Силуети і ветки
- Принципи: "чем правее, тем хуже", царская дорога, общая судьба

Автор: DevOps Engineer
Версія: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class IconType(Enum):
    """Типи ікон ДРАКОН згідно зі специфікацією"""
    # Основні ікони
    ACTION = "action"  # Дія (прямокутник)
    QUESTION = "question"  # Вопрос (усічений ромб)
    SELECT = "select"  # Выбор (ромб з варіантами)
    CASE = "case"  # Варіант вибору

    # Цикли
    LOOP_BEGIN = "loopBegin"  # Початок циклу
    LOOP_END = "loopEnd"  # Кінець циклу
    FOR_LOOP = "foreach"  # Цикл ДЛЯ

    # Силует
    BRANCH = "branch"  # Ветка силуету (шапка ветки)
    ADDRESS = "address"  # Адрес (посилання на ветку)

    # Спеціальні
    START = "start"  # Початок (заголовок)
    END = "end"  # Кінець
    PARAMS = "params"  # Формальні параметри
    COMMENT = "comment"  # Коментар

    UNKNOWN = "unknown"  # Невідомий тип

    @classmethod
    def from_string(cls, type_str: str) -> 'IconType':
        """Конвертує рядок в IconType"""
        try:
            return cls(type_str.lower())
        except ValueError:
            return cls.UNKNOWN


@dataclass
class DrakonNode:
    """Вузол ДРАКОН-схеми"""
    node_id: str
    icon_type: IconType
    text: str = ""
    x: int = 0
    y: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_control_flow(self) -> bool:
        """Чи є це вузол управління потоком"""
        return self.icon_type in {
            IconType.QUESTION, IconType.SELECT, IconType.LOOP_BEGIN,
            IconType.FOR_LOOP, IconType.BRANCH
        }

    @property
    def is_loop(self) -> bool:
        """Чи є це цикл"""
        return self.icon_type in {IconType.LOOP_BEGIN, IconType.FOR_LOOP}


@dataclass
class DrakonEdge:
    """Зв'язок між вузлами"""
    source: str
    target: str
    label: str = ""
    is_yes: bool = False
    is_no: bool = False

    @property
    def is_backward(self) -> bool:
        """Чи є це зворотній зв'язок (стрілка вгору = цикл)"""
        # Визначається за координатами або позначкою
        return "loop" in self.label.lower() or "↑" in self.label


class DrakonConverter:
    """
    Покращений конвертер ДРАКОН → Псевдокод.

    Враховує всі принципи мови ДРАКОН:
    - Структурне програмування
    - Візуальні логічні формули
    - Силуети та ветки
    - Царська дорога (шампур)
    - Принцип "чем правее, тем хуже"
    """

    def __init__(self):
        self.nodes: Dict[str, DrakonNode] = {}
        self.edges: List[DrakonEdge] = []
        self.indent_level = 0
        self.output: List[str] = []

    def load_from_file(self, file_path: Path) -> bool:
        """Завантажує ДРАКОН-схему з JSON файлу"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._parse_nodes(data.get('nodes', {}))
            self._parse_edges(data.get('edges', []))

            return True

        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False

    def _parse_nodes(self, nodes_data: Dict[str, Any]):
        """Розбирає вузли з JSON"""
        for node_id, node_info in nodes_data.items():
            icon_type = IconType.from_string(node_info.get('type', 'unknown'))

            # Витягуємо текст
            content = node_info.get('content', {})
            if isinstance(content, dict):
                text = content.get('txt', '').strip()
            else:
                text = str(content).strip()

            # Координати (для визначення розташування)
            x = node_info.get('x', 0)
            y = node_info.get('y', 0)

            node = DrakonNode(
                node_id=node_id,
                icon_type=icon_type,
                text=text,
                x=x,
                y=y,
                metadata=node_info
            )

            self.nodes[node_id] = node

    def _parse_edges(self, edges_data: List[Dict[str, Any]]):
        """Розбирає зв'язки між вузлами"""
        for edge_info in edges_data:
            source = edge_info.get('src', '')
            target = edge_info.get('dst', '')
            label = edge_info.get('label', '').strip()

            # Визначаємо тип зв'язку
            is_yes = label.lower() in ['да', 'yes', '+']
            is_no = label.lower() in ['нет', 'но', 'no', '-']

            edge = DrakonEdge(
                source=source,
                target=target,
                label=label,
                is_yes=is_yes,
                is_no=is_no
            )

            self.edges.append(edge)

    def convert_to_pseudocode(self) -> str:
        """
        Конвертує ДРАКОН-схему в структурований псевдокод.

        Returns:
            Рядок з псевдокодом
        """
        self.output = []
        self.indent_level = 0

        # Заголовок
        self._add_header()

        # Знаходимо вузол START
        start_node = self._find_start_node()
        if not start_node:
            self._add_line("# ❌ START node not found")
            return "\n".join(self.output)

        # Формальні параметри (якщо є)
        self._add_parameters()

        # Силует або звичайна діаграма
        if self._has_silhouette():
            self._process_silhouette()
        else:
            self._process_main_flow(start_node)

        # Підсумок
        self._add_footer()

        return "\n".join(self.output)

    def _add_header(self):
        """Додає заголовок документа"""
        self._add_line("=" * 70)
        self._add_line("ДРАКОН-СХЕМА: Псевдокод алгоритму")
        self._add_line("=" * 70)
        self._add_line("")

    def _add_footer(self):
        """Додає підвал документа"""
        self._add_line("")
        self._add_line("=" * 70)
        self._add_line("КІНЕЦЬ АЛГОРИТМУ")
        self._add_line("=" * 70)

    def _find_start_node(self) -> Optional[DrakonNode]:
        """Знаходить початковий вузол"""
        for node in self.nodes.values():
            if node.icon_type == IconType.START:
                return node
        return None

    def _add_parameters(self):
        """Додає формальні параметри функції"""
        for node in self.nodes.values():
            if node.icon_type == IconType.PARAMS and node.text:
                self._add_line(f"ПАРАМЕТРИ: {node.text}")
                self._add_line("")

    def _has_silhouette(self) -> bool:
        """Перевіряє, чи є в схемі силует (ветки)"""
        for node in self.nodes.values():
            if node.icon_type == IconType.BRANCH:
                return True
        return False

    def _process_silhouette(self):
        """Обробляє схему типу 'силует'"""
        self._add_line("# СТРУКТУРА: Силует (багатогіллєвий алгоритм)")
        self._add_line("")

        # Знаходимо всі ветки
        branches = [n for n in self.nodes.values() if n.icon_type == IconType.BRANCH]
        branches.sort(key=lambda n: n.x)  # Сортуємо зліва направо

        self._add_line("ВЕТКИ СИЛУЕТУ:")
        for i, branch in enumerate(branches, 1):
            self._add_line(f"  {i}. {branch.text or f'Ветка {branch.node_id}'}")

        self._add_line("")
        self._add_line("ВИКОНАННЯ:")
        self._add_line("")

        # Обробляємо кожну ветку
        for branch in branches:
            self._process_branch(branch)

    def _process_branch(self, branch: DrakonNode):
        """Обробляє одну ветку силуету"""
        self._add_line(f"╔═══ ВЕТКА: {branch.text} ═══╗")
        self.indent_level += 1

        # Знаходимо наступні вузли після шапки ветки
        next_nodes = self._get_outgoing_nodes(branch.node_id)

        for next_node_id in next_nodes:
            self._process_node_flow(next_node_id)

        self.indent_level -= 1
        self._add_line(f"╚══════════════════════════════╝")
        self._add_line("")

    def _process_main_flow(self, start_node: DrakonNode):
        """Обробляє основний потік виконання (без силуету)"""
        self._add_line(f"АЛГОРИТМ: {start_node.text or 'Unnamed'}")
        self._add_line("")
        self._add_line("ПОЧАТОК")
        self.indent_level += 1

        # Знаходимо наступні вузли після START
        next_nodes = self._get_outgoing_nodes(start_node.node_id)

        for next_node_id in next_nodes:
            self._process_node_flow(next_node_id)

        self.indent_level -= 1
        self._add_line("КІНЕЦЬ")

    def _process_node_flow(self, node_id: str, visited: Optional[set] = None):
        """Рекурсивно обробляє потік вузлів"""
        if visited is None:
            visited = set()

        if node_id in visited:
            self._add_line("# [Цикл: повернення до раніше відвіданого вузла]")
            return

        visited.add(node_id)

        node = self.nodes.get(node_id)
        if not node:
            return

        # Обробка різних типів ікон
        if node.icon_type == IconType.ACTION:
            self._process_action(node)

        elif node.icon_type == IconType.QUESTION:
            self._process_question(node, visited)

        elif node.icon_type == IconType.SELECT:
            self._process_select(node, visited)

        elif node.icon_type == IconType.FOR_LOOP:
            self._process_for_loop(node, visited)

        elif node.icon_type == IconType.LOOP_BEGIN:
            self._process_loop_begin(node, visited)

        elif node.icon_type == IconType.ADDRESS:
            self._process_address(node)

        elif node.icon_type == IconType.END:
            self._add_line("# ВИХІД з алгоритму")

        elif node.icon_type == IconType.COMMENT:
            self._add_line(f"# КОМЕНТАР: {node.text}")

        # Переходимо до наступних вузлів (якщо не контрольний потік)
        if not node.is_control_flow:
            next_nodes = self._get_outgoing_nodes(node_id)
            for next_id in next_nodes:
                self._process_node_flow(next_id, visited.copy())

    def _process_action(self, node: DrakonNode):
        """Обробляє ікону 'Действие'"""
        if node.text:
            self._add_line(f"ВИКОНАТИ: {node.text}")
        else:
            self._add_line(f"ВИКОНАТИ: [операція {node.node_id}]")

    def _process_question(self, node: DrakonNode, visited: set):
        """Обробляє ікону 'Вопрос' (if-then-else)"""
        condition = node.text or "умова?"

        self._add_line(f"ЯКЩО ({condition}):")
        self.indent_level += 1

        # Знаходимо гілки ДА і НІ
        yes_edges = [e for e in self.edges if e.source == node.node_id and e.is_yes]
        no_edges = [e for e in self.edges if e.source == node.node_id and e.is_no]

        # Гілка ДА (вниз - царська дорога)
        if yes_edges:
            self._add_line("# [ДА - основний шлях]")
            for edge in yes_edges:
                self._process_node_flow(edge.target, visited.copy())
        else:
            self._add_line("# [порожня гілка ДА]")

        self.indent_level -= 1

        # Гілка НІ (вправо - проблемний шлях згідно принципу "чем правее, тем хуже")
        if no_edges:
            self._add_line("ІНАКШЕ:")
            self.indent_level += 1
            self._add_line("# [НІ - альтернативний/проблемний шлях]")
            for edge in no_edges:
                self._process_node_flow(edge.target, visited.copy())
            self.indent_level -= 1

        self._add_line("КІНЕЦЬ ЯКЩО")

    def _process_select(self, node: DrakonNode, visited: set):
        """Обробляє ікону 'Выбор' (switch-case)"""
        expression = node.text or "вираз"

        self._add_line(f"ВИБРАТИ ({expression}):")
        self.indent_level += 1

        # Знаходимо всі варіанти
        case_edges = [e for e in self.edges if e.source == node.node_id]

        for edge in case_edges:
            if edge.label:
                self._add_line(f"ВАРІАНТ '{edge.label}':")
            else:
                self._add_line(f"ВАРІАНТ default:")

            self.indent_level += 1
            self._process_node_flow(edge.target, visited.copy())
            self.indent_level -= 1

        self.indent_level -= 1
        self._add_line("КІНЕЦЬ ВИБОРУ")

    def _process_for_loop(self, node: DrakonNode, visited: set):
        """Обробляє ікону 'Цикл ДЛЯ'"""
        loop_expr = node.text or "елемент in колекція"

        self._add_line(f"ДЛЯ КОЖНОГО ({loop_expr}):")
        self.indent_level += 1

        # Знаходимо тіло циклу
        body_edges = [e for e in self.edges if e.source == node.node_id and not e.is_backward]

        for edge in body_edges:
            self._process_node_flow(edge.target, visited.copy())

        self.indent_level -= 1
        self._add_line("КІНЕЦЬ ЦИКЛУ ДЛЯ")

    def _process_loop_begin(self, node: DrakonNode, visited: set):
        """Обробляє початок циклу зі стрілкою (while)"""
        condition = node.text or "умова циклу"

        self._add_line(f"ПОКИ ({condition}):")
        self.indent_level += 1

        # Знаходимо тіло циклу
        body_edges = [e for e in self.edges if e.source == node.node_id and not e.is_backward]

        for edge in body_edges:
            self._process_node_flow(edge.target, visited.copy())

        self.indent_level -= 1
        self._add_line("КІНЕЦЬ ЦИКЛУ ПОКИ")

    def _process_address(self, node: DrakonNode):
        """Обробляє ікону 'Адрес' (перехід до ветки)"""
        target_branch = node.text or "ветка"
        self._add_line(f"→ ПЕРЕХІД ДО ВЕТКИ: {target_branch}")

    def _get_outgoing_nodes(self, node_id: str) -> List[str]:
        """Повертає список ID вузлів, до яких є вихідні зв'язки"""
        return [e.target for e in self.edges if e.source == node_id]

    def _add_line(self, text: str):
        """Додає рядок з відступом"""
        indent = "  " * self.indent_level
        self.output.append(f"{indent}{text}")

    def save_to_file(self, output_path: Path):
        """Зберігає псевдокод у файл"""
        pseudocode = self.convert_to_pseudocode()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pseudocode)

        print(f"✅ Псевдокод збережено: {output_path}")
        print(f"📏 Розмір: {output_path.stat().st_size:,} bytes")


# ============================================================================
# CLI
# ============================================================================

def main():
    """Головна функція CLI"""
    if len(sys.argv) < 2:
        print("Використання:")
        print("  python motia-drakon-converter.py <input.json> [-o output.md]")
        print("")
        print("Опції:")
        print("  -o, --output    Шлях до вихідного файлу (за замовчуванням: input_pseudocode.md)")
        print("")
        print("Приклад:")
        print("  python motia-drakon-converter.py diagrams/logic-flow.json -o output/logic-flow.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    # Визначаємо вихідний файл
    if "-o" in sys.argv or "--output" in sys.argv:
        idx = sys.argv.index("-o") if "-o" in sys.argv else sys.argv.index("--output")
        output_file = Path(sys.argv[idx + 1])
    else:
        output_file = input_file.with_name(f"{input_file.stem}_pseudocode.md")

    # Перевіряємо існування вхідного файлу
    if not input_file.exists():
        print(f"❌ Файл не знайдено: {input_file}")
        sys.exit(1)

    print(f"\n🔄 Конвертація ДРАКОН → Псевдокод")
    print(f"📁 Вхід:  {input_file}")
    print(f"📄 Вихід: {output_file}")
    print("")

    # Конвертуємо
    converter = DrakonConverter()

    if not converter.load_from_file(input_file):
        print("❌ Помилка завантаження файлу")
        sys.exit(1)

    converter.save_to_file(output_file)

    print("\n✅ Конвертацію завершено!")


if __name__ == "__main__":
    main()
