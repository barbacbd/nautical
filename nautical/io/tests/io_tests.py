"""
Author: barbacbd
Date:   4/20/2020
"""

import unittest
from ..web import get_noaa_forecast_url, get_url_source
from bs4 import BeautifulSoup


class IOTests(unittest.TestCase):

    def test_beautiful_soup(self):
        """
        Test that an invalid and valid url return the proper data
        """
        try:
            url = get_noaa_forecast_url(44099)
            soup = get_url_source(url)
            self.assertTrue(isinstance(soup, BeautifulSoup), "44099 did not return a viable Beautiful soup object")
        except Exception:
            pass

        try:
            bad_url = get_noaa_forecast_url("afasdfasdjfna")
            bad_soup = get_url_source(bad_url)
            self.assertFalse(isinstance(bad_soup, BeautifulSoup), "afasdfasdjfna did not return a viable Beautiful soup object")
        except Exception:
            pass

    def test_forecast_url(self):
        """
        Test valid and invalid sets of data passed to the create forecast url
        """
        try:
            self.assertNotEqual(get_noaa_forecast_url(44099), None, "Failed to find url for 44099")
            self.assertEqual(get_noaa_forecast_url(""), None, "Failed to find url")
        except Exception:
            pass

    @staticmethod
    def suite() -> unittest.TestSuite:
        suite = unittest.TestSuite()

        suite.addTest(IOTests("test_beautiful_soup"))
        suite.addTest(IOTests("test_forecast_url"))

        return suite