import concurrent.futures
import json
import os
import sys
import time
import joblib
import numpy as np
import pandas as pd
from openai import OpenAI
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from classifier_heart import classify, load_config

# 1. Load data & models
test_df = pd.read_csv("test.csv")
# Take 50 stratified samples for fair comparison
sample_eval = test_df.sample(50, random_state=42).reset_index(drop=True)

model_rf = joblib.load("model_heart.pkl")
with open("model_info.json") as f:
    info_rf = json.load(f)

cfg_llm = load_config("config_heart.json")
api_key = os.getenv("API_KEY", "sk-b7f268f48d288357-bzbyya-48b7884e")
base_url = os.getenv("BASE_URL", "https://rutaau4.abc-tunnel.us/v1")
client = OpenAI(api_key=api_key, base_url=base_url)

FEATURES = info_rf["fitur_numerik"] + info_rf["fitur_kategori"]
y_true = sample_eval["Target"].tolist()

print(f"Evaluating {len(sample_eval)} test samples...")

# --- 2. Evaluate Library (Random Forest) ---
t0 = time.time()
rf_preds = model_rf.predict(sample_eval[FEATURES]).tolist()
rf_proba = model_rf.predict_proba(sample_eval[FEATURES])
rf_total_time = (time.time() - t0) * 1000
rf_avg_latency = rf_total_time / len(sample_eval)

rf_acc = accuracy_score(y_true, rf_preds)
rf_f1 = f1_score(y_true, rf_preds, average="macro")
rf_prec = precision_score(y_true, rf_preds, average="macro")
rf_rec = recall_score(y_true, rf_preds, average="macro")
rf_cm = confusion_matrix(y_true, rf_preds, labels=["Normal", "Penyakit Jantung"]).tolist()

print("\n=== Library Model (Random Forest) ===")
print(f"Accuracy : {rf_acc:.4f}")
print(f"F1 Macro : {rf_f1:.4f}")
print(f"Avg Latency : {rf_avg_latency:.2f} ms/sample")
print("Confusion Matrix:\n", np.array(rf_cm))

# --- 3. Evaluate AI Model Service (LLM) ---
print("\nRunning LLM evaluation (50 samples)...")
llm_preds = []
llm_latencies = []

def eval_single_llm(row):
    t_start = time.time()
    pred = classify(client, cfg_llm, dict(row))
    lat = (time.time() - t_start) * 1000
    return pred, lat

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(eval_single_llm, [row for _, row in sample_eval.iterrows()]))

llm_preds = [r[0] for r in results]
llm_latencies = [r[1] for r in results]
llm_avg_latency = float(np.mean(llm_latencies))

llm_acc = accuracy_score(y_true, llm_preds)
llm_f1 = f1_score(y_true, llm_preds, average="macro")
llm_prec = precision_score(y_true, llm_preds, average="macro")
llm_rec = recall_score(y_true, llm_preds, average="macro")
llm_cm = confusion_matrix(y_true, llm_preds, labels=["Normal", "Penyakit Jantung"]).tolist()

print("\n=== AI Model Service (LLM Few-Shot) ===")
print(f"Accuracy : {llm_acc:.4f}")
print(f"F1 Macro : {llm_f1:.4f}")
print(f"Avg Latency : {llm_avg_latency:.2f} ms/sample")
print("Confusion Matrix:\n", np.array(llm_cm))

# 4. Save evaluation CSVs
sample_eval["pred_rf"] = rf_preds
sample_eval["pred_llm"] = llm_preds
sample_eval["latensi_llm_ms"] = llm_latencies
sample_eval.to_csv("hasil_evaluasi_komparasi.csv", index=False)

summary = {
    "n_samples": len(sample_eval),
    "metrics": {
        "Random Forest (Library)": {
            "accuracy": rf_acc,
            "f1_macro": rf_f1,
            "precision_macro": rf_prec,
            "recall_macro": rf_rec,
            "latency_ms": rf_avg_latency,
            "confusion_matrix": rf_cm
        },
        "LLM Service (ai-practicum)": {
            "accuracy": llm_acc,
            "f1_macro": llm_f1,
            "precision_macro": llm_prec,
            "recall_macro": llm_rec,
            "latency_ms": llm_avg_latency,
            "confusion_matrix": llm_cm
        }
    }
}

with open("evaluasi_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\nSaved hasil_evaluasi_komparasi.csv and evaluasi_summary.json successfully.")
