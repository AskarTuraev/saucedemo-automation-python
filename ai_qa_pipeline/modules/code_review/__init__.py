"""
Code Review Module
==================

Модуль для статического анализа и AI-ревью сгенерированного кода.
"""

from .linter import CodeLinter, LintResult
from .ai_reviewer import AICodeReviewer, ReviewComment, ReviewSeverity

__all__ = [
    'CodeLinter',
    'LintResult',
    'AICodeReviewer',
    'ReviewComment',
    'ReviewSeverity'
]
