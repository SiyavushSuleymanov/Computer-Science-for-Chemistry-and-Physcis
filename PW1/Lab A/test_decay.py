"""
Tests for the decay simulation.

One complete test is given as a model. Add the two tests described in the
lab handout (a negative-rate test, and a test against the analytical law).
Run with:  pytest -v
"""

import numpy as np
import pytest
from decay import simulate, simulate_loop


def test_starts_at_N0():
    # at time zero, no atoms have decayed yet
    assert simulate(1000, 0.4)[0] == 1000

def test_negative_rate():
    with pytest.raises(ValueError):
        simulate(1000, -0.4)

def test_average_decay():
    N0 = 1000
    lam = 0.4

    results = []

    for seed in range(100):
        counts = simulate(N0, lam, dt=0.01, steps=100, seed=seed)
        results.append(counts[-1])

    average = sum(results) / len(results)

    expected = N0 * np.exp(-lam)

    assert average == pytest.approx(expected, rel=0.03)
