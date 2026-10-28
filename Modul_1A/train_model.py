# ===== 1. Import library =====
import json
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (accuracy_score, f1_score,
                             classification_report, confusion_matrix)

# ===== 2. Muat dan kenali data =====
df = pd.read_csv("dataset_status_akademik.csv")
print(df.shape)
print(df.head())
print(df.isna().sum())
print(pd.crosstab(df["status"], df["bagian"]))

# ===== 3. Pisahkan fitur & label sesuai kolom "bagian" =====
FITUR_NUMERIK = ["ipk", "kehadiran", "jam_belajar", "tugas_terkumpul", "nilai_uts"]
FITUR_KATEGORI = ["aktif_organisasi"]
FITUR = FITUR_NUMERIK + FITUR_KATEGORI

train = df[df["bagian"] == "train"]
test = df[df["bagian"] == "test"]            # data test yang SAMA dipakai di Modul 2A
X_train, y_train = train[FITUR], train["status"]
X_test, y_test = test[FITUR], test["status"]
print("Train:", X_train.shape, "| Test:", X_test.shape)

# ===== 4. Preprocessing + Deep Neural Network dalam satu Pipeline =====
preprocess = ColumnTransformer([
    ("num", StandardScaler(), FITUR_NUMERIK),
    ("cat", OneHotEncoder(handle_unknown="ignore"), FITUR_KATEGORI),
])

dnn = MLPClassifier(
    hidden_layer_sizes=(64, 32, 16),   # 3 hidden layer
    activation="relu",
    solver="adam",
    alpha=1e-3,                        # regularisasi L2
    learning_rate_init=1e-3,
    max_iter=500,
    early_stopping=True,               # 10% data train dipakai sebagai validasi
    validation_fraction=0.1,
    n_iter_no_change=20,
    random_state=42,
)

model = Pipeline([("preprocess", preprocess), ("dnn", dnn)])

# ===== 5. Training =====
model.fit(X_train, y_train)
mlp = model.named_steps["dnn"]
print("Epoch berjalan:", mlp.n_iter_)
print("Akurasi validasi terbaik:", round(max(mlp.validation_scores_), 4))

# ===== 6. Evaluasi pada data test =====
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="macro")
print(f"Accuracy : {acc:.4f}")
print(f"F1 macro : {f1:.4f}")
print(classification_report(y_test, y_pred))

LABEL = ["Aman", "Waspada", "Berisiko"]
cm = confusion_matrix(y_test, y_pred, labels=LABEL)
print(pd.DataFrame(cm, index=[f"asli_{l}" for l in LABEL],
                   columns=[f"pred_{l}" for l in LABEL]))

# Baseline: selalu menebak kelas terbanyak
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
f1_base = f1_score(y_test, baseline.predict(X_test), average="macro")
print(f"F1 baseline: {f1_base:.4f}")

# ===== 7. Gerbang evaluasi & simpan model =====
TARGET_F1 = 0.80
if f1 >= TARGET_F1 and f1 > f1_base:
    joblib.dump(model, "model_status_akademik.pkl")
    info = {
        "nama_model": "DNN (MLPClassifier 64-32-16)",
        "fitur_numerik": FITUR_NUMERIK,
        "fitur_kategori": FITUR_KATEGORI,
        "kelas": list(model.classes_),
        "rentang_fitur": {c: [float(df[c].min()), float(df[c].max())] for c in FITUR_NUMERIK},
        "metrik": {"accuracy": round(acc, 4), "f1_macro": round(f1, 4),
                   "f1_baseline": round(f1_base, 4), "n_test": int(len(y_test))},
        "versi": {"scikit-learn": sklearn.__version__, "pandas": pd.__version__,
                  "numpy": np.__version__, "joblib": joblib.__version__},
    }
    with open("model_info.json", "w") as f:
        json.dump(info, f, indent=2)
    print("LOLOS evaluasi -> model_status_akademik.pkl & model_info.json disimpan")
else:
    print(f"BELUM LOLOS (F1 {f1:.4f} < {TARGET_F1}) -> perbaiki model, jangan deploy")
