@echo off
chcp 65001 >nul
REM ========================================================================
REM ШАГ 2: Запуск тестов с автоматическими отчетами
REM ========================================================================
REM
REM Этот скрипт:
REM 1. Запускает все тесты (из tests/ или ai_generated_tests/)
REM 2. Генерирует HTML отчет и Allure отчет
REM 3. Автоматически открывает отчеты в браузере
REM
REM Используйте после: 1_generate_tests_ollama.bat
REM ========================================================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ШАГ 2: ЗАПУСК ТЕСТОВ И ГЕНЕРАЦИЯ ОТЧЕТОВ                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Активация виртуального окружения
echo [1/5] Активация виртуального окружения...
if not exist "venv\Scripts\activate.bat" (
    echo ✖ ОШИБКА: Виртуальное окружение не найдено!
    echo Запустите сначала: setup.bat
    pause
    exit /b 1
)
call venv\Scripts\activate
echo ✓ Виртуальное окружение активировано
echo.

REM Установка allure-pytest если нужно
echo [2/5] Проверка зависимостей...
pip show allure-pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка allure-pytest...
    pip install allure-pytest
)
echo ✓ Все зависимости установлены
echo.

REM Очистка старых отчетов
echo [3/5] Очистка старых отчетов...
if exist "reports\allure-results" (
    rmdir /s /q "reports\allure-results"
)
if exist "reports\allure-report" (
    rmdir /s /q "reports\allure-report"
)
mkdir "reports\allure-results" 2>nul
echo ✓ Старые отчеты очищены
echo.

REM Определение папки с тестами
set TEST_DIR=tests
if exist "ai_generated_tests" (
    set /p USE_AI="Обнаружена папка ai_generated_tests. Запустить эти тесты? (y/n): "
    if /i "%USE_AI%"=="y" set TEST_DIR=ai_generated_tests
)

REM Запуск тестов
echo [4/5] Запуск тестов из папки: %TEST_DIR%
echo ⏳ Это может занять несколько минут...
echo.
pytest %TEST_DIR% -v --headed --html=reports/report.html --self-contained-html --alluredir=reports/allure-results

REM Проверка результата
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Внимание: Некоторые тесты завершились с ошибками
    echo Отчеты все равно будут сгенерированы
    echo.
)

REM Генерация Allure отчета
echo.
echo [5/5] Генерация Allure отчета...
where allure >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Внимание: Allure CLI не установлен
    echo HTML отчет доступен, но Allure отчет пропущен
    echo.
    echo Установите Allure CLI:
    echo   scoop install allure
    echo   ИЛИ
    echo   Скачайте: https://github.com/allure-framework/allure2/releases
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
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ГОТОВО! ОТКРЫВАЕМ ОТЧЕТЫ                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Открываем HTML отчет...
start "" "%CD%\reports\report.html"

REM Задержка перед открытием Allure
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
echo ════════════════════════════════════════════════════════════
echo ОТЧЕТЫ:
echo   - HTML:   reports\report.html
if exist "reports\allure-report\index.html" (
    echo   - Allure: reports\allure-report\index.html
)
echo ════════════════════════════════════════════════════════════
echo.
pause
