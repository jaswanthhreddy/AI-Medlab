import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("Retraining model (FAST VERSION)...")

# Load data
df = pd.read_csv("healthcare_dataset_onehot.csv")

# Remove Patient_ID - it's just an identifier, not a feature!
df = df.drop(columns=["Patient_ID"])

# Encode Gender
gender_map = {"Male": 0, "Female": 1, "Other": 2}
df["Gender"] = df["Gender"].map(gender_map)

# Split features and target
X = df.drop(columns=["Disease"])
y = df["Disease"]

# Encode disease labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data (smaller test set for faster training)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.1, random_state=42, stratify=y_encoded
)

# Train model with fewer trees for speed
import xgboost as xgb
model = xgb.XGBClassifier(
    n_estimators=50,  # Fewer trees for speed
    max_depth=3,
    learning_rate=0.3,
    random_state=42,
    tree_method='hist',
    use_label_encoder=False,
    eval_metric='mlogloss'
)

print(f"Training on {len(X_train)} samples with {X.shape[1]} features...")
model.fit(X_train, y_train)

# Evaluate
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print(f"✅ Training complete!")
print(f"   Train accuracy: {train_acc:.4f}")
print(f"   Test accuracy: {test_acc:.4f}")

# Save
joblib.dump(model, "disease_prediction_model_xgb.pkl")
joblib.dump(le, "label_encoder.pkl")
joblib.dump(gender_map, "gender_mapping.pkl")

print(f"✅ Model saved! ({model.n_features_in_} features)")
print(f"   Features: {list(X.columns)}")
