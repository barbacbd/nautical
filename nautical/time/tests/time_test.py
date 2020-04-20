"""
Author: barbacbd
Date:   4/18/2020
"""
import unittest
from ..nautical_time import nTime
from ..conversion import convert_noaa_time
from .. import TimeFormat, Midday


class TimeTest(unittest.TestCase):

    def test_correct_conversion(self):
        """
        Properly convert the normal time string that will be retrieved
        from noaa website.
        """
        time_str = "10:30&nbsp;am"
        t = convert_noaa_time(time_str)
        self.failIfEqual(t, None)
        self.assertEqual(t.minutes, 30)
        try:
            hours, units = t.hours
        except ValueError:
            hours = t.hours

        self.assertEqual(hours, 10)

    def test_incorrect_conversion(self):
        """
        First test:
            The time string below has extra fields after that will cause
            an error which means that no nTime object is created.

        Second Test:
            The time string has an invalid midday value. The value should
            be am or pm. LM will cause an error to occur and none will be
            returned instead of an nTime object
        """
        time_str = "10:30:123&nbsp;am"
        t = convert_noaa_time(time_str)
        self.assertEqual(t, None)

        time_str = "10:30&nbsp;lm"
        t = convert_noaa_time(time_str)
        self.assertEqual(t, None)

    def test_nTime_12_hr_correct(self):
        """
        The Test has both a correct minute and hour value.
        """
        t = nTime()
        t.minutes = 45
        t.hours = 8, Midday.PM
        self.assertEqual(t.minutes, 45)
        self.assertEqual(t.hours, 8)

    def test_nTime_24_hr_incorrect_minutes(self):
        """
        The minutes value is less than 0 meaning that the value
        wont change. The current value is initialized to 0, so
        that is what we will expect.
        """
        u = nTime(TimeFormat.HOUR_24)
        u.minutes = -1
        u.hours = 10, Midday.PM
        self.assertEqual(u.minutes, 0)
        self.assertEqual(u.hours, 22)

    def test_nTime_24_hr_pm_set(self):
        """
        Test the ability to set a pm value along with a value greater
        than 12. The value will be ignored and it will be interpreted
        as a 24 hour format.
        """
        v = nTime(TimeFormat.HOUR_24)
        v.minutes = 59
        v.hours = 13, Midday.PM
        self.assertEqual(v.minutes, 59)
        self.assertEqual(v.hours, 13)

    def test_nTime_24_hr_high_minutes_high_hours(self):
        """
        Test that the minute value is too large. Again
        The value is initialized to 0, so that is the value
        that we expect. The hour value is also incorrect
        as it is greater than 24
        """
        x = nTime(TimeFormat.HOUR_24)
        x.minutes = 61
        x.hours = 25
        self.assertEqual(x.minutes, 0)
        self.assertEqual(x.hours, 0)

    def test_nTime_24_hr_low_hours(self):
        """
        Test that the hour value is too low.
        """
        x = nTime(TimeFormat.HOUR_24)
        x.minutes = 45
        x.hours = -1
        self.assertEqual(x.minutes, 45)
        self.assertEqual(x.hours, 0)

    @staticmethod
    def suite() -> unittest.TestSuite:
        suite = unittest.TestSuite()
        suite.addTest(TimeTest("test_correct_conversion"))
        suite.addTest(TimeTest("test_incorrect_conversion"))
        suite.addTest(TimeTest("test_nTime_24_hr_incorrect_minutes"))
        suite.addTest(TimeTest("test_nTime_24_hr_pm_set"))
        suite.addTest(TimeTest("test_nTime_24_hr_high_minutes_high_hours"))
        suite.addTest(TimeTest("test_nTime_24_hr_low_hours"))

        return suite
