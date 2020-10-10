<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django REST framework

[![Build Status](https://travis-ci.com/typeddjango/djangorestframework-stubs.svg?branch=master)](https://travis-ci.com/typeddjango/djangorestframework-stubs)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Gitter](https://badges.gitter.im/mypy-django/Lobby.svg)](https://gitter.im/mypy-django/Lobby)


Mypy stubs for [DRF 3.12.x](https://pypi.org/project/djangorestframework/). 
Supports Python 3.6, 3.7 and 3.8.

## Installation

```bash
pip install djangorestframework-stubs
```

To make mypy aware of the plugin, you need to add

```ini
[mypy]
plugins =
    mypy_drf_plugin.main
```

in your `mypy.ini` file.


## To get help

We have Gitter here: <https://gitter.im/mypy-django/Lobby>

If you think you have more generic typing issue, please refer to <https://github.com/python/mypy> and their Gitter.
