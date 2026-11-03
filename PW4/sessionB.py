"""Wine: B1-B6 and the supervised bonus. Run from PW4/."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

OUT = Path("results")
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"figure.figsize": (8, 5), "figure.dpi": 120})
CHOSEN_K = 3  # Check and justify with the elbow plot, without cultivar labels.


def table(df, name, index=False):
    df.to_csv(OUT / f"{name}.csv", index=index)
    print(f"\n{name}\n{df.to_string(index=index)}")


def figure(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png")
    plt.close()


def kmeans(k, seed=0, n_init=10):
    return KMeans(n_clusters=k, init="k-means++", n_init=n_init,
                  max_iter=300, random_state=seed)


def scatter(scores, name, labels=None):
    plt.figure()
    points = plt.scatter(scores[:, 0], scores[:, 1], c="steelblue" if labels is None else labels,
                         cmap=None if labels is None else "viridis", s=35, alpha=.8)
    plt.xlabel("PC1 score")
    plt.ylabel("PC2 score")
    if labels is not None:
        plt.legend(*points.legend_elements(), title="Cluster")
    figure(name)


# B1: Cultivar labels are not accessed until B6.
wine = load_wine(as_frame=True)
X = wine.data
print(wine.DESCR)
(OUT / "B_dataset_description.txt").write_text(wine.DESCR, encoding="utf-8")
table(X.describe(), "B_description", index=True)
table(pd.DataFrame({"range": X.max()-X.min(), "std": X.std()})
      .sort_values("std", ascending=False), "B_scales", index=True)

# B2: Raw PCA centres, but does not standardise, its inputs.
pca_raw = PCA().fit(X)
raw_loadings = pd.Series(pca_raw.components_[0], index=X.columns, name="PC1")
table(raw_loadings.reindex(raw_loadings.abs().sort_values(ascending=False).index).to_frame(),
      "B_raw_PC1_loadings", index=True)
print("Raw PC1 explained variance:", pca_raw.explained_variance_ratio_[0])

# B3: Fit all unsupervised transformations without looking at cultivars.
scaler = StandardScaler()
Z = scaler.fit_transform(X)
table(pd.DataFrame({"mean": Z.mean(axis=0), "std_ddof0": Z.std(axis=0)}, index=X.columns),
      "B_scaling_check", index=True)
pca = PCA().fit(Z)
scores = pca.transform(Z)
ratios = pca.explained_variance_ratio_
cumulative = np.cumsum(ratios)
variance = pd.DataFrame({"component": np.arange(1, len(ratios)+1),
                         "variance_ratio": ratios, "cumulative": cumulative})
table(variance, "B_PCA_variance")
table(pd.DataFrame({"data": ["raw", "scaled"],
                     "PC1_variance": [pca_raw.explained_variance_ratio_[0], ratios[0]],
                     "PC1_PC2_variance": [pca_raw.explained_variance_ratio_[:2].sum(), ratios[:2].sum()]}),
      "B_PCA_comparison")
print("Components for 90% variance:", np.searchsorted(cumulative, .9)+1)
print("Variance in PC1-PC2:", cumulative[1])
plt.figure()
plt.bar(variance.component, ratios, label="Individual")
plt.plot(variance.component, cumulative, "o-", label="Cumulative")
plt.axhline(.9, color="red", linestyle="--", label="90%")
plt.xticks(variance.component)
plt.xlabel("Principal component")
plt.ylabel("Fraction of variance")
plt.legend()
figure("B_scree")
loadings = pd.DataFrame(pca.components_[:2].T, index=X.columns, columns=["PC1", "PC2"])
for pc in loadings:
    table(loadings.sort_values(pc, ascending=False), f"B_loadings_sorted_{pc}", index=True)
scatter(scores, "B_PCA_unlabelled")

# B4: Compare initialisations and the elbow curve.
table(pd.DataFrame([{"seed": seed, "inertia": kmeans(3, seed, 1).fit(Z).inertia_}
                    for seed in range(8)]), "B_initialisations")
elbow = pd.DataFrame([{"k": k, "inertia": kmeans(k).fit(Z).inertia_} for k in range(1, 11)])
table(elbow, "B_elbow")
plt.figure()
plt.plot(elbow.k, elbow.inertia, "o-")
plt.xticks(elbow.k)
plt.xlabel("Number of clusters k")
plt.ylabel("Inertia (scaled feature space)")
figure("B_elbow")

# B5: Interpret the chosen clusters in original measurement units.
km = kmeans(CHOSEN_K).fit(Z)
table(pd.DataFrame({"cluster": range(CHOSEN_K), "size": np.bincount(km.labels_, minlength=CHOSEN_K)}),
      "B_cluster_sizes")
centres = pd.DataFrame(scaler.inverse_transform(km.cluster_centers_), columns=X.columns)
centres.index.name = "cluster"
table(centres, "B_centres_real_units", index=True)
contrast = pd.Series(np.ptp(km.cluster_centers_, axis=0), index=X.columns).sort_values(ascending=False)
table(contrast.rename("centre_range_in_SD").to_frame(), "B_cluster_contrasts", index=True)
top = contrast.index[:3]
descriptions = []
for cluster in range(CHOSEN_K):
    parts = [f"{feature}={centres.loc[cluster, feature]:.3g} "
             f"({'above' if km.cluster_centers_[cluster, X.columns.get_loc(feature)] > 0 else 'below'} overall mean)"
             for feature in top]
    descriptions.append(f"Cluster {cluster}: " + ", ".join(parts) + ".")
print("\n".join(descriptions))
(OUT / "B_cluster_descriptions.txt").write_text("\n".join(descriptions), encoding="utf-8")
scatter(scores, "B_PCA_clusters", km.labels_)

# B6: Reveal the labels only now. Compare all three versions at k=3.
cultivar = wine.target
rows = []
for name, values in {"scaled": Z, "raw": X, "scaled_PC1_PC2": scores[:, :2]}.items():
    labels = kmeans(3).fit_predict(values)
    counts = pd.crosstab(cultivar.rename("cultivar"), pd.Series(labels, name="cluster"))
    table(counts, f"B_crosstab_{name}", index=True)
    rows.append({"version": name, "agreement": counts.max(axis=0).sum()/len(cultivar)})
agreement = pd.DataFrame(rows)

# Bonus: Scaler and PCA learn from the training rows only.
X_train, X_test, y_train, y_test = train_test_split(
    X, cultivar, test_size=.25, random_state=42, stratify=cultivar)
models = {"Scaled KNN": make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
          "Scaled PCA(2) KNN": make_pipeline(StandardScaler(), PCA(n_components=2),
                                               KNeighborsClassifier(5))}
table(pd.DataFrame([{"model": name, "test_accuracy": model.fit(X_train, y_train).score(X_test, y_test)}
                    for name, model in models.items()]), "B_supervised_bonus")
table(agreement, "B_agreement")  # Write the Snakemake completion target last.
