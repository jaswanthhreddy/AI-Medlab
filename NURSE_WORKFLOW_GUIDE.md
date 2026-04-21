# Nurse Report Generation Workflow (v2.0)

## Overview
The nurse workflow now includes comprehensive patient management features:
- ✅ **Auto-generated health reports** from CSV medical database
- ✅ **PDF report generation** with doctor/nurse attribution
- ✅ **Gender tracking** for complete patient demographics
- ✅ **Patient removal** capability for efficient list management
- ✅ **Streamlined UI** with clean tables and download buttons

## Complete Workflow

### Step 1: Doctor Provides Health Tips & Appointment
1. Doctor logs in and views **Patient Records** table (with gender column)
2. Doctor clicks **"View History"** for a patient
3. Doctor sees patient's prediction history (latest first)
4. Doctor clicks **"+ Add Tips"** button on any prediction
5. **Doctor enters their name** (e.g., "Dr. John Smith") - **NEW v2.0**
6. Doctor can:
   - **Auto-Generate Tips**: Click button to auto-fill from health CSV data
   - **Manually Enter**: Type custom health recommendations
   - **Set Appointment**: Select appointment date
7. Doctor clicks **"✅ Submit"** to save tips + appointment date **with doctor name attribution**

### Step 2: Nurse Generates Comprehensive Report
1. Nurse logs in and views **📭 Patient Tracking** table showing:
   - Name | Age | **Gender** | Email | View History | **Remove** - **NEW v2.0**
2. Nurse can **remove patients** no longer under care using Remove button - **NEW v2.0**
3. Nurse clicks **"View History"** for a patient
4. Nurse sees patient's complete prediction history modal with:
   - Date & Time
   - Disease
   - **Gender** column - **NEW v2.0**
   - Symptoms
   - Nurse Report status (if any)
   - **Report button** for each prediction
5. Nurse clicks **"➕ Report"** on the prediction they need to report on
6. **Report Modal Opens** showing:
   - **Nurse Name** input field - **NEW v2.0** (e.g., "Nurse Sarah Johnson")
   - Patient Email (read-only, auto-filled)
   - **Disease Name** (auto-filled from selected prediction)
   - Report Text Area (empty, ready for input)
   - **"🤖 Auto-Generate Report" button**

### Step 3: Auto-Generate Health Report
1. Nurse enters their name in the "Nurse Name" field - **NEW v2.0**
2. Nurse clicks **"🤖 Auto-Generate Report"** button
3. System fetches health recommendations from CSV files for the disease:
   - 📋 **Disease Description** - Medical background
   - 💊 **Medications** - Treatment drugs
   - 🥗 **Diet & Nutrition** - Recommended foods
   - ⚠️ **Precautions** - Things to avoid
   - 💪 **Workouts & Exercise** - Physical activity recommendations
4. All recommendations auto-populate in the text area
5. **Nurse can then:**
   - ✏️ Edit the recommendations (add personal observations)
   - Add vital signs (BP, Temp, HR, RR)
   - Add patient-specific notes
   - Add any clinical observations
6. Click **"✅ Submit"** to save the comprehensive report **with nurse name attribution**

### Step 4: Patient Views & Downloads Complete Health Report
1. Patient logs in and sees **"📋 Your Prediction History"** table
2. Table shows for each prediction:
   - 📅 Date & Time of prediction
   - 🏥 Disease diagnosed
   - 🤒 Symptoms
   - 💊 Health Tips (from doctor with name attribution)
   - 📆 Appointment Date (scheduled by doctor)
   - 📄 **"Download PDF Report" button** - **NEW v2.0** (replaces long text)
3. **Patient clicks "Download PDF Report" button** - **NEW v2.0**
4. **Professional PDF generates including:**
   - Patient information (name, email, age, gender)
   - Disease diagnosis and symptoms
   - Appointment date
   - **Doctor Name** and health guidance
   - **Nurse Name** and clinical report
   - Professional healthcare formatting
5. PDF automatically downloads to patient's device

## Data Flow

```
CSV Files (Backend/HealthPredict/)
├─ description.csv      → Medical condition overview
├─ diets.csv           → Nutritional recommendations
├─ medications.csv     → Drug treatments
├─ precautions_df.csv  → Things to avoid
└─ workout_df.csv      → Exercise recommendations
         ↓
Health Recommendations Utility
         ↓
         ├─ Doctor Uses (Health Tips)
         │  └─→ Auto-generate suggestions for patient treatment
         │
         └─ Nurse Uses (Comprehensive Report) ✨ NEW
            └─→ Auto-generate health guidance with medical details

         ↓ Both populate in
Patient's Complete Health History
```

## Key Features

### For Doctors 👨‍⚕️ (v2.0 Enhanced)
- View patient list with **gender column** - **NEW v2.0**
- Access full patient history from history modal
- **Enter doctor name** for attribution - **NEW v2.0**
- **Auto-generate health tips** using CSV data
- Set appointment dates
- Track multiple predictions per patient

### For Nurses 👩‍⚕️ (v2.0 Enhanced)
- View patient list with **gender column** - **NEW v2.0**
- **Remove patients** no longer under care - **NEW v2.0**
- Access full patient history modal with gender displayed - **NEW v2.0**
- **Enter nurse name** for attribution - **NEW v2.0**
- **Auto-generate comprehensive reports** using CSV data
- Add personal clinical observations to auto-generated reports
- **Download PDF reports** from patient history modal - **NEW v2.0**
- Track patient progress over time
- Link reports to specific predictions with timestamps

### For Patients 🏥 (v2.0 Enhanced)
- View complete prediction history in clean table format
- See health tips **from named doctor** - **NEW v2.0**
- See clinical reports **from named nurse** - **NEW v2.0**
- **Download professional PDF health reports** - **NEW v2.0**
- PDF includes all medical information with provider attribution
- Access reports anytime from history table
- Professional documentation for personal records or sharing
- View all their medical predictions (latest first)
- See doctor's health recommendations and appointments
- See nurse's comprehensive health report
- Track their health conditions and treatment progress
- Get access to complete medical information

## CSV Data Used

The system uses 5 health recommendation CSV files covering **41 diseases**:

1. **Disease Description** - Medical background & overview
2. **Medications** - Prescribed drugs & dosage info
3. **Diets** - Recommended and restricted foods
4. **Precautions** - Lifestyle adjustments & safety measures
5. **Workouts** - Exercise programs & physical activity

### Example Report Auto-Generation

**Disease:** Diabetes

**Auto-Generated Report includes:**
```
📋 DISEASE DESCRIPTION:
Diabetes is a chronic metabolic disorder...

💊 MEDICATIONS:
Metformin, Insulin, Glibenclamide...

🥗 DIET RECOMMENDATIONS:
- Include whole grains
- Avoid sugar & sweets
- Eat vegetables & proteins...

⚠️ PRECAUTIONS:
- Monitor blood sugar regularly
- Avoid stress
- Regular check-ups...

💪 EXERCISE:
- 30 minutes daily walking
- Yoga for flexibility
- Avoid strenuous exercise initially...
```

**Nurse can then edit & add:**
- Vital signs (BP 120/80, Sugar 150mg/dL)
- Patient's current medications
- Progress observations
- Any complications or changes
- Follow-up recommendations

## Technical Implementation

### Backend Changes
- `/nurse/generate_report` endpoint now supports prediction_timestamp
- Reports are stored in patient prediction records with timestamp
- All health recommendations accessible via `/health_recommendations/formatted/<disease>`

### Frontend Changes
- Report modal now shows disease name (auto-filled)
- New button: "🤖 Auto-Generate Report"
- Function: `autoGenerateNurseReport()` fetches CSV-based recommendations
- Disease info passed from history modal to report form

### Data Storage
- Patient history stores: health_tips, appointment_date, nurse_report, report_date
- All linked to specific prediction timestamps
- Patient sees complete workflow in one history table

## Workflow Benefits

✅ **Consistency** - Both doctor and nurse use same CSV data source
✅ **Comprehensive Care** - Patient gets medical guidelines from doctor + detailed report from nurse
✅ **Time-Saving** - Auto-generate features speed up data entry
✅ **Customizable** - Both roles can edit auto-generated content
✅ **Complete History** - All information stored per prediction in one place
✅ **Patient-Centric** - Patient sees complete health journey in one view

## Summary

The new workflow enables:
1. **Doctor** → Provides health tips + appointments (using CSV data for consistency)
2. **Nurse** → Generates comprehensive reports (using same CSV data + personal observations)
3. **Patient** → Receives complete health profile (doctor tips + nurse report in one history view)

All powered by the shared **health recommendation CSV database** for accuracy and consistency.
