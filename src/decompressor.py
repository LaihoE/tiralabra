from bitarray import bitarray
from src.bitreader import BitReader


class Huffman:
    def __init__(self, codelengths):
        # Create codes that are made in a way that no key can be
        # a sub-key of another ie. this is impossible:
        # key1 = 000111   key2 = 0001

        self.bits_to_symbol = {}
        max_codelength = max(codelengths) + 1
        nextcode = 0

        for codelength in range(1, max_codelength):
            nextcode <<= 1
            startbit = 1 << codelength
            for idx, codelen in enumerate(codelengths):
                if codelen == codelength:
                    self.bits_to_symbol[startbit + nextcode] = idx
                    nextcode += 1

    def interpert_next_symbol(self, bitreader):
        # Read bits until we find a match in our dictionary
        bits = 1
        while True:
            bits = bits << 1 | bitreader.read_bit()
            if bits in self.bits_to_symbol:
                return self.bits_to_symbol[bits]


class Decompressor:
    def __init__(self, data):
        bitarr = bitarray(endian='little')
        bitarr.frombytes(data)
        self.bitreader = BitReader(bitarr)

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

    def generate_codelengths(self, huffman, n_literal_codes, n_distcodes):
        codes = []
        while len(codes) < n_literal_codes + n_distcodes:
            symbol = huffman.interpert_next_symbol(self.bitreader)
            # 0-15 literal
            if symbol <= 15:
                codes.append(symbol)
            # Copy previous code 3-6 times
            if symbol == 16:
                extra_runs = self.bitreader.read_n_bit_int(2)
                for _ in range(3 + extra_runs):
                    codes.append(codes[-1])
            # Repeat a code len of 0 for 3-10 times
            if symbol == 17:
                extra_runs = self.bitreader.read_n_bit_int(3)
                for _ in range(3 + extra_runs):
                    codes.append(0)
            # Repeat a code len of 0 for 11-138 times
            if symbol == 18:
                extra_runs = self.bitreader.read_n_bit_int(7)
                for _ in range(3 + extra_runs):
                    codes.append(0)
        return codes

    def decode_huffman_tree(self):
        n_literal_codes = self.bitreader.read_n_bit_int(5) + 257
        n_distcodes = self.bitreader.read_n_bit_int(5) + 1
        codelen_arr = self.generate_codelen_arr()
        huffman = Huffman(codelen_arr)
        codes = self.generate_codelengths(huffman, n_literal_codes, n_distcodes)

    def decompress(self):
        is_last = self.bitreader.read_bit()
        block_type = self.bitreader.read_n_bit_int(2)

        if block_type == 2:
            self.decode_huffman_tree()
