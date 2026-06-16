import unittest
from wallet.ethereum import EthereumWallet
from wallet.bitcoin import BitcoinWallet
from wallet.solana import SolanaWallet


class WalletTest(unittest.TestCase):
    def test_ethereum_keypair(self):
        wallet = EthereumWallet.create()
        kp = wallet.keypair()
        self.assertIn("address", kp)
        self.assertTrue(kp["address"].startswith("0x"))

    def test_bitcoin_keypair(self):
        wallet = BitcoinWallet.create()
        kp = wallet.keypair()
        self.assertIn("address", kp)
        self.assertTrue(kp["address"].startswith("1") or kp["address"].startswith("3") or kp["address"].startswith("bc1"))

    def test_solana_keypair(self):
        wallet = SolanaWallet.create()
        kp = wallet.keypair()
        self.assertIn("address", kp)
        self.assertEqual(len(kp["address"]), 44)


if __name__ == "__main__":
    unittest.main()
