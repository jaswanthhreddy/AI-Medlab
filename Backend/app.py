





from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import hashlib
import json
import os
from datetime import datetime
from utils.health_recommendations import health_recommender
from utils.pdf_generator import generate_health_report_pdf

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Configure CORS properly to handle preflight requests
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Simple file-based storage (for demo purposes)
USERS_FILE = "users.json"
HISTORY_FILE = "patient_history.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

users_db = load_users()
history_db = load_history()

# -----------------------------
# Load Model and Label Encoder
# -----------------------------
model = joblib.load("model/disease_prediction_model_xgb.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

print("Model expects:", model.n_features_in_, "features")

# -----------------------------
# Load Dataset (to get columns)
# -----------------------------
df = pd.read_csv("model/healthcare_dataset_onehot.csv")

# The retrained model doesn't use Patient_ID
# Get feature columns (Age, Gender, and all symptoms)
all_columns = list(df.columns)
feature_columns = [col for col in all_columns if col not in ["Disease", "Patient_ID"]]

print("Feature Columns:", feature_columns)
print("Total Features:", len(feature_columns))

# Gender mapping
gender_mapping = {"Male": 0, "Female": 1, "Other": 2}


# =============================
# ROUTE 1: Get Symptoms
# =============================
@app.route("/symptoms", methods=["GET"])
def get_symptoms():

    # Remove non-symptom columns
    non_symptom_cols = {"Patient_ID", "Age", "Gender", "Disease"}

    symptoms = [col for col in df.columns if col not in non_symptom_cols]

    return jsonify(symptoms)


# =============================
# ROUTE 2: Predict Disease  
# =============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        age = data.get("age")
        gender = data.get("gender")  # Should be "Male", "Female", or "Other"
        selected_symptoms = data.get("symptoms", [])
        email = data.get("email")  # Patient email for history

        # Convert gender to numeric
        if isinstance(gender, str):
            gender_num = gender_mapping.get(gender, 0)
        else:
            gender_num = gender
        
        # Create input dictionary (NO Patient_ID!)
        input_dict = {}
        
        for col in feature_columns:
            if col == "Age":
                input_dict[col] = int(age)
                
            elif col == "Gender":
                input_dict[col] = int(gender_num)
                
            elif col in selected_symptoms:
                # Symptom is present
                input_dict[col] = 1
            else:
                # Symptom is absent
                input_dict[col] = 0

        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])
        
        # Ensure columns are in the correct order
        input_df = input_df[feature_columns]
        
        # Make prediction
        prediction_numeric = model.predict(input_df)[0]
        
        # Decode using label encoder
        predicted_disease = label_encoder.inverse_transform([int(prediction_numeric)])[0]
        
        # Store in history if email provided
        if email and email in users_db:
            prediction_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "disease": predicted_disease,
                "symptoms": selected_symptoms,
                "age": age,
                "gender": gender
            }
            
            if email not in history_db:
                history_db[email] = []
            
            history_db[email].append(prediction_record)
            save_history(history_db)
        
        return jsonify({
            "predicted_disease": predicted_disease
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error in prediction:", error_details)
        return jsonify({
            "error": str(e),
            "details": error_details
        }), 500


# =============================
# Home Route & Frontend Service
# =============================
@app.route("/")
def root():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route("/<path:filename>")
def serve_frontend(filename):
    return send_from_directory('../frontend', filename)

# Keep backend info endpoint
@app.route("/api/info", methods=["GET"])
def home():
    return "AI MedLab Backend Running Successfully"


# =============================
# Authentication Routes
# =============================
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        email = data.get("email")
        password = data.get("password")
        name = data.get("name", "User")
        role = data.get("role", "patient")
        age = data.get("age")
        gender = data.get("gender")
        
        # Validate required fields
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Check if user already exists
        if email in users_db:
            return jsonify({"error": "User already exists"}), 400
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Store user
        users_db[email] = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "age": age,
            "gender": gender
        }
        
        save_users(users_db)
        
        # Initialize history for patient
        if role == "patient" and email not in history_db:
            history_db[email] = []
            save_history(history_db)
        
        return jsonify({"message": "Registration successful"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        
        email = data.get("email")
        password = data.get("password")
        
        # Check if user exists
        if email not in users_db:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Verify password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if users_db[email]["password"] != hashed_password:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Return user info
        return jsonify({
            "message": "Login successful",
            "role": users_db[email]["role"],
            "name": users_db[email]["name"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# Records Route - For Doctors
# =============================
@app.route("/all_records", methods=["GET"])
def all_records():
    try:
        # Return all user information (for doctor view)
        records = []
        for email, user_data in users_db.items():
            records.append({
                "name": user_data.get("name"),
                "email": email,
                "role": user_data.get("role")
            })
        
        return jsonify({
            "records": records,
            "total": len(records)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# Patient History Routes
# =============================
@app.route("/patient_history/<email>", methods=["GET"])
def patient_history(email):
    try:
        if email in history_db:
            return jsonify({
                "email": email,
                "history": history_db[email]
            }), 200
        else:
            return jsonify({
                "email": email,
                "history": []
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/patient_history/<email>/record", methods=["DELETE"])
def delete_patient_history_record(email):
    try:
        data = request.get_json(silent=True) or {}
        prediction_timestamp = data.get("prediction_timestamp")

        if not prediction_timestamp:
            return jsonify({"error": "prediction_timestamp is required"}), 400

        if email not in history_db or not history_db[email]:
            return jsonify({"error": "No history found for patient"}), 404

        original_count = len(history_db[email])
        history_db[email] = [
            record for record in history_db[email]
            if record.get("timestamp") != prediction_timestamp
        ]

        if len(history_db[email]) == original_count:
            return jsonify({"error": "Record not found"}), 404

        save_history(history_db)
        return jsonify({
            "message": "History record removed successfully",
            "remaining": len(history_db[email])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/patient_history/<email>/clear", methods=["DELETE"])
def clear_patient_history(email):
    try:
        if email not in history_db:
            return jsonify({"error": "No history found for patient"}), 404

        history_db[email] = []
        save_history(history_db)

        return jsonify({"message": "All patient history cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# Doctor Routes - View Patient Records & Add Health Tips
# =============================
@app.route("/doctor/patients", methods=["GET"])
def doctor_patients():
    try:
        # Get all patients with their history
        patients_data = []
        for email, user_data in users_db.items():
            if user_data.get("role") == "patient":
                patient_history = history_db.get(email, [])
                
                # Get auto health tips for last disease if available
                auto_health_tips = None
                if patient_history and patient_history[-1].get("disease"):
                    last_disease = patient_history[-1]["disease"]
                    try:
                        auto_health_tips = health_recommender.format_recommendations_text(last_disease)
                    except:
                        auto_health_tips = None
                
                patients_data.append({
                    "name": user_data.get("name"),
                    "email": email,
                    "age": user_data.get("age"),
                    "gender": user_data.get("gender"),
                    "history": patient_history,
                    "last_prediction": patient_history[-1] if patient_history else None,
                    "auto_health_tips": auto_health_tips
                })
        
        return jsonify({
            "patients": patients_data,
            "total": len(patients_data)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctor/add_health_tips", methods=["POST"])
def add_health_tips():
    try:
        data = request.get_json()
        patient_email = data.get("patient_email")
        health_tips = data.get("health_tips")
        appointment_date = data.get("appointment_date")
        prediction_timestamp = data.get("prediction_timestamp")
        doctor_name = data.get("doctor_name", "Unknown Doctor")
        
        if patient_email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        
        # Store health tips in selected record (or latest if not provided)
        if patient_email in history_db and len(history_db[patient_email]) > 0:
            target_record = None
            if prediction_timestamp:
                for record in reversed(history_db[patient_email]):
                    if record.get("timestamp") == prediction_timestamp:
                        target_record = record
                        break
            if target_record is None:
                target_record = history_db[patient_email][-1]

            target_record["health_tips"] = health_tips
            target_record["appointment_date"] = appointment_date
            target_record["doctor_name"] = doctor_name
            save_history(history_db)
        
        return jsonify({"message": "Health tips added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# Nurse Routes - Patient Tracking & Report Generation
# =============================
@app.route("/nurse/patients", methods=["GET"])
def nurse_patients():
    try:
        # Get all patients for tracking
        patients_data = []
        for email, user_data in users_db.items():
            if user_data.get("role") == "patient":
                patient_history = history_db.get(email, [])
                patients_data.append({
                    "name": user_data.get("name"),
                    "email": email,
                    "age": user_data.get("age"),
                    "gender": user_data.get("gender"),
                    "total_visits": len(patient_history),
                    "last_visit": patient_history[-1]["timestamp"] if patient_history else None,
                    "diseases": list(set([h["disease"] for h in patient_history]))
                })
        
        return jsonify({
            "patients": patients_data,
            "total": len(patients_data)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/nurse/generate_report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        patient_email = data.get("patient_email")
        report_text = data.get("report_text")
        prediction_timestamp = data.get("prediction_timestamp")
        nurse_name = data.get("nurse_name", "Unknown Nurse")
        
        if patient_email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        
        # Create report entry
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nurse_report": report_text,
            "status": "pending_doctor_review"
        }
        
        # Store in selected record (or latest if not provided)
        if patient_email in history_db and len(history_db[patient_email]) > 0:
            target_record = None
            if prediction_timestamp:
                for record in reversed(history_db[patient_email]):
                    if record.get("timestamp") == prediction_timestamp:
                        target_record = record
                        break
            if target_record is None:
                target_record = history_db[patient_email][-1]

            target_record["nurse_report"] = report_text
            target_record["report_date"] = report["timestamp"]
            target_record["nurse_name"] = nurse_name
            save_history(history_db)
        
        return jsonify({"message": "Report generated successfully", "report": report}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# Generate PDF Report - For Download
# =============================
@app.route("/generate_pdf_report/<email>", methods=["POST"])
def generate_pdf_report(email):
    """Generate and return PDF report for patient"""
    try:
        data = request.get_json()
        prediction_timestamp = data.get("prediction_timestamp")
        
        if email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        
        if email not in history_db or not history_db[email]:
            return jsonify({"error": "No history found for patient"}), 404
        
        # Find the specific record
        target_record = None
        if prediction_timestamp:
            for record in reversed(history_db[email]):
                if record.get("timestamp") == prediction_timestamp:
                    target_record = record
                    break
        
        if target_record is None:
            target_record = history_db[email][-1]
        
        # Get patient info
        patient_info = users_db[email]
        
        # Prepare data for PDF
        pdf_data = {
            "patient_name": patient_info.get("name", "Unknown Patient"),
            "patient_email": email,
            "age": patient_info.get("age", "N/A"),
            "gender": patient_info.get("gender", "N/A"),
            "disease": target_record.get("disease", "N/A"),
            "symptoms": target_record.get("symptoms", []),
            "appointment_date": target_record.get("appointment_date", "N/A"),
            "doctor_name": target_record.get("doctor_name", "Not assigned"),
            "doctor_guidance": target_record.get("health_tips", "No guidance provided"),
            "nurse_name": target_record.get("nurse_name", "Not assigned"),
            "nurse_report": target_record.get("nurse_report", "No report available"),
            "report_date": target_record.get("report_date", target_record.get("timestamp", "Unknown"))
        }
        
        # Generate PDF
        pdf_path = generate_health_report_pdf(email, pdf_data)
        
        # Return file for download
        return send_from_directory(
            os.path.dirname(pdf_path),
            os.path.basename(pdf_path),
            as_attachment=True,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({"error": str(e), "details": error_details}), 500


# =============================
# Get Automatic Health Recommendations
# =============================
@app.route("/health_recommendations/<disease>", methods=["GET"])
def get_health_recommendations(disease):
    """Get comprehensive health recommendations for a disease"""
    try:
        recommendations = health_recommender.get_recommendations(disease)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health_recommendations/formatted/<disease>", methods=["GET"])
def get_formatted_recommendations(disease):
    """Get formatted health tips text for a disease"""
    try:
        formatted_text = health_recommender.format_recommendations_text(disease)
        return jsonify({
            "disease": disease,
            "health_tips": formatted_text
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/available_diseases", methods=["GET"])
def get_available_diseases():
    """Get list of all diseases with recommendations available"""
    try:
        diseases = health_recommender.get_all_diseases()
        return jsonify({
            "diseases": diseases,
            "total": len(diseases)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    
    # =============================
    # Remove Patient (Admin/Nurse/Doctor)
    # =============================
    @app.route("/remove_patient/<email>", methods=["DELETE"])
    def remove_patient(email):
        try:
            # Remove from users_db
            if email in users_db:
                del users_db[email]
                save_users(users_db)
            # Remove from history_db
            if email in history_db:
                del history_db[email]
                save_history(history_db)
            return jsonify({"message": "Patient removed successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    app.run(debug=True)
