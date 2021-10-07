import unittest

# import the classes where the tests are contained
import nautical.units.units_test as ut

suites  = []
suites.append(unittest.TestLoader().loadTestsFromTestCase(ut.UnitsTest))

global_suite = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=0).run(global_suite)
