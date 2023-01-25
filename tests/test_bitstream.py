import unittest
from bitstream import BitStream

class TestBitSteam(unittest.TestCase):
    def setUp(self):
        pass

    def test_init_correctly(self):
        z = 69
        test_data = z.to_bytes(4, "little")
        bs = BitStream(test_data)
        self.assertEqual(bs.bytes, test_data)


    def test_fill_buffer(self):

        z = 69
        test_data = z.to_bytes(4, "little")
        bs = BitStream(test_data)

        x = bs.fill_buffer()
        self.assertEqual(x, 69)