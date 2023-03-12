from bitarray import bitarray
from utils import BitReader

STATIC_HUFFMAN_LITERAL_CODES = ([8]*144 + [9]*112 + [7]*24 + [8]*8)
STATIC_HUFFMAN_DISTANCE_CODES = ([5] * 32)


class Huffman:
    def __init__(self, codelengths):
        self.bits_to_symbol = {}
        max_codelength = max(codelengths) + 1
        next_code = 0

        for codelength in range(1, max_codelength):
            next_code <<= 1
            start_bit = 1 << codelength
            for idx, codelen in enumerate(codelengths):
                if codelen == codelength:
                    self.bits_to_symbol[start_bit + next_code] = idx
                    next_code += 1

    def interpert_next_symbol(self, bitreader):
        # Read bits until we find a match in our dictionary
        bits = 1
        while True:
            bits = bits << 1 | bitreader.read_bit()
            if bits in self.bits_to_symbol:
                return self.bits_to_symbol[bits]

    @staticmethod
    def generate_huffman_trees(bitreader):
        n_literal_codes = bitreader.read_n_bit_int(5) + 257
        n_distcodes = bitreader.read_n_bit_int(5) + 1
        codelen_arr = Huffman.generate_codelen_arr(bitreader)
        
        code_lengths = Huffman(codelen_arr)
        codes = Huffman.generate_codelengths(code_lengths, n_literal_codes, n_distcodes, bitreader)

        literal_codes = Huffman(codes[:n_literal_codes])
        distance_codes = codes[n_literal_codes:]

        # If no distance codes
        if len(distance_codes) == 1 and distance_codes[0] == 0:
            return (distance_codes, None)
        else:
            # If we have distance codes
            dist_codes = Huffman(distance_codes)
            return (dist_codes, literal_codes)

    @staticmethod
    def generate_codelen_arr(bitreader):
        code_len_list = [0] * 19
        # Odd order to fill arr, see: https://www.rfc-editor.org/rfc/rfc1951#page-13
        # Not sure why it is filled in this way
        code_len_codes = bitreader.read_n_bit_int(4)
        code_len_list[16] = bitreader.read_n_bit_int(3)
        code_len_list[17] = bitreader.read_n_bit_int(3)
        code_len_list[18] = bitreader.read_n_bit_int(3)
        code_len_list[0] = bitreader.read_n_bit_int(3)
        j = 0
        for i in range(code_len_codes):
            if i % 2 == 0:
                j = 8 + i // 2
            else:
                j = 7 - i // 2
            code_len_list[j] = bitreader.read_n_bit_int(3)
        return code_len_list

    @staticmethod
    def generate_codelengths(huffman, n_literal_codes, n_distcodes, bitreader):
        codes = []
        while len(codes) < n_literal_codes + n_distcodes:
            symbol = huffman.interpert_next_symbol(bitreader)
            # 0-15 literal
            if symbol <= 15:
                codes.append(symbol)
            # Copy previous code 3-6 times
            if symbol == 16:
                extra_runs = bitreader.read_n_bit_int(2)
                for _ in range(3 + extra_runs):
                    codes.append(codes[-1])
            # Repeat a code len of 0 for 3-10 times
            if symbol == 17:
                extra_runs = bitreader.read_n_bit_int(3)
                for _ in range(3 + extra_runs):
                    codes.append(0)
            # Repeat a code len of 0 for 11-138 times
            if symbol == 18:
                extra_runs = bitreader.read_n_bit_int(7)
                for _ in range(11 + extra_runs):
                    codes.append(0)
        return codes
