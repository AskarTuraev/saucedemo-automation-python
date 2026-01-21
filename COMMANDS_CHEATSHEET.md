# 🎯 Шпаргалка по командам

**Все команды для быстрого доступа**

---

## ⚡ Быстрый старт

```bash
# Установка
setup.bat

# Первый тест
quick_test.bat
```

---

## 📦 Установка и настройка

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Установить Playwright
playwright install chromium

# Установить Spacy модель
python -m spacy download en_core_web_sm
```

---

## 🔍 Stage 1: PII Detection

```bash
# Базовая проверка
python -m ai_qa_pipeline.modules.pii_detection.cli requirements.txt -f

# С сохранением результата
python -m ai_qa_pipeline.modules.pii_detection.cli requirements.txt -f -o safe.txt

# С отчетом
python -m ai_qa_pipeline.modules.pii_detection.cli requirements.txt -f -o safe.txt --report

# Разные стратегии маскирования
python -m ai_qa_pipeline.modules.pii_detection.cli file.txt -f -s replace
python -m ai_qa_pipeline.modules.pii_detection.cli file.txt -f -s hash
python -m ai_qa_pipeline.modules.pii_detection.cli file.txt -f -s fake
python -m ai_qa_pipeline.modules.pii_detection.cli file.txt -f -s redact

# Помощь
python -m ai_qa_pipeline.modules.pii_detection.cli --help
```

---

## 🤖 Stage 2: Test Generation

```bash
# С OpenAI
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f -o scenarios.json --llm openai

# С Claude
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f -o scenarios.json --llm anthropic

# С Ollama (локально)
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f -o scenarios.json --llm ollama --model llama2

# Помощь
python -m ai_qa_pipeline.modules.test_generation.cli --help
```

---

## 📝 Stage 3-4: Code Generation

### Полный пайплайн (requirements → code):

```bash
# OpenAI
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output tests

# Ollama
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://app.com --llm ollama --model llama2 --output tests
```

### Пошагово:

```bash
# Шаг 1: Создать JSON contracts
python -m ai_qa_pipeline.modules.code_generation.cli contracts scenarios.json -o contracts.json --base-url https://www.saucedemo.com

# Шаг 2: Сгенерировать код
python -m ai_qa_pipeline.modules.code_generation.cli generate contracts.json -o tests -f playwright

# Помощь
python -m ai_qa_pipeline.modules.code_generation.cli --help
```

---

## 🔍 Stage 5-6: Code Review

```bash
# Static анализ (linting)
python -m ai_qa_pipeline.modules.code_review.cli lint tests/ -o lint-report.json

# AI Code Review
python -m ai_qa_pipeline.modules.code_review.cli ai-review tests/ --llm openai -o ai-review.md

# AI Review в JSON формате
python -m ai_qa_pipeline.modules.code_review.cli ai-review tests/ --llm openai --format json -o review.json

# Полный review (lint + AI)
python -m ai_qa_pipeline.modules.code_review.cli full tests/ --llm openai -o full-review.md

# Помощь
python -m ai_qa_pipeline.modules.code_review.cli --help
```

---

## 🧪 Stage 7: Test Execution

```bash
# Базовый запуск
pytest -v

# С браузером
pytest -v --headed

# С замедлением (для демонстрации)
pytest -v --headed --slowmo=1000

# Параллельный запуск (4 потока)
pytest -v -n4

# С Allure отчетом
pytest -v --alluredir=allure-results

# С JSON отчетом
pytest -v --json-report --json-report-file=results.json

# Полный набор
pytest -v --headed --alluredir=allure-results --json-report --json-report-file=results.json

# Конкретный тест
pytest tests/test_login.py -v

# Конкретная функция
pytest tests/test_login.py::test_successful_login -v
```

---

## 📊 Allure Reports

```bash
# Генерация и просмотр
allure serve allure-results

# Только генерация
allure generate allure-results -o allure-report

# Открыть существующий отчет
allure open allure-report
```

---

## 🔬 Stage 8-9: Log Analysis

```bash
# AI анализ результатов тестов
python -m ai_qa_pipeline.modules.log_analysis.cli results.json -o analysis.md

# С OpenAI
python -m ai_qa_pipeline.modules.log_analysis.cli results.json -o analysis.md --llm openai

# С детальным анализом
python -m ai_qa_pipeline.modules.log_analysis.cli results.json -o analysis.md --llm openai --detailed

# Помощь
python -m ai_qa_pipeline.modules.log_analysis.cli --help
```

---

## 🐛 Stage 10: Bug Reports

```bash
# Генерация баг-репортов
python -m ai_qa_pipeline.modules.bug_reporting.cli results.json -o bug-reports

# В Markdown формате
python -m ai_qa_pipeline.modules.bug_reporting.cli results.json -o bug-reports --format markdown

# В JSON формате
python -m ai_qa_pipeline.modules.bug_reporting.cli results.json -o bug-reports --format json

# С OpenAI
python -m ai_qa_pipeline.modules.bug_reporting.cli results.json -o bug-reports --format markdown --llm openai

# Помощь
python -m ai_qa_pipeline.modules.bug_reporting.cli --help
```

---

## 👁️ Applitools Tests

```bash
# Baseline тест
pytest tests/test_saucedemo_baseline.py -v

# Visual defects тест
pytest tests/test_saucedemo_visual_defects.py -v

# Все Applitools тесты
pytest tests/ -v

# С браузером
pytest tests/ -v --headed
```

---

## 🔧 Полезные команды

```bash
# Проверить версию Python
python --version

# Проверить установленные пакеты
pip list

# Обновить pip
python -m pip install --upgrade pip

# Проверить виртуальное окружение
where python  # должно показать путь в venv

# Выйти из виртуального окружения
deactivate

# Очистить кеш Python
find . -type d -name __pycache__ -exec rm -rf {} +

# Переустановить зависимости
pip install -r requirements.txt --force-reinstall

# Показать дерево файлов
tree /F  # Windows
ls -R    # Linux/Mac
```

---

## 📁 Работа с файлами

```bash
# Посмотреть файл
type filename.txt      # Windows
cat filename.txt       # Linux/Mac

# Создать файл
echo "content" > file.txt

# Добавить в файл
echo "more" >> file.txt

# Копировать файл
copy source.txt dest.txt    # Windows
cp source.txt dest.txt      # Linux/Mac

# Удалить файл
del file.txt               # Windows
rm file.txt                # Linux/Mac

# Показать структуру папки
dir                        # Windows
ls -la                     # Linux/Mac
```

---

## 🌐 Git команды

```bash
# Клонировать репозиторий
git clone https://github.com/AskarTuraev/saucedemo-automation-python.git

# Статус
git status

# Добавить все файлы
git add -A

# Коммит
git commit -m "Message"

# Пуш
git push origin main

# Пулл (обновление)
git pull

# Посмотреть историю
git log --oneline -10

# Создать ветку
git checkout -b feature-name

# Переключиться на ветку
git checkout main
```

---

## 🔑 Проверка .env файла

```bash
# Посмотреть .env
type .env              # Windows
cat .env               # Linux/Mac

# Создать .env
echo OPENAI_API_KEY=sk-your-key > .env

# Проверить что ключ установлен (из Python)
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

---

## 🎬 Команды для демонстрации

### Быстрая демонстрация (5 минут):

```bash
# 1. PII Detection
test_pii.bat

# 2. Full Pipeline
quick_test.bat

# 3. Показать код
type quick_tests\test_login.py

# 4. Запустить тесты
cd quick_tests && pytest -v --headed --slowmo=1000
```

### Полная демонстрация (10 минут):

```bash
# 1. PII Detection
test_pii.bat

# 2. Создать требования
echo "Feature: Login Test
User wants to login with valid credentials" > demo_req.txt

# 3. Полная генерация
python -m ai_qa_pipeline.modules.code_generation.cli full demo_req.txt --base-url https://www.saucedemo.com --llm openai --output demo_tests

# 4. Показать структуру
dir demo_tests

# 5. Показать код
type demo_tests\test_*.py

# 6. AI Code Review
python -m ai_qa_pipeline.modules.code_review.cli full demo_tests --llm openai -o demo_review.md

# 7. Показать review
type demo_review.md

# 8. Запустить тесты
cd demo_tests
pytest -v --headed --slowmo=1000 --alluredir=allure-results --json-report --json-report-file=results.json

# 9. AI анализ (если были failures)
cd ..
python -m ai_qa_pipeline.modules.log_analysis.cli demo_tests\results.json -o demo_analysis.md
type demo_analysis.md

# 10. Генерация баг-репортов
python -m ai_qa_pipeline.modules.bug_reporting.cli demo_tests\results.json -o demo_bugs
dir demo_bugs
type demo_bugs\bug_1.md
```

---

## 🐛 Troubleshooting команды

```bash
# Проверить Python
python --version

# Проверить pip
pip --version

# Проверить Playwright
playwright --version

# Проверить что модули установлены
python -c "import playwright; print('Playwright OK')"
python -c "import pytest; print('Pytest OK')"
python -c "import presidio_analyzer; print('Presidio OK')"

# Переустановить Playwright
pip uninstall playwright -y
pip install playwright
playwright install chromium

# Переустановить все зависимости
pip install -r requirements.txt --force-reinstall

# Очистить pip кеш
pip cache purge
```

---

## 💡 Однострочники (полезные комбинации)

```bash
# Полный цикл от требований до отчета
python -m ai_qa_pipeline.modules.code_generation.cli full req.txt --base-url https://app.com --llm openai --output tests && cd tests && pytest -v --alluredir=allure-results && allure serve allure-results

# PII → Safe → Tests → Run
python -m ai_qa_pipeline.modules.pii_detection.cli req.txt -f -o safe.txt && python -m ai_qa_pipeline.modules.code_generation.cli full safe.txt --base-url https://app.com --llm openai --output tests && cd tests && pytest -v

# Review → Fix → Run
python -m ai_qa_pipeline.modules.code_review.cli full tests --llm openai -o review.md && type review.md && cd tests && pytest -v

# Run → Analyze → Report
cd tests && pytest -v --json-report --json-report-file=results.json && cd .. && python -m ai_qa_pipeline.modules.log_analysis.cli tests\results.json -o analysis.md && python -m ai_qa_pipeline.modules.bug_reporting.cli tests\results.json -o bugs
```

---

## 📋 Чек-лист команд для защиты

Выполните по порядку перед защитой:

```bash
# 1. Проверка окружения
python --version
pip list
playwright --version

# 2. Активация venv
venv\Scripts\activate

# 3. Проверка .env
type .env

# 4. Тест PII (должно работать)
test_pii.bat

# 5. Тест полного пайплайна (должно работать)
quick_test.bat

# 6. Проверка тестов (должны запускаться)
cd quick_tests && pytest -v && cd ..

# 7. Проверка AI review (должен создаться файл)
python -m ai_qa_pipeline.modules.code_review.cli full quick_tests --llm openai -o check_review.md && type check_review.md
```

Если все 7 команд прошли успешно ✅ - вы готовы к защите!

---

## 🎯 Самые важные команды

Если запомните только эти 5 команд - этого достаточно:

```bash
# 1. Установка
setup.bat

# 2. Быстрый тест
quick_test.bat

# 3. Полная генерация
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output tests

# 4. Запуск тестов
cd tests && pytest -v --headed

# 5. Code Review
python -m ai_qa_pipeline.modules.code_review.cli full tests --llm openai -o review.md
```

---

**Сохраните эту шпаргалку - пригодится! 📌**
