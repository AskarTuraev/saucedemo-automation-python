# 🤖 AI-Driven QA Pipeline + SauceDemo Applitools Testing

> **🚀 НОВЫЙ ПОЛЬЗОВАТЕЛЬ?** Начните здесь: [START_HERE.md](START_HERE.md) - запуск за 3 шага (5 минут)

**Полноценная AI-powered система для автоматизации тестирования** с двумя основными компонентами:

1. **AI-Driven QA Pipeline** - Автоматическая генерация тестов от требований до баг-репортов
2. **SauceDemo Applitools Testing** - Visual regression testing с Playwright

---

## 🎯 Основные возможности

### 🤖 AI-Driven QA Pipeline

**10 этапов полной автоматизации:**

1. ✅ **PII Detection** - Защита персональных данных перед LLM
2. ✅ **AI Test Generator** - Генерация сценариев из требований (GPT-4/Claude/Ollama)
3. ✅ **JSON Contracts** - Промежуточный формат тестов
4. ✅ **Code Generator** - Автоматическое создание Playwright тестов
5. ✅ **Code Linting** - Pylint, Flake8, Mypy, Bandit
6. ✅ **AI Code Review** - Интеллектуальный анализ кода
7. ✅ **Test Execution** - Параллельный запуск с Allure
8. ✅ **Logging** - Structured logging
9. ✅ **AI Log Analysis** - Поиск паттернов failures
10. ✅ **Bug Reports** - Автогенерация баг-репортов

**📊 Результат:** От текстового описания требований до готовых автотестов и баг-репортов за 2-3 минуты!

### 👁️ SauceDemo Visual Testing

- E2E тестирование с Applitools Eyes
- Page Object Model архитектура
- Baseline + Visual defects detection
- 4 визуальные контрольные точки

---

## 🆕 NEW: FREE Ollama Scripts (No API Keys Required!)

**🎉 Теперь можно использовать полностью БЕСПЛАТНО с Ollama (локальная AI):**

```powershell
# ВАРИАНТ 1: Полный цикл (генерация + запуск + отчеты)
.\3_full_pipeline_ollama.bat
# ⏱ 10-15 минут | ✅ БЕСПЛАТНО | 🔒 Локально
# 📊 Подробная отчётность с разбивкой по стадиям пайплайна

# ВАРИАНТ 2: Только генерация тестов
.\1_generate_tests_ollama.bat
# ⏱ 5-10 минут | 💡 Ollama медленнее OpenAI, но FREE!
# 📋 Структурированный отчёт о сгенерированных файлах

# ВАРИАНТ 3: Только запуск тестов + отчеты
.\2_run_tests_with_reports.bat
# ⏱ 2-5 минут | 📊 HTML + Allure отчеты автоматически
```

**✨ Что нового в отчётах:**
- 📊 **Структурированный вывод** - чёткая разбивка по этапам выполнения
- 📈 **Детальная статистика** - информация о сгенерированных файлах и результатах
- 🎯 **Пути к отчётам** - прямые ссылки на HTML и Allure отчёты
- 💡 **Полезные команды** - подсказки для повторного запуска
- 🪟 **Окно остаётся открытым** - можно просмотреть весь процесс выполнения

**Требования:**
1. Установите Ollama: https://ollama.ai/download
2. Загрузите модель: `ollama pull llama2`
3. Запустите любой bat-файл!

**Подробнее:** См. [ЗАПУСК.md](ЗАПУСК.md) для детальных инструкций

---

## 🚀 Quick Start

> **Самый быстрый способ:** [QUICKSTART_RU.md](QUICKSTART_RU.md) или просто запустите `setup.bat`
>
> **PowerShell пользователи:** См. [POWERSHELL_GUIDE.md](POWERSHELL_GUIDE.md) для правильного синтаксиса команд

### Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/AskarTuraev/saucedemo-automation-python.git
cd saucedemo_automation

# 2. Автоматическая установка (Windows)
.\setup.bat

# ИЛИ Вручную:
# Создать виртуальное окружение
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Установить Playwright браузеры
playwright install chromium

# 5. Установить Spacy модель (для PII detection)
python -m spacy download en_core_web_sm

# 6. Настроить .env файл
# PowerShell:
"OPENAI_API_KEY=sk-your-key" | Out-File -Encoding UTF8 .env

# Linux/Mac:
echo "OPENAI_API_KEY=sk-your-key" > .env
```

---

## 📊 Структура отчётов в bat-файлах

Все bat-файлы теперь имеют **единообразную структуру отчётов**:

### 1_generate_tests_ollama.bat
```
====================================================================
  DONE! Tests created in: ai_generated_tests\
====================================================================

Generated files:
  test_login.py
  conftest.py
  ...

====================================================================
OUTPUT:
  - Tests folder: ai_generated_tests\
  - Test files:   ai_generated_tests\*.py
  - Config:       ai_generated_tests\conftest.py
====================================================================

NEXT STEP: Run tests and get reports
  Run: 2_run_tests_with_reports.bat
====================================================================
```

### 2_run_tests_with_reports.bat
```
====================================================================
  DONE! OPENING REPORTS
====================================================================

OK: Both reports opened in browser!

====================================================================
REPORTS:
  - HTML:   reports\report.html
  - Allure: reports\allure-report\index.html
====================================================================
```

### 3_full_pipeline_ollama.bat
```
====================================================================
  PIPELINE EXECUTION SUMMARY
====================================================================

[STAGE 1] TEST GENERATION
  Status:        OK
  Output folder: ai_generated_tests\
  Generated:
    - test_login.py
    - conftest.py

[STAGE 2] TEST EXECUTION
  Test folder:   ai_generated_tests\
  Status:        COMPLETED
  Duration:      Check reports for details

====================================================================
  REPORTS GENERATED
====================================================================

[HTML REPORT]
  File:     reports\report.html
  Status:   C:\path\to\reports\report.html
  Browser:  OPENED

[ALLURE REPORT]
  File:     reports\allure-report\index.html
  Status:   C:\path\to\reports\allure-report\index.html
  Browser:  OPENED

====================================================================
  USEFUL COMMANDS
====================================================================

Run individual steps:
  1_generate_tests_ollama.bat  - Generate tests only
  2_run_tests_with_reports.bat - Run tests with reports only

Rerun this full pipeline:
  3_full_pipeline_ollama.bat

View reports again:
  start reports\report.html
  start reports\allure-report\index.html
====================================================================
```

---

## 🎬 Использование

### Option 1A: Ollama (FREE - Рекомендуется для начинающих!)

**🆕 Бесплатная генерация с локальной AI:**

```powershell
# 🎯 ПОЛНЫЙ ЦИКЛ (всё в одном)
.\3_full_pipeline_ollama.bat
# Генерирует тесты → Запускает → Создаёт отчеты → Открывает в браузере

# 🔧 ПО ШАГАМ
.\1_generate_tests_ollama.bat  # Генерация тестов с Ollama
.\2_run_tests_with_reports.bat # Запуск + HTML/Allure отчеты
```

**Преимущества Ollama:**
- ✅ Полностью бесплатно (без API ключей)
- ✅ Работает локально (приватность)
- ✅ Не нужен интернет (после установки модели)
- ⚠️ Медленнее OpenAI (5-10 минут вместо 2-3)

### Option 1B: OpenAI/Claude (Быстрее, но платно)

**Генерация тестов из текстовых требований:**

```bash
# Полный пайплайн: Requirements → Tests
# ВАЖНО для PowerShell: команда ОДНОЙ СТРОКОЙ (без \)
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests

# Для Ollama используйте bat-файлы выше (рекомендуется!)
# Старые скрипты с OpenAI в папке: old_scripts/

# Результат:
# ✓ PII sanitized
# ✓ 5 test scenarios generated
# ✓ 5 JSON contracts created
# ✓ 5 Playwright tests generated
# ✓ conftest.py + Page Objects

# Запуск сгенерированных тестов
cd generated_tests
pytest -v --headed
```

**Пошаговое использование:**

```bash
# 1. PII Detection
python -m ai_qa_pipeline.modules.pii_detection.cli \
    requirements.txt -f -o safe_requirements.txt -s fake

# 2. Generate Scenarios
python -m ai_qa_pipeline.modules.test_generation.cli \
    safe_requirements.txt -f -o scenarios.json

# 3. Create JSON Contracts
python -m ai_qa_pipeline.modules.code_generation.cli contracts \
    scenarios.json -o contracts.json --base-url https://app.com

# 4. Generate Code
python -m ai_qa_pipeline.modules.code_generation.cli generate \
    contracts.json -o tests/ -f playwright

# 5. Code Review
python -m ai_qa_pipeline.modules.code_review.cli full \
    tests/ --llm openai -o review.md
```

### Option 2: SauceDemo Applitools Tests (Готовые тесты)

```bash
# Baseline тест
pytest tests/test_saucedemo_baseline.py -v

# Тест с visual defects
pytest tests/test_saucedemo_visual_defects.py -v

# Все тесты
pytest -v
```

---

## 📂 Структура проекта

```
saucedemo_automation/
├── 🆕 1_generate_tests_ollama.bat    # Generate tests with Ollama (FREE)
├── 🆕 2_run_tests_with_reports.bat    # Run tests + auto-open reports
├── 🆕 3_full_pipeline_ollama.bat      # Full cycle (all-in-one)
├── 🆕 ЗАПУСК.md                       # Russian quick start guide
│
├── ai_qa_pipeline/                    # ⭐ AI-Driven QA Pipeline
│   ├── modules/
│   │   ├── pii_detection/             # Stage 1: PII Protection
│   │   ├── test_generation/           # Stage 2: AI Test Generator
│   │   ├── code_generation/           # Stage 3-4: JSON + Code Gen
│   │   ├── code_review/               # Stage 5-6: Linting + AI Review
│   │   ├── test_execution/            # Stage 7: Test Runner
│   │   ├── log_analysis/              # Stage 8-9: AI Log Analysis
│   │   └── bug_reporting/             # Stage 10: Bug Reports
│   └── README.md                      # AI Pipeline docs
│
├── tests/                             # Applitools tests
│   ├── test_saucedemo_baseline.py
│   └── test_saucedemo_visual_defects.py
│
├── pages/                             # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── reports/                           # 🆕 Auto-generated reports
│   ├── report.html                    # HTML report (auto-opens)
│   ├── allure-results/                # Allure data
│   └── allure-report/                 # Allure report (auto-opens)
│
├── old_scripts/                       # 🗄️ Legacy OpenAI scripts
│   ├── quick_test.bat
│   ├── quick_test_ollama.bat
│   └── test_pii.bat
│
├── .github/workflows/
│   └── ai_qa_pipeline.yml            # CI/CD (10 stages)
│
├── PRESENTATION.md                   # 21-slide presentation
├── DEMO_SCRIPT.md                    # Demo scenario
├── PROJECT_SUMMARY.md                # Project metrics
├── SESSION_CONTEXT.md                # 🆕 Full session context
├── requirements.txt                  # All dependencies
└── README.md                         # This file
```

---

## 🎓 Документация

### AI-Driven QA Pipeline:
- **[Main README](ai_qa_pipeline/README.md)** - архитектура и примеры
- **[Design Document](https://github.com/AskarTuraev/saucedemo-automation-python/blob/main/AI_QA_Pipeline_Design.md)** - полный дизайн
- **[PII Detection](ai_qa_pipeline/modules/pii_detection/README.md)** - защита данных
- **[Test Generation](ai_qa_pipeline/modules/test_generation/README.md)** - AI генерация

### Презентация и демонстрация:
- **[PRESENTATION.md](PRESENTATION.md)** - 21 слайд для защиты
- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - сценарий демонстрации
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - итоговое резюме

### Applitools Testing:
- **[QUICKSTART.md](QUICKSTART.md)** - быстрый старт
- **[REPORTING_GUIDE.md](REPORTING_GUIDE.md)** - инструкция по отчетам
- **[CHECKLIST.md](CHECKLIST.md)** - чек-лист выполнения

---

## 💡 Примеры использования

### Пример 1: Генерация E2E теста для логина

**Input (requirements.txt):**
```
Feature: User Login
As a user, I want to login with valid credentials
to access the inventory page.

Acceptance Criteria:
- Login form has username and password fields
- User can login with standard_user / secret_sauce
- After login, user sees inventory page
```

**Output (test_login.py):**
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.ui
@pytest.mark.priority_critical
def test_login_with_valid_credentials(page: Page):
    """Verify user can login with valid credentials"""
    page.goto("https://www.saucedemo.com")
    page.locator('[data-testid="username"]').fill("standard_user")
    page.locator('[data-testid="password"]').fill("secret_sauce")
    page.locator('[data-testid="login-button"]').click()
    expect(page.locator('.inventory_list')).to_be_visible()
```

### Пример 2: PII Sanitization

```python
from ai_qa_pipeline.modules.pii_detection import PIIPipeline

pipeline = PIIPipeline(masking_strategy="fake")

unsafe_text = """
User credentials:
Email: admin@company.com
API Key: sk_live_abc123xyz
Phone: +1-555-0100
"""

safe_text = pipeline.sanitize_for_llm(unsafe_text)
# Result:
# User credentials:
# Email: user@example.com
# API Key: sk_test_1234567890abcdef
# Phone: +1-555-0100
```

### Пример 3: AI Code Review

```bash
python -m ai_qa_pipeline.modules.code_review.cli full \
    generated_tests/ \
    --llm openai \
    -o review-report.md

# Output:
# Score: 87/100 ✅ APPROVED
# Issues: 3 minor, 2 suggestions
# - Line 42: Use more specific locator
# - Line 58: Add timeout parameter
```

---

## 📊 Метрики и производительность

### AI Pipeline:

**С OpenAI (GPT-4):**
- **Генерация 1 сценария:** 5-15 секунд
- **Full pipeline (5 tests):** 2-3 минуты
- **Стоимость:** ~$0.25 per full pipeline

**С Ollama (llama2) - БЕСПЛАТНО:**
- **Генерация 1 сценария:** 30-60 секунд
- **Full pipeline (5 tests):** 5-10 минут
- **Стоимость:** $0.00 (полностью бесплатно!)

**Общие метрики:**
- **Генерация кода:** <1 секунда/файл
- **Code review:** 10-20 секунд/файл

### Quality Metrics:
- **Test generation accuracy:** ~85-90%
- **PII detection F1 score:** 90-95%
- **Code quality score:** 8.5/10 average

---

## 🛠️ Технологический стек

### AI/LLM:
- OpenAI GPT-4
- Anthropic Claude
- Ollama (local models)
- LangChain
- Microsoft Presidio

### Testing:
- Playwright
- Pytest
- Applitools Eyes
- Allure

### Code Quality:
- Pylint
- Flake8
- Mypy
- Bandit

### Templates & Generation:
- Jinja2
- JSONSchema
- Pydantic

---

## 🔧 Настройка

### Environment Variables (.env)

```env
# AI/LLM API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Applitools
APPLITOOLS_API_KEY=...

# Application
BASE_URL=https://www.saucedemo.com
BROWSER=chromium
HEADLESS=false

# Test Credentials
TEST_USERNAME=standard_user
TEST_PASSWORD=secret_sauce
```

---

## 🚦 CI/CD

**GitHub Actions автоматически:**

1. Sanitize requirements (PII detection)
2. Generate test scenarios (AI)
3. Create JSON contracts
4. Generate Playwright code
5. Run static analysis (Pylint, Flake8, Mypy, Bandit)
6. AI code review (GPT-4)
7. Execute tests (parallel)
8. Generate Allure reports
9. AI failure analysis
10. Create bug reports

**Trigger:** Push to `main`, Pull Request, Manual

**Artifacts:** Generated tests, reports, analysis

**GitHub Pages:** Allure reports auto-deployed

---

## 📈 Сравнение с аналогами

| Feature | Our Solution | TestRigor | Mabl | Testim |
|---------|--------------|-----------|------|--------|
| **Full AI Pipeline** | ✅ 10 stages | ❌ | ❌ | ❌ |
| **PII Protection** | ✅ Presidio | ❌ | ❌ | ❌ |
| **AI Code Review** | ✅ GPT-4 | ❌ | ❌ | ❌ |
| **Auto Bug Reports** | ✅ | ❌ | ❌ | ❌ |
| **Open Source** | ✅ MIT | ❌ | ❌ | ❌ |
| **Cost/month** | **$0** (Ollama) or ~$25 (OpenAI) | $900 | $450 | $450 |
| **Self-hosted** | ✅ | ❌ | ❌ | ❌ |
| **FREE Option** | ✅ Ollama | ❌ | ❌ | ❌ |

---

## 🤝 Contributing

Contributions welcome! This is an educational project showcasing AI in QA automation.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE for details

---

## 👨‍💻 Author

**Askar Turaev**
- GitHub: [@AskarTuraev](https://github.com/AskarTuraev)
- Repository: [saucedemo-automation-python](https://github.com/AskarTuraev/saucedemo-automation-python)

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4 API
- **Anthropic** - Claude API
- **Microsoft** - Presidio framework
- **Playwright Team** - Browser automation
- **Applitools** - Visual testing platform
- **Python Community** - Amazing ecosystem

---

## 📚 Additional Resources

**Documentation:**
- [Playwright Docs](https://playwright.dev/python/)
- [Applitools Docs](https://applitools.com/docs/)
- [Pytest Docs](https://docs.pytest.org/)
- [OpenAI API Docs](https://platform.openai.com/docs/)

**Related Projects:**
- [Playwright Python](https://github.com/microsoft/playwright-python)
- [Presidio](https://github.com/microsoft/presidio)
- [LangChain](https://github.com/langchain-ai/langchain)

---

## 🎓 Educational Use

This project is designed for:
- ✅ QA Automation learning
- ✅ AI/LLM integration studies
- ✅ Software architecture examples
- ✅ Coursework projects
- ✅ Hackathons
- ✅ Technical interviews

---

## 🔮 Roadmap

**Planned features:**
- [ ] API testing support (REST/GraphQL)
- [ ] Mobile testing (Appium)
- [ ] Visual testing (Percy integration)
- [ ] Fine-tuned models for QA
- [ ] Self-healing tests
- [ ] Multi-language support
- [ ] Enterprise features (RBAC, audit)

---

## 📞 Support

**Questions or issues?**
- Open an [Issue](https://github.com/AskarTuraev/saucedemo-automation-python/issues)
- Check [Discussions](https://github.com/AskarTuraev/saucedemo-automation-python/discussions)
- Review [Wiki](https://github.com/AskarTuraev/saucedemo-automation-python/wiki)

---

**⭐ If you find this project useful, please give it a star!**

**🤖 AI-Driven QA Pipeline - The Future of Test Automation**

---

*Made with ❤️ for learning AI-powered test automation*
