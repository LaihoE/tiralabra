import unittest
from file_reader import FileReader
from decompressor import Decompressor
from decompressor import Huffman

CODELEN_ARR_STARTBIT = 13
LIT_DIST_STARTBIT = 3
SYMBOL_DECODE_STARTBIT = 65
N_LITERAL_CODES = 269
N_DISTCODES = 13


class TestDecompressor(unittest.TestCase):
    def setUp(self):
        file_reader = FileReader("src/tests/test_text.txt.gz")
        _ = file_reader.read_header()
        self.decompressor = Decompressor(file_reader.get_compressed_block())

    def test_codelen_array(self):
        self.decompressor.bitreader.bit_idx = CODELEN_ARR_STARTBIT
        arr = self.decompressor.generate_codelen_arr()
        self.assertEqual(arr, [2, 0, 4, 3, 3, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4])

    def test_lit_and_dist_codes(self):
        self.decompressor.bitreader.bit_idx = CODELEN_ARR_STARTBIT
        self.assertEqual(self.decompressor.bitreader.read_n_bit_int(5) + 257, N_LITERAL_CODES)
        self.assertEqual(self.decompressor.bitreader.read_n_bit_int(5) + 1, N_DISTCODES)

    def test_huffman_creator(self):
        codes = [2, 0, 4, 3, 3, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4]
        h = Huffman(codes)
        self.assertEqual(h.bits_to_symbol, {4: 0, 10: 3, 11: 4, 12: 6, 13: 17, 28: 2, 29: 5, 30: 7, 31: 18})

    def test_decode_symbol(self):
        self.decompressor.bitreader.bit_idx = SYMBOL_DECODE_STARTBIT
        codes = [2, 0, 4, 3, 3, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4]
        h = Huffman(codes)
        self.assertEqual(h.interpert_next_symbol(self.decompressor.bitreader), 17)
        self.assertEqual(h.interpert_next_symbol(self.decompressor.bitreader), 18)
        self.assertEqual(h.interpert_next_symbol(self.decompressor.bitreader), 5)

    def test_dyn_huffman_decode(self):
        self.decompressor.bitreader.bit_idx = SYMBOL_DECODE_STARTBIT
        codes = [2, 0, 4, 3, 3, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4]
        codelens = self.decompressor.generate_codelengths(Huffman(codes), N_LITERAL_CODES, N_DISTCODES)
        # Ehh
        self.assertEqual(codelens,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 6, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 4, 0, 0, 5, 4, 0, 7, 4, 5, 0, 0, 6, 0, 4, 4, 0, 0, 6,
            4, 3, 6, 6, 6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 6, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 3, 0, 0, 0, 3,
            0, 2, 3, 2, 0, 3])

    def test_literal_codes(self):
        self.decompressor.bitreader.bit_idx = LIT_DIST_STARTBIT
        _, literal_codes = self.decompressor.decode_huffman_tree()
        # in > Python3.7 dict order is deterministic
        self.assertEqual(literal_codes.bits_to_symbol, {8: 32, 9: 116, 20: 97, 21: 101, 22: 104, 23: 110, 24: 111,
        25: 115, 52: 46, 53: 100, 54: 105, 55: 257, 56: 258, 114: 73,
        115: 84, 116: 87, 117: 108, 118: 114, 119: 117, 120: 118,
        121: 119, 122: 121, 123: 256, 124: 259, 125: 268, 252: 10,
        253: 44, 254: 77, 255: 103})

    def test_dist_codes(self):
        self.decompressor.bitreader.bit_idx = LIT_DIST_STARTBIT
        dist_codes, _ = self.decompressor.decode_huffman_tree()
        # in > Python3.7 dict order is deterministic
        self.assertEqual(dist_codes.bits_to_symbol, {4: 8, 5: 10, 12: 2, 13: 6, 14: 9, 15: 12})

    def test_huffman_block(self):
        file_reader = FileReader("src/tests/test_text.txt.gz")
        _ = file_reader.read_header()
        self.decompressor = Decompressor(file_reader.get_compressed_block())
        self.decompressor.decompress()
        self.assertEqual(bytes(self.decompressor.decompressed, ),
         b'this is test data. There is nothing interesting here. Move on. What should I write here, dont  \nhave anything interesting to say.')