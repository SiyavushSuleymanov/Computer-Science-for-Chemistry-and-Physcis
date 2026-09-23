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