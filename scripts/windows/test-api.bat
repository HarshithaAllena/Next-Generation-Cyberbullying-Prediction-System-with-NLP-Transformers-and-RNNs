@echo off
REM =============================================================================
REM Test API Endpoint - Windows
REM =============================================================================

echo Testing API Gateway...
echo.

curl -X POST http://localhost:3000/classify -H "Content-Type: application/json" -d "{\"text\": \"Hello world\", \"include_explanation\": false}"

echo.
echo.
pause
