import matplotlib.pyplot as plt
import numpy as np
import os
import json
# Set style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

os.makedirs('figures', exist_ok=True)

# 1. Confusion Matrix Comparison Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

labels = ['Aman', 'Waspada', 'Berisiko']

# CM Data
cm_dnn = np.array([
    [65, 9, 0],
    [9, 37, 9],
    [0, 5, 66]
])

cm_s1 = np.array([
    [46, 28, 0],
    [4, 51, 0],
    [0, 46, 25]
])

cm_s2 = np.array([
    [38, 36, 0],
    [8, 42, 5],
    [0, 26, 45]
])

cms = [
    (cm_dnn, "DNN (Modul 1A)\nMLPClassifier (64-32-16)", "Blues"),
    (cm_s1, "LLM Service 1 (Modul 2A)\nai-practicum (Gemini 3.8 Flash)", "Greens"),
    (cm_s2, "LLM Service 2 (Modul 2A Pengganti)\nOpenAI GPT-4o-mini", "Oranges")
]

for ax, (cm, title, cmap) in zip(axes, cms):
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    tick_marks = np.arange(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_ylabel('True Label', fontweight='bold')
    ax.set_xlabel('Predicted Label', fontweight='bold')
    
    # Annotate values
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontweight='bold', fontsize=11)
    ax.grid(False)

plt.tight_layout()
plt.savefig('figures/confusion_matrices_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/confusion_matrices_comparison.png")

# 2. Performance Metrics Comparison Bar Chart
fig, ax = plt.subplots(figsize=(10, 5))

categories = ['Accuracy', 'F1-Macro', 'F1 Aman', 'F1 Waspada', 'F1 Berisiko']
dnn_scores = [0.8400, 0.8269, 0.8784, 0.6981, 0.9041]
s1_scores = [0.6100, 0.6098, 0.7419, 0.5667, 0.5208]
s2_scores = [0.6250, 0.6351, 0.6333, 0.5283, 0.7438]

x = np.arange(len(categories))
width = 0.25

rects1 = ax.bar(x - width, dnn_scores, width, label='DNN (MLPClassifier)', color='#1f77b4', edgecolor='black', alpha=0.9)
rects2 = ax.bar(x, s1_scores, width, label='LLM Service 1 (ai-practicum)', color='#2ca02c', edgecolor='black', alpha=0.9)
rects3 = ax.bar(x + width, s2_scores, width, label='LLM Service 2 (OpenAI GPT-4o-mini)', color='#ff7f0e', edgecolor='black', alpha=0.9)

ax.set_ylabel('Score (0.0 - 1.0)', fontweight='bold')
ax.set_title('Perbandingan Metrik Evaluasi Data Test (200 Sampel)', fontweight='bold', fontsize=12, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontweight='bold', fontsize=10)
ax.set_ylim(0, 1.05)
ax.axhline(0.80, color='red', linestyle='--', linewidth=1, label='Target Gerbang DNN (0.80)')
ax.axhline(0.70, color='purple', linestyle=':', linewidth=1, label='Target Gerbang LLM (0.70)')
ax.legend(loc='lower right', frameon=True, fontsize=9)

# Value labels on bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('figures/metrics_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/metrics_comparison.png")

# 3. Prompt Iteration Validation F1 Trajectory
fig, ax = plt.subplots(figsize=(8.5, 4.5))

iterations = ['Iterasi 1\n(Zero-Shot)', 'Iterasi 2\n(Few-Shot)', 'Iterasi 3\n(Few-Shot + Median)', 'Iterasi 4\n(Refined Rules)']
s1_f1_val = [0.3996, 0.6627, 0.6180, 0.3761]
s2_f1_val = [0.4743, 0.7707, 0.5778, 0.4603]

ax.plot(iterations, s1_f1_val, marker='o', linewidth=2.5, markersize=8, color='#2ca02c', label='LLM S1 (ai-practicum)')
ax.plot(iterations, s2_f1_val, marker='s', linewidth=2.5, markersize=8, color='#ff7f0e', label='LLM S2 (GPT-4o-mini)')

for i, txt in enumerate(s1_f1_val):
    ax.annotate(f'{txt:.4f}', (i, txt), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#2ca02c')

for i, txt in enumerate(s2_f1_val):
    ax.annotate(f'{txt:.4f}', (i, txt), textcoords="offset points", xytext=(0,-15), ha='center', fontweight='bold', color='#ff7f0e')

ax.set_ylabel('F1-Macro Score (Data Validasi N=30)', fontweight='bold')
ax.set_title('Evolusi Skor F1-Macro pada Berbagai Iterasi Prompt', fontweight='bold', fontsize=12, pad=12)
ax.set_ylim(0.25, 0.90)
ax.legend(loc='lower left', frameon=True)
plt.tight_layout()
plt.savefig('figures/prompt_iteration_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/prompt_iteration_comparison.png")

# 4. Latency / Inference Time Comparison (Log scale)
fig, ax = plt.subplots(figsize=(7.5, 4))
models = ['DNN\n(Local CPU)', 'LLM Service 2\n(GPT-4o-mini)', 'LLM Service 1\n(ai-practicum)']
latency_ms = [0.21, 165.7, 1522.8] # ms per sample
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

bars = ax.barh(models, latency_ms, color=colors, edgecolor='black', alpha=0.9, height=0.55)
ax.set_xscale('log')
ax.set_xlabel('Inference Latency per Sample (milidetik, skala logaritmik)', fontweight='bold')
ax.set_title('Perbandingan Latensi Inferensi per Sampel Data Test', fontweight='bold', fontsize=11, pad=10)

for bar in bars:
    w = bar.get_width()
    ax.text(w * 1.2, bar.get_y() + bar.get_height()/2, f'{w:.2f} ms',
            va='center', ha='left', fontweight='bold', fontsize=9)

ax.set_xlim(0.05, 5000)
plt.tight_layout()
plt.savefig('figures/latency_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/latency_comparison.png")
