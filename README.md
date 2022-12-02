<h1 align="center">
  <a href="https://github.com/barbacbd/nautical">
    <img src="https://raw.githubusercontent.com/barbacbd/nautical/master/.images/buoy.jpg" width="256" height="256" border-radius="50%" >
  </a>
  <br>Nautical</br>
</h1>

<h2 align="center">
  
[![Build-Linux](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml) [![Build-OSX](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml) [![Build-Windows](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml)

[![PyPI version fury.io](https://badge.fury.io/py/nautical.svg)](https://pypi.python.org/pypi/nautical/) [![GitHub latest commit](https://badgen.net/github/last-commit/barbacbd/nautical)](https://github.com/barbacbd/nautical/commit/) ![Code Coverage](https://raw.githubusercontent.com/barbacbd/nautical/master/.cov/coverage-badge.svg)

[![Go](https://github.com/barbacbd/nautical/actions/workflows/go.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/go.yml) [![Go Reference](https://pkg.go.dev/badge/github.com/barbacbd/nautical.svg)](https://pkg.go.dev/github.com/barbacbd/nautical)

# Description

Ahoy! Whether you've got your sea legs under yeh', or you're just looking to get those toes wet, you have discovered Nautical. Nautical is a web scraper that allows its users to parse real time data from [NOAA's](https://www.ndbc.noaa.gov/) buoys. You can try Nautical as a python or GO package! Nautical was created for research and data logging purposes, but there are many more possibilities for users to discover. 


If you would like to view the python documentation follow the [link to nautical's python documentation](https://barbacbd.github.io/nautical/build/html/index.html). 

If you would like to view the GO documentation follow the [link to nautical's GO documentation](https://pkg.go.dev/github.com/barbacbd/nautical).


# Table of Contents

   * [Features](#features)
      * [Buoys](#buoys)
      * [Sources](#sources)
      * [Data Caching](#data-caching)
   * [Prerequisites](#prerequisites)
   * [Casting Off](#casting-off)
   * [Tutorials](#tutorials)
   * [Testing](#testing)
      * [Python](#python)
      * [Golang](#go)
   * [Contributing](#contributing)
      * [Contribution Flow](#contribution-flow)
      * [Suggested Commit Message Format](#suggested-commit-message-format)
   * [Copyright](#copyright)

# Features

The following are a set of features and/or data that can be accessed via the package. 

## Sources

A source is a group of buoys. The source can be thought of as a sponsor or owner of the group/set of buoys. The source may be used as an indicator of the type of data that is stored in a buoy object. 

**Note**: The `TAO` and `Tsunami` sources are not available in any regard.


## Buoys

A buoy _may_ contain, but are not limitted to, any of the following variables.

| Data | Abbreviation |Units |
| ---- | ---- | ---- |
| Wind Speed | wspd | Knots |
| Gust | gst | Knots |
| Wave Height | wvht | Feet |
| Dominant Wave Period | dpd | Seconds |
| Average Wave Period | apd | Seconds |
| Pressure | pres | PSI |
| Pressure Tendency | ptdy | PSI |
| Air Temperature | atmp | Fahrenheit |
| Water Temperature | wtmp | Fahrenheit |
| Dew Point | dewp | Fahrenheigt |
| Salinity | sal | PSU |
| Visibility | vis | Nautical Miles |
| Tide | tide | Feet |
| Swell Height | swh | Feet |
| Swell Wave Period | swp | Seconds |
| Wind Wave Height | wwh | Feet |
| Wind Wave Period | wwp | Seconds |
| Ocean Temperature | otmp | Fahrenheit |
| Wind Speed 10m Interval | wspd10m | Knots |
| Wind Speed 20m Interval | wspd10m | Knots |
| Depth | depth | Feet |

## Data Caching

The cache can be used to save and load information about buoys and sources. The feature enables users to locally store and retrieve older information. NOAA refreshes the online data roughly every 30 minutes. The cache package can be used to throttle data retrieval calls to ensure the user is not wasting system resources when data has not been updated by NOAA.

- Create cache files
- Copy cache files to new names (with timestamps or custom names)
- Load Cache files to Nautical Objects.

**Note**: _[Nautical cache](https://github.com/barbacbd/nautical/blob/master/nautical/cache/) was added in version 3.1.0_.

# Prerequisites 

The python package requires `python>=3.6`. You can use a package manager to install a version of python that satifies the requirements, or you may manually install python from the [website](https://www.python.org/downloads/).
<br>
<br>
The GO package requires `golang>=1.18`. To install go please visit the official [website](https://go.dev/doc/install).

**Note**: _The GO requirement is not strict, but previous versions have Not been tested_.

# Casting Off

- Ensure your system meets the [prerequisites](#prerequisites).
- Clone or Fork the repository.
- Run the [package tests](#testing)

# Tutorials

Follow the link to view the [tutorials for the python package](https://github.com/barbacbd/nautical/blob/master/user/docs/PythonTutorials.md).

Follow the link to view the [tutorials for the go package](https://github.com/barbacbd/nautical/blob/master/user/docs/GoTutorials.md).

# Testing

## Python 

All python tests are located in the [tests](https://github.com/barbacbd/nautical/tree/master/tests) directory.

```bash
python 3.x -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r test_requirements.txt
pytest --cov=tests
```

**Note**: _The virtual environment and coverage are optional_.

## GO

All golang tests are located with the golang source in [pkg](https://gith
ub.com/barbacbd/nautical/tree/master/pkg). The following should be executed from the project home directory.

```bash
go get -u
go test -v ./...
```

# Contributing

If you are aiming to become the first mate, second mate, deck cadet, engineer, or scallywag you have found your
way to the contributions documentation. Please continue reading if you would like to contribute or just follow along with the
development progress of the package.

- Ensure your system meets the [prerequisites](#prerequisites).
- Fork the repository
- Follow the [Casting Off](#casting-off) section above
- Install the build dependencies, see [building and testing](https://github.com/barbacbd/nautical/blob/master/README.md).
- Play with the project, submit bugs, submit patches!

## Contribution Flow

Anyone may submit [issues](https://github.com/barbacbd/nautical/issues). In fact, it is encouraged that users submit issues to contribute to the success and improvement of the project.
The issues will be reviewed by the captain, and given the proper tags to assist developers. Shipmates that would like to work on pull requests, the workflow is roughly:

1. Create a topic branch from where you want to base your work (usually master).
2. Make commits of logical units.
3. Make commit messages that clearly document the changes.
4. Push your changes to a topic branch in your fork of the repository.
5. Make sure the tests pass, and add any new tests as appropriate.
6. Submit a pull request to the original repository.

## Suggested Commit Message Format

A rough convention for commit messages that is designed to answer two
questions: what changed and why. The subject line should feature the what and
the body of the commit should describe the why.

Example:

```

noaa: Added XXX functionality to XXXX

** Added the XXX function to XXX to satisfy the need/
requirement for XXX.

** Additional information followed in other bullet points.

```

**Note**: _It is suggested (but not required) to add the Issue number to the commit message._


# Copyright

Copyright © 2022, Brent Barbachem. Released under the [MIT License](https://raw.githubusercontent.com/barbacbd/nautical/master/LICENSE.txt).