# Nautical

A dual-language (Python + Go) library for scraping and parsing real-time and historical oceanographic/meteorological data from NOAA's National Data Buoy Center.

## Project structure

```
nautical/          Python package source
pkg/               Go package source
tests/             Python tests
scripts/           Shell helpers (pylint, pytest)
user/docs/         Tutorials and documentation
.github/workflows/ CI (pytest, go test, coverage badges, PyPI deploy)
```

Both Python and Go packages mirror the same module layout: `cache`, `io`, `location`, `noaa/buoy`, `sea_state`, `time`, `units`.

## Quick reference

```sh
make setup         # install package + activate pre-commit hooks
make install       # pip install ".[test]" --upgrade
make test          # run both Python and Go tests
make test-py       # pytest --cov=tests
make test-go       # go test -v ./...
make lint          # pylint (downloads .pylintrc if missing)
make format        # auto-fix formatting (ruff for Python, gofmt for Go)
make format-check  # check formatting without modifying files (used in CI)
make coverage      # tests with detailed coverage for both languages
make clean         # remove build artifacts and caches
```

### Running directly

```sh
# Python
pip install ".[test]" --upgrade
pytest --cov=tests
pylint nautical/* --rcfile=.pylintrc

# Go
go test -v ./...
go test -v -race -coverprofile=coverage.out -covermode=atomic ./...
go tool cover -func=coverage.out
```

## CI

- **Python**: tests run on Ubuntu, macOS, and Windows across Python 3.9–3.13
- **Go**: tests run on Ubuntu with race detector enabled
- **Coverage**: badge workflows auto-commit to `master` on push
- **Deploy**: PyPI publish triggered by GitHub release events

## Conventions

- Commit messages follow the format in `.github/CONTRIBUTING.md` (type prefix: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, etc.)
- Python uses `__slots__` on `BuoyData` for memory efficiency
- Properties with getters/setters for validation on `Buoy` and `Point`
- `copy`/`deepcopy` used to prevent mutation of internal state through the public API
- Custom exception hierarchy in `nautical/exceptions.py` (24 classes) — see `EXCEPTION_DESIGN.md`
- Retry/rate-limiting decorator (`@with_retry`) for web requests — see `RETRY_USAGE.md`
- Go structs use JSON/XML struct tags for serialization
- Formatting enforced via `ruff` (Python) and `gofmt` (Go) — CI checks on push and PRs
- Pre-commit hooks configured (`.pre-commit-config.yaml`) — run `make setup` to activate
