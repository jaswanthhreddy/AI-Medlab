import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import hashlib
import json
import os
from datetime import datetime
from Backend.utils.health_recommendations import health_recommender
from utils.pdf_generator import generate_health_report_pdf

# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
# ──────────────────────────────────────────────

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

USERS_FILE    = os.path.join(BASE_DIR, "users.json")
HISTORY_FILE  = os.path.join(BASE_DIR, "patient_history.json")
REPORTS_DIR   = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

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

users_db   = load_users()
history_db = load_history()

# ── Load Model & Encoder ──────────────────────
model         = joblib.load(os.path.join(BASE_DIR, "model", "disease_prediction_model_xgb.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "model", "label_encoder.pkl"))
print("Model expects:", model.n_features_in_, "features")

# ── Load Dataset ──────────────────────────────
df = pd.read_csv(os.path.join(BASE_DIR, "model", "healthcare_dataset_onehot.csv"))
all_columns     = list(df.columns)
feature_columns = [col for col in all_columns if col not in ["Disease", "Patient_ID"]]
print("Total Features:", len(feature_columns))

gender_mapping = {"Male": 0, "Female": 1, "Other": 2}


# ── ROUTE: Remove Patient (must be OUTSIDE __main__) ──
@app.route("/remove_patient/<email>", methods=["DELETE"])
def remove_patient(email):
    try:
        if email in users_db:
            del users_db[email]
            save_users(users_db)
        if email in history_db:
            del history_db[email]
            save_history(history_db)
        return jsonify({"message": "Patient removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    non_symptom_cols = {"Patient_ID", "Age", "Gender", "Disease"}
    symptoms = [col for col in df.columns if col not in non_symptom_cols]
    return jsonify(symptoms)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        age              = data.get("age")
        gender           = data.get("gender")
        selected_symptoms = data.get("symptoms", [])
        email            = data.get("email")

        gender_num = gender_mapping.get(gender, 0) if isinstance(gender, str) else gender

        input_dict = {}
        for col in feature_columns:
            if col == "Age":       input_dict[col] = int(age)
            elif col == "Gender":  input_dict[col] = int(gender_num)
            elif col in selected_symptoms: input_dict[col] = 1
            else:                  input_dict[col] = 0

        input_df = pd.DataFrame([input_dict])[feature_columns]
        prediction_numeric  = model.predict(input_df)[0]
        predicted_disease   = label_encoder.inverse_transform([int(prediction_numeric)])[0]

        if email and email in users_db:
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "disease":   predicted_disease,
                "symptoms":  selected_symptoms,
                "age":       age,
                "gender":    gender
            }
            if email not in history_db:
                history_db[email] = []
            history_db[email].append(record)
            save_history(history_db)

        return jsonify({"predicted_disease": predicted_disease})

    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "details": traceback.format_exc()}), 500


@app.route("/")
def root():
    return send_from_directory(FRONTEND_DIR, 'dashboard.html')

@app.route("/<path:filename>")
def serve_frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route("/api/info", methods=["GET"])
def home():
    return "AI MedLab Backend Running Successfully"


@app.route("/register", methods=["POST"])
def register():
    try:
        data     = request.get_json()
        email    = data.get("email")
        password = data.get("password")
        name     = data.get("name", "User")
        role     = data.get("role", "patient")
        age      = data.get("age")
        gender   = data.get("gender")
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        if email in users_db:
            return jsonify({"error": "User already exists"}), 400
        hashed = hashlib.sha256(password.encode()).hexdigest()
        users_db[email] = {"name": name, "email": email, "password": hashed,
                           "role": role, "age": age, "gender": gender}
        save_users(users_db)
        if role == "patient" and email not in history_db:
            history_db[email] = []
            save_history(history_db)
        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data     = request.get_json()
        email    = data.get("email")
        password = data.get("password")
        if email not in users_db:
            return jsonify({"error": "Invalid credentials"}), 401
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if users_db[email]["password"] != hashed:
            return jsonify({"error": "Invalid credentials"}), 401
        return jsonify({"message": "Login successful",
                        "role": users_db[email]["role"],
                        "name": users_db[email]["name"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/all_records", methods=["GET"])
def all_records():
    try:
        records = [{"name": u.get("name"), "email": e, "role": u.get("role")}
                   for e, u in users_db.items()]
        return jsonify({"records": records, "total": len(records)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/patient_history/<email>", methods=["GET"])
def patient_history(email):
    try:
        return jsonify({"email": email, "history": history_db.get(email, [])}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/patient_history/<email>/record", methods=["DELETE"])
def delete_patient_history_record(email):
    try:
        data = request.get_json(silent=True) or {}
        ts   = data.get("prediction_timestamp")
        if not ts:
            return jsonify({"error": "prediction_timestamp is required"}), 400
        if email not in history_db or not history_db[email]:
            return jsonify({"error": "No history found for patient"}), 404
        before = len(history_db[email])
        history_db[email] = [r for r in history_db[email] if r.get("timestamp") != ts]
        if len(history_db[email]) == before:
            return jsonify({"error": "Record not found"}), 404
        save_history(history_db)
        return jsonify({"message": "History record removed successfully",
                        "remaining": len(history_db[email])}), 200
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


@app.route("/doctor/patients", methods=["GET"])
def doctor_patients():
    try:
        patients_data = []
        for email, user_data in users_db.items():
            if user_data.get("role") == "patient":
                ph = history_db.get(email, [])
                auto_tips = None
                if ph and ph[-1].get("disease"):
                    try: auto_tips = health_recommender.format_recommendations_text(ph[-1]["disease"])
                    except: pass
                patients_data.append({
                    "name": user_data.get("name"), "email": email,
                    "age": user_data.get("age"), "gender": user_data.get("gender"),
                    "history": ph, "last_prediction": ph[-1] if ph else None,
                    "auto_health_tips": auto_tips
                })
        return jsonify({"patients": patients_data, "total": len(patients_data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctor/add_health_tips", methods=["POST"])
def add_health_tips():
    try:
        data = request.get_json()
        patient_email = data.get("patient_email")
        if patient_email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        if patient_email in history_db and history_db[patient_email]:
            ts      = data.get("prediction_timestamp")
            target  = next((r for r in reversed(history_db[patient_email])
                            if r.get("timestamp") == ts), None) if ts else None
            if target is None:
                target = history_db[patient_email][-1]
            target["health_tips"]       = data.get("health_tips")
            target["appointment_date"]  = data.get("appointment_date")
            target["doctor_name"]       = data.get("doctor_name", "Unknown Doctor")
            save_history(history_db)
        return jsonify({"message": "Health tips added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/nurse/patients", methods=["GET"])
def nurse_patients():
    try:
        patients_data = []
        for email, user_data in users_db.items():
            if user_data.get("role") == "patient":
                ph = history_db.get(email, [])
                patients_data.append({
                    "name": user_data.get("name"), "email": email,
                    "age": user_data.get("age"), "gender": user_data.get("gender"),
                    "total_visits": len(ph),
                    "last_visit": ph[-1]["timestamp"] if ph else None,
                    "diseases": list(set([h["disease"] for h in ph]))
                })
        return jsonify({"patients": patients_data, "total": len(patients_data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/nurse/generate_report", methods=["POST"])
def generate_report():
    try:
        data          = request.get_json()
        patient_email = data.get("patient_email")
        if patient_email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        if patient_email in history_db and history_db[patient_email]:
            ts     = data.get("prediction_timestamp")
            target = next((r for r in reversed(history_db[patient_email])
                           if r.get("timestamp") == ts), None) if ts else None
            if target is None:
                target = history_db[patient_email][-1]
            target["nurse_report"] = data.get("report_text")
            target["report_date"]  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            target["nurse_name"]   = data.get("nurse_name", "Unknown Nurse")
            save_history(history_db)
        return jsonify({"message": "Report generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_pdf_report/<email>", methods=["POST"])
def generate_pdf_report(email):
    try:
        data = request.get_json()
        ts   = data.get("prediction_timestamp")
        if email not in users_db:
            return jsonify({"error": "Patient not found"}), 404
        if email not in history_db or not history_db[email]:
            return jsonify({"error": "No history found for patient"}), 404
        target = next((r for r in reversed(history_db[email])
                       if r.get("timestamp") == ts), None) if ts else None
        if target is None:
            target = history_db[email][-1]
        pi = users_db[email]
        pdf_data = {
            "patient_name":  pi.get("name", "Unknown Patient"),
            "patient_email": email,
            "age":           pi.get("age", "N/A"),
            "gender":        pi.get("gender", "N/A"),
            "disease":       target.get("disease", "N/A"),
            "symptoms":      target.get("symptoms", []),
            "appointment_date": target.get("appointment_date", "N/A"),
            "doctor_name":   target.get("doctor_name", "Not assigned"),
            "doctor_guidance": target.get("health_tips", "No guidance provided"),
            "nurse_name":    target.get("nurse_name", "Not assigned"),
            "nurse_report":  target.get("nurse_report", "No report available"),
            "report_date":   target.get("report_date", target.get("timestamp", "Unknown"))
        }
        pdf_path = generate_health_report_pdf(email, pdf_data, output_dir=REPORTS_DIR)
        return send_from_directory(
            os.path.dirname(pdf_path), os.path.basename(pdf_path),
            as_attachment=True, mimetype='application/pdf'
        )
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "details": traceback.format_exc()}), 500


@app.route("/health_recommendations/<disease>", methods=["GET"])
def get_health_recommendations(disease):
    try:
        return jsonify(health_recommender.get_recommendations(disease)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health_recommendations/formatted/<disease>", methods=["GET"])
def get_formatted_recommendations(disease):
    try:
        return jsonify({"disease": disease,
                        "health_tips": health_recommender.format_recommendations_text(disease)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/available_diseases", methods=["GET"])
def get_available_diseases():
    try:
        diseases = health_recommender.get_all_diseases()
        return jsonify({"diseases": diseases, "total": len(diseases)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)