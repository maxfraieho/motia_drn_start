#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motia Markdown Service v1.0
============================
Сервіс для інтеграції з Motia-проєктом та Claude CLI.

Автоматична агрегація markdown-файлів для триступеневого процесу генерації:
- Project Context → Pattern Context → Target Step Context

Автор: DevOps Engineer
Версія: 1.0.0
"""

import os
import sys
import json
import shutil
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class MotiaConfig:
    """Конфігурація Motia-сервісу"""
    project_root: Path
    patterns_dir: Path
    steps_dir: Path
    output_dir: Path
    step_descriptions_dir: Path

    # Директорії для ігнорування
    ignore_dirs: set = field(default_factory=lambda: {
        '.git', 'node_modules', 'venv', '__pycache__', '.vscode',
        '.idea', 'dist', 'build', 'target', '.pytest_cache', 'env', '.env'
    })

    # Сервісні файли для виключення
    service_files: set = field(default_factory=lambda: {
        'codetomd.py', 'codetomd.bat', 'drakon_converter.py',
        'md_to_embeddings_service.py', 'md_to_embeddings_service_v4.py',
        'md-to-embeddings-service.bat', 'run_md_service.sh',
        'run_md_service.bat', '.gitignore', 'package-lock.json',
        'yarn.lock', '.DS_Store', 'Thumbs.db'
    })

    # Валідні розширення файлів
    valid_extensions: set = field(default_factory=lambda: {
        '.py', '.js', '.ts', '.html', '.css', '.md', '.txt',
        '.yml', '.yaml', '.json', '.xml', '.sql', '.sh', '.bat',
        '.jsx', '.tsx', '.vue', '.svelte', '.php', '.java', '.cs',
        '.cpp', '.c', '.h', '.hpp', '.rb', '.go', '.rs', '.swift',
        '.drakon'
    })

    @classmethod
    def from_path(cls, project_path: str = ".") -> 'MotiaConfig':
        """Створює конфігурацію з шляху до проєкту"""
        root = Path(project_path).resolve()
        return cls(
            project_root=root,
            patterns_dir=root / "patterns",
            steps_dir=root / "steps",
            output_dir=root / "output",
            step_descriptions_dir=root / "step-descriptions"
        )


# ============================================================================
# MARKDOWN AGGREGATOR CLASS
# ============================================================================

class MarkdownAggregator:
    """
    Клас для агрегації markdown-файлів з структури проєкту.

    Відповідає за:
    - Збір всіх файлів з папок кроків
    - Конвертацію ДРАКОН-схем в markdown
    - Створення єдиного контекстного документа
    """

    def __init__(self, config: MotiaConfig):
        self.config = config
        self.stats = {
            'files_processed': 0,
            'files_skipped': 0,
            'total_size': 0,
            'drakon_converted': 0
        }

    def aggregate_project_context(self, output_file: str = "motia-project-context.md") -> Path:
        """
        Агрегує загальний контекст проєкту (рівень 1).

        Включає:
        - motia.md
        - README.md
        - Структуру проєкту
        - Список доступних патернів
        """
        print("\n📋 Агрегація контексту проєкту...")

        output_path = self.config.output_dir / output_file
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as out:
            # Заголовок
            out.write("# Motia Project Context\n\n")
            out.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"**Project Root**: `{self.config.project_root}`\n\n")
            out.write("---\n\n")

            # Motia.md (основний опис проєкту)
            motia_md = self.config.project_root / "motia.md"
            if motia_md.exists():
                out.write("## Motia Project Description\n\n")
                out.write(motia_md.read_text(encoding='utf-8'))
                out.write("\n\n---\n\n")

            # README
            readme = self.config.project_root / "README.md"
            if readme.exists():
                out.write("## Project README\n\n")
                out.write(readme.read_text(encoding='utf-8'))
                out.write("\n\n---\n\n")

            # Структура проєкту
            out.write("## Project Structure\n\n```\n")
            self._write_tree(out, self.config.project_root, max_depth=3)
            out.write("```\n\n---\n\n")

            # Список патернів
            if self.config.patterns_dir.exists():
                out.write("## Available Patterns\n\n")
                patterns = sorted(self.config.patterns_dir.glob("*.md"))
                for pattern in patterns:
                    if pattern.name != "README.md":
                        out.write(f"- {pattern.stem}\n")
                out.write("\n")

        size = output_path.stat().st_size
        print(f"✅ Створено: {output_path} ({size:,} bytes)")
        return output_path

    def aggregate_pattern_context(self, pattern_name: str,
                                   output_file: Optional[str] = None) -> Path:
        """
        Агрегує контекст патерну (рівень 2).

        Args:
            pattern_name: Назва патерну (наприклад, "factory-pattern")
            output_file: Назва вихідного файлу (опціонально)
        """
        print(f"\n🎯 Агрегація контексту патерну: {pattern_name}...")

        if not output_file:
            output_file = f"motia-pattern-{pattern_name}.md"

        output_path = self.config.output_dir / output_file
        pattern_file = self.config.patterns_dir / f"{pattern_name}.md"

        if not pattern_file.exists():
            raise FileNotFoundError(f"Патерн не знайдено: {pattern_file}")

        with open(output_path, 'w', encoding='utf-8') as out:
            # Заголовок
            out.write(f"# Motia Pattern Context: {pattern_name}\n\n")
            out.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            out.write("---\n\n")

            # Вміст патерну
            out.write(pattern_file.read_text(encoding='utf-8'))
            out.write("\n\n---\n\n")

            # Приклади використання в існуючих кроках
            out.write("## Pattern Usage Examples in Existing Steps\n\n")
            self._find_pattern_usage(out, pattern_name)

        size = output_path.stat().st_size
        print(f"✅ Створено: {output_path} ({size:,} bytes)")
        return output_path

    def aggregate_step_context(self, step_path: str,
                                output_file: Optional[str] = None) -> Path:
        """
        Агрегує контекст кроку (рівень 3).

        Args:
            step_path: Шлях до папки кроку
            output_file: Назва вихідного файлу (опціонально)
        """
        step_dir = Path(step_path).resolve()
        step_name = step_dir.name

        print(f"\n🔧 Агрегація контексту кроку: {step_name}...")

        if not output_file:
            output_file = f"{step_name}-complete.md"

        self.config.step_descriptions_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.config.step_descriptions_dir / output_file

        with open(output_path, 'w', encoding='utf-8') as out:
            # Заголовок
            out.write(f"# Motia Step: {step_name}\n\n")
            out.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"**Step Path**: `{step_dir}`\n\n")
            out.write("---\n\n")

            # Структура кроку
            out.write("## Step Structure\n\n```\n")
            self._write_tree(out, step_dir, prefix="", max_depth=5)
            out.write("```\n\n---\n\n")

            # README
            readme = step_dir / "README.md"
            if readme.exists():
                out.write("## Step Description\n\n")
                out.write(readme.read_text(encoding='utf-8'))
                out.write("\n\n---\n\n")

            # Конфігурація
            self._add_config_files(out, step_dir)

            # Код handler
            self._add_handler_code(out, step_dir)

            # ДРАКОН діаграми
            self._add_drakon_diagrams(out, step_dir)

            # Тести
            self._add_tests(out, step_dir)

            # Статистика
            out.write("---\n\n## Aggregation Statistics\n\n")
            out.write(f"- Files processed: {self.stats['files_processed']}\n")
            out.write(f"- DRAKON diagrams converted: {self.stats['drakon_converted']}\n")
            out.write(f"- Total size: {self.stats['total_size']:,} bytes\n")

        size = output_path.stat().st_size
        print(f"✅ Створено: {output_path} ({size:,} bytes)")
        print(f"📊 Оброблено файлів: {self.stats['files_processed']}")
        print(f"📊 ДРАКОН діаграм: {self.stats['drakon_converted']}")

        return output_path

    def _write_tree(self, out, root_dir: Path, prefix: str = "",
                    max_depth: int = 3, current_depth: int = 0):
        """Записує дерево файлів"""
        if current_depth >= max_depth:
            return

        try:
            items = sorted(root_dir.iterdir())
            dirs = [i for i in items if i.is_dir() and i.name not in self.config.ignore_dirs
                    and not i.name.startswith('.')]
            files = [i for i in items if i.is_file() and i.name not in self.config.service_files
                     and not i.name.startswith('.')]

            # Директорії
            for i, directory in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and not files
                out.write(f"{prefix}{'└── ' if is_last_dir else '├── '}{directory.name}/\n")
                extension = "    " if is_last_dir else "│   "
                self._write_tree(out, directory, prefix + extension, max_depth, current_depth + 1)

            # Файли (максимум 15)
            display_files = files[:15]
            for i, file in enumerate(display_files):
                is_last = i == len(display_files) - 1 and len(files) <= 15
                out.write(f"{prefix}{'└── ' if is_last else '├── '}{file.name}\n")

            if len(files) > 15:
                out.write(f"{prefix}└── ... та ще {len(files) - 15} файлів\n")

        except PermissionError:
            out.write(f"{prefix}└── [Немає доступу]\n")

    def _add_config_files(self, out, step_dir: Path):
        """Додає конфігураційні файли"""
        config_files = ['config.json', 'schema.json']

        for config_file in config_files:
            file_path = step_dir / config_file
            if file_path.exists():
                out.write(f"## {config_file}\n\n")
                out.write("```json\n")
                out.write(file_path.read_text(encoding='utf-8'))
                out.write("\n```\n\n---\n\n")
                self.stats['files_processed'] += 1

    def _add_handler_code(self, out, step_dir: Path):
        """Додає код handler"""
        handlers = list(step_dir.glob("handler.*")) + list(step_dir.glob("*.ts")) + \
                   list(step_dir.glob("*.py"))

        for handler in handlers[:1]:  # Беремо тільки перший знайдений
            if handler.suffix in self.config.valid_extensions:
                out.write(f"## Handler Code: {handler.name}\n\n")

                # Визначаємо мову
                lang_map = {
                    '.ts': 'typescript', '.py': 'python', '.js': 'javascript',
                    '.tsx': 'tsx', '.jsx': 'jsx'
                }
                lang = lang_map.get(handler.suffix, 'text')

                out.write(f"```{lang}\n")
                content = handler.read_text(encoding='utf-8')
                out.write(content)
                out.write("\n```\n\n---\n\n")

                self.stats['files_processed'] += 1
                self.stats['total_size'] += handler.stat().st_size

    def _add_drakon_diagrams(self, out, step_dir: Path):
        """Додає ДРАКОН діаграми з конвертацією"""
        diagrams_dir = step_dir / "diagrams"

        if not diagrams_dir.exists():
            return

        drakon_files = list(diagrams_dir.glob("*.json")) + \
                       list(diagrams_dir.glob("*.drakon"))

        if drakon_files:
            out.write("## DRAKON Diagrams\n\n")

            for drakon_file in drakon_files:
                try:
                    out.write(f"### {drakon_file.name}\n\n")

                    # Конвертуємо ДРАКОН в псевдокод/markdown
                    pseudocode = self._convert_drakon_to_pseudocode(drakon_file)
                    out.write("```\n")
                    out.write(pseudocode)
                    out.write("\n```\n\n")

                    self.stats['drakon_converted'] += 1
                    self.stats['files_processed'] += 1

                except Exception as e:
                    out.write(f"[Помилка конвертації: {e}]\n\n")

            out.write("---\n\n")

    def _convert_drakon_to_pseudocode(self, drakon_file: Path) -> str:
        """
        Конвертує ДРАКОН-схему в псевдокод згідно з описом мови ДРАКОН.

        Враховує:
        - Ікони: Вопрос, Выбор, Цикл ДЛЯ, Действие
        - Візуальні логічні формули
        - Силуети і ветки
        - Принцип "чем правее, тем хуже"
        """
        try:
            with open(drakon_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            pseudocode = []
            pseudocode.append(f"ДРАКОН-схема: {drakon_file.stem}")
            pseudocode.append("=" * 60)
            pseudocode.append("")

            # Обробка вузлів (nodes)
            if 'nodes' in data:
                pseudocode.append("СТРУКТУРА АЛГОРИТМУ:")
                pseudocode.append("")

                for node_id, node_data in data.get('nodes', {}).items():
                    node_type = node_data.get('type', 'unknown')
                    content = node_data.get('content', {})

                    if isinstance(content, dict):
                        text = content.get('txt', '').strip()
                    else:
                        text = str(content).strip()

                    # Інтерпретація згідно ДРАКОН
                    if node_type == 'action':
                        pseudocode.append(f"  ├─ ДЕЙСТ ВІЯ: {text}")

                    elif node_type == 'question':
                        pseudocode.append(f"  ├─ ВОПРОС: {text}?")
                        pseudocode.append(f"  │   ├─ ДА: [перехід вниз]")
                        pseudocode.append(f"  │   └─ НІ: [перехід вправо]")

                    elif node_type == 'loopBegin' or node_type == 'foreach':
                        pseudocode.append(f"  ├─ ЦИКЛ ДЛЯ: {text}")
                        pseudocode.append(f"  │   └─ [тіло циклу]")

                    elif node_type == 'case' or node_type == 'select':
                        pseudocode.append(f"  ├─ ВИБІР: {text}")
                        pseudocode.append(f"  │   └─ [варіанти]")

                    elif node_type == 'branch':
                        pseudocode.append(f"  ├─ ВЕТКА: {text}")

                    elif node_type == 'address':
                        pseudocode.append(f"  └─ АДРЕС: {text}")

                    elif text:
                        pseudocode.append(f"  ├─ {node_type.upper()}: {text}")

            # Обробка зв'язків (edges)
            if 'edges' in data:
                pseudocode.append("")
                pseudocode.append("ПОТІК ВИКОНАННЯ:")
                pseudocode.append("")

                for edge in data.get('edges', []):
                    src = edge.get('src', '?')
                    dst = edge.get('dst', '?')
                    label = edge.get('label', '')

                    if label:
                        pseudocode.append(f"  {src} --[{label}]--> {dst}")
                    else:
                        pseudocode.append(f"  {src} --> {dst}")

            pseudocode.append("")
            pseudocode.append("=" * 60)

            return "\n".join(pseudocode)

        except json.JSONDecodeError:
            return f"[Помилка: неможливо розібрати JSON в {drakon_file.name}]"
        except Exception as e:
            return f"[Помилка конвертації: {e}]"

    def _add_tests(self, out, step_dir: Path):
        """Додає тести"""
        tests_dir = step_dir / "tests"

        if not tests_dir.exists():
            return

        test_files = list(tests_dir.glob("*.ts")) + list(tests_dir.glob("*.py"))

        if test_files:
            out.write("## Tests\n\n")

            for test_file in test_files:
                out.write(f"### {test_file.name}\n\n")

                lang = 'typescript' if test_file.suffix == '.ts' else 'python'
                out.write(f"```{lang}\n")
                out.write(test_file.read_text(encoding='utf-8'))
                out.write("\n```\n\n")

                self.stats['files_processed'] += 1

            out.write("---\n\n")

    def _find_pattern_usage(self, out, pattern_name: str):
        """Шукає використання патерну в існуючих кроках"""
        if not self.config.steps_dir.exists():
            out.write("_Директорія steps/ не знайдена_\n\n")
            return

        found_examples = []

        for step_dir in self.config.steps_dir.iterdir():
            if not step_dir.is_dir():
                continue

            # Шукаємо згадки патерну в README
            readme = step_dir / "README.md"
            if readme.exists():
                content = readme.read_text(encoding='utf-8').lower()
                if pattern_name.lower() in content:
                    found_examples.append(step_dir.name)

        if found_examples:
            out.write("Знайдено використання в кроках:\n\n")
            for example in found_examples:
                out.write(f"- `{example}`\n")
        else:
            out.write("_Приклади використання не знайдені_\n")

        out.write("\n")


# ============================================================================
# ENVIRONMENT DEPLOYER CLASS
# ============================================================================

class EnvironmentDeployer:
    """
    Клас для розгортання робочого середовища Motia.

    Відповідає за:
    - Створення структури директорій
    - Ініціалізацію конфігурацій
    - Підготовку шаблонів
    """

    def __init__(self, config: MotiaConfig):
        self.config = config

    def deploy_structure(self) -> bool:
        """Розгортає базову структуру Motia-проєкту"""
        print("\n🚀 Розгортання структури Motia...")

        try:
            # Створюємо основні директорії
            directories = [
                self.config.patterns_dir,
                self.config.steps_dir,
                self.config.output_dir,
                self.config.step_descriptions_dir
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ {directory.relative_to(self.config.project_root)}/")

            # Створюємо базові конфігурації
            self._create_motia_config()

            print("\n✅ Структура успішно розгорнута!")
            return True

        except Exception as e:
            print(f"❌ Помилка розгортання: {e}")
            return False

    def _create_motia_config(self):
        """Створює базовий конфігураційний файл motia.json"""
        config_file = self.config.project_root / "motia-config.json"

        if config_file.exists():
            print(f"  ⏭️  Конфігурація вже існує: {config_file.name}")
            return

        config_data = {
            "version": "1.0.0",
            "name": self.config.project_root.name,
            "description": "Motia AI-powered project structure",
            "created": datetime.now().isoformat(),
            "directories": {
                "patterns": str(self.config.patterns_dir.relative_to(self.config.project_root)),
                "steps": str(self.config.steps_dir.relative_to(self.config.project_root)),
                "output": str(self.config.output_dir.relative_to(self.config.project_root)),
                "step_descriptions": str(self.config.step_descriptions_dir.relative_to(self.config.project_root))
            }
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        print(f"  ✅ Створено: {config_file.name}")


# ============================================================================
# CLAUDE STEP PREPARATOR CLASS
# ============================================================================

class ClaudeStepPreparator:
    """
    Клас для підготовки контексту для Claude CLI.

    Відповідає за:
    - Триступеневу агрегацію (Project → Pattern → Step)
    - Формування команд для Claude CLI
    - Підготовку промптів
    """

    def __init__(self, config: MotiaConfig, aggregator: MarkdownAggregator):
        self.config = config
        self.aggregator = aggregator

    async def prepare_three_level_context(self, pattern_name: str,
                                          step_path: str) -> Dict[str, Path]:
        """
        Підготовка триступеневого контексту для Claude CLI.

        Args:
            pattern_name: Назва патерну (наприклад, "factory-pattern")
            step_path: Шлях до кроку

        Returns:
            Dict з шляхами до згенерованих контекстних файлів
        """
        print("\n🎯 Підготовка триступеневого контексту для Claude CLI...")
        print("=" * 70)

        contexts = {}

        # Рівень 1: Project Context
        print("\n[1/3] Рівень 1: Project Context")
        contexts['project'] = self.aggregator.aggregate_project_context()

        # Рівень 2: Pattern Context
        print("\n[2/3] Рівень 2: Pattern Context")
        contexts['pattern'] = self.aggregator.aggregate_pattern_context(pattern_name)

        # Рівень 3: Step Context
        print("\n[3/3] Рівень 3: Step Context")
        contexts['step'] = self.aggregator.aggregate_step_context(step_path)

        print("\n" + "=" * 70)
        print("✅ Триступеневий контекст підготовлено!")

        return contexts

    def generate_claude_command(self, contexts: Dict[str, Path],
                                task_description: str = "") -> str:
        """
        Генерує команду для виклику Claude CLI.

        Args:
            contexts: Словник з контекстними файлами
            task_description: Опис задачі для Claude

        Returns:
            Готова команда для виконання
        """
        if not task_description:
            task_description = "Оптимізуй код кроку згідно з патерном та архітектурою проєкту"

        # Формуємо команду для Claude CLI
        cmd_parts = [
            "claude",
            "--context-file", f'"{contexts["project"]}"',
            "--context-file", f'"{contexts["pattern"]}"',
            "--context-file", f'"{contexts["step"]}"',
            "--prompt", f'"{task_description}"'
        ]

        command = " ".join(cmd_parts)

        print("\n📋 Згенерована команда для Claude CLI:")
        print("=" * 70)
        print(command)
        print("=" * 70)

        return command

    async def execute_claude_pipeline(self, pattern_name: str, step_path: str,
                                      task_description: str = "",
                                      auto_execute: bool = False) -> Optional[str]:
        """
        Виконує повний pipeline: агрегація → підготовка → виклик Claude CLI.

        Args:
            pattern_name: Назва патерну
            step_path: Шлях до кроку
            task_description: Опис задачі
            auto_execute: Автоматично виконати команду (за замовчуванням False)

        Returns:
            Результат виконання Claude CLI або None
        """
        # Підготовка контексту
        contexts = await self.prepare_three_level_context(pattern_name, step_path)

        # Генерація команди
        command = self.generate_claude_command(contexts, task_description)

        if not auto_execute:
            print("\n💡 Команду згенеровано. Скопіюйте та виконайте вручну.")
            return None

        # Виконання
        print("\n🚀 Виконання Claude CLI...")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 хвилин timeout
            )

            if result.returncode == 0:
                print("✅ Claude CLI виконано успішно!")
                return result.stdout
            else:
                print(f"❌ Помилка виконання: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("❌ Timeout: Claude CLI не відповів протягом 5 хвилин")
            return None
        except Exception as e:
            print(f"❌ Помилка: {e}")
            return None


# ============================================================================
# CLI MENU
# ============================================================================

def show_menu():
    """Показує головне меню"""
    print("\n" + "=" * 70)
    print("    🤖 MOTIA MARKDOWN SERVICE v1.0 - Claude CLI Integration")
    print("=" * 70)
    print("\n📋 Оберіть варіант:")
    print()
    print("  1. 🚀 Розгорнути структуру Motia-проєкту")
    print("  2. 📋 Агрегувати Project Context (рівень 1)")
    print("  3. 🎯 Агрегувати Pattern Context (рівень 2)")
    print("  4. 🔧 Агрегувати Step Context (рівень 3)")
    print("  5. 🎯 Повний цикл: Триступенева підготовка для Claude CLI")
    print("  6. 🌳 Показати структуру проєкту")
    print("  7. 🚪 Вихід")
    print()
    print("=" * 70)


async def option_5_full_pipeline(config: MotiaConfig):
    """Варіант 5: Повний цикл підготовки для Claude CLI"""
    print("\n🎯 Повний цикл триступеневої підготовки")
    print("=" * 70)

    # Запитуємо параметри
    pattern_name = input("\n📌 Введіть назву патерну (наприклад, factory-pattern): ").strip()
    step_path = input("📁 Введіть шлях до кроку (наприклад, ./steps/my-step): ").strip()
    task = input("📝 Опис задачі для Claude (Enter для стандартного): ").strip()

    if not pattern_name or not step_path:
        print("❌ Патерн та шлях до кроку обов'язкові!")
        return

    # Створюємо інстанси
    aggregator = MarkdownAggregator(config)
    preparator = ClaudeStepPreparator(config, aggregator)

    # Виконуємо pipeline
    await preparator.execute_claude_pipeline(
        pattern_name=pattern_name,
        step_path=step_path,
        task_description=task,
        auto_execute=False  # Не виконуємо автоматично, тільки генеруємо команду
    )

    input("\n✅ Натисніть Enter для продовження...")


async def main():
    """Головна функція"""
    print("\n🚀 Запуск Motia Markdown Service v1.0")
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Визначаємо шлях до проєкту
    project_path = input("\n📁 Введіть шлях до Motia-проєкту (Enter для поточної директорії): ").strip()
    if not project_path:
        project_path = "."

    config = MotiaConfig.from_path(project_path)
    print(f"📁 Робоча директорія: {config.project_root}")

    while True:
        try:
            show_menu()
            choice = input("👉 Ваш вибір (1-7): ").strip()

            if choice == "1":
                deployer = EnvironmentDeployer(config)
                deployer.deploy_structure()
                input("\n✅ Натисніть Enter для продовження...")

            elif choice == "2":
                aggregator = MarkdownAggregator(config)
                aggregator.aggregate_project_context()
                input("\n✅ Натисніть Enter для продовження...")

            elif choice == "3":
                pattern = input("\n📌 Введіть назву патерну: ").strip()
                if pattern:
                    aggregator = MarkdownAggregator(config)
                    aggregator.aggregate_pattern_context(pattern)
                input("\n✅ Натисніть Enter для продовження...")

            elif choice == "4":
                step = input("\n📁 Введіть шлях до кроку: ").strip()
                if step:
                    aggregator = MarkdownAggregator(config)
                    aggregator.aggregate_step_context(step)
                input("\n✅ Натисніть Enter для продовження...")

            elif choice == "5":
                await option_5_full_pipeline(config)

            elif choice == "6":
                print("\n📂 Структура проєкту:")
                print("=" * 70)
                aggregator = MarkdownAggregator(config)
                import io
                buffer = io.StringIO()
                aggregator._write_tree(buffer, config.project_root)
                print(buffer.getvalue())
                input("\n✅ Натисніть Enter для продовження...")

            elif choice == "7":
                print("\n👋 До побачення!")
                print("📊 Дякуємо за використання Motia Markdown Service!")
                break

            else:
                print("\n❌ Невірний вибір! Оберіть число від 1 до 7.")
                input("Натисніть Enter для продовження...")

        except KeyboardInterrupt:
            print("\n\n⚠️ Програму перервано користувачем.")
            print("👋 До побачення!")
            break
        except Exception as e:
            print(f"\n❌ Неочікувана помилка: {e}")
            import traceback
            traceback.print_exc()
            input("Натисніть Enter для продовження...")


if __name__ == "__main__":
    asyncio.run(main())
