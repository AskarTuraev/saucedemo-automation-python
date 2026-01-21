@echo off
REM ========================================
REM Setup AI-Driven QA Pipeline
REM ========================================

echo.
echo ================================
echo AI-Driven QA Pipeline Setup
echo ================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.12+
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists, skipping...
)

REM Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo.
echo [4/6] Installing Python dependencies (this may take a few minutes)...
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo [5/6] Installing Playwright browsers...
playwright install chromium

REM Install Spacy model
echo.
echo [6/6] Installing Spacy NLP model...
python -m spacy download en_core_web_sm

REM Check .env file
echo.
echo ================================
echo Checking .env configuration...
echo ================================
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo.
    echo Please create .env file with the following content:
    echo.
    echo OPENAI_API_KEY=sk-your-key-here
    echo ANTHROPIC_API_KEY=sk-ant-your-key-here
    echo APPLITOOLS_API_KEY=your-applitools-key
    echo BASE_URL=https://www.saucedemo.com
    echo BROWSER=chromium
    echo HEADLESS=false
    echo TEST_USERNAME=standard_user
    echo TEST_PASSWORD=secret_sauce
    echo.
    echo Get your OpenAI API key from: https://platform.openai.com/
    echo.
) else (
    echo .env file found!
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Make sure .env file is configured with your API keys
echo 2. Run: quick_test.bat (to test the full pipeline)
echo 3. Or run: test_pii.bat (to test PII detection only)
echo.
pause
