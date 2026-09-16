import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the filtered target data
y_train = pd.read_csv(os.path.join("dataset", "y_train.csv"))

# Set clean aesthetic plot parameters
plt.figure(figsize=(7, 5))
colors = ['#2ca02c', '#d62728'] # Green for Safe, Red for At-Risk

# Count frequencies
class_counts = y_train.value_counts()
class_counts.plot(kind='bar', color=colors, edgecolor='black', width=0.6)

# Graph annotations
plt.title("InsightED Thesis Figure: Target Student Risk Distribution (Train Split)", fontsize=12, fontweight='bold', pad=15)
plt.xlabel("Student Performance Category Class Labels", fontsize=10, labelpad=10)
plt.ylabel("Number of Student Records", fontsize=10)
plt.xticks(ticks=[0, 1], labels=["Safe Performance (G3 >= 10)", "At-Risk of Academic Failure (G3 < 10)"], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add counts value labels directly above bars
for i, count in enumerate(class_counts):
    plt.text(i, count + 5, f"n = {count}", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()

# Save image file directly to workspace directory for report document reference
plot_path = os.path.join("models", "target_distribution_chart.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"📈 Chart successfully generated and saved to: '{plot_path}'! Open it to inspect your class imbalance profile.")