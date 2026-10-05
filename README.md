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