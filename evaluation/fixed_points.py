import numpy as np
#from numba import jit

from sboxes import SBox

#@jit(nopython=True)
def fixed_ponts(sbox: SBox, square: bool = True, detail: bool = False):
    ans = False
    counter = 0
    if square:
        for i in range(len(sbox.table)):
            print(f"{i} -> {int(sbox.table[i])}")
            if int(sbox.table[i]) == i:
                ans = ans & False
                if not detail:
                    break
                counter += 1
    else:
        return False
    if detail: return ans, counter
    else: return ans

