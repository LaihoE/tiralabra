# Implementation
The implementation is optimized for readability and so all unnecessary stuff is taken out. This also means some error handling is left out. I did this because I wanted to focus on learning how the deflate algorithm works and not put too much time into handling edge cases. 


On a high level deflate works something like this:
```python
decompressed_data = []

While not end:
    huffman = create_huffman_tree()
    while block not ended:
        symbol = read_bits_until_match(huffman)
        if symbol == special:
            byte_slice = look_back_n_bytes(offset, n_bytes)
            decompressed.extend(byte_slice)
        else:
            decompressed.append(symbol)
```

So for each block we create a tree and then just read bits until we find a match in the tree.



### Files:


**Huffman**
Class for creating huffman trees that are used in the decompression.

**file_reader**
Takes care of the IO and parses the header. Passes the decompressor all the data it needs.

**decompressor**
This is where the main deflate algorithm is. This includes the main loop of the file.

**utils**
- Bitreader
is just an abstraction over the bytes that lets us easily manipulate bits. This uses the Bitarray library under the hood. This allows us to read individual bits without having to worry about where in the byte we are etc.
- History
Keeps track of bytes decompressed so far. It's a circular buffer data structure.


# Performance
Since the parser is written in Python it is difficult to get reasonable performance compared to lower level languages. I compared this implementation against gzip tool and the difference is quite big:

| gzip      | This       |
| --------- | ---------- |
| 9 seconds | 8min 23sec |

