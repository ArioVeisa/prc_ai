import json
from pathlib import Path
import sys
import time
import joblib
import pandas as pd
import streamlit as st

DIR = Path(__file__).resolve().parent
if str(DIR) not in sys.path:
    sys.path.insert(0, str(DIR))

from classifier_heart import NAMA_FITUR, classify, load_config

st.set_page_config(
    page_title="CardioGuard AI - Prediksi Penyakit Jantung",
    page_icon="❤️",
    layout="wide"
)

# ---------- 1. Muat Model Library & Konfigurasi LLM ----------
@st.cache_resource
def load_library_model():
    return joblib.load(DIR / "model_heart.pkl")

@st.cache_data
def load_meta_info():
    with open(DIR / "model_info.json") as f:
        return json.load(f)

@st.cache_data
def load_sample_csv():
    with open(DIR / "sample_test_heart.csv", "rb") as f:
        return f.read()

model_rf = load_library_model()
meta_info = load_meta_info()
cfg_llm = load_config(DIR / "config_heart.json")
sample_csv_bytes = load_sample_csv()

# Konfigurasi client LLM (aman dari secrets)
api_key = None
base_url = None

if "API_KEY" in st.secrets and str(st.secrets["API_KEY"]).strip():
    api_key = str(st.secrets["API_KEY"]).strip()
    base_url = st.secrets.get("BASE_URL")
elif "GROQ_API_KEY" in st.secrets and str(st.secrets["GROQ_API_KEY"]).strip():
    api_key = str(st.secrets["GROQ_API_KEY"]).strip()

@st.cache_resource
def get_llm_client():
    if not api_key:
        return None
    if base_url:
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        from groq import Groq
        return Groq(api_key=api_key)

llm_client = get_llm_client()

@st.cache_data(show_spinner=False)
def predict_llm_cached(data_dict):
    if llm_client is None:
        return "API Key belum terpasang"
    return classify(llm_client, cfg_llm, data_dict)

# ---------- 2. Sidebar ----------
with st.sidebar:
    st.header("❤️ CardioGuard AI")
    st.caption("Studi Kasus: Heart Failure Prediction (Kaggle/UCI)")
    
    st.subheader("Pilihan Engine Prediksi")
    engine = st.radio(
        "Pilih Model:",
        ["Komparasi Keduanya (Library vs LLM)", "Random Forest (Library .pkl)", "LLM Service (ai-practicum)"]
    )
    
    st.divider()
    st.subheader("Evaluasi Data Uji (N=50)")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Akurasi RF", f"{meta_info['metrik']['accuracy']:.1%}")
        st.metric("F1 RF", f"{meta_info['metrik']['f1_macro']:.3f}")
    with c2:
        st.metric("Akurasi LLM", f"{cfg_llm['evaluasi']['accuracy']:.1%}")
        st.metric("F1 LLM", f"{cfg_llm['evaluasi']['f1_macro']:.3f}")
    
    st.divider()
    st.subheader("📥 Data Sampel Uji")
    st.write("Unduh 15 sampel data pasien untuk diujicobakan pada tab CSV:")
    st.download_button(
        label="Unduh sample_test_heart.csv",
        data=sample_csv_bytes,
        file_name="sample_test_heart.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------- 3. Header Utama ----------
st.title("❤️ Sistem Deteksi Dini Risiko Penyakit Jantung")
st.write(
    "Aplikasi komparasi AI berbasis **Machine Learning Library (Random Forest)** "
    "dan **AI Model Service (LLM Few-Shot)** untuk klasifikasi risiko penyakit jantung."
)

tab1, tab2 = st.tabs(["🩺 Prediksi Satu Pasien", "📁 Prediksi Batch dari File CSV"])

# ---------- 4. Tab 1: Form Input Pasien ----------
with tab1:
    with st.form("form_pasien"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Indikator Demografi & Nyeri")
            age = st.number_input("Usia (Age)", min_value=18, max_value=90, value=52, step=1)
            sex = st.selectbox("Jenis Kelamin (Sex)", options=["M", "F"], format_func=lambda x: "Pria (M)" if x == "M" else "Wanita (F)")
            cp = st.selectbox(
                "Tipe Nyeri Dada (ChestPainType)",
                options=["ASY", "NAP", "ATA", "TA"],
                format_func=lambda x: {
                    "ASY": "ASY - Asimptomatik (Paling Berisiko)",
                    "NAP": "NAP - Non-Anginal Pain",
                    "ATA": "ATA - Atypical Angina",
                    "TA": "TA - Typical Angina"
                }[x]
            )
            resting_bp = st.slider("Tekanan Darah Istirahat (RestingBP, mmHg)", 80, 200, 130)
            chol = st.slider("Kolesterol Serum (Cholesterol, mg/dL)", 0, 500, 220)
            fasting_bs = st.radio("Gula Darah Puasa > 120 mg/dL? (FastingBS)", [0, 1], format_func=lambda x: "Ya (> 120)" if x == 1 else "Tidak (<= 120)", horizontal=True)

        with col2:
            st.markdown("##### Indikator Klinis & EKG")
            resting_ecg = st.selectbox("Hasil EKG Istirahat (RestingECG)", options=["Normal", "ST", "LVH"])
            max_hr = st.slider("Detak Jantung Maksimum (MaxHR, bpm)", 60, 210, 145)
            ex_angina = st.radio("Nyeri Dada Saat Olahraga? (ExerciseAngina)", ["N", "Y"], format_func=lambda x: "Ya (Y)" if x == "Y" else "Tidak (N)", horizontal=True)
            oldpeak = st.number_input("Depresi ST Akibat Olahraga (Oldpeak)", min_value=-2.0, max_value=6.0, value=1.0, step=0.1)
            st_slope = st.selectbox(
                "Kemiringan Segmen ST Puncak (ST_Slope)",
                options=["Up", "Flat", "Down"],
                format_func=lambda x: {
                    "Up": "Up - Menanjak (Indikasi Sehat)",
                    "Flat": "Flat - Datar (Indikasi Risiko)",
                    "Down": "Down - Menurun (Indikasi Risiko Berat)"
                }[x]
            )

        submit = st.form_submit_button("Analisis Risiko Pasien", use_container_width=True)

    if submit:
        data_input = {
            "Age": age, "Sex": sex, "ChestPainType": cp, "RestingBP": resting_bp,
            "Cholesterol": chol, "FastingBS": fasting_bs, "RestingECG": resting_ecg,
            "MaxHR": max_hr, "ExerciseAngina": ex_angina, "Oldpeak": oldpeak, "ST_Slope": st_slope
        }
        df_single = pd.DataFrame([data_input])
        
        st.subheader("Hasil Analisis:")
        
        # 1. Random Forest Inference
        rf_pred = model_rf.predict(df_single)[0]
        rf_proba = pd.Series(model_rf.predict_proba(df_single)[0], index=model_rf.classes_)
        
        # 2. LLM Inference
        llm_pred = None
        if engine != "Random Forest (Library .pkl)":
            with st.spinner("Menghubungi AI Model Service..."):
                llm_pred = predict_llm_cached(data_input)
        
        if engine == "Random Forest (Library .pkl)":
            if rf_pred == "Penyakit Jantung":
                st.error(f"⚠️ Prediksi: **Penyakit Jantung** (Keyakinan: {rf_proba['Penyakit Jantung']:.1%})")
            else:
                st.success(f"✅ Prediksi: **Normal** (Keyakinan: {rf_proba['Normal']:.1%})")
            st.bar_chart(rf_proba.rename("Probabilitas"))
            
        elif engine == "LLM Service (ai-practicum)":
            if llm_pred == "Penyakit Jantung":
                st.error("⚠️ Prediksi LLM: **Penyakit Jantung** (Terindikasi Risiko Jantung)")
            else:
                st.success("✅ Prediksi LLM: **Normal** (Kondisi Jantung Sehat)")
                
        else: # Komparasi Keduanya
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown("#### Model Library (Random Forest)")
                if rf_pred == "Penyakit Jantung":
                    st.error(f"Prediksi: **Penyakit Jantung**\nKeyakinan: {rf_proba['Penyakit Jantung']:.1%}")
                else:
                    st.success(f"Prediksi: **Normal**\nKeyakinan: {rf_proba['Normal']:.1%}")
                st.bar_chart(rf_proba.rename("Probabilitas"))
                
            with col_res2:
                st.markdown("#### AI Model Service (LLM Few-Shot)")
                if llm_pred == "Penyakit Jantung":
                    st.error("Prediksi: **Penyakit Jantung**\nPenalaran: Fitur klinis mengindikasikan iskemia miokard.")
                else:
                    st.success("Prediksi: **Normal**\nPenalaran: Respon fisiologis dalam batas toleransi normal.")
                
                # Agreement check
                if rf_pred == llm_pred:
                    st.info("🤝 **Konsensus AI:** Kedua model menyepakati diagnosa yang sama.")
                else:
                    st.warning("⚠️ **Perbedaan Prediksi:** Model Library dan LLM memiliki diagnosa berbeda untuk profil ini.")

# ---------- 5. Tab 2: Batch CSV Prediction ----------
with tab2:
    st.markdown("##### Unggah File CSV untuk Prediksi Sekaligus")
    st.write(
        "File CSV harus memuat kolom: "
        + ", ".join(f"`{c}`" for c in NAMA_FITUR)
        + ". Kolom identitas seperti `Nama_Pasien` akan tetap disertakan pada hasil."
    )
    
    uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        missing_cols = [c for c in NAMA_FITUR if c not in df_upload.columns]
        
        if missing_cols:
            st.error(f"Kolom berikut tidak ditemukan dalam file: {', '.join(missing_cols)}")
        else:
            st.write(f"Menampilkan {min(len(df_upload), 20)} baris data:")
            st.dataframe(df_upload.head(20))
            
            if st.button("Mulai Prediksi Batch", use_container_width=True):
                # Prediksi Library
                df_upload["Prediksi_Random_Forest"] = model_rf.predict(df_upload[NAMA_FITUR])
                
                # Jika mode LLM atau Komparasi, prediksi juga dengan LLM (dibatasi 15 baris agar cepat)
                if engine != "Random Forest (Library .pkl)":
                    st.write("Menjalankan inferensi LLM Service...")
                    prog_bar = st.progress(0.0)
                    llm_batch_res = []
                    limit_rows = min(len(df_upload), 15)
                    for idx, (_, r) in enumerate(df_upload.head(limit_rows).iterrows(), start=1):
                        row_dict = dict(r[NAMA_FITUR])
                        llm_batch_res.append(predict_llm_cached(row_dict))
                        prog_bar.progress(idx / limit_rows)
                        time.sleep(0.5)
                    df_upload["Prediksi_LLM"] = llm_batch_res + ["-"] * (len(df_upload) - limit_rows)
                
                st.success("Prediksi batch selesai!")
                st.dataframe(df_upload)
                
                st.markdown("##### Distribusi Hasil Prediksi:")
                st.write(df_upload["Prediksi_Random_Forest"].value_counts())
                
                st.download_button(
                    label="Unduh Hasil Prediksi (.csv)",
                    data=df_upload.to_csv(index=False),
                    file_name="hasil_prediksi_penyakit_jantung.csv",
                    mime="text/csv",
                    use_container_width=True
                )
