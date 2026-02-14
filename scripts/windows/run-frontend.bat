@echo off
REM =============================================================================
REM Cyberbullying Detection Web GUI - Windows Launcher
REM =============================================================================

echo Starting Web GUI...
echo.

REM Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "%~dp0..\web\node_modules" (
    echo Installing dependencies...
    cd "%~dp0..\web"
    call npm install
)

REM Start the frontend
cd "%~dp0..\web"
call npm run dev

pause
