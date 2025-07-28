from numba.experimental import jitclass
from numba import uint8, uint64

spec = [
    ("input_size", uint8), # Input size greater than 256 would be crazy
    ("output_size", uint8), # Output size greater than 256 would be crazy
    ("table", uint64[:]),
]

@jitclass(spec)
class SBox:
    input_size: int
    output_size: int
    table: list[int]
    name: str

    def __init__(self, input_size, output_size, table, name):
        self.input_size = input_size
        self.output_size = output_size
        self.table = table
        self.name = name