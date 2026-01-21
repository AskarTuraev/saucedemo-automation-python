"""
Code Generator
==============

Генератор кода автотестов из JSON-контрактов с использованием Jinja2 шаблонов.
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from enum import Enum
from jinja2 import Environment, FileSystemLoader, Template

from .json_contract import TestContract, ActionType, LocatorStrategy


class TestFramework(Enum):
    """Поддерживаемые фреймворки для автотестов"""
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    PYTEST_PLAYWRIGHT = "pytest-playwright"


class CodeGenerator:
    """
    Генератор кода автотестов из JSON-контрактов

    Использует Jinja2 шаблоны для генерации Python кода
    для различных фреймворков (Playwright, Selenium).
    """

    def __init__(
        self,
        framework: TestFramework = TestFramework.PLAYWRIGHT,
        template_dir: Optional[str] = None,
        output_dir: str = "generated_tests"
    ):
        """
        Инициализация генератора

        Args:
            framework: Фреймворк для генерации
            template_dir: Директория с Jinja2 шаблонами
            output_dir: Директория для сохранения сгенерированных тестов
        """
        self.framework = framework
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Настройка Jinja2
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            # Используем встроенные шаблоны
            self.template_dir = Path(__file__).parent / "templates"
            self.template_dir.mkdir(exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Регистрация custom filters
        self.jinja_env.filters['to_python_var'] = self._to_python_var
        self.jinja_env.filters['to_locator'] = self._to_locator

    def generate_test_file(
        self,
        contract: TestContract,
        filename: Optional[str] = None
    ) -> str:
        """
        Генерация файла с тестом из контракта

        Args:
            contract: JSON-контракт теста
            filename: Имя выходного файла (опционально)

        Returns:
            Путь к сгенерированному файлу
        """
        # Определение имени файла
        if not filename:
            filename = f"{contract.test_id}.py"

        # Выбор шаблона в зависимости от фреймворка
        template_name = f"{self.framework.value}_test.py.j2"

        try:
            template = self.jinja_env.get_template(template_name)
        except Exception:
            # Если шаблон не найден, используем встроенный
            template = self._get_default_template()

        # Генерация кода
        code = template.render(
            contract=contract,
            framework=self.framework.value
        )

        # Сохранение файла
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)

        return str(output_path)

    def generate_batch(
        self,
        contracts: List[TestContract]
    ) -> List[str]:
        """
        Генерация нескольких тестов

        Args:
            contracts: Список контрактов

        Returns:
            Список путей к сгенерированным файлам
        """
        generated_files = []
        for contract in contracts:
            file_path = self.generate_test_file(contract)
            generated_files.append(file_path)
        return generated_files

    def generate_page_object(
        self,
        page_name: str,
        locators: Dict[str, str],
        base_url: Optional[str] = None
    ) -> str:
        """
        Генерация Page Object класса

        Args:
            page_name: Название страницы
            locators: Словарь локаторов {element_name: locator}
            base_url: URL страницы

        Returns:
            Путь к сгенерированному файлу
        """
        template_name = f"{self.framework.value}_page_object.py.j2"

        try:
            template = self.jinja_env.get_template(template_name)
        except Exception:
            template = self._get_default_page_object_template()

        code = template.render(
            page_name=page_name,
            locators=locators,
            base_url=base_url,
            framework=self.framework.value
        )

        filename = f"{self._to_python_var(page_name)}_page.py"
        output_path = self.output_dir / "pages" / filename

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)

        return str(output_path)

    def generate_conftest(
        self,
        base_url: str,
        browser: str = "chromium",
        headless: bool = False
    ) -> str:
        """
        Генерация conftest.py для pytest

        Args:
            base_url: Базовый URL приложения
            browser: Браузер (chromium/firefox/webkit)
            headless: Headless режим

        Returns:
            Путь к conftest.py
        """
        template_name = "conftest.py.j2"

        try:
            template = self.jinja_env.get_template(template_name)
        except Exception:
            template = self._get_default_conftest_template()

        code = template.render(
            base_url=base_url,
            browser=browser,
            headless=headless,
            framework=self.framework.value
        )

        output_path = self.output_dir / "conftest.py"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)

        return str(output_path)

    def _to_python_var(self, text: str) -> str:
        """Конвертация текста в валидное Python имя переменной"""
        var_name = text.lower().replace(" ", "_")
        var_name = ''.join(c for c in var_name if c.isalnum() or c == '_')
        return var_name

    def _to_locator(self, locator_dict: Dict[str, str]) -> str:
        """Конвертация локатора в строку для кода"""
        if not locator_dict:
            return '""'

        strategy = locator_dict.get("strategy", "css")
        value = locator_dict.get("value", "")

        if self.framework == TestFramework.PLAYWRIGHT:
            if strategy == "css":
                return f'"{value}"'
            elif strategy == "xpath":
                return f'"xpath={value}"'
            elif strategy == "data-testid":
                return f'\'[data-testid="{value}"]\''
            elif strategy == "text":
                return f'"text={value}"'
            elif strategy == "id":
                return f'"#{value}"'

        return f'"{value}"'

    def _get_default_template(self) -> Template:
        """Встроенный шаблон Playwright теста"""
        template_str = '''"""
{{ contract.test_name }}

{{ contract.description }}
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.{{ contract.test_type }}
@pytest.mark.priority_{{ contract.priority }}
{% for tag in contract.tags %}
@pytest.mark.{{ tag }}
{% endfor %}
def {{ contract.test_id }}(page: Page):
    """{{ contract.description }}"""

    # Preconditions
{% for precondition in contract.preconditions %}
    # {{ precondition }}
{% endfor %}

    # Test steps
{% for action in contract.actions %}
    # {{ action.description }}
{% if action.type == "navigate" %}
    page.goto("{{ action.value }}")
{% elif action.type == "click" %}
    page.locator({{ action.locator | to_locator }}).click()
{% elif action.type == "fill" %}
    page.locator({{ action.locator | to_locator }}).fill("{{ action.value }}")
{% elif action.type == "select" %}
    page.locator({{ action.locator | to_locator }}).select_option("{{ action.value }}")
{% elif action.type == "wait" %}
    page.wait_for_timeout({{ action.value }})
{% elif action.type == "assert" %}
    expect(page.locator({{ action.locator | to_locator }})).to_be_visible()
{% endif %}
{% if action.expected_result %}
    # Expected: {{ action.expected_result }}
{% endif %}

{% endfor %}

    # Postconditions
{% for postcondition in contract.postconditions %}
    # {{ postcondition }}
{% endfor %}
'''
        return Template(template_str)

    def _get_default_page_object_template(self) -> Template:
        """Встроенный шаблон Page Object"""
        template_str = '''"""
{{ page_name }} Page Object

Auto-generated Page Object Model
"""

from playwright.sync_api import Page


class {{ page_name|title }}Page:
    """{{ page_name }} page"""

    def __init__(self, page: Page):
        self.page = page
{% if base_url %}
        self.url = "{{ base_url }}"
{% endif %}

        # Locators
{% for element_name, locator in locators.items() %}
        self.{{ element_name }} = "{{ locator }}"
{% endfor %}

{% if base_url %}
    def navigate(self):
        """Navigate to {{ page_name }} page"""
        self.page.goto(self.url)
{% endif %}

{% for element_name, locator in locators.items() %}
    def get_{{ element_name }}(self):
        """Get {{ element_name }} element"""
        return self.page.locator(self.{{ element_name }})
{% endfor %}
'''
        return Template(template_str)

    def _get_default_conftest_template(self) -> Template:
        """Встроенный шаблон conftest.py"""
        template_str = '''"""
Pytest configuration for generated tests

Auto-generated conftest.py
"""

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context configuration"""
    return {
        "base_url": "{{ base_url }}",
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "videos/" if not {{ headless }} else None
    }


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test"""
    page = browser.new_page()
    yield page
    page.close()
'''
        return Template(template_str)
