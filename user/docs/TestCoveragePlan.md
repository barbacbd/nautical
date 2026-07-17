# Test Coverage Expansion Plan

This document outlines a comprehensive plan to expand test coverage for both Python and Go codebases.

## Current Coverage Status

### Go: 62.0% overall
- ✅ `pkg/sea_state`: 100.0%
- ✅ `pkg/location`: 92.6%
- 🟡 `pkg/noaa/buoy`: 65.9%
- 🟡 `pkg/cache`: 62.7%
- 🟡 `pkg/units`: 60.4%
- 🔴 `pkg/time`: 32.1%
- 🔴 `pkg/io`: 0.0%
- 🔴 `pkg/util`: 0.0%

### Python: ~87% (estimated from badge)
- Test files exist for: buoy, cache, io, location, sea_state, time, units
- No test file for: retry (just added), exceptions (just added)

## Priority 1: Critical Gaps (0% coverage)

### Go - pkg/io (0% coverage)
**Missing tests:**
- `GetNOAAForecastURL()` - URL construction
- `GetURLSource()` - Web scraping with BeautifulSoup

**Proposed tests:**
```go
// pkg/io/web_test.go
func TestGetNOAAForecastURL(t *testing.T) {
    tests := []struct {
        name     string
        buoyID   string
        expected string
    }{
        {
            name:     "Valid buoy ID",
            buoyID:   "44099",
            expected: "https://www.ndbc.noaa.gov/station_page.php?station=44099",
        },
        {
            name:     "Empty buoy ID",
            buoyID:   "",
            expected: "https://www.ndbc.noaa.gov/station_page.php?station=",
        },
        {
            name:     "Buoy ID with special characters",
            buoyID:   "TEST-123",
            expected: "https://www.ndbc.noaa.gov/station_page.php?station=TEST-123",
        },
    }
}

func TestGetURLSource(t *testing.T) {
    // Test with mock HTTP server
    // Test error handling for invalid URLs
    // Test HTML parsing
}
```

### Go - pkg/util (0% coverage)
**Missing tests:**
- `GetAliases()` - Reflection-based alias extraction

**Proposed tests:**
```go
// pkg/util/util_test.go
func TestGetAliases(t *testing.T) {
    type TestStruct struct {
        Field1 string `json:"field1"`
        Field2 int    `json:"field2"`
        Field3 bool   `json:"field3,omitempty"`
    }

    aliases := GetAliases(TestStruct{})
    // Verify alias map is correct
}
```

### Go - Source operations (0% coverage)
**Missing tests:**
- `GetBuoySources()` - Fetch sources from NOAA KML
- `FilterSourcesByType()` - Filter sources by type
- `downloadSourcesFile()` - Download KML file
- `removeSourcesFile()` - Clean up downloaded file

**Challenge**: These require network access or file I/O
**Proposed solution**: Mock HTTP client or use test fixtures

```go
func TestGetBuoySources(t *testing.T) {
    // Option 1: Use httptest.Server with mock KML
    // Option 2: Use test fixture KML file
    // Test different source types
    // Test error handling
}

func TestFilterSourcesByType(t *testing.T) {
    // Create test sources
    // Filter by different types
    // Verify correct sources returned
}
```

## Priority 2: Low Coverage (<50%)

### Go - pkg/time (32.1% coverage)
**Untested functions:**
- `SetMinutes()`, `GetHours()`, `SetHours()` - Getters/setters
- `SetFormat()`, `SetMidday()` - Time format operations
- `String()` - String representation

**Proposed tests:**
```go
// pkg/time/nautical_time_test.go
func TestNauticalTimeGettersSetters(t *testing.T) {
    nt := &NauticalTime{}

    // Test SetMinutes
    nt.SetMinutes(30)
    assert.Equal(t, 30, nt.Minutes)

    // Test GetHours
    nt.Hours = 14
    assert.Equal(t, 14, nt.GetHours())

    // Test SetHours with validation
    err := nt.SetHours(25) // Invalid
    assert.Error(t, err)

    // Test SetFormat
    nt.SetFormat(HOUR_24)
    assert.Equal(t, HOUR_24, nt.Format)
}

func TestNauticalTimeString(t *testing.T) {
    tests := []struct {
        name     string
        nt       NauticalTime
        expected string
    }{
        {
            name:     "12-hour AM format",
            nt:       NauticalTime{Hours: 9, Minutes: 30, Format: HOUR_12, Midday: AM},
            expected: "09:30 AM",
        },
        {
            name:     "24-hour format",
            nt:       NauticalTime{Hours: 14, Minutes: 45, Format: HOUR_24},
            expected: "14:45",
        },
    }
}
```

### Go - pkg/cache (62.7% coverage)
**Low coverage functions:**
- `FindCacheDir()` - Only 18.2% coverage
- `CopyCurrentCacheWithTimestamp()` - 0% coverage

**Proposed tests:**
```go
func TestFindCacheDir(t *testing.T) {
    // Test with NAUTICAL_CACHE_DIR env var set
    os.Setenv("NAUTICAL_CACHE_DIR", "/tmp/test-cache")
    defer os.Unsetenv("NAUTICAL_CACHE_DIR")

    dir, err := FindCacheDir()
    assert.NoError(t, err)
    assert.Equal(t, "/tmp/test-cache", dir)

    // Test default behavior per OS
    os.Unsetenv("NAUTICAL_CACHE_DIR")
    dir, err = FindCacheDir()
    assert.NoError(t, err)
    assert.Contains(t, dir, "nautical")
}

func TestCopyCurrentCacheWithTimestamp(t *testing.T) {
    // Create test cache
    cache := &NauticalCacheData{Filename: "/tmp/test.json"}

    // Copy with timestamp
    err := cache.CopyCurrentCacheWithTimestamp()
    assert.NoError(t, err)

    // Verify new filename contains timestamp
    assert.Contains(t, cache.Filename, "test")
    assert.Regexp(t, `\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}`, cache.Filename)
}
```

## Priority 3: Missing String() Methods

Many types have 0% coverage for `String()` methods. These are usually simple but should be tested:

```go
func TestPointString(t *testing.T) {
    p := Point{Latitude: 36.5, Longitude: -75.3, Altitude: 10.0}
    expected := "36.50, -75.30, 10.00"
    assert.Equal(t, expected, p.String())
}

func TestSourceString(t *testing.T) {
    source := Source{Name: "Test Source", Description: "Test Description"}
    str := source.String()
    assert.Contains(t, str, "Test Source")
    assert.Contains(t, str, "Test Description")
}

// Similar for all unit types
func TestTimeUnitsString(t *testing.T) {
    assert.Equal(t, "SECONDS", SECONDS.String())
    assert.Equal(t, "MINUTES", MINUTES.String())
}
```

## Priority 4: Python - New Modules

### Python - nautical/io/retry.py (0% Python coverage)
**Status**: Just added, no tests yet in main test suite
**Note**: Has comprehensive Go-style tests in `tests/test_retry.py`

**Integration needed:**
```python
# tests/test_io.py - Add retry integration tests
def test_get_url_source_with_retry():
    """Test that get_url_source uses retry decorator."""
    # Verify retry behavior
    # Test with mock that fails first attempt
    pass

def test_get_url_source_rate_limiting():
    """Test rate limiter is applied."""
    # Make multiple requests
    # Verify rate limiting occurs
    pass
```

### Python - nautical/exceptions.py (0% coverage in main suite)
**Status**: Has dedicated test file `tests/test_exceptions.py`
**Action**: Verify it's run in coverage calculation

**Additional integration tests:**
```python
# tests/test_buoy.py - Add exception tests
def test_create_buoy_raises_buoy_not_found():
    """Test that invalid buoy raises BuoyNotFoundError."""
    from nautical.exceptions import BuoyNotFoundError

    with pytest.raises(BuoyNotFoundError):
        create_buoy("INVALID_BUOY_ID_12345")

def test_convert_units_raises_invalid_units():
    """Test that invalid units raise InvalidUnitsError."""
    from nautical.exceptions import InvalidUnitsError

    with pytest.raises(InvalidUnitsError):
        convert_temperature(100, "invalid", TemperatureUnits.DEG_C)
```

## Priority 5: Edge Cases and Error Paths

### Error Handling Tests

Many functions have low coverage because error paths aren't tested:

```go
// Test error returns
func TestParseWithErrors(t *testing.T) {
    tests := []struct {
        name        string
        input       string
        expectError bool
    }{
        {"Invalid format", "not-a-coordinate", true},
        {"Out of bounds latitude", "100.0, 200.0", true},
        {"Missing longitude", "50.0", true},
    }
}

// Test nil/empty inputs
func TestNilInputs(t *testing.T) {
    _, err := GetDistance(nil, &Point{})
    assert.Error(t, err)

    _, err = InRange(nil, nil, 100.0)
    assert.Error(t, err)
}

// Test boundary conditions
func TestBoundaryConditions(t *testing.T) {
    // Test exactly at limits
    p := Point{}
    err := p.SetLatitude(90.0)  // Max valid
    assert.NoError(t, err)

    err = p.SetLatitude(90.1)   // Just over
    assert.Error(t, err)
}
```

### Integration Tests

Currently most tests are unit tests. Add integration tests:

```python
# tests/test_integration.py
def test_full_buoy_workflow():
    """Test complete workflow from fetch to cache."""
    # 1. Fetch buoy data
    buoy = create_buoy("44099")
    assert buoy.valid

    # 2. Save to cache
    cache_data = {CacheData.BUOYS.name: [buoy]}
    dumps(cache_data)

    # 3. Load from cache
    loaded = load()
    assert len(loaded[CacheData.BUOYS.name]) == 1

    # 4. Verify data matches
    assert loaded[CacheData.BUOYS.name][0].station == "44099"

def test_source_filtering_workflow():
    """Test fetching and filtering sources."""
    sources = get_buoy_sources()
    assert len(sources) > 0

    filtered = FilterSourcesByType(sources, SourceType.SHIPS)
    for source in filtered:
        assert source.type == SourceType.SHIPS
```

## Priority 6: Performance and Stress Tests

```go
func BenchmarkGetDistance(b *testing.B) {
    p1 := Point{Latitude: 36.0, Longitude: -75.0}
    p2 := Point{Latitude: 37.0, Longitude: -76.0}

    for i := 0; i < b.N; i++ {
        _, _ = p1.GetDistance(&p2)
    }
}

func TestLargeDataSet(t *testing.T) {
    // Test with 1000 buoys
    buoys := make([]Buoy, 1000)
    for i := range buoys {
        buoys[i] = Buoy{Station: fmt.Sprintf("TEST%d", i)}
    }

    // Verify cache can handle it
    cache := NauticalCache{Buoys: buoys}
    // ... test operations
}
```

## Implementation Strategy

### Phase 1: Quick Wins (Week 1)
1. Add String() method tests for all types (~2 hours)
2. Add getter/setter tests for NauticalTime (~2 hours)
3. Add Point.Z() and Point.String() tests (~1 hour)
4. Target: +10% Go coverage (62% → 72%)

### Phase 2: I/O and Network (Week 2)
1. Create mock HTTP server for testing
2. Add GetURLSource() tests (~4 hours)
3. Add GetBuoySources() tests with fixtures (~6 hours)
4. Add Python retry integration tests (~2 hours)
5. Target: +15% Go coverage (72% → 87%)

### Phase 3: Edge Cases (Week 3)
1. Add error path tests for all functions (~6 hours)
2. Add boundary condition tests (~4 hours)
3. Add nil/empty input tests (~2 hours)
4. Target: +5% Go coverage (87% → 92%)

### Phase 4: Integration & Performance (Week 4)
1. Add Python integration tests (~4 hours)
2. Add Go benchmarks (~2 hours)
3. Add stress tests (~2 hours)
4. Target: Maintain 92%+ coverage

## Test Infrastructure Improvements

### 1. Test Fixtures
Create test data fixtures for consistent testing:

```
tests/fixtures/
├── buoy_data/
│   ├── valid_buoy_44099.json
│   ├── invalid_buoy.json
│   └── empty_buoy.json
├── kml/
│   ├── sample_sources.kml
│   └── empty_sources.kml
└── html/
    ├── valid_station_page.html
    └── error_page.html
```

### 2. Mock Helpers
Create reusable mocks:

```go
// tests/mocks/http.go
func NewMockNOAAServer(t *testing.T) *httptest.Server {
    return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Serve test fixtures based on URL
    }))
}

// tests/mocks/buoy.go
func NewMockBuoy(station string) *Buoy {
    // Return pre-configured test buoy
}
```

### 3. Test Utilities
```go
// tests/testutil/assertions.go
func AssertPointsEqual(t *testing.T, expected, actual Point) {
    assert.InDelta(t, expected.Latitude, actual.Latitude, 0.0001)
    assert.InDelta(t, expected.Longitude, actual.Longitude, 0.0001)
    assert.InDelta(t, expected.Altitude, actual.Altitude, 0.0001)
}
```

### 4. Coverage Tools
Add coverage analysis scripts:

```bash
#!/bin/bash
# scripts/coverage-report.sh

# Generate coverage report
go test -coverprofile=coverage.out ./...

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# Find files with <80% coverage
go tool cover -func=coverage.out | awk '$3 < 80.0 {print $1, $3}'

# Calculate overall coverage
go tool cover -func=coverage.out | grep total | awk '{print $3}'
```

## Success Metrics

### Target Coverage Goals
- **Go Overall**: 62% → 90%+
- **Go pkg/io**: 0% → 80%+
- **Go pkg/time**: 32% → 85%+
- **Go pkg/util**: 0% → 100%
- **Python Overall**: 87% → 95%+

### Quality Metrics
- All public functions have at least one test
- All error paths are tested
- All boundary conditions are tested
- All String() methods are tested
- Integration tests cover main workflows

## Conclusion

Expanding test coverage is a systematic process focusing on:
1. **0% coverage functions** (highest priority)
2. **Error paths and edge cases**
3. **Integration tests** (currently missing)
4. **Test infrastructure** (fixtures, mocks, utilities)

By following this phased approach, we can achieve 90%+ coverage while ensuring tests are meaningful and maintainable.
