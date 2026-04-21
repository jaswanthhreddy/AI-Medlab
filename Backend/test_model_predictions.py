import joblib
import pandas as pd

# Load model and components
model = joblib.load("model/disease_prediction_model_xgb.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")
df = pd.read_csv("model/healthcare_dataset_onehot.csv")

# Get feature columns
feature_columns = [col for col in df.columns if col not in ["Disease", "Patient_ID"]]

print("=" * 60)
print("MODEL DIAGNOSTICS")
print("=" * 60)
print(f"\nModel n_features_in_: {model.n_features_in_}")
print(f"Feature columns count: {len(feature_columns)}")
print(f"Feature columns: {feature_columns}")

# Test with different inputs
test_cases = [
    {"name": "Test 1: Fever + Cough", "age": 30, "gender": 0, "symptoms": ["fever", "cough"]},
    {"name": "Test 2: Headache + Dizziness", "age": 45, "gender": 1, "symptoms": ["headache", "dizziness"]},
    {"name": "Test 3: Chest pain", "age": 60, "gender": 0, "symptoms": ["chest pain", "shortness of breath"]},
    {"name": "Test 4: No symptoms", "age": 25, "gender": 1, "symptoms": []},
]

print("\n" + "=" * 60)
print("PREDICTION TESTS")
print("=" * 60)

for test in test_cases:
    print(f"\n{test['name']}")
    print(f"  Age: {test['age']}, Gender: {test['gender']}, Symptoms: {test['symptoms']}")
    
    # Build input
    input_dict = {}
    for col in feature_columns:
        if col == "Age":
            input_dict[col] = test['age']
        elif col == "Gender":
            input_dict[col] = test['gender']
        elif col in test['symptoms']:
            input_dict[col] = 1
        else:
            input_dict[col] = 0
    
    # Create DataFrame
    input_df = pd.DataFrame([input_dict])
    input_df = input_df[feature_columns]
    
    # Debug: print the actual values being sent
    print(f"  Input shape: {input_df.shape}")
    print(f"  Input values: {input_df.values[0][:5]}... (first 5 features)")
    
    # Make prediction
    try:
        pred_numeric = model.predict(input_df)[0]
        pred_disease = label_encoder.inverse_transform([int(pred_numeric)])[0]
        print(f"  ✓ Prediction: {pred_disease}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
