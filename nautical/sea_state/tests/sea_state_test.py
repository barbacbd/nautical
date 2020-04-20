"""
Author: barbacbd
Date:   4/19/2020
"""
import unittest
from .. import sea_state
from nautical.units.units import DistanceUnits


class SeaStateTests(unittest.TestCase):

    def test_sea_state_m(self):
        """
        Test that the proper sea state value was found
        """
        self.assertEqual(sea_state(0), 0)
        self.assertEqual(sea_state(-121312), 0)
        self.assertEqual(sea_state(0.05), 1)
        self.assertEqual(sea_state(0.49), 2)
        self.assertEqual(sea_state(0.51), 3)
        self.assertEqual(sea_state(2), 4)
        self.assertEqual(sea_state(3.99), 5)
        self.assertEqual(sea_state(4.001), 6)
        self.assertEqual(sea_state(7.5), 7)
        self.assertEqual(sea_state(12), 8)
        self.assertEqual(sea_state(123123123), 9)

    def test_sea_state_other(self):
        """
        Test that the proper sea state can be found given a different unit
        below and above the value of meters.
        """
        self.assertEqual(sea_state(6.234, DistanceUnits.FEET), 4)          # 1.900 Meters
        self.assertEqual(sea_state(0.0028353168, DistanceUnits.MILES), 6)  # 4.563 Meters

    @staticmethod
    def suite() -> unittest.TestSuite:
        suite = unittest.TestSuite()
        suite.addTest(SeaStateTests("test_sea_state_m"))
        suite.addTest(SeaStateTests("test_sea_state_other"))

        return suite