<h1 align="center">
  <a href="https://github.com/barbacbd/nautical">
    <img src="https://raw.githubusercontent.com/barbacbd/nautical/master/.images/buoy.jpg" width="256" height="256" border-radius="50%" >
  </a>
  <br>Nautical</br>
</h1>

<h2 align="center">
  
[![Build-Linux](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml) [![Build-OSX](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml) [![Build-Windows](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml)

[![PyPI version fury.io](https://badge.fury.io/py/nautical.svg)](https://pypi.python.org/pypi/nautical/) [![GitHub latest commit](https://badgen.net/github/last-commit/barbacbd/nautical)](https://github.com/barbacbd/nautical/commit/) 

[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/Dev-nautical/community)


# Description

Ahoy! Whether you've got your sea legs under yeh', or you're just looking to get those toes wet, you have discovered Nautical. Nautical contains an extension to a python based web scraper that
allows users to retrieve [NOAA](https://www.ndbc.noaa.gov/) buoy information. Nautical also provides users with a simple interface to the [NOAA NCEI](https://www.ncei.noaa.gov/) web api.

Peer into that spyglass and review the [nautical documentation](https://barbacbd.github.io/nautical/build/html/index.html) for more information.


# Documentation

View the [documentation](https://github.com/barbacbd/nautical/blob/master/user/docs/Documentation.md) page for more information.

# Contributing

View the [contirbuting guidelines](https://github.com/barbacbd/nautical/blob/master/user/docs/Contributing.md) for more information.

# Examples

More details and specific examples can be found in [here](https://github.com/barbacbd/nautical/blob/master/user/docs/). 

# Building and Testing

## Create the environment [optional]

If you wish to create a virtual environment:

```
python -m venv /path/to/nautical_venv
```

**NOTE:** The `python` referenced above should be a version of python that is acceptable for this library.

Don't forget to activate the virtual environment, `source /path/to/nautical_venv/bin/activate`.

## Install dependencies

**NOTE:** The dependencies will be installed in the next step, but provides the opportunity to view
the dependency install by itself.

```
pip install pip --upgrade;

pip install -r requirements.txt
```

## Install the package

```
pip install . --upgrade
```

## Execute Tests

If you wish to view the results with a bit more information, run the following commmand:

```
pip install pytest coverage pytest-cov mock
```

All tests for the project are located in the [tests](https://github.com/barbacbd/nautical/blob/master/tests)  directory.
The minimal requirements for the contributions to make it into the repository will be to pass all tests.
Run the `pytest` command in this directory, or provide the directory to the
command. Use the `coverage and pytest-cov` packages to view all of the results more clearly.

```
pytest --cov=tests
```

If the user is running a system that can execute shell scripts, run the following from the project base directory:

```bash
scripts/pytest.sh
```

The user may also view the output of linting with:

```bash
scripts/pylint.sh
```
