import unittest

# import the classes where the tests are contained
from units_test import UnitsTest

suites  = []
suites.append(unittest.TestLoader().loadTestsFromTestCase(UnitsTest))

global_suite = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=0).run(global_suite)
