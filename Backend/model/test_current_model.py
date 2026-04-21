import joblib
import pandas as pd
import numpy as np

print("=" * 60)
print("TESTING CURRENT MODEL")
print("=" * 60)

# Load model and data
model = joblib.load("disease_prediction_model_xgb.pkl")
df = pd.read_csv("healthcare_dataset_onehot.csv")

print(f"\nModel expects {model.n_features_in_} features")

# Get first 5 rows excluding Disease
X_test = df.drop("Disease", axis=1).head(5)

print(f"\nTest data shape: {X_test.shape}")
print(f"Columns: {list(X_test.columns)}")
print(f"\nData types:\n{X_test.dtypes}")

print("\n" + "-" * 60)
print("ATTEMPTING PREDICTION WITH RAW DATA (strings)")
print("-" * 60)
try:
    predictions = model.predict(X_test)
    print(f"✅ SUCCESS! Predictions: {predictions}")
except Exception as e:
    print(f"❌ FAILED: {str(e)}")

print("\n" + "-" * 60)
print("ATTEMPTING PREDICTION WITH ENCODED DATA")
print("-" * 60)

# Try encoding strings to numbers
X_test_encoded = X_test.copy()

# Encode Patient_ID: Extract numbers from "P1", "P2", etc.
X_test_encoded["Patient_ID"] = X_test_encoded["Patient_ID"].str.replace("P", "").astype(int)

# Encode Gender
gender_map = {"Male": 0, "Female": 1, "Other": 2}
X_test_encoded["Gender"] = X_test_encoded["Gender"].map(gender_map)

print(f"\nEncoded data types:\n{X_test_encoded.dtypes}")
print(f"\nFirst row:\n{X_test_encoded.iloc[0]}")

try: 
    predictions = model.predict(X_test_encoded)
    label_encoder = joblib.load("label_encoder.pkl")
    
    print(f"\n✅ SUCCESS!")
    print("\nPredictions:")
    for i, pred in enumerate(predictions):
        predicted_disease = label_encoder.inverse_transform([int(pred)])[0]
        actual_disease = df.iloc[i]["Disease"]
        match = "✓" if predicted_disease == actual_disease else "✗"
        print(f"  {match} Row {i}: Predicted={predicted_disease}, Actual={actual_disease}")
        
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
