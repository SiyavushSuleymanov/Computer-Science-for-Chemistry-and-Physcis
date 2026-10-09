import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


df = pd.read_csv("heart.csv")

print("\n========== HEART DATASET ==========\n")

print("Shape:")
print(df.shape)

print("\nFirst rows:")
print(df.head())

continuous_columns = ["age", "chol", "trestbps", "thalach"]

continuous = df[continuous_columns]

print("\nContinuous variables:")
print(continuous.head())

print("\nSummary statistics:")
print(continuous.describe())



fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].hist(df["age"], bins=15)
axes[0, 0].set_title("Age")
axes[0, 0].set_xlabel("Age")
axes[0, 0].set_ylabel("Frequency")

axes[0, 1].hist(df["chol"], bins=15)
axes[0, 1].set_title("Cholesterol")
axes[0, 1].set_xlabel("Cholesterol")
axes[0, 1].set_ylabel("Frequency")

axes[1, 0].hist(df["trestbps"], bins=15)
axes[1, 0].set_title("Resting Blood Pressure")
axes[1, 0].set_xlabel("Resting Blood Pressure")
axes[1, 0].set_ylabel("Frequency")

axes[1, 1].hist(df["thalach"], bins=15)
axes[1, 1].set_title("Maximum Heart Rate")
axes[1, 1].set_xlabel("Maximum Heart Rate")
axes[1, 1].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig("heart_distributions.png")
plt.close()



print("\n========== NORMALITY ==========\n")

normality = {}

for column in continuous_columns:

    values = df[column].dropna()

    statistic, p_value = stats.shapiro(values)

    normal = p_value >= 0.05

    normality[column] = normal

    print(column)
    print(f"Shapiro statistic = {statistic:.4f}")
    print(f"p-value = {p_value:.6f}")

    if normal:
        print("Verdict: approximately normal")
    else:
        print("Verdict: not normally distributed")

    print()


# Q-Q plots

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

for ax, column in zip(axes.flat, continuous_columns):

    stats.probplot(
        df[column].dropna(),
        dist="norm",
        plot=ax
    )

    ax.set_title(f"Q-Q Plot: {column}")

plt.tight_layout()
plt.savefig("heart_qqplots.png")
plt.close()


print("\n========== THALACH GROUP COMPARISON ==========\n")

healthy = df[df["target"] == 0]["thalach"].dropna()
disease = df[df["target"] == 1]["thalach"].dropna()

print("Healthy patients:", len(healthy))
print("Disease patients:", len(disease))


# Check normality of each group

healthy_shapiro = stats.shapiro(healthy)
disease_shapiro = stats.shapiro(disease)

print("\nHealthy thalach normality:")
print(f"p-value = {healthy_shapiro.pvalue:.6f}")

print("\nDisease thalach normality:")
print(f"p-value = {disease_shapiro.pvalue:.6f}")


# At least one group is non-normal in this dataset,
# so use Mann-Whitney U

u_statistic, group_p = stats.mannwhitneyu(
    healthy,
    disease,
    alternative="two-sided"
)

print("\nMethod: Mann-Whitney U test")
print(f"U statistic = {u_statistic:.4f}")
print(f"p-value = {group_p:.6e}")

if group_p < 0.05:
    print("Conclusion: the two groups differ significantly in thalach.")
else:
    print("Conclusion: no significant difference was detected.")



healthy_mean = healthy.mean()
disease_mean = disease.mean()

healthy_se = stats.sem(healthy)
disease_se = stats.sem(disease)

healthy_ci = stats.t.interval(
    0.95,
    df=len(healthy) - 1,
    loc=healthy_mean,
    scale=healthy_se
)

disease_ci = stats.t.interval(
    0.95,
    df=len(disease) - 1,
    loc=disease_mean,
    scale=disease_se
)

print("\nHealthy group:")
print(f"Mean thalach = {healthy_mean:.3f}")
print(f"Standard error = {healthy_se:.3f}")
print(f"95% CI = ({healthy_ci[0]:.3f}, {healthy_ci[1]:.3f})")

print("\nDisease group:")
print(f"Mean thalach = {disease_mean:.3f}")
print(f"Standard error = {disease_se:.3f}")
print(f"95% CI = ({disease_ci[0]:.3f}, {disease_ci[1]:.3f})")


# Plot group means with 95% confidence intervals

means = [healthy_mean, disease_mean]

ci_errors = [
    healthy_mean - healthy_ci[0],
    disease_mean - disease_ci[0]
]

plt.figure(figsize=(7, 5))

plt.errorbar(
    ["Healthy", "Heart disease"],
    means,
    yerr=ci_errors,
    fmt="o",
    capsize=7
)

plt.ylabel("Mean thalach")
plt.title("Maximum Heart Rate with 95% Confidence Intervals")

plt.tight_layout()
plt.savefig("thalach_groups.png")

print("\n========== AGE vs THALACH ==========\n")

# Both variables are non-normal in this dataset,
# so use Spearman correlation

rho, age_thalach_p = stats.spearmanr(
    df["age"],
    df["thalach"]
)

print("Method: Spearman correlation")
print(f"Spearman rho = {rho:.4f}")
print(f"p-value = {age_thalach_p:.6e}")

if rho > 0:
    print("Direction: positive relationship")
elif rho < 0:
    print("Direction: negative relationship")
else:
    print("Direction: no monotonic relationship")


# Scatter plot

plt.figure(figsize=(7, 5))

plt.scatter(
    df["age"],
    df["thalach"],
    alpha=0.7
)

plt.xlabel("Age")
plt.ylabel("Maximum Heart Rate (thalach)")
plt.title("Age vs Maximum Heart Rate")

plt.tight_layout()
plt.savefig("age_thalach.png")
plt.close()


chem = pd.read_csv("chemicals_cancer.csv")

print("\n========== CHEMICAL DATASET ==========\n")

print("Shape:")
print(chem.shape)

print("\nFirst rows:")
print(chem.head())

print("\nSummary:")
print(chem.describe())


print("\n========== NAIVE CHEMICAL ANALYSIS ==========\n")


benzene_r, benzene_p = stats.pearsonr(
    chem["benzene"],
    chem["malignancy"]
)

cadmium_r, cadmium_p = stats.pearsonr(
    chem["cadmium"],
    chem["malignancy"]
)


print("Benzene vs malignancy:")
print(f"Pearson r = {benzene_r:.4f}")
print(f"p-value = {benzene_p:.6e}")

print("\nCadmium vs malignancy:")
print(f"Pearson r = {cadmium_r:.4f}")
print(f"p-value = {cadmium_p:.6e}")


if abs(benzene_r) > abs(cadmium_r):
    print("\nNaive conclusion: benzene appears more strongly associated.")
else:
    print("\nNaive conclusion: cadmium appears more strongly associated.")


# Plot naive relationships

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].scatter(
    chem["benzene"],
    chem["malignancy"],
    alpha=0.5
)

axes[0].set_xlabel("Benzene")
axes[0].set_ylabel("Malignancy")
axes[0].set_title("Benzene vs Malignancy")


axes[1].scatter(
    chem["cadmium"],
    chem["malignancy"],
    alpha=0.5
)

axes[1].set_xlabel("Cadmium")
axes[1].set_ylabel("Malignancy")
axes[1].set_title("Cadmium vs Malignancy")

plt.tight_layout()
plt.savefig("chemical_naive.png")
plt.close()


print("\n========== CONFOUNDING ANALYSIS ==========\n")


# First examine pollution index relationships

pollution_cadmium_r, pollution_cadmium_p = stats.pearsonr(
    chem["pollution_index"],
    chem["cadmium"]
)

pollution_benzene_r, pollution_benzene_p = stats.pearsonr(
    chem["pollution_index"],
    chem["benzene"]
)

pollution_malignancy_r, pollution_malignancy_p = stats.pearsonr(
    chem["pollution_index"],
    chem["malignancy"]
)


print("Pollution index vs cadmium:")
print(f"r = {pollution_cadmium_r:.4f}")

print("\nPollution index vs benzene:")
print(f"r = {pollution_benzene_r:.4f}")

print("\nPollution index vs malignancy:")
print(f"r = {pollution_malignancy_r:.4f}")


# Restrict patients to similar pollution levels

restricted = chem[
    (chem["pollution_index"] > 40)
    &
    (chem["pollution_index"] < 60)
].copy()


print("\nPatients with pollution index between 40 and 60:")
print(len(restricted))


benzene_controlled_r, benzene_controlled_p = stats.pearsonr(
    restricted["benzene"],
    restricted["malignancy"]
)

cadmium_controlled_r, cadmium_controlled_p = stats.pearsonr(
    restricted["cadmium"],
    restricted["malignancy"]
)


print("\nBenzene vs malignancy after controlling pollution:")
print(f"Pearson r = {benzene_controlled_r:.4f}")
print(f"p-value = {benzene_controlled_p:.6e}")

print("\nCadmium vs malignancy after controlling pollution:")
print(f"Pearson r = {cadmium_controlled_r:.4f}")
print(f"p-value = {cadmium_controlled_p:.6e}")


if abs(benzene_controlled_r) > abs(cadmium_controlled_r):
    print(
        "\nAfter controlling for pollution, "
        "benzene has the stronger remaining association."
    )
else:
    print(
        "\nAfter controlling for pollution, "
        "cadmium has the stronger remaining association."
    )


# Plot controlled relationships

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].scatter(
    restricted["benzene"],
    restricted["malignancy"],
    alpha=0.6
)

axes[0].set_xlabel("Benzene")
axes[0].set_ylabel("Malignancy")
axes[0].set_title(
    "Benzene vs Malignancy\nPollution Index 40–60"
)


axes[1].scatter(
    restricted["cadmium"],
    restricted["malignancy"],
    alpha=0.6
)

axes[1].set_xlabel("Cadmium")
axes[1].set_ylabel("Malignancy")
axes[1].set_title(
    "Cadmium vs Malignancy\nPollution Index 40–60"
)

plt.tight_layout()
plt.savefig("chemical_controlled.png")
plt.close()


print("\n========== BONUS: CATEGORY BALANCE ==========\n")

proportions = df["target"].value_counts(normalize=True)

print("Target proportions:")
print(proportions)

entropy = stats.entropy(
    proportions,
    base=2
)

print(f"\nShannon entropy = {entropy:.4f} bits")

if entropy > 0.9:
    print("The target categories are quite balanced.")
elif entropy > 0.6:
    print("The target categories are moderately balanced.")
else:
    print("The target categories are strongly imbalanced.")


print("\n========== PW3 COMPLETE ==========\n")