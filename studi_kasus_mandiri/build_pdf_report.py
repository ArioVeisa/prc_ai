import os
import json
import numpy as np
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class HeartReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(16, 16, 16)
        
        font_dir = "/usr/share/fonts/truetype/dejavu/"
        self.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", os.path.join(font_dir, "DejaVuSans-Bold.ttf"))
        self.add_font("DejaVu", "I", os.path.join(font_dir, "DejaVuSans-Oblique.ttf"))
        self.add_font("DejaVuMono", "", os.path.join(font_dir, "DejaVuSansMono.ttf"))

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8.5)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, str(self.page_no()), align="C")

    def judul_laporan(self, title, sub):
        self.set_font("DejaVu", "B", 13)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 6, title, align="C")
        self.ln(1)
        self.set_font("DejaVu", "I", 9.5)
        self.set_text_color(70, 70, 70)
        self.cell(0, 5, sub, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(3)

    def bab(self, nomor, judul):
        self.ln(2)
        self.set_font("DejaVu", "B", 10.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5.5, f"{nomor}. {judul}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(1)

    def sub_bab(self, teks):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(30, 30, 30)
        self.cell(0, 4.5, teks, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(0.5)

    def paragraf(self, teks):
        self.set_font("DejaVu", "", 8.5)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 4.2, teks, align="J")
        self.ln(1.5)

    def code_box(self, code_text):
        self.set_font("DejaVuMono", "", 7.5)
        self.set_fill_color(248, 248, 248)
        self.set_text_color(30, 30, 30)
        self.set_draw_color(210, 210, 210)
        
        lines = code_text.strip().split("\n")
        h_total = len(lines) * 3.8 + 4
        self.rect(self.get_x(), self.get_y(), 178, h_total, "DF")
        self.set_x(self.get_x() + 2)
        self.set_y(self.get_y() + 2)
        
        for line in lines:
            self.cell(174, 3.8, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

def generate_pdf():
    pdf = HeartReportPDF()
    pdf.add_page()

    # Header / Title
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 5, "LAPORAN PRAKTIKUM INDIVIDU", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVu", "", 9.5)
    pdf.cell(0, 4.5, "Kecerdasan Artifisial dan Penerapannya", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.judul_laporan(
        "Klasifikasi Risiko Penyakit Jantung Menggunakan Machine Learning Library (Random Forest) dan AI Model Service (LLM Few-Shot) Berbasis Streamlit Deployment",
        "Studi Kasus Mandiri — Heart Failure Prediction Dataset (Kaggle / UCI)"
    )

    # Metadata Table
    pdf.set_font("DejaVu", "", 8)
    pdf.set_draw_color(200, 200, 200)
    meta = [
        ("Nama Mahasiswa", "Ario veisa Rayanda Utomo"),
        ("NIM", "1204230086"),
        ("Kelas / Prodi", "SI-06-REG / S1 Sistem Informasi"),
        ("Fakultas / Kampus", "Fakultas Direktorat Kampus Surabaya — Telkom University Surabaya"),
        ("Mata Kuliah / Semester", "Kecerdasan Artifisial dan Penerapannya / Ganjil 2026–2027"),
        ("Tanggal Praktikum", "28 Oktober 2026"),
        ("Dosen Pengampu", "M. Nizar P. Ma'ady, S.Kom., M.IM., M.Kom.")
    ]
    for k, v in meta:
        pdf.set_font("DejaVu", "B", 8)
        pdf.cell(48, 4.5, f"  {k}", border=1)
        pdf.set_font("DejaVu", "", 8)
        pdf.cell(130, 4.5, f"  {v}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # 1. Tujuan Praktikum
    pdf.bab("1", "Tujuan Praktikum")
    pdf.paragraf(
        "1. Membangun dan mengevaluasi model klasifikasi data tabular berbasis Machine Learning Library (Random Forest Pipeline) untuk memprediksi risiko penyakit jantung secara akurat dan efisien.\n"
        "2. Merancang strategi rekayasa prompt dan in-context few-shot learning pada AI Model Service (Large Language Model) untuk melakukan penalaran klinis diagnosis risiko jantung.\n"
        "3. Mengintegrasikan kedua model ke dalam aplikasi web Streamlit interaktif (input manual formulir, prediksi batch CSV, dan penyediaan downloadable sample dataset) serta men-deploy aplikasi ke cloud publik (Streamlit Community Cloud)."
    )

    # 2. Dasar Teori Singkat
    pdf.bab("2", "Dasar Teori Singkat")
    pdf.paragraf(
        "Machine Learning Library (khususnya Random Forest Classifier) bekerja dengan membangun sekumpulan decision tree secara ensemble dan melakukan majority voting. Pipeline scikit-learn menggunakan ColumnTransformer untuk memisahkan fitur numerik (diskalakan dengan StandardScaler) dan fitur kategorikal (dikonversi dengan OneHotEncoder). Pendekatan library lokal memiliki keunggulan inferensi sangat cepat (< 5 ms per sampel), deterministik, dan dapat dijalankan sepenuhnya secara offline.\n\n"
        "Sebaliknya, AI Model Service berbasis LLM memanfaatkan in-context learning. Tanpa retraining bobot parameter, model diberi instruksi sistemik (system prompt) dan demonstrasi contoh representatif (few-shot demonstrations). LLM mampu mengenali interaksi semantik antar-gejala (misal: nyeri dada asimptomatik/ASY disertai depresi segmen ST Oldpeak tinggi menandakan iskemia jantung). Namun, pendekatan ini memiliki konsekuensi latensi tinggi akibat pemanggilan remote API serta biaya token.\n\n"
        "Streamlit menyajikan model AI menjadi antarmuka web interaktif secara reaktif. Fitur st.secrets melindungi rahasia API key, sementara @st.cache_data dan @st.cache_resource mencegah komputasi dan pemanggilan API berulang."
    )

    # 3. Alat dan Bahan
    pdf.bab("3", "Alat dan Bahan")
    pdf.paragraf(
        "• Perangkat keras: PC / Laptop x86_64, CPU 8-Core, RAM 16 GB, SSD 512 GB.\n"
        "• Sistem operasi: Linux Ubuntu 24.04 LTS (x86_64).\n"
        "• Perangkat lunak: Python 3.12, scikit-learn 1.9.1, pandas 3.0.6, joblib 1.6.0, openai 1.66.1, streamlit 1.66.1, git 2.43.0.\n"
        "• Akun/Layanan & Data: Repositori GitHub (ArioVeisa/prc_ai), Streamlit Community Cloud, AI Practicum LLM Service API, dan Heart Failure Prediction Dataset (Kaggle/UCI, 918 baris, 11 fitur klinis)."
    )

    # ==================== PAGE 2: LANGKAH 1 ====================
    pdf.add_page()
    pdf.bab("4", "Hasil dan Pembahasan")
    pdf.sub_bab("Langkah 1 — Persiapan Data & Pemodelan Machine Learning Library (Random Forest)")
    pdf.paragraf(
        "Dataset Heart Failure Prediction (918 sampel) dibagi menjadi data latih 80% (734 sampel) dan data uji 20% (184 sampel) secara terstratifikasi. Sebuah pipeline scikit-learn dibangun menggunakan ColumnTransformer untuk menstandarisasi 6 fitur numerik dan melakukan one-hot encoding pada 5 fitur kategori. Model dilatih dengan RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42), dievaluasi pada data uji, lalu disimpan sebagai artefak model_heart.pkl beserta model_info.json."
    )
    
    code_1 = (
        "# Potongan kode training Random Forest Pipeline (train_model.py)\n"
        "preprocessor = ColumnTransformer(transformers=[\n"
        "    ('num', StandardScaler(), ['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak']),\n"
        "    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope'])\n"
        "])\n"
        "model = Pipeline([('preprocessor', preprocessor),\n"
        "                  ('classifier', RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42))])\n"
        "model.fit(train_df[FEATURES], train_df['Target'])\n"
        "y_pred = model.predict(test_df[FEATURES])\n"
        "joblib.dump(model, 'model_heart.pkl')"
    )
    pdf.code_box(code_1)

    # Gambar 1
    pdf.image("studi_kasus_mandiri/figures/confusion_matrices_heart.png", x=16, y=pdf.get_y(), w=178)
    pdf.set_y(pdf.get_y() + 75)
    pdf.set_font("DejaVu", "I", 8)
    pdf.cell(0, 4.5, "Gambar 1. Matriks Konfusi dan Evaluasi Model Random Forest vs LLM pada Data Uji.", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    pdf.paragraf(
        "Analisis: Pada pengujian data uji (N=184), model Random Forest berhasil meraih akurasi sebesar 88.59% dan Macro F1-Score sebesar 0.8837. Pada evaluasi sampel uji acak 50 pasien (Gambar 1 kiri), model mencatatkan 20 True Normal, 25 True Penyakit Jantung, 3 False Positive, dan 2 False Negative (Akurasi 90.0%, F1 0.8990). Kecepatan inferensi model library sangat unggul, yakni hanya 3.08 milidetik per sampel, menjadikannya opsi ideal untuk pemrosesan data bervolume besar secara instan tanpa biaya jaringan."
    )

    # ==================== PAGE 3: LANGKAH 2 ====================
    pdf.add_page()
    pdf.sub_bab("Langkah 2 — Rekayasa Prompt & Evaluasi AI Model Service (LLM Few-Shot)")
    pdf.paragraf(
        "Klasifikasi kedua dilakukan menggunakan Large Language Model Service (ai-practicum) via API. Konfigurasi disimpan dalam config_heart.json dengan menyusun system prompt yang menjelaskan indikator risiko kardiologi mayor (ChestPainType ASY, ST_Slope Flat, dan Oldpeak tinggi), disertai 6 contoh data few-shot representatif (3 Normal, 3 Penyakit Jantung). Fungsi classify() diimplementasikan dalam classifier_heart.py dengan mekanisme pemanggilan OpenAI-compatible API dan parsing label deterministik."
    )

    code_2 = (
        "# Potongan logika prompt & classifier LLM Service (classifier_heart.py)\n"
        "def build_messages(cfg, data_input):\n"
        "    messages = [{'role': 'system', 'content': cfg['system_prompt']}]\n"
        "    for fs in cfg.get('few_shot', []):\n"
        "        messages.append({'role': 'user', 'content': format_data(fs['data'])})\n"
        "        messages.append({'role': 'assistant', 'content': fs['label']})\n"
        "    messages.append({'role': 'user', 'content': format_data(data_input)})\n"
        "    return messages\n\n"
        "def classify(client, cfg, data_input):\n"
        "    resp = client.chat.completions.create(model=cfg['model'], temperature=0.0, max_tokens=10,\n"
        "                                          messages=build_messages(cfg, data_input))\n"
        "    return parse_label(resp.choices[0].message.content, cfg['labels'])"
    )
    pdf.code_box(code_2)

    # Gambar 2
    pdf.image("studi_kasus_mandiri/figures/metrics_comparison_heart.png", x=26, y=pdf.get_y(), w=158)
    pdf.set_y(pdf.get_y() + 85)
    pdf.set_font("DejaVu", "I", 8)
    pdf.cell(0, 4.5, "Gambar 2. Grafik Perbandingan Metrik Evaluasi: Random Forest vs LLM Service.", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    pdf.paragraf(
        "Analisis: Evaluasi 50 data uji menunjukkan bahwa LLM Service mencapai akurasi sebesar 94.0% dan Macro F1-Score sebesar 0.9398 (Gambar 2). LLM berhasil menekan False Positive menjadi hanya 1 kasus (Gambar 1 kanan) berkat kemampuannya membedakan profil klinis asimptomatik dengan depresi ST secara semantik. Meskipun akurasi LLM lebih tinggi 4% dibanding Random Forest pada sampel uji, latensinya mencapai 9.132,80 ms (~9,1 detik per sampel) atau 2.965 kali lebih lambat dibanding Random Forest. Hal ini menegaskan trade-off antara fleksibilitas penalaran LLM dan efisiensi waktu komputasi library."
    )

    # ==================== PAGE 4: LANGKAH 3 ====================
    pdf.add_page()
    pdf.sub_bab("Langkah 3 — Pembuatan Web Streamlit, Unduh Sampel Data, dan Deployment Cloud")
    pdf.paragraf(
        "Aplikasi web CardioGuard AI dibangun menggunakan Streamlit (app.py) dengan antarmuka terpadu yang memadukan kedua model. Aplikasi memiliki formulir input manual 11 fitur klinis (Tab 1) dan fasilitas batch prediction file CSV (Tab 2). Sesuai instruksi penugasan poin 5, tombol unduh sampel data uji (sample_test_heart.csv, 15 data pasien) disediakan langsung di sidebar aplikasi. Proyek di-push ke GitHub dan di-deploy ke Streamlit Community Cloud."
    )

    code_3 = (
        "# Potongan antarmuka Streamlit (studi_kasus_mandiri/app.py)\n"
        "with st.sidebar:\n"
        "    st.header('❤️ CardioGuard AI')\n"
        "    engine = st.radio('Pilih Model:', ['Komparasi Keduanya', 'Random Forest', 'LLM Service'])\n"
        "    st.download_button('Unduh sample_test_heart.csv', data=sample_csv_bytes, file_name='sample_test_heart.csv')\n\n"
        "tab1, tab2 = st.tabs(['🩺 Prediksi Satu Pasien', '📁 Prediksi Batch dari File CSV'])\n"
        "with tab1:\n"
        "    # Form 11 input klinis pasien...\n"
        "    if st.form_submit_button('Analisis Risiko Pasien'):\n"
        "        # Inferensi Random Forest (proba) & LLM Service...\n"
        "        st.success(f'Hasil: {hasil_prediksi}')"
    )
    pdf.code_box(code_3)

    # Gambar 3
    pdf.image("studi_kasus_mandiri/figures/latency_comparison_heart.png", x=38, y=pdf.get_y(), w=134)
    pdf.set_y(pdf.get_y() + 82)
    pdf.set_font("DejaVu", "I", 8)
    pdf.cell(0, 4.5, "Gambar 3. Grafik Perbandingan Latensi Eksekusi Inferensi (Skala Logaritmik).", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    pdf.paragraf(
        "Analisis: Antarmuka web memfasilitasi interaksi pengguna secara komprehensif. Pengguna dapat memilih model yang diinginkan atau menjalankan komparasi konsensus AI. Fitur unduh contoh data memungkinkan penguji langsung mengunduh 15 sampel pasien terverifikasi lalu mengunggahnya ke tab CSV tanpa perlu mengetik manual. Aplikasi telah aktif dan ter-deploy secara publik pada URL Streamlit Community Cloud:\n"
        "• URL Deployment : https://arioveisa-prc-ai-studi-kasus-mandiriapp-0nybuc.streamlit.app\n"
        "• Repositori GitHub: https://github.com/ArioVeisa/prc_ai/tree/main/studi_kasus_mandiri"
    )

    # ==================== PAGE 5: KENDALA & KESIMPULAN ====================
    pdf.add_page()
    pdf.bab("6", "Kendala dan Solusi")
    pdf.paragraf("Berikut kendala teknis nyata yang dihadapi selama pengerjaan praktikum mandiri beserta solusi penyelesaiannya:")

    # Table Kendala dan Solusi
    kendala_data = [
        ("1", "FileNotFoundError saat memuat model (.pkl), metadata, dan konfigurasi (.json) saat aplikasi pertama kali dijalankan di Streamlit Community Cloud.",
         "Menggunakan modul Path(__file__).resolve().parent untuk menentukan direktori kerja dinamis file aplikasi, sehingga pencarian aset model selalu valid terlepas dari root direktori kerja server cloud."),
        ("2", "Konflik pembacaan environment secrets di Streamlit Cloud ketika kunci GROQ_API_KEY terdefinisi sebagai string kosong, menyebabkan fallback ke endpoint praktikum terblokir.",
         "Memperbaiki logika parser secret dengan menerapkan fungsi .strip() dan validasi non-empty sebelum instansiasi client API, serta menyelaraskan isian menu Secrets pada dashboard Streamlit Cloud."),
        ("3", "Latensi pemanggilan AI Model Service yang mencapai ~9 detik per data menyebabkan proses prediksi batch CSV terasa membeku (unresponsive).",
         "Menerapkan dekorator @st.cache_data pada fungsi prediksi LLM, menambahkan progress bar dinamis saat iterasi baris, dan membatasi inferensi interaktif LLM pada 15 baris sampel teratas.")
    ]

    pdf.set_font("DejaVu", "B", 8)
    pdf.set_fill_color(235, 235, 235)
    pdf.cell(10, 6, "No", border=1, fill=True, align="C")
    pdf.cell(78, 6, "Kendala yang Dihadapi", border=1, fill=True, align="C")
    pdf.cell(90, 6, "Solusi / Tindakan Perbaikan", border=1, fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("DejaVu", "", 7.5)
    for no, k, s in kendala_data:
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # calculate max height
        h_k = len(pdf.multi_cell(78, 3.8, k, dry_run=True, output="LINES")) * 3.8 + 2
        h_s = len(pdf.multi_cell(90, 3.8, s, dry_run=True, output="LINES")) * 3.8 + 2
        max_h = max(h_k, h_s, 16)
        
        # Cell 1
        pdf.rect(x_start, y_start, 10, max_h)
        pdf.set_xy(x_start, y_start + (max_h - 4)/2)
        pdf.cell(10, 4, no, align="C")
        
        # Cell 2
        pdf.rect(x_start + 10, y_start, 78, max_h)
        pdf.set_xy(x_start + 11, y_start + 1.5)
        pdf.multi_cell(76, 3.7, k, align="L")
        
        # Cell 3
        pdf.rect(x_start + 88, y_start, 90, max_h)
        pdf.set_xy(x_start + 89, y_start + 1.5)
        pdf.multi_cell(88, 3.7, s, align="L")
        
        pdf.set_xy(x_start, y_start + max_h)

    pdf.ln(3)

    # 7. Kesimpulan
    pdf.bab("7", "Kesimpulan")
    pdf.paragraf(
        "Berdasarkan pelaksanaan studi kasus mandiri klasifikasi risiko penyakit jantung (Heart Failure Prediction Dataset, Kaggle/UCI) menggunakan Machine Learning Library (Random Forest) dan AI Model Service (LLM Few-Shot) berbasis Streamlit Deployment, diperoleh kesimpulan sebagai berikut:\n\n"
        "1. Model Machine Learning Library (Random Forest Pipeline) terbukti sangat handal untuk data tabular terstruktur, meraih akurasi 88.59% pada keseluruhan data uji (dan 90.0% pada evaluasi sampel) dengan keunggulan kecepatan inferensi superior sebesar 3.08 milidetik per sampel tanpa ketergantungan koneksi internet.\n"
        "2. AI Model Service (LLM Few-Shot) membuktikan kapabilitas in-context learning yang tajam dengan akurasi 94.0% dan Macro F1-Score 0.9398. LLM mampu melakukan penalaran semantik terhadap interaksi multi-gejala klinis tanpa retraining, namun memiliki kendala latensi tinggi (9.132,80 ms/sampel) dan biaya kuota token.\n"
        "3. Seluruh instruksi penugasan praktikum berhasil dipenuhi secara tuntas: integrasi form input manual otomatis, tab prediksi batch CSV, penyediaan file data sampel siap unduh (sample_test_heart.csv), serta keberhasilan deployment cloud pada URL publik: https://arioveisa-prc-ai-studi-kasus-mandiriapp-0nybuc.streamlit.app."
    )

    out_pdf = "studi_kasus_mandiri/Laporan_Praktikum_Individu_Heart_Disease.pdf"
    pdf.output(out_pdf)
    print(f"Laporan PDF berhasil dibuat: {out_pdf}")

if __name__ == "__main__":
    generate_pdf()
