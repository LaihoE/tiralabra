from dataclasses import dataclass
from decompressor import Decompressor

@dataclass
class Header:
    compression_method: int
    flags: int
    modif_time: int
    extra_flags: int
    os_type: int
    file_name: str


class FileReader:
    def __init__(self, path: str):
        self.__data = open(path, "rb")

    def read_header(self) -> Header:
        """
        Reads header and returns bytes of compressed data.
        """
        # gzip starts with these 2 magic bytes
        assert self.__read_byte() != b'\x1f'
        assert self.__read_byte() != b'\x8b'

        compression_method = self.__read_byte()
        flags = self.__read_byte()
        modif_time = self.__read_i32()
        extra_flags = self.__read_byte()
        os_type = self.__read_byte()
        file_name = ""

        # Just get file name, not so interested in the others
        if flags & 0x04 != 0:
            self.__data.read(self.__read_i16())
        if flags & 0x08 != 0:
            file_name = self.__read_c_string()
        if flags & 0x02 != 0:
            print(f"CRC16: {self.__read_i16()}")
        if flags & 0x10 != 0:
            print(f"comment: {self.__read_c_string()}")

        return Header(compression_method, flags, modif_time, extra_flags, os_type, file_name)

    def get_compressed_block(self):
        return self.__data.read()

    def __read_byte(self):
        return self.__data.read(1)[0]

    def __read_i16(self):
        return self.__read_byte() | self.__read_byte() << 8

    def __read_i32(self):
        return self.__read_i16() | self.__read_i16() << 16

    def __read_c_string(self):
        # Read null terminated string
        return ''.join(iter(lambda: self.__data.read(1).decode('ascii'), '\x00'))


if __name__ == "__main__":
    # The DEFLATE rfc is the example file.
    # Found here: https://www.rfc-editor.org/rfc/rfc1951
    f = FileReader("src/tests/test.gz")
    f.read_header()
    d = Decompressor(f.get_compressed_block())
    d.decompress()
    print("File contents:\n", bytes(d.decompressed,))