"""
Author: barbacbd
Date:   4/18/2020
"""
import unittest
from ..conversion import convert
from ..units import (
    TimeUnits,
    SpeedUnits,
    DistanceUnits,
    TemperatureUnits
)


class UnitsTest(unittest.TestCase):

    def test_good_time_conversion(self):
        """
        Start with a minutes value and see if that can be converted to all of the other
        values possible.

        Minutes =  5432.45

        Expect:
            Seconds = 325947.0
            Hours = 90.541
            Days = 3.773
        """
        init_time = 5432.45  # minutes

        self.assertAlmostEqual(
            convert(
                init_time,
                TimeUnits.MINUTES,
                TimeUnits.SECONDS
            ),
            325947.0,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_time,
                TimeUnits.MINUTES,
                TimeUnits.MINUTES
            ),
            5432.45,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_time,
                TimeUnits.MINUTES,
                TimeUnits.HOURS
            ),
            90.541,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_time,
                TimeUnits.MINUTES,
                TimeUnits.DAYS
            ),
            3.773,
            3
        )

    def test_good_speed_conversion(self):
        """
        Start with knots value and see if that can be converted to all of the other
        values possible.

        KTS =  5.34

        Expect:
            MPS = 2.747
            MPH = 6.145
            KPH = 9.890
            FPS = 9.013
        """
        init_speed = 5.34  # KTS

        self.assertAlmostEqual(
            convert(
                init_speed,
                SpeedUnits.KNOTS,
                SpeedUnits.KNOTS
            ),
            5.34,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_speed,
                SpeedUnits.KNOTS,
                SpeedUnits.MPS
            ),
            2.747,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_speed,
                SpeedUnits.KNOTS,
                SpeedUnits.MPH
            ),
            6.145,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_speed,
                SpeedUnits.KNOTS,
                SpeedUnits.KPH
            ),
            9.890,
            3
        )

        self.assertAlmostEqual(
            convert(
                init_speed,
                SpeedUnits.KNOTS,
                SpeedUnits.FPS
            ),
            9.013,
            3
        )

    def test_good_distance_conversion(self):
        """
        Start with MILES value and see if that can be converted to all of the other
        values possible.

        MILES = 2.10

        Expect:
            cm = 337961.4
            ft = 11088.0
            yd = 3696.0
            mt = 3379.620
            km = 3.380
            nm = 1.825
        """
        init_distance = 2.10  # miles

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.CENTIMETERS
            ),
            337961.4,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.FEET
            ),
            11088.0,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.YARDS
            ),
            3696.0,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.METERS
            ),
            3379.6,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.MILES
            ),
            2.1,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.KILOMETERS
            ),
            3.4,
            1
        )

        self.assertAlmostEqual(
            convert(
                init_distance,
                DistanceUnits.MILES,
                DistanceUnits.NAUTICAL_MILES
            ),
            1.8,
            1
        )

    def test_good_temperature_conversion(self):
        """
        Test converting from Fahrenheit to Celsius and the opposite
        """
        deg_f = 54.45
        self.assertAlmostEqual(
            convert(
                deg_f,
                TemperatureUnits.DEG_F,
                TemperatureUnits.DEG_C
            ),
            12.472,
            3
        )

        deg_c = 20.56
        self.assertAlmostEqual(
            convert(
                deg_c,
                TemperatureUnits.DEG_C,
                TemperatureUnits.DEG_F
            ),
            69.008,
            3
        )

    @staticmethod
    def suite() -> unittest.TestSuite:
        suite = unittest.TestSuite()
        suite.addTest(UnitsTest("test_good_time_conversion"))
        suite.addTest(UnitsTest("test_good_speed_conversion"))
        suite.addTest(UnitsTest("test_good_distance_conversion"))
        suite.addTest(UnitsTest("test_good_temperature_conversion"))

        return suite
