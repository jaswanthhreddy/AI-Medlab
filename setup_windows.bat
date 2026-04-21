@echo off
REM AI Medical Lab - Windows Automated Setup Script
REM This script automates the setup process for Windows systems

echo.
echo ================================
echo AI Medical Lab - Windows Setup v1.0
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed
    echo Try: python -m pip install --upgrade pip
    pause
    exit /b 1
)

echo [OK] pip is installed
pip --version
echo.

REM Create virtual environment
echo [1/5] Creating virtual environment...
if exist "venv" (
    echo [SKIP] Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo Try running from PowerShell with Set-ExecutionPolicy RemoteSigned
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install requirements
echo [4/5] Installing dependencies...
echo This may take 2-3 minutes...
if exist "requirement.txt" (
    pip install -r requirement.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements
        echo Check requirement.txt file
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirement.txt not found
    echo Installing packages manually...
    pip install flask flask-cors bcrypt joblib numpy xgboost scikit-learn
    if errorlevel 1 (
        echo [ERROR] Failed to install packages
        pause
        exit /b 1
    )
)
echo [OK] All dependencies installed
echo.

REM Verify files structure
echo [5/5] Verifying project structure...
if not exist "Backend\app.py" (
    echo [WARNING] Backend\app.py not found
)
if not exist "Backend\model\disease_prediction_model_xgb.pkl" (
    echo [WARNING] Model files not found in Backend\model\
)
if not exist "frontend\dashboard.html" (
    echo [WARNING] frontend\dashboard.html not found
)
if not exist "frontend\script.js" (
    echo [WARNING] frontend\script.js not found
)
echo [OK] Project structure verified
echo.

echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next Steps:
echo 1. Open TWO new terminal windows (or PowerShell tabs)
echo.
echo Terminal 1 - Run Backend:
echo   cd Backend
echo   python app.py
echo.
echo Terminal 2 - Run Frontend:
echo   cd frontend
echo   python -m http.server 8000
echo.
echo Then open browser and go to: http://localhost:8000/index.html
echo.
echo Test Credentials:
echo   Patient: john@example.com / password123
echo   Doctor: doctor@example.com / password123
echo   Nurse: nurse@example.com / password123
echo.
pause
