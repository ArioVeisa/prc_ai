import joblib
import pandas as pd

model = joblib.load("model_status_akademik.pkl")
contoh = pd.DataFrame([{
    "ipk": 3.45, "kehadiran": 92, "jam_belajar": 12,
    "tugas_terkumpul": 95, "nilai_uts": 82, "aktif_organisasi": "Ya",
}])
print("Prediksi :", model.predict(contoh)[0])
proba = model.predict_proba(contoh)[0]
for kelas, p in zip(model.classes_, proba):
    print(f"  {kelas:9s}: {p:.3f}")
