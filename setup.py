import os
from distutils.core import setup

from setuptools import find_packages


def find_stub_files(name):
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith(".pyi"):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


with open("README.md", "r") as f:
    readme = f.read()

dependencies = ["mypy>=0.782", "django-stubs>=1.6.0", "typing-extensions"]

setup(
    name="djangorestframework-stubs",
    version="1.2.0",
    description="PEP-484 stubs for django-rest-framework",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/typeddjango/djangorestframework-stubs",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    license="MIT",
    install_requires=dependencies,
    packages=["rest_framework-stubs", *find_packages(exclude=["scripts"])],
    package_data={"rest_framework-stubs": find_stub_files("rest_framework-stubs")},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
