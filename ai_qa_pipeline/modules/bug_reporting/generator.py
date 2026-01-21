"""
Bug Report Generator
====================

Автоматическая генерация баг-репортов с помощью LLM.
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from ..test_generation.llm_client import LLMClient, LLMProvider


@dataclass
class BugReport:
    """Баг-репорт"""
    title: str
    severity: str  # critical, high, medium, low
    priority: str  # P0, P1, P2, P3
    description: str
    steps_to_reproduce: List[str]
    expected_result: str
    actual_result: str
    environment: str
    test_name: str
    error_message: str
    screenshot_paths: List[str]
    video_path: Optional[str] = None

    def to_markdown(self) -> str:
        """Конвертация в Markdown"""
        return f"""# {self.title}

**Severity:** {self.severity}
**Priority:** {self.priority}
**Test:** `{self.test_name}`

## Description
{self.description}

## Steps to Reproduce
{chr(10).join(f'{i}. {step}' for i, step in enumerate(self.steps_to_reproduce, 1))}

## Expected Result
{self.expected_result}

## Actual Result
{self.actual_result}

## Error Message
```
{self.error_message}
```

## Environment
{self.environment}

## Attachments
{chr(10).join(f'- ![Screenshot]({path})' for path in self.screenshot_paths)}
{f'- [Video]({self.video_path})' if self.video_path else ''}

---
*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def to_jira_format(self) -> Dict[str, Any]:
        """Конвертация в формат Jira"""
        return {
            "fields": {
                "project": {"key": "QA"},
                "summary": self.title,
                "description": self.description,
                "issuetype": {"name": "Bug"},
                "priority": {"name": self.priority},
                "labels": ["automated-test", self.severity],
                "customfield_steps": "\n".join(self.steps_to_reproduce),
                "customfield_expected": self.expected_result,
                "customfield_actual": self.actual_result,
                "environment": self.environment
            }
        }


class BugReportGenerator:
    """
    Автоматический генератор баг-репортов

    Создает детальные баг-репорты из:
    - Test failure data
    - Error messages
    - Screenshots
    - Videos
    """

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        environment: str = "Test Environment"
    ):
        """Инициализация генератора"""
        self.llm = LLMClient(
            provider=llm_provider,
            model=model,
            api_key=api_key,
            temperature=0.5
        )
        self.environment = environment

    def generate_from_test_failure(
        self,
        test_name: str,
        error_message: str,
        test_steps: Optional[List[str]] = None,
        screenshot_paths: Optional[List[str]] = None,
        video_path: Optional[str] = None
    ) -> BugReport:
        """
        Генерация баг-репорта из failure

        Args:
            test_name: Название теста
            error_message: Сообщение об ошибке
            test_steps: Шаги теста (если есть)
            screenshot_paths: Пути к скриншотам
            video_path: Путь к видео

        Returns:
            Сгенерированный баг-репорт
        """
        # Создаем prompt для LLM
        prompt = self._create_bug_report_prompt(
            test_name, error_message, test_steps
        )

        # Генерируем репорт через LLM
        bug_data = self.llm.generate_json(prompt)

        return BugReport(
            title=bug_data.get("title", f"Bug in {test_name}"),
            severity=bug_data.get("severity", "medium"),
            priority=bug_data.get("priority", "P2"),
            description=bug_data.get("description", ""),
            steps_to_reproduce=bug_data.get("steps_to_reproduce", test_steps or []),
            expected_result=bug_data.get("expected_result", ""),
            actual_result=bug_data.get("actual_result", ""),
            environment=self.environment,
            test_name=test_name,
            error_message=error_message,
            screenshot_paths=screenshot_paths or [],
            video_path=video_path
        )

    def generate_batch(
        self,
        test_results_json: str
    ) -> List[BugReport]:
        """
        Генерация баг-репортов для всех failures

        Args:
            test_results_json: Путь к JSON с результатами тестов

        Returns:
            Список баг-репортов
        """
        with open(test_results_json, 'r') as f:
            results = json.load(f)

        bug_reports = []

        for test in results.get("tests", []):
            if test.get("outcome") in ["failed", "error"]:
                report = self.generate_from_test_failure(
                    test_name=test.get("nodeid", ""),
                    error_message=test.get("call", {}).get("longrepr", ""),
                    test_steps=[]
                )
                bug_reports.append(report)

        return bug_reports

    def _create_bug_report_prompt(
        self,
        test_name: str,
        error_message: str,
        test_steps: Optional[List[str]]
    ) -> str:
        """Создание prompt для генерации баг-репорта"""
        steps_info = ""
        if test_steps:
            steps_info = f"\n\nTest Steps:\n" + "\n".join(f"{i}. {step}" for i, step in enumerate(test_steps, 1))

        prompt = f"""
Создай детальный баг-репорт на основе failed автотеста.

TEST NAME: {test_name}

ERROR MESSAGE:
{error_message}
{steps_info}

Создай профессиональный баг-репорт в формате JSON:
{{
  "title": "Краткое название бага (30-50 символов)",
  "severity": "critical|high|medium|low",
  "priority": "P0|P1|P2|P3",
  "description": "Детальное описание проблемы",
  "steps_to_reproduce": [
    "Шаг 1",
    "Шаг 2",
    "Шаг 3"
  ],
  "expected_result": "Что должно было произойти",
  "actual_result": "Что произошло на самом деле"
}}

Критерии severity:
- critical: система не работает, блокирует основной функционал
- high: серьезная проблема, но есть workaround
- medium: проблема заметна пользователю
- low: косметический дефект

Верни ТОЛЬКО валидный JSON.
"""
        return prompt

    def export_to_github_issues(
        self,
        bug_reports: List[BugReport],
        repo: str,
        token: str
    ):
        """Создание GitHub Issues из баг-репортов"""
        # TODO: Implement GitHub API integration
        pass

    def export_to_jira(
        self,
        bug_reports: List[BugReport],
        jira_url: str,
        credentials: Dict[str, str]
    ):
        """Создание Jira Issues из баг-репортов"""
        # TODO: Implement Jira API integration
        pass
