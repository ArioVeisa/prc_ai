# ===== Evaluasi Tambahan: Tugas Praktikum No. 3 (Iterasi 4) =====
import os
import pandas as pd
from dotenv import load_dotenv
from evaluasi_groq import PROMPT_DASAR, cfg_v3, evaluasi, pool, val, client

FITUR = list(NAMA_FITUR)
LABELS = ["Aman", "Waspada", "Berisiko"]

# Iterasi 4: Tambah instruksi batas kritis kelas Waspada & contoh terfokus
PROMPT_V4 = (
    PROMPT_DASAR
    + "\n\nPanduan Batas Status Akademik:"
    + "\n- Aman: IPK >= 3.20, kehadiran >= 80%, tugas >= 80%, UTS >= 70."
    + "\n- Berisiko: IPK < 2.75 ATAU kehadiran < 75% ATAU tugas < 60% ATAU UTS < 50."
    + "\n- Waspada: Mahasiswa yang berada di antara Aman dan Berisiko (performa marginal / inkonsisten)."
    + "\nCatatan Prioritas: Kehadiran < 75% otomatis membuat status Berisiko."
)

cfg_v4 = dict(cfg_v3)
cfg_v4["system_prompt"] = PROMPT_V4

print("=== Menjalankan Evaluasi Iterasi 4 pada Data Validasi ===")
hasil_v4, _ = evaluasi(cfg_v4, val)
print("Hasil Iterasi 4 (Validasi):", hasil_v4)
