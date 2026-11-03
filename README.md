CSPC - Computer Science for Physics and Chemistry

My coursework repository. Each practical is under PW<n>/Lab <X>/.

Setup

Create the environment for a given lab:

conda env create -f PW1<n>/Lab\ <X>/environment.yml
conda activate cspc

PW1 - Lab A: Reproducible Foundations

What I built:

Created a reproducible Conda environment for the lab.

Implemented and tested radioactive decay simulations using both a pure-Python loop and NumPy.

Speed comparison (loop vs NumPy):

loop: 3.820340 s

numpy: 0.000359 s

speed-up: 10651.70x faster

Tests: all passing? yes

Conclusion:

All three tests passed successfully, including the negative-rate error test and the average-decay test.

The NumPy implementation was much faster than the pure-Python loop because it uses vectorized operations instead of processing atoms one by one in Python.

In this lab, I also practised Conda environments, Git branching and merging, pytest, and performance measurement with time.perf_counter().


## PW1 - Lab B: Data, Plotting, and Automation

**What I did:**
- I read the observed decay data from `decay_observed.csv` and compared it with the analytical decay law.
- I created a figure with the observed data on one side and the analytical curve on the other side.

**Result:**
- The observed data was close to the analytical decay curve, so the simulation and the theoretical result matched quite well.

**Snakemake:**
- I used Snakemake to automate the creation of `figure.png`.
- If the output file is missing or the input changes, Snakemake runs `plot.py` again and rebuilds the figure.

**Conclusion:**
- In this lab I learned how to read data with NumPy, plot results with Matplotlib, and automate a simple workflow using Snakemake.


## PW2 - Lab A: Motion from Tracking Data

**What I did:**
- I used the position data from `freefall.csv` to calculate velocity and acceleration using numerical differentiation.
- Then I integrated the acceleration back to velocity and position and compared the recovered position with the original data.

**Results:**
- In ideal free fall, the acceleration should be about `-9.81 m/s²`, but from the provided data I obtained a mean acceleration of about `-8.5 m/s²`.
- The standard deviation of the acceleration was about `28.7 m/s²`, which shows that the individual acceleration values are very spread out.

**Noise observation:**
- The position values in `freefall.csv` contain measurement noise. For example, the position starts at `500.001 m` and then becomes `500.100 m`, even though the height of a freely falling object should generally decrease.
- When Python calculates the derivative from measured data, it uses finite differences between nearby points. Here, the time difference is `0.1 s`, so even a small error in position can have a much larger effect after dividing the position difference by `0.1`.
- Acceleration requires differentiating again, so the noise is amplified a second time. This is why the acceleration values are much noisier than the original position values.

**Integrating back:**
- I integrated the acceleration to recover velocity and then integrated the recovered velocity to get position again.
- The recovered values are not exactly the same as the original values because the calculations are numerical approximations. In calculus, integration is defined using the limit of increasingly small intervals, while here we only have a finite set of measured data points.
- `cumulative_trapezoid` approximates the area between each pair of points using trapezoids. Even though the acceleration was noisy, after integration the recovered position was still close to the original position.

**Conclusion:**
- This lab showed that differentiation can strongly amplify measurement noise, especially when it is applied more than once.
- Integration has the opposite effect: the positive and negative noise partly cancels while values are accumulated, so the recovered position can still be close to the original data.


## PW2 - Lab B: Optimization in Chemistry

**What I did:**
- I compared three optimization methods: Gradient Descent, Newton's method, and SLSQP.
- I first tested them on a simple convex function, where all three methods found the same minimum at `x = 3`.
- Then I used a harder function with several stationary points. This showed that the result can depend on both the starting point and the optimization method.
- With Gradient Descent using `lr = 0.1`, starting from `x = 0` and `x = 2` both converged to about `x = -1.30`.
- Newton's method starting from `x = 0` converged to a local maximum near `x = 0.17`, while starting from `x = 2` converged to a local minimum near `x = 1.13`.
- SLSQP converged to the lower minimum near `x = -1.30`.

**Reaction rate fitting:**
- I used the first-order reaction model `C(t) = C0 * exp(-k*t)` to fit noisy concentration data.
- I created a total squared error function and used SLSQP to find the value of `k` that minimized this error.
- The fitted rate constant was about `k = 0.25`.
- I plotted the measured concentration data together with the fitted curve in `kinetics.png`.

**Chemical equilibrium:**
- I studied the reaction `H2 + I2 <=> 2HI`, starting with `1 mol` of `H2` and `1 mol` of `I2`.
- I represented the reaction using the extent `x`, where `H2 = 1-x`, `I2 = 1-x`, and `HI = 2x`.
- I solved the equilibrium condition in two ways: Newton root-finding and SLSQP by minimizing the squared imbalance.
- Both methods gave approximately `x = 0.66`.
- This gives equilibrium amounts of about `0.34 mol H2`, `0.34 mol I2`, and `1.32-1.33 mol HI`.
- I plotted how the amounts change with reaction extent and marked the equilibrium point in `equilibrium.png`.

**Conclusion:**
- This lab showed that optimization algorithms can behave differently on functions with several stationary points.
- I learned that Newton's method finds stationary points, so it can converge to either a minimum or a maximum.
- I also learned how optimization can be applied to real chemistry problems, such as fitting a reaction rate constant and finding chemical equilibrium.

## PW3 - Data, Distributions, Testing, and Causation

**What I did:**
- I loaded and analysed the `heart.csv` and `chemicals_cancer.csv` datasets using pandas.
- I studied the distributions of the continuous heart-disease variables and checked whether they were approximately normally distributed.
- I compared maximum heart rate between healthy and heart-disease patients.
- I investigated the relationship between age and maximum heart rate.
- I also analysed the chemical dataset to study the difference between correlation and causation.

**Distributions and normality:**
- I analysed `age`, `chol`, `trestbps`, and `thalach` using histograms, Q-Q plots, and the Shapiro-Wilk test.
- For all four variables, the Shapiro-Wilk test gave `p < 0.05`, so I treated them as not normally distributed.
- The histograms and Q-Q plots were also used to visually check the shapes of the distributions.

**Heart-rate comparison:**
- I separated `thalach` into healthy patients (`target = 0`) and heart-disease patients (`target = 1`).
- Since the data were not normally distributed, I used the Mann-Whitney U test to compare the groups.
- The mean maximum heart rate was about `158.38` for healthy patients and `139.26` for heart-disease patients.
- The test gave a very small p-value (`p ≈ 1.86 × 10^-13`), showing a statistically significant difference between the groups.
- I also calculated the uncertainty of the group means and plotted the means with 95% confidence intervals.

**Age and maximum heart rate:**
- I used Spearman correlation to investigate the relationship between `age` and `thalach`.
- The result was approximately `rho = -0.392`.
- This shows a moderate negative relationship: as age increases, maximum heart rate tends to decrease.

**Chemical exposure analysis:**
- In the first, naive analysis, I calculated the correlations between each chemical and malignancy.
- Benzene had a correlation of about `r = 0.385` with malignancy.
- Cadmium had a much stronger apparent correlation of about `r = 0.880`.
- From this result alone, cadmium appeared to be the more important chemical.

**Confounding and causation:**
- I then investigated `pollution_index` as a possible confounding variable.
- Cadmium was very strongly correlated with pollution index (`r ≈ 0.982`).
- To control for pollution, I restricted the analysis to patients with similar pollution levels (`40 < pollution_index < 60`).
- After controlling for pollution, benzene still had a strong association with malignancy (`r ≈ 0.702`), while cadmium's association dropped to about `r ≈ 0.316`.
- This shows that cadmium initially looked strongly related to malignancy mainly because it was also strongly related to pollution.
- After accounting for the confounding variable, benzene remained the stronger relationship and is the chemical supported by this dataset as the real driver of malignancy.

**Plots created:**
- `heart_distributions.png`
- `heart_qqplots.png`
- `thalach_groups.png`
- `age_thalach.png`
- `chemical_naive.png`
- `chemical_controlled.png`

**Conclusion:**
- This practical showed how the choice of a statistical method depends on the characteristics of the data.
- I learned how to examine distributions, test normality, compare groups, quantify uncertainty, and measure relationships between variables.
- The chemical dataset also showed an important statistical principle: a strong correlation does not automatically imply causation.
- A third variable can create a misleading relationship, so possible confounding variables should be investigated before making causal conclusions.

# PW4 — Supervised and unsupervised machine learning

## Run

Put this directory inside your CSPC repository. Run commands from `PW4/`:

```bash
conda activate cspc
python -m pip install -r requirements.txt
snakemake -n
snakemake --cores 1
```

Or run the scripts manually, in order:

```bash
python fetch_concrete.py
python sessionA.py
python sessionB.py
```

The fetch script needs internet access. Session A then reads the saved CSV;
Session B uses the Wine dataset packaged with scikit-learn. PNG plots and CSV
tables are written into `results/`. No window is required to generate the figures.
Use the same Python environment for installing and running the packages.

## Variables

| Concrete variable | Unit |
| --- | --- |
| cement | kg/m³ |
| slag | kg/m³ |
| ash | kg/m³ |
| water | kg/m³ |
| superplastic | kg/m³ |
| coarse_agg | kg/m³ |
| fine_agg | kg/m³ |
| age | days |
| strength (target) | MPa |

Check the printed original-to-local column mapping against the UCI variables table.

## Model choices and interpretation

KNN K and decision-tree depth are chosen by the highest mean accuracy in five-fold
cross-validation on the training portion, among K>=3 and the listed finite depths.
K=1 is retained as a baseline, but produces only 0/1 probabilities, preventing a
useful threshold comparison. The unlimited tree is also retained as a baseline;
choosing a bounded depth places a limit on how many questions a decision path asks.
These constraints trade possible accuracy for smoother votes and readability;
they do not guarantee better test performance. Scaling is fitted separately inside each
cross-validation fold. Ties use the first listed candidate. The test sweeps are
reported to match the handout; do not use them to retune the models if you want the
held-out estimates to remain independent of those choices. The five extra splits
illustrate sensitivity to splitting; they are overlapping samples, not independent
trials or a formal confidence interval.

The threshold table uses explicit `probability >= threshold` decisions.
The default metrics table uses each estimator's `predict`; at a probability tie of
0.5 a tree's `predict` chooses the first class. A cautious example threshold is 0.7;
examine the actual FP, precision and recall values before arguing for a threshold.
Here an FP accepts a mix below 40 MPa. Higher precision means fewer false approvals
among approved mixes. The false-positive rate is FP/(FP+TN). A higher threshold
can reduce false approvals but rejects more satisfactory mixes and lowers recall.
These classifiers and probabilities are educational models, not certified tests.

For the Wine analysis, `CHOSEN_K = 3` is set before revealing cultivars; justify it
using the elbow and unlabelled PCA plots. All B6 comparisons use k=3 as required,
even if you change B5's chosen k. Agreement is the cluster-majority score defined
in the handout; it is also called purity and is not held-out classification accuracy.
PCA signs may flip across implementations without changing the solution. Interpret
positive and negative sides using the loadings produced by your run.

## Complete your report from the generated results

The assignment asks for explanations in your own words. This file provides a run
guide and reporting checklist, rather than claiming that a personal report is done.

- **A2-A3:** Use `A_missing.csv`, the printed duplicate count, `A_description.csv`
  and `A_strength_scatter.png`. Explain how a repeated row could enter both splits
  and make performance appear better than it is. Discuss scales, trends and sizes.
- **A4:** Include `A_equation.txt`, `A_linear.csv` and `A_linear_residuals.png`.
  Explain what a systematic residual pattern says about a missing relationship.
- **A5:** Include `A_polynomials.csv`; compare training and test errors and feature
  counts. Adjusted R² is not a substitute for held-out performance. Its conventional
  formula needs n > p+1; for collinear expanded features, raw p is not model rank.
- **A6:** Include `A_knn_sweep.csv`, `A_scaling_comparison.csv`, `A_split_scores.csv`,
  `A_split_spread.csv`, `A_tree_sweep.csv`, both accuracy plots and `A_tree_rules.txt`.
  Discuss the selected values in `A_choices.txt`, variability and readability.
- **A7:** Include `A_metrics.csv` and `A_thresholds.csv`. Confusion matrices have
  true classes as rows and predicted classes as columns: [[TN, FP], [FN, TP]].
  Justify the error tradeoff and your threshold.
- **A8:** Include `A_importance.csv` and `A_importance.png`. Rank coefficients by
  absolute magnitude while retaining their signs. Raw coefficients have different
  units; standardised coefficients measure MPa per input standard deviation.
  Importance is association/predictive contribution, not proof of a causal effect.
- **A bonus:** Compare `A_physics_bonus.csv` with the polynomial table.
- **B1-B3:** Use `B_dataset_description.txt`, `B_scales.csv`, `B_PCA_comparison.csv`,
  `B_raw_PC1_loadings.csv`, `B_PCA_variance.csv`, the sorted loading tables,
  `B_scree.png` and `B_PCA_unlabelled.png`. Describe the chemical contrasts,
  components needed for 90% variance and the variance in the first two PCs.
- **B4-B5:** Include `B_initialisations.csv`, `B_elbow.csv`, `B_elbow.png`,
  `B_cluster_sizes.csv`, `B_centres_real_units.csv`, `B_cluster_contrasts.csv`,
  `B_cluster_descriptions.txt` and `B_PCA_clusters.png`. Inertia decreases with k;
  minimising it alone would favour ever more clusters.
- **B6:** Include the three `B_crosstab_*.csv` tables and `B_agreement.csv`.
  Explain why scale and dropping PCs change the chemical information used.
- **B bonus:** Discuss `B_supervised_bonus.csv`. Supervised accuracy uses labels
  during training and evaluates unseen rows; clustering purity uses all wines,
  then their labels to describe cluster composition. These are different evaluations.

## B7 — Perform and document the Snakemake experiment

1. Run `snakemake -n` and record the planned jobs.
2. After confirming you are inside this PW4 directory and these folders contain
   only generated outputs, delete `data/` and `results/`, then run
   `snakemake --cores 1`. Fetch must precede A; B is independent of fetch.
3. Run it again. With up-to-date inputs, there should be no work to do.
4. Edit one hyperparameter in `sessionA.py`, run again, and record the actual
   output: only A should rerun. Its script is an input; fetch and B are unchanged.

`all` tracks the two final CSVs required by the handout. Other tables and PNGs are
side outputs: deleting one of those alone does not trigger regeneration. To
regenerate all A or B outputs explicitly:

```bash
snakemake --cores 1 --forcerun session_a session_b
```

## References

- Yeh, I.-C. (1998). Modeling of strength of high-performance concrete using
  artificial neural networks. Cement and Concrete Research, 28(12), 1797–1808.
  UCI Concrete Compressive Strength dataset, ID 165:
  https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength
- Forina et al., UCI Wine dataset, distributed with scikit-learn:
  https://archive.ics.uci.edu/dataset/109/wine
  See `B_dataset_description.txt` for its full description and original attribution.
