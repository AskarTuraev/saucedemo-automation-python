@echo off
REM ========================================================================
REM STEP 1: Generate Tests with AI (Ollama - FREE)
REM ========================================================================

echo.
echo ====================================================================
echo   STEP 1: AI TEST GENERATION (OLLAMA - FREE)
echo ====================================================================
echo.

REM Check Ollama
echo [1/6] Checking Ollama installation...
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
echo [2/6] Checking llama2 model...
ollama list | findstr llama2 >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Model llama2 not found
    echo Downloading model (~4GB, may take 5-10 minutes)...
    ollama pull llama2
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to download model
        pause
        exit /b 1
    )
)
echo OK: Model llama2 is ready
echo.

REM Activate venv
echo [3/6] Activating virtual environment...
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
echo [4/6] Creating requirements file...
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
echo OK: Requirements created: quick_requirements.txt
echo.

REM Generate tests
echo [5/6] Generating autotests with AI...
echo NOTE: This may take 5-10 minutes (Ollama is slower but FREE)
echo.
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output ai_generated_tests

REM Check result
if not exist "ai_generated_tests" (
    echo.
    echo ERROR: Test generation failed!
    echo Check error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo [6/6] Tests generated successfully!
echo.
echo ====================================================================
echo   DONE! Tests created in: ai_generated_tests\
echo ====================================================================
echo.
echo Contents:
dir ai_generated_tests /b
echo.
echo ====================================================================
echo NEXT STEP: Run tests and get reports
echo.
echo Run: 2_run_tests_with_reports.bat
echo ====================================================================
echo.
pause
