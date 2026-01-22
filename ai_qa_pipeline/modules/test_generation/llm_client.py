"""
LLM Client for Test Generation
===============================

Клиент для работы с различными LLM (OpenAI, Anthropic, Ollama).
"""

import json
import os
from typing import Dict, Any, Optional, List
from enum import Enum


class LLMProvider(Enum):
    """Поддерживаемые LLM провайдеры"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class LLMClient:
    """
    Универсальный клиент для работы с LLM

    Поддерживает OpenAI GPT-4, Anthropic Claude, Ollama (локальные модели).
    """

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ):
        """
        Инициализация LLM клиента

        Args:
            provider: Провайдер LLM
            model: Название модели (если None, используется дефолтная)
            api_key: API ключ (если None, берется из ENV)
            temperature: Температура генерации (0.0-1.0)
            max_tokens: Максимум токенов в ответе
        """
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Определяем модель
        if model:
            self.model = model
        else:
            self.model = self._get_default_model()

        # Инициализация клиента в зависимости от провайдера
        if provider == LLMProvider.OPENAI:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

        elif provider == LLMProvider.ANTHROPIC:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

        elif provider == LLMProvider.OLLAMA:
            try:
                import ollama
                self.client = ollama
            except ImportError:
                raise ImportError("ollama-python not installed. Run: pip install ollama-python")

    def _get_default_model(self) -> str:
        """Получение дефолтной модели для провайдера"""
        defaults = {
            LLMProvider.OPENAI: "gpt-4-turbo-preview",
            LLMProvider.ANTHROPIC: "claude-3-opus-20240229",
            LLMProvider.OLLAMA: "llama2"
        }
        return defaults[self.provider]

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        """
        Генерация ответа от LLM

        Args:
            prompt: Пользовательский промпт
            system_prompt: Системный промпт (опционально)
            json_mode: Форсировать JSON ответ

        Returns:
            Ответ от LLM
        """
        if self.provider == LLMProvider.OPENAI:
            return self._generate_openai(prompt, system_prompt, json_mode)

        elif self.provider == LLMProvider.ANTHROPIC:
            return self._generate_anthropic(prompt, system_prompt)

        elif self.provider == LLMProvider.OLLAMA:
            return self._generate_ollama(prompt, system_prompt)

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        json_mode: bool
    ) -> str:
        """Генерация через OpenAI API"""
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> str:
        """Генерация через Anthropic API"""
        messages = [{
            "role": "user",
            "content": prompt
        }]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> str:
        """Генерация через Ollama (локальная модель)"""
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat(
            model=self.model,
            messages=messages
        )

        return response['message']['content']

    def _extract_json_from_text(self, text: str) -> str:
        """
        Извлекает JSON из текста с пояснениями

        Args:
            text: Текст, содержащий JSON

        Returns:
            Чистый JSON строка
        """
        # Пытаемся найти JSON объект или массив
        start = text.find('{')
        if start == -1:
            start = text.find('[')

        if start == -1:
            return text  # Не найдено начало JSON

        # Ищем конец JSON (последнюю закрывающую скобку)
        # Простой подход: берем от первой { до последней }
        end = text.rfind('}')
        if end == -1:
            end = text.rfind(']')

        if end == -1 or end < start:
            return text  # Не найдено корректного конца

        return text[start:end + 1]

    def _fix_incomplete_json(self, json_str: str) -> str:
        """
        Попытка исправить неполный или некорректный JSON ответ от Ollama

        Args:
            json_str: Неполный JSON строка

        Returns:
            Исправленный JSON строка
        """
        # Попытка 1: Исправить структурные ошибки (неправильные скобки)
        fixed = self._fix_bracket_mismatches(json_str)

        # Попытка 2: Добавить недостающие закрывающие скобки
        open_braces = fixed.count('{')
        close_braces = fixed.count('}')
        open_brackets = fixed.count('[')
        close_brackets = fixed.count(']')

        missing_brackets = open_brackets - close_brackets
        missing_braces = open_braces - close_braces

        # Сначала закрываем массивы, потом объекты
        fixed += ']' * missing_brackets
        fixed += '}' * missing_braces

        return fixed

    def _fix_bracket_mismatches(self, json_str: str) -> str:
        """
        Исправляет неправильные типы скобок в JSON

        Например: {...}] вместо {...}}

        Args:
            json_str: JSON строка с возможными ошибками

        Returns:
            Исправленный JSON строка
        """
        stack = []
        result = list(json_str)

        for i, char in enumerate(json_str):
            if char == '{':
                stack.append(('{', i))
            elif char == '[':
                stack.append(('[', i))
            elif char == '}':
                if stack and stack[-1][0] == '{':
                    stack.pop()
                elif stack and stack[-1][0] == '[':
                    # Неправильная скобка: должно быть ] но стоит }
                    # Пропускаем, оставляем как есть
                    pass
            elif char == ']':
                if stack and stack[-1][0] == '[':
                    stack.pop()
                elif stack and stack[-1][0] == '{':
                    # Неправильная скобка: должно быть } но стоит ]
                    # Исправляем на }
                    result[i] = '}'
                    stack.pop()

        return ''.join(result)

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Генерация JSON ответа

        Args:
            prompt: Промпт
            system_prompt: Системный промпт

        Returns:
            Распарсенный JSON объект
        """
        # Добавляем инструкцию про JSON в промпт
        if "JSON" not in prompt:
            prompt += "\n\nВерни ответ ТОЛЬКО в валидном JSON формате, без дополнительного текста."

        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=(self.provider == LLMProvider.OPENAI)
        )

        # Очистка ответа от markdown
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        # Извлекаем чистый JSON из текста (если есть пояснения)
        response = self._extract_json_from_text(response)

        # Парсинг JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Попытка починить неполный JSON от Ollama
            try:
                fixed_response = self._fix_incomplete_json(response)
                return json.loads(fixed_response)
            except (json.JSONDecodeError, ValueError):
                raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {response}")

    def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Пакетная генерация

        Args:
            prompts: Список промптов
            system_prompt: Системный промпт

        Returns:
            Список ответов
        """
        return [
            self.generate(prompt, system_prompt)
            for prompt in prompts
        ]
