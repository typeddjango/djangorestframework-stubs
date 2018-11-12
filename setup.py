import os
from distutils.core import setup


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
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
    packages=['mypy_djangorestframework_plugin']
    # package_data=find_stubs('django-stubs')
)
