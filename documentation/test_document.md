## Test document

The project is tested in parts with unit tests and also with some end to end tests. Nothing too interesting here.


## Run tests:

Install dep:
```
pip install poetry
poetry install
```

Run tests and get test coverage (from root dir):
```
poetry run coverage run -m pytest
poetry run coverage html
```

## Coverage:
![](code_cov.png)