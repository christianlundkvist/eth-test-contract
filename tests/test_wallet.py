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

    def fund_wallets(self, state, w0, w1, value):

        state.send(self.k0, w0, value)
        state.send(self.k1, w1, value)

    def test_send_to_addr(self):

        s = self.reset_state()
        w0, w1, nc = self.reset_all_contracts(s)
        self.fund_wallets(s, w0, w1, 10**18)

        # Bal before
        balbefore0 = s.block.get_balance(w0)
        balbefore1 = s.block.get_balance(w1)

        self.assertEqual(balbefore0, 10**18)
        self.assertEqual(balbefore1, 10**18)

        # send from w0 to w1
        s.send(self.k0, w0, 0, funid=SEND_TO_ADDR, abi=['0x'+w1, 10**17])
        
        # Balance after
        balafter0 = s.block.get_balance(w0)
        balafter1 = s.block.get_balance(w1)

        self.assertEqual(balafter0, balbefore0 - 10**17)
        self.assertEqual(balafter1, balbefore1 + 10**17)

    def test_send_to_name(self):

        s = self.reset_state()
        w0, w1, nc = self.reset_all_contracts(s)
        self.fund_wallets(s, w0, w1, 10**18)
        getbal = s.block.get_balance

        # Bal before
        balbefore0 = getbal(w0)
        balbefore1 = getbal(w1)

        self.assertEqual(balbefore0, 10**18)
        self.assertEqual(balbefore1, 10**18)

        # Register names in namecoin contract
        alice = '0x' + 'alice'.encode('hex')
        s.send(self.k0, nc, 0, funid=REGISTER_KEY, abi=[alice])
        s.send(self.k0, nc, 0, funid=SET_VALUE, abi=[alice, w0])

        bob = '0x' + 'bob'.encode('hex')
        s.send(self.k1, nc, 0, funid=REGISTER_KEY, abi=[bob])
        s.send(self.k1, nc, 0, funid=SET_VALUE, abi=[bob, w1])
        
        # Set namecoin contract addr in wallets
        s.send(self.k0, w0, 0, funid=SET_NAMEREG, abi=[nc])
        s.send(self.k1, w1, 0, funid=SET_NAMEREG, abi=[nc])

        # send from alice to bob
        s.send(self.k0, w0, 0, funid=SEND_TO_NAME, abi=[bob, 10**17])
        
        self.assertEqual(getbal(w0), balbefore0 - 10**17)
        self.assertEqual(getbal(w1), balbefore1 + 10**17)

        # send from bob to alice
        s.send(self.k1, w1, 0, funid=SEND_TO_NAME, abi=[alice, 10**17])

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
