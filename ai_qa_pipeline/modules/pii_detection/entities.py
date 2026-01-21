"""
PII Entity Definitions
======================

Определение типов персональных данных и их сущностей.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PIIType(Enum):
    """Типы персональных данных для детекции"""
    EMAIL = "EMAIL"
    PHONE = "PHONE_NUMBER"
    CREDIT_CARD = "CREDIT_CARD"
    SSN = "US_SSN"
    PASSPORT = "PASSPORT"
    IP_ADDRESS = "IP_ADDRESS"
    PERSON_NAME = "PERSON"
    ADDRESS = "LOCATION"
    DATE_OF_BIRTH = "DATE_OF_BIRTH"
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"
    API_KEY = "API_KEY"
    ACCESS_TOKEN = "ACCESS_TOKEN"


@dataclass
class PIIEntity:
    """
    Обнаруженная PII сущность

    Attributes:
        entity_type: Тип PII данных
        start: Начальная позиция в тексте
        end: Конечная позиция в тексте
        score: Уверенность детекции (0.0-1.0)
        text: Исходный текст PII
        masked_text: Замаскированный текст
    """
    entity_type: PIIType
    start: int
    end: int
    score: float
    text: str
    masked_text: Optional[str] = None

    def __str__(self) -> str:
        return f"PIIEntity(type={self.entity_type.value}, text='{self.text[:20]}...', score={self.score:.2f})"

    def to_dict(self) -> dict:
        """Конвертация в словарь для JSON"""
        return {
            "type": self.entity_type.value,
            "start": self.start,
            "end": self.end,
            "score": self.score,
            "text": self.text,
            "masked_text": self.masked_text
        }
