import json
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("default")
plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

with open("evaluasi_summary.json") as f:
    data = json.load(f)["metrics"]

rf_metrics = data["Random Forest (Library)"]
llm_metrics = data["LLM Service (ai-practicum)"]
labels = ["Normal", "Penyakit Jantung"]

# 1. Confusion Matrices Comparison using pure Matplotlib
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
cm_rf = np.array(rf_metrics["confusion_matrix"])
cm_llm = np.array(llm_metrics["confusion_matrix"])

for ax, cm, title, cmap_name in [
    (axes[0], cm_rf, f"Random Forest (Library)\nAccuracy: {rf_metrics['accuracy']:.1%} | F1: {rf_metrics['f1_macro']:.3f}", "Blues"),
    (axes[1], cm_llm, f"LLM Service (ai-practicum)\nAccuracy: {llm_metrics['accuracy']:.1%} | F1: {llm_metrics['f1_macro']:.3f}", "Greens")
]:
    im = ax.imshow(cm, cmap=cmap_name)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Prediksi Model")
    ax.set_ylabel("Data Aktual")
    
    # Annotate values
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], "d"),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=14, fontweight="bold")

plt.savefig("figures/confusion_matrices_heart.png", dpi=200)
plt.close()
print("Saved figures/confusion_matrices_heart.png")

# 2. Performance Metrics Comparison Bar Chart
fig, ax = plt.subplots(figsize=(8.5, 4.8))
metric_names = ["Akurasi", "Presisi Macro", "Recall Macro", "F1 Macro"]
rf_vals = [rf_metrics["accuracy"], rf_metrics["precision_macro"], rf_metrics["recall_macro"], rf_metrics["f1_macro"]]
llm_vals = [llm_metrics["accuracy"], llm_metrics["precision_macro"], llm_metrics["recall_macro"], llm_metrics["f1_macro"]]

x = np.arange(len(metric_names))
width = 0.35

rects1 = ax.bar(x - width/2, rf_vals, width, label="Random Forest (Library)", color="#2b5c8f")
rects2 = ax.bar(x + width/2, llm_vals, width, label="LLM Service (ai-practicum)", color="#2ca02c")

ax.set_ylabel("Skor (0.0 - 1.0)")
ax.set_title("Perbandingan Metrik Evaluasi: Random Forest vs LLM Service", fontweight="bold", fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(metric_names)
ax.set_ylim(0.7, 1.05)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.legend(loc="lower right")

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=10)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=10)

plt.savefig("figures/metrics_comparison_heart.png", dpi=200)
plt.close()
print("Saved figures/metrics_comparison_heart.png")

# 3. Latency Comparison (Log Scale)
fig, ax = plt.subplots(figsize=(6.5, 4.2))
models = ["Random Forest\n(Library)", "LLM Service\n(ai-practicum)"]
latencies = [rf_metrics["latency_ms"], llm_metrics["latency_ms"]]
colors = ["#2b5c8f", "#e67e22"]

bars = ax.bar(models, latencies, color=colors, width=0.45)
ax.set_yscale("log")
ax.set_ylabel("Latensi Inferensi per Sampel (milidetik, log-scale)")
ax.set_title("Perbandingan Kecepatan Inferensi (Latensi)", fontweight="bold", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.5)

ax.annotate(f"{rf_metrics['latency_ms']:.2f} ms", xy=(0, rf_metrics['latency_ms']),
            xytext=(0, 6), textcoords="offset points", ha="center", va="bottom", fontweight="bold")
ax.annotate(f"{llm_metrics['latency_ms']:.1f} ms\n({llm_metrics['latency_ms']/1000:.2f} s)", xy=(1, llm_metrics['latency_ms']),
            xytext=(0, 6), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

ax.set_ylim(1, 30000)
plt.savefig("figures/latency_comparison_heart.png", dpi=200)
plt.close()
print("Saved figures/latency_comparison_heart.png")
