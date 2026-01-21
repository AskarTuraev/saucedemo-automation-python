"""
Code Linter
===========

Статический анализ кода с помощью Pylint, Flake8, Mypy, Bandit.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class LintSeverity(Enum):
    """Уровень серьезности проблемы"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    CONVENTION = "convention"
    REFACTOR = "refactor"


@dataclass
class LintIssue:
    """Проблема найденная линтером"""
    file: str
    line: int
    column: int
    severity: LintSeverity
    message: str
    code: str
    source: str  # pylint, flake8, mypy, bandit

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "severity": self.severity.value,
            "message": self.message,
            "code": self.code,
            "source": self.source
        }


@dataclass
class LintResult:
    """Результат линтинга"""
    total_issues: int
    errors: int
    warnings: int
    info: int
    issues: List[LintIssue] = field(default_factory=list)
    score: float = 10.0
    passed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_issues": self.total_issues,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
            "score": self.score,
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues]
        }


class CodeLinter:
    """
    Статический анализатор кода

    Запускает несколько линтеров и агрегирует результаты:
    - Pylint: общий анализ кода
    - Flake8: PEP 8 style guide
    - Mypy: статическая типизация
    - Bandit: security vulnerabilities
    """

    def __init__(
        self,
        enable_pylint: bool = True,
        enable_flake8: bool = True,
        enable_mypy: bool = True,
        enable_bandit: bool = True,
        fail_on_error: bool = True
    ):
        """
        Инициализация линтера

        Args:
            enable_pylint: Включить Pylint
            enable_flake8: Включить Flake8
            enable_mypy: Включить Mypy
            enable_bandit: Включить Bandit
            fail_on_error: Считать ошибки как failure
        """
        self.enable_pylint = enable_pylint
        self.enable_flake8 = enable_flake8
        self.enable_mypy = enable_mypy
        self.enable_bandit = enable_bandit
        self.fail_on_error = fail_on_error

    def lint_file(self, file_path: str) -> LintResult:
        """
        Анализ одного файла

        Args:
            file_path: Путь к Python файлу

        Returns:
            Результат линтинга
        """
        issues = []

        # Pylint
        if self.enable_pylint:
            issues.extend(self._run_pylint(file_path))

        # Flake8
        if self.enable_flake8:
            issues.extend(self._run_flake8(file_path))

        # Mypy
        if self.enable_mypy:
            issues.extend(self._run_mypy(file_path))

        # Bandit
        if self.enable_bandit:
            issues.extend(self._run_bandit(file_path))

        # Агрегация результатов
        return self._aggregate_results(issues)

    def lint_directory(self, directory: str) -> LintResult:
        """
        Анализ директории

        Args:
            directory: Путь к директории с Python файлами

        Returns:
            Агрегированный результат
        """
        dir_path = Path(directory)
        all_issues = []

        # Найти все Python файлы
        python_files = list(dir_path.rglob("*.py"))

        for file_path in python_files:
            result = self.lint_file(str(file_path))
            all_issues.extend(result.issues)

        return self._aggregate_results(all_issues)

    def _run_pylint(self, file_path: str) -> List[LintIssue]:
        """Запуск Pylint"""
        issues = []

        try:
            result = subprocess.run(
                ["pylint", "--output-format=json", file_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout:
                pylint_output = json.loads(result.stdout)

                for item in pylint_output:
                    severity = self._map_pylint_severity(item.get("type", "warning"))
                    issues.append(LintIssue(
                        file=file_path,
                        line=item.get("line", 0),
                        column=item.get("column", 0),
                        severity=severity,
                        message=item.get("message", ""),
                        code=item.get("message-id", ""),
                        source="pylint"
                    ))

        except subprocess.TimeoutExpired:
            issues.append(LintIssue(
                file=file_path,
                line=0,
                column=0,
                severity=LintSeverity.ERROR,
                message="Pylint timeout",
                code="E9999",
                source="pylint"
            ))
        except Exception as e:
            # Pylint не установлен или ошибка
            pass

        return issues

    def _run_flake8(self, file_path: str) -> List[LintIssue]:
        """Запуск Flake8"""
        issues = []

        try:
            result = subprocess.run(
                ["flake8", "--format=json", file_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout:
                try:
                    flake8_output = json.loads(result.stdout)

                    for file, file_issues in flake8_output.items():
                        for issue in file_issues:
                            issues.append(LintIssue(
                                file=file_path,
                                line=issue.get("line_number", 0),
                                column=issue.get("column_number", 0),
                                severity=LintSeverity.WARNING,
                                message=issue.get("text", ""),
                                code=issue.get("code", ""),
                                source="flake8"
                            ))
                except json.JSONDecodeError:
                    # Flake8 может возвращать не-JSON формат
                    pass

        except Exception:
            pass

        return issues

    def _run_mypy(self, file_path: str) -> List[LintIssue]:
        """Запуск Mypy"""
        issues = []

        try:
            result = subprocess.run(
                ["mypy", "--show-column-numbers", "--no-error-summary", file_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout:
                # Парсинг вывода mypy
                for line in result.stdout.split("\n"):
                    if ":" in line and "error:" in line:
                        parts = line.split(":")
                        if len(parts) >= 4:
                            issues.append(LintIssue(
                                file=file_path,
                                line=int(parts[1]) if parts[1].isdigit() else 0,
                                column=int(parts[2]) if parts[2].isdigit() else 0,
                                severity=LintSeverity.ERROR,
                                message=":".join(parts[3:]).strip(),
                                code="mypy",
                                source="mypy"
                            ))

        except Exception:
            pass

        return issues

    def _run_bandit(self, file_path: str) -> List[LintIssue]:
        """Запуск Bandit (security scanner)"""
        issues = []

        try:
            result = subprocess.run(
                ["bandit", "-f", "json", file_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout:
                bandit_output = json.loads(result.stdout)

                for item in bandit_output.get("results", []):
                    severity = self._map_bandit_severity(item.get("issue_severity", "LOW"))
                    issues.append(LintIssue(
                        file=file_path,
                        line=item.get("line_number", 0),
                        column=0,
                        severity=severity,
                        message=f"[Security] {item.get('issue_text', '')}",
                        code=item.get("test_id", ""),
                        source="bandit"
                    ))

        except Exception:
            pass

        return issues

    def _aggregate_results(self, issues: List[LintIssue]) -> LintResult:
        """Агрегация результатов всех линтеров"""
        errors = sum(1 for i in issues if i.severity == LintSeverity.ERROR)
        warnings = sum(1 for i in issues if i.severity == LintSeverity.WARNING)
        info = sum(1 for i in issues if i.severity in [LintSeverity.INFO, LintSeverity.CONVENTION, LintSeverity.REFACTOR])

        # Подсчет score (10.0 - идеально, 0.0 - плохо)
        score = 10.0
        score -= errors * 0.5
        score -= warnings * 0.1
        score -= info * 0.05
        score = max(0.0, score)

        passed = True
        if self.fail_on_error and errors > 0:
            passed = False

        return LintResult(
            total_issues=len(issues),
            errors=errors,
            warnings=warnings,
            info=info,
            issues=issues,
            score=round(score, 2),
            passed=passed
        )

    def _map_pylint_severity(self, pylint_type: str) -> LintSeverity:
        """Маппинг типов Pylint на severity"""
        mapping = {
            "error": LintSeverity.ERROR,
            "warning": LintSeverity.WARNING,
            "convention": LintSeverity.CONVENTION,
            "refactor": LintSeverity.REFACTOR,
            "info": LintSeverity.INFO
        }
        return mapping.get(pylint_type.lower(), LintSeverity.WARNING)

    def _map_bandit_severity(self, bandit_severity: str) -> LintSeverity:
        """Маппинг severity Bandit"""
        mapping = {
            "HIGH": LintSeverity.ERROR,
            "MEDIUM": LintSeverity.WARNING,
            "LOW": LintSeverity.INFO
        }
        return mapping.get(bandit_severity.upper(), LintSeverity.INFO)

    def format_report(self, result: LintResult) -> str:
        """Форматирование отчета линтинга"""
        report = f"""
=== Code Linting Report ===

Score: {result.score}/10.0
Status: {'✓ PASSED' if result.passed else '✗ FAILED'}

Issues Found:
  Errors:   {result.errors}
  Warnings: {result.warnings}
  Info:     {result.info}
  Total:    {result.total_issues}

"""

        if result.issues:
            report += "\nDetailed Issues:\n"
            report += "-" * 80 + "\n"

            # Group by file
            by_file = {}
            for issue in result.issues:
                if issue.file not in by_file:
                    by_file[issue.file] = []
                by_file[issue.file].append(issue)

            for file_path, file_issues in by_file.items():
                report += f"\n{file_path}\n"
                for issue in sorted(file_issues, key=lambda x: x.line):
                    report += f"  Line {issue.line}:{issue.column} [{issue.severity.value}] {issue.code}: {issue.message} ({issue.source})\n"

        return report
