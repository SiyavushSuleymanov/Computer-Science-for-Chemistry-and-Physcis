import time

from decay import simulate_loop, simulate


N0 = 200_000
lam = 0.4
dt = 0.05
steps = 200
seed = 0


start = time.perf_counter()
simulate_loop(N0, lam, dt, steps, seed)
end = time.perf_counter()

loop_time = end - start


start = time.perf_counter()
simulate(N0, lam, dt, steps, seed)
end = time.perf_counter()

numpy_time = end - start


speedup = loop_time / numpy_time


print(f"Pure Python time: {loop_time:.6f} seconds")
print(f"NumPy time:       {numpy_time:.6f} seconds")
print(f"NumPy is {speedup:.2f} times faster")