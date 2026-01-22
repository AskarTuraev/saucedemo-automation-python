@echo off
REM ========================================================================
REM STEP 2: Run Tests with Automatic Reports
REM ========================================================================

echo.
echo ====================================================================
echo   STEP 2: RUN TESTS AND GENERATE REPORTS
echo ====================================================================
echo.

REM Activate venv
echo [1/5] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)
call venv\Scripts\activate
echo OK: Virtual environment activated
echo.

REM Install allure-pytest if needed
echo [2/5] Checking dependencies...
pip show allure-pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing allure-pytest...
    pip install allure-pytest
)
echo OK: All dependencies installed
echo.

REM Clean old reports
echo [3/5] Cleaning old reports...
if exist "reports\allure-results" (
    rmdir /s /q "reports\allure-results"
)
if exist "reports\allure-report" (
    rmdir /s /q "reports\allure-report"
)
mkdir "reports\allure-results" 2>nul
echo OK: Old reports cleaned
echo.

REM Determine test directory
set TEST_DIR=tests
if exist "ai_generated_tests" (
    set /p USE_AI="Found ai_generated_tests folder. Run these tests? (y/n): "
    if /i "%USE_AI%"=="y" set TEST_DIR=ai_generated_tests
)

REM Run tests
echo [4/5] Running tests from folder: %TEST_DIR%
echo NOTE: This may take a few minutes...
echo.
pytest %TEST_DIR% -v --headed --html=reports/report.html --self-contained-html --alluredir=reports/allure-results

REM Check result
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some tests failed
    echo Reports will be generated anyway
    echo.
)

REM Generate Allure report
echo.
echo [5/5] Generating Allure report...
where allure >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Allure CLI not installed
    echo HTML report available, but Allure report skipped
    echo.
    echo Install Allure CLI:
    echo   scoop install allure
    echo   OR
    echo   Download: https://github.com/allure-framework/allure2/releases
    echo.
    goto :open_html
)

allure generate reports/allure-results -o reports/allure-report --clean
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate Allure report
    goto :open_html
)
echo OK: Allure report generated
echo.

REM Open reports
:open_html
echo.
echo ====================================================================
echo   DONE! OPENING REPORTS
echo ====================================================================
echo.

echo Opening HTML report...
start "" "%CD%\reports\report.html"

REM Delay before opening Allure
timeout /t 2 /nobreak >nul

if exist "reports\allure-report\index.html" (
    echo Opening Allure report...
    start "" "%CD%\reports\allure-report\index.html"
    echo.
    echo OK: Both reports opened in browser!
) else (
    echo OK: HTML report opened in browser!
)

echo.
echo ====================================================================
echo REPORTS:
echo   - HTML:   reports\report.html
if exist "reports\allure-report\index.html" (
    echo   - Allure: reports\allure-report\index.html
)
echo ====================================================================
echo.
pause
