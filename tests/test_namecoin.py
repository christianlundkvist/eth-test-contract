import testcontract
from pyethereum import utils

REGISTER_KEY = 0
TRANSFER_OWNERSHIP = 1
SET_VALUE = 2
GET_VALUE = 3
GET_OWNER = 4

class TestNameCoin(testcontract.TestContract):

    def test_register_key(self):

        self.state.send(self.k0, self.ctr, 0, funid=REGISTER_KEY, abi=['0xdeadbeef'])
        retval = self.state.send(self.k0, self.ctr, 0, funid=GET_OWNER, abi=['0xdeadbeef'])
        retaddr = utils.int_to_addr(retval[0])
        self.assertEqual(retaddr, self.a0)

    def test_set_value(self):

        self.state.send(self.k0, self.ctr, 0, funid=REGISTER_KEY, abi=['0xdeadbeef'])
        self.state.send(self.k0, self.ctr, 0, funid=SET_VALUE, abi=['0xdeadbeef', '0xabbababe'])
        retval = self.state.send(self.k0, self.ctr, 0, funid=GET_VALUE, abi=['0xdeadbeef'])
        self.assertEqual(retval[0], int('abbababe',16))

    def test_transfer_ownership(self):

        self.state.send(self.k0, self.ctr, 0, funid=REGISTER_KEY, abi=['0xdeadbeef'])
        self.state.send(self.k0, self.ctr, 0, funid=TRANSFER_OWNERSHIP, abi=['0xdeadbeef', '0x' + self.a1])
        retval = self.state.send(self.k0, self.ctr, 0, funid=GET_OWNER, abi=['0xdeadbeef'])
        retaddr = utils.int_to_addr(retval[0])
        self.assertEqual(retaddr, self.a1)

def suite():
    return testcontract.make_test_suite(TestNameCoin, 'contracts/namecoin.se')

if __name__ == '__main__':
    testcontract.run_tests(TestNameCoin, 'contracts/namecoin.se')
