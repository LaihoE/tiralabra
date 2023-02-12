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
        if n == 0:
            return 0
        n_bit_int = ba2int(self.bitarray[self.bit_idx : self.bit_idx + n])
        self.bit_idx += n
        return n_bit_int

    def read_n_bytes(self, n):
        # bytes need to be aligned ie. cant start in middle of byte
        self.byte_align()
        return self.bitarray[self.bit_idx : self.bit_idx + n * 8]
    
    def byte_align(self):
        while self.bit_idx % 8 != 0:
            self.read_bit()