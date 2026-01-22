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
if errorlevel 1 (
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
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed
    echo Reports will be generated anyway
    echo.
)

REM Generate Allure report
echo.
echo [5/5] Generating Allure report...
where allure >nul 2>&1
if errorlevel 1 (
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
if errorlevel 1 (
    echo ERROR: Failed to generate Allure report
    goto :open_html
)
echo OK: Allure report generated
echo.

REM Display report summary
:open_html
echo.
echo ====================================================================
echo   TEST EXECUTION COMPLETED
echo ====================================================================
echo.

REM Check report files
if exist "reports\report.html" (
    echo [HTML REPORT]
    echo   File:   reports\report.html
    echo   Path:   %CD%\reports\report.html
    echo   Status: READY
    echo.
) else (
    echo [HTML REPORT]
    echo   Status: NOT FOUND
    echo.
)

if exist "reports\allure-report\index.html" (
    echo [ALLURE REPORT]
    echo   File:   reports\allure-report\index.html
    echo   Path:   %CD%\reports\allure-report\index.html
    echo   Status: READY
    echo.
) else (
    echo [ALLURE REPORT]
    echo   Status: NOT GENERATED (Allure CLI not installed)
    echo.
)

echo ====================================================================
echo   OPENING REPORTS IN BROWSER
echo ====================================================================
echo.

REM Open reports
if exist "reports\report.html" (
    echo [1/2] Opening HTML report...
    start "" "%CD%\reports\report.html"
    timeout /t 1 /nobreak >nul
) else (
    echo [ERROR] HTML report not found
)

if exist "reports\allure-report\index.html" (
    echo [2/2] Opening Allure report...
    start "" "%CD%\reports\allure-report\index.html"
    timeout /t 1 /nobreak >nul
    echo.
    echo OK: Both reports opened in browser!
) else (
    echo.
    echo OK: HTML report opened in browser!
)

echo.
echo ====================================================================
echo   EXECUTION SUMMARY
echo ====================================================================
echo.
echo Test execution completed successfully
echo Reports generated and opened in your browser
echo.
echo Available reports:
if exist "reports\report.html" (
    echo   - HTML:   reports\report.html
)
if exist "reports\allure-report\index.html" (
    echo   - Allure: reports\allure-report\index.html
)
echo.
echo ====================================================================
echo.
echo TIP: Scroll up in this window to review test execution logs
echo      You can see all test results, errors, and warnings
echo.
echo ====================================================================
echo Close this window when done reviewing, or press any key...
echo ====================================================================
pause >nul
