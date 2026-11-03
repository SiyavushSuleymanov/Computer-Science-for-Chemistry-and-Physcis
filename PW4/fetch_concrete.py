"""A1: Download once; later analyses read the local CSV."""
from pathlib import Path
import json
from ucimlrepo import fetch_ucirepo

data = Path("data")
data.mkdir(exist_ok=True)
concrete = fetch_ucirepo(id=165)
print(concrete.metadata)
print(concrete.variables.to_string(index=False))

names = ["cement", "slag", "ash", "water", "superplastic",
         "coarse_agg", "fine_agg", "age"]
X = concrete.data.features.copy()
if X.shape[1] != len(names) or concrete.data.targets.shape[1] != 1:
    raise ValueError("Unexpected UCI schema: check the variable order.")
mapping = concrete.variables.copy()
print("Original feature names -> local names:")
print(dict(zip(X.columns, names)))
X.columns = names
y = concrete.data.targets.iloc[:, 0].rename("strength")
X.assign(strength=y).to_csv(data / "concrete.csv", index=False)
mapping.to_csv(data / "concrete_variables.csv", index=False)
(data / "concrete_metadata.json").write_text(
    json.dumps(concrete.metadata, indent=2, default=str), encoding="utf-8")
print("Saved data/concrete.csv")
