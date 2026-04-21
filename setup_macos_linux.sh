#!/bin/bash

# AI Medical Lab - macOS/Linux Automated Setup Script
# This script automates the setup process for macOS and Linux systems

echo ""
echo "================================"
echo "AI Medical Lab - Setup v1.0"
echo "================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.7+ from python.org or using:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3"
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not installed"
    echo "Try: python3 -m pip install --upgrade pip"
    exit 1
fi

echo "[OK] pip3 is installed"
pip3 --version
echo ""

# Create virtual environment
echo "[1/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "[SKIP] Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"
echo ""

# Upgrade pip
echo "[3/5] Upgrading pip..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
echo "[OK] pip upgraded"
echo ""

# Install requirements
echo "[4/5] Installing dependencies..."
echo "This may take 2-3 minutes..."

if [ -f "requirement.txt" ]; then
    pip3 install -r requirement.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install requirements"
        echo "Check requirement.txt file"
        exit 1
    fi
else
    echo "[WARNING] requirement.txt not found"
    echo "Installing packages manually..."
    pip3 install flask flask-cors bcrypt joblib numpy xgboost scikit-learn
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install packages"
        exit 1
    fi
fi
echo "[OK] All dependencies installed"
echo ""

# Verify files structure
echo "[5/5] Verifying project structure..."
[ ! -f "Backend/app.py" ] && echo "[WARNING] Backend/app.py not found"
[ ! -f "Backend/model/disease_prediction_model_xgb.pkl" ] && \
    echo "[WARNING] Model files not found in Backend/model/"
[ ! -f "frontend/dashboard.html" ] && echo "[WARNING] frontend/dashboard.html not found"
[ ! -f "frontend/script.js" ] && echo "[WARNING] frontend/script.js not found"
echo "[OK] Project structure verified"
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next Steps:"
echo "1. Open TWO new terminal windows"
echo ""
echo "Terminal 1 - Run Backend:"
echo "  source venv/bin/activate"
echo "  cd Backend"
echo "  python3 app.py"
echo ""
echo "Terminal 2 - Run Frontend:"
echo "  source venv/bin/activate"
echo "  cd frontend"
echo "  python3 -m http.server 8000"
echo ""
echo "Then open browser and go to: http://localhost:8000/index.html"
echo ""
echo "Test Credentials:"
echo "  Patient: john@example.com / password123"
echo "  Doctor: doctor@example.com / password123"
echo "  Nurse: nurse@example.com / password123"
echo ""
echo "To deactivate virtual environment later, run: deactivate"
echo ""
