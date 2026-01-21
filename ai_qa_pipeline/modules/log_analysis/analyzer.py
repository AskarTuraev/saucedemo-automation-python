"""
AI Log Analyzer
===============

Анализ логов и отчетов с помощью LLM для выявления root cause failures.
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

from ..test_generation.llm_client import LLMClient, LLMProvider


@dataclass
class FailurePattern:
    """Паттерн failure обнаруженный в логах"""
    pattern_type: str  # timeout, assertion, network, element_not_found, etc.
    frequency: int
    affected_tests: List[str]
    root_cause: str
    suggestion: str


@dataclass
class AnalysisResult:
    """Результат анализа логов"""
    total_failures: int
    unique_patterns: int
    patterns: List[FailurePattern] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_failures": self.total_failures,
            "unique_patterns": self.unique_patterns,
            "patterns": [
                {
                    "type": p.pattern_type,
                    "frequency": p.frequency,
                    "affected_tests": p.affected_tests,
                    "root_cause": p.root_cause,
                    "suggestion": p.suggestion
                }
                for p in self.patterns
            ],
            "root_causes": self.root_causes,
            "recommendations": self.recommendations,
            "summary": self.summary
        }


class LogAnalyzer:
    """
    AI Log Analyzer

    Анализирует:
    - Test failures и их причины
    - Повторяющиеся паттерны ошибок
    - Network/timeout issues
    - Element locator problems
    - Assertion failures
    - Environment issues
    """

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """Инициализация analyzer"""
        self.llm = LLMClient(
            provider=llm_provider,
            model=model,
            api_key=api_key,
            temperature=0.3
        )

    def analyze_test_results(
        self,
        test_results_json: str
    ) -> AnalysisResult:
        """
        Анализ результатов тестов из JSON

        Args:
            test_results_json: Путь к JSON файлу с результатами

        Returns:
            Результат анализа
        """
        # Загрузка результатов
        with open(test_results_json, 'r') as f:
            results = json.load(f)

        # Извлечение failures
        failures = []
        for test in results.get("tests", []):
            if test.get("outcome") in ["failed", "error"]:
                failures.append({
                    "test_id": test.get("nodeid"),
                    "error": test.get("call", {}).get("longrepr", ""),
                    "duration": test.get("duration", 0)
                })

        if not failures:
            return AnalysisResult(
                total_failures=0,
                unique_patterns=0,
                summary="No failures detected"
            )

        # AI анализ failures
        prompt = self._create_analysis_prompt(failures)
        analysis = self.llm.generate_json(prompt)

        return self._parse_analysis(analysis, len(failures))

    def analyze_logs(
        self,
        log_file: str
    ) -> AnalysisResult:
        """Анализ лог-файла"""
        with open(log_file, 'r') as f:
            logs = f.read()

        # Извлечение ошибок из логов
        errors = self._extract_errors_from_logs(logs)

        if not errors:
            return AnalysisResult(
                total_failures=0,
                unique_patterns=0,
                summary="No errors found in logs"
            )

        # AI анализ
        prompt = f"""
Проанализируй следующие ошибки из логов тестов:

{json.dumps(errors, indent=2)}

Определи:
1. Паттерны ошибок (timeout, assertion, network, element not found, etc.)
2. Root cause для каждого паттерна
3. Рекомендации по исправлению

Верни JSON:
{{
  "patterns": [
    {{
      "type": "timeout",
      "frequency": 5,
      "affected_tests": ["test1", "test2"],
      "root_cause": "Slow page load",
      "suggestion": "Increase timeout or optimize page"
    }}
  ],
  "root_causes": ["Root cause 1", "Root cause 2"],
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "summary": "Overall summary"
}}
"""

        analysis = self.llm.generate_json(prompt)
        return self._parse_analysis(analysis, len(errors))

    def _create_analysis_prompt(self, failures: List[Dict[str, Any]]) -> str:
        """Создание prompt для анализа"""
        prompt = f"""
Ты — опытный QA-инженер. Проанализируй следующие failures из автотестов:

{json.dumps(failures, indent=2)}

Твоя задача:
1. Определить паттерны ошибок (группировка похожих failures)
2. Найти root cause для каждого паттерна
3. Предложить решения

Категории паттернов:
- timeout: элемент не появился вовремя
- assertion: ожидаемое != фактическое
- element_not_found: локатор не найден
- network: проблемы с сетью/API
- environment: проблемы окружения
- data: проблемы с тестовыми данными

Верни JSON:
{{
  "patterns": [
    {{
      "type": "timeout",
      "frequency": 3,
      "affected_tests": ["test_login", "test_checkout"],
      "root_cause": "Page load too slow, default timeout insufficient",
      "suggestion": "Increase page.goto timeout to 60s or optimize page performance"
    }}
  ],
  "root_causes": [
    "Main root cause 1",
    "Main root cause 2"
  ],
  "recommendations": [
    "Actionable recommendation 1",
    "Actionable recommendation 2"
  ],
  "summary": "Overall summary of failures and main issues"
}}

ВАЖНО: Будь конкретным, давай actionable recommendations.
"""
        return prompt

    def _parse_analysis(
        self,
        analysis: Dict[str, Any],
        total_failures: int
    ) -> AnalysisResult:
        """Парсинг результатов анализа"""
        patterns = []

        for pattern_data in analysis.get("patterns", []):
            patterns.append(FailurePattern(
                pattern_type=pattern_data.get("type", "unknown"),
                frequency=pattern_data.get("frequency", 1),
                affected_tests=pattern_data.get("affected_tests", []),
                root_cause=pattern_data.get("root_cause", ""),
                suggestion=pattern_data.get("suggestion", "")
            ))

        return AnalysisResult(
            total_failures=total_failures,
            unique_patterns=len(patterns),
            patterns=patterns,
            root_causes=analysis.get("root_causes", []),
            recommendations=analysis.get("recommendations", []),
            summary=analysis.get("summary", "")
        )

    def _extract_errors_from_logs(self, logs: str) -> List[Dict[str, str]]:
        """Извлечение ошибок из текстовых логов"""
        errors = []
        lines = logs.split("\n")

        for i, line in enumerate(lines):
            if "ERROR" in line or "FAILED" in line or "Exception" in line:
                # Собираем контекст (3 строки до и после)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 4)
                context = "\n".join(lines[context_start:context_end])

                errors.append({
                    "line_number": i + 1,
                    "error_line": line,
                    "context": context
                })

        return errors

    def generate_report(self, result: AnalysisResult) -> str:
        """Генерация markdown отчета"""
        report = f"""# Test Failure Analysis Report

## Summary
{result.summary}

**Total Failures:** {result.total_failures}
**Unique Patterns:** {result.unique_patterns}

---

## Failure Patterns

"""

        for pattern in result.patterns:
            report += f"""### {pattern.pattern_type.upper()} ({pattern.frequency} occurrences)

**Root Cause:** {pattern.root_cause}

**Affected Tests:**
{chr(10).join(f'- {test}' for test in pattern.affected_tests)}

**💡 Suggestion:**
{pattern.suggestion}

---

"""

        if result.root_causes:
            report += "\n## Main Root Causes\n\n"
            for i, cause in enumerate(result.root_causes, 1):
                report += f"{i}. {cause}\n"

        if result.recommendations:
            report += "\n## Recommendations\n\n"
            for i, rec in enumerate(result.recommendations, 1):
                report += f"{i}. {rec}\n"

        return report
