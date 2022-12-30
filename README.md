# team9-server
[![Python 3.8.13](https://img.shields.io/badge/python-3.8.13-blue.svg)](https://www.python.org/downloads/release/python-3813/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Development Guide

To setup virtualenv, follow below commands. (It is based on pyenv, but it is also fine to use conda or other virtualenv tools)
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
## Development Cycle
We use 3 environments : `local`, `dev`, `prod`
1. Test at local
2. Test at dev
3. PR Review
4. Automatically deploy at prod(ec2)

### Local Server
Local server uses gunicorn + sqlite3.
You can test api at http://localhost:8000/

```bash
$ make run-local # Start Local Server - automatically migrate db
$ make down-local # Terminate Local Server
```

### Dev Server
Dev server uses gunicorn + sqlite3, but use docker which is same setting with prod
You can test api at http://localhost:8000/

```bash
$ make run-dev # Start Dev Server - automatically migrate db
$ make down-dev # Terminate Dev Server
```

# 

## Convention
- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [black](https://black.readthedocs.io/en/stable/)
- [isort](https://pycqa.github.io/isort/)
