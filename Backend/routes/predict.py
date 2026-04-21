
from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
import os

predict_bp = Blueprint("predict_bp", __name__)

# ==============================
# Load Model & Dataset
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model", "disease_prediction_model_xgb.pkl")
dataset_path = os.path.join(BASE_DIR, "model", "healthcare_dataset_onehot.csv")

# Load trained model
model = joblib.load(model_path)

# Load dataset to extract feature columns & disease labels
df = pd.read_csv(dataset_path)

# Separate features and target
X = df.drop("Disease", axis=1)
y = df["Disease"]

# Create label mapping (index → disease name)
disease_mapping = dict(enumerate(y.astype("category").cat.categories))

# ==============================
# Prediction Route
# ==============================

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Convert input JSON to DataFrame
        input_df = pd.DataFrame([data])

        # Align input with training feature columns
        input_df = input_df.reindex(columns=X.columns, fill_value=0)

        # Predict
        prediction_index = int(model.predict(input_df)[0])

        # Decode disease name
        disease_name = disease_mapping.get(prediction_index, "Unknown")

        return jsonify({
            "predicted_disease": disease_name
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500