## Test document

Using typical unit tests for testing and will add some end to end test when deflate is done.

The tricky part is to test the parser one part at a time. To make this easier I keep track of the current bit index so that the parser can be quickly set to a specific place in the parsing. 


## Run tests:

Install dep:
```
pip install poetry
poetry install
```

Run tests and get test coverage (from root dir):
```
poetry run pytest
```

Current coverage (12.2):
|      file       | coverage |
| :-------------: | :------: |
|  bitreader.py   |   77%    |
| decompressor.py |   86%    |
| file_reader.py  |   83%    |
(some parts are still under construction thats why quite low %)
