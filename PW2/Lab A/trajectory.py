import numpy as np
import matplotlib.pyplot as plt


# Read trajectory.csv
data = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)

t = data[:, 0]
x = data[:, 1]
y = data[:, 2]


# Plot the 2D trajectory
plt.figure()

plt.plot(x, y)

plt.xlabel("x")
plt.ylabel("y")
plt.title("2D Trajectory")

plt.tight_layout()
plt.show()


# Calculate velocity components
vx = np.gradient(x, t)
vy = np.gradient(y, t)


# Calculate total speed
speed = np.sqrt(vx**2 + vy**2)


# Plot speed over time
plt.figure()

plt.plot(t, speed)

plt.xlabel("Time (s)")
plt.ylabel("Speed")
plt.title("Speed Over Time")

plt.tight_layout()
plt.savefig("trajectory.png")