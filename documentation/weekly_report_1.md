## Week 1

The first week was spent studying deflate on a high level to be able to understand it enough to plan out the project. Simple implementations seem to be around 300-500 LOC. The project seems like one where it is worth it to spend time upfront, to understand the algorithm, rather than jumping straight into the code.

Time was also spent on setting up the repo and creating the project_definition. Hopefully next week will be spent on writing code.


Below are some ramblings about what ive learned:

Deflate allows 3 different modes:
- 00: raw (no compression)
- 01: static huffman (predefined huffman tree)
- 10: dynamic huffman (we create the huffman tree)
  
We will need the following parts:


- Create Huffman trees
- Decode huffman codes
- Create LZ dictionary
- Bitstream functionality
