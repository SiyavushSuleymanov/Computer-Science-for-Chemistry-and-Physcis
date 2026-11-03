"""Concrete: A2-A8 and the physics-feature bonus. Run from PW4/."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.inspection import permutation_importance
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             confusion_matrix, accuracy_score, precision_score,
                             recall_score, f1_score)

OUT = Path("results")
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"figure.figsize": (8, 5), "figure.dpi": 120})


def table(df, name, index=False):
    df.to_csv(OUT / f"{name}.csv", index=index)
    print(f"\n{name}\n{df.to_string(index=index)}")


def figure(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png")
    plt.close()


def regression_scores(model, X_train, X_test, y_train, y_test, p):
    train, test = model.predict(X_train), model.predict(X_test)
    r2 = r2_score(y_train, train)
    n = len(y_train)
    return {"features": p, "train_RMSE": np.sqrt(mean_squared_error(y_train, train)),
            "test_RMSE": np.sqrt(mean_squared_error(y_test, test)),
            "test_MAE": mean_absolute_error(y_test, test), "train_R2": r2,
            "train_adjusted_R2": 1 - (1-r2)*(n-1)/(n-p-1) if n > p+1 else np.nan,
            "test_R2": r2_score(y_test, test)}


def classification_scores(y, predicted):
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "accuracy": accuracy_score(y, predicted),
            "precision": precision_score(y, predicted, zero_division=0),
            "recall": recall_score(y, predicted, zero_division=0),
            "F1": f1_score(y, predicted, zero_division=0)}


# A2: Clean complete records before splitting.
df = pd.read_csv("data/concrete.csv")
table(df.isna().sum().rename("missing").to_frame(), "A_missing", index=True)
duplicates = int(df.duplicated().sum())
print("Duplicate rows removed:", duplicates)
df = df.drop_duplicates().reset_index(drop=True)
if df.isna().any().any():
    raise ValueError("Missing data found: choose and document a cleaning policy first.")
X, y = df.drop(columns="strength"), df["strength"]
table(df.describe(), "A_description", index=True)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, col, unit in zip(axes, ["cement", "age"], ["kg/m³", "days"]):
    ax.scatter(X[col], y, s=12, alpha=.5)
    ax.set(xlabel=f"{col} ({unit})", ylabel="Strength (MPa)")
figure("A_strength_scatter")

# A3-A4: The test rows never enter fit().
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
print("Regression train/test sizes:", len(X_train), len(X_test))
linear = LinearRegression().fit(X_train, y_train)
table(pd.DataFrame([regression_scores(linear, X_train, X_test, y_train, y_test,
                                       X.shape[1])]), "A_linear")
equation = f"strength (MPa) = {linear.intercept_:.8g}" + "".join(
    f" {coef:+.8g}*{name}" for name, coef in zip(X.columns, linear.coef_))
print(equation)
(OUT / "A_equation.txt").write_text(
    equation + "\nIngredient inputs: kg/m³; age: days.\n"
    "Ingredient coefficients: MPa/(kg/m³); age coefficient: MPa/day.\n",
    encoding="utf-8")
plt.figure()
plt.scatter(X_test["age"], y_test-linear.predict(X_test), s=18, alpha=.6)
plt.axhline(0, color="black", linewidth=1)
plt.xscale("log")
plt.xlabel("Age (days; logarithmic scale)")
plt.ylabel("True − predicted strength (MPa)")
figure("A_linear_residuals")

# A5: Polynomial powers/products are scaled inside the pipeline.
rows = []
for degree in [1, 2, 3, 4]:
    poly = make_pipeline(PolynomialFeatures(degree, include_bias=False),
                         StandardScaler(), LinearRegression())
    poly.fit(X_train, y_train)
    rows.append({"degree": degree, **regression_scores(
        poly, X_train, X_test, y_train, y_test, poly[0].n_output_features_)})
table(pd.DataFrame(rows), "A_polynomials")

# A6: Select K and depth with training-only cross-validation.
# Test sweeps are still reported as the PW requires; do not tune on them.
y_class = (y >= 40).astype(int)
table(y_class.value_counts(normalize=True).sort_index().rename("proportion").to_frame(),
      "A_class_proportions", index=True)
Xc_train, Xc_test, c_train, c_test = train_test_split(
    X, y_class, test_size=.2, random_state=42, stratify=y_class)
print("Classification train/test sizes:", len(Xc_train), len(Xc_test))
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def make_knn(K, scaled=True):
    model = KNeighborsClassifier(n_neighbors=K)
    return make_pipeline(StandardScaler(), model) if scaled else model


rows = []
for K in [1, 3, 5, 7, 15, 25, 51, 101]:
    model = make_knn(K).fit(Xc_train, c_train)
    rows.append({"K": K, "train_accuracy": model.score(Xc_train, c_train),
                 "test_accuracy": model.score(Xc_test, c_test),
                 "CV_accuracy": cross_val_score(make_knn(K), Xc_train, c_train,
                                                 cv=cv).mean()})
knn_sweep = pd.DataFrame(rows)
table(knn_sweep, "A_knn_sweep")
# Keep K=1 as a baseline. Choose K>=3 so probabilities can be between 0 and 1.
eligible_knn = knn_sweep[knn_sweep.K >= 3]
K = int(eligible_knn.loc[eligible_knn.CV_accuracy.idxmax(), "K"])
knn = make_knn(K).fit(Xc_train, c_train)
plt.figure()
plt.plot(knn_sweep.K, knn_sweep.train_accuracy, "o-", label="Train")
plt.plot(knn_sweep.K, knn_sweep.test_accuracy, "o-", label="Test")
plt.xscale("log")
plt.xlabel("K")
plt.ylabel("Accuracy")
plt.legend()
figure("A_knn_accuracy")
table(pd.DataFrame([{"scaled": scaled, "K": K, "test_accuracy":
                    make_knn(K, scaled).fit(Xc_train, c_train).score(Xc_test, c_test)}
                   for scaled in [True, False]]), "A_scaling_comparison")
rows = []
for seed in range(5):
    a, b, c, d = train_test_split(X, y_class, test_size=.2, random_state=seed,
                                 stratify=y_class)
    rows.append({"seed": seed, "test_accuracy": make_knn(K).fit(a, c).score(b, d)})
split_scores = pd.DataFrame(rows)
table(split_scores, "A_split_scores")
table(split_scores.test_accuracy.agg(["min", "max", "mean", "std"])
      .rename("accuracy").to_frame(), "A_split_spread", index=True)
print("Accuracy range:", split_scores.test_accuracy.max()-split_scores.test_accuracy.min())

rows, trees = [], []
depths = [1, 2, 3, 4, 5, 6, 8, None]
for depth in depths:
    model = DecisionTreeClassifier(criterion="entropy", max_depth=depth,
                                   random_state=0).fit(Xc_train, c_train)
    trees.append(model)
    rows.append({"max_depth": str(depth), "actual_depth": model.get_depth(),
                 "leaves": model.get_n_leaves(),
                 "train_accuracy": model.score(Xc_train, c_train),
                 "test_accuracy": model.score(Xc_test, c_test),
                 "CV_accuracy": cross_val_score(
                     DecisionTreeClassifier(criterion="entropy", max_depth=depth,
                                            random_state=0),
                     Xc_train, c_train, cv=cv).mean()})
tree_sweep = pd.DataFrame(rows)
table(tree_sweep, "A_tree_sweep")
# Keep the unlimited tree as a baseline; select among bounded-depth trees.
chosen = int(tree_sweep.iloc[:-1].CV_accuracy.idxmax())
tree = trees[chosen]
plt.figure()
for col, label in [("train_accuracy", "Train"), ("test_accuracy", "Test")]:
    plt.plot(range(len(depths)), tree_sweep[col], "o-", label=label)
plt.xticks(range(len(depths)), [str(d) for d in depths])
plt.xlabel("Maximum depth (None = unlimited)")
plt.ylabel("Accuracy")
plt.legend()
figure("A_tree_accuracy")
rules = export_text(tree, feature_names=list(X.columns), max_depth=2)
root = f"{X.columns[tree.tree_.feature[0]]} <= {tree.tree_.threshold[0]:.6g}"
print("Chosen K:", K, "Chosen tree depth:", depths[chosen], "Root:", root)
print(rules)
(OUT / "A_tree_rules.txt").write_text(rules, encoding="utf-8")

# A7: Class 1 means suitable; FP means unsafe concrete is accepted.
models = {"KNN": knn, "Tree": tree}
metrics = pd.DataFrame([{"model": name, **classification_scores(c_test, model.predict(Xc_test))}
                        for name, model in models.items()])
proba = knn.predict_proba(Xc_test)[:, 1]
thresholds = pd.DataFrame([{"threshold": t, **classification_scores(c_test, (proba >= t).astype(int))}
                           for t in [.3, .5, .7, .9]])
table(thresholds, "A_thresholds")
print("Illustrative cautious threshold: 0.7; compare FP, precision and recall in A_thresholds.csv.")

# A8: Importance measures use different scales and are not causal effects.
standard = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
importance = pd.DataFrame({"raw_coefficient": linear.coef_,
                            "standardised_coefficient": standard[-1].coef_,
                            "tree_impurity": tree.feature_importances_}, index=X.columns)
for name, model in models.items():
    perm = permutation_importance(model, Xc_test, c_test, scoring="f1",
                                  n_repeats=20, random_state=0)
    importance[f"{name}_permutation_mean"] = perm.importances_mean
    importance[f"{name}_permutation_std"] = perm.importances_std
table(importance, "A_importance", index=True)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, ["standardised_coefficient", "tree_impurity", "KNN_permutation_mean"]):
    importance[col].sort_values().plot.barh(ax=ax)
    ax.set_title(col.replace("_", " "))
    ax.set_xlabel("MPa per input SD" if col == "standardised_coefficient" else
                  "Normalised impurity decrease" if col == "tree_impurity" else "F1 decrease")
figure("A_importance")

# Bonus: Use the same regression split as A3-A5.
rows = []
for ratio in [False, True]:
    a, b = X_train.copy(), X_test.copy()
    for part in [a, b]:
        part["age"] = np.log(part["age"])
        if ratio:
            part["water"] = part["water"] / part[["cement", "slag", "ash"]].sum(axis=1)
    model = LinearRegression().fit(a, y_train)
    rows.append({"features_used": "log(age) + water/binder" if ratio else "log(age)",
                 **regression_scores(model, a, b, y_train, y_test, a.shape[1])})
table(pd.DataFrame(rows), "A_physics_bonus")
(OUT / "A_choices.txt").write_text(
    f"Removed duplicates: {duplicates}\nK: {K}\nMax depth: {depths[chosen]}\n"
    f"Root question: {root}\nSelection maximises training-only 5-fold CV accuracy\n"
    "among K>=3 (non-binary probabilities) and bounded-depth trees (readability).\n"
    "Threshold 0.7 is an illustrative cautious choice, not a safety certification.\n"
    "Interpret the printed tables and plots in your README.\n", encoding="utf-8")
table(metrics, "A_metrics")  # Write the Snakemake completion target last.
