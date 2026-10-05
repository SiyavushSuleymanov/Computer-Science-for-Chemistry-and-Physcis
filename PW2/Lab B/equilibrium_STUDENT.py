"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

def k_imbalance(x):
    return (2*x)**2 / ((1-x)*(1-x)) - K

x_newton = newton(k_imbalance, x0=0.5) #without fprime, it supplies derivative itself
print("Newton equilibrium extent =", x_newton)

result = minimize(lambda x: k_imbalance(x[0])**2, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)])

x_slsqp = result.x[0]
print("SLSQP equilibrium extent =", x_slsqp)

x_eq = x_slsqp

H2_eq = a - x_eq
I2_eq = b - x_eq
HI_eq = 2 * x_eq

print("H2 at equilibrium =", H2_eq)
print("I2 at equilibrium =", I2_eq)
print("HI at equilibrium =", HI_eq)

x_values = np.linspace(0, 0.999, 300)

H2 = a - x_values
I2 = b - x_values
HI = 2 * x_values

plt.plot(x_values, H2, label="H2")
plt.plot(x_values, I2, label="I2")
plt.plot(x_values, HI, label="HI")

plt.axvline(x_eq, linestyle="--", label="Equilibrium")

plt.xlabel("Reaction extent x")
plt.ylabel("Amount (mol)")
plt.title("Chemical equilibrium")
plt.legend()

plt.tight_layout()
plt.savefig("equilibrium.png")