
## Testing

  1. Install all the dev dependencies: `pip install -e .[dev]` (or just look at the dev dependencies in setup.py and install them seperately)
  2. Run the tests:  `pytest`  or `python -m pytest`  (which works depends on how it's setup on your machine)
     1. If you will want to check the test coverage, instead do `coverage run --source regexport -m pytest` or `coverage run --source regexport -m python -m pytest`
  3. (optional) Generate a coverage report:
     1. In the terminal: `coverage report`
     2. As an interactive web page: `coverage html`, then open the file coveralls/index.html 

## Deploying a New Version

### 1. Update the version number

Increment the version number in `setup.py`.  This project uses semantic versioning.

### 2. Build a new source distribution
```
python setup.py sdist
```

### 3. Upload the source distribution to PyPi

*Note*: For this step, you'll need account permissions for the project.

```
twine upload dist/*
```