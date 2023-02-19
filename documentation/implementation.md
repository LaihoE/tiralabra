# Implementation
The implementation is optimized for readability and so all unnecessary stuff is taken out. This also means some error handling is left out. I did this because I wanted to focus on learning how the deflate algorithm works and not put too much time into handling edge cases. 

### Files:

**utils**
- Bitreader
is just an abstraction over the bytes that lets us easily manipulate bits. This uses the Bitarray library under the hood. This allows us to read individual bits without having to worry about where in the byte we are etc.
- History
Keeps track of bytes decompressed so far. It's a circular buffer data structure.

**Huffman**
Class for creating huffman trees that are used in the decompression.

**file_reader**
Takes care of the IO and parses the header. Passes the decompressor all the data it needs.

**decompressor**
This is where the main deflate algorithm is. This includes the main loop of the file.



## Performance

### Big O
I'm not so sure Big O notation is very interesting for this project. The algorithm is obviously linear with respect to how many bytes we are decompressing. Maybe ill look into this slightly more later.. maybe the specific functions can be analysed.

### Space and speed
to be continued