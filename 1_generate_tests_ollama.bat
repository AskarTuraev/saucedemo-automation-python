@echo off
REM ========================================================================
REM ШАГ 1: Генерация тестов с помощью AI (Ollama - БЕСПЛАТНО)
REM ========================================================================
REM
REM Этот скрипт:
REM 1. Проверяет установку Ollama
REM 2. Загружает модель llama2 если нужно
REM 3. Генерирует автотесты из текстовых требований
REM
REM После генерации используйте: 2_run_tests_with_reports.bat
REM ========================================================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ШАГ 1: ГЕНЕРАЦИЯ ТЕСТОВ С AI (OLLAMA)                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Ollama
echo [1/6] Проверка установки Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ✖ ОШИБКА: Ollama не найдена!
    echo.
    echo Установите Ollama:
    echo 1. Скачайте: https://ollama.ai/download
    echo 2. Установите OllamaSetup.exe
    echo 3. Запустите: ollama pull llama2
    echo.
    pause
    exit /b 1
)
echo ✓ Ollama установлена
echo.

REM Проверка модели
echo [2/6] Проверка модели llama2...
ollama list | findstr llama2 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Модель llama2 не найдена
    echo Загружаем модель (~4GB, это может занять 5-10 минут)...
    ollama pull llama2
    if %errorlevel% neq 0 (
        echo.
        echo ✖ ОШИБКА: Не удалось загрузить модель
        pause
        exit /b 1
    )
)
echo ✓ Модель llama2 готова
echo.

REM Активация виртуального окружения
echo [3/6] Активация виртуального окружения...
if not exist "venv\Scripts\activate.bat" (
    echo ✖ ОШИБКА: Виртуальное окружение не найдено!
    echo Запустите сначала: setup.bat
    pause
    exit /b 1
)
call venv\Scripts\activate
echo ✓ Виртуальное окружение активировано
echo.

REM Создание требований
echo [4/6] Создание файла требований...
(
echo Feature: SauceDemo Login
echo As a user I want to login to SauceDemo
echo So that I can access the product catalog
echo.
echo Scenario: Successful login
echo Given I am on the login page
echo When I enter username 'standard_user'
echo And I enter password 'secret_sauce'
echo And I click login button
echo Then I should see the inventory page
) > quick_requirements.txt
echo ✓ Требования созданы: quick_requirements.txt
echo.

REM Генерация тестов
echo [5/6] Генерация автотестов с помощью AI...
echo ⏳ Это займет 5-10 минут (Ollama медленнее OpenAI, но БЕСПЛАТНО)
echo.
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output ai_generated_tests

REM Проверка результата
if not exist "ai_generated_tests" (
    echo.
    echo ✖ ОШИБКА: Генерация тестов не удалась!
    echo Проверьте сообщения об ошибках выше
    echo.
    pause
    exit /b 1
)

echo.
echo [6/6] ✓ Тесты успешно сгенерированы!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ГОТОВО! Тесты созданы в папке: ai_generated_tests\       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Содержимое папки:
dir ai_generated_tests /b
echo.
echo ════════════════════════════════════════════════════════════
echo СЛЕДУЮЩИЙ ШАГ: Запустите тесты и получите отчеты
echo.
echo Запустите: 2_run_tests_with_reports.bat
echo ════════════════════════════════════════════════════════════
echo.
pause
