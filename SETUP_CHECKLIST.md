# AI Medical Lab - Quick Setup Checklist (v2.0)

## Pre-Installation Checklist
- [ ] Python 3.7+ installed (verify: `python --version`)
- [ ] pip installed (verify: `pip --version`)
- [ ] Ports 5000 and 8000 are available (not in use)
- [ ] 2GB free disk space available
- [ ] Administrator/sudo access if needed

---

## Installation Checklist

### 1. Environment Setup
- [ ] Project folder created (AI_Medlab)
- [ ] Changed to project directory
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated

### 2. Dependencies Installation (v2.0 Updated)
- [ ] Executed: `pip install -r requirement.txt`
- [ ] **NEW v2.0:** Verified `reportlab` installed
- [ ] **NEW v2.0:** Verified `pandas` installed
- [ ] All packages installed without errors
- [ ] Verified with: `pip list`

### 3. File Copy Verification
- [ ] Backend folder copied with all subfolders
- [ ] Frontend folder copied with all files
- [ ] Model files present in Backend/model/:
  - [ ] disease_prediction_model_xgb.pkl
  - [ ] gender_mapping.pkl
  - [ ] label_encoder.pkl
- [ ] **NEW v2.0:** Utils folder present in Backend/utils/:
  - [ ] health_recommendations.py
  - [ ] pdf_generator.py
- [ ] **NEW v2.0:** HealthPredict folder with CSV files:
  - [ ] description.csv
  - [ ] medications.csv
  - [ ] diets.csv
  - [ ] precautions_df.csv
  - [ ] workout_df.csv
- [ ] **NEW v2.0:** Reports directory created: Backend/reports/
- [ ] Python files intact:
  - [ ] Backend/app.py
  - [ ] Backend/config/db.py
  - [ ] Backend/routes/auth.py
  - [ ] Backend/routes/predict.py
  - [ ] frontend/script.js
  - [ ] frontend/dashboard.html
  - [ ] frontend/index.html

---

## Running the Application Checklist

### Terminal 1 - Backend
- [ ] Opened new terminal/PowerShell
- [ ] Navigated to backend folder
- [ ] Activated virtual environment
- [ ] Executed: `python app.py` (or `python3 app.py`)
- [ ] Confirmed: "Running on http://127.0.0.1:5000"
- [ ] Backend terminal still open

### Terminal 2 - Frontend
- [ ] Opened new terminal/PowerShell window
- [ ] Navigated to frontend folder
- [ ] Activated virtual environment (if needed)
- [ ] Executed: `python -m http.server 8000` (or `python3 -m http.server 8000`)
- [ ] Confirmed: "Serving HTTP on 0.0.0.0 port 8000"
- [ ] Frontend terminal still open

---

## Access & Login Checklist

### Browser Access
- [ ] Opened web browser (Chrome, Firefox, Safari, Edge)
- [ ] Navigated to: `http://localhost:8000/index.html`
- [ ] Page loaded successfully
- [ ] Login form visible

### Test Login
Choose one to test:
- [ ] Patient Login: john@example.com / password123
- [ ] Doctor Login: doctor@example.com / password123
- [ ] Nurse Login: nurse@example.com / password123
- [ ] Logged in successfully
- [ ] Appropriate dashboard displayed

---

## Functionality Testing Checklist

### Patient Features
- [ ] Age input accepts numbers
- [ ] Gender dropdown shows options
- [ ] Symptom selector opens/closes
- [ ] Can select multiple symptoms
- [ ] Selected symptoms display below dropdown
- [ ] Predict button is visible and clickable
- [ ] Prediction results display correctly
- [ ] Medical history table shows data
- [ ] Load History button works
- [ ] **NEW v2.0:** "📄 Download PDF Report" button visible in history
- [ ] **NEW v2.0:** PDF downloads successfully when clicked
- [ ] **NEW v2.0:** PDF contains complete patient data
- [ ] **NEW v2.0:** PDF shows doctor and nurse names

### Doctor Features
- [ ] Can see patient list
- [ ] **NEW v2.0:** Gender column displays in patient list
- [ ] Health tips modal opens
- [ ] **NEW v2.0:** Doctor Name field visible in modal
- [ ] **NEW v2.0:** Auto-generate button works
- [ ] Can add health tips with doctor name
- [ ] Tips save successfully with attribution

### Nurse Features
- [ ] Can see patient tracking list
- [ ] **NEW v2.0:** Gender column displays in patient list
- [ ] **NEW v2.0:** Remove button visible next to each patient
- [ ] **NEW v2.0:** Remove button deletes patient from list
- [ ] Nurse report modal opens
- [ ] **NEW v2.0:** Nurse Name field visible in modal
- [ ] **NEW v2.0:** Disease name auto-fills
- [ ] **NEW v2.0:** Auto-generate report button works
- [ ] Can add nurse reports with nurse name
- [ ] Reports save successfully with attribution
- [ ] **NEW v2.0:** Patient history modal shows gender
- [ ] **NEW v2.0:** PDF download button works in nurse view

---

## Troubleshooting Verification

### Port Issues
- [ ] Run: `netstat -ano | findstr :5000` (Windows) or `lsof -i :5000` (Mac/Linux)
- [ ] Identified any process using ports
- [ ] Stopped conflicting process if needed
- [ ] Restarted servers

### Module Issues
- [ ] Checked virtual environment is activated
- [ ] Ran: `pip install -r requirement.txt` again
- [ ] Verified all packages with: `pip list`

### Connection Issues
- [ ] Backend running and showing "127.0.0.1:5000"
- [ ] Frontend running and showing port 8000
- [ ] Checked browser console (F12) for CORS errors
- [ ] Confirmed `API = "http://localhost:5000"` in script.js

### File Issues
- [ ] Verified all model .pkl files exist
- [ ] Checked file permissions (readable)
- [ ] Confirmed folder structure matches documentation

---

## Performance Verification

- [ ] Application loads within 3 seconds
- [ ] Login completes in under 2 seconds
- [ ] Prediction completes in under 5 seconds
- [ ] Dashboard displays smoothly without lag
- [ ] No console errors (F12 developer tools)
- [ ] All buttons are visible and clickable
- [ ] Tables display with proper formatting

---

## Deployment Success Criteria

✓ **SUCCESS** if all the following are met:
1. Both terminals running without errors
2. Can access http://localhost:8000/index.html
3. Can login with test credentials
4. Dashboard displays correctly for logged-in role
5. All buttons and forms are functional
6. Predictions return results
7. Historical data displays properly
8. No CORS, module, or connection errors

---

## Quick Troubleshooting Commands

**Check Python version:**
```
python --version
pip --version
```

**List installed packages:**
```
pip list
```

**Check port usage:**
```
Windows: netstat -ano | findstr :5000
Mac/Linux: lsof -i :5000
```

**Reinstall packages:**
```
pip install --upgrade pip
pip install -r requirement.txt --force-reinstall
```

**Deactivate virtual environment:**
```
deactivate
```

**Reactivate virtual environment:**
```
Windows: .\venv\Scripts\Activate.ps1
Mac/Linux: source venv/bin/activate
```

---

## Next Steps After Successful Deployment

1. **Create User Accounts**
   - Register new users for each role (Patient, Doctor, Nurse)
   - Test with actual credentials

2. **Test All Workflows**
   - Patient: Make predictions, check history
   - Doctor: View patients, add health tips
   - Nurse: Track patients, generate reports

3. **Customize as Needed**
   - Modify symptoms list
   - Add more diseases
   - Adjust styling/colors
   - Retrain model with new data

4. **Backup Data**
   - BackupJSON data files regularly
   - Keep model files safe
   - Document any customizations

5. **Maintenance**
   - Monitor performance
   - Keep Python packages updated
   - Review prediction accuracy
   - Collect user feedback

---

**Date Created**: February 2026
**Version**: 2.0
**Status**: Ready for Deployment (Including PDF Generation Features)
