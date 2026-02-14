@echo off
REM =============================================================================
REM Cyberbullying Detection - Windows Setup Script
REM =============================================================================

echo ============================================
echo Cyberbullying Detection - Windows Setup
echo ============================================
echo.

REM Check Python version
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Installing Python dependencies...
pip install structlog tenacity pydantic pyyaml python-dotenv orjson fastapi uvicorn

echo.
echo [2/5] Checking Node.js...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Node.js not found. Web GUI requires Node.js.
    echo Install from https://nodejs.org/
) else (
    echo [3/5] Installing Web GUI dependencies...
    cd "%~dp0..\web"
    call npm install
)

echo.
echo [4/5] Verifying project structure...
if exist "%~dp0..apps\api-gateway\src\main.py" (
    echo   - API Gateway: OK
)
if exist "%~dp0..apps\feature-service\src\feature_service\extractor.py" (
    echo   - Feature Service: OK
)
if exist "%~dp0..web\package.json" (
    echo   - Web GUI: OK
)

echo.
echo [5/5] Setup complete!
echo.
echo To run the application:
echo   1. Run run-api.bat to start the backend
echo   2. Run run-frontend.bat to start the web GUI
echo.
echo Default URLs:
echo   - API:    http://localhost:3000
echo   - Web:    http://localhost:5173
echo   - API Docs: http://localhost:3000/docs
echo.
pause
