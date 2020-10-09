#!/bin/bash
set -ex

pip install wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist/ build/
