
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