import joblib
import pandas as pd
import numpy as np

# Load model and label encoder
model = joblib.load("model/disease_prediction_model_xgb.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Load dataset
df = pd.read_csv("model/healthcare_dataset_onehot.csv")

print("=" * 50)
print("MODEL INFO")
print("=" * 50)
print(f"Model expects {model.n_features_in_} features")
print(f"\nFeature columns from dataset: {len(df.columns) - 1} (excluding Disease)")

# Get feature columns (everything except Disease)
X = df.drop("Disease", axis=1)
print(f"\nActual feature columns: {list(X.columns)}")

print("\n" + "=" * 50)
print("LABEL ENCODER INFO")
print("=" * 50)
print(f"Label Encoder Classes: {label_encoder.classes_}")
print(f"\nNumber of diseases: {len(label_encoder.classes_)}")

# Show mapping
print("\nLabel Encoder Mapping:")
for i, disease in enumerate(label_encoder.classes_):
    print(f"  {i} -> {disease}")

print("\n" + "=" * 50)
print("TESTING PREDICTION")
print("=" * 50)

# Test with a sample from the dataset
sample = X.iloc[0:1]
print(f"\nTest input (first row from dataset):")
print(sample)

prediction_numeric = model.predict(sample)[0]
print(f"\nModel prediction (numeric): {prediction_numeric}")

predicted_disease = label_encoder.inverse_transform([int(prediction_numeric)])[0]
print(f"Predicted disease (decoded): {predicted_disease}")

actual_disease = df.iloc[0]["Disease"]
print(f"Actual disease: {actual_disease}")

print("\n" + "=" * 50)
print("TESTING MULTIPLE SAMPLES")
print("=" * 50)

# Test with 5 different samples
for i in range(5):
    sample = X.iloc[i:i+1]
    prediction_numeric = model.predict(sample)[0]
    predicted_disease = label_encoder.inverse_transform([int(prediction_numeric)])[0]
    actual_disease = df.iloc[i]["Disease"]
    
    match = "✓" if predicted_disease == actual_disease else "✗"
    print(f"{match} Row {i}: Predicted={predicted_disease}, Actual={actual_disease}")
