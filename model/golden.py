"""Golden reference models. Tests compare RTL output against these."""

import numpy as np

INT8_MIN, INT8_MAX = -128, 127


def random_int8(shape, rng):
    """Random signed 8-bit matrix (as int64 so math never overflows in Python)."""
    return rng.integers(INT8_MIN, INT8_MAX + 1, size=shape, dtype=np.int64)


def matmul_ref(a, b):
    """C = A @ B with exact integer math. A is (N, K), B is (K, N)."""
    return np.asarray(a, dtype=np.int64) @ np.asarray(b, dtype=np.int64)
