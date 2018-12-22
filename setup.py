import os
from distutils.core import setup


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
