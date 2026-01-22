@echo off
REM ========================================
REM Quick Test - AI-Driven QA Pipeline
REM Using Ollama (FREE, no API key needed)
REM ========================================

echo.
echo ================================
echo AI-Driven QA Pipeline - Quick Test
echo Using Ollama (FREE)
echo ================================
echo.

REM Check if Ollama is installed
echo [1/6] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama not found!
    echo.
    echo Please install Ollama:
    echo 1. Download from: https://ollama.ai/download
    echo 2. Install OllamaSetup.exe
    echo 3. Run: ollama pull llama2
    echo.
    pause
    exit /b 1
)

echo Ollama found!

REM Check if model is available
echo.
echo [2/6] Checking if llama2 model is available...
ollama list | findstr llama2 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Model llama2 not found. Downloading...
    echo This will download ~4GB, please wait...
    ollama pull llama2
)

echo Model ready!

REM Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate

REM Create test requirements
echo.
echo [4/6] Creating test requirements...
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

REM Run full pipeline with Ollama
echo.
echo [5/6] Running AI Pipeline with Ollama...
echo This may take 5-10 minutes (Ollama is slower than OpenAI but FREE)
echo.
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm ollama --model llama2 --output quick_tests_ollama

REM Check if generation successful
if not exist "quick_tests_ollama" (
    echo.
    echo ERROR: Test generation failed!
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo [6/6] Generated tests successfully!
dir quick_tests_ollama

REM Run tests
echo.
echo [6/6] Running tests...
cd quick_tests_ollama
pytest -v --headed

REM Return to root
cd ..

echo.
echo ================================
echo COMPLETE! Check quick_tests_ollama/ folder
echo ================================
echo.
echo Note: Ollama is FREE but slower than OpenAI
echo For faster results, use OpenAI with quick_test.bat
echo.
pause
