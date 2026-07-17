from __future__ import annotations

from itertools import product
from typing import Any

import numpy as np


def solve_box_constrained_least_squares(
    matrix: Any,
    target: Any,
    lower_bounds: Any,
    upper_bounds: Any,
) -> np.ndarray:
    """Solve a small bounded least-squares problem by enumerating active bounds."""
    coefficients = np.asarray(matrix, dtype="float64")
    desired = np.asarray(target, dtype="float64")
    lower = np.asarray(lower_bounds, dtype="float64")
    upper = np.asarray(upper_bounds, dtype="float64")
    if coefficients.ndim != 2:
        raise ValueError("least-squares matrix must be two-dimensional")
    variable_count = coefficients.shape[1]
    if desired.shape != (coefficients.shape[0],):
        raise ValueError("least-squares target shape does not match the matrix")
    if lower.shape != (variable_count,) or upper.shape != (variable_count,):
        raise ValueError("least-squares bounds shape does not match the matrix")
    if np.any(lower > upper):
        raise ValueError("least-squares lower bounds must not exceed upper bounds")

    best: np.ndarray | None = None
    best_objective = float("inf")
    tolerance = 1e-12
    # RGBWW feedback has at most four free channels, so 3^4 active sets are cheap.
    for states in product((-1, 0, 1), repeat=variable_count):
        candidate = np.zeros(variable_count, dtype="float64")
        fixed_indices = [index for index, state in enumerate(states) if state != 0]
        free_indices = [index for index, state in enumerate(states) if state == 0]
        for index in fixed_indices:
            candidate[index] = lower[index] if states[index] < 0 else upper[index]

        adjusted_target = desired
        if fixed_indices:
            adjusted_target = desired - coefficients[:, fixed_indices] @ candidate[fixed_indices]
        if free_indices:
            free_solution = np.linalg.lstsq(
                coefficients[:, free_indices],
                adjusted_target,
                rcond=None,
            )[0]
            free_lower = lower[free_indices]
            free_upper = upper[free_indices]
            if np.any(free_solution < free_lower - tolerance) or np.any(
                free_solution > free_upper + tolerance
            ):
                continue
            candidate[free_indices] = np.clip(free_solution, free_lower, free_upper)

        residual = coefficients @ candidate - desired
        objective = float(residual @ residual)
        if objective < best_objective:
            best = candidate
            best_objective = objective

    if best is None:
        raise RuntimeError("bounded least-squares solver did not find a feasible solution")
    return best
