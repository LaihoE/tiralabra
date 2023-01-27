from bitstream import BitStream
from enum import Enum
import struct

class BlockType(Enum):
    UNCOMPRESSED = [False, False]
    STATIC_HUFFMAN = [False, True]
    DYNAMIC_HUFFMAN = [True, False]
    # Should not be used
    RESERVED_BLOCK = [True, True]


class Decompressor:
    def __init__(self, data):
        print(data)
        self.bitstream = BitStream(data)
        self.data = data

    def decompress(self):
        is_last = self.bitstream.read(bool, n=1)
        block_type = BlockType(self.bitstream.read(bool, n=2))
