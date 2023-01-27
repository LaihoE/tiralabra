from bitarray import *
from bitarray.util import *

from enum import Enum
import struct
import numpy as np


class BitReader:
    def __init__(self, bitarray):
        self.bitarray = bitarray
        self.bit_idx = 0
    
    def read_bit(self):
        out = self.bitarray[self.bit_idx]
        self.bit_idx += 1
        return out
    
    def read_n_bit_int(self, n):
        integer = ba2int(self.bitarray[self.bit_idx : self.bit_idx + n])
        self.bit_idx += n
        return integer