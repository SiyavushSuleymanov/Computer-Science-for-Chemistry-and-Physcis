"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)
t = data[:, 0] #gives us all rows in column 0 (1)
y = data[:, 1] #gives all rows in column 1 (2)

v = np.gradient(y, t) #get derivation of y for getting v
a = np.gradient(v, t) #get derivcation of v for getting a

print("Mean acceleration:", a.mean()) #difference between derived and actual value is big

print("Standard deviation:", a.std()) #for that difference, standard deviation becomes larget too

v_recovered = cumulative_trapezoid(a, t, initial=0) + v[0]  #integrating backward, v(0) + integration of a
y_recovered = cumulative_trapezoid(v_recovered, t, initial=0) + y[0]

difference = np.abs(y_recovered - y)
print("Largest difference:", difference.max())
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 8))

axes[0].plot(t, y)
axes[0].set_ylabel("Position (m)")
axes[0].set_title("Position")

axes[1].plot(t, v)
axes[1].set_ylabel("Velocity (m/s)")
axes[1].set_title("Velocity")

axes[2].plot(t, a)
axes[2].axhline(-9.81, linestyle="--")
axes[2].set_ylabel("Acceleration (m/s²)")
axes[2].set_xlabel("Time (s)")
axes[2].set_title("Acceleration")

plt.tight_layout()
plt.savefig("motion.png")