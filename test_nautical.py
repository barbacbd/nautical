import unittest

# import the classes where the tests are contained
#import nautical.units.units_test as ut
import tests.test_units as tu

suites  = []
suites.append(unittest.TestLoader().loadTestsFromTestCase(tu.UnitsTest))

global_suite = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(global_suite)
