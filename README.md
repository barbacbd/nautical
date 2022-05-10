# Nautical ![build workflow](https://github.com/barbacbd/nautical/actions/workflows/python-app.yml/badge.svg) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI version fury.io](https://badge.fury.io/py/nautical.svg)](https://pypi.python.org/pypi/nautical/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barbacbd/nautical/pulse/commit-activity)
[![GitHub latest commit](https://badgen.net/github/last-commit/barbacbd/nautical)](https://github.com/barbacbd/nautical/commit/)
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)


# Tested Operating Systems

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)


# Description

A python based web scraper (extension) that grabs the buoy data from [NOAA](https://www.ndbc.noaa.gov/). The scraper utilizes kml parsing
and [BeautifulSoup](https://pypi.org/project/BeautifulSoup/) to parse through data found online. NOAA provides a single endpoint that can be
formatted with the bupy name/id for easy information retrieval.

To view the [documentation](https://barbacbd.github.io/nautical/html/index.html) for the source code please visit this [site](https://barbacbd.github.io/nautical/html/index.html).


# Documentation

View the [documentation](./Documentation.md) page for more information.

# Contributing

View the [contirbution](./Contributing.md) for more information.


# [tests](./tests)

All tests for the project are located in this directory. The minimal requirements for the contributions to make it into
the repository will be to pass all tests. Run the `pytest` command in this directory, or provide the directory to the
command. Use the `coverage and pytest-cov` packages to view all of the results more clearly.
