import os

from setuptools import find_packages, setup


def find_stub_files(name):
    result = []
    for root, _dirs, files in os.walk(name):
        for file in files:
            if file.endswith(".pyi"):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


with open("README.md") as f:
    readme = f.read()

dependencies = [
    "mypy>=0.930,<0.950",
    "django-stubs>=1.10.1",
    "typing-extensions>=3.7.2",
    "requests>=2.0.0",
    "coreapi>=2.0.0",
    "types-requests>=0.1.12",
    "types-PyYAML>=5.4.3",
    "types-Markdown>=0.1.5",
]

setup(
    name="djangorestframework-stubs",
    version="1.5.0",
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
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
)
