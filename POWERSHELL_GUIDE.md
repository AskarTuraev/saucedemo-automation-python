# 🔷 PowerShell Guide для AI-Driven QA Pipeline

**Все команды адаптированы для PowerShell (Windows)**

---

## ⚡ Быстрый старт

```powershell
# 1. Установка
.\setup.bat

# 2. Создайте .env файл (замените на ваш ключ)
"OPENAI_API_KEY=sk-your-key-here" | Out-File -Encoding UTF8 .env

# 3. Быстрый тест
.\quick_test.bat
```

---

## 📋 Основные команды

### Активация виртуального окружения

```powershell
# Активировать venv
.\venv\Scripts\Activate.ps1

# Проверить что активирован (должно быть (venv) перед строкой)
```

### Создание файла requirements.txt

```powershell
# Создать тестовый файл с требованиями
@"
Feature: User Login
As a user I want to login to SauceDemo
So that I can access the product catalog

Scenario: Successful login
Given I am on the login page
When I enter username 'standard_user'
And I enter password 'secret_sauce'
And I click login button
Then I should see the inventory page
"@ | Out-File -Encoding UTF8 test_requirements.txt
```

---

## 🔍 Stage 1: PII Detection

```powershell
# Базовая проверка
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f

# С сохранением результата
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -o safe_requirements.txt

# С отчетом
python -m ai_qa_pipeline.modules.pii_detection.cli test_requirements.txt -f -o safe_requirements.txt --report

# Или используйте готовый скрипт
.\test_pii.bat
```

---

## 🤖 Полный пайплайн (одной строкой)

```powershell
# ВАЖНО: В PowerShell НЕ используйте \ для переноса строк!
# Пишите всю команду в одну строку:

python -m ai_qa_pipeline.modules.code_generation.cli full test_requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests
```

### Или с переносами (используйте обратный апостроф `` ` ``):

```powershell
python -m ai_qa_pipeline.modules.code_generation.cli full `
    test_requirements.txt `
    --base-url https://www.saucedemo.com `
    --llm openai `
    --output generated_tests
```

### Самый простой способ:

```powershell
.\quick_test.bat
```

---

## 📝 Пошаговое использование

### Шаг 1: Создать требования

```powershell
@"
Feature: SauceDemo Login
User wants to login with valid credentials

Test Data:
- URL: https://www.saucedemo.com
- Username: standard_user
- Password: secret_sauce
"@ | Out-File -Encoding UTF8 my_requirements.txt
```

### Шаг 2: Генерация тестов (одной строкой!)

```powershell
python -m ai_qa_pipeline.modules.code_generation.cli full my_requirements.txt --base-url https://www.saucedemo.com --llm openai --output my_tests
```

### Шаг 3: Запуск тестов

```powershell
cd my_tests
pytest -v --headed
cd ..
```

---

## 🔍 Code Review

```powershell
# Static analysis
python -m ai_qa_pipeline.modules.code_review.cli lint my_tests -o lint-report.json

# AI Review (одной строкой)
python -m ai_qa_pipeline.modules.code_review.cli ai-review my_tests --llm openai --format markdown -o ai-review.md

# Полный review
python -m ai_qa_pipeline.modules.code_review.cli full my_tests --llm openai -o full-review.md

# Посмотреть результат
cat ai-review.md
```

---

## 🧪 Запуск тестов

```powershell
# Перейти в папку с тестами
cd generated_tests

# Базовый запуск
pytest -v

# С браузером
pytest -v --headed

# С замедлением (для демонстрации)
pytest -v --headed --slowmo=1000

# Параллельно (4 потока)
pytest -v -n4

# С отчетами
pytest -v --alluredir=allure-results --json-report --json-report-file=results.json

# Вернуться назад
cd ..
```

---

## 📊 Работа с .env файлом

```powershell
# Создать .env файл
@"
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-key
BASE_URL=https://www.saucedemo.com
BROWSER=chromium
HEADLESS=false
"@ | Out-File -Encoding UTF8 .env

# Проверить содержимое
cat .env

# Или отредактировать в блокноте
notepad .env
```

---

## 🔧 Полезные PowerShell команды

```powershell
# Посмотреть содержимое файла
cat filename.txt
type filename.txt

# Показать первые 10 строк
cat filename.txt | Select-Object -First 10

# Создать файл
"content" | Out-File -Encoding UTF8 file.txt

# Показать список файлов
ls
dir

# Показать дерево папок (если есть tree.com)
tree /F

# Копировать файл
Copy-Item source.txt dest.txt

# Удалить файл
Remove-Item file.txt

# Очистить экран
Clear-Host
cls

# Проверить версию Python
python --version

# Проверить установленные пакеты
pip list

# Найти файлы
Get-ChildItem -Recurse -Filter "*.py"
```

---

## 🎬 Команды для демонстрации

### Быстрая демо (5 минут):

```powershell
# 1. PII Detection
.\test_pii.bat

# 2. Full Pipeline
.\quick_test.bat

# 3. Показать сгенерированный код
cat quick_tests\test_login_with_valid_credentials.py

# 4. Запустить тесты
cd quick_tests
pytest -v --headed --slowmo=1000
cd ..
```

### Полная демо (10 минут):

```powershell
# 1. Создать требования
@"
Feature: SauceDemo E2E Test
Test login and add to cart functionality
"@ | Out-File -Encoding UTF8 demo_req.txt

# 2. Генерация (одной строкой!)
python -m ai_qa_pipeline.modules.code_generation.cli full demo_req.txt --base-url https://www.saucedemo.com --llm openai --output demo_tests

# 3. Показать структуру
ls demo_tests

# 4. Показать код
cat demo_tests\test_*.py

# 5. AI Code Review
python -m ai_qa_pipeline.modules.code_review.cli full demo_tests --llm openai -o demo_review.md

# 6. Показать review
cat demo_review.md

# 7. Запустить тесты
cd demo_tests
pytest -v --headed --slowmo=1000
cd ..
```

---

## ⚠️ Частые ошибки в PowerShell

### ❌ НЕ РАБОТАЕТ (bash синтаксис):

```powershell
# НЕ ИСПОЛЬЗУЙТЕ \ для переноса строк!
python -m ai_qa_pipeline.modules.code_generation.cli full \
    requirements.txt \
    --base-url https://www.saucedemo.com
```

### ✅ РАБОТАЕТ (PowerShell синтаксис):

```powershell
# Вариант 1: Одной строкой
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output tests

# Вариант 2: С переносами (обратный апостроф `)
python -m ai_qa_pipeline.modules.code_generation.cli full `
    requirements.txt `
    --base-url https://www.saucedemo.com `
    --llm openai `
    --output tests
```

---

## 🐛 Troubleshooting PowerShell

### Проблема: "execution policy"

```powershell
# Если не активируется venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Затем повторите
.\venv\Scripts\Activate.ps1
```

### Проблема: "command not found"

```powershell
# Проверьте что venv активирован
.\venv\Scripts\Activate.ps1

# Проверьте путь к Python
Get-Command python
```

### Проблема: Кодировка файлов

```powershell
# Всегда используйте UTF8 при создании файлов
"content" | Out-File -Encoding UTF8 file.txt

# НЕ используйте редирект > (создаст файл в UTF16)
# "content" > file.txt  # ❌ НЕ ДЕЛАЙТЕ ТАК
```

---

## 📋 Готовые команды (копировать-вставить)

### Полный цикл от нуля:

```powershell
# 1. Активировать venv
.\venv\Scripts\Activate.ps1

# 2. Создать требования
@"
Feature: Login Test
User can login with valid credentials
"@ | Out-File -Encoding UTF8 req.txt

# 3. Генерация тестов
python -m ai_qa_pipeline.modules.code_generation.cli full req.txt --base-url https://www.saucedemo.com --llm openai --output tests

# 4. Запуск
cd tests
pytest -v --headed
cd ..
```

### Code Review + Tests:

```powershell
# 1. Review
python -m ai_qa_pipeline.modules.code_review.cli full tests --llm openai -o review.md

# 2. Посмотреть
cat review.md

# 3. Запустить тесты
cd tests
pytest -v --headed --alluredir=allure-results
cd ..

# 4. Allure отчет
allure serve tests\allure-results
```

---

## ✅ Проверка что все работает

```powershell
# 1. Активировать venv
.\venv\Scripts\Activate.ps1

# 2. Проверить Python
python --version

# 3. Проверить пакеты
pip list | Select-String "playwright"

# 4. Проверить .env
cat .env

# 5. Тест PII
.\test_pii.bat

# 6. Полный тест
.\quick_test.bat
```

Если все прошло ✅ - вы готовы!

---

## 🎯 Шпаргалка: Bash → PowerShell

| Bash | PowerShell |
|------|------------|
| `cat file` | `cat file` или `type file` |
| `ls` | `ls` или `dir` |
| `echo "text" > file` | `"text" \| Out-File file` |
| `rm file` | `Remove-Item file` или `del file` |
| `cp src dst` | `Copy-Item src dst` или `copy src dst` |
| `pwd` | `pwd` или `Get-Location` |
| `cd path` | `cd path` или `Set-Location path` |
| `\` (перенос) | `` ` `` (обратный апостроф) |
| `&&` | `;` или Enter между командами |
| `grep pattern` | `Select-String pattern` |

---

## 💡 Полезные алиасы PowerShell

PowerShell уже понимает многие bash команды:
- `ls` → `Get-ChildItem`
- `cat` → `Get-Content`
- `pwd` → `Get-Location`
- `cd` → `Set-Location`
- `clear` → `Clear-Host`

Но синтаксис немного отличается!

---

**Теперь вы готовы работать в PowerShell! 🔷**
