from bitarray import bitarray
from bitreader import BitReader


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
        self.byte_history = []
        self.decompressed = []

    def decode_huffman_tree(self):
        n_literal_codes = self.bitreader.read_n_bit_int(5) + 257
        n_distcodes = self.bitreader.read_n_bit_int(5) + 1
        codelen_arr = self.generate_codelen_arr()
        
        huffman = Huffman(codelen_arr)
        codes = self.generate_codelengths(huffman, n_literal_codes, n_distcodes)

        literal_codes = Huffman(codes[:n_literal_codes])
        distance_codes = codes[n_literal_codes:]

        # If no distance codes
        if len(distance_codes) == 1 and distance_codes[0] == 0:
            return (distance_codes, None)
        else:
            # If we have distance codes
            dist_codes = Huffman(distance_codes)
            return (dist_codes, literal_codes)


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
                for _ in range(11 + extra_runs):
                    codes.append(0)
        return codes

    def decompress(self):
        is_last = self.bitreader.read_bit()
        block_type = self.bitreader.read_n_bit_int(2)
        if block_type == 2:
            d,l = self.decode_huffman_tree()
            self.decompress_huffman_block(l, d)

    def decompress_huffman_block(self, literal_codes, distance_codes):
        """
        Reads symbols from bitstream until we get the special symbol 256 (END).
        If symbol value < 256 then we use the actual value for the byte (0-255).
        If symbol >= 256 we look back into our history starting from "distance" 
        indexes ago and continue for "run_length" symbols.

        For example:
        history = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        distance = 6
        run_length = 3
        --> == [4, 5, 6]
        """
        while True:
            symbol = literal_codes.interpert_next_symbol(self.bitreader)
            # Symbol 256 means end of the block
            if symbol == 256:
                return
            # Literal byte
            if symbol < 256:
                self.decompressed.append(symbol)
                self.byte_history.append(symbol)
            elif symbol >= 256:
                # Between 3 and 258
                run_length = self.interpret_run_length(symbol)
                # Between 1 and 32768
                symbol = distance_codes.interpert_next_symbol(self.bitreader)
                distance = self.interpret_distance(symbol)
                # Look back into history "distance" amount, until run_length
                start_idx = len(self.byte_history) - distance
                end_idx = start_idx + run_length

                self.decompressed.extend(self.byte_history[start_idx : end_idx])
                self.byte_history.extend(self.byte_history[start_idx : end_idx])

    def interpret_distance(self, symbol):
        """
        Are these tables good here or do they just clutter?

        From https://www.ietf.org/rfc/rfc1951.txt page 11
        Extra           Extra               Extra
        Code Bits Dist  Code Bits   Dist     Code Bits Distance
        ---- ---- ----  ---- ----  ------    ---- ---- --------
        0   0    1     10   4     33-48    20    9   1025-1536
        1   0    2     11   4     49-64    21    9   1537-2048
        2   0    3     12   5     65-96    22   10   2049-3072
        3   0    4     13   5     97-128   23   10   3073-4096
        4   1   5,6    14   6    129-192   24   11   4097-6144
        5   1   7,8    15   6    193-256   25   11   6145-8192
        6   2   9-12   16   7    257-384   26   12  8193-12288
        7   2  13-16   17   7    385-512   27   12 12289-16384
        8   3  17-24   18   8    513-768   28   13 16385-24576
        9   3  25-32   19   8   769-1024   29   13 24577-32768
        """
        if symbol < 4:
            return symbol + 1
        else:
            extra_bits = symbol // 2 - 1
            return ((symbol % 2 + 2) << extra_bits) + 1 + self.bitreader.read_n_bit_int(extra_bits)

    def interpret_run_length(self, symbol):
        """
        Are these tables here good or do they just clutter?
        
        From https://www.ietf.org/rfc/rfc1951.txt page 11
                Extra               Extra               Extra
        Code Bits Length(s) Code Bits Lengths   Code Bits Length(s)
        ---- ---- ------     ---- ---- -------   ---- ---- -------
        257   0     3       267   1   15,16     277   4   67-82
        258   0     4       268   1   17,18     278   4   83-98
        259   0     5       269   2   19-22     279   4   99-114
        260   0     6       270   2   23-26     280   4  115-130
        261   0     7       271   2   27-30     281   5  131-162
        262   0     8       272   2   31-34     282   5  163-194
        263   0     9       273   3   35-42     283   5  195-226
        264   0    10       274   3   43-50     284   5  227-257
        265   1  11,12      275   3   51-58     285   0    258
        266   1  13,14      276   3   59-66
        """
        if symbol == 285:
            return 258
        if symbol < 264:
            return symbol - 254
        else:
            extra_bits = (symbol - 261) // 4
            return (((symbol - 265) % 4 + 4) << extra_bits) + self.bitreader.read_n_bit_int(extra_bits) + 3
