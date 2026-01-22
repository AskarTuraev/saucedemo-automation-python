@echo off
REM ========================================
REM Test PII Detection Module
REM ========================================

echo.
echo ================================
echo Testing PII Detection
echo ================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Create test file with PII
echo [1/3] Creating test file with sensitive data...
echo Feature: User Registration > pii_test.txt
echo. >> pii_test.txt
echo User Details: >> pii_test.txt
echo Email: john.doe@company.com >> pii_test.txt
echo API Key: sk_live_abc123xyz456789 >> pii_test.txt
echo Phone: +1-555-0100 >> pii_test.txt
echo SSN: 123-45-6789 >> pii_test.txt
echo Credit Card: 4532-1234-5678-9010 >> pii_test.txt

echo.
echo Original file content:
echo -----------------------
type pii_test.txt

REM Run PII detection
echo.
echo.
echo [2/3] Running PII Detection...
python -m ai_qa_pipeline.modules.pii_detection.cli pii_test.txt -f -o pii_safe.txt -s fake --report

REM Show results
echo.
echo.
echo [3/3] Sanitized file content:
echo -----------------------
type pii_safe.txt

echo.
echo ================================
echo PII Detection Test Complete!
echo ================================
echo.
echo Compare the two files:
echo - Original: pii_test.txt
echo - Sanitized: pii_safe.txt
echo.
pause
