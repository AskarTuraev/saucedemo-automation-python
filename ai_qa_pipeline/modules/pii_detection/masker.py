"""
PII Masker
==========

Маскировщик персональных данных для безопасной отправки в LLM.
"""

import hashlib
from typing import List, Dict, Optional
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from .entities import PIIEntity, PIIType


class PIIMasker:
    """
    Маскировщик персональных данных

    Заменяет обнаруженные PII на безопасные плейсхолдеры или
    синтетические данные для безопасной работы с LLM.
    """

    def __init__(self, masking_strategy: str = "replace"):
        """
        Инициализация маскировщика

        Args:
            masking_strategy: Стратегия маскирования
                - "replace": замена на <TYPE>
                - "hash": хеширование значения
                - "fake": замена на синтетические данные
                - "redact": полное удаление
        """
        self.masking_strategy = masking_strategy
        self.anonymizer = AnonymizerEngine()

        # Маппинг для восстановления данных (если нужно)
        self.pii_mapping: Dict[str, str] = {}

    def mask(self, text: str, entities: List[PIIEntity]) -> str:
        """
        Маскирование PII в тексте

        Args:
            text: Исходный текст
            entities: Список обнаруженных PII сущностей

        Returns:
            Замаскированный текст
        """
        if not entities:
            return text

        # Сортировка entities в обратном порядке для корректной замены
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)

        masked_text = text
        for entity in sorted_entities:
            # Генерация маски в зависимости от стратегии
            mask = self._generate_mask(entity)

            # Замена в тексте
            masked_text = (
                masked_text[:entity.start] +
                mask +
                masked_text[entity.end:]
            )

            # Обновление entity
            entity.masked_text = mask

            # Сохранение в mapping для возможного восстановления
            self.pii_mapping[mask] = entity.text

        return masked_text

    def _generate_mask(self, entity: PIIEntity) -> str:
        """
        Генерация маски для PII сущности

        Args:
            entity: PII сущность

        Returns:
            Замаскированное значение
        """
        if self.masking_strategy == "replace":
            return f"<{entity.entity_type.value}>"

        elif self.masking_strategy == "hash":
            hash_value = hashlib.sha256(entity.text.encode()).hexdigest()[:16]
            return f"<{entity.entity_type.value}_{hash_value}>"

        elif self.masking_strategy == "fake":
            return self._generate_fake_value(entity.entity_type)

        elif self.masking_strategy == "redact":
            return "[REDACTED]"

        else:
            return f"<{entity.entity_type.value}>"

    def _generate_fake_value(self, pii_type: PIIType) -> str:
        """
        Генерация синтетических данных

        Args:
            pii_type: Тип PII

        Returns:
            Синтетическое значение
        """
        fake_values = {
            PIIType.EMAIL: "user@example.com",
            PIIType.PHONE: "+1-555-0100",
            PIIType.CREDIT_CARD: "4111-1111-1111-1111",
            PIIType.SSN: "123-45-6789",
            PIIType.PERSON_NAME: "John Doe",
            PIIType.ADDRESS: "123 Main St, City, ST 12345",
            PIIType.IP_ADDRESS: "192.0.2.1",
            PIIType.USERNAME: "testuser",
            PIIType.PASSWORD: "TestPass123!",
            PIIType.API_KEY: "sk_test_1234567890abcdef",
            PIIType.ACCESS_TOKEN: "eyJ0eXAiOiJKV1QiLCJhbGc...",
        }

        return fake_values.get(pii_type, f"<{pii_type.value}>")

    def mask_file(
        self,
        input_path: str,
        output_path: str,
        entities: List[PIIEntity]
    ) -> Dict[str, any]:
        """
        Маскирование PII в файле

        Args:
            input_path: Путь к исходному файлу
            output_path: Путь для сохранения замаскированного файла
            entities: Список PII сущностей

        Returns:
            Статистика маскирования
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        masked_content = self.mask(content, entities)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(masked_content)

        return {
            "input_path": input_path,
            "output_path": output_path,
            "total_masked": len(entities),
            "masked_by_type": self._count_by_type(entities)
        }

    def _count_by_type(self, entities: List[PIIEntity]) -> Dict[str, int]:
        """Подсчет сущностей по типам"""
        counts = {}
        for entity in entities:
            type_name = entity.entity_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def unmask(self, masked_text: str) -> str:
        """
        Восстановление оригинального текста (если mapping сохранен)

        Args:
            masked_text: Замаскированный текст

        Returns:
            Восстановленный текст
        """
        unmasked = masked_text
        for mask, original in self.pii_mapping.items():
            unmasked = unmasked.replace(mask, original)
        return unmasked

    def clear_mapping(self):
        """Очистка mapping для безопасности"""
        self.pii_mapping.clear()
