import numpy as np
from numba import jit

@jit(nopython=True)
def dot(u: int, v: int) -> int:
    c = 0
    x = u & v
    while x > 0:
        x &= x - 1
        c += 1
    return c % 2

@jit(nopython=True)
def fwht_inplace(a: np.ndarray):
    n = a.shape[0]
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2

@jit(nopython=True, fastmath=True)
def evaluate_table(table: np.ndarray, input_size: int) -> float:
    maximum = 0.0
    size = 1 << input_size

    for b in range(1, size):
        h = np.empty(size, dtype=np.float64)
        for x in range(size):
            h[x] = 1.0 - 2.0 * dot(b, table[x])

        fwht_inplace(h)

        current_max = 0.0
        for val in h:
            abs_val = abs(val)
            if abs_val > current_max:
                current_max = abs_val

        if current_max > maximum:
            maximum = current_max

    nonlinearity = (2 ** (input_size - 1)) - (maximum / 2.0)
    return nonlinearity


@jit(nopython=True)
def evaluate(sbox):
    return evaluate_table(sbox.table, sbox.input_size)
