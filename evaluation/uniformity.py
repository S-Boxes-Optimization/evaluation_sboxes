import numpy as np
from numba import jit

from sboxes import SBox

@jit(nopython=True)
def ddt(table: list[int], input_size: int, output_size: int):
    ddt = np.zeros((1 << input_size, 1 << output_size), dtype=np.uint32)

    for dx in range(1 << input_size):
        for x in range(1 << input_size):
            x_prime = x ^ dx
            assert table[x] < 1 << output_size
            assert table[x_prime] < 1 << output_size
            dy = table[x] ^ table[x_prime]
            ddt[dx][dy] += 1

    return ddt


@jit(nopython=True)
def get_ddt(sbox: SBox) -> np.ndarray:
    return ddt(sbox.table, sbox.output_size, sbox.input_size)