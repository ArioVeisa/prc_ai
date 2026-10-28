# Praktikum Artificial Intelligence and Its Application

Repositori pengerjaan praktikum kecerdasan artifisial:
- **Modul 1A & 1B**: Klasifikasi Status Akademik Mahasiswa berbasis Deep Neural Network (MLPClassifier).
- **Modul 2A & 2B**: Klasifikasi Status Akademik Mahasiswa berbasis Large Language Model Service.
- **Laporan Praktikum**: `Laporan_Praktikum_AI_Modul_1A_dan_2A.pdf`.

---

## Struktur Folder

```text
├── Modul_1A/               # Training dan evaluasi model DNN
│   ├── dataset_status_akademik.csv
│   ├── train_model.py
│   ├── cek_model.py
│   ├── model_status_akademik.pkl
│   └── model_info.json
├── Modul_1B/               # Web App Streamlit untuk model DNN (.pkl)
│   ├── app.py
│   ├── model_status_akademik.pkl
│   ├── model_info.json
│   ├── requirements.txt
│   └── contoh_data_baru.csv
├── Modul_2A/               # Eksperimen prompt dan evaluasi LLM
│   ├── classifier.py
│   ├── config.json
│   ├── evaluasi_groq.py
│   └── run_prompt_iterations.py
├── Modul_2B/               # Web App Streamlit untuk LLM Service
│   ├── app.py
│   ├── classifier.py
│   ├── config.json
│   ├── requirements.txt
│   └── contoh_data_baru.csv
└── Laporan_Praktikum_AI_Modul_1A_dan_2A.pdf
```

---

## Cara Menjalankan Aplikasi Secara Lokal

### 1. Modul 1B (DNN App)
```bash
cd Modul_1B
pip install -r requirements.txt
streamlit run app.py
```

### 2. Modul 2B (LLM App)
```bash
cd Modul_2B
pip install -r requirements.txt
# Atur GROQ_API_KEY di .streamlit/secrets.toml
streamlit run app.py
```
