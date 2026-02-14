@echo off
REM =============================================================================
REM Cyberbullying Detection API Gateway - Windows Launcher
REM =============================================================================

echo Starting API Gateway...
echo.

REM Set Python path for Windows
set PYTHONPATH=%~dp0..\apps\feature-service\src;%~dp0..\packages\data-models\src;%~dp0..packages\shared-common\src;%~dp0..apps\api-gateway\src;%PYTHONPATH%

REM Start the API Gateway
python -m uvicorn apps.api-gateway.src.main:app --host 0.0.0.0 --port 3000

pause
