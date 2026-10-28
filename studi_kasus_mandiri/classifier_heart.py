import json
import time

NAMA_FITUR = [
    "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol",
    "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"
]

def load_config(path="config_heart.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def format_data(data):
    return (
        f"Data Pasien:\n"
        f"- Usia (Age): {data['Age']}\n"
        f"- Jenis Kelamin (Sex): {data['Sex']}\n"
        f"- Tipe Nyeri Dada (ChestPainType): {data['ChestPainType']}\n"
        f"- Tekanan Darah Istirahat (RestingBP): {data['RestingBP']} mmHg\n"
        f"- Kolesterol Serum (Cholesterol): {data['Cholesterol']} mg/dl\n"
        f"- Gula Darah Puasa > 120 (FastingBS): {data['FastingBS']}\n"
        f"- Hasil EKG Istirahat (RestingECG): {data['RestingECG']}\n"
        f"- Detak Jantung Maksimum (MaxHR): {data['MaxHR']} bpm\n"
        f"- Nyeri Dada Latihan (ExerciseAngina): {data['ExerciseAngina']}\n"
        f"- Depresi ST Latihan (Oldpeak): {data['Oldpeak']}\n"
        f"- Kemiringan ST Puncak (ST_Slope): {data['ST_Slope']}"
    )

def build_messages(cfg, data_input):
    messages = [{"role": "system", "content": cfg["system_prompt"]}]
    for fs in cfg.get("few_shot", []):
        messages.append({"role": "user", "content": format_data(fs["data"])})
        messages.append({"role": "assistant", "content": fs["label"]})
    messages.append({"role": "user", "content": format_data(data_input)})
    return messages

def parse_label(raw_text, labels):
    clean = raw_text.strip().lower()
    for lbl in labels:
        if lbl.lower() in clean:
            return lbl
    # Fallback keyword checks
    if "jantung" in clean or "sakit" in clean or "disease" in clean:
        return "Penyakit Jantung"
    if "normal" in clean or "sehat" in clean:
        return "Normal"
    return "invalid"

def classify(client, cfg, data_input, max_retry=3):
    messages = build_messages(cfg, data_input)
    for trial in range(max_retry):
        try:
            resp = client.chat.completions.create(
                model=cfg["model"],
                temperature=cfg.get("temperature", 0.0),
                max_tokens=cfg.get("max_tokens", 10),
                messages=messages
            )
            raw = resp.choices[0].message.content
            return parse_label(raw, cfg["labels"])
        except Exception:
            time.sleep(2 * (trial + 1))
    return "invalid"
