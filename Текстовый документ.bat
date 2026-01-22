batch@echo off
echo Закрытие VS Code...
taskkill /F /IM "Code.exe" 2>nul
timeout /t 2 /nobreak > nul

echo Очистка данных...
rmdir /s /q "%APPDATA%\Code\User\globalStorage\anthropic.claude-code" 2>nul

echo Запуск VS Code...
start code

echo.
echo Теперь удалите и установите расширение вручную:
echo 1. В VS Code откройте Extensions (Ctrl+Shift+X)
echo 2. Найдите Claude Code и удалите его
echo 3. Установите заново из Marketplace
echo.
pause