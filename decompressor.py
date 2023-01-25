from bitstream import BitStream


class Decompress:
    def __init__(self, bytes_input):
        self.bitstream = BitStream(bytes_input)
    


z = 69
x = z.to_bytes(4, "little")
d = Decompress(x)