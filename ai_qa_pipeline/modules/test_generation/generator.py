"""
Test Scenario Generator
=======================

Генератор тест-сценариев из бизнес-требований с помощью LLM.
"""

import json
from typing import List, Optional, Dict, Any
from pathlib import Path

from .llm_client import LLMClient, LLMProvider
from .models import TestScenario, RequirementsAnalysis, TestPriority, TestType, TestStep
from .prompts import (
    REQUIREMENTS_ANALYSIS_PROMPT,
    TEST_SCENARIO_GENERATION_PROMPT,
    BATCH_SCENARIOS_PROMPT,
    EDGE_CASES_PROMPT,
    OPTIMIZATION_PROMPT
)


class TestScenarioGenerator:
    """
    Генератор тест-сценариев с помощью LLM

    Преобразует бизнес-требования в детальные тест-кейсы.
    """

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Инициализация генератора

        Args:
            llm_provider: Провайдер LLM (OpenAI/Anthropic/Ollama)
            model: Конкретная модель (опционально)
            api_key: API ключ (опционально, можно в ENV)
        """
        self.llm = LLMClient(
            provider=llm_provider,
            model=model,
            api_key=api_key,
            temperature=0.7
        )

    def analyze_requirements(
        self,
        requirements: str
    ) -> RequirementsAnalysis:
        """
        Анализ бизнес-требований

        Args:
            requirements: Текст бизнес-требований

        Returns:
            Структурированный анализ требований
        """
        prompt = REQUIREMENTS_ANALYSIS_PROMPT.format(
            requirements=requirements
        )

        response = self.llm.generate_json(prompt)

        return RequirementsAnalysis(
            feature_name=response.get("feature_name", ""),
            user_stories=response.get("user_stories", []),
            acceptance_criteria=response.get("acceptance_criteria", []),
            edge_cases=response.get("edge_cases", []),
            suggested_scenarios=response.get("suggested_scenarios", [])
        )

    def generate_scenario(
        self,
        feature_name: str,
        feature_description: str,
        scenario_description: str,
        additional_context: str = ""
    ) -> TestScenario:
        """
        Генерация одного тест-сценария

        Args:
            feature_name: Название фичи
            feature_description: Описание фичи
            scenario_description: Описание сценария
            additional_context: Дополнительный контекст

        Returns:
            Сгенерированный тест-сценарий
        """
        prompt = TEST_SCENARIO_GENERATION_PROMPT.format(
            feature_name=feature_name,
            feature_description=feature_description,
            scenario_description=scenario_description,
            additional_context=additional_context
        )

        response = self.llm.generate_json(prompt)

        # Конвертация в TestScenario объект
        return self._parse_scenario(response)

    def generate_batch_scenarios(
        self,
        feature_name: str,
        feature_description: str,
        scenarios_list: List[str],
        count: Optional[int] = None
    ) -> List[TestScenario]:
        """
        Генерация нескольких тест-сценариев

        Args:
            feature_name: Название фичи
            feature_description: Описание фичи
            scenarios_list: Список названий сценариев
            count: Количество сценариев (если None, по списку)

        Returns:
            Список тест-сценариев
        """
        if count is None:
            count = len(scenarios_list)

        scenarios_text = "\n".join(f"- {s}" for s in scenarios_list)

        prompt = BATCH_SCENARIOS_PROMPT.format(
            feature_name=feature_name,
            feature_description=feature_description,
            scenarios_list=scenarios_text,
            count=count
        )

        response = self.llm.generate_json(prompt)

        # Парсим массив сценариев
        scenarios = []
        for scenario_data in response.get("test_scenarios", []):
            scenarios.append(self._parse_scenario(scenario_data))

        return scenarios

    def generate_from_requirements(
        self,
        requirements: str
    ) -> List[TestScenario]:
        """
        Полный цикл: анализ требований + генерация сценариев

        Args:
            requirements: Бизнес-требования

        Returns:
            Список тест-сценариев
        """
        # 1. Анализируем требования
        analysis = self.analyze_requirements(requirements)

        # 2. Генерируем сценарии на основе анализа
        scenarios = self.generate_batch_scenarios(
            feature_name=analysis.feature_name,
            feature_description=requirements,
            scenarios_list=analysis.suggested_scenarios
        )

        return scenarios

    def suggest_edge_cases(
        self,
        feature_name: str,
        base_scenario: str
    ) -> List[Dict[str, Any]]:
        """
        Генерация граничных случаев и негативных сценариев

        Args:
            feature_name: Название фичи
            base_scenario: Базовый сценарий

        Returns:
            Список граничных случаев
        """
        prompt = EDGE_CASES_PROMPT.format(
            feature_name=feature_name,
            base_scenario=base_scenario
        )

        response = self.llm.generate_json(prompt)
        return response.get("edge_cases", [])

    def optimize_scenarios(
        self,
        scenarios: List[TestScenario]
    ) -> Dict[str, Any]:
        """
        Анализ и оптимизация набора сценариев

        Args:
            scenarios: Список тест-сценариев

        Returns:
            Рекомендации по оптимизации
        """
        scenarios_json = json.dumps(
            [s.to_dict() for s in scenarios],
            indent=2
        )

        prompt = OPTIMIZATION_PROMPT.format(
            scenarios_json=scenarios_json
        )

        return self.llm.generate_json(prompt)

    def export_to_json(
        self,
        scenarios: List[TestScenario],
        output_path: str
    ):
        """
        Экспорт сценариев в JSON файл

        Args:
            scenarios: Список сценариев
            output_path: Путь для сохранения
        """
        data = {
            "test_scenarios": [s.to_dict() for s in scenarios],
            "total_count": len(scenarios),
            "total_estimated_time": sum(
                s.estimated_time or 0 for s in scenarios
            )
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_from_json(
        self,
        input_path: str
    ) -> List[TestScenario]:
        """
        Импорт сценариев из JSON файла

        Args:
            input_path: Путь к JSON файлу

        Returns:
            Список тест-сценариев
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        scenarios = []
        for scenario_data in data.get("test_scenarios", []):
            scenarios.append(TestScenario.from_dict(scenario_data))

        return scenarios

    def _parse_scenario(self, data: Dict[str, Any]) -> TestScenario:
        """
        Парсинг JSON в TestScenario объект

        Args:
            data: JSON данные

        Returns:
            TestScenario объект
        """
        # Парсинг шагов
        steps = []
        for step_data in data.get("steps", []):
            steps.append(TestStep(
                action=step_data.get("action", ""),
                expected_result=step_data.get("expected_result", ""),
                test_data=step_data.get("test_data")
            ))

        # Парсинг приоритета
        priority_str = data.get("priority", "medium").lower()
        try:
            priority = TestPriority[priority_str.upper()]
        except KeyError:
            priority = TestPriority.MEDIUM

        # Парсинг типа теста
        test_type_str = data.get("test_type", "functional").lower()
        try:
            test_type = TestType[test_type_str.upper()]
        except KeyError:
            test_type = TestType.FUNCTIONAL

        return TestScenario(
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=priority,
            test_type=test_type,
            preconditions=data.get("preconditions", []),
            steps=steps,
            postconditions=data.get("postconditions", []),
            tags=data.get("tags", []),
            estimated_time=data.get("estimated_time")
        )

    def generate_test_data(
        self,
        scenario: TestScenario,
        data_type: str = "valid"
    ) -> Dict[str, Any]:
        """
        Генерация тестовых данных для сценария

        Args:
            scenario: Тест-сценарий
            data_type: Тип данных (valid/invalid/boundary)

        Returns:
            Тестовые данные
        """
        prompt = f"""
        Сгенерируй {data_type} тестовые данные для следующего тест-кейса:

        Название: {scenario.title}
        Описание: {scenario.description}
        Шаги: {json.dumps([s.to_dict() for s in scenario.steps], indent=2)}

        Верни JSON объект с тестовыми данными для каждого поля/параметра.

        Пример:
        {{
          "username": "test_user",
          "password": "SecurePass123!",
          "email": "test@example.com"
        }}

        Верни ТОЛЬКО валидный JSON.
        """

        return self.llm.generate_json(prompt)
