"""
AI Code Reviewer
================

AI-powered code review с использованием LLM для анализа качества кода.
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from ..test_generation.llm_client import LLMClient, LLMProvider


class ReviewSeverity(Enum):
    """Серьезность замечания"""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    SUGGESTION = "suggestion"


class ReviewCategory(Enum):
    """Категория замечания"""
    BUG = "bug"
    SECURITY = "security"
    PERFORMANCE = "performance"
    BEST_PRACTICES = "best_practices"
    CODE_STYLE = "code_style"
    MAINTAINABILITY = "maintainability"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


@dataclass
class ReviewComment:
    """Комментарий code review"""
    file: str
    line: int
    severity: ReviewSeverity
    category: ReviewCategory
    message: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "line": self.line,
            "severity": self.severity.value,
            "category": self.category.value,
            "message": self.message,
            "suggestion": self.suggestion,
            "code_snippet": self.code_snippet
        }


@dataclass
class AIReviewResult:
    """Результат AI code review"""
    overall_score: float  # 0-100
    total_comments: int
    critical: int
    major: int
    minor: int
    suggestions: int
    comments: List[ReviewComment] = field(default_factory=list)
    summary: str = ""
    approved: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": self.overall_score,
            "total_comments": self.total_comments,
            "critical": self.critical,
            "major": self.major,
            "minor": self.minor,
            "suggestions": self.suggestions,
            "summary": self.summary,
            "approved": self.approved,
            "comments": [c.to_dict() for c in self.comments]
        }


class AICodeReviewer:
    """
    AI Code Reviewer

    Использует LLM для интеллектуального code review:
    - Поиск багов и логических ошибок
    - Security vulnerabilities
    - Performance issues
    - Best practices violations
    - Code style improvements
    - Suggestions для рефакторинга
    """

    def __init__(
        self,
        llm_provider: LLMProvider = LLMProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        auto_approve_threshold: float = 85.0
    ):
        """
        Инициализация AI reviewer

        Args:
            llm_provider: Провайдер LLM
            model: Модель LLM
            api_key: API ключ
            auto_approve_threshold: Порог для автоматического approve
        """
        self.llm = LLMClient(
            provider=llm_provider,
            model=model,
            api_key=api_key,
            temperature=0.3  # Lower temperature for more consistent reviews
        )
        self.auto_approve_threshold = auto_approve_threshold

    def review_file(
        self,
        file_path: str,
        context: Optional[str] = None
    ) -> AIReviewResult:
        """
        Review одного файла

        Args:
            file_path: Путь к файлу
            context: Дополнительный контекст (цель кода, фреймворк и т.д.)

        Returns:
            Результат review
        """
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Генерируем prompt для LLM
        prompt = self._create_review_prompt(
            code=code,
            file_name=Path(file_path).name,
            context=context
        )

        # Получаем review от LLM
        try:
            review_data = self.llm.generate_json(prompt)
            return self._parse_review_response(review_data, file_path)
        except Exception as e:
            # Fallback: базовый результат при ошибке
            return AIReviewResult(
                overall_score=50.0,
                total_comments=1,
                critical=0,
                major=1,
                minor=0,
                suggestions=0,
                comments=[ReviewComment(
                    file=file_path,
                    line=0,
                    severity=ReviewSeverity.MAJOR,
                    category=ReviewCategory.BUG,
                    message=f"AI Review failed: {str(e)}"
                )],
                summary="AI review failed",
                approved=False
            )

    def review_directory(
        self,
        directory: str,
        pattern: str = "*.py"
    ) -> AIReviewResult:
        """
        Review всех файлов в директории

        Args:
            directory: Путь к директории
            pattern: Glob pattern для поиска файлов

        Returns:
            Агрегированный результат
        """
        dir_path = Path(directory)
        files = list(dir_path.rglob(pattern))

        all_comments = []
        total_score = 0.0

        for file_path in files:
            result = self.review_file(str(file_path))
            all_comments.extend(result.comments)
            total_score += result.overall_score

        avg_score = total_score / len(files) if files else 0.0

        # Подсчет комментариев по severity
        critical = sum(1 for c in all_comments if c.severity == ReviewSeverity.CRITICAL)
        major = sum(1 for c in all_comments if c.severity == ReviewSeverity.MAJOR)
        minor = sum(1 for c in all_comments if c.severity == ReviewSeverity.MINOR)
        suggestions = sum(1 for c in all_comments if c.severity == ReviewSeverity.SUGGESTION)

        return AIReviewResult(
            overall_score=round(avg_score, 1),
            total_comments=len(all_comments),
            critical=critical,
            major=major,
            minor=minor,
            suggestions=suggestions,
            comments=all_comments,
            summary=f"Reviewed {len(files)} files. Average score: {avg_score:.1f}/100",
            approved=(avg_score >= self.auto_approve_threshold and critical == 0)
        )

    def _create_review_prompt(
        self,
        code: str,
        file_name: str,
        context: Optional[str]
    ) -> str:
        """Создание prompt для AI code review"""
        prompt = f"""
Ты — опытный Senior QA Engineer и Code Reviewer. Проведи детальный code review следующего файла.

FILE: {file_name}
{f"CONTEXT: {context}" if context else ""}

CODE:
```python
{code}
```

Проанализируй код на предмет:
1. **Bugs & Logic Errors** - логические ошибки, потенциальные баги
2. **Security Vulnerabilities** - SQL injection, XSS, insecure data handling
3. **Performance Issues** - неэффективные алгоритмы, memory leaks
4. **Best Practices** - нарушения Python/Pytest/Playwright best practices
5. **Code Style** - PEP 8, naming conventions, code readability
6. **Maintainability** - сложность кода, дублирование, необходимость рефакторинга
7. **Testing** - качество тестов, покрытие edge cases
8. **Documentation** - docstrings, комментарии, type hints

Верни результат в JSON формате:
{{
  "overall_score": 85,  // 0-100, где 100 = идеально
  "summary": "Краткое резюме code review",
  "comments": [
    {{
      "line": 42,
      "severity": "critical|major|minor|suggestion",
      "category": "bug|security|performance|best_practices|code_style|maintainability|testing|documentation",
      "message": "Описание проблемы",
      "suggestion": "Как исправить (опционально)",
      "code_snippet": "Проблемный код (опционально)"
    }}
  ]
}}

ВАЖНО:
- Будь конструктивным и helpful
- Давай конкретные suggestions как исправить
- Фокусируйся на реальных проблемах, не придирайся к мелочам
- Для тестов: проверяй покрытие edge cases, assertions, error handling
- Для Playwright: проверяй правильность locators, waits, assertions

Верни ТОЛЬКО валидный JSON, без markdown блоков.
"""
        return prompt

    def _parse_review_response(
        self,
        review_data: Dict[str, Any],
        file_path: str
    ) -> AIReviewResult:
        """Парсинг ответа от LLM"""
        # Парсинг комментариев
        comments = []
        for comment_data in review_data.get("comments", []):
            try:
                severity = ReviewSeverity(comment_data.get("severity", "minor"))
            except ValueError:
                severity = ReviewSeverity.MINOR

            try:
                category = ReviewCategory(comment_data.get("category", "best_practices"))
            except ValueError:
                category = ReviewCategory.BEST_PRACTICES

            comments.append(ReviewComment(
                file=file_path,
                line=comment_data.get("line", 0),
                severity=severity,
                category=category,
                message=comment_data.get("message", ""),
                suggestion=comment_data.get("suggestion"),
                code_snippet=comment_data.get("code_snippet")
            ))

        # Подсчет по severity
        critical = sum(1 for c in comments if c.severity == ReviewSeverity.CRITICAL)
        major = sum(1 for c in comments if c.severity == ReviewSeverity.MAJOR)
        minor = sum(1 for c in comments if c.severity == ReviewSeverity.MINOR)
        suggestions = sum(1 for c in comments if c.severity == ReviewSeverity.SUGGESTION)

        overall_score = review_data.get("overall_score", 50.0)
        approved = (overall_score >= self.auto_approve_threshold and critical == 0)

        return AIReviewResult(
            overall_score=overall_score,
            total_comments=len(comments),
            critical=critical,
            major=major,
            minor=minor,
            suggestions=suggestions,
            comments=comments,
            summary=review_data.get("summary", ""),
            approved=approved
        )

    def generate_report(
        self,
        result: AIReviewResult,
        output_format: str = "markdown"
    ) -> str:
        """
        Генерация отчета code review

        Args:
            result: Результат review
            output_format: Формат отчета (markdown, html, json)

        Returns:
            Форматированный отчет
        """
        if output_format == "json":
            return json.dumps(result.to_dict(), indent=2)

        elif output_format == "markdown":
            return self._generate_markdown_report(result)

        elif output_format == "html":
            return self._generate_html_report(result)

        return str(result.to_dict())

    def _generate_markdown_report(self, result: AIReviewResult) -> str:
        """Markdown отчет"""
        status = "✅ APPROVED" if result.approved else "❌ CHANGES REQUESTED"

        report = f"""# AI Code Review Report

## Summary

**Status:** {status}
**Overall Score:** {result.overall_score}/100

**Issues Found:**
- 🔴 Critical: {result.critical}
- 🟠 Major: {result.major}
- 🟡 Minor: {result.minor}
- 💡 Suggestions: {result.suggestions}
- **Total:** {result.total_comments}

{result.summary}

---

"""

        if result.comments:
            report += "## Detailed Comments\n\n"

            # Group by severity
            for severity in [ReviewSeverity.CRITICAL, ReviewSeverity.MAJOR, ReviewSeverity.MINOR, ReviewSeverity.SUGGESTION]:
                severity_comments = [c for c in result.comments if c.severity == severity]

                if severity_comments:
                    icon = {"critical": "🔴", "major": "🟠", "minor": "🟡", "suggestion": "💡"}
                    report += f"### {icon[severity.value]} {severity.value.title()}\n\n"

                    for comment in severity_comments:
                        report += f"**{Path(comment.file).name}:{comment.line}** - `{comment.category.value}`\n\n"
                        report += f"{comment.message}\n\n"

                        if comment.suggestion:
                            report += f"**💡 Suggestion:**\n```python\n{comment.suggestion}\n```\n\n"

                        report += "---\n\n"

        return report

    def _generate_html_report(self, result: AIReviewResult) -> str:
        """HTML отчет (упрощенный)"""
        # TODO: Implement full HTML report with styling
        return f"<html><body><h1>AI Code Review</h1><p>Score: {result.overall_score}</p></body></html>"
