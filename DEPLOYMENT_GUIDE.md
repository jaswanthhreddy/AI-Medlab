# AI Medical Lab - Complete Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Running the Application](#running-the-application)
4. [Accessing the Application](#accessing-the-application)
5. [Troubleshooting](#troubleshooting)
6. [File Structure Reference](#file-structure-reference)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.7 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 2GB free space
- **Ports Available**: 5000 (Backend), 8000 (Frontend)

### Required Software
- Python 3.7+
- pip (Python package manager, usually comes with Python)
- Git (optional, for cloning the project)

---

## Step-by-Step Setup

### Step 1: Prepare the System

#### On Windows:
```powershell
# Open Command Prompt or PowerShell as Administrator
# Check Python installation
python --version
pip --version
```

#### On macOS/Linux:
```bash
# Open Terminal
# Check Python installation
python3 --version
pip3 --version
```

### Step 2: Create Project Directory

#### Windows:
```powershell
# Navigate to desired location
cd C:\Users\YourUsername\Desktop  # or any desired location

# Create project folder
mkdir AI_Medlab
cd AI_Medlab
```

#### macOS/Linux:
```bash
cd ~/Desktop  # or any desired location
mkdir AI_Medlab
cd AI_Medlab
```

### Step 3: Create Python Virtual Environment

#### Windows:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then run Activate.ps1 again
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 4: Install Required Packages

**With virtual environment activated**:

#### Windows/macOS/Linux:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install flask flask-cors bcrypt joblib numpy xgboost scikit-learn pandas reportlab

# Or use requirements file (recommended for v2.0)
pip install -r requirement.txt
```

**v2.0 New Dependencies:**
- `pandas` - For CSV health recommendations data processing
- `reportlab` - For professional PDF health report generation

### Step 4.5: Create PDF Reports Directory

The application stores generated PDF reports in a dedicated directory:

#### Windows:
```powershell
# From project root
cd Backend
mkdir reports
```

#### macOS/Linux:
```bash
cd Backend
mkdir reports
```

This directory will store all generated health reports with format: `health_report_{email}_{timestamp}.pdf`

### Step 5: Copy Project Files

Copy the entire project structure from the original system to your new location:

```
AI_Medlab/
├── Backend/
│   ├── app.py
│   ├── config/
│   │   └── db.py
│   ├── model/
│   │   ├── healthcare_dataset_onehot.csv
│   │   ├── disease_prediction_model_xgb.pkl
│   │   ├── gender_mapping.pkl
│   │   ├── label_encoder.pkl
│   │   └── (other training files)
│   ├── routes/
│   │   ├── auth.py
│   │   └── predict.py
│   ├── utils/                    ← NEW in v2.0
│   │   ├── __init__.py
│   │   ├── health_recommendations.py
│   │   └── pdf_generator.py      ← NEW: PDF generation utility
│   ├── HealthPredict/
│   │   ├── description.csv
│   │   ├── medications.csv
│   │   ├── diets.csv
│   │   ├── precautions_df.csv
│   │   └── workout_df.csv
│   ├── reports/                  ← NEW: PDF storage directory
│   ├── users.json
│   ├── patient_history.json
│   ├── test.html (optional)
│   └── test.py (optional)
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── script.js
│   ├── style.css
│   └── (other HTML files if any)
├── venv/ (created in Step 3)
├── requirement.txt
└── DEPLOYMENT_GUIDE.md
```

### Step 6: Verify All Files Are Copied

Ensure these critical files are present:
- `Backend/app.py` - Main Flask application
- `Backend/model/disease_prediction_model_xgb.pkl` - ML model
- `Backend/model/gender_mapping.pkl` - Gender encoder
- `Backend/model/label_encoder.pkl` - Disease label encoder
- **`Backend/utils/pdf_generator.py`** - **NEW v2.0:** PDF generation utility
- **`Backend/utils/health_recommendations.py`** - Health recommendations processor
- **`Backend/HealthPredict/*.csv`** - CSV health data files (5 files)
- **`Backend/reports/`** - **NEW v2.0:** Directory for PDF storage (should be empty)
- `frontend/dashboard.html` - Main dashboard
- `frontend/script.js` - Frontend logic
- `frontend/index.html` - Login page

---

## Running the Application

### Terminal Setup

You need **TWO separate terminal windows/tabs** running simultaneously:
1. One for **Backend (Flask API)**
2. One for **Frontend (File Server)**

### Step 1: Start Backend Server

**Terminal 1 - Windows:**
```powershell
# Ensure you're in the project root
cd C:\Users\YourUsername\Desktop\AI_Medlab

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Navigate to Backend folder
cd Backend

# Run Flask app
python app.py
```

**Terminal 1 - macOS/Linux:**
```bash
cd ~/Desktop/AI_Medlab
source venv/bin/activate
cd Backend
python3 app.py
```

**Expected Output:**
```
WARNING in app.run_simple...
Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✓ Keep this terminal running - DO NOT close it

### Step 2: Start Frontend Server

**Terminal 2 - Windows:**
```powershell
# Open a NEW terminal window
# Navigate to project root
cd C:\Users\YourUsername\Desktop\AI_Medlab

# Activate virtual environment (if needed)
.\venv\Scripts\Activate.ps1

# Navigate to frontend folder
cd frontend

# Start HTTP server
python -m http.server 8000
```

**Terminal 2 - macOS/Linux:**
```bash
cd ~/Desktop/AI_Medlab
source venv/bin/activate
cd frontend
python3 -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

✓ Keep this terminal running - DO NOT close it

---

## Accessing the Application

### Open Web Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge, etc.)
2. Navigate to: **http://localhost:8000/index.html**

### Application Login

**Demo Credentials (pre-configured in system):**

#### Patient Account:
- Email: `john@example.com`
- Password: `password123`

#### Doctor Account:
- Email: `doctor@example.com`
- Password: `password123`

#### Nurse Account:
- Email: `nurse@example.com`
- Password: `password123`

### Create New Account
1. Click **"Register"** on the login page
2. Fill in:
   - Email address
   - Password
   - Select Role (Patient/Doctor/Nurse)
3. Click **"Register"** button

---

## Working with the Application

### Patient Workflow
1. Login with patient credentials
2. Enter age and select gender
3. Click dropdown to select symptoms (checkboxes)
4. Click **"Predict Disease"** button
5. View prediction results
6. View your medical history in the table below

### Doctor Workflow
1. Login with doctor credentials
2. Click **"Load All Patients"** to see all patients
3. View patient list with their predictions
4. Add health tips for patients
5. View patient appointments

### Nurse Workflow
1. Login with nurse credentials
2. Click **"Load Patient Tracking"**
3. View all patients
4. Generate nurse reports for patients

---

## Troubleshooting

### Issue 1: "Address already in use" Error

**Problem**: Port 5000 or 8000 is already in use

**Solution**:
```powershell
# Windows - Find and stop process
netstat -ano | findstr :5000  # Find process on port 5000
taskkill /PID <PID> /F  # Replace <PID> with actual number

# Or change port in app.py (line with app.run())
# Change: app.run(debug=True, port=5000)
# To: app.run(debug=True, port=5001)  # or any free port
```

```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue 2: "ModuleNotFoundError" Errors

**Problem**: Missing Python packages

**Solution**:
```bash
# Ensure virtual environment is activated
pip install flask flask-cors bcrypt joblib numpy xgboost scikit-learn

# Or
pip install -r requirement.txt
```

### Issue 3: "Cannot find model files" Error

**Problem**: Model pickle files not copied

**Solution**:
- Verify `Backend/model/` contains:
  - `disease_prediction_model_xgb.pkl`
  - `gender_mapping.pkl`
  - `label_encoder.pkl`
- Copy these files from original system

### Issue 4: "CORS Error" in Browser Console

**Problem**: Frontend can't communicate with backend

**Solution**:
- Ensure Backend is running on http://127.0.0.1:5000
- Check `Backend/app.py` has `CORS(app)` enabled
- Verify `API = "http://localhost:5000"` in `frontend/script.js`

### Issue 5: "Page not found" when accessing frontend

**Problem**: Frontend server not running

**Solution**:
- Go to Terminal 2
- Make sure you're in the `frontend` folder
- Run: `python -m http.server 8000`
- Access: http://localhost:8000/index.html

### Issue 6: Buttons/Headings Not Visible

**Problem**: CSS styling issues in dashboard

**Solution**:
- Clear browser cache: Ctrl+Shift+Del (Windows) or Cmd+Shift+Del (Mac)
- Press F5 or Ctrl+R to reload page
- Try different browser

---

## File Structure Reference

```
AI_Medlab/
│
├── Backend/
│   ├── app.py                           # Main Flask application
│   ├── config/
│   │   └── db.py                       # Database configuration
│   ├── model/
│   │   ├── disease_prediction_model_xgb.pkl  # ML model
│   │   ├── gender_mapping.pkl          # Gender encoder
│   │   ├── label_encoder.pkl           # Disease label encoder
│   │   ├── healthcare_dataset_onehot.csv     # Training data
│   │   └── train_model.py              # Model training script
│   ├── routes/
│   │   ├── auth.py                     # Authentication endpoints
│   │   └── predict.py                  # Prediction endpoints
│   ├── test.html                       # Backend test page
│   └── test.py                         # Backend tests
│
├── frontend/
│   ├── index.html                      # Login/Register page
│   ├── dashboard.html                  # Main dashboard
│   ├── script.js                       # All JS logic
│   ├── style.css                       # Styling
│   └── [other HTML if any]
│
├── venv/                               # Virtual environment (created)
├── requirement.txt                     # Python dependencies
├── DEPLOYMENT_GUIDE.md                # This file
└── README.md                          # Project info (if exists)
```

---

## Quick Start Command Summary

### Windows - All Commands in Order

```powershell
# 1. Create project
mkdir AI_Medlab
cd AI_Medlab

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install packages
pip install -r requirement.txt

# 4. In Terminal 1 - Start Backend
cd Backend
python app.py

# 5. In Terminal 2 - Start Frontend
cd frontend
python -m http.server 8000

# 6. Open browser and go to: http://localhost:8000/index.html
```

### macOS/Linux - All Commands in Order

```bash
# 1. Create project
mkdir AI_Medlab
cd AI_Medlab

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install packages
pip install -r requirement.txt

# 4. In Terminal 1 - Start Backend
cd Backend
python3 app.py

# 5. In Terminal 2 - Start Frontend
cd frontend
python3 -m http.server 8000

# 6. Open browser and go to: http://localhost:8000/index.html
```

---

## Important Notes

1. **Virtual Environment**: Always activate it before running commands
2. **Two Terminals Required**: Both Backend and Frontend must run simultaneously
3. **Ports**: Ensure ports 5000 and 8000 are not in use
4. **Model Files**: Critical - all `.pkl` files must be copied
5. **API Connection**: Frontend communicates with Backend at `http://localhost:5000`
6. **Browser**: Works with all modern browsers (Chrome, Firefox, Safari, Edge)

---

## Support Contacts

For issues or questions:
1. Check the Troubleshooting section above
2. Review console errors (F12 in browser)
3. Check terminal output for error messages
4. Verify all files are in correct locations

---

**Last Updated**: February 24, 2026
**Application Version**: 1.0
**Status**: Production Ready
