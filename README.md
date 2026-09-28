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
