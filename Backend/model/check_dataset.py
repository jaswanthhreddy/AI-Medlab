import pandas as pd

df = pd.read_csv("healthcare_dataset_onehot.csv")

print("=" * 60)
print("DATASET QUALITY CHECK")
print("=" * 60)

# Check how many unique symptom combinations there are
symptom_cols = [col for col in df.columns if col not in ["Patient_ID", "Age", "Gender", "Disease"]]

print(f"\nTotal rows: {len(df)}")
print(f"\nSymptom columns ({len(symptom_cols)}):")
print(symptom_cols)

# Check symptom combinations per disease
print("\n" + "=" * 60)
print("SYMPTOM PATTERNS PER DISEASE")
print("=" * 60)

for disease in sorted(df["Disease"].unique())[:10]:  # First 10 diseases
    disease_df = df[df["Disease"] == disease]
    symptom_patterns = disease_df[symptom_cols].drop_duplicates()
    
    print(f"\n{disease}:")
    print(f"  Total samples: {len(disease_df)}")
    print(f"  Unique symptom patterns: {len(symptom_patterns)}")
    
    if len(symptom_patterns) <= 3:
        # Show the patterns
        for idx, row in symptom_patterns.iterrows():
            active_symptoms = [col for col in symptom_cols if row[col] == 1]
            print(f"    - {active_symptoms}")

# Check if there are duplicate symptom patterns across different diseases
print("\n" + "=" * 60)
print("OVERLAP CHECK")
print("=" * 60)

symptom_df = df[symptom_cols + ["Disease"]]
duplicates = symptom_df.groupby(symptom_cols)["Disease"].apply(lambda x: list(x.unique()))

# Find patterns that map to multiple diseases
problematic = {k: v for k, v in duplicates.items() if len(v) > 1}

print(f"\nSymptom patterns that map to multiple diseases: {len(problematic)}")
if len(problematic) <= 5:
    for pattern, diseases in list(problematic.items())[:5]:
        print(f"  Same symptoms -> {diseases}")
