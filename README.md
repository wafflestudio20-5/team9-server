# team9-server
[![Python 3.8.13](https://img.shields.io/badge/python-3.8.13-blue.svg)](https://www.python.org/downloads/release/python-3813/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Development Environment Setting

To setup virtualenv, follow below commands. (It is based on pyenv, but it is also fine to use conda)
```bash
$ pyenv virtualenv 3.8.13 dear_j
$ pyenv activate dear_j
$ pip install -r requirements.dev.txt
```

To apply precommit hook, please execute below command in terminal.
```bash
$ yarn install
```

#

## Development Guide

To run local server, execute follow command.
```bash
$ make up # -> http://localhost
```

#


## Convention
- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [black](https://black.readthedocs.io/en/stable/)
- [isort](https://pycqa.github.io/isort/)
