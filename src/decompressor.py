from bitarray import bitarray
from utils import BitReader
from utils import History
from huffman import generate_huffman_trees, Huffman, STATIC_HUFFMAN_LITERAL_CODES, STATIC_HUFFMAN_DISTANCE_CODES


class Decompressor:
    def __init__(self, data):
        bitarr = bitarray(endian='little')
        bitarr.frombytes(data)
        self.bitreader = BitReader(bitarr)
        self.byte_history = History()
        self.decompressed = []
    
    def decompress(self):
        # Read blocks until end of file
        while True:
            is_last = self.bitreader.read_bit()
            block_type = self.bitreader.read_n_bit_int(2)
            print(block_type)
            if block_type == 0:
                self.handle_uncompressed_block()
            elif block_type == 1:
                self.decompress_static_huffman()
            elif block_type == 2:
                self.decompress_huffman_block(None, None)

            if is_last:
                return

    def decompress_static_huffman(self):
        # These are predetermined like this:
        literal_len_codes = Huffman(STATIC_HUFFMAN_LITERAL_CODES)
        distance_len_codes = Huffman(STATIC_HUFFMAN_DISTANCE_CODES)
        self.decompress_huffman_block(distance_len_codes, literal_len_codes)
    
    def handle_uncompressed_block(self):
        length = self.bitreader.read_n_bit_int(16)
        # Can be used to check for correct length
        _ = self.bitreader.read_n_bit_int(16)

        byte_slice = self.bitreader.read_n_bytes(length)
        self.decompressed.append((byte_slice, ))
        self.byte_history.append((byte_slice, ))

    def decompress_huffman_block(self, distance_codes, literal_codes):
        """
        The main loop that we spend most of time doing (other blocks are quite rare)

        Creates 2 huffman trees and then begins decompressing from stream.
        Reads symbols from bitstream until we get the special symbol 256 (END).
        If symbol value < 256 then we use the actual value for the symbol (0-255).
        If symbol >= 256 we look back into our history starting from "distance" 
        indexes ago and continue for "run_length" symbols.

        For example:
        history = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        distance = 6
        run_length = 3
        --> == [4, 5, 6]
        """
        # Create our huffman trees
        if distance_codes == None and literal_codes == None:
            distance_codes, literal_codes = generate_huffman_trees(self.bitreader)
        while True:
            symbol = literal_codes.interpert_next_symbol(self.bitreader)
            # Symbol 256 means end of the block
            if symbol == 256:
                return
            # Literal byte
            if symbol < 256:
                self.decompressed.append(symbol)
                self.byte_history.append(symbol)
            # Look back into history
            elif symbol >= 256:
                # Between 3 and 258
                run_length = self.interpret_run_length(symbol)
                # Between 1 and 32768
                symbol = distance_codes.interpert_next_symbol(self.bitreader)
                distance = self.interpret_distance(symbol)
                # Look back into history
                byte_slice = self.byte_history.slice_history(distance, run_length)
                self.decompressed.extend(byte_slice)


    def interpret_distance(self, symbol):
        """
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
        # This decodes according to the above table
        if symbol < 4:
            return symbol + 1
        else:
            extra_bits = symbol // 2 - 1
            return ((symbol % 2 + 2) << extra_bits) + 1 + self.bitreader.read_n_bit_int(extra_bits)

    def interpret_run_length(self, symbol):
        """        
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
        # This decodes according to the above table
        if symbol == 285:
            return 258
        if symbol < 264:
            return symbol - 254
        else:
            extra_bits = (symbol - 261) // 4
            return (((symbol - 265) % 4 + 4) << extra_bits) + self.bitreader.read_n_bit_int(extra_bits) + 3
