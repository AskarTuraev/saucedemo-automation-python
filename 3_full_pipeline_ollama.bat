@echo off
REM ========================================================================
REM FULL PIPELINE: Generate + Run + Reports (Ollama)
REM ========================================================================

echo.
echo ====================================================================
echo   FULL AI TESTING PIPELINE (OLLAMA - FREE)
echo ====================================================================
echo.
echo This script will:
echo   1. Generate tests with AI (5-10 minutes)
echo   2. Run tests
echo   3. Create reports
echo   4. Open reports in browser
echo.
echo Total time: 10-15 minutes
echo.
pause

REM ========================================
REM STAGE 1: Generate Tests
REM ========================================

echo.
echo ====================================================================
echo   STAGE 1/2: TEST GENERATION
echo ====================================================================
echo.

REM Check Ollama
echo [1/9] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Ollama not found!
    echo.
    echo Please install Ollama:
    echo 1. Download: https://ollama.ai/download
    echo 2. Install OllamaSetup.exe
    echo 3. Run: ollama pull llama2
    echo.
    pause
    exit /b 1
)
echo OK: Ollama is installed
echo.

REM Check model
echo [2/9] Checking llama2 model...
ollama list | findstr llama2 >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Model llama2 not found
    echo Downloading model (~4GB, may take 5-10 minutes)...
    ollama pull llama2
)
echo OK: Model llama2 is ready
echo.

REM Activate venv
echo [3/9] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)
call venv\Scripts\activate
echo OK: Virtual environment activated
echo.

REM Create requirements
echo [4/9] Creating requirements file...
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
echo OK: Requirements created
echo.

REM Remove old tests
if exist "ai_generated_tests" (
    echo [5/9] Removing old generated tests...
    rmdir /s /q "ai_generated_tests"
    echo OK: Old tests removed
    echo.
)

REM Generate tests
echo [5/9] Generating autotests with AI...
echo NOTE: This may take 5-10 minutes (Ollama is slower but FREE)
echo.
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output ai_generated_tests

REM Check result
if not exist "ai_generated_tests" (
    echo.
    echo ERROR: Test generation failed!
    pause
    exit /b 1
)

echo.
echo OK: Tests generated successfully!
echo.

REM ========================================
REM STAGE 2: Run Tests and Reports
REM ========================================

echo.
echo ====================================================================
echo   STAGE 2/2: RUN TESTS AND GENERATE REPORTS
echo ====================================================================
echo.

REM Check dependencies
echo [6/9] Checking dependencies...
pip show allure-pytest >nul 2>&1
if errorlevel 1 (
    echo Installing allure-pytest...
    pip install allure-pytest
)
echo OK: All dependencies installed
echo.

REM Clean old reports
echo [7/9] Cleaning old reports...
if exist "reports\allure-results" (
    rmdir /s /q "reports\allure-results"
)
if exist "reports\allure-report" (
    rmdir /s /q "reports\allure-report"
)
mkdir "reports\allure-results" 2>nul
echo OK: Old reports cleaned
echo.

REM Run tests
echo [8/9] Running AI-generated tests...
echo NOTE: This may take a few minutes...
echo.
pytest ai_generated_tests -v --headed --html=reports/report.html --self-contained-html --alluredir=reports/allure-results

if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed
    echo Reports will be generated anyway
    echo.
)

REM Generate Allure report
echo.
echo [9/9] Generating Allure report...
where allure >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Allure CLI not installed
    echo HTML report will be available, but Allure report skipped
    echo.
    goto :open_html
)

allure generate reports/allure-results -o reports/allure-report --clean
if errorlevel 1 (
    echo ERROR: Failed to generate Allure report
    goto :open_html
)
echo OK: Allure report generated
echo.

REM Open reports
:open_html
echo.
echo ====================================================================
echo   FULL PIPELINE COMPLETE! OPENING REPORTS
echo ====================================================================
echo.

echo Opening HTML report...
start "" "%CD%\reports\report.html"

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
echo SUMMARY:
echo   OK: Tests generated: ai_generated_tests\
echo   OK: Tests executed
echo   OK: Reports created:
echo     - HTML:   reports\report.html
if exist "reports\allure-report\index.html" (
    echo     - Allure: reports\allure-report\index.html
)
echo ====================================================================
echo.
echo To run again:
echo   - Generate only: 1_generate_tests_ollama.bat
echo   - Run only:      2_run_tests_with_reports.bat
echo.
pause
