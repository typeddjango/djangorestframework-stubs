#!/bin/bash
set -ex

if [[ "$VIRTUAL_ENV" != "" ]]
then
  pip install --upgrade setuptools wheel twine
  python setup.py sdist bdist_wheel
  twine upload dist/*
  rm -rf dist/ build/
else
  echo "this script must be executed inside an active virtual env"
fi

