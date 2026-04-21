import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# Load dataset
df = pd.read_csv("healthcare_dataset_onehot.csv")

# Remove Patient_ID (it's not a feature, just an identifier)
df = df.drop(columns=["Patient_ID"])

# Encode Gender: Male=0, Female=1, Other=2
gender_mapping = {"Male": 0, "Female": 1, "Other": 2}
df["Gender"] = df["Gender"].map(gender_mapping)

# Save the gender mapping for future use
joblib.dump(gender_mapping, "gender_mapping.pkl")

# Ensure all columns except 'Disease' are numerical
X = df.drop(columns=["Disease"])
X = X.astype(int)  # Ensure integer type

# Encode "Disease" labels into numeric values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Disease"])  # Convert disease names to numbers

# Save the label encoder for future use
joblib.dump(label_encoder, "label_encoder.pkl")

# Split dataset into train and test sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost model
model_xgb = xgb.XGBClassifier(
    use_label_encoder=False, 
    eval_metric="mlogloss",
    n_estimators=100,  # Number of trees
    max_depth=5,  # Control complexity
    learning_rate=0.1,  # Learning rate
    random_state=42
)

# Train the model
model_xgb.fit(X_train, y_train)

# Save trained model
joblib.dump(model_xgb, "disease_prediction_model_xgb.pkl")

print("✅ Model training complete. Saved as 'disease_prediction_model_xgb.pkl'.")


# # Features (symptoms) and target (disease)
# X = df.iloc[:, 3:]  # All symptom columns
# y = df["Disease"]

# # Encode disease labels
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y)

# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
# # Convert "Disease" column to categorical numeric values
# label_encoder = LabelEncoder()
# y_train = label_encoder.fit_transform(y_train)
# y_test = label_encoder.transform(y_test)  # Transform test labels

# # Save the label encoder for future use in prediction

# joblib.dump(label_encoder, "label_encoder.pkl")


# # Train XGBoost model
# model_xgb = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=10, random_state=42, use_label_encoder=False, eval_metric="mlogloss")
# model_xgb.fit(X_train, y_train)

# # Save model & label encoder
# joblib.dump(model_xgb, "disease_prediction_model_xgb.pkl")
# joblib.dump(label_encoder, "label_encoder.pkl")

# print("Model training complete & saved.")
