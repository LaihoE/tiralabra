# Useage

Install dependencies:
```
pip install poetry
poetry install
```
If you have problems/don't want to use poetry, you can install with other ways these:
```bash
pip install bitarray coverage pytest
```



The program can now be run with the command (from root of the project):
```python
poetry run python3 src/file_reader.py src/tests/test.gz
```

### Test your own file

Create a txt file by any means. Then gzip the file like so:
```
gzip my_txt_file.txt
```
Should produce a file like "my_txt_file.txt.gz". This one can be given to the program.