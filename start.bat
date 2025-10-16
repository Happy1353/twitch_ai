@echo off
REM Quick start script for Twitch AI Girl (Windows)

echo.
echo 🎀 Twitch AI Girl - Quick Start
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ⚠ Virtual environment not found. Creating...
    python -m venv venv
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import twitchio" 2>nul
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Check configuration
if not exist ".env" (
    echo ❌ Error: .env file not found
    echo Please copy .env.example to .env and configure it
    echo Run: copy .env.example .env
    pause
    exit /b 1
)

REM Run setup test
echo 🔍 Testing configuration...
python utils\test_setup.py

if errorlevel 1 (
    echo.
    echo ❌ Configuration test failed
    echo Please fix the errors above before starting
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Twitch AI Girl...
echo Press Ctrl+C to stop
echo.
python main.py

pause

