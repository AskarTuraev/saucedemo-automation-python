"""
Code Generation Module
======================

Модуль для автоматической генерации кода автотестов из JSON-контрактов.
"""

from .json_contract import JSONContractGenerator, TestContract
from .code_generator import CodeGenerator, TestFramework

__all__ = [
    'JSONContractGenerator',
    'TestContract',
    'CodeGenerator',
    'TestFramework'
]
