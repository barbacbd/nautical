<h1 align="center">
  <a href="https://github.com/barbacbd/nautical">
    <img src=".images/buoy.jpg" width="256" height="256" border-radius="50%" >
  </a>
  <br>Nautical</br>
</h1>

<h2 align="center">
  
[![build workflow](https://github.com/barbacbd/nautical/actions/workflows/python-app.yml/badge.svg) [![PyPI version fury.io](https://badge.fury.io/py/nautical.svg)](https://pypi.python.org/pypi/nautical/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barbacbd/nautical/pulse/commit-activity) [![GitHub latest commit](https://badgen.net/github/last-commit/barbacbd/nautical)](https://github.com/barbacbd/nautical/commit/)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
</h2>

# Description

A python based web scraper (extension) that grabs the buoy data from [NOAA](https://www.ndbc.noaa.gov/). The scraper utilizes kml parsing
and [BeautifulSoup](https://pypi.org/project/BeautifulSoup/) to parse through data found online. NOAA provides a single endpoint that can be
formatted with the bupy name/id for easy information retrieval.

To view the [documentation](https://barbacbd.github.io/nautical/html/index.html) for the source code please visit this [site](https://barbacbd.github.io/nautical/html/index.html).


# Documentation

View the [documentation](./Documentation.md) page for more information.

# Contributing

View the [contirbution](./Contributing.md) for more information.


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
pip install pytest coverage pytest-cov
```

All tests for the project are located in the [tests](./tests)  directory.
The minimal requirements for the contributions to make it into the repository will be to pass all tests.
Run the `pytest` command in this directory, or provide the directory to the
command. Use the `coverage and pytest-cov` packages to view all of the results more clearly.

```
pytest --cov=tests
```
