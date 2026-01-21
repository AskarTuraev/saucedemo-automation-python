"""
JSON Contract Generator
=======================

Генератор JSON-контрактов тесткейсов для последующей кодогенерации.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum

from ..test_generation.models import TestScenario, TestStep


class ActionType(Enum):
    """Типы действий в тесте"""
    NAVIGATE = "navigate"
    CLICK = "click"
    FILL = "fill"
    SELECT = "select"
    WAIT = "wait"
    ASSERT = "assert"
    API_CALL = "api_call"
    EXECUTE_SCRIPT = "execute_script"
    SCREENSHOT = "screenshot"


class LocatorStrategy(Enum):
    """Стратегии поиска элементов"""
    CSS = "css"
    XPATH = "xpath"
    ID = "id"
    NAME = "name"
    DATA_TESTID = "data-testid"
    TEXT = "text"
    ROLE = "role"


@dataclass
class Locator:
    """Локатор элемента на странице"""
    strategy: LocatorStrategy
    value: str
    timeout: int = 30000

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy.value,
            "value": self.value,
            "timeout": self.timeout
        }


@dataclass
class TestAction:
    """
    Действие в тесте (кликнуть, заполнить и т.д.)

    Attributes:
        type: Тип действия
        description: Описание действия
        locator: Локатор элемента (если нужен)
        value: Значение для заполнения (если нужно)
        expected_result: Ожидаемый результат
        timeout: Таймаут действия (мс)
        screenshot: Делать ли скриншот после действия
    """
    type: ActionType
    description: str
    locator: Optional[Locator] = None
    value: Optional[Any] = None
    expected_result: Optional[str] = None
    timeout: int = 30000
    screenshot: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "description": self.description,
            "locator": self.locator.to_dict() if self.locator else None,
            "value": self.value,
            "expected_result": self.expected_result,
            "timeout": self.timeout,
            "screenshot": self.screenshot
        }


@dataclass
class TestContract:
    """
    JSON-контракт для генерации теста

    Это промежуточный формат между test scenario и финальным кодом.
    Содержит всю необходимую информацию для генерации автотеста.
    """
    # Метаданные
    test_id: str
    test_name: str
    description: str
    priority: str
    test_type: str
    tags: List[str] = field(default_factory=list)

    # Структура теста
    preconditions: List[str] = field(default_factory=list)
    actions: List[TestAction] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)

    # Конфигурация
    framework: str = "playwright"
    browser: str = "chromium"
    headless: bool = False
    viewport: Dict[str, int] = field(default_factory=lambda: {"width": 1920, "height": 1080})

    # Ожидания и таймауты
    timeout: int = 30000
    retry_count: int = 0

    # Дополнительные настройки
    screenshots_on_failure: bool = True
    video_recording: bool = False
    trace: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь для JSON"""
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "description": self.description,
            "priority": self.priority,
            "test_type": self.test_type,
            "tags": self.tags,
            "preconditions": self.preconditions,
            "actions": [action.to_dict() for action in self.actions],
            "postconditions": self.postconditions,
            "framework": self.framework,
            "browser": self.browser,
            "headless": self.headless,
            "viewport": self.viewport,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "screenshots_on_failure": self.screenshots_on_failure,
            "video_recording": self.video_recording,
            "trace": self.trace
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestContract':
        """Создание из словаря"""
        # Парсинг actions
        actions = []
        for action_data in data.get("actions", []):
            locator = None
            if action_data.get("locator"):
                locator = Locator(
                    strategy=LocatorStrategy(action_data["locator"]["strategy"]),
                    value=action_data["locator"]["value"],
                    timeout=action_data["locator"].get("timeout", 30000)
                )

            actions.append(TestAction(
                type=ActionType(action_data["type"]),
                description=action_data["description"],
                locator=locator,
                value=action_data.get("value"),
                expected_result=action_data.get("expected_result"),
                timeout=action_data.get("timeout", 30000),
                screenshot=action_data.get("screenshot", False)
            ))

        return cls(
            test_id=data["test_id"],
            test_name=data["test_name"],
            description=data["description"],
            priority=data["priority"],
            test_type=data["test_type"],
            tags=data.get("tags", []),
            preconditions=data.get("preconditions", []),
            actions=actions,
            postconditions=data.get("postconditions", []),
            framework=data.get("framework", "playwright"),
            browser=data.get("browser", "chromium"),
            headless=data.get("headless", False),
            viewport=data.get("viewport", {"width": 1920, "height": 1080}),
            timeout=data.get("timeout", 30000),
            retry_count=data.get("retry_count", 0),
            screenshots_on_failure=data.get("screenshots_on_failure", True),
            video_recording=data.get("video_recording", False),
            trace=data.get("trace", False)
        )


class JSONContractGenerator:
    """
    Генератор JSON-контрактов из тест-сценариев

    Преобразует TestScenario в TestContract с автоматическим
    определением локаторов и действий.
    """

    def __init__(
        self,
        framework: str = "playwright",
        use_llm_for_locators: bool = True
    ):
        """
        Инициализация генератора

        Args:
            framework: Фреймворк для тестов (playwright/selenium)
            use_llm_for_locators: Использовать LLM для генерации локаторов
        """
        self.framework = framework
        self.use_llm_for_locators = use_llm_for_locators

    def generate_contract(
        self,
        scenario: TestScenario,
        base_url: Optional[str] = None
    ) -> TestContract:
        """
        Генерация контракта из сценария

        Args:
            scenario: Тест-сценарий
            base_url: Базовый URL приложения

        Returns:
            JSON-контракт для кодогенерации
        """
        # Генерация test_id из названия
        test_id = self._generate_test_id(scenario.title)

        # Конвертация шагов в actions
        actions = self._convert_steps_to_actions(scenario.steps, base_url)

        # Создание контракта
        contract = TestContract(
            test_id=test_id,
            test_name=scenario.title,
            description=scenario.description,
            priority=scenario.priority.value,
            test_type=scenario.test_type.value,
            tags=scenario.tags,
            preconditions=scenario.preconditions,
            actions=actions,
            postconditions=scenario.postconditions,
            framework=self.framework
        )

        return contract

    def generate_batch_contracts(
        self,
        scenarios: List[TestScenario],
        base_url: Optional[str] = None
    ) -> List[TestContract]:
        """Генерация контрактов для нескольких сценариев"""
        return [
            self.generate_contract(scenario, base_url)
            for scenario in scenarios
        ]

    def export_to_json(
        self,
        contracts: List[TestContract],
        output_path: str
    ):
        """
        Экспорт контрактов в JSON файл

        Args:
            contracts: Список контрактов
            output_path: Путь для сохранения
        """
        data = {
            "version": "1.0",
            "framework": self.framework,
            "test_contracts": [c.to_dict() for c in contracts],
            "total_tests": len(contracts)
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_from_json(
        self,
        input_path: str
    ) -> List[TestContract]:
        """Импорт контрактов из JSON"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        contracts = []
        for contract_data in data.get("test_contracts", []):
            contracts.append(TestContract.from_dict(contract_data))

        return contracts

    def _generate_test_id(self, title: str) -> str:
        """Генерация test_id из названия"""
        # Убираем специальные символы, заменяем пробелы на underscores
        test_id = title.lower()
        test_id = test_id.replace(" ", "_")
        test_id = ''.join(c for c in test_id if c.isalnum() or c == '_')
        return f"test_{test_id}"

    def _convert_steps_to_actions(
        self,
        steps: List[TestStep],
        base_url: Optional[str]
    ) -> List[TestAction]:
        """
        Конвертация шагов сценария в actions с локаторами

        Args:
            steps: Шаги из TestScenario
            base_url: Базовый URL

        Returns:
            Список TestAction
        """
        actions = []

        for step in steps:
            action_type, locator, value = self._parse_step_action(
                step.action,
                step.test_data
            )

            actions.append(TestAction(
                type=action_type,
                description=step.action,
                locator=locator,
                value=value,
                expected_result=step.expected_result,
                screenshot=False
            ))

        return actions

    def _parse_step_action(
        self,
        action_text: str,
        test_data: Optional[Dict[str, Any]]
    ) -> tuple[ActionType, Optional[Locator], Optional[Any]]:
        """
        Парсинг текста действия и определение типа, локатора и значения

        Args:
            action_text: Текст действия
            test_data: Тестовые данные

        Returns:
            Tuple (ActionType, Locator, value)
        """
        action_lower = action_text.lower()

        # Определение типа действия
        if "navigate" in action_lower or "open" in action_lower or "go to" in action_lower:
            return ActionType.NAVIGATE, None, test_data.get("url") if test_data else None

        elif "click" in action_lower or "press" in action_lower:
            locator = self._infer_locator_from_text(action_text)
            return ActionType.CLICK, locator, None

        elif "enter" in action_lower or "type" in action_lower or "fill" in action_lower or "input" in action_lower:
            locator = self._infer_locator_from_text(action_text)
            value = self._extract_value_from_test_data(test_data, action_text)
            return ActionType.FILL, locator, value

        elif "select" in action_lower or "choose" in action_lower:
            locator = self._infer_locator_from_text(action_text)
            value = self._extract_value_from_test_data(test_data, action_text)
            return ActionType.SELECT, locator, value

        elif "wait" in action_lower:
            return ActionType.WAIT, None, 3000

        elif "verify" in action_lower or "assert" in action_lower or "check" in action_lower:
            locator = self._infer_locator_from_text(action_text)
            return ActionType.ASSERT, locator, None

        else:
            # Default: assume it's a click action
            locator = self._infer_locator_from_text(action_text)
            return ActionType.CLICK, locator, None

    def _infer_locator_from_text(self, text: str) -> Optional[Locator]:
        """
        Автоматическое определение локатора из текста действия

        Args:
            text: Текст действия (например, "Click Login button")

        Returns:
            Locator или None
        """
        # Простые эвристики для определения локатора
        text_lower = text.lower()

        # Проверка на data-testid
        if "login" in text_lower and "button" in text_lower:
            return Locator(LocatorStrategy.DATA_TESTID, "login-button")

        if "username" in text_lower and "field" in text_lower:
            return Locator(LocatorStrategy.DATA_TESTID, "username")

        if "password" in text_lower and "field" in text_lower:
            return Locator(LocatorStrategy.DATA_TESTID, "password")

        # Fallback: попытка извлечь элемент из текста
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ["button", "field", "input", "link"]:
                if i > 0:
                    element_name = words[i-1].lower()
                    return Locator(LocatorStrategy.DATA_TESTID, element_name)

        return None

    def _extract_value_from_test_data(
        self,
        test_data: Optional[Dict[str, Any]],
        action_text: str
    ) -> Optional[Any]:
        """Извлечение значения из тестовых данных"""
        if not test_data:
            return None

        # Если есть только одно значение, возвращаем его
        if len(test_data) == 1:
            return list(test_data.values())[0]

        # Иначе пытаемся найти по ключевым словам
        action_lower = action_text.lower()
        for key, value in test_data.items():
            if key.lower() in action_lower:
                return value

        # Fallback: возвращаем первое значение
        return list(test_data.values())[0] if test_data else None
