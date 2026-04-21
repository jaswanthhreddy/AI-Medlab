# AI Medical Lab - Troubleshooting & FAQ

## Frequently Asked Questions

### Q1: What if I get "Address already in use" error?

**Error Message**:
```
OSError: [Errno 48] Address already in use
Address already in use: ('127.0.0.1', 5000)
```

**Solution**:

**Windows**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID 12345 /F

# Or change port in Backend/app.py:
# Find: if __name__ == '__main__':
#       app.run(debug=True)
# Change to:
#       app.run(debug=True, port=5001)
```

**macOS/Linux**:
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port in app.py
```

---

### Q2: Python modules not found errors

**Error Messages**:
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'xgboost'
```

**Solution**:
```bash
# Make sure virtual environment is activated
# Windows:
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# Then install:
pip install -r requirement.txt

# If still failing, reinstall:
pip install --force-reinstall flask flask-cors xgboost joblib numpy bcrypt scikit-learn
```

---

### Q3: "Cannot find model file" error

**Error Message**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'model/disease_prediction_model_xgb.pkl'
```

**Solution**:
1. Verify file structure:
   ```
   Backend/
   └── model/
       ├── disease_prediction_model_xgb.pkl  ✓ Must exist
       ├── gender_mapping.pkl                ✓ Must exist
       ├── label_encoder.pkl                 ✓ Must exist
       └── healthcare_dataset_onehot.csv
   ```

2. Copy model files from original system:
   - Get all `.pkl` files from original Backend/model/
   - Copy to your Backend/model/ directory
   - Verify files are not corrupted

3. If files are corrupted:
   ```bash
   cd Backend/model
   python train_model.py  # Retrain models
   ```

---

### Q4: CORS errors in browser console

**Error**:
```
Access to XMLHttpRequest at 'http://localhost:5000/...' from origin 'http://localhost:8000' 
has been blocked by CORS policy
```

**Solution**:
1. Verify Backend is running on `http://127.0.0.1:5000`
2. Check `Backend/app.py` contains:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

3. Verify `frontend/script.js` has:
   ```javascript
   API = "http://localhost:5000"
   ```

4. If still failing, restart both servers:
   - Stop backend (Ctrl+C in Terminal 1)
   - Stop frontend (Ctrl+C in Terminal 2)
   - Start again in order: Backend first, then Frontend

---

### Q5: Page shows "Cannot GET /dashboard.html"

**Cause**: Frontend server not running

**Solution**:
```bash
# In Terminal 2, from frontend folder:
cd frontend
python -m http.server 8000

# Or Python 3:
python3 -m http.server 8000

# Access via: http://localhost:8000/index.html
```

---

### Q6: Login not working

**Symptoms**: Credentials not accepted even with demo accounts

**Solution**:

1. **Clear browser cache**:
   - Chrome/Edge: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Safari: Safari > Clear History

2. **Check browser console** (F12):
   - Look for error messages
   - Check network tab for failed requests

3. **Verify data files exist**:
   ```bash
   # In Backend folder, check:
   - users.json (should contain registered users)
   - patient_history.json (should contain patient records)
   ```

4. **Reset demo data**:
   - Create new accounts instead of using demo accounts
   - Or restore original `users.json` from backup

---

### Q7: Prediction gives wrong results

**Cause**: Model not loaded correctly or feature mismatch

**Solution**:

1. **Verify model files**:
   ```bash
   cd Backend/model
   python test_current_model.py
   ```

2. **Check symptom mapping**:
   - Ensure all 20 symptoms are sent correctly
   - Feature order must match training data

3. **Retrain model**:
   ```bash
   cd Backend/model
   python train_model.py
   ```

---

### Q8: Application very slow or freezing

**Cause**: CPU/Memory issues or blocking operations

**Solution**:

1. **Check available resources**:
   - Windows: Task Manager
   - macOS: Activity Monitor
   - Linux: `top` command

2. **Reduce parallel operations**:
   - Close unnecessary applications
   - Clear browser cache

3. **Check network connectivity**:
   - Ensure both servers are responsive
   - Test with: `curl http://localhost:5000/symptoms`

4. **Profile the application**:
   ```bash
   # Add timing to Flask
   import time
   start = time.time()
   # ... operation ...
   print(f"Duration: {time.time() - start}s")
   ```

---

### Q9: How do I stop the servers?

**Process**:
1. In Terminal 1 (Backend):
   - Press `Ctrl+C`
   - Wait for graceful shutdown

2. In Terminal 2 (Frontend):
   - Press `Ctrl+C`
   - Wait for termination

3. Verify ports are free:
   ```bash
   # Windows:
   netstat -ano | findstr :5000
   netstat -ano | findstr :8000
   
   # macOS/Linux:
   lsof -i :5000
   lsof -i :8000
   ```

---

### Q10: How do I run on a different port?

**Backend** - Edit `Backend/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed from 5000
```

**Frontend** - Edit command:
```bash
python -m http.server 8001  # Changed from 8000
```

**Then update script.js**:
```javascript
API = "http://localhost:5001"  // Changed from 5000
```

---

## Common Errors & Quick Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Missing package | `pip install -r requirement.txt` |
| `Port already in use` | Process running on port | `netstat -ano \| findstr :5000` then `taskkill /PID xxx /F` |
| `FileNotFoundError: model file` | Model not copied | Copy `.pkl` files to Backend/model/ |
| `CORS error` | Frontend can't reach backend | Ensure backend running, check API setting |
| `Cannot GET /` | Frontend not running | Run `python -m http.server 8000` in frontend folder |
| `Login failed` | Wrong credentials/no users | Check users.json, create account if needed |
| `Empty prediction` | Missing symptoms | Select at least one symptom |
| `No prediction history` | No predictions made | Make a prediction first |
| `Page not updating` | JavaScript error | Check console (F12), reload page |
| `Buttons not visible` | CSS issue | Clear cache, reload, check CSS |

---

## v2.0 Feature Troubleshooting

### Q10: PDF Generation Errors

**Error Message**:
```
ModuleNotFoundError: No module named 'reportlab'
```

**Solution**:
```bash
# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# Install reportlab
pip install reportlab pandas

# Or reinstall all requirements
pip install -r requirement.txt
```

---

### Q11: PDF Download Button Not Working

**Symptoms**:
- Button doesn't respond
- Download doesn't start
- 500 Internal Server Error

**Solutions**:

1. **Check Backend Reports Directory**:
   ```bash
   # Create if missing
   cd Backend
   mkdir reports
   
   # Verify permissions
   # Windows:
   icacls reports /grant Users:F
   
   # macOS/Linux:
   chmod 755 reports
   ```

2. **Verify doctor_name and nurse_name fields exist**:
   - Doctor must have entered name when adding health tips
   - Nurse must have entered name when creating report
   - Check patient_history.json for these fields

3. **Check browser console**:
   ```javascript
   // Error: "doctor_name or nurse_name missing"
   // Solution: Re-create the report with names entered
   ```

4. **Test PDF endpoint directly**:
   ```bash
   # Test with curl (replace email and timestamp)
   curl -X POST http://localhost:5000/generate_pdf_report/patient@example.com \
     -H "Content-Type: application/json" \
     -d '{"prediction_timestamp":"2026-02-24 10:30:45"}'
   ```

---

### Q12: PDF Contains Incomplete Data

**Symptoms**:
- PDF missing doctor or nurse name
- "Not Provided" appears in PDF
- Blank sections in report

**Solutions**:

1. **Ensure names were entered in modals**:
   - Doctor Health Tips modal has "Doctor Name" field
   - Nurse Report modal has "Nurse Name" field
   - These fields are required for complete PDF

2. **Re-create reports with names**:
   - Have doctor add health tips again with name
   - Have nurse generate report again with name
   - Download new PDF

3. **Check data in patient_history.json**:
   ```json
   {
     "history": [{
       "doctor_name": "Dr. John Smith",  // Must be present
       "nurse_name": "Nurse Sarah Johnson",  // Must be present
       "health_tips": "...",
       "nurse_report": "..."
     }]
   }
   ```

---

### Q13: Gender Column Not Showing in Nurse View

**Symptoms**:
- Gender column missing from nurse patient list
- Gender shows as "undefined" or "N/A"

**Solutions**:

1. **Update user registration**:
   - Older accounts may not have gender field
   - Have patients re-register or update profile
   - Verify gender is stored in users.json

2. **Check JavaScript console**:
   ```javascript
   // Press F12 > Console
   // Look for: "gender property missing"
   ```

3. **Verify users.json structure**:
   ```json
   {
     "users": [{
       "email": "patient@example.com",
       "name": "John Doe",
       "gender": "Male",  // Must be present
       "age": 35
     }]
   }
   ```

---

### Q14: "Remove Patient" Button Not Working

**Symptoms**:
- Button visible but doesn't remove patient
- Error in console
- Patient reappears after page refresh

**Solutions**:

1. **Check DELETE endpoint**:
   ```bash
   # Test directly
   curl -X DELETE http://localhost:5000/patient_history/patient@example.com/clear
   ```

2. **Browser console errors**:
   - Press F12 > Console
   - Look for fetch errors or CORS issues
   - Verify API endpoint in script.js

3. **Permissions check**:
   - Ensure patient_history.json is writable
   - Check file permissions

---

### Q15: ReportLab StyleSheet Errors

**Error Message**:
```
Exception: Style 'BodyText' already defined in stylesheet
```

**Solution**:
This is already fixed in v2.0 code. If you still see this error:

1. **Update pdf_generator.py**:
   ```python
   # In _setup_custom_styles method
   # Check if style exists before adding:
   if 'BodyText' not in self.styles:
       self.styles.add(ParagraphStyle(...))
   ```

2. **Restart Flask server**:
   ```bash
   # Press Ctrl+C in Backend terminal
   # Run again:
   python app.py
   ```

---

## Performance Optimization Tips

### 1. Reduce API Response Time
```bash
# Add caching to Flask
pip install Flask-Caching

# In Backend/app.py:
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/symptoms')
@cache.cached(timeout=3600)
def get_symptoms():
    # Symptoms change rarely, cache for 1 hour
    ...
```

### 2. Optimize Frontend
```javascript
// Debounce API calls
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Use: toggleSymptomDropdown = debounce(toggleSymptomDropdown, 300);
```

### 3. Database Optimization
```python
# Current: JSON files
# For production, migrate to:
# - PostgreSQL for relational data
# - MongoDB for document-based data
# - Redis for session caching
```

---

## Testing Guide

### Unit Testing Backend

**Create `Backend/test_api.py`**:
```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_register():
    data = {
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User",
        "role": "patient"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    assert response.status_code == 200
    print("✓ Register test passed")

def test_login():
    data = {
        "email": "test@example.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200
    print("✓ Login test passed")

def test_symptoms():
    response = requests.get(f"{BASE_URL}/symptoms")
    assert response.status_code == 200
    data = response.json()
    assert "symptoms" in data
    print(f"✓ Symptoms test passed ({len(data['symptoms'])} symptoms)")

def test_predict():
    data = {
        "age": 35,
        "gender": 0,
        "symptoms": ["Fever", "Cough"]
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "predicted_disease" in result
    print(f"✓ Prediction test passed: {result['predicted_disease']}")

if __name__ == "__main__":
    print("Running API tests...")
    test_register()
    test_login()
    test_symptoms()
    test_predict()
    print("\n✓ All tests passed!")
```

**Run tests**:
```bash
cd Backend
pip install requests
python test_api.py
```

---

## Debugging Tips

### 1. Enable Debug Logging
```python
# In Backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In Flask route
@app.route('/predict', methods=['POST'])
def predict():
    print("DEBUG: Received prediction request")
    print(f"DEBUG: Data = {request.json}")
    # ... rest of code ...
```

### 2. Browser Console Debugging
```javascript
// In frontend/script.js
console.log("DEBUG: Calling predict with", selectedSymptoms);
async function predict() {
    console.time("prediction");
    // ... code ...
    console.timeEnd("prediction");
}
```

### 3. Network Inspection
1. Open Browser DevTools (F12)
2. Go to Network tab
3. Make API call
4. Check request/response details
5. Verify status codes (200 = OK)

---

## Migration from Test to Production

### 1. Security Hardening
```python
# Install security packages
pip install python-dotenv Flask-SQLAlchemy

# Use environment variables
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

### 2. Database Migration
```bash
# Instead of JSON, use PostgreSQL
pip install psycopg2-binary flask-sqlalchemy

# In config file:
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/aimedlab'
```

### 3. Production Server
```bash
# Use gunicorn instead of Flask built-in
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 Backend.app:app
```

### 4. HTTPS Support
```bash
# Install certificate (use Let's Encrypt)
pip install certifi

# Run with SSL:
app.run(ssl_context=('cert.pem', 'key.pem'))
```

---

## Support Resources

### When You Need Help:

1. **Check Error Message**: Search first part of error
2. **Review Console Logs**: F12 > Console for JavaScript errors
3. **Check Terminal Output**: Look at server logs
4. **Test API Directly**: 
   ```bash
   curl http://localhost:5000/symptoms
   ```
5. **Verify Configuration**:
   - Check API endpoint in script.js
   - Verify ports are correct
   - Ensure model files exist

### Useful Commands

```bash
# Test connectivity
curl http://localhost:5000/symptoms
curl http://localhost:8000/index.html

# Check Python version
python --version

# List installed packages
pip list | grep flask
pip list | grep xgboost

# View application structure
tree AI_Medlab /L

# Count lines of code
wc -l *.py *.js *.html
```

---

**Document Updated**: February 2026
**Version**: 2.0
**Status**: Comprehensive Troubleshooting Guide (Including v2.0 PDF Generation Features)
