from bitarray import *
from bitarray.util import *
from bitreader import BitReader
from enum import Enum
import struct
import numpy as np


class Decompressor:
    def __init__(self, data):
        ba = bitarray(endian='little')
        ba.frombytes(data)
        self.bitreader = BitReader(ba)

    def generate_codelen_arr(self):
        code_len_list = [0] * 19
        # Odd order to fill arr, see: https://www.rfc-editor.org/rfc/rfc1951#page-13
        # Not sure why it is filled in this way
        code_len_codes = self.bitreader.read_n_bit_int(4)
        code_len_list[16] = self.bitreader.read_n_bit_int(3)
        code_len_list[17] = self.bitreader.read_n_bit_int(3)
        code_len_list[18] = self.bitreader.read_n_bit_int(3)
        code_len_list[0] = self.bitreader.read_n_bit_int(3)

        for i in range(code_len_codes):
            j = (8 + i // 2) if (i % 2 == 0) else (7 - i // 2)
            code_len_list[j] = self.bitreader.read_n_bit_int(3)
        return code_len_list

    def decode_huffman_tree(self):
        print(self.bitreader.bit_idx)
        n_lit_codes = self.bitreader.read_n_bit_int(5) + 257
        n_distcodes = self.bitreader.read_n_bit_int(5) + 1
        cla = self.generate_codelen_arr()


    def decompress(self):
    
        is_last = self.bitreader.read_bit()
        block_type = self.bitreader.read_n_bit_int(2)

        if block_type == 2:
            self.decode_huffman_tree()