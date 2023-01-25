import unittest
from file_reader import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.file_reader = FileReader("tests/test_text.txt.gz")

    def test_header(self):
        header = self.file_reader.read_header()
        self.assertAlmostEqual(header.compression_method, 8)
        self.assertAlmostEqual(header.flags, 8)
        self.assertAlmostEqual(header.modif_time, 1674663495)
        self.assertAlmostEqual(header.extra_flags, 0)
        self.assertAlmostEqual(header.os_type, 3)
        self.assertAlmostEqual(header.file_name, "test_text.txt")
