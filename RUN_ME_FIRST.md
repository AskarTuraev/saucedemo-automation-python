# 🚀 ЗАПУСТИТЕ ЭТО ПЕРВЫМ ДЕЛОМ

**Для Windows PowerShell пользователей**

---

## ✅ ШАГ 1: Активируйте виртуальное окружение

```powershell
.\venv\Scripts\Activate.ps1
```

Вы должны увидеть `(venv)` перед строкой.

---

## ✅ ШАГ 2: Создайте .env файл

**Вариант А: Через PowerShell (быстро)**

```powershell
"OPENAI_API_KEY=sk-ваш-ключ-здесь" | Out-File -Encoding UTF8 .env
```

**Вариант Б: Через блокнот (понятнее)**

1. Откройте блокнот
2. Напишите: `OPENAI_API_KEY=sk-ваш-ключ-здесь`
3. Сохраните как `.env` (с точкой!) в папке проекта

**Где взять ключ?** https://platform.openai.com/ → API Keys → Create new key

---

## ✅ ШАГ 3: Создайте файл требований

```powershell
@"
Feature: User Login to SauceDemo
As a user I want to login to the application
So that I can access the product catalog

Scenario: Successful login
Given I am on the login page at https://www.saucedemo.com
When I enter username 'standard_user'
And I enter password 'secret_sauce'
And I click the login button
Then I should see the inventory page with products
"@ | Out-File -Encoding UTF8 requirements.txt
```

---

## ✅ ШАГ 4: Запустите генерацию тестов

**⚠️ ВАЖНО: Вся команда ОДНОЙ СТРОКОЙ (без переносов)!**

```powershell
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests
```

**Или используйте готовый скрипт:**

```powershell
.\quick_test.bat
```

---

## ✅ ШАГ 5: Проверьте результат

```powershell
# Посмотрите что создалось
ls generated_tests

# Посмотрите код
cat generated_tests\test_*.py

# Запустите тесты
cd generated_tests
pytest -v --headed
```

---

## 🎉 ГОТОВО!

Если все прошло успешно, вы увидите:
- ✅ Созданные тестовые файлы
- ✅ Браузер автоматически открывается и выполняет тесты
- ✅ Результаты в консоли

---

## 🐛 Если что-то не работает

### Проблема: "execution policy"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Проблема: "unrecognized arguments"

Вы использовали `\` для переноса строк. В PowerShell это не работает!

**НЕ ДЕЛАЙТЕ ТАК:**
```powershell
python -m ai_qa_pipeline.modules.code_generation.cli full \
    requirements.txt \
    --base-url https://www.saucedemo.com
```

**ДЕЛАЙТЕ ТАК:**
```powershell
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests
```

### Проблема: "No such file: requirements.txt"

Сначала создайте файл (см. ШАГ 3 выше)

### Проблема: "OPENAI_API_KEY not found"

Проверьте .env файл:
```powershell
cat .env
```

Должно быть: `OPENAI_API_KEY=sk-...`

---

## 📋 Все команды по порядку (копировать-вставить)

```powershell
# 1. Активировать venv
.\venv\Scripts\Activate.ps1

# 2. Создать .env (ЗАМЕНИТЕ на ваш ключ!)
"OPENAI_API_KEY=sk-ваш-настоящий-ключ" | Out-File -Encoding UTF8 .env

# 3. Создать requirements.txt
@"
Feature: User Login
User wants to login to SauceDemo
"@ | Out-File -Encoding UTF8 requirements.txt

# 4. Генерация тестов (ОДНОЙ СТРОКОЙ!)
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output generated_tests

# 5. Запуск
cd generated_tests
pytest -v --headed
```

---

## 🎯 Еще проще - используйте готовые скрипты

```powershell
# Тест PII Detection (10 секунд)
.\test_pii.bat

# Полный тест пайплайна (2-3 минуты)
.\quick_test.bat
```

**Но сначала создайте .env файл!**

---

## 📚 Дополнительная помощь

- [POWERSHELL_GUIDE.md](POWERSHELL_GUIDE.md) - Полное руководство для PowerShell
- [QUICKSTART_RU.md](QUICKSTART_RU.md) - Детальный быстрый старт
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Руководство по тестированию

---

**Удачи! 🚀**
