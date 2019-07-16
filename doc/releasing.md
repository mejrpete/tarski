
# Uploading a Tarski release to the Python Package Index

Docs: <https://packaging.python.org/tutorials/packaging-projects/>

First, make sure you are on the master branch and on the right commit.

1. Update the `CHANGELOG.md` file.
1. Update the version number in `src/tarski/version.py`
1. Commit and tag the release.
1. Run the following instructions from the root directory of the project:


    python3 -m pip install --upgrade twine setuptools wheel  # (optional)

    rm -rf dist/
    python3 setup.py sdist bdist_wheel
    
    # Test first (result will go to https://test.pypi.org/project/tarski/):
    python3 -m twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
    
    # Then go!
    python3 -m twine upload --skip-existing dist/*


