## Test document

Using typical unit tests for testing and will add some end to end test when deflate is done.

The tricky part is to test the parser one part at a time. To make this easier I keep track of the current bit index so that the parser can be quickly set to a specific place in the parsing. 


## Run tests:

Install dep:
```
pip install pytest coverage
```

Run tests and get test coverage:
```
coverage run -m pytest
coverage html
```

Current coverage:
|      file       | coverage |
| :-------------: | :------: |
|  bitreader.py   |   100%   |
| decompressor.py |   83%    |
| file_reader.py  |   93%    |



## Pylint
If you want to try pylint then install pylint: ```pip install pylint``` and run ```pylint src```. Currently gives 8/10 but with meh warnings atm.