import os
import json
import numpy as np
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class SimpleLaporanPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(18, 18, 18)
        
        font_dir = '/usr/share/fonts/truetype/dejavu/'
        self.add_font('DejaVu', '', os.path.join(font_dir, 'DejaVuSans.ttf'))
        self.add_font('DejaVu', 'B', os.path.join(font_dir, 'DejaVuSans-Bold.ttf'))
        self.add_font('DejaVu', 'I', os.path.join(font_dir, 'DejaVuSans-Oblique.ttf'))
        self.add_font('DejaVuMono', '', os.path.join(font_dir, 'DejaVuSansMono.ttf'))

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font('DejaVu', '', 8.5)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, str(self.page_no()), align='C')

    def judul_bab(self, nomor, judul):
        self.ln(2)
        self.set_font('DejaVu', 'B', 11.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, f'{nomor}. {judul}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(1)

    def sub_judul(self, teks):
        self.set_font('DejaVu', 'B', 9.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, teks, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(0.5)

    def paragraf(self, teks):
        self.set_font('DejaVu', '', 8.5)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4.3, teks, align='J')
        self.ln(1.5)

    def kode(self, teks_kode):
        lines = teks_kode.strip().split('\n')
        line_height = 3.6
        h = len(lines) * line_height + 3
        cur_x = self.get_x()
        cur_y = self.get_y()
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.rect(cur_x, cur_y, 174, h, style='DF')
        self.set_font('DejaVuMono', '', 7.5)
        self.set_text_color(20, 20, 20)
        self.set_xy(cur_x + 3, cur_y + 1.5)
        for line in lines:
            self.cell(168, line_height, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(cur_x, cur_y + h + 2)

def buat_laporan():
    pdf = SimpleLaporanPDF()

    # ================= PAGE 1: COVER =================
    pdf.add_page()
    pdf.ln(35)
    
    pdf.set_font('DejaVu', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'LAPORAN', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(1)
    pdf.set_font('DejaVu', 'B', 13)
    pdf.cell(0, 7, 'Praktikum Artificial Intelligence', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(1)
    pdf.set_font('DejaVu', '', 10.5)
    pdf.cell(0, 6, 'Klasifikasi Status Akademik Mahasiswa (Modul 1A & Modul 2A)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.ln(50)
    
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 6, 'Oleh:', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(2)
    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 6.5, 'Ario veisa Rayanda Utomo ( 1204230086 )', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.ln(60)
    
    pdf.set_font('DejaVu', 'B', 11)
    pdf.cell(0, 6, 'S1 SISTEM INFORMASI', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, 'FAKULTAS DIREKTORAT KAMPUS SURABAYA', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(2)
    pdf.cell(0, 6, 'TELKOM UNIVERSITY SURABAYA', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 6, '2026', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # ================= PAGE 2: 0. PRAKTIK MODUL 1A =================
    pdf.add_page()
    pdf.judul_bab('0', 'Praktik Modul 1A (Deep Neural Network)')
    
    pdf.sub_judul('Dataset dan Pembagian Data')
    pdf.paragraf(
        'Pada Modul 1A, model Deep Neural Network (DNN) dilatih untuk memprediksi status akademik mahasiswa '
        '(Aman, Waspada, Berisiko). Dataset yang digunakan adalah dataset_status_akademik.csv yang berisi 1.000 baris data '
        'dengan 6 fitur: ipk, kehadiran, jam_belajar, tugas_terkumpul, nilai_uts, dan aktif_organisasi. '
        'Data sudah dipisah lewat kolom bagian menjadi 800 data train dan 200 data test. '
        'Sebanyak 200 data test ini dipakai sebagai data uji yang sama pada evaluasi model DNN maupun model LLM di Modul 2A.'
    )
    
    pdf.sub_judul('Pipeline dan Model DNN')
    pdf.paragraf(
        'Preprocessing dan model disatukan ke dalam satu Pipeline scikit-learn. '
        'Fitur numerik diskalakan dengan StandardScaler, sedangkan fitur aktif_organisasi diubah dengan OneHotEncoder. '
        'Model DNN menggunakan MLPClassifier dengan 3 hidden layer (64, 32, 16 neuron), aktivasi ReLU, solver Adam, '
        'regularisasi L2 alpha=0.001, dan early stopping (10% data train dipakai untuk validasi internal).'
    )
    
    pdf.kode(
        'preprocess = ColumnTransformer([\n'
        '    ("num", StandardScaler(), ["ipk", "kehadiran", "jam_belajar", "tugas_terkumpul", "nilai_uts"]),\n'
        '    ("cat", OneHotEncoder(handle_unknown="ignore"), ["aktif_organisasi"])\n'
        '])\n'
        'dnn = MLPClassifier(\n'
        '    hidden_layer_sizes=(64, 32, 16), activation="relu", solver="adam", alpha=1e-3,\n'
        '    learning_rate_init=1e-3, max_iter=500, early_stopping=True, validation_fraction=0.1, random_state=42\n'
        ')\n'
        'model = Pipeline([("preprocess", preprocess), ("dnn", dnn)])'
    )
    
    pdf.sub_judul('Hasil Training dan Evaluasi Test')
    pdf.paragraf(
        'Proses training berjalan hingga epoch ke-50 dan berhenti karena early stopping dengan akurasi validasi terbaik 87.50%. '
        'Pada 200 data test, model DNN memperoleh akurasi 84.00% dan F1 macro 0.8269. '
        'Hasil ini melebihi target gerbang kelulusan modul (F1 >= 0.80) dan jauh di atas baseline tebakan terbanyak (F1 baseline = 0.1800). '
        'Model berhasil disimpan ke file model_status_akademik.pkl bersama ringkasan model_info.json.'
    )
    
    with pdf.table(col_widths=(35, 27, 27, 27, 28, 30)) as table:
        row = table.row()
        row.cell('Kelas')
        row.cell('Precision')
        row.cell('Recall')
        row.cell('F1-Score')
        row.cell('Support')
        row.cell('Hasil')
        
        row = table.row()
        row.cell('Aman')
        row.cell('0.88')
        row.cell('0.88')
        row.cell('0.88')
        row.cell('74')
        row.cell('Bagus')
        
        row = table.row()
        row.cell('Waspada')
        row.cell('0.73')
        row.cell('0.67')
        row.cell('0.70')
        row.cell('55')
        row.cell('Paling sulit')
        
        row = table.row()
        row.cell('Berisiko')
        row.cell('0.88')
        row.cell('0.93')
        row.cell('0.90')
        row.cell('71')
        row.cell('Sangat bagus')
        
        row = table.row()
        row.cell('Macro Avg')
        row.cell('0.83')
        row.cell('0.83')
        row.cell('0.83')
        row.cell('200')
        row.cell('Lolos (>= 0.80)')

    pdf.ln(2)
    pdf.sub_judul('Pengujian Model Mandiri (cek_model.py)')
    pdf.paragraf(
        'File model_status_akademik.pkl diuji dengan script cek_model.py pada satu contoh mahasiswa: '
        'IPK 3.45, Kehadiran 92%, Jam belajar 12, Tugas 95%, UTS 82, Aktif organisasi Ya. '
        'Model memprediksi status Aman dengan probabilitas: Aman = 0.995, Waspada = 0.005, Berisiko = 0.000. '
        'File model terbukti valid dan siap dideploy ke Streamlit pada Modul 1B.'
    )

    # ================= PAGE 3: 1. TUGAS 1 =================
    pdf.add_page()
    pdf.judul_bab('1', 'Tabel Perbandingan DNN vs LLM dan Analisis Evaluasi')
    
    pdf.paragraf(
        'Pada Modul 2A, 200 data test yang sama diuji menggunakan AI model service (LLM). '
        'Konfigurasi LLM yang dipakai adalah prompt terbaik dari tahap validasi, yaitu Iterasi 2 (few-shot 6 contoh data train). '
        'Berikut tabel perbandingan hasil evaluasi antara DNN Modul 1A dan LLM Service 1 (ai-practicum):'
    )
    
    with pdf.table(col_widths=(45, 43, 43, 43)) as table:
        row = table.row()
        row.cell('Metrik Evaluasi')
        row.cell('DNN (Modul 1A)')
        row.cell('LLM S1 (Modul 2A)')
        row.cell('Keterangan')
        
        metrics = [
            ('Akurasi Keseluruhan', '0.8400 (84.00%)', '0.6100 (61.00%)', 'DNN lebih tinggi +23%'),
            ('F1-Score (Macro)', '0.8269 (82.69%)', '0.6098 (60.98%)', 'DNN lebih tinggi +21.7%'),
            ('Precision (Macro)', '0.8280 (82.80%)', '0.7760 (77.60%)', 'DNN lebih tinggi'),
            ('Recall (Macro)', '0.8269 (82.69%)', '0.6337 (63.37%)', 'DNN lebih tinggi'),
            ('F1 Aman', '0.8784', '0.7419', 'DNN lebih baik'),
            ('F1 Waspada', '0.6981', '0.5667', 'DNN lebih baik'),
            ('F1 Berisiko', '0.9041', '0.5208', 'DNN jauh lebih baik'),
            ('Jawaban Invalid', '0 (0.0%)', '0 (0.0%)', 'Semua format rapi'),
            ('Status Gerbang', 'Lolos (>= 0.80)', 'Tidak Lolos (< 0.70)', 'Hanya DNN lolos gerbang')
        ]
        for m, v1, v2, ket in metrics:
            row = table.row()
            row.cell(m)
            row.cell(v1)
            row.cell(v2)
            row.cell(ket)

    pdf.ln(2)
    pdf.sub_judul('Perbandingan Confusion Matrix')
    pdf.paragraf(
        'Hasil tebakan kedua model pada 200 data uji (74 Aman, 55 Waspada, 71 Berisiko) adalah sebagai berikut:'
    )
    
    with pdf.table(col_widths=(35, 23, 23, 23, 23, 23, 24)) as table:
        row = table.row()
        row.cell('Asli')
        row.cell('DNN: Aman')
        row.cell('DNN: Wasp')
        row.cell('DNN: Risk')
        row.cell('LLM: Aman')
        row.cell('LLM: Wasp')
        row.cell('LLM: Risk')
        
        row = table.row()
        row.cell('Aman (74)')
        row.cell('65')
        row.cell('9')
        row.cell('0')
        row.cell('46')
        row.cell('28')
        row.cell('0')
        
        row = table.row()
        row.cell('Waspada (55)')
        row.cell('9')
        row.cell('37')
        row.cell('9')
        row.cell('4')
        row.cell('51')
        row.cell('0')
        
        row = table.row()
        row.cell('Berisiko (71)')
        row.cell('0')
        row.cell('5')
        row.cell('66')
        row.cell('0')
        row.cell('46')
        row.cell('25')

    pdf.ln(2)
    pdf.sub_judul('Analisis Hasil Evaluasi Data Test')
    pdf.paragraf(
        '1. Akurasi DNN Jauh Lebih Tinggi: DNN mencapai 84.00% sedangkan LLM hanya 61.00%. '
        'DNN memproses angka secara langsung dan menyesuaikan bobot matematisnya lewat data train 800 baris. '
        'Model DNN bisa memisahkan batas angka yang tipis (misalnya batas kehadiran 75% atau IPK 2.75). '
        'Sebaliknya, LLM membaca data sebagai teks biasa dan hanya mengandalkan pemahaman bahasa, '
        'sehingga kesulitan menentukan batas kuantitatif yang ketat.'
    )
    pdf.paragraf(
        '2. LLM Terlalu Sering Menebak Waspada: Pada confusion matrix terlihat bahwa LLM Service 1 menebak Waspada '
        'sebanyak 125 kali dari 200 data (lebih dari 60% total tebakan). '
        'Dari 71 mahasiswa yang sebenarnya Berisiko, 46 di antaranya justru ditebak Waspada. '
        'Hal ini membuat recall kelas Berisiko anjlok ke 35.21%. Kesalahan ini berbahaya jika diterapkan di kampus '
        'karena mahasiswa yang terancam gagal studi tidak terdeteksi sejak awal.'
    )
    pdf.paragraf(
        '3. Tidak Ada Kesalahan Ekstrem: Sisi baiknya, kedua model tidak pernah menukar Aman dan Berisiko secara langsung '
        '(0 mahasiswa Aman ditebak Berisiko, dan 0 mahasiswa Berisiko ditebak Aman). '
        'Namun DNN jauh lebih tegas: DNN mendeteksi 66 dari 71 mahasiswa Berisiko (recall 93%), sedangkan LLM hanya menemukan 25 mahasiswa.'
    )

    # ================= PAGE 4: 2. TUGAS 2 =================
    pdf.add_page()
    pdf.judul_bab('2', 'Analisis Kelebihan dan Kekurangan DNN vs LLM')
    
    pdf.paragraf(
        'Berikut perbandingan kelebihan dan kekurangan antara DNN (Modul 1A) dan LLM Service (Modul 2A) '
        'berdasarkan hasil praktikum:'
    )
    
    with pdf.table(col_widths=(34, 70, 70)) as table:
        row = table.row()
        row.cell('Aspek')
        row.cell('DNN (Modul 1A)')
        row.cell('LLM Service (Modul 2A)')
        
        dims = [
            ('Akurasi Data Tabular',
             'Tinggi (84.00%). Mampu mempelajari pola hubungan angka non-linear dengan batas tegas.',
             'Sedang (61.00%). Kurang peka membedakan angka-angka yang berada di dekat batas ambang.'),
            ('Kelas Tersulit',
             'Waspada (F1 0.6981) karena posisinya berada di zona peralihan antara Aman dan Berisiko.',
             'Berisiko (Recall 35.21%) dan Waspada (Precision 40.80%) karena model terlalu sering memilih jawaban tengah.'),
            ('Biaya (Cost)',
             'Gratis. Model dijalankan di komputer lokal tanpa biaya request atau token.',
             'Berbayar per request/token API. Jika dipakai untuk ribuan data, biaya akan membengkak.'),
            ('Kecepatan',
             'Sangat cepat (~0.21 ms per data, total 42 ms untuk 200 data). Tidak bergantung internet.',
             'Lambat (~1.522 ms per data, total 5 menit untuk 200 data) karena harus mengirim request ke server cloud.'),
            ('Kebutuhan Data Latih',
             'Butuh data berlabel cukup banyak (800 baris) agar bobot model bisa belajar dengan baik.',
             'Bisa bekerja dengan sedikit data. Cukup beri instruksi dan 6 contoh data di prompt (few-shot).'),
            ('Privasi Data',
             'Aman. Data mahasiswa tetap berada di server lokal kampus.',
             'Ada risiko privasi karena data nilai dan presensi mahasiswa dikirim ke server pihak ketiga di cloud.'),
            ('Konsistensi Output',
             'Konsisten 100%. Model file .pkl selalu memberi hasil yang sama untuk input yang sama.',
             'Bisa berubah jika penyedia cloud memperbarui versi model di backend.'),
            ('Fleksibilitas Fitur',
             'Kaku. Menambah data teks (misal catatan dosen wali) perlu arsitektur baru dan training ulang.',
             'Sangat fleksibel. Catatan teks tambahan bisa langsung diselipkan ke dalam prompt.')
        ]
        
        for d, c1, c2 in dims:
            row = table.row()
            row.cell(d)
            row.cell(c1)
            row.cell(c2)

    pdf.ln(2)
    pdf.sub_judul('Pembahasan Ringkas')
    pdf.paragraf(
        'Kedua model sama-sama paling kesulitan di kelas Waspada. Mahasiswa di kelas ini memiliki nilai yang saling bertolak belakang '
        '(misalnya IPK cukup tinggi tetapi presensi rendah, atau sebaliknya presensi rajin tetapi nilai UTS kecil). '
        'DNN memproses kondisi ini dengan bobot kompromi terbaik sehingga meraih F1 0.6981. '
        'Sedangkan LLM justru memakai Waspada sebagai jawaban aman setiap kali ragu, '
        'sehingga akurasi dan recall kelas lainnya ikut rusak.'
    )
    pdf.paragraf(
        'Untuk data tabel angka terstruktur, DNN menang telak dalam hal akurasi, kecepatan (7.000 kali lebih cepat), dan biaya. '
        'Namun keunggulan LLM ada pada kemudahan awal: jika kampus belum punya dataset berlabel 800 data, '
        'LLM bisa langsung dipakai dengan beberapa contoh saja tanpa perlu proses training berhari-hari.'
    )

    if os.path.exists('figures/confusion_matrices_comparison.png'):
        pdf.ln(1)
        pdf.image('figures/confusion_matrices_comparison.png', x=18, y=None, w=174)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4.5, 'Gambar 1: Perbandingan Confusion Matrix DNN vs LLM Service 1 vs GPT-4o-mini', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(3)

    # ================= 3. TUGAS 3 =================
    pdf.judul_bab('3', 'Penggantian AI Service dan Komparasi Tri-Model')
    
    pdf.paragraf(
        'Sesuai tugas nomor 3, saya mengganti AI service di Modul 2A dari ai-practicum ke OpenAI GPT-4o-mini. '
        'Model ini dipilih karena merupakan standar industri untuk model ringkas yang cepat dan murah.'
    )
    
    pdf.sub_judul('Hasil Iterasi Prompt pada Data Validasi (N=30)')
    pdf.paragraf(
        'Kedua AI service diuji menggunakan 4 iterasi prompt yang sama pada 30 data validasi dari data train:'
    )
    
    with pdf.table(col_widths=(46, 32, 32, 32, 32)) as table:
        row = table.row()
        row.cell('Versi Prompt')
        row.cell('Akurasi (S1)')
        row.cell('F1 Macro (S1)')
        row.cell('Akurasi (GPT)')
        row.cell('F1 Macro (GPT)')
        
        row = table.row()
        row.cell('Iterasi 1 (Zero-Shot)')
        row.cell('0.4667')
        row.cell('0.3996')
        row.cell('0.5667')
        row.cell('0.4743')
        
        row = table.row()
        row.cell('Iterasi 2 (Few-Shot 6 Contoh)')
        row.cell('0.6667')
        row.cell('0.6627 (Terbaik)')
        row.cell('0.7667')
        row.cell('0.7707 (Terbaik)')
        
        row = table.row()
        row.cell('Iterasi 3 (Few-Shot + Median)')
        row.cell('0.6333')
        row.cell('0.6180')
        row.cell('0.6000')
        row.cell('0.5778')
        
        row = table.row()
        row.cell('Iterasi 4 (Aturan Manual)')
        row.cell('0.4667')
        row.cell('0.3761 (Turun)')
        row.cell('0.5000')
        row.cell('0.4603 (Turun)')

    pdf.ln(1.5)
    pdf.paragraf(
        'Mengapa Iterasi 4 Malah Turun? Pada iterasi 4, saya menambahkan aturan batasan manual '
        '(misalnya: "Berisiko jika IPK < 2.75 ATAU kehadiran < 75% ATAU UTS < 50..."). '
        'Skor F1 kedua model justru merosot tajam (S1 turun ke 0.3761, GPT-4o-mini turun ke 0.4603). '
        'Hal ini terjadi karena aturan logika teks yang panjang dengan banyak kata "ATAU" membingungkan model bahasa '
        'saat menimbang atribut yang saling bertentangan. Memberi contoh konkret lewat few-shot (Iterasi 2) '
        'terbukti jauh lebih efektif daripada mendikte aturan logika yang kaku.'
    )

    if os.path.exists('figures/prompt_iteration_comparison.png'):
        pdf.ln(1)
        pdf.image('figures/prompt_iteration_comparison.png', x=42, y=None, w=126)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4.5, 'Gambar 2: Skor F1 Macro pada 4 Iterasi Prompt (Data Validasi)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # ================= PAGE 6: LANJUTAN TUGAS 3 =================
    pdf.add_page()
    pdf.sub_judul('Tabel Perbandingan 3 Model pada Data Test (200 Sampel)')
    pdf.paragraf(
        'Berikut tabel perbandingan hasil evaluasi akhir pada 200 data test yang sama setelah menambahkan OpenAI GPT-4o-mini:'
    )
    
    with pdf.table(col_widths=(44, 38, 46, 46)) as table:
        row = table.row()
        row.cell('Metrik Evaluasi')
        row.cell('DNN (Modul 1A)')
        row.cell('LLM S1 (ai-practicum)')
        row.cell('LLM S2 (GPT-4o-mini)')
        
        tri_metrics = [
            ('Akurasi Keseluruhan', '0.8400 (84.00%)', '0.6100 (61.00%)', '0.6250 (62.50%)'),
            ('F1-Score (Macro)', '0.8269 (82.69%)', '0.6098 (60.98%)', '0.6351 (63.51%)'),
            ('F1 Aman', '0.8784', '0.7419', '0.6333'),
            ('F1 Waspada', '0.6981', '0.5667', '0.5283'),
            ('F1 Berisiko', '0.9041', '0.5208', '0.7438 (+22.30%)'),
            ('Recall Berisiko', '0.9296 (93.0%)', '0.3521 (35.2%)', '0.6338 (63.4%)'),
            ('Jawaban Invalid', '0 (0.0%)', '0 (0.0%)', '0 (0.0%)'),
            ('Waktu 200 Data Uji', '0.042 detik (42 ms)', '304 detik (5 menit)', '33 detik (33 detik)'),
            ('Waktu Rata-rata / Data', '0.21 ms', '1.522 ms', '165 ms (9x lebih cepat)'),
            ('File Konfigurasi', 'model_status_akademik.pkl', 'config.json', 'config_service2.json')
        ]
        for m, c1, c2, c3 in tri_metrics:
            row = table.row()
            row.cell(m)
            row.cell(c1)
            row.cell(c2)
            row.cell(c3)

    pdf.ln(2)
    pdf.sub_judul('Analisis Penambahan AI Service 2 (GPT-4o-mini)')
    pdf.paragraf(
        '1. GPT-4o-mini Memperbaiki Deteksi Kelas Berisiko: Masalah terbesar pada Service 1 adalah rendahnya deteksi '
        'mahasiswa Berisiko (recall hanya 35.21%). Saat diganti ke GPT-4o-mini, recall kelas Berisiko naik ke 63.38%, '
        'dan F1 Berisiko naik dari 0.5208 menjadi 0.7438 (+22.30%). GPT-4o-mini lebih tegas mendeteksi mahasiswa yang bermasalah '
        'dan tidak melempar semua keraguan ke status Waspada.'
    )
    pdf.paragraf(
        '2. Jauh Lebih Cepat: GPT-4o-mini menyelesaikan 200 data test hanya dalam 33 detik (165 milidetik per data), '
        'sekitar 9 kali lebih cepat dibanding ai-practicum yang membutuhkan waktu 5 menit. '
        'Kecepatan ini penting agar aplikasi web Streamlit pada Modul 2B terasa responsif.'
    )
    pdf.paragraf(
        '3. DNN Tetap Paling Akurat: Meskipun GPT-4o-mini lebih baik dari Service 1, akurasinya (62.50%) '
        'tetap belum bisa menyaingi DNN (84.00%). Hasil ini membuktikan bahwa untuk data tabel angka, '
        'model machine learning khusus seperti DNN tetap menjadi pilihan utama.'
    )

    if os.path.exists('figures/metrics_comparison.png'):
        pdf.ln(1)
        pdf.image('figures/metrics_comparison.png', x=20, y=None, w=170)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, 'Gambar 3: Perbandingan Akurasi dan F1 per Kelas pada 200 Data Test', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # ================= PAGE 7: 4. KESIMPULAN & GAMBAR 4 =================
    pdf.add_page()
    if os.path.exists('figures/latency_comparison.png'):
        pdf.image('figures/latency_comparison.png', x=38, y=None, w=134)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, 'Gambar 4: Perbandingan Kecepatan Waktu Inferensi per Data (Skala Logaritmik)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(3)

    pdf.judul_bab('4', 'Kesimpulan')
    
    pdf.paragraf(
        '1. DNN Terbukti Terbaik untuk Data Tabel Angka: Model Deep Neural Network (MLPClassifier 64-32-16) '
        'meraih akurasi tertinggi (84.00%) dan F1 macro 82.69%, serta waktu inferensi instan 0.21 milidetik per data tanpa biaya API. '
        'Model ini lolos gerbang evaluasi (F1 >= 0.80) dan siap digunakan untuk deploy di Streamlit pada Modul 1B.'
    )
    pdf.paragraf(
        '2. Karakteristik LLM: LLM siap pakai bisa langsung digunakan tanpa training data ratusan baris, '
        'tetapi akurasinya di data tabel masih terbatas (61-62%) dan rawan bias ke kelas tengah (Waspada). '
        'Prompt few-shot (Iterasi 2) terbukti paling efektif, sedangkan mendikte aturan panjang (Iterasi 4) justru menurunkan skor.'
    )
    pdf.paragraf(
        '3. Penggantian AI Service: Penggunaan OpenAI GPT-4o-mini memperbaiki deteksi kelas Berisiko (F1 naik ke 0.7438) '
        'dan berjalan 9 kali lebih cepat dibanding service bawaan praktikum.'
    )
    pdf.paragraf(
        '4. Saran Penerapan: Di sistem kampus, kombinasi terbaik adalah memakai DNN untuk skrining massal seluruh mahasiswa tiap semester '
        'karena cepat, akurat, dan gratis. Setelah itu, LLM dapat dipakai untuk membuat rekomendasi belajar atau draf pesan personal '
        'bagi mahasiswa yang terdeteksi Waspada atau Berisiko.'
    )
    pdf.paragraf(
        '5. Keamanan: Seluruh pengerjaan praktikum dan dokumen laporan ini dipastikan bersih tanpa menyertakan API Key privat. '
        'Kunci disimpan lewat file .env yang diabaikan oleh git.'
    )

    pdf_path = 'Laporan_Praktikum_AI_Modul_1A_dan_2A.pdf'
    pdf.output(pdf_path)
    print(f"Berhasil membuat {pdf_path} ({pdf.page_no()} halaman)")

if __name__ == '__main__':
    buat_laporan()
