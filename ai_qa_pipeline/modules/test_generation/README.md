# Test Scenario Generation Module

AI-powered генератор тест-сценариев из бизнес-требований с использованием LLM (GPT-4, Claude, Ollama).

## Возможности

- ✅ Автоматический анализ бизнес-требований
- ✅ Генерация детальных тест-кейсов с шагами
- ✅ Поддержка multiple LLM (OpenAI GPT-4, Anthropic Claude, Ollama)
- ✅ Генерация граничных случаев и негативных сценариев
- ✅ Оптимизация набора тест-кейсов
- ✅ Экспорт в JSON для последующей кодогенерации
- ✅ CLI интерфейс

## Установка

```bash
# С OpenAI GPT-4
pip install openai

# Или с Anthropic Claude
pip install anthropic

# Или с локальной Ollama
pip install ollama-python
```

## Использование

### Python API

```python
from ai_qa_pipeline.modules.test_generation import TestScenarioGenerator
from ai_qa_pipeline.modules.test_generation.llm_client import LLMProvider

# Инициализация с OpenAI
generator = TestScenarioGenerator(
    llm_provider=LLMProvider.OPENAI,
    model="gpt-4-turbo-preview",
    api_key="sk-..."
)

# Бизнес-требования
requirements = """
Как пользователь, я хочу иметь возможность войти в систему
с помощью email и пароля, чтобы получить доступ к защищенному контенту.

Acceptance Criteria:
- Форма логина должна содержать поля email и password
- Email должен быть валидным
- После успешного логина пользователь перенаправляется на dashboard
- При неверных данных показывается ошибка
"""

# 1. Анализ требований
analysis = generator.analyze_requirements(requirements)
print(f"Feature: {analysis.feature_name}")
print(f"Suggested scenarios: {len(analysis.suggested_scenarios)}")

# 2. Генерация тест-сценариев
scenarios = generator.generate_from_requirements(requirements)

for scenario in scenarios:
    print(f"\n{scenario.title}")
    print(f"  Priority: {scenario.priority.value}")
    print(f"  Steps: {len(scenario.steps)}")
    print(f"  Time: {scenario.estimated_time}s")

# 3. Экспорт в JSON
generator.export_to_json(scenarios, "test_scenarios.json")
```

### CLI

```bash
# Полная генерация из файла требований
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f -o scenarios.json

# Анализ без генерации
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f --analyze-only

# Генерация граничных случаев
python -m ai_qa_pipeline.modules.test_generation.cli "Login Feature" --edge-cases "Login with valid credentials"

# Оптимизация существующих сценариев
python -m ai_qa_pipeline.modules.test_generation.cli dummy --optimize existing_scenarios.json

# Использование Claude вместо GPT-4
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -p anthropic --api-key "sk-..."

# Использование локальной Ollama
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -p ollama -m llama2
```

## Пример сгенерированного сценария

```json
{
  "title": "Test Login with Valid Credentials",
  "description": "Verify that user can successfully login with valid email and password",
  "priority": "critical",
  "test_type": "ui",
  "preconditions": [
    "User account exists in database",
    "Browser is opened",
    "User is on login page"
  ],
  "steps": [
    {
      "action": "Enter valid email in email field",
      "expected_result": "Email is displayed in the field",
      "test_data": {"email": "user@example.com"}
    },
    {
      "action": "Enter valid password in password field",
      "expected_result": "Password is masked with dots",
      "test_data": {"password": "SecurePass123!"}
    },
    {
      "action": "Click Login button",
      "expected_result": "User is redirected to dashboard, welcome message is visible"
    }
  ],
  "postconditions": [
    "Logout from application",
    "Clear browser cookies"
  ],
  "tags": ["login", "authentication", "smoke", "critical"],
  "estimated_time": 45
}
```

## Поддерживаемые LLM

### OpenAI (Recommended)
```python
generator = TestScenarioGenerator(
    llm_provider=LLMProvider.OPENAI,
    model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo"
    api_key=os.getenv("OPENAI_API_KEY")
)
```

**Преимущества**: Лучшее качество, JSON mode, быстрая генерация
**Стоимость**: ~$0.01-0.03 per 1K tokens

### Anthropic Claude
```python
generator = TestScenarioGenerator(
    llm_provider=LLMProvider.ANTHROPIC,
    model="claude-3-opus-20240229",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

**Преимущества**: Длинный контекст, хорошее качество
**Стоимость**: ~$0.015-0.075 per 1K tokens

### Ollama (Local)
```python
generator = TestScenarioGenerator(
    llm_provider=LLMProvider.OLLAMA,
    model="llama2"  # or "codellama", "mistral"
)
```

**Преимущества**: Бесплатно, приватность, офлайн работа
**Недостатки**: Медленнее, качество ниже, требует GPU

## Workflow Integration

### 1. Requirements → Scenarios → JSON Contracts → Code

```python
from ai_qa_pipeline.modules.test_generation import TestScenarioGenerator
from ai_qa_pipeline.modules.code_generation import CodeGenerator

# Step 1: Generate scenarios from requirements
generator = TestScenarioGenerator()
scenarios = generator.generate_from_requirements(requirements_text)

# Step 2: Export to JSON
generator.export_to_json(scenarios, "scenarios.json")

# Step 3: Generate code (next module)
code_gen = CodeGenerator()
test_files = code_gen.generate_from_json("scenarios.json")
```

### 2. Edge Cases & Negative Testing

```python
# Генерация граничных случаев
edge_cases = generator.suggest_edge_cases(
    feature_name="User Login",
    base_scenario="Login with valid credentials"
)

# Результат:
# - Login with SQL injection
# - Login with extremely long password
# - Login with special characters
# - Login with empty fields
# - Concurrent login attempts
```

### 3. Scenario Optimization

```python
# Оптимизация дублирующихся тестов
optimization = generator.optimize_scenarios(scenarios)

# Результат:
# - Duplicate steps detection
# - Parametrization suggestions
# - Execution order optimization
# - Time reduction recommendations
```

## Advanced Features

### Custom Test Data Generation

```python
scenario = scenarios[0]
test_data = generator.generate_test_data(
    scenario=scenario,
    data_type="valid"  # or "invalid", "boundary"
)

print(test_data)
# {"email": "test@example.com", "password": "SecurePass123!"}
```

### Batch Processing

```python
requirements_list = [
    "Login feature requirements",
    "Registration feature requirements",
    "Password reset requirements"
]

all_scenarios = []
for req in requirements_list:
    scenarios = generator.generate_from_requirements(req)
    all_scenarios.extend(scenarios)

print(f"Total scenarios: {len(all_scenarios)}")
```

### Integration with PII Detection

```python
from ai_qa_pipeline.modules.pii_detection import PIIPipeline

# Sanitize requirements before sending to LLM
pii_pipeline = PIIPipeline()
safe_requirements = pii_pipeline.sanitize_for_llm(requirements)

# Generate scenarios from sanitized requirements
scenarios = generator.generate_from_requirements(safe_requirements)
```

## Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
```

### Custom Configuration

```python
from ai_qa_pipeline.modules.test_generation import TestScenarioGenerator
from ai_qa_pipeline.modules.test_generation.llm_client import LLMClient

# Custom LLM client
custom_llm = LLMClient(
    provider=LLMProvider.OPENAI,
    model="gpt-4",
    temperature=0.5,  # Lower = more deterministic
    max_tokens=3000
)

generator = TestScenarioGenerator()
generator.llm = custom_llm
```

## Best Practices

1. **Clear Requirements**: Чем детальнее требования, тем лучше сценарии
2. **PII Protection**: Всегда используйте PII detection для production данных
3. **Review Generated**: Проверяйте сгенерированные сценарии перед использованием
4. **Iterative Refinement**: Используйте edge cases и optimization для улучшения
5. **Version Control**: Храните JSON сценарии в git для трекинга изменений

## Testing

```bash
pytest ai_qa_pipeline/modules/test_generation/tests/ -v
```

## Troubleshooting

### Error: "JSON parsing failed"
- LLM вернул невалидный JSON
- Решение: Увеличьте temperature или смените модель

### Error: "API key not found"
- API ключ не установлен
- Решение: Установите через ENV или параметр api_key

### Low Quality Scenarios
- Недостаточно контекста в требованиях
- Решение: Добавьте примеры, acceptance criteria, edge cases

## Performance

- Время генерации: ~5-15 секунд per scenario
- Batch генерация: ~30-60 секунд for 10 scenarios
- Стоимость: ~$0.01-0.05 per scenario (OpenAI GPT-4)

## Roadmap

- [ ] Fine-tuned модели для QA domain
- [ ] Интеграция с Jira/TestRail
- [ ] Visual scenario designer
- [ ] Multi-language support
- [ ] Scenario versioning & diff

## License

MIT
