@echo off
REM ========================================
REM Quick Test - AI-Driven QA Pipeline
REM ========================================

echo.
echo ================================
echo AI-Driven QA Pipeline - Quick Test
echo ================================
echo.

REM Activate virtual environment
echo [1/5] Activating virtual environment...
call venv\Scripts\activate

REM Create test requirements
echo.
echo [2/5] Creating test requirements...
echo Feature: SauceDemo Login > quick_requirements.txt
echo As a user I want to login to SauceDemo >> quick_requirements.txt
echo So that I can access the product catalog >> quick_requirements.txt
echo. >> quick_requirements.txt
echo Scenario: Successful login >> quick_requirements.txt
echo Given I am on the login page >> quick_requirements.txt
echo When I enter username 'standard_user' >> quick_requirements.txt
echo And I enter password 'secret_sauce' >> quick_requirements.txt
echo And I click login button >> quick_requirements.txt
echo Then I should see the inventory page >> quick_requirements.txt

REM Run full pipeline
echo.
echo [3/5] Running AI Pipeline (this may take 2-3 minutes)...
python -m ai_qa_pipeline.modules.code_generation.cli full quick_requirements.txt --base-url https://www.saucedemo.com --llm openai --output quick_tests

REM Check if generation successful
if not exist "quick_tests" (
    echo.
    echo ERROR: Test generation failed!
    echo Please check your OPENAI_API_KEY in .env file
    pause
    exit /b 1
)

echo.
echo [4/5] Generated tests successfully!
dir quick_tests

REM Run tests
echo.
echo [5/5] Running tests...
cd quick_tests
pytest -v --headed

REM Return to root
cd ..

echo.
echo ================================
echo COMPLETE! Check quick_tests/ folder
echo ================================
pause
