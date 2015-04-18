import testcontract
import unittest

# Test uses two wallet contracts and
# a namecoin contract

class TestWallet(testcontract.TestContract):

    def fund_wallets(self, state, w0, w1, value):

        state.send(self.k0, w0.address, value)
        state.send(self.k1, w1.address, value)

    def test_send_to_addr(self):

        s = self.reset_state()
        w0, w1, nc = self.reset_all_contracts(s)
        self.fund_wallets(s, w0, w1, 10**18)
        getbal = lambda x: s.block.get_balance(x.address)

        self.assertNotEqual(w0.address, w1.address)

        # Bal before
        balbefore0 = getbal(w0)
        balbefore1 = getbal(w1)

        self.assertEqual(balbefore0, 10**18)
        self.assertEqual(balbefore1, 10**18)

        # send from w0 to w1
        w0.send_to_addr(w1.address, 10**17)
        
        # Balance after
        self.assertEqual(getbal(w0), balbefore0 - 10**17)
        self.assertEqual(getbal(w1), balbefore1 + 10**17)

        # send from w1 to w0
        w1.send_to_addr(w0.address, 10**17, sender=self.k1)
        
        # Balance after
        self.assertEqual(getbal(w0), balbefore0)
        self.assertEqual(getbal(w1), balbefore1)


    def test_send_to_name(self):

        s = self.reset_state()
        w0, w1, nc = self.reset_all_contracts(s)
        self.fund_wallets(s, w0, w1, 10**18)
        getbal = lambda x: s.block.get_balance(x.address)


        # Bal before
        balbefore0 = getbal(w0)
        balbefore1 = getbal(w1)

        self.assertEqual(balbefore0, 10**18)
        self.assertEqual(balbefore1, 10**18)

        alice = int('alice'.encode('hex'), 16)
        bob = int('bob'.encode('hex'), 16)

        # Register names in namecoin contract
        nc.register(alice, sender=self.k0)
        nc.set_value(alice, w0.address, sender=self.k0)
        nc.register(bob, sender=self.k1)
        nc.set_value(bob, w1.address, sender=self.k1)
        
        # Set namecoin contract addr in wallets
        w0.set_namereg(nc.address, sender=self.k0)
        w1.set_namereg(nc.address, sender=self.k1)

        # send from alice to bob
        w0.send_to_name(bob, 10**17, sender=self.k0)
        
        self.assertEqual(getbal(w0), balbefore0 - 10**17)
        self.assertEqual(getbal(w1), balbefore1 + 10**17)

        # send from bob to alice
        w1.send_to_name(alice, 10**17, sender=self.k1)

        self.assertEqual(getbal(w0), balbefore0)
        self.assertEqual(getbal(w1), balbefore1)

def suite():
    files = ['contracts/wallet.se',
             'contracts/wallet.se',
             'contracts/namecoin.se']
    return testcontract.make_test_suite(TestWallet, files)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
