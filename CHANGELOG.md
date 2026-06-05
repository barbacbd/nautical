# Changelog

All notable changes to the Nautical project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-06-05

### Added
- Custom exception hierarchy for better error handling
  - 24 custom exception classes with backward compatibility
  - Comprehensive exception documentation in `user/docs/ErrorHandling.md`
  - Full test coverage in `tests/test_exceptions.py` (413 lines, 27 tests)
- Intelligent retry logic and rate limiting for web requests
  - Token bucket rate limiter (30 requests/min default)
  - Exponential backoff with ±20% jitter
  - HTTP 429 detection and Retry-After header support
  - Configurable retry behavior via `RetryConfig` class
  - Complete usage guide in `RETRY_USAGE.md`
  - Full test coverage in `tests/test_retry.py` (448 lines, 27 tests)
- Go code coverage reporting infrastructure
  - Automated coverage workflow (`.github/workflows/go-coverage.yml`)
  - Coverage badge generation and auto-commit
  - Coverage profile, percentage, and HTML reports
  - Integration with shields.io for badge rendering
- Comprehensive test coverage expansion
  - Test coverage plan document (`TEST_COVERAGE_PLAN.md`)
  - Tests for `pkg/io/web.go` (GetNOAAForecastURL)
  - Tests for `pkg/util/util.go` (GetAliases reflection function)
  - Tests for `pkg/time/nautical_time.go` (all getter/setter methods)
  - Tests for `pkg/location/point.go` (String(), X(), Y(), Z())
  - Tests for all `pkg/units/units.go` String() methods
  - Overall Go coverage improved: 62.0% → 75.2% (+13.2%)

### Changed
- **BREAKING**: Python version requirements updated from >=3.6 to >=3.8
  - Removed Python 3.6 and 3.7 support (end-of-life)
  - Added support for Python 3.11, 3.12, 3.13
  - Updated classifiers in `setup.cfg`
- **BREAKING**: Go version upgraded from 1.18 to 1.25
  - Updated dependencies: testify v1.8.1→v1.11.1, x/net v0.8.0→v0.55.0, x/text v0.8.0→v0.37.0
  - Fixed non-constant format string in `pkg/cache/file.go`
  - Fixed floating-point precision in `pkg/units/units_test.go`
- GitHub Actions updated to latest versions
  - `actions/checkout@v2` → `v4`
  - `actions/setup-python@v2` → `v5`
  - `actions/setup-go@v3` → `v5`
  - Updated Python CI matrix to test 3.8-3.13
- Improved whitespace handling in coordinate parsing
  - Now handles tabs, newlines, and all whitespace types
  - Previously only handled spaces in `pkg/location/point.go`
- Replaced deprecated BeautifulSoup methods
  - `table.findAll()` → `table.find_all()` in `nautical/io/buoy.py`

### Fixed
- Security: Removed hardcoded credentials from coverage workflow
  - Replaced personal access token with GitHub's built-in authentication
  - Uses `secrets.GITHUB_TOKEN` instead of hardcoded value
- Missing `lxml` dependency added to `requirements.txt`
  - Required by BeautifulSoup parser
- Non-constant format string error in Go cache file
  - Fixed `fmt.Sprintf(time.Now().UTC().Format(...))` pattern
- Floating-point precision issues in temperature conversion tests
  - Changed `assert.Equal` to `assert.InDelta` with 0.001 tolerance

### Documentation
- Added comprehensive error handling guide (`user/docs/ErrorHandling.md`)
  - Common error scenarios and handling patterns
  - Migration guide from generic exceptions
  - Best practices for network errors and invalid data
- Added retry logic usage guide (`RETRY_USAGE.md`)
  - Configuration examples
  - Rate limiting behavior
  - Integration with existing code
- Added test coverage expansion plan (`TEST_COVERAGE_PLAN.md`)
  - Phased approach to reach 90%+ coverage
  - Priority-based gap analysis
  - Test infrastructure improvements
  - Success metrics and quality goals

### Infrastructure
- Added `.coverage` and `*.egg-info` to `.gitignore`
- Go tests now use race detector and atomic coverage mode
- Python CI now tests across 3.8-3.13 on Linux, macOS, and Windows

### Coverage Improvements
- **Go Overall**: 62.0% → 75.2% (+13.2%)
  - `pkg/time`: 32.1% → 83.3% (+51.2%)
  - `pkg/units`: 60.4% → 97.9% (+37.5%)
  - `pkg/location`: 92.6% → 95.1% (+2.5%)
  - `pkg/util`: 0% → 92.3% (+92.3%)
  - `pkg/io`: 0% → 16.7% (+16.7%)
- **Python**: Maintained ~87% overall coverage

---

## [4.2.1] - 2024-02-15

### Changed
- Updated code coverage information (automated commit)
- Default language selection improvements

### Fixed
- Updated logs to not show by default

---

## [4.2.0] - 2024-02-14

### Changed
- Updated code coverage information (automated commit)
- Various Go package improvements

---

## [4.1.1] - 2024-02-10

### Fixed
- Fixed Go package to use a set rather than a map
- Updated tests for BeautifulSoup changes
- Updated output handling

---

## [4.1.0] - 2024-02-08

### Changed
- Updated release process
- Major updates to README and documentation
- Moved docs to correct location

---

## [4.0.0] - 2024-02-05

### Changed
- Major version release with breaking changes
- Updated Go package implementation
- Improved documentation structure

---

## [1.0.1] - Earlier Release

### Fixed
- Versioning issues resolved

---

## [1.0.0] - Initial Release

### Added
- Initial release of Nautical package
- Python package for NOAA buoy data scraping
- Go package implementation
- Core features:
  - Buoy data retrieval from NOAA
  - Source management (buoy groups/sponsors)
  - Data caching functionality
  - Location and coordinate parsing
  - Unit conversion (temperature, speed, distance, pressure, time, salinity)
  - Nautical time handling
- Basic documentation and tutorials
- Test suite for both Python and Go

### Features
- Support for various buoy data types:
  - Wind Speed, Gust, Wave Height
  - Dominant/Average Wave Period
  - Pressure, Air/Water Temperature
  - Dew Point, Salinity, Visibility
  - Tide, Swell data
  - And more
- Cache system for local data storage
- Python 3.6+ support
- Go 1.18+ support

---

## Release Versioning

- **Major version** (X.0.0): Breaking changes, major architectural updates
- **Minor version** (x.Y.0): New features, non-breaking changes
- **Patch version** (x.y.Z): Bug fixes, documentation updates

---

## Links

- [Repository](https://github.com/barbacbd/nautical)
- [Python Documentation](https://barbacbd.github.io/nautical/build/html/index.html)
- [Go Documentation](https://pkg.go.dev/github.com/barbacbd/nautical)
- [PyPI Package](https://pypi.org/project/nautical/)
- [Issue Tracker](https://github.com/barbacbd/nautical/issues)

---

[Unreleased]: https://github.com/barbacbd/nautical/compare/v4.2.1...HEAD
[4.2.1]: https://github.com/barbacbd/nautical/compare/v4.2.0...v4.2.1
[4.2.0]: https://github.com/barbacbd/nautical/compare/v4.1.1...v4.2.0
[4.1.1]: https://github.com/barbacbd/nautical/compare/v4.1.0...v4.1.1
[4.1.0]: https://github.com/barbacbd/nautical/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.com/barbacbd/nautical/compare/v1.0.1...v4.0.0
[1.0.1]: https://github.com/barbacbd/nautical/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/barbacbd/nautical/releases/tag/v1.0.0
