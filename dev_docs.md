
## Testing

  1. Install all the dev dependencies: `pip install -e .[dev]` (or just look at the dev dependencies in setup.py and install them seperately)
  2. Run the tests:  `pytest`  or `python -m pytest`  (which works depends on how it's setup on your machine)
     1. If you will want to check the test coverage, instead do `coverage run --source regexport -m pytest` or `coverage run --source regexport -m python -m pytest`
  3. (optional) Generate a coverage report:
     1. In the terminal: `coverage report`
     2. As an interactive web page: `coverage html`, then open the file coveralls/index.html 

## Deploying a New Version

### Commit a new screenshot of the latest version of the app

`python regexport/get_screenshot.py`
`git commit -am "updated screenshot"`

### Make a changelog

  - Make a new section for the release in the changelog `echo <tag-name> >> CHANGELOG.md`
  - Fill the section with all the commit messages since the last release `git log --pretty="- %s" <tag-name>..HEAD >> CHANGELOG.md`
  - Edit the list, summarizing the changes in a readable way

### Update the version number

  - Increment the version number in `setup.py`.  This project uses semantic versioning.
  - Create a Git Tag around the version number (helps with future changelog generation and GitHub Releases)
    - git tag -a <version number> -m "v<version number>"
    - Push tags with "git push origin --tags"

### Build a new source distribution
```
python setup.py sdist
```

### Upload the source distribution to PyPi

*Note*: For this step, you'll need account permissions for the project.

```
twine upload dist/*
```

### Convert Github Tag to Release

  - In Github, Under "Releases", click "Tags", then the latest tag
  - Click "Make Release" from the tag
  - In the box, copy-past the relevant changelog notes
  - Submit!
