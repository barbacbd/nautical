# Github Documentation

This document will provide instructions for generating the formal documentation for the `Nautical` package.
The documentation can be found [here](https://barbacbd.github.io/nautical/html/index.html). 

# Location

The `pages` branch will always contain all of the [documentation](https://barbacbd.github.io/nautical/html/index.html).
As new code is added to the repository (on `master`), the `pages` branch must be rebased off of `master` and the
documents should be regenerated based on the new source.

# Process

The documentation tool used to generate the documentation can be found [here](https://github.com/barbacbd/auto_doc/).

The following command _should_ be executed from the base or source directory of this project. 

```
AutoDocExt nautical -a "Brent Barbachem" -e {VERSION} -c {YEAR} -d nautical --exclusions __pycache__ venv -vvvvv
```

## Removing Old Documentation [Optional]

If the `autodoc_ext_artifacts.yaml` exists, execute `AutoDocExtClean -vvvvv`.

_If the file does **not** exist, run `make clean` (if the Makefile exists)_

```
rm -rf docs/ rst_docs/ Makefile make.bat conf.py index.rst
```
