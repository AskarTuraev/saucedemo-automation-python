"""
PII Detection Pipeline
======================

Полный пайплайн для детекции и маскирования PII перед отправкой в LLM.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from .detector import PIIDetector
from .masker import PIIMasker
from .entities import PIIEntity


class PIIPipeline:
    """
    Пайплайн детекции и маскирования PII

    Объединяет детектор и маскировщик для обработки текстов
    перед отправкой в LLM.
    """

    def __init__(
        self,
        language: str = "en",
        score_threshold: float = 0.5,
        masking_strategy: str = "replace",
        custom_patterns: Dict[str, str] = None
    ):
        """
        Инициализация пайплайна

        Args:
            language: Язык текста
            score_threshold: Порог уверенности детекции
            masking_strategy: Стратегия маскирования
            custom_patterns: Дополнительные паттерны
        """
        self.detector = PIIDetector(
            language=language,
            score_threshold=score_threshold,
            custom_patterns=custom_patterns
        )
        self.masker = PIIMasker(masking_strategy=masking_strategy)

    def process_text(
        self,
        text: str,
        return_entities: bool = False
    ) -> Dict[str, Any]:
        """
        Обработка текста: детекция и маскирование PII

        Args:
            text: Исходный текст
            return_entities: Возвращать ли список сущностей

        Returns:
            Словарь с результатами обработки
        """
        # Детекция PII
        entities = self.detector.detect(text)

        # Маскирование
        masked_text = self.masker.mask(text, entities)

        result = {
            "original_text": text,
            "masked_text": masked_text,
            "pii_found": len(entities) > 0,
            "pii_count": len(entities),
            "pii_types": list(set(e.entity_type.value for e in entities))
        }

        if return_entities:
            result["entities"] = [e.to_dict() for e in entities]

        return result

    def process_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        save_report: bool = True
    ) -> Dict[str, Any]:
        """
        Обработка файла

        Args:
            input_path: Путь к входному файлу
            output_path: Путь для сохранения (опционально)
            save_report: Сохранять ли отчет

        Returns:
            Результаты обработки
        """
        # Читаем файл
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Обрабатываем
        result = self.process_text(content, return_entities=True)

        # Сохраняем замаскированную версию
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result["masked_text"])

        # Сохраняем отчет
        if save_report:
            report_path = Path(input_path).with_suffix('.pii_report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "input_file": input_path,
                    "output_file": output_path,
                    "pii_count": result["pii_count"],
                    "pii_types": result["pii_types"],
                    "entities": result["entities"]
                }, f, indent=2)

        return result

    def process_batch(
        self,
        texts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Пакетная обработка текстов

        Args:
            texts: Список текстов

        Returns:
            Список результатов
        """
        return [self.process_text(text) for text in texts]

    def is_safe_for_llm(self, text: str) -> bool:
        """
        Проверка, безопасен ли текст для отправки в LLM

        Args:
            text: Текст для проверки

        Returns:
            True если PII не обнаружено
        """
        entities = self.detector.detect(text)
        return len(entities) == 0

    def sanitize_for_llm(self, text: str) -> str:
        """
        Подготовка текста для безопасной отправки в LLM

        Args:
            text: Исходный текст

        Returns:
            Замаскированный текст
        """
        result = self.process_text(text)
        return result["masked_text"]
