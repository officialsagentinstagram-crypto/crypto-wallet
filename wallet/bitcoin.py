from dataclasses import dataclass
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39WordsNum
from bit import Key
from typing import Dict


@dataclass
class BitcoinWallet:
    mnemonic: str
    path: str = "m/44'/0'/0'/0/0"

    @classmethod
    def create(cls, words: int = 12) -> "BitcoinWallet":
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        return cls(str(mnemonic))

    @classmethod
    def from_mnemonic(cls, mnemonic: str, path: str = "m/44'/0'/0'/0/0") -> "BitcoinWallet":
        return cls(mnemonic, path)

    def _seed(self) -> bytes:
        return Bip39SeedGenerator(self.mnemonic).Generate()

    def keypair(self) -> Dict[str, str]:
        bip44 = Bip44.FromSeed(self._seed(), Bip44Coins.BITCOIN).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = bip44.PrivateKey().Raw().ToHex()
        key = Key.from_hex(private_key)
        return {
            "address": key.address,
            "wif": key.to_wif(),
            "private_key": private_key,
            "mnemonic": self.mnemonic,
        }

    def sign_message(self, message: str) -> Dict[str, str]:
        key = Key.from_hex(self.keypair()["private_key"])
        signature = key.sign(message)
        return {
            "message": message,
            "signature": signature.hex(),
            "address": key.address,
        }

    def create_transaction(self, to_address: str, amount: float, fee: Optional[float] = None) -> Dict[str, str]:
        key = Key.from_hex(self.keypair()["private_key"])
        tx_hex = key.create_transaction([(to_address, amount, 'btc')], fee=fee)
        return {
            "transaction_hex": tx_hex,
            "from_address": key.address,
            "to_address": to_address,
            "amount": amount,
        }
