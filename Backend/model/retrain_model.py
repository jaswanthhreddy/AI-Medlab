import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("=" * 60)
print("TRAINING MODEL WITH CORRECTED FEATURES")
print("=" * 60)

# Load processed dataset
print("\nLoading processed dataset...")
df = pd.read_csv("healthcare_dataset_processed.csv")

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Prepare features and target
X = df.drop(columns=["Disease"])
y = df["Disease"]

print(f"\nFeatures shape: {X.shape}")
print(f"Data types:\n{X.dtypes}")

# Encode disease labels
print("\nEncoding disease labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"Number of unique diseases: {len(label_encoder.classes_)}")

# Split data
print("\nSplitting dataset (80-20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train XGBoost model
print("\nTraining XGBoost model...")

try:
    import xgboost as xgb
    
    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric="mlogloss",
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        tree_method='hist'  # Faster training
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\n✅ Training completed!")
    print(f"Train accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    # Save model and label encoder
    joblib.dump(model, "disease_prediction_model_xgb.pkl")
    joblib.dump(label_encoder, "label_encoder.pkl")
    
    print(f"\n✅ Model saved as 'disease_prediction_model_xgb.pkl'")
    print(f"✅ Label encoder saved as 'label_encoder.pkl'")
    
    print("\n" + "=" * 60)
    print("MODEL INFO")
    print("=" * 60)
    print(f"Number of features: {model.n_features_in_}")
    print(f"Feature names: {list(X.columns)}")
    
except ImportError as e:
    print(f"\n❌ Error importing XGBoost: {e}")
    print("Please install xgboost: pip install xgboost")
except Exception as e:
    print(f"\n❌ Error during training: {e}")
    import traceback
    traceback.print_exc()
