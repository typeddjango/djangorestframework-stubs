import os
from distutils.core import setup


def find_stubs(package):
    stubs = []
    for fpath in os.scandir(package):
        if fpath.is_file():
            path = fpath.path.replace(package + os.sep, 'rest_framework' + os.sep, 1)
            stubs.append(path)
    return {package: stubs}


setup(
    name="djangorestframework-stubs",
    url="https://github.com/mkurnikov/djangorestframework-stubs.git",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    version="0.1.0",
    license='BSD',
    install_requires='djangorestframework>=3.9.0',
    packages=['mypy_rest_framework_plugin']
)
