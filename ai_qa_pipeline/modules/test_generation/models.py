"""
Test Scenario Data Models
==========================

Модели данных для тест-сценариев.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


class TestPriority(Enum):
    """Приоритет тест-кейса"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestType(Enum):
    """Тип тестирования"""
    FUNCTIONAL = "functional"
    UI = "ui"
    API = "api"
    INTEGRATION = "integration"
    E2E = "e2e"
    REGRESSION = "regression"
    SMOKE = "smoke"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class TestStep:
    """
    Шаг тест-кейса

    Attributes:
        action: Действие (например, "Открыть страницу логина")
        expected_result: Ожидаемый результат
        test_data: Тестовые данные для этого шага
    """
    action: str
    expected_result: str
    test_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            "action": self.action,
            "expected_result": self.expected_result,
            "test_data": self.test_data
        }


@dataclass
class TestScenario:
    """
    Тест-сценарий

    Attributes:
        title: Название тест-кейса
        description: Описание что тестируется
        priority: Приоритет (critical/high/medium/low)
        test_type: Тип теста
        preconditions: Предусловия
        steps: Список шагов теста
        postconditions: Постусловия (cleanup)
        tags: Теги для категоризации
        estimated_time: Примерное время выполнения (в секундах)
    """
    title: str
    description: str
    priority: TestPriority
    test_type: TestType
    preconditions: List[str] = field(default_factory=list)
    steps: List[TestStep] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    estimated_time: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь для JSON"""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "test_type": self.test_type.value,
            "preconditions": self.preconditions,
            "steps": [step.to_dict() for step in self.steps],
            "postconditions": self.postconditions,
            "tags": self.tags,
            "estimated_time": self.estimated_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestScenario':
        """Создание из словаря"""
        return cls(
            title=data["title"],
            description=data["description"],
            priority=TestPriority(data["priority"]),
            test_type=TestType(data["test_type"]),
            preconditions=data.get("preconditions", []),
            steps=[
                TestStep(**step) for step in data.get("steps", [])
            ],
            postconditions=data.get("postconditions", []),
            tags=data.get("tags", []),
            estimated_time=data.get("estimated_time")
        )


@dataclass
class RequirementsAnalysis:
    """
    Результат анализа требований

    Attributes:
        feature_name: Название фичи/функции
        user_stories: Список user stories
        acceptance_criteria: Критерии приемки
        edge_cases: Граничные случаи
        suggested_scenarios: Предложенные сценарии
    """
    feature_name: str
    user_stories: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    suggested_scenarios: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            "feature_name": self.feature_name,
            "user_stories": self.user_stories,
            "acceptance_criteria": self.acceptance_criteria,
            "edge_cases": self.edge_cases,
            "suggested_scenarios": self.suggested_scenarios
        }
