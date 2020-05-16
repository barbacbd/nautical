"""
Author: barbacbd
Date:   4/20/2020
"""
from unittest import TextTestRunner
from nautical.io.tests.io_tests import IOTests
from nautical.location.tests.location_test import LocationTests
from nautical.sea_state.tests.sea_state_test import SeaStateTests
from nautical.time.tests.time_test import TimeTest
from nautical.units.tests.units_test import UnitsTest


def main():
    # Create the runner to run each suite
    runner = TextTestRunner()

    runner.run(IOTests().suite())
    runner.run(LocationTests().suite())
    runner.run(SeaStateTests().suite())
    runner.run(TimeTest().suite())
    runner.run(UnitsTest().suite())


if __name__ == '__main__':
    main()
