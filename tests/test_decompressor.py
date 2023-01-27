import unittest
from file_reader import FileReader
from decompressor import Decompressor

CODELEN_ARR_STARTBIT = 13
LIT_DIST_STARTBIT = 3

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
        self.assertEqual(self.decompressor.bitreader.read_n_bit_int(5) + 257, 269)
        self.assertEqual(self.decompressor.bitreader.read_n_bit_int(5) + 1, 13)
