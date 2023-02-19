from bitarray import bitarray
from bitarray.util import ba2int

MAX_HISTORY_LEN = 32 * 1024

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


class History:
    """
    A circular buffer to keep history efficiently at max length
    and allow wrap-around behavior needed for decompressing.
    Wrap-around example:
    
    buffer = [1, 2, 3, 4]
    dist = 1
    run_length = 4
    >>> [3, 4, 1, 2]
    """
    def __init__(self):
        self.buffer = [0] * MAX_HISTORY_LEN
        self.max_len = len(self.buffer)
        self.index = 0

    def append(self, item):
        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.max_len

    def slice_history(self, distance, run_length):
        byte_slice = []
        index = (self.index - distance) % self.max_len
        for byte_num in range(run_length):
            # Push into history and output list
            self.append(self.buffer[index])
            byte_slice.append(self.buffer[index])
            index = (index + 1) % self.max_len
        return byte_slice
