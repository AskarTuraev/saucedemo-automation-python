# 🦙 Ollama Setup - Бесплатная альтернатива OpenAI

**Как запустить AI-Driven QA Pipeline без платных API ключей**

---

## ⚡ Быстрый старт

### Шаг 1: Установите Ollama (5 минут)

1. Скачайте Ollama для Windows:
   - https://ollama.ai/download
   - Или прямая ссылка: https://ollama.ai/download/windows

2. Запустите установщик `OllamaSetup.exe`

3. Дождитесь завершения установки

### Шаг 2: Загрузите модель (5-10 минут)

```powershell
# Откройте новый PowerShell и выполните:
ollama pull llama2
```

**Это скачает ~4GB данных, подождите пока загрузится.**

### Шаг 3: Проверьте что работает

```powershell
# Проверить версию
ollama --version

# Список загруженных моделей
ollama list

# Должно показать:
# llama2:latest
```

### Шаг 4: Запустите генерацию тестов!

```powershell
# Активируйте venv
.\venv\Scripts\Activate.ps1

# Запустите с Ollama
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output generated_tests
```

---

## 🎯 Готовые команды (копировать-вставить)

### Полная генерация с Ollama:

```powershell
# 1. Активировать venv
.\venv\Scripts\Activate.ps1

# 2. Создать requirements
@"
Feature: User Login
As a user I want to login to SauceDemo
So that I can access the product catalog

Scenario: Successful login
Given I am on the login page
When I enter valid credentials
Then I should see the inventory page
"@ | Out-File -Encoding UTF8 requirements.txt

# 3. Генерация с Ollama
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output generated_tests

# 4. Запуск тестов
cd generated_tests
pytest -v --headed
```

---

## 📊 Сравнение: OpenAI vs Ollama

| Параметр | OpenAI GPT-4 | Ollama (llama2) |
|----------|--------------|-----------------|
| **Стоимость** | ~$0.25 за 5 тестов | 🆓 Бесплатно |
| **Скорость** | 30-60 секунд | 2-5 минут |
| **Качество** | ⭐⭐⭐⭐⭐ Отлично | ⭐⭐⭐⭐ Хорошо |
| **Требования** | Интернет + API ключ | Локальная установка |
| **Размер** | - | ~4GB на диске |
| **Настройка** | 2 минуты (.env) | 10 минут (установка) |

---

## 🔄 Доступные модели Ollama

```powershell
# Рекомендуемые модели для кода:

# 1. llama2 (универсальная, 4GB)
ollama pull llama2

# 2. codellama (специально для кода, 4GB)
ollama pull codellama

# 3. mistral (быстрая и качественная, 4GB)
ollama pull mistral

# 4. llama3 (новейшая, 4.7GB) - РЕКОМЕНДУЕТСЯ!
ollama pull llama3
```

### Какую модель выбрать?

- **llama2** - универсальная, хорошая для начала
- **llama3** - новейшая, лучшее качество (рекомендуется!)
- **codellama** - оптимизирована для генерации кода
- **mistral** - быстрая, хороший баланс

---

## 🎬 Использование разных моделей

```powershell
# С llama2
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output tests

# С llama3 (рекомендуется)
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama3 --output tests

# С codellama
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model codellama --output tests

# С mistral
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model mistral --output tests
```

---

## 🔧 Все этапы с Ollama

### Stage 2: Test Generation

```powershell
python -m ai_qa_pipeline.modules.test_generation.cli requirements.txt -f -o scenarios.json --llm ollama --model llama2
```

### Stage 5-6: AI Code Review

```powershell
python -m ai_qa_pipeline.modules.code_review.cli ai-review generated_tests --llm ollama --model llama2 --format markdown -o review.md
```

### Stage 9: Log Analysis

```powershell
python -m ai_qa_pipeline.modules.log_analysis.cli results.json -o analysis.md --llm ollama --model llama2
```

### Stage 10: Bug Reports

```powershell
python -m ai_qa_pipeline.modules.bug_reporting.cli results.json -o bugs --format markdown --llm ollama --model llama2
```

---

## ⚠️ Известные ограничения

### 1. Скорость
Ollama работает на вашем компьютере и медленнее облачных API:
- **Генерация 1 теста:** 1-3 минуты (vs 10 секунд с GPT-4)
- **Code review:** 2-5 минут (vs 30 секунд с GPT-4)

### 2. Требования к железу
Для комфортной работы нужно:
- **RAM:** минимум 8GB, рекомендуется 16GB
- **Диск:** ~10GB свободного места
- **CPU:** современный процессор (желательно с AVX2)

### 3. Качество
- Иногда генерирует менее точный код
- Может потребоваться ручная доработка
- Но для обучения и базовых тестов вполне достаточно!

---

## 🐛 Troubleshooting

### Проблема: "ollama: command not found"

```powershell
# Перезапустите PowerShell
# Или проверьте что Ollama установлен:
Get-Command ollama

# Если не нашло - переустановите Ollama
```

### Проблема: "connection refused"

```powershell
# Убедитесь что Ollama запущен
# Откройте новое окно PowerShell:
ollama serve

# Оставьте это окно открытым и используйте другое для команд
```

### Проблема: Медленная работа

```powershell
# 1. Используйте меньшую модель
ollama pull llama2:7b  # вместо llama2:13b

# 2. Или используйте mistral (быстрее)
ollama pull mistral

# Затем:
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model mistral --output tests
```

### Проблема: Out of memory

```powershell
# Закройте другие программы
# Используйте меньшую модель
# Или добавьте больше RAM
```

---

## 🎯 Рекомендуемая настройка

```powershell
# 1. Установите Ollama
# Скачайте с https://ollama.ai/download

# 2. Загрузите llama3 (лучшее качество)
ollama pull llama3

# 3. Проверьте
ollama list

# 4. Создайте алиас для удобства
# Добавьте в $PROFILE:
function Generate-Tests {
    param([string]$req = "requirements.txt", [string]$out = "generated_tests")
    python -m ai_qa_pipeline.modules.code_generation.cli full $req --base-url https://www.saucedemo.com --llm ollama --model llama3 --output $out
}

# Теперь можно просто:
# Generate-Tests
```

---

## 💡 Советы по использованию

### 1. Первый запуск
При первом запуске модель загружается в память (~4GB), это занимает время. Последующие запросы будут быстрее.

### 2. Простые требования
Пишите простые и четкие требования:
```
Feature: Login
User can login with valid credentials
Username: standard_user
Password: secret_sauce
```

### 3. Проверяйте результат
Ollama может ошибаться чаще чем GPT-4. Всегда проверяйте сгенерированный код перед использованием.

### 4. Используйте Code Review
```powershell
python -m ai_qa_pipeline.modules.code_review.cli full generated_tests --llm ollama --model llama3 -o review.md
```

---

## 📊 Производительность

На среднем ПК (i5, 16GB RAM):

| Операция | Время | Vs OpenAI |
|----------|-------|-----------|
| Генерация 1 теста | 1-3 мин | 10x медленнее |
| Генерация 5 тестов | 5-15 мин | 10x медленнее |
| Code review (1 файл) | 2-5 мин | 6x медленнее |
| Full pipeline | 10-20 мин | 8x медленнее |

**Но зато бесплатно! 🆓**

---

## ✅ Проверка установки

```powershell
# 1. Ollama установлен?
ollama --version

# 2. Модель загружена?
ollama list

# 3. Тест генерации
ollama run llama2 "Write a simple Python function that adds two numbers"

# Если вывел код - все работает!
```

---

## 🎓 Для защиты проекта

Если используете Ollama на защите:

**Плюсы:**
- ✅ Не нужен интернет (если модель загружена)
- ✅ Бесплатно
- ✅ Работает офлайн

**Минусы:**
- ❌ Медленнее (10-20 минут вместо 2-3)
- ❌ Качество чуть ниже
- ❌ Нужен мощный ПК

**Рекомендация:**
- Загрузите модель заранее
- Сгенерируйте тесты до защиты
- На защите покажите уже готовые результаты
- Или используйте OpenAI (быстрее и качественнее)

---

## 🔄 Переключение между OpenAI и Ollama

```powershell
# OpenAI (быстро, платно, требует .env)
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm openai --output tests

# Ollama (медленно, бесплатно, локально)
python -m ai_qa_pipeline.modules.code_generation.cli full requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama3 --output tests
```

---

## 📚 Дополнительная информация

- **Ollama GitHub:** https://github.com/ollama/ollama
- **Документация:** https://github.com/ollama/ollama/blob/main/docs/README.md
- **Список моделей:** https://ollama.ai/library
- **Community:** https://discord.gg/ollama

---

**Теперь вы можете использовать AI-Driven QA Pipeline бесплатно! 🦙🆓**
