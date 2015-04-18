import unittest, testcontract
from ethereum import utils

class TestNameCoin(testcontract.TestContract):

    def test_register_key(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)

        key = 1111

        # Explicit default values of sender, value
        ctr.register(key, sender=self.k0, value=0)
        
        retval = ctr.get_owner(key)
        retaddr = utils.int_to_addr(retval)

        self.assertEqual(retaddr, self.a0)

    def test_set_value(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)

        key = 1111
        value = 6789

        ctr.register(key)
        ctr.set_value(key, value)
        retval = ctr.get_value(key)

        self.assertEqual(retval, value)

    def test_transfer_ownership(self):

        s = self.reset_state()
        ctr = self.reset_contract(s, 0, self.k0)

        key = 1111
        value = 6789

        ctr.register(key)
        ctr.transfer_ownership(key, self.a1)
        retval = ctr.get_owner(key)
        retaddr = utils.int_to_addr(retval)
        self.assertEqual(retaddr, self.a1)

        ctr.set_value(key, value, sender=self.k1)
        retval1 = ctr.get_value(key)
        self.assertEqual(retval1, value)

def suite():
    return testcontract.make_test_suite(TestNameCoin, 'contracts/namecoin.se')

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

