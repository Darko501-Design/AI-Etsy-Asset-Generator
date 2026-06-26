@echo off
echo ===================================================
echo Starting AI Etsy Asset Generator...
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH. 
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if virtual environment exists
if not exist "venv\" (
    echo [1/3] First time setup: Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install requirements
echo [2/3] Checking and installing required packages...
pip install -r requirements.txt

:: Disable Streamlit email prompt for first-time users
set STREAMLIT_EMAIL=

:: Run Streamlit
echo [3/3] Opening your Web App...
echo Please wait a moment, a browser window should open automatically.
streamlit run app.py --browser.gatherUsageStats false

pause
