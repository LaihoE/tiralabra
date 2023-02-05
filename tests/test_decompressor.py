import unittest
from src.file_reader import FileReader
from src.decompressor import Decompressor
from src.decompressor import Huffman

CODELEN_ARR_STARTBIT = 13
LIT_DIST_STARTBIT = 3
SYMBOL_DECODE_STARTBIT = 65
N_LITERAL_CODES = 269
N_DISTCODES = 13


class TestDecompressor(unittest.TestCase):
    def setUp(self):
        file_reader = FileReader("tests/test_text.txt.gz")
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 7, 0, 5, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0,
            0, 0, 7, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 4, 0, 0, 5, 4, 0, 7, 4, 5, 0, 0, 6,
            0, 4, 4, 0, 0, 6, 4, 3, 6, 6, 6, 0, 6, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 6, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0,
            0, 3, 0, 0, 0, 3, 0, 2, 3, 2, 0, 3, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
