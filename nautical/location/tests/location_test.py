"""
Author: barbacbd
Date:   4/20/2020
"""
import unittest
from ..point import Point
from ..util import haversine


class LocationTests(unittest.TestCase):

    def test_latitude(self):
        """
        Test both a valid and invalid latitude value checking the whether the values were set or not
        after each attempt.
        """
        p1 = Point(67.23, 0, 0)
        self.assertAlmostEqual(p1.latitude, 67.23, 2, "Latitude value is incorrect")

        p2 = Point(-67.23, 0, 0)
        self.assertAlmostEqual(p2.latitude, -67.23, 2, "Latitude value is incorrect")

        p2.latitude = "abgsdf"
        self.assertAlmostEqual(p2.latitude, -67.23, 2, "Latitude value is incorrect")

        p3 = Point(-90.23, 0, 0)
        self.assertAlmostEqual(p3.latitude, 0.0, 2, "Latitude value is incorrect")

    def test_longitude(self):
        """
        Test both a valid and invalid longitude value checking the whether the values were set or not
        after each attempt.
        """
        p1 = Point(0, 0.23, 0)
        self.assertAlmostEqual(p1.longitude, 0.23, 2, "Longitude value is incorrect")

        p2 = Point(0, -167.23, 0)
        self.assertAlmostEqual(p2.longitude, -167.23, 2, "Longitude value is incorrect")

        p2.longitude = "dasdf"
        self.assertAlmostEqual(p2.longitude, -167.23, 2, "Longitude value is incorrect")

        p3 = Point(0, 180.23, 0)
        self.assertAlmostEqual(p3.longitude, 0.0, 2, "Longitude value is incorrect")

    def test_altitude(self):
        """
        Test both a valid and invalid altitude value checking the whether the values were set or not
        after each attempt.
        """
        p1 = Point(0, 0, 1251231.2342)
        self.assertAlmostEqual(p1.altitude, 1251231.2342, 4, "Altitude value is incorrect")

        p1.altitude = "123123jnnkjk"
        self.assertAlmostEqual(p1.altitude, 1251231.2342, 4, "Altitude value is incorrect")

    def test_parser(self):
        """
        Test the parse function of the Point
        """
        p1 = Point()
        p1.parse("-110.123, 76.45, 123.67")

        self.assertAlmostEqual(p1.latitude, 76.45, 2, "Latitude value is incorrect")
        self.assertAlmostEqual(p1.longitude, -110.123, 3, "Longitude value is incorrect")
        self.assertAlmostEqual(p1.altitude, 123.67, 2, "Altitude value is incorrect")

    def test_distance(self):
        """
        Test the haversine distance function of the Point class

        test distance from virginia beach to norfolk Virginia

        """
        # location of virginia beach
        p = Point(36.8529, -75.9780)

        # location of norfolk
        dist = haversine(p, Point(36.8508, -76.2859))

        # roughly 27 km but it is closer to 27404.727 .... meters
        self.assertAlmostEqual(dist, 27404.73, 2, "Distance between VB and Norfolk is incorrect.")

    @staticmethod
    def suite() -> unittest.TestSuite:
        suite = unittest.TestSuite()
        """ LOCATION TESTS """
        suite.addTest(LocationTests("test_latitude"))
        suite.addTest(LocationTests("test_longitude"))
        suite.addTest(LocationTests("test_altitude"))
        suite.addTest(LocationTests("test_parser"))
        suite.addTest(LocationTests("test_distance"))

        return suite