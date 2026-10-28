import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. Load dataset
df = pd.read_csv("heart.csv")
label_map = {0: "Normal", 1: "Penyakit Jantung"}
df["Target"] = df["HeartDisease"].map(label_map)

# 2. Split train/test (80% / 20%)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["Target"])

train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)

cat_features = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
num_features = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"]
all_features = num_features + cat_features

# 3. Build Scikit-Learn Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)),
])

# 4. Train model
model.fit(train_df[all_features], train_df["Target"])

# 5. Evaluate on test set
y_true = test_df["Target"]
y_pred = model.predict(test_df[all_features])

acc = float(accuracy_score(y_true, y_pred))
f1_mac = float(f1_score(y_true, y_pred, average="macro"))
cm = confusion_matrix(y_true, y_pred, labels=["Normal", "Penyakit Jantung"]).tolist()

print(f"Test Accuracy : {acc:.4f}")
print(f"Test F1 Macro : {f1_mac:.4f}")
print("Confusion Matrix:\n", np.array(cm))

# 6. Save model and metadata
joblib.dump(model, "model_heart.pkl")

# Calculate feature ranges for UI warning checks
feature_ranges = {}
for col in num_features:
    feature_ranges[col] = [float(train_df[col].min()), float(train_df[col].max())]

model_info = {
    "nama_model": "Random Forest Classifier (100 Trees, max_depth=6)",
    "dataset": "Heart Failure Prediction Dataset (Kaggle / UCI)",
    "fitur_numerik": num_features,
    "fitur_kategori": cat_features,
    "kelas": ["Normal", "Penyakit Jantung"],
    "rentang_fitur": feature_ranges,
    "kategori_pilihan": {
        "Sex": ["M", "F"],
        "ChestPainType": ["ATA", "NAP", "ASY", "TA"],
        "RestingECG": ["Normal", "ST", "LVH"],
        "ExerciseAngina": ["N", "Y"],
        "ST_Slope": ["Up", "Flat", "Down"],
    },
    "metrik": {
        "accuracy": acc,
        "f1_macro": f1_mac,
        "n_train": len(train_df),
        "n_test": len(test_df),
        "confusion_matrix": cm,
    },
    "versi": {
        "scikit-learn": "1.9.1",
        "joblib": "1.6.0",
        "pandas": "3.0.6",
    },
}

with open("model_info.json", "w") as f:
    json.dump(model_info, f, indent=2)

# 7. Create sample_test_heart.csv (15 downloadable test samples with sample patient names)
sample_names = [
    "Budi Santoso", "Siti Aminah", "Rudi Hermawan", "Dewi Sartika",
    "Agus Pratama", "Rina Marlina", "Hendra Wijaya", "Sri Mulyani",
    "Bambang Soedirgo", "Fitri Handayani", "Joko Susilo", "Nurul Hidayah",
    "Ahmad Zarkasyi", "Ratna Sari", "Eko Yulianto"
]
sample_df = test_df.sample(15, random_state=42).copy()
sample_df["Nama_Pasien"] = sample_names
cols_ordered = ["Nama_Pasien"] + all_features
sample_df[cols_ordered].to_csv("sample_test_heart.csv", index=False)
print("sample_test_heart.csv created successfully with 15 rows.")
