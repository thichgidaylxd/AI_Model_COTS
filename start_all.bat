@echo off
echo =====================================
echo Disease Prediction - Start All
echo =====================================
echo.

echo Starting API Server...
start "API Server" cmd /k "python run.py"

timeout /t 3 /nobreak > nul

echo.
echo Starting Test Server...
start "Test Server" cmd /k "python serve_test.py"

echo.
echo =====================================
echo Servers are starting...
echo =====================================
echo.
echo API Server: http://localhost:5000
echo Test Page: http://localhost:8000/test.html
echo.
echo Press any key to close this window...
pause > nul