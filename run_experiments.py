import os
import sys
import time
import json
import pandas as pd
import numpy as np
from datetime import date
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

sys.path.append('Modul_2A')
from classifier import NAMA_FITUR, build_messages, parse_label

FITUR = list(NAMA_FITUR)
LABELS = ["Aman", "Waspada", "Berisiko"]

df = pd.read_csv("Modul_2A/dataset_status_akademik.csv")
train = df[df["bagian"] == "train"]
test = df[df["bagian"] == "test"]
val = train.groupby("status").sample(10, random_state=7)
pool = train.drop(val.index)

# Prompts
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

contoh = pool.groupby("status").sample(2, random_state=1)
few_shot_examples = [{"data": b[FITUR].to_dict(), "label": b["status"]} for _, b in contoh.iterrows()]

median = train.groupby("status")[["ipk", "kehadiran", "jam_belajar", "tugas_terkumpul", "nilai_uts"]].median()
profil = "\n".join(
    f"- {s}: IPK {r.ipk:.2f}, kehadiran {r.kehadiran:.0f}%, jam belajar {r.jam_belajar:.0f}, "
    f"tugas {r.tugas_terkumpul:.0f}%, UTS {r.nilai_uts:.0f}"
    for s, r in median.loc[LABELS].iterrows()
)
PROMPT_V3 = (
    PROMPT_DASAR
    + "\n\nNilai tengah (median) setiap kelas dari data historis:\n" + profil
    + "\nCatatan: kehadiran di bawah 75% sangat menurunkan status."
)

PROMPT_V4 = (
    PROMPT_DASAR
    + "\n\nPanduan Batas Status Akademik:"
    + "\n- Aman: IPK >= 3.20, kehadiran >= 80%, tugas >= 80%, UTS >= 70."
    + "\n- Berisiko: IPK < 2.75 ATAU kehadiran < 75% ATAU tugas < 60% ATAU UTS < 50."
    + "\n- Waspada: Mahasiswa yang berada di antara Aman dan Berisiko (performa marginal / inkonsisten)."
    + "\nCatatan Prioritas: Kehadiran < 75% otomatis membuat status Berisiko."
)

def get_configs(model_name):
    cfg_v1 = {
        "model": model_name, "temperature": 0, "max_tokens": 5,
        "labels": LABELS, "system_prompt": PROMPT_DASAR, "few_shot": []
    }
    cfg_v2 = dict(cfg_v1)
    cfg_v2["few_shot"] = few_shot_examples

    cfg_v3 = dict(cfg_v2)
    cfg_v3["system_prompt"] = PROMPT_V3

    cfg_v4 = dict(cfg_v2)
    cfg_v4["system_prompt"] = PROMPT_V4

    return {"v1": cfg_v1, "v2": cfg_v2, "v3": cfg_v3, "v4": cfg_v4}

def run_eval(client, cfg, data, max_workers=10):
    t0 = time.time()
    def call_api(row):
        msgs = build_messages(cfg, row[FITUR].to_dict())
        for attempt in range(4):
            try:
                res = client.chat.completions.create(
                    model=cfg["model"],
                    temperature=cfg["temperature"],
                    max_tokens=cfg["max_tokens"],
                    messages=msgs
                )
                return parse_label(res.choices[0].message.content, cfg["labels"])
            except Exception as e:
                time.sleep(2 * (attempt + 1))
        return "invalid"

    rows = [r for _, r in data.iterrows()]
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        preds = list(ex.map(call_api, rows))

    dur = time.time() - t0
    y_true = data["status"].tolist()
    acc = accuracy_score(y_true, preds)
    f1 = f1_score(y_true, preds, labels=LABELS, average="macro", zero_division=0)
    cm = confusion_matrix(y_true, preds, labels=LABELS).tolist()
    report = classification_report(y_true, preds, labels=LABELS, zero_division=0, output_dict=True)
    
    return {
        "accuracy": round(acc, 4),
        "f1_macro": round(f1, 4),
        "invalid": preds.count("invalid"),
        "n": len(data),
        "duration_sec": round(dur, 2),
        "avg_latency_ms": round((dur / len(data)) * 1000, 1),
        "confusion_matrix": cm,
        "report": report,
        "predictions": preds
    }

def main():
    results = {}

    # Service 1: ai-practicum
    print("=== EVALUATING AI SERVICE 1 (ai-practicum) ===")
    load_dotenv("Modul_2A/.env")
    client1 = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
    cfgs1 = get_configs("ai-practicum")

    val_res1 = {}
    for ver in ["v1", "v2", "v3", "v4"]:
        print(f"Running Validation {ver}...")
        r = run_eval(client1, cfgs1[ver], val, max_workers=10)
        val_res1[ver] = r
        print(f"Val {ver}: Acc={r['accuracy']}, F1={r['f1_macro']}, Dur={r['duration_sec']}s")

    # Pick best among v1, v2, v3
    best_ver1 = max(["v1", "v2", "v3"], key=lambda k: val_res1[k]["f1_macro"])
    print(f"Best prompt among v1-v3: {best_ver1} (F1={val_res1[best_ver1]['f1_macro']})")
    print(f"Iterasi 4 prompt (v4): F1={val_res1['v4']['f1_macro']}")

    print("Running Test Evaluation for Service 1...")
    test_res1 = run_eval(client1, cfgs1[best_ver1], test, max_workers=10)
    print(f"Test S1: Acc={test_res1['accuracy']}, F1={test_res1['f1_macro']}, Invalid={test_res1['invalid']}, Dur={test_res1['duration_sec']}s")

    # Save config.json and hasil_evaluasi_test.csv in Modul_2A
    cfg_final1 = dict(cfgs1[best_ver1])
    cfg_final1["evaluasi"] = {
        "accuracy": test_res1["accuracy"],
        "f1_macro": test_res1["f1_macro"],
        "invalid": test_res1["invalid"],
        "n": test_res1["n"],
        "dataset": "dataset_status_akademik.csv (bagian test)",
        "tanggal": date.today().isoformat()
    }
    with open("Modul_2A/config.json", "w", encoding="utf-8") as f:
        json.dump(cfg_final1, f, indent=2, ensure_ascii=False)
    test.assign(prediksi=test_res1["predictions"]).to_csv("Modul_2A/hasil_evaluasi_test.csv", index=False)

    results["service1"] = {
        "name": "ai-practicum (Gemini 3.8 Flash)",
        "validation": {k: {m: v[m] for m in ["accuracy", "f1_macro", "invalid", "duration_sec"]} for k, v in val_res1.items()},
        "best_ver": best_ver1,
        "test": test_res1
    }

    # Service 2: OpenAI GPT-4o-mini
    print("\n=== EVALUATING AI SERVICE 2 (sm/gpt-4o-mini) ===")
    client2 = OpenAI(api_key="sk-b7f268f48d288357-tsbfva-9a27dac2", base_url="https://rutaau4.abc-tunnel.us/v1")
    cfgs2 = get_configs("sm/gpt-4o-mini")

    val_res2 = {}
    for ver in ["v1", "v2", "v3", "v4"]:
        print(f"Running Validation {ver}...")
        r = run_eval(client2, cfgs2[ver], val, max_workers=10)
        val_res2[ver] = r
        print(f"Val {ver}: Acc={r['accuracy']}, F1={r['f1_macro']}, Dur={r['duration_sec']}s")

    best_ver2 = max(["v1", "v2", "v3"], key=lambda k: val_res2[k]["f1_macro"])
    print(f"Best prompt among v1-v3: {best_ver2} (F1={val_res2[best_ver2]['f1_macro']})")
    print(f"Iterasi 4 prompt (v4): F1={val_res2['v4']['f1_macro']}")

    print("Running Test Evaluation for Service 2...")
    test_res2 = run_eval(client2, cfgs2[best_ver2], test, max_workers=10)
    print(f"Test S2: Acc={test_res2['accuracy']}, F1={test_res2['f1_macro']}, Invalid={test_res2['invalid']}, Dur={test_res2['duration_sec']}s")

    cfg_final2 = dict(cfgs2[best_ver2])
    cfg_final2["evaluasi"] = {
        "accuracy": test_res2["accuracy"],
        "f1_macro": test_res2["f1_macro"],
        "invalid": test_res2["invalid"],
        "n": test_res2["n"],
        "dataset": "dataset_status_akademik.csv (bagian test)",
        "tanggal": date.today().isoformat()
    }
    with open("Modul_2A/config_service2.json", "w", encoding="utf-8") as f:
        json.dump(cfg_final2, f, indent=2, ensure_ascii=False)
    test.assign(prediksi=test_res2["predictions"]).to_csv("Modul_2A/hasil_evaluasi_test_service2.csv", index=False)

    results["service2"] = {
        "name": "OpenAI GPT-4o-mini",
        "validation": {k: {m: v[m] for m in ["accuracy", "f1_macro", "invalid", "duration_sec"]} for k, v in val_res2.items()},
        "best_ver": best_ver2,
        "test": test_res2
    }

    # Save all raw results
    # Remove predictions list to keep json clean or keep it
    with open("all_experiment_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nALL EXPERIMENTS COMPLETED SUCCESSFULLY! Saved to all_experiment_results.json")

if __name__ == "__main__":
    main()
