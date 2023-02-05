# Project definition

This project implements the DEFLATE algorithm in Python. Deflate is one of the most used compression algorihms. Deflate uses a combination of LZ77-algorithm and Huffman trees to compress data. 

The project will most likely just implement a decoder, if time is left then also an encoder (unlikely). The focus of the project is to learn about compression, and so the code will priorite simplicity over performance.

Deflate allows 3 different modes:
- 00: raw
- 01: static huffman
- 10: dynamic huffman

The goal is to support all 3 ways.




##### Goal
The end goal is that the user can uncompress a file like so:
```bash
python3 decoder.py file.gz outfile.txt
```


##### Languages for review
Rust, C, C++, Go, Python ~ in order of most wanted to least :)

##### Study program
bachelor’s in science (TKT)

##### Language
English

### Sources
https://www.ietf.org/rfc/rfc1951.txt  
https://en.wikipedia.org/wiki/Deflate  
https://www.youtube.com/watch?v=oi2lMBBjQ8s