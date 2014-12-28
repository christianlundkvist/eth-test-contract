import testcontract
from pyethereum import utils

# Test uses two wallet contracts and
# a namecoin contract

# namecoin funcs
REGISTER_KEY = 0
SET_VALUE = 2

# wallet funcs
SET_NAMEREG = 0
SEND_TO_ADDR = 1
SEND_TO_NAME = 2
TRANSFER_OWNERSHIP = 3

class TestWallet(testcontract.TestContract):

    def setUp(self):
        testcontract.TestContract.setUp(self)

        self.w0 = self.contracts[0]
        self.w1 = self.contracts[1]
        self.nc = self.contracts[2]

        # Fund wallets
        self.state.send(self.k0, self.w0, 10**18)
        self.state.send(self.k1, self.w1, 10**18)

    def test_send_to_addr(self):

        w0, w1 = self.w0, self.w1

        # Bal before
        balbefore0 = self.state.block.get_balance(w0)
        balbefore1 = self.state.block.get_balance(w1)

        # send from w0 to w1
        self.state.send(self.k0, w0, 0, funid=SEND_TO_ADDR, abi=['0x'+w1, 10**17])
        
        # Balance after
        balafter0 = self.state.block.get_balance(w0)
        balafter1 = self.state.block.get_balance(w1)

        self.assertEqual(balafter0, balbefore0 - 10**17)
        self.assertEqual(balafter1, balbefore1 + 10**17)

    def test_send_to_name(self):

        w0, w1, nc = self.w0, self.w1, self.nc
        getbal = self.state.block.get_balance

        # Register names in namecoin contract
        alice = '0x' + 'alice'.encode('hex')
        self.state.send(self.k0, nc, 0, funid=REGISTER_KEY, abi=[alice])
        self.state.send(self.k0, nc, 0, funid=SET_VALUE, abi=[alice, w0])

        bob = '0x' + 'bob'.encode('hex')
        self.state.send(self.k1, nc, 0, funid=REGISTER_KEY, abi=[bob])
        self.state.send(self.k1, nc, 0, funid=SET_VALUE, abi=[bob, w1])
        
        # Set namecoin contract addr in wallets
        self.state.send(self.k0, w0, 0, funid=SET_NAMEREG, abi=[nc])
        self.state.send(self.k1, w1, 0, funid=SET_NAMEREG, abi=[nc])

        # Bal before
        balbefore0 = getbal(w0)
        balbefore1 = getbal(w1)

        # send from alice to bob
        self.state.send(self.k0, w0, 0, funid=SEND_TO_NAME, abi=[bob, 10**17])
        
        self.assertEqual(getbal(w0), balbefore0 - 10**17)
        self.assertEqual(getbal(w1), balbefore1 + 10**17)

        # send from bob to alice
        self.state.send(self.k1, w1, 0, funid=SEND_TO_NAME, abi=[alice, 10**17])

        self.assertEqual(getbal(w0), balbefore0)
        self.assertEqual(getbal(w1), balbefore1)

def suite():
    files = ['contracts/wallet.se',
             'contracts/wallet.se',
             'contracts/namecoin.se']
    return testcontract.make_test_suite(TestWallet, files)

if __name__ == '__main__':
    files = ['contracts/wallet.se',
             'contracts/wallet.se',
             'contracts/namecoin.se']
    testcontract.run_tests(TestWallet, files)
