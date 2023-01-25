import numpy

class BitStream:
    """
    Used for reading data one bit at a time.
    """
    def __init__(self, bytes_input):
        self.bytes = bytes_input
        self.buffer = None
        self.byte_idx = 0
        self.bit_idx = 0

    def fill_buffer(self):
        self.buffer = int.from_bytes(self.bytes, "little")

    def fill_one_bit(self):
        if self.byte_idx == len(self.bytes) and self.bit_idx > 7:
            exit("BIT OUT OF RANGE")
        self.buffer

    def read_n_bits(self, n):
        pass
