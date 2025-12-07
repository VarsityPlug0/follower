@echo off
REM Instagram Automation Tool Runner
REM This script runs the Instagram automation tool with common parameters

echo Instagram Automation Tool
echo ========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "instagram_automation.py" (
    echo Error: instagram_automation.py not found
    echo Please run this script from the project directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install/update dependencies
echo Installing/updating dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Failed to install dependencies
    echo Continuing with execution...
)

REM Run the automation tool
echo Starting Instagram automation...
python instagram_automation.py %*

echo.
echo Automation completed.
pause