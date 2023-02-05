from bitarray import bitarray
from bitarray.util import ba2int

class BitReader:
    def __init__(self, bitarray):
        self.bitarray = bitarray
        self.bit_idx = 0

    def read_bit(self):
        out = self.bitarray[self.bit_idx]
        self.bit_idx += 1
        return out

    def read_n_bit_int(self, n):
        n_bit_int = ba2int(self.bitarray[self.bit_idx : self.bit_idx + n])
        self.bit_idx += n
        return n_bit_int
