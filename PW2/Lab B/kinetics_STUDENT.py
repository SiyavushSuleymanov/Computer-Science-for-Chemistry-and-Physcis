"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

data = np.loadtxt("kinetics.csv", delimiter=",", skiprows=1)

t = data[:, 0]
C = data[:, 1]
C0 = C[0]


def total_error(k): #takes small intended k as argument
    k = k[0] #this makes k as vector, because .minimize function works in a way that variable can be vector
    C_predicted = C0 * np.exp(-k * t)
    errors = C - C_predicted
    return np.sum(errors**2)


result = minimize(total_error, x0=[0.5], method="SLSQP", bounds=[(0, 5)])

k_fitted = result.x[0]
print("Fitted k =", k_fitted)


C_fitted = C0 * np.exp(-k_fitted * t)
plt.scatter(t, C, label="Measured data")
plt.plot(t, C_fitted, label="Fitted curve")

plt.xlabel("Time")
plt.ylabel("Concentration")
plt.title("First-order reaction fit")
plt.legend()

plt.tight_layout()
plt.savefig("kinetics.png")
