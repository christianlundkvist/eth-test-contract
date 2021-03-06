import unittest
import functools
import inspect
import operator
import itertools

from ethereum import tester
from ethereum import utils

import serpent

class TestContract(unittest.TestCase):

    def __init__(self, filenames, testcase):
        unittest.TestCase.__init__(self, testcase)
        if isinstance(filenames, list):
            if len(filenames) == 0:
                raise RuntimeError('List of contract filenames cannot be empty.')
            self.files = filenames
        else:
            raise RuntimeError('Input filenames must be a list')

    def setUp(self):

        self.keys = tester.keys
        self.accounts = tester.accounts

        self.k0, self.k1, self.k2 = self.keys[:3]
        self.a0, self.a1, self.a2 = self.accounts[:3]

    def reset_state(self):
        return tester.state()

    def reset_all_contracts(self, state):

        num_files = len(self.files)
        contracts = list( itertools.starmap(state.abi_contract, zip(self.files,self.keys[:num_files])) )
        return contracts

    def reset_contract(self, state, contract_idx, key):

        return state.abi_contract(self.files[contract_idx], key, gas=500000000)


def make_test_suite(TestClass, filenames, test_funcs=None):

    # One string is interpreted as one file
    if isinstance(filenames,str):
        filenames = [filenames]
    
    if test_funcs is None:
        # inspect.getmembers returns list of pairs (name, value)
        member_func_names = map(operator.itemgetter(0), inspect.getmembers(TestClass, inspect.ismethod))
        is_test_case = lambda fname: len(fname) >=4 and fname[:4] == 'test'
        testcase_names = filter(is_test_case, member_func_names)
    else:
        testcase_names = test_funcs

    TestClassWithFiles = functools.partial(TestClass, filenames)
    testcases = map(TestClassWithFiles, testcase_names)

    if test_funcs is not None:
        testcases = map(TestClassWithFiles, test_funcs)

    suite = unittest.TestSuite(testcases)

    return suite

def run_tests(TestClass, filenames, test_funcs=None):

    suite = make_test_suite(TestClass, filenames, test_funcs)
    unittest.TextTestRunner(verbosity=2).run(suite)
