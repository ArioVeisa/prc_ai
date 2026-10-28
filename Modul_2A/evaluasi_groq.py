# ===== 1. Import & koneksi ke LLM Service =====
import json
import os
import time
from datetime import date

import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from classifier import NAMA_FITUR, classify

load_dotenv()                                   # membaca konfigurasi dari file .env
api_key = os.getenv("API_KEY") or os.getenv("GROQ_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

if base_url:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
else:
    from groq import Groq
    client = Groq(api_key=api_key)

# ===== 2. Muat dataset (SAMA dengan Modul 1A) =====
df = pd.read_csv("dataset_status_akademik.csv")
FITUR = list(NAMA_FITUR)                        # ipk, kehadiran, ..., aktif_organisasi
LABELS = ["Aman", "Waspada", "Berisiko"]

train = df[df["bagian"] == "train"]
test = df[df["bagian"] == "test"]               # 200 data test yang SAMA dengan Modul 1A

# data validasi: 10 per kelas, diambil dari data TRAIN (untuk memilih prompt)
val = train.groupby("status").sample(10, random_state=7)
pool = train.drop(val.index)                    # sumber contoh few-shot (tidak tumpang tindih)
print("Validasi:", len(val), "| Test:", len(test))


# ===== 3. Fungsi evaluasi =====
def evaluasi(cfg, data, jeda=1):
    prediksi = []
    for i, (_, baris) in enumerate(data.iterrows(), start=1):
        prediksi.append(classify(client, cfg, baris[FITUR].to_dict()))
        print(f"\r{i}/{len(data)}", end="")
        time.sleep(jeda)                        # jaga batas request/token per menit (free tier)
    print()
    y_true = data["status"].tolist()
    hasil = {
        "accuracy": round(accuracy_score(y_true, prediksi), 4),
        "f1_macro": round(f1_score(y_true, prediksi, labels=LABELS, average="macro", zero_division=0), 4),
        "invalid": prediksi.count("invalid"),
        "n": len(data),
    }
    print(hasil)
    print(classification_report(y_true, prediksi, labels=LABELS, zero_division=0))
    print(pd.DataFrame(confusion_matrix(y_true, prediksi, labels=LABELS),
                       index=[f"asli_{l}" for l in LABELS], columns=[f"pred_{l}" for l in LABELS]))
    return hasil, prediksi


# ===== 4. Iterasi 1: zero-shot (hanya instruksi) =====
PROMPT_DASAR = (
    "Kamu adalah sistem klasifikasi status akademik mahasiswa.\n"
    "Data: IPK (2,00-4,00), kehadiran kuliah (%), jam belajar mandiri per minggu, "
    "tugas terkumpul (%), nilai UTS (0-100), dan keaktifan organisasi.\n"
    "Label:\n"
    "- Aman: performa akademik baik secara keseluruhan\n"
    "- Waspada: performa sedang, ada beberapa indikator yang perlu diperhatikan\n"
    "- Berisiko: performa rendah, berisiko gagal studi\n"
    "Jawab HANYA dengan satu kata: Aman, Waspada, atau Berisiko."
)
cfg_v1 = {
    "model": model_name,
    "temperature": 0,
    "max_tokens": 5,
    "labels": LABELS,
    "system_prompt": PROMPT_DASAR,
    "few_shot": [],
}
hasil_v1, _ = evaluasi(cfg_v1, val)

# ===== 5. Iterasi 2: few-shot (contoh dari data train) =====
contoh = pool.groupby("status").sample(2, random_state=1)        # 2 contoh per kelas
cfg_v2 = dict(cfg_v1)
cfg_v2["few_shot"] = [{"data": b[FITUR].to_dict(), "label": b["status"]} for _, b in contoh.iterrows()]
hasil_v2, _ = evaluasi(cfg_v2, val)

# ===== 6. Iterasi 3: few-shot + profil kelas dari data train =====
median = train.groupby("status")[["ipk", "kehadiran", "jam_belajar", "tugas_terkumpul", "nilai_uts"]].median()
profil = "\n".join(
    f"- {s}: IPK {r.ipk:.2f}, kehadiran {r.kehadiran:.0f}%, jam belajar {r.jam_belajar:.0f}, "
    f"tugas {r.tugas_terkumpul:.0f}%, UTS {r.nilai_uts:.0f}"
    for s, r in median.loc[LABELS].iterrows()
)
cfg_v3 = dict(cfg_v2)
cfg_v3["system_prompt"] = (
    PROMPT_DASAR
    + "\n\nNilai tengah (median) setiap kelas dari data historis:\n" + profil
    + "\nCatatan: kehadiran di bawah 75% sangat menurunkan status."
)
hasil_v3, _ = evaluasi(cfg_v3, val)

# ===== 7. Pilih konfigurasi terbaik, lalu uji SEKALI pada data TEST =====
kandidat = [(hasil_v1, cfg_v1), (hasil_v2, cfg_v2), (hasil_v3, cfg_v3)]
hasil_val, cfg_final = max(kandidat, key=lambda k: k[0]["f1_macro"])
print("Konfigurasi terpilih: F1 validasi =", hasil_val["f1_macro"])
hasil_test, pred_test = evaluasi(cfg_final, test)

# ===== 8. Bandingkan dengan DNN (Modul 1A) pada data test yang sama =====
if os.path.exists("model_info.json"):
    with open("model_info.json") as f:
        dnn = json.load(f)["metrik"]
    print(pd.DataFrame({
        "DNN (Modul 1A)": [dnn["accuracy"], dnn["f1_macro"]],
        "LLM (Modul 2A)": [hasil_test["accuracy"], hasil_test["f1_macro"]],
    }, index=["accuracy", "f1_macro"]))
    hasil_test["f1_dnn_pembanding"] = dnn["f1_macro"]

# ===== 9. Gerbang evaluasi & simpan konfigurasi =====
TARGET_F1 = 0.70                                 # ditetapkan dosen/asisten
MAKS_INVALID = 0.05 * hasil_test["n"]
if hasil_test["f1_macro"] >= TARGET_F1 and hasil_test["invalid"] <= MAKS_INVALID:
    cfg_final["evaluasi"] = {**hasil_test, "dataset": "dataset_status_akademik.csv (bagian test)",
                             "tanggal": date.today().isoformat()}
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(cfg_final, f, indent=2, ensure_ascii=False)
    test.assign(prediksi=pred_test).to_csv("hasil_evaluasi_test.csv", index=False)
    print("LOLOS evaluasi -> config.json siap dipakai Streamlit")
else:
    print("BELUM LOLOS -> perbaiki prompt / ganti model, lalu evaluasi ulang")
