import pandas as pd
import joblib

# Load the dataset
print("Loading dataset...")
df = pd.read_csv("healthcare_dataset_onehot.csv")

# Remove Patient_ID - it's not a useful feature
print("Removing Patient_ID...")
df = df.drop(columns=["Patient_ID"])

# Encode Gender: Male=0, Female=1, Other=2
print("Encoding Gender...")
gender_mapping = {"Male": 0, "Female": 1, "Other": 2}
df["Gender"] = df["Gender"].map(gender_mapping)

# Save gender mapping
joblib.dump(gender_mapping, "gender_mapping.pkl")
print("Saved gender_mapping.pkl")

# Prepare features and target
X = df.drop(columns=["Disease"])
y = df["Disease"]

print(f"\nDataset shape: {df.shape}")
print(f"Features: {X.shape[1]}")
print(f"Samples: {len(df)}")
print(f"Diseases: {y.nunique()}")

# Check data types
print("\nData types:")
print(X.dtypes)

# Save processed dataset for verification
df.to_csv("healthcare_dataset_processed.csv", index=False)
print("\nSaved processed dataset to healthcare_dataset_processed.csv")
