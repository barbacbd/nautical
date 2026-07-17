<h1 align="center">
  <a href="https://github.com/barbacbd/nautical">
    <img src="https://raw.githubusercontent.com/barbacbd/nautical/master/.images/buoy.jpg" width="200" height="200">
  </a>
  <br>Nautical<br>
  <sub>Real-time ocean data from NOAA buoys — Python & Go</sub>
</h1>

<p align="center">

[![Build-Linux](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-linux.yml)
[![Build-OSX](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-osx.yml)
[![Build-Windows](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/python-app-windows.yml)
[![PyPI version fury.io](https://badge.fury.io/py/nautical.svg)](https://pypi.python.org/pypi/nautical/)
![Python Code Coverage](https://raw.githubusercontent.com/barbacbd/nautical/master/.cov/coverage-badge.svg)

[![Go](https://github.com/barbacbd/nautical/actions/workflows/go.yml/badge.svg)](https://github.com/barbacbd/nautical/actions/workflows/go.yml)
[![Go Reference](https://pkg.go.dev/badge/github.com/barbacbd/nautical.svg)](https://pkg.go.dev/github.com/barbacbd/nautical)
![Go Code Coverage](https://raw.githubusercontent.com/barbacbd/nautical/master/.cov-go/coverage-badge.svg)

</p>

Nautical is a library for scraping and parsing real-time and historical oceanographic data from [NOAA's National Data Buoy Center](https://www.ndbc.noaa.gov/). It supports both **Python** and **Go**, and was built for research, data logging, and monitoring — but there are many more possibilities to discover.

## Installation

**Python** (requires 3.9+):

```bash
pip install nautical
```

**Go** (requires 1.18+):

```bash
go get github.com/barbacbd/nautical
```

## Quick Start

```python
from nautical.io.buoy import create_buoy

# Fetch live data for a buoy station
buoy = create_buoy("44099")

if buoy and buoy.valid:
    # Iterate over all available measurements
    for name, value in buoy.data:
        print(f"{name}: {value}")
```

```go
buoy, err := noaa.CreateBuoy("44099")
if err != nil {
    log.Fatal(err)
}
fmt.Println(buoy)
```

## Features

### Buoy Data

A buoy may contain any of the following measurements:

| Data | Abbreviation | Units |
| ---- | ---- | ---- |
| Wind Speed | `wspd` | Knots |
| Gust | `gst` | Knots |
| Wave Height | `wvht` | Feet |
| Dominant Wave Period | `dpd` | Seconds |
| Average Wave Period | `apd` | Seconds |
| Pressure | `pres` | PSI |
| Pressure Tendency | `ptdy` | PSI |
| Air Temperature | `atmp` | Fahrenheit |
| Water Temperature | `wtmp` | Fahrenheit |
| Dew Point | `dewp` | Fahrenheit |
| Salinity | `sal` | PSU |
| Visibility | `vis` | Nautical Miles |
| Tide | `tide` | Feet |
| Swell Height | `swh` | Feet |
| Swell Wave Period | `swp` | Seconds |
| Wind Wave Height | `wwh` | Feet |
| Wind Wave Period | `wwp` | Seconds |
| Ocean Temperature | `otmp` | Fahrenheit |
| Wind Speed 10m | `wspd10m` | Knots |
| Wind Speed 20m | `wspd20m` | Knots |
| Depth | `depth` | Feet |

### Sources

A source is a group of buoys organized by sponsor or owner. Use sources to discover available buoys by category.

```python
from nautical.io.sources import get_buoy_sources

sources = get_buoy_sources()
for name, source in sources.items():
    print(f"{name}: {len(source)} buoys")
```

### Data Caching

Save and reload buoy data locally. NOAA refreshes data roughly every 30 minutes — the cache lets you avoid redundant network calls.

```python
from nautical.cache import dumps, load

# Save current data
dumps(data)

# Load it back later
cached = load()
```

## Documentation

- [Python API Reference](https://barbacbd.github.io/nautical/) — auto-generated from source
- [Go API Reference](https://pkg.go.dev/github.com/barbacbd/nautical) — hosted on pkg.go.dev
- [Python Tutorials](https://github.com/barbacbd/nautical/blob/master/user/docs/PythonTutorials.md)
- [Go Tutorials](https://github.com/barbacbd/nautical/blob/master/user/docs/GoTutorials.md)
- [Error Handling Guide](https://github.com/barbacbd/nautical/blob/master/user/docs/ErrorHandling.md)

## Development

```bash
make setup         # install + activate pre-commit hooks
make test          # run Python and Go tests
make lint          # pylint
make format        # auto-fix formatting (ruff + gofmt)
make docs          # build Sphinx API docs locally
make clean         # remove build artifacts
```

## Contributing

See [CONTRIBUTING.md](https://github.com/barbacbd/nautical/tree/master/.github/CONTRIBUTING.md) for guidelines and commit message conventions.

## License

Copyright © 2022–2026, Brent Barbachem. Released under the [MIT License](https://raw.githubusercontent.com/barbacbd/nautical/master/LICENSE.txt).
