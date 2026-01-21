"""
PII Detector
============

Детектор персональных данных с использованием Microsoft Presidio.
"""

import re
from typing import List, Dict, Any
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

from .entities import PIIEntity, PIIType


class PIIDetector:
    """
    Детектор персональных данных (PII)

    Использует Microsoft Presidio для обнаружения различных типов
    персональных данных в текстах перед отправкой в LLM.
    """

    def __init__(
        self,
        language: str = "en",
        score_threshold: float = 0.5,
        custom_patterns: Dict[str, str] = None
    ):
        """
        Инициализация детектора

        Args:
            language: Язык текста для анализа
            score_threshold: Минимальная уверенность для детекции
            custom_patterns: Дополнительные regex паттерны
        """
        self.language = language
        self.score_threshold = score_threshold
        self.custom_patterns = custom_patterns or {}

        # Инициализация Presidio Analyzer
        provider = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
        })

        nlp_engine = provider.create_engine()
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers(nlp_engine=nlp_engine)

        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            registry=registry
        )

        # Добавляем custom recognizers для API ключей, паролей и т.д.
        self._add_custom_recognizers()

    def _add_custom_recognizers(self):
        """Добавление кастомных распознавателей"""
        # API Key patterns
        api_key_patterns = [
            r"(?i)api[_-]?key\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{20,})['\"]?",
            r"(?i)bearer\s+([a-zA-Z0-9_\-\.]{20,})",
            r"(?i)token\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{20,})['\"]?"
        ]

        # Password patterns
        password_patterns = [
            r"(?i)password\s*[:=]\s*['\"]?([^\s'\"]{8,})['\"]?",
            r"(?i)pwd\s*[:=]\s*['\"]?([^\s'\"]{8,})['\"]?"
        ]

        # Сохраняем паттерны для дальнейшего использования
        self.custom_patterns.update({
            "API_KEY": "|".join(api_key_patterns),
            "PASSWORD": "|".join(password_patterns)
        })

    def detect(self, text: str) -> List[PIIEntity]:
        """
        Обнаружение PII в тексте

        Args:
            text: Текст для анализа

        Returns:
            Список обнаруженных PII сущностей
        """
        if not text or not text.strip():
            return []

        # Анализ через Presidio
        results = self.analyzer.analyze(
            text=text,
            language=self.language,
            score_threshold=self.score_threshold
        )

        # Конвертация в PIIEntity объекты
        pii_entities = []
        for result in results:
            try:
                entity_type = PIIType[result.entity_type]
            except KeyError:
                # Если тип не найден в enum, пропускаем
                continue

            entity = PIIEntity(
                entity_type=entity_type,
                start=result.start,
                end=result.end,
                score=result.score,
                text=text[result.start:result.end]
            )
            pii_entities.append(entity)

        # Дополнительная детекция через custom patterns
        custom_entities = self._detect_custom_patterns(text)
        pii_entities.extend(custom_entities)

        # Сортировка по позиции в тексте
        pii_entities.sort(key=lambda e: e.start)

        return pii_entities

    def _detect_custom_patterns(self, text: str) -> List[PIIEntity]:
        """
        Детекция через custom regex паттерны

        Args:
            text: Текст для анализа

        Returns:
            Список обнаруженных сущностей
        """
        entities = []

        for pattern_name, pattern in self.custom_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                # Пытаемся получить тип из enum
                try:
                    entity_type = PIIType[pattern_name]
                except KeyError:
                    continue

                entity = PIIEntity(
                    entity_type=entity_type,
                    start=match.start(),
                    end=match.end(),
                    score=0.9,  # Высокая уверенность для regex
                    text=match.group(0)
                )
                entities.append(entity)

        return entities

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Анализ файла на наличие PII

        Args:
            file_path: Путь к файлу

        Returns:
            Словарь с результатами анализа
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        entities = self.detect(content)

        return {
            "file_path": file_path,
            "total_entities": len(entities),
            "entities_by_type": self._group_by_type(entities),
            "entities": [e.to_dict() for e in entities]
        }

    def _group_by_type(self, entities: List[PIIEntity]) -> Dict[str, int]:
        """Группировка сущностей по типам"""
        grouped = {}
        for entity in entities:
            type_name = entity.entity_type.value
            grouped[type_name] = grouped.get(type_name, 0) + 1
        return grouped
