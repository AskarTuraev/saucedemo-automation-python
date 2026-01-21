"""
LLM Prompts for Test Generation
================================

Промпты для генерации тест-сценариев через LLM.
"""


REQUIREMENTS_ANALYSIS_PROMPT = """
Ты — опытный QA-инженер и тест-аналитик. Проанализируй следующие бизнес-требования и предоставь структурированный анализ.

БИЗНЕС-ТРЕБОВАНИЯ:
{requirements}

Твоя задача:
1. Определить основную фичу/функцию
2. Выделить user stories (истории пользователей)
3. Определить acceptance criteria (критерии приемки)
4. Найти edge cases (граничные случаи) и потенциальные проблемы
5. Предложить список тест-сценариев для покрытия

Ответь в следующем JSON формате:
{{
  "feature_name": "Название фичи",
  "user_stories": [
    "Как пользователь, я хочу...",
    "Как администратор, я хочу..."
  ],
  "acceptance_criteria": [
    "Система должна...",
    "Пользователь может..."
  ],
  "edge_cases": [
    "Что если пользователь...",
    "Граничный случай когда..."
  ],
  "suggested_scenarios": [
    "Позитивный тест: успешный логин",
    "Негативный тест: логин с неверным паролем",
    "Граничный случай: логин с пустыми полями"
  ]
}}

Верни ТОЛЬКО валидный JSON, без дополнительного текста.
"""


TEST_SCENARIO_GENERATION_PROMPT = """
Ты — опытный QA-автоматизатор. Создай детальный тест-сценарий для следующего случая.

КОНТЕКСТ:
Feature: {feature_name}
Описание фичи: {feature_description}

ТЕСТ-СЦЕНАРИЙ:
{scenario_description}

ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:
{additional_context}

Твоя задача — создать детальный, пошаговый тест-кейс со следующими элементами:
1. Название теста (краткое и понятное)
2. Описание что тестируется
3. Приоритет (critical/high/medium/low)
4. Тип теста (ui/api/e2e/integration)
5. Предусловия (что нужно подготовить)
6. Шаги теста с ожидаемыми результатами
7. Постусловия (cleanup)
8. Теги для категоризации
9. Примерное время выполнения (в секундах)

Верни результат в следующем JSON формате:
{{
  "title": "Test Login with Valid Credentials",
  "description": "Verify that user can successfully login with valid username and password",
  "priority": "critical",
  "test_type": "ui",
  "preconditions": [
    "User account exists in database",
    "Browser is opened",
    "User is on login page"
  ],
  "steps": [
    {{
      "action": "Enter valid username in username field",
      "expected_result": "Username is displayed in the field",
      "test_data": {{"username": "standard_user"}}
    }},
    {{
      "action": "Enter valid password in password field",
      "expected_result": "Password is masked with dots",
      "test_data": {{"password": "secret_sauce"}}
    }},
    {{
      "action": "Click Login button",
      "expected_result": "User is redirected to inventory page, products are visible"
    }}
  ],
  "postconditions": [
    "Logout from application",
    "Clear browser cookies"
  ],
  "tags": ["login", "authentication", "smoke", "regression"],
  "estimated_time": 30
}}

ВАЖНО:
- Шаги должны быть детальными и выполнимыми
- Каждый шаг должен иметь четкий expected_result
- test_data указывать только там где нужны конкретные данные
- Теги должны быть релевантными
- Время в секундах (реалистичное)

Верни ТОЛЬКО валидный JSON, без markdown, без дополнительного текста.
"""


BATCH_SCENARIOS_PROMPT = """
Ты — опытный QA-автоматизатор. Создай набор тест-сценариев для покрытия следующей функциональности.

ФИЧА: {feature_name}

ОПИСАНИЕ:
{feature_description}

СЦЕНАРИИ ДЛЯ СОЗДАНИЯ:
{scenarios_list}

Твоя задача — создать {count} детальных тест-кейсов, покрывающих:
1. Позитивные сценарии (happy path)
2. Негативные сценарии (invalid inputs, error handling)
3. Граничные случаи (edge cases)
4. Регрессионные проверки

Для каждого тест-кейса используй формат:
{{
  "title": "название",
  "description": "описание",
  "priority": "critical|high|medium|low",
  "test_type": "ui|api|e2e|integration",
  "preconditions": ["список предусловий"],
  "steps": [
    {{
      "action": "действие",
      "expected_result": "ожидаемый результат",
      "test_data": {{"key": "value"}}
    }}
  ],
  "postconditions": ["cleanup действия"],
  "tags": ["теги"],
  "estimated_time": секунды
}}

Верни результат как JSON массив тест-кейсов:
{{
  "test_scenarios": [
    {{...}},
    {{...}}
  ]
}}

Верни ТОЛЬКО валидный JSON, без дополнительного текста.
"""


EDGE_CASES_PROMPT = """
Ты — опытный QA-инженер, специализирующийся на поиске багов и граничных случаев.

ФИЧА: {feature_name}
БАЗОВЫЙ СЦЕНАРИЙ: {base_scenario}

Твоя задача — предложить граничные случаи (edge cases) и негативные сценарии, которые могут выявить баги:

1. Граничные значения (boundary values)
2. Некорректные входные данные
3. Неожиданное поведение пользователя
4. Проблемы с производительностью
5. Проблемы с безопасностью
6. Проблемы с совместимостью

Верни список в JSON формате:
{{
  "edge_cases": [
    {{
      "scenario": "Login with SQL injection attempt",
      "description": "Try to login with SQL injection in username field",
      "risk_level": "high",
      "attack_vector": "security"
    }},
    {{
      "scenario": "Login with extremely long username",
      "description": "Enter 10000 characters in username field",
      "risk_level": "medium",
      "attack_vector": "boundary"
    }}
  ]
}}

Верни ТОЛЬКО валидный JSON.
"""


OPTIMIZATION_PROMPT = """
Ты — QA-архитектор. Проанализируй следующий набор тест-сценариев и предложи оптимизацию.

ТЕСТ-СЦЕНАРИИ:
{scenarios_json}

Твоя задача:
1. Найти дублирующиеся шаги
2. Предложить параметризацию похожих тестов
3. Оптимизировать порядок выполнения
4. Выявить тесты которые можно объединить
5. Предложить разделение больших тестов

Верни рекомендации в JSON формате:
{{
  "duplicates": [
    {{
      "tests": ["test1", "test2"],
      "duplicate_steps": ["step description"],
      "suggestion": "Extract to fixture or helper method"
    }}
  ],
  "parametrization": [
    {{
      "tests": ["test1", "test2"],
      "parameter": "user_role",
      "values": ["admin", "user"],
      "suggestion": "Combine into parametrized test"
    }}
  ],
  "optimization_score": 85,
  "total_time_before": 300,
  "total_time_after": 180
}}

Верни ТОЛЬКО валидный JSON.
"""
