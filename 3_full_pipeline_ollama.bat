@echo off
REM ========================================================================
REM ПОЛНЫЙ ЦИКЛ: Генерация + Запуск + Отчеты (Ollama)
REM ========================================================================
REM
REM Этот скрипт выполняет полный цикл:
REM 1. Генерирует тесты с помощью AI (Ollama)
REM 2. Запускает сгенерированные тесты
REM 3. Создает HTML и Allure отчеты
REM 4. Автоматически открывает отчеты
REM
REM Удобно для демонстрации возможностей AI-тестирования!
REM ========================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ПОЛНЫЙ ЦИКЛ AI-ТЕСТИРОВАНИЯ (OLLAMA - БЕСПЛАТНО)           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Этот скрипт выполнит:
echo   1. Генерацию тестов с AI (5-10 минут)
echo   2. Запуск тестов
echo   3. Создание отчетов
echo   4. Открытие отчетов в браузере
echo.
echo Общее время: 10-15 минут
echo.
pause

REM ========================================
REM ШАГ 1: Генерация тестов
REM ========================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ЭТАП 1/2: ГЕНЕРАЦИЯ ТЕСТОВ                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Проверка Ollama
echo [1/9] Проверка установки Ollama...
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
echo [2/9] Проверка модели llama2...
ollama list | findstr llama2 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Модель llama2 не найдена
    echo Загружаем модель (~4GB, это может занять 5-10 минут)...
    ollama pull llama2
)
echo ✓ Модель llama2 готова
echo.

REM Активация виртуального окружения
echo [3/9] Активация виртуального окружения...
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
echo [4/9] Создание файла требований...
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
echo ✓ Требования созданы
echo.

REM Удаление старых тестов
if exist "ai_generated_tests" (
    echo [5/9] Удаление старых сгенерированных тестов...
    rmdir /s /q "ai_generated_tests"
    echo ✓ Старые тесты удалены
    echo.
)

REM Генерация тестов
echo [5/9] Генерация автотестов с помощью AI...
echo ⏳ Это займет 5-10 минут (Ollama медленнее OpenAI, но БЕСПЛАТНО)
echo.
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output ai_generated_tests

REM Проверка результата
if not exist "ai_generated_tests" (
    echo.
    echo ✖ ОШИБКА: Генерация тестов не удалась!
    pause
    exit /b 1
)

echo.
echo ✓ Тесты успешно сгенерированы!
echo.

REM ========================================
REM ШАГ 2: Запуск тестов и отчеты
REM ========================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ЭТАП 2/2: ЗАПУСК ТЕСТОВ И ГЕНЕРАЦИЯ ОТЧЕТОВ                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Проверка зависимостей
echo [6/9] Проверка зависимостей...
pip show allure-pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка allure-pytest...
    pip install allure-pytest
)
echo ✓ Все зависимости установлены
echo.

REM Очистка старых отчетов
echo [7/9] Очистка старых отчетов...
if exist "reports\allure-results" (
    rmdir /s /q "reports\allure-results"
)
if exist "reports\allure-report" (
    rmdir /s /q "reports\allure-report"
)
mkdir "reports\allure-results" 2>nul
echo ✓ Старые отчеты очищены
echo.

REM Запуск тестов
echo [8/9] Запуск AI-сгенерированных тестов...
echo ⏳ Это может занять несколько минут...
echo.
pytest ai_generated_tests -v --headed --html=reports/report.html --self-contained-html --alluredir=reports/allure-results

if %errorlevel% neq 0 (
    echo.
    echo ⚠ Внимание: Некоторые тесты завершились с ошибками
    echo Отчеты все равно будут сгенерированы
    echo.
)

REM Генерация Allure отчета
echo.
echo [9/9] Генерация Allure отчета...
where allure >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Внимание: Allure CLI не установлен
    echo HTML отчет будет доступен, но Allure отчет пропущен
    echo.
    goto :open_html
)

allure generate reports/allure-results -o reports/allure-report --clean
if %errorlevel% neq 0 (
    echo ✖ Не удалось сгенерировать Allure отчет
    goto :open_html
)
echo ✓ Allure отчет сгенерирован
echo.

REM Открытие отчетов
:open_html
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ПОЛНЫЙ ЦИКЛ ЗАВЕРШЕН! ОТКРЫВАЕМ ОТЧЕТЫ                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo Открываем HTML отчет...
start "" "%CD%\reports\report.html"

timeout /t 2 /nobreak >nul

if exist "reports\allure-report\index.html" (
    echo Открываем Allure отчет...
    start "" "%CD%\reports\allure-report\index.html"
    echo.
    echo ✓ Оба отчета открыты в браузере!
) else (
    echo ✓ HTML отчет открыт в браузере!
)

echo.
echo ════════════════════════════════════════════════════════════════
echo ИТОГИ:
echo   ✓ Тесты сгенерированы: ai_generated_tests\
echo   ✓ Тесты выполнены
echo   ✓ Отчеты созданы:
echo     - HTML:   reports\report.html
if exist "reports\allure-report\index.html" (
    echo     - Allure: reports\allure-report\index.html
)
echo ════════════════════════════════════════════════════════════════
echo.
echo Для повторного запуска используйте:
echo   - Только генерация: 1_generate_tests_ollama.bat
echo   - Только тесты:     2_run_tests_with_reports.bat
echo.
pause
