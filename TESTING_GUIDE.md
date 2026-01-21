# 🧪 Руководство по тестированию AI-Driven QA Pipeline

**Полная инструкция для самостоятельного запуска и проверки всех 10 этапов**

---

## 📋 Предварительная подготовка

### 1. Проверка окружения

```bash
# Проверьте версии
python --version  # Должно быть 3.12+
pip --version
git --version

# Проверьте что находитесь в правильной директории
cd c:\Users\UserAsk\saucedemo_automation
```

### 2. Создание виртуального окружения

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Вы должны увидеть (venv) перед командной строкой
```

### 3. Установка зависимостей

```bash
# Установить все зависимости
pip install -r requirements.txt

# Установить Playwright браузеры
playwright install chromium

# Установить Spacy модель для PII detection
python -m spacy download en_core_web_sm
```

### 4. Настройка .env файла

```bash
# Создайте файл .env в корне проекта
# Скопируйте и заполните:
```

Создайте файл `.env`:
```env
# OpenAI API (обязательно для полной функциональности)
OPENAI_API_KEY=sk-your-key-here

# Anthropic API (опционально, для альтернативного LLM)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Applitools (опционально, только для visual testing)
APPLITOOLS_API_KEY=your-applitools-key

# Приложение
BASE_URL=https://www.saucedemo.com
BROWSER=chromium
HEADLESS=false

# Тестовые данные
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
```

**Где получить OPENAI_API_KEY:**
1. Зайдите на https://platform.openai.com/
2. Зарегистрируйтесь/войдите
3. Перейдите в API Keys
4. Создайте новый ключ
5. Скопируйте и вставьте в .env

---

## 🎯 Тестирование по этапам

### ✅ Stage 1: PII Detection

**Создайте тестовый файл requirements.txt:**

```bash
# Создайте файл test_requirements.txt
echo "Feature: User Login
As a user I want to login to the system
My email is john.doe@company.com
API Key: sk_live_abc123xyz456
Phone: +1-555-0100" > test_requirements.txt
```

**Запустите PII detection:**

```bash
# Базовый запуск
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f

# С отчетом
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -o safe_requirements.txt -s fake --report

# Проверьте результат
type safe_requirements.txt
```

**Что должно произойти:**
- ✅ Email должен замениться на фейковый (user@example.com)
- ✅ API ключ должен замениться
- ✅ Phone должен остаться или замениться
- ✅ Должен вывестись отчет с найденными PII

**Проверка работоспособности:**
```bash
# Запустите с разными стратегиями
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -s replace
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -s hash
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -s redact
```

---

### ✅ Stage 2: AI Test Generation

**Создайте файл с реальными требованиями:**

```bash
# Создайте demo_requirements.txt
echo "Feature: SauceDemo Login
As a user I want to login to SauceDemo
So that I can access the product catalog

Scenario: Successful login
Given I am on the login page
When I enter username 'standard_user'
And I enter password 'secret_sauce'
And I click login button
Then I should see the inventory page" > demo_requirements.txt
```

**Запустите генерацию сценариев:**

```bash
# С OpenAI (требует API ключ)
python -m ai_qa_pipeline.modules.test_generation.cli demo_requirements.txt -f -o scenarios.json --llm openai

# АЛЬТЕРНАТИВА: С Ollama (бесплатно, но нужно установить)
# Установите Ollama: https://ollama.ai/
# ollama pull llama2
# python -m ai_qa_pipeline.modules.test_generation.cli demo_requirements.txt -f -o scenarios.json --llm ollama --model llama2
```

**Что должно произойти:**
- ✅ Создается файл scenarios.json
- ✅ В консоли выводятся сгенерированные сценарии
- ✅ Каждый сценарий имеет steps и expected results

**Проверьте результат:**
```bash
type scenarios.json
# Должен быть валидный JSON с test scenarios
```

---

### ✅ Stage 3-4: JSON Contracts + Code Generation

**Полный пайплайн (самый простой способ):**

```bash
# Запустите полную генерацию от requirements до кода
python -m ai_qa_pipeline.modules.code_generation.cli full demo_requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests
```

**Что должно произойти:**
- ✅ Создается папка generated_tests/
- ✅ Внутри: test_*.py файлы
- ✅ conftest.py с fixtures
- ✅ pages/ с Page Object классами

**Проверка:**
```bash
dir generated_tests
type generated_tests\test_login_with_valid_credentials.py
```

**Пошаговый подход (для детального контроля):**

```bash
# Шаг 1: Создать JSON contracts
python -m ai_qa_pipeline.modules.code_generation.cli contracts scenarios.json -o contracts.json --base-url https://www.saucedemo.com

# Шаг 2: Проверить contracts
type contracts.json

# Шаг 3: Сгенерировать код
python -m ai_qa_pipeline.modules.code_generation.cli generate contracts.json -o manual_tests -f playwright

# Шаг 4: Проверить результат
dir manual_tests
```

---

### ✅ Stage 5-6: Code Review

**Static Analysis:**

```bash
# Запустите линтинг
python -m ai_qa_pipeline.modules.code_review.cli lint generated_tests -o lint-report.json

# Проверьте отчет
type lint-report.json
```

**AI Code Review:**

```bash
# Запустите AI review
python -m ai_qa_pipeline.modules.code_review.cli ai-review generated_tests --llm openai --format markdown -o ai-review.md

# Просмотрите результат
type ai-review.md
```

**Полный review (static + AI):**

```bash
python -m ai_qa_pipeline.modules.code_review.cli full generated_tests --llm openai -o full-review.md

type full-review.md
```

**Что должно быть в отчете:**
- ✅ Score (обычно 7-9/10)
- ✅ Issues list (warnings, errors)
- ✅ Suggestions for improvement
- ✅ Best practices recommendations

---

### ✅ Stage 7: Test Execution

**Запустите сгенерированные тесты:**

```bash
cd generated_tests

# Базовый запуск (headless)
pytest -v

# С браузером (чтобы видеть что происходит)
pytest -v --headed

# С замедлением (slowmo)
pytest -v --headed --slowmo=1000

# Параллельный запуск
pytest -v -n4

# С Allure отчетом
pytest -v --alluredir=allure-results
```

**Что должно произойти:**
- ✅ Браузер открывается (если --headed)
- ✅ Тесты выполняются
- ✅ В консоли видны результаты
- ✅ Создаются screenshots (при failures)
- ✅ Создается allure-results/

**Просмотр Allure отчета:**

```bash
# Установите Allure (если еще не установлен)
# Скачайте с https://github.com/allure-framework/allure2/releases
# Или через Scoop: scoop install allure

# Сгенерируйте и откройте отчет
allure serve allure-results
```

---

### ✅ Stage 8-9: Log Analysis

**Создайте тестовый файл с results:**

```bash
# Если тесты прошли, results в test-results/
# Если нет, создайте вручную для теста:

echo '{
  "tests": [
    {
      "nodeid": "test_login.py::test_failed_login",
      "outcome": "failed",
      "call": {
        "longrepr": "AssertionError: Element not found: .inventory_list"
      }
    }
  ]
}' > test-results.json
```

**Запустите AI анализ:**

```bash
python -m ai_qa_pipeline.modules.log_analysis.cli test-results.json -o failure-analysis.md --llm openai

# Просмотрите анализ
type failure-analysis.md
```

**Что должно быть в анализе:**
- ✅ Паттерны failures
- ✅ Root cause analysis
- ✅ Рекомендации по исправлению
- ✅ Affected tests list

---

### ✅ Stage 10: Bug Reports

**Сгенерируйте баг-репорты:**

```bash
python -m ai_qa_pipeline.modules.bug_reporting.cli test-results.json -o bug-reports --format markdown --llm openai

# Просмотрите баг-репорты
dir bug-reports
type bug-reports\bug_1.md
```

**Что должно быть в баг-репорте:**
- ✅ Title
- ✅ Severity (Critical, High, Medium, Low)
- ✅ Steps to reproduce
- ✅ Expected vs Actual results
- ✅ Screenshots (если есть)
- ✅ Environment info

---

## 🚀 Запуск оригинальных Applitools тестов

**Baseline тест:**

```bash
# Вернитесь в корневую директорию
cd c:\Users\UserAsk\saucedemo_automation

# Запустите baseline
pytest tests/test_saucedemo_baseline.py -v --headed
```

**Visual defects тест:**

```bash
pytest tests/test_saucedemo_visual_defects.py -v --headed
```

**Все тесты:**

```bash
pytest tests/ -v
```

---

## 🎬 Полный End-to-End тест (все 10 этапов)

**Создайте скрипт для полного теста:**

```bash
# Создайте файл run_full_pipeline.bat
echo @echo off > run_full_pipeline.bat
echo echo "=== Stage 1: PII Detection ===" >> run_full_pipeline.bat
echo python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -o safe_req.txt >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== Stage 2-4: Full Generation ===" >> run_full_pipeline.bat
echo python -m ai_qa_pipeline.modules.code_generation.cli full safe_req.txt --base-url https://www.saucedemo.com --llm openai --output e2e_tests >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== Stage 5-6: Code Review ===" >> run_full_pipeline.bat
echo python -m ai_qa_pipeline.modules.code_review.cli full e2e_tests --llm openai -o e2e_review.md >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== Stage 7: Test Execution ===" >> run_full_pipeline.bat
echo cd e2e_tests >> run_full_pipeline.bat
echo pytest -v --alluredir=allure-results --json-report --json-report-file=test-results.json >> run_full_pipeline.bat
echo cd .. >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== Stage 9: AI Analysis ===" >> run_full_pipeline.bat
echo python -m ai_qa_pipeline.modules.log_analysis.cli e2e_tests/test-results.json -o e2e_analysis.md >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== Stage 10: Bug Reports ===" >> run_full_pipeline.bat
echo python -m ai_qa_pipeline.modules.bug_reporting.cli e2e_tests/test-results.json -o e2e_bugs >> run_full_pipeline.bat
echo. >> run_full_pipeline.bat
echo echo "=== COMPLETE! ===" >> run_full_pipeline.bat

# Запустите
run_full_pipeline.bat
```

---

## 🐛 Troubleshooting

### Проблема: "No module named 'presidio'"

**Решение:**
```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_sm
```

### Проблема: "OpenAI API error"

**Решение:**
1. Проверьте `.env` файл
2. Убедитесь что OPENAI_API_KEY установлен
3. Проверьте баланс на https://platform.openai.com/
4. Альтернатива: используйте `--llm ollama`

### Проблема: "Playwright not installed"

**Решение:**
```bash
playwright install chromium
```

### Проблема: "Import error: ai_qa_pipeline"

**Решение:**
```bash
# Убедитесь что находитесь в корне проекта
cd c:\Users\UserAsk\saucedemo_automation

# Установите в editable mode
pip install -e .
```

### Проблема: "Tests fail with timeout"

**Решение:**
```bash
# Увеличьте timeout
pytest -v --timeout=60

# Или запустите с headed mode чтобы видеть что происходит
pytest -v --headed --slowmo=500
```

---

## ✅ Чек-лист проверки

- [ ] Виртуальное окружение создано и активировано
- [ ] Все зависимости установлены (`pip list`)
- [ ] Playwright браузеры установлены
- [ ] Spacy модель загружена
- [ ] .env файл создан с OPENAI_API_KEY
- [ ] PII Detection работает
- [ ] Test Generation создает scenarios
- [ ] Code Generation создает тесты
- [ ] Code Review выдает отчеты
- [ ] Тесты запускаются
- [ ] AI Analysis работает
- [ ] Bug Reports генерируются
- [ ] Applitools тесты проходят
- [ ] Allure отчеты создаются

---

## 📊 Ожидаемые результаты

### Время выполнения:
- **PII Detection**: 1-2 секунды
- **Test Generation** (1 сценарий): 5-15 секунд
- **Code Generation**: <1 секунда
- **Code Review**: 10-20 секунд/файл
- **Test Execution**: 10-30 секунд/тест
- **AI Analysis**: 5-10 секунд
- **Bug Reports**: 3-5 секунд/баг

### Полный пайплайн: **2-3 минуты**

---

## 🎓 Что показывать на защите

1. **Demo 1: Quick Win**
   ```bash
   python -m ai_qa_pipeline.modules.code_generation.cli full demo_requirements.txt --base-url https://www.saucedemo.com --llm openai --output demo
   cd demo
   pytest -v --headed
   ```

2. **Demo 2: PII Protection**
   ```bash
   # Покажите файл с PII
   type test_requirements.txt
   # Запустите sanitization
   python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -o safe.txt --report
   # Покажите результат
   type safe.txt
   ```

3. **Demo 3: AI Code Review**
   ```bash
   python -m ai_qa_pipeline.modules.code_review.cli full demo --llm openai -o review.md
   type review.md
   ```

---

## 💰 Стоимость тестирования (OpenAI)

- **1 полный цикл**: ~$0.25-0.50
- **10 циклов для тестирования**: ~$2.50-5.00
- **Рекомендация**: Начните с $5-10 на счету

---

## 📞 Если что-то не работает

1. Проверьте [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Проверьте логи в консоли
3. Убедитесь что все зависимости установлены
4. Проверьте что .env файл настроен
5. Попробуйте запустить каждый этап отдельно

---

**Готово! Теперь у вас есть полное руководство для тестирования всей системы.**

**Начните с простого:**
1. PII Detection
2. Один Full Pipeline
3. Запуск сгенерированных тестов

**Удачи! 🚀**
