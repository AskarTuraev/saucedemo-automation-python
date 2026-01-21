"""
Test Executor
=============

Выполнение автотестов с Pytest + Playwright и сбор метрик.
"""

import subprocess
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import structlog

logger = structlog.get_logger()


@dataclass
class TestResult:
    """Результат одного теста"""
    test_id: str
    status: str  # passed, failed, skipped, error
    duration: float
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)
    video: Optional[str] = None


@dataclass
class ExecutionResult:
    """Результат выполнения тестов"""
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    tests: List[TestResult] = field(default_factory=list)
    allure_report_path: Optional[str] = None
    html_report_path: Optional[str] = None

    @property
    def success_rate(self) -> float:
        """Процент успешных тестов"""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "errors": self.errors,
            "duration": self.duration,
            "success_rate": self.success_rate,
            "tests": [
                {
                    "test_id": t.test_id,
                    "status": t.status,
                    "duration": t.duration,
                    "error": t.error_message
                }
                for t in self.tests
            ]
        }


class TestExecutor:
    """
    Test Executor

    Выполнение Pytest тестов с:
    - Parallel execution (pytest-xdist)
    - Allure reporting
    - Structured logging
    - Screenshot/video capture
    - Metrics collection
    """

    def __init__(
        self,
        tests_dir: str,
        workers: int = 4,
        headless: bool = True,
        capture_screenshots: bool = True,
        capture_video: bool = False,
        allure_results_dir: str = "allure-results"
    ):
        """
        Инициализация executor

        Args:
            tests_dir: Директория с тестами
            workers: Количество parallel workers
            headless: Headless режим браузера
            capture_screenshots: Делать скриншоты при failure
            capture_video: Записывать видео
            allure_results_dir: Директория для Allure результатов
        """
        self.tests_dir = Path(tests_dir)
        self.workers = workers
        self.headless = headless
        self.capture_screenshots = capture_screenshots
        self.capture_video = capture_video
        self.allure_results_dir = Path(allure_results_dir)

    def run_tests(
        self,
        test_pattern: str = "test_*.py",
        markers: Optional[List[str]] = None
    ) -> ExecutionResult:
        """
        Запуск тестов

        Args:
            test_pattern: Паттерн для поиска тестов
            markers: Pytest markers для фильтрации

        Returns:
            Результат выполнения
        """
        logger.info("starting_test_execution",
                   tests_dir=str(self.tests_dir),
                   workers=self.workers)

        start_time = time.time()

        # Построение команды pytest
        cmd = self._build_pytest_command(test_pattern, markers)

        # Выполнение
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.tests_dir)
        )

        duration = time.time() - start_time

        # Парсинг результатов
        execution_result = self._parse_results(result, duration)

        logger.info("test_execution_completed",
                   total=execution_result.total,
                   passed=execution_result.passed,
                   failed=execution_result.failed,
                   duration=duration)

        return execution_result

    def _build_pytest_command(
        self,
        test_pattern: str,
        markers: Optional[List[str]]
    ) -> List[str]:
        """Построение команды pytest"""
        cmd = [
            "pytest",
            "-v",
            "--tb=short",
            f"-n{self.workers}",  # parallel execution
            f"--alluredir={self.allure_results_dir}",
            "--json-report",
            "--json-report-file=test-results.json"
        ]

        if self.headless:
            cmd.append("--headed=false")

        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])

        cmd.append(test_pattern)

        return cmd

    def _parse_results(
        self,
        result: subprocess.CompletedProcess,
        duration: float
    ) -> ExecutionResult:
        """Парсинг результатов pytest"""
        # Попытка парсинга JSON отчета
        json_report_path = self.tests_dir / "test-results.json"

        if json_report_path.exists():
            with open(json_report_path, 'r') as f:
                report_data = json.load(f)

            summary = report_data.get("summary", {})
            tests = []

            for test_data in report_data.get("tests", []):
                tests.append(TestResult(
                    test_id=test_data.get("nodeid", ""),
                    status=test_data.get("outcome", "unknown"),
                    duration=test_data.get("duration", 0.0),
                    error_message=test_data.get("call", {}).get("longrepr"),
                    screenshots=[],
                    video=None
                ))

            return ExecutionResult(
                total=summary.get("total", 0),
                passed=summary.get("passed", 0),
                failed=summary.get("failed", 0),
                skipped=summary.get("skipped", 0),
                errors=summary.get("error", 0),
                duration=duration,
                tests=tests,
                allure_report_path=str(self.allure_results_dir)
            )

        # Fallback: парсинг из stdout
        return self._parse_stdout(result.stdout, duration)

    def _parse_stdout(self, stdout: str, duration: float) -> ExecutionResult:
        """Парсинг результатов из stdout"""
        lines = stdout.split("\n")

        passed = failed = skipped = errors = 0

        for line in lines:
            if " passed" in line:
                try:
                    passed = int(line.split()[0])
                except:
                    pass
            if " failed" in line:
                try:
                    failed = int(line.split()[0])
                except:
                    pass

        total = passed + failed + skipped + errors

        return ExecutionResult(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            tests=[]
        )

    def generate_allure_report(self) -> str:
        """Генерация Allure HTML отчета"""
        output_dir = "allure-report"

        cmd = [
            "allure",
            "generate",
            str(self.allure_results_dir),
            "-o",
            output_dir,
            "--clean"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info("allure_report_generated", path=output_dir)
            return output_dir

        logger.error("allure_generation_failed", error=result.stderr)
        return ""
