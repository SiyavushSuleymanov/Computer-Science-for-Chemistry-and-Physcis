"""
PW1 Lab B -- read observed decay data and compare it to the analytical law.
Produce a 1x2 figure:  left = observed data,  right = analytical N0*exp(-lam*t),
with SHARED axes so the two shapes are directly comparable.

Complete the TODOs below. Run with:  python plot.py
"""

import numpy as np
import matplotlib.pyplot as plt

LAMBDA = 0.3     # decay constant, given

data = np.loadtxt("decay_observed.csv", delimiter=",", skiprows=1)

t = data[:, 0]
observed = data[:, 1]

N0 = observed[0]
analytical = N0 * np.exp(-LAMBDA * t)


fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)

# Left plot: observed data
axes[0].scatter(t, observed)
axes[0].set_title("Observed Data")
axes[0].set_xlabel("Time")
axes[0].set_ylabel("Count")

# Right plot: analytical law
axes[1].plot(t, analytical)
axes[1].set_title("Analytical Decay")
axes[1].set_xlabel("Time")

plt.tight_layout()

plt.savefig("figure.png")