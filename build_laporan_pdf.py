import os
import json
import numpy as np
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

class LaporanPraktikumPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(18, 18, 18)
        
        font_dir = '/usr/share/fonts/truetype/dejavu/'
        self.add_font('DejaVu', '', os.path.join(font_dir, 'DejaVuSans.ttf'))
        self.add_font('DejaVu', 'B', os.path.join(font_dir, 'DejaVuSans-Bold.ttf'))
        self.add_font('DejaVu', 'I', os.path.join(font_dir, 'DejaVuSans-Oblique.ttf'))
        self.add_font('DejaVu', 'BI', os.path.join(font_dir, 'DejaVuSans-BoldOblique.ttf'))
        
        self.add_font('DejaVuMono', '', os.path.join(font_dir, 'DejaVuSansMono.ttf'))
        self.add_font('DejaVuMono', 'B', os.path.join(font_dir, 'DejaVuSansMono-Bold.ttf'))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('DejaVu', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(105, 5, 'Laporan Praktikum AI - Modul 1A & Modul 2A', align='L')
        self.cell(69, 5, 'Ario Veisa Rayanda Utomo (1204230086)', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(18, 22, 192, 22)
        self.ln(3)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(148, 163, 184)
        self.cell(105, 5, 'S1 Sistem Informasi - Telkom University Surabaya', align='L')
        self.cell(69, 5, f'Halaman {self.page_no()} dari {{nb}}', align='R')

    def chapter_title(self, number_str, title_str):
        if self.get_y() > 215:
            self.add_page()
        else:
            self.ln(3)
        self.set_font('DejaVu', 'B', 11.5)
        self.set_text_color(160, 12, 26)  # Telkom Maroon
        self.cell(0, 6.5, f'{number_str}. {title_str}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.set_draw_color(160, 12, 26)
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(2.5)

    def section_title(self, title_str):
        if self.get_y() > 245:
            self.add_page()
        self.set_font('DejaVu', 'B', 9.5)
        self.set_text_color(30, 41, 59)
        self.cell(0, 5.5, title_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(1)

    def body_p(self, text):
        self.set_font('DejaVu', '', 8.5)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 4.4, text, align='J')
        self.ln(1.8)

    def code_box(self, code_text):
        lines = code_text.strip().split('\n')
        line_height = 3.6
        box_height = len(lines) * line_height + 3
        if self.get_y() + box_height > 270:
            self.add_page()
            
        cur_x = self.get_x()
        cur_y = self.get_y()
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(203, 213, 225)
        self.rect(cur_x, cur_y, 174, box_height, style='DF')
        self.set_font('DejaVuMono', '', 7.5)
        self.set_text_color(15, 23, 42)
        self.set_xy(cur_x + 3, cur_y + 1.5)
        for line in lines:
            self.cell(168, line_height, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(cur_x, cur_y + box_height + 2)

    def ensure_space(self, h):
        if self.get_y() + h > 265:
            self.add_page()

def build_pdf():
    pdf = LaporanPraktikumPDF()
    pdf.alias_nb_pages()

    # ================= PAGE 1: COVER PAGE (EXACT STUDENT TEMPLATE) =================
    pdf.add_page()
    pdf.ln(35)
    
    pdf.set_font('DejaVu', 'B', 20)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 9, 'LAPORAN', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(2)
    
    pdf.set_font('DejaVu', 'B', 14)
    pdf.set_text_color(160, 12, 26) # Telkom Maroon
    pdf.cell(0, 7, 'Praktikum Artificial Intelligence and Its Application', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, 'Klasifikasi Status Akademik: Modul 1A & Modul 2A', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.ln(45)
    
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, 'Oleh:', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(2)
    
    pdf.set_font('DejaVu', 'B', 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6.5, 'Ario veisa Rayanda Utomo ( 1204230086 )', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.ln(55)
    
    pdf.set_font('DejaVu', 'B', 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, 'S1 SISTEM INFORMASI', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 6, 'FAKULTAS DIREKTORAT KAMPUS SURABAYA', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(2)
    pdf.cell(0, 6, 'TELKOM UNIVERSITY SURABAYA', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('DejaVu', '', 11)
    pdf.cell(0, 6, '2026', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # ================= CHAPTER 0 =================
    pdf.add_page()
    pdf.chapter_title('0', 'PRAKTIK MODUL 1A (DEEP NEURAL NETWORK)')
    
    pdf.section_title('0.1. Dataset dan Pembagian Data')
    pdf.body_p(
        'Pada praktikum Modul 1A, saya melatih model Deep Neural Network (DNN) untuk mengklasifikasikan status akademik '
        'mahasiswa menjadi Aman, Waspada, atau Berisiko. Dataset yang dipakai adalah dataset_status_akademik.csv dengan total 1.000 data. '
        'Data ini memiliki 6 fitur: ipk, kehadiran, jam_belajar, tugas_terkumpul, nilai_uts, dan aktif_organisasi. '
        'Dataset sudah dibagi lewat kolom "bagian" menjadi 800 data train dan 200 data test. '
        'Data test 200 baris ini tidak disentuh saat training dan dipakai sebagai data uji yang sama persis di Modul 1A dan Modul 2A.'
    )
    
    pdf.section_title('0.2. Pipeline dan Arsitektur Model DNN')
    pdf.body_p(
        'Saya menggabungkan preprocessing dan model ke dalam satu Pipeline scikit-learn. '
        'Lima fitur numerik dinormalisasi menggunakan StandardScaler, dan fitur aktif_organisasi diubah dengan OneHotEncoder. '
        'Untuk model klasifikasi, saya menggunakan MLPClassifier dengan arsitektur 3 hidden layer: layer pertama 64 neuron, '
        'layer kedua 32 neuron, dan layer ketiga 16 neuron. Fungsi aktivasi memakai ReLU, solver Adam, regularisasi L2 (alpha=1e-3), '
        'dan early stopping aktif (10% data train untuk validasi internal).'
    )
    
    pdf.code_box(
        '# Pipeline Preprocessing dan DNN Modul 1A\n'
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
    
    pdf.section_title('0.3. Hasil Training dan Evaluasi Data Test')
    pdf.body_p(
        'Training berhenti di epoch ke-50 karena early stopping dengan akurasi validasi terbaik 87.50%. '
        'Saat diuji pada 200 data test, model memperoleh akurasi 84.00% dan F1 macro 0.8269. '
        'Nilai ini jauh melampaui baseline dummy classifier (F1 0.1800) dan melewati target gerbang kelulusan modul (F1 >= 0.80). '
        'Model berhasil diekspor menjadi model_status_akademik.pkl bersama file konfigurasi model_info.json.'
    )
    
    with pdf.table(col_widths=(34, 26, 26, 26, 30, 32)) as table:
        row = table.row()
        row.cell('Kelas', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Precision', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Recall', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('F1-Score', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Support', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Keterangan', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        row = table.row()
        row.cell('Aman')
        row.cell('0.8784')
        row.cell('0.8784')
        row.cell('0.8784')
        row.cell('74')
        row.cell('Tinggi')
        
        row = table.row()
        row.cell('Waspada')
        row.cell('0.7255')
        row.cell('0.6727')
        row.cell('0.6981')
        row.cell('55')
        row.cell('Paling sulit')
        
        row = table.row()
        row.cell('Berisiko')
        row.cell('0.8800')
        row.cell('0.9296')
        row.cell('0.9041')
        row.cell('71')
        row.cell('Sangat baik')
        
        row = table.row()
        row.cell('Macro Avg / Total', style=FontFace(emphasis="B"))
        row.cell('0.8280', style=FontFace(emphasis="B"))
        row.cell('0.8269', style=FontFace(emphasis="B"))
        row.cell('0.8269', style=FontFace(emphasis="B"))
        row.cell('200', style=FontFace(emphasis="B"))
        row.cell('Lolos (>= 0.80)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))

    pdf.ln(1.5)
    pdf.section_title('0.4. Pengujian Inferensi Mandiri (cek_model.py)')
    pdf.body_p(
        'Saya menguji file .pkl yang sudah disimpan lewat script cek_model.py pada satu contoh profil mahasiswa '
        '(IPK 3.45, Kehadiran 92%, Jam belajar 12, Tugas 95%, UTS 82, Aktif organisasi Ya). '
        'Hasil prediksi model adalah "Aman" dengan probabilitas softmax: Aman = 0.995, Berisiko = 0.000, dan Waspada = 0.005. '
        'Ini membuktikan file model siap dipakai untuk deployment di Streamlit pada Modul 1B.'
    )

    # ================= CHAPTER 1: TUGAS 1 =================
    pdf.add_page()
    pdf.chapter_title('1', 'TABEL PERBANDINGAN DNN VS LLM & ANALISIS EVALUASI (TUGAS 1)')
    
    pdf.section_title('1.1. Tabel Perbandingan Evaluasi pada Data Test yang Sama (200 Sampel)')
    pdf.body_p(
        'Pada Modul 2A, 200 data test yang sama diuji menggunakan AI model service (LLM). '
        'Konfigurasi LLM yang dipakai adalah hasil prompt terbaik dari tahap validasi, yaitu Iterasi 2 (few-shot 6 contoh). '
        'Tabel 1 merangkum perbandingan metrik evaluasi antara DNN (Modul 1A) dan LLM Service 1 (ai-practicum):'
    )
    
    with pdf.table(col_widths=(46, 42, 42, 44)) as table:
        row = table.row()
        row.cell('Metrik Evaluasi', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('DNN (Modul 1A)\nMLPClassifier (64-32-16)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service 1 (Modul 2A)\nai-practicum (Gemini 3.8)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Selisih', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        metrics = [
            ('Akurasi', '0.8400 (84.00%)', '0.6100 (61.00%)', '+23.00% (DNN lebih tinggi)'),
            ('F1-Score (Macro)', '0.8269 (82.69%)', '0.6098 (60.98%)', '+21.71% (DNN lebih tinggi)'),
            ('Precision (Macro)', '0.8280 (82.80%)', '0.7760 (77.60%)', '+5.20% (DNN lebih tinggi)'),
            ('Recall (Macro)', '0.8269 (82.69%)', '0.6337 (63.37%)', '+19.32% (DNN lebih tinggi)'),
            ('F1 Aman', '0.8784', '0.7419', '+0.1365 (DNN lebih tinggi)'),
            ('F1 Waspada', '0.6981', '0.5667', '+0.1314 (DNN lebih tinggi)'),
            ('F1 Berisiko', '0.9041', '0.5208', '+0.3833 (DNN lebih tinggi)'),
            ('Respon Invalid', '0 (0.0%)', '0 (0.0%)', 'Keduanya patuh format'),
            ('Target Gerbang', 'Lolos (0.8269 >= 0.80)', 'Tidak Lolos (0.6098 < 0.70)', 'Hanya DNN lolos gerbang')
        ]
        for m, v1, v2, diff in metrics:
            row = table.row()
            row.cell(m, style=FontFace(emphasis="B" if "Akurasi" in m or "Macro" in m else None))
            row.cell(v1)
            row.cell(v2)
            row.cell(diff, style=FontFace(fill_color=(220, 252, 231) if "DNN" in diff else (254, 242, 242)))

    pdf.ln(2)
    pdf.section_title('1.2. Tabel Confusion Matrix')
    pdf.body_p(
        'Rincian tebakan kedua model pada 200 data test (74 Aman, 55 Waspada, 71 Berisiko) terlihat pada Tabel 2:'
    )
    
    with pdf.table(col_widths=(34, 24, 24, 24, 24, 24, 24)) as table:
        row = table.row()
        row.cell('Kelas Aktual', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('DNN: Aman', style=FontFace(emphasis="B", fill_color=(224, 242, 254)))
        row.cell('DNN: Waspada', style=FontFace(emphasis="B", fill_color=(224, 242, 254)))
        row.cell('DNN: Berisiko', style=FontFace(emphasis="B", fill_color=(224, 242, 254)))
        row.cell('LLM: Aman', style=FontFace(emphasis="B", fill_color=(254, 243, 199)))
        row.cell('LLM: Waspada', style=FontFace(emphasis="B", fill_color=(254, 243, 199)))
        row.cell('LLM: Berisiko', style=FontFace(emphasis="B", fill_color=(254, 243, 199)))
        
        row = table.row()
        row.cell('Asli Aman (74)')
        row.cell('65 (87.8%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('9 (12.2%)')
        row.cell('0 (0.0%)')
        row.cell('46 (62.2%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('28 (37.8%)')
        row.cell('0 (0.0%)')
        
        row = table.row()
        row.cell('Asli Waspada (55)')
        row.cell('9 (16.4%)')
        row.cell('37 (67.3%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('9 (16.4%)')
        row.cell('4 (7.3%)')
        row.cell('51 (92.7%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('0 (0.0%)')
        
        row = table.row()
        row.cell('Asli Berisiko (71)')
        row.cell('0 (0.0%)')
        row.cell('5 (7.0%)')
        row.cell('66 (93.0%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('0 (0.0%)')
        row.cell('46 (64.8%)', style=FontFace(fill_color=(254, 226, 226)))
        row.cell('25 (35.2%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))

    pdf.ln(1.5)
    pdf.section_title('1.3. Analisis Hasil Evaluasi Data Test')
    pdf.body_p(
        '1. Mengapa Akurasi DNN Jauh Lebih Tinggi? Akurasi DNN mencapai 84%, sedangkan LLM hanya 61%. '
        'DNN memproses angka secara langsung dan mengoptimalkan fungsi matematis melalui backpropagation dari 800 data latih. '
        'Model DNN bisa membedakan batas tipis antar-angka (misal IPK 2.74 vs 2.76). '
        'Sebaliknya, LLM membaca data sebagai kalimat teks biasa. LLM memperkirakan probabilitas kata berikutnya '
        'lewat contoh di prompt, tanpa pernah mengubah bobotnya untuk memahami batas numerik data ini secara presisi.'
    )
    pdf.body_p(
        '2. LLM Terlalu Sering Menebak "Waspada": Pada confusion matrix, LLM Service 1 menebak label "Waspada" sebanyak 125 kali '
        'dari total 200 data (62.5% dari seluruh tebakan). Mahasiswa Berisiko sebanyak 46 orang (64.8%) keliru ditebak sebagai Waspada. '
        'Begitu juga dengan 28 mahasiswa Aman yang turun status menjadi Waspada. '
        'LLM cenderung memilih jawaban tengah saat ragu menimbang angka. Dampaknya buruk untuk sistem kampus: '
        'recall kelas Berisiko anjlok ke 35.21%, artinya 46 mahasiswa yang sebenarnya terancam drop out tidak terdeteksi.'
    )
    pdf.body_p(
        '3. Tidak Ada Kesalahan Ekstrem: Nilai positif dari kedua model adalah tidak pernah menukar kelas Aman dan Berisiko secara langsung '
        '(0 mahasiswa Aman ditebak Berisiko, dan 0 mahasiswa Berisiko ditebak Aman). Namun DNN jauh lebih tegas: '
        'DNN mendeteksi 66 dari 71 mahasiswa Berisiko (recall 93%), sedangkan LLM hanya menemukan 25 mahasiswa.'
    )

    # ================= CHAPTER 2: TUGAS 2 =================
    pdf.add_page()
    pdf.chapter_title('2', 'ANALISIS KELEBIHAN DAN KEKURANGAN DNN VS LLM (TUGAS 2)')
    
    pdf.section_title('2.1. Tabel Perbandingan Multi-Aspek')
    pdf.body_p(
        'Berikut perbandingan antara model terlatih lokal (DNN) dan model layanan cloud (LLM) pada berbagai aspek teknis dan operasional:'
    )
    
    with pdf.table(col_widths=(32, 71, 71)) as table:
        row = table.row()
        row.cell('Aspek', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('DNN (Modul 1A)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service (Modul 2A)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        dims = [
            ('Akurasi & F1-Score',
             'Tinggi (Akurasi 84.00%, F1 0.8269). Mampu memetakan pola angka tabular dengan batas yang tegas.',
             'Sedang (Akurasi 61.00%, F1 0.6098). Kurang peka membedakan angka-angka yang berdekatan.'),
            ('Kelas Tersulit',
             'Kelas Waspada (F1 0.6981) karena berada di tengah-tengah antara Aman dan Berisiko.',
             'Kelas Berisiko (Recall 35.21%) dan Waspada (Precision 40.80%) karena model terlalu sering memilih kelas tengah.'),
            ('Biaya (Cost)',
             'Gratis. Model berjalan di komputer atau server lokal tanpa biaya pemanggilan API.',
             'Berbayar per request atau token API. Penggunaan rutin pada ribuan mahasiswa akan memakan biaya terus-menerus.'),
            ('Kecepatan (Latency)',
             'Sangat cepat (~0.21 milidetik per data, total 42 milidetik untuk 200 data). Tanpa jeda jaringan internet.',
             'Lambat (~1.522 milidetik per data, total 304 detik atau 5 menit untuk 200 data) karena harus kirim request ke server cloud.'),
            ('Kebutuhan Data',
             'Butuh ratusan data berlabel (800 baris train) agar bobot neural network bisa belajar pola dengan benar.',
             'Bisa jalan dengan sedikit data. Cukup beri instruksi prompt dan 6 contoh data (few-shot in-context learning).'),
            ('Privasi Data',
             'Aman. Data nilai dan presensi mahasiswa tetap tersimpan di server kampus dan tidak keluar ke pihak ketiga.',
             'Ada risiko privasi. Data akademik mahasiswa harus dikirim ke internet menuju server penyedia LLM.'),
            ('Konsistensi Hasil',
             'Konsisten 100%. File model .pkl akan selalu mengeluarkan hasil yang persis sama untuk input yang sama.',
             'Bisa berubah. Walaupun temperature=0, pembaruan versi model oleh penyedia API bisa mengubah hasil tebakan.'),
            ('Penambahan Fitur Baru',
             'Kaku. Kalau ada fitur teks baru (misal catatan dosen wali), kita harus bikin arsitektur dan melatih ulang model.',
             'Sangat mudah. Konteks teks tambahan bisa langsung kita tempelkan ke dalam prompt tanpa perlu training ulang.')
        ]
        
        for d, c1, c2 in dims:
            row = table.row()
            row.cell(d, style=FontFace(emphasis="B"))
            row.cell(c1)
            row.cell(c2)

    pdf.ln(2)
    pdf.section_title('2.2. Pembahasan Kelebihan dan Kekurangan')
    pdf.body_p(
        '1. Kenapa Kelas Waspada Paling Sulit? Kedua model sama-sama paling kesulitan di kelas Waspada. '
        'Status Waspada berisi mahasiswa dengan indikator yang saling bertolak belakang, misalnya IPK tinggi 3.40 tetapi kehadiran rendah 72%, '
        'atau sebaliknya kehadiran 95% tetapi nilai UTS 40. DNN menangani kondisi ini dengan mencari bobot kompromi terbaik, '
        'sehingga menghasilkan F1 0.6981. Sedangkan LLM justru memakai Waspada sebagai jawaban aman saat ragu, '
        'sehingga presisi kelas Waspada anjlok ke 40.80% (dari 125 tebakan Waspada, hanya 51 yang aslinya Waspada).'
    )
    pdf.body_p(
        '2. Perbandingan Efisiensi: Untuk data tabel akademik biasa, DNN menang telak karena kecepatannya 7.000 kali lebih cepat '
        'dan biayanya nol. Namun kelebihan LLM ada pada kecepatan awal pembuatan: kalau kampus belum sempat mengumpulkan 800 data latih '
        'yang sudah diverifikasi dosen, kita bisa langsung memakai LLM sebagai solusi sementara hanya dengan beberapa baris prompt.'
    )

    pdf.ensure_space(55)
    if os.path.exists('figures/confusion_matrices_comparison.png'):
        pdf.image('figures/confusion_matrices_comparison.png', x=18, y=None, w=174)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4, 'Gambar 1: Perbandingan Confusion Matrix DNN vs LLM Service 1 vs LLM Service 2 pada 200 Data Test', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(1)

    # ================= CHAPTER 3: TUGAS 3 =================
    pdf.add_page()
    pdf.chapter_title('3', 'PENGGANTIAN AI SERVICE & KOMPARASI TRI-MODEL (TUGAS 3)')
    
    pdf.section_title('3.1. Penggantian AI Service: OpenAI GPT-4o-mini')
    pdf.body_p(
        'Untuk Tugas 3, saya mengganti AI service di Modul 2A dari ai-practicum ke OpenAI GPT-4o-mini. '
        'Model ini dipilih karena merupakan model bahasa berukuran ringkas dengan kecepatan inferensi tinggi dan biaya token yang murah.'
    )
    
    pdf.section_title('3.2. Hasil Uji Iterasi Prompt pada Data Validasi (N=30)')
    pdf.body_p(
        'Saya menguji 4 iterasi prompt yang sama pada 30 data validasi (10 Aman, 10 Waspada, 10 Berisiko) '
        'untuk kedua layanan LLM. Hasilnya dirangkum pada Tabel 4:'
    )
    
    with pdf.table(col_widths=(46, 32, 33, 33, 30)) as table:
        row = table.row()
        row.cell('Versi Prompt', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Akurasi (Service 1)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('F1 Macro (Service 1)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('Akurasi (GPT-4o-mini)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('F1 Macro (GPT)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        row = table.row()
        row.cell('Iterasi 1 (Zero-Shot)')
        row.cell('0.4667 (46.67%)')
        row.cell('0.3996')
        row.cell('0.5667 (56.67%)')
        row.cell('0.4743')
        
        row = table.row()
        row.cell('Iterasi 2 (Few-Shot 6 Contoh)', style=FontFace(emphasis="B"))
        row.cell('0.6667 (66.67%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('0.6627 (Terbaik)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('0.7667 (76.67%)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        row.cell('0.7707 (Terbaik)', style=FontFace(emphasis="B", fill_color=(220, 252, 231)))
        
        row = table.row()
        row.cell('Iterasi 3 (Few-Shot + Median)')
        row.cell('0.6333 (63.33%)')
        row.cell('0.6180')
        row.cell('0.6000 (60.00%)')
        row.cell('0.5778')
        
        row = table.row()
        row.cell('Iterasi 4 (Perbaikan Aturan Logika)')
        row.cell('0.4667 (46.67%)')
        row.cell('0.3761 (Turun)')
        row.cell('0.5000 (50.00%)')
        row.cell('0.4603 (Turun)')

    pdf.ln(1.5)
    pdf.body_p(
        'Kenapa Iterasi 4 Malah Turun? Pada iterasi 4, saya menambahkan aturan batasan manual '
        '("Aman: IPK >= 3.20, Berisiko: IPK < 2.75 ATAU kehadiran < 75% ATAU tugas < 60%..."). '
        'Skor F1 kedua model justru merosot tajam (S1 turun ke 0.3761, GPT-4o-mini turun ke 0.4603). '
        'Penyebabnya adalah prompt yang terlalu rumit: kalimat logika bertingkat dengan banyak kata ATAU membuat model bingung '
        'memprioritaskan fitur saat ada kondisi yang saling tumpang tindih. '
        'Memberi contoh data nyata lewat few-shot (Iterasi 2) terbukti jauh lebih efektif daripada mendikte aturan logika panjang.'
    )

    pdf.ensure_space(52)
    if os.path.exists('figures/prompt_iteration_comparison.png'):
        pdf.image('figures/prompt_iteration_comparison.png', x=36, y=None, w=138)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4, 'Gambar 2: Grafik Skor F1 Macro pada 4 Iterasi Prompt (Data Validasi N=30)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(1)

    pdf.section_title('3.3. Tabel Perbandingan 3 Model pada Data Test')
    pdf.body_p(
        'Tabel 5 menyajikan perbandingan hasil evaluasi pada 200 data test yang sama setelah menambahkan OpenAI GPT-4o-mini, '
        'dan Tabel 6 membandingkan karakteristik operasionalnya:'
    )
    
    with pdf.table(col_widths=(44, 38, 46, 46)) as table:
        row = table.row()
        row.cell('Metrik Evaluasi Test', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('DNN (Modul 1A)\nMLPClassifier (64-32-16)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service 1 (Modul 2A)\nai-practicum (Gemini 3.8)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service 2 (Modul 2A Baru)\nOpenAI GPT-4o-mini', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        tri_metrics = [
            ('Akurasi Keseluruhan', '0.8400 (84.00%)', '0.6100 (61.00%)', '0.6250 (62.50%)'),
            ('F1-Score (Macro)', '0.8269 (82.69%)', '0.6098 (60.98%)', '0.6351 (63.51%)'),
            ('F1 Aman', '0.8784', '0.7419', '0.6333'),
            ('F1 Waspada', '0.6981', '0.5667', '0.5283'),
            ('F1 Berisiko', '0.9041', '0.5208', '0.7438 (+22.30%)'),
            ('Recall Berisiko', '0.9296 (93.0%)', '0.3521 (35.2%)', '0.6338 (63.4%)'),
            ('Respon Invalid', '0 (0.0%)', '0 (0.0%)', '0 (0.0%)'),
            ('Waktu 200 Data Uji', '0.042 detik (42 ms)', '304.56 detik (5 menit)', '33.14 detik (33 detik)'),
            ('Rata-rata Waktu / Data', '0.21 milidetik', '1.522,8 milidetik', '165,7 milidetik'),
            ('File Artefak', 'model_status_akademik.pkl', 'config.json', 'config_service2.json')
        ]
        for m, c1, c2, c3 in tri_metrics:
            row = table.row()
            row.cell(m, style=FontFace(emphasis="B" if "Akurasi" in m or "Macro" in m or "Waktu" in m else None))
            row.cell(c1)
            row.cell(c2)
            row.cell(c3, style=FontFace(emphasis="B" if "0.7438" in c3 or "63.51%" in c3 or "165,7" in c3 else None))

    pdf.ln(2)
    pdf.ensure_space(60)
    
    with pdf.table(col_widths=(30, 48, 48, 48)) as table:
        row = table.row()
        row.cell('Aspek', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('DNN (Modul 1A)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service 1 (ai-practicum)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        row.cell('LLM Service 2 (GPT-4o-mini)', style=FontFace(emphasis="B", fill_color=(241, 245, 249)))
        
        tri_arch = [
            ('Akurasi Tabular', 'Sangat tinggi (84%). Paling presisi untuk data tabel angka.', 'Sedang (61%). Cenderung ragu membedakan batas angka.', 'Sedang (62.5%). Sedikit lebih baik dari Service 1.'),
            ('Distribusi Tebakan', 'Seimbang (A:65, W:37, B:66). Sesuai dengan data aslinya.', 'Sangat berat ke Waspada (W:125, A:50, B:25). Recall Berisiko rendah.', 'Lebih merata (W:104, A:46, B:50). Recall Berisiko naik ke 63.4%.'),
            ('Kecepatan', 'Paling cepat (0.21 ms per data). 780x lebih cepat dari GPT-4o-mini.', 'Paling lambat (1.522 ms per data). Terhambat antrean server proxy.', 'Cepat untuk ukuran cloud (165 ms per data). 9.2x lebih cepat dari Service 1.'),
            ('Biaya', 'Gratis $0 (jalan di komputer sendiri).', 'Pakai kuota server praktikum.', 'Hemat token (biaya resmi $0.15 per 1 juta token).'),
            ('Format Simpan', 'model_status_akademik.pkl (file bobot model 85 KB).', 'config.json (file teks prompt dan contoh).', 'config_service2.json (file teks prompt dan contoh).')
        ]
        for d, c1, c2, c3 in tri_arch:
            row = table.row()
            row.cell(d, style=FontFace(emphasis="B"))
            row.cell(c1)
            row.cell(c2)
            row.cell(c3)

    pdf.ln(1.5)
    pdf.section_title('3.4. Analisis Perbandingan Tiga Model')
    pdf.body_p(
        '1. GPT-4o-mini Memperbaiki Deteksi Kelas Berisiko: Masalah utama pada Service 1 adalah rendahnya deteksi '
        'mahasiswa Berisiko (recall hanya 35.21%). Saat diganti ke GPT-4o-mini, recall kelas Berisiko melonjak ke 63.38%, '
        'dan skor F1 Berisiko naik dari 0.5208 menjadi 0.7438 (+22.30%). GPT-4o-mini lebih tegas dalam mengidentifikasi '
        'mahasiswa bermasalah dan tidak melempar semua keraguan ke status Waspada.'
    )
    pdf.body_p(
        '2. Peningkatan Kecepatan 9 Kali Lipat: GPT-4o-mini menyelesaikan 200 data test hanya dalam 33 detik (165 ms per data), '
        'jauh lebih cepat dibanding ai-practicum yang memakan waktu 5 menit (1.522 ms per data). '
        'Kecepatan ini sangat membantu agar aplikasi dashboard di Modul 2B tidak terasa lambat saat dibuka pengguna.'
    )

    pdf.ensure_space(52)
    if os.path.exists('figures/metrics_comparison.png'):
        pdf.image('figures/metrics_comparison.png', x=20, y=None, w=170)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4, 'Gambar 3: Perbandingan Akurasi dan F1-Score per Kelas pada Data Test (200 Sampel)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(1)

    pdf.ensure_space(48)
    if os.path.exists('figures/latency_comparison.png'):
        pdf.image('figures/latency_comparison.png', x=36, y=None, w=138)
        pdf.set_font('DejaVu', 'I', 7.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4, 'Gambar 4: Perbandingan Waktu Inferensi per Data Uji (Skala Logaritmik)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(1)

    # ================= CHAPTER 4 =================
    pdf.chapter_title('4', 'KESIMPULAN')
    
    pdf.body_p(
        '1. DNN Paling Cocok untuk Data Tabel Angka: Deep Neural Network (MLPClassifier) terbukti paling unggul '
        'dengan akurasi 84.00% dan F1 macro 82.69%, serta waktu inferensi instan 0.21 milidetik per data. '
        'Model ini lolos gerbang evaluasi (F1 >= 0.80) dan siap dideploy di Streamlit pada Modul 1B.'
    )
    pdf.body_p(
        '2. Kelemahan dan Solusi Prompt LLM: LLM siap pakai bisa dipakai tanpa perlu training bobot, '
        'tetapi akurasinya di data tabel angka masih terbatas (61-62%). LLM cenderung bias menebak kelas tengah (Waspada). '
        'Teknik few-shot (Iterasi 2) terbukti menjadi prompt paling efektif, sedangkan mendikte aturan manual panjang (Iterasi 4) '
        'justru memperburuk akurasi.'
    )
    pdf.body_p(
        '3. Manfaat GPT-4o-mini: Mengganti service ke GPT-4o-mini berhasil menaikkan F1 Berisiko dari 0.52 ke 0.74 '
        'dan mempercepat waktu inferensi 9 kali lipat dibanding service bawaan praktikum.'
    )
    pdf.body_p(
        '4. Saran Penerapan di Kampus: Kombinasi terbaik adalah memakai DNN untuk mengecek status seluruh mahasiswa '
        'secara massal tiap semester karena cepat, akurat, dan gratis. Setelah itu, LLM dapat difungsikan untuk menyusun '
        'saran belajar atau draf surat bimbingan khusus bagi mahasiswa yang terdeteksi Waspada atau Berisiko.'
    )
    pdf.body_p(
        '5. Keamanan Kredensial: Seluruh script praktikum dan laporan ini telah dipastikan bebas dari API Key privat. '
        'Kunci disimpan aman lewat file .env yang dikecualikan di file .gitignore.'
    )

    pdf_path = 'Laporan_Praktikum_AI_Modul_1A_dan_2A.pdf'
    pdf.output(pdf_path)
    print(f"Successfully generated {pdf_path} (Pages: {pdf.page_no()})")

if __name__ == '__main__':
    build_pdf()
