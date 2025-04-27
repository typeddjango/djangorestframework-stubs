import os

from setuptools import find_packages, setup


def find_stub_files(name: str) -> list[str]:
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
    "django-stubs>=5.2.0",
    "typing-extensions>=4.0",
    "requests>=2.0",
    "types-requests",
    "types-PyYAML",
]

# Keep compatible-mypy major.minor version pinned to what latest django-stubs release uses.
extras_require = {
    "compatible-mypy": ["mypy>=1.13,<1.16", "django-stubs[compatible-mypy]"],
    "coreapi": ["coreapi>=2.0.0"],
    "markdown": ["types-Markdown>=0.1.5"],
}

setup(
    name="djangorestframework-stubs",
    version="3.15.4",
    description="PEP-484 stubs for django-rest-framework",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/typeddjango/djangorestframework-stubs",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    maintainer="Marti Raudsepp",
    maintainer_email="marti@juffo.org",
    license="MIT",
    install_requires=dependencies,
    extras_require=extras_require,
    packages=["rest_framework-stubs", *find_packages(exclude=["scripts"])],
    package_data={"rest_framework-stubs": find_stub_files("rest_framework-stubs")},
    python_requires=">=3.10",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Typing :: Typed",
        "Framework :: Django",
    ],
    project_urls={
        "Release notes": "https://github.com/typeddjango/djangorestframework-stubs/releases",
        "Funding": "https://github.com/sponsors/typeddjango",
    },
)
