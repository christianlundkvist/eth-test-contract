import unittest, testcontract

class TestArrays(testcontract.TestContract):

    def test_set_stored_array(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)

        in_arr = [1,2,3,4]
        ctr.set_stored_array(in_arr)
        out_arr = ctr.get_stored_array()
        self.assertEqual(in_arr, out_arr)

        empty_arr = []
        ctr.set_stored_array(empty_arr)
        out_empty_arr = ctr.get_stored_array()
        self.assertEqual(empty_arr, out_empty_arr)

    def test_hardcoded_array(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)

        out_arr = ctr.get_hardcoded_array_111()
        self.assertEqual(out_arr, [1,1,1])

    def test_get_stored_array_from_call(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)
        in_arr = [1,2,3,4]
        ctr.set_stored_array(in_arr)
        
        out_arr = ctr.get_stored_array_from_call()
        self.assertEqual(in_arr, out_arr)
        
        # When outsz is less than the size we
        # get a return value with the same
        # array size but padded with zeros
        out_arr2 = ctr.get_stored_array_from_call_with_outsz_minus_one()
        self.assertEqual(in_arr[:-1], out_arr2[:-1])
        self.assertEqual(0, out_arr2[-1])

def suite():
    return testcontract.make_test_suite(TestArrays, 'contracts/arrays.se')

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

