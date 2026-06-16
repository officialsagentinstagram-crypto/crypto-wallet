from dataclasses import dataclass
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39WordsNum
from eth_account import Account
from eth_account.messages import encode_defunct
from typing import Dict, Optional


@dataclass
class EthereumWallet:
    mnemonic: str
    path: str = "m/44'/60'/0'/0/0"

    @classmethod
    def create(cls, words: int = 12) -> "EthereumWallet":
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        return cls(str(mnemonic))

    @classmethod
    def from_mnemonic(cls, mnemonic: str, path: str = "m/44'/60'/0'/0/0") -> "EthereumWallet":
        return cls(mnemonic, path)

    def _seed(self) -> bytes:
        return Bip39SeedGenerator(self.mnemonic).Generate()

    def keypair(self) -> Dict[str, str]:
        bip44 = Bip44.FromSeed(self._seed(), Bip44Coins.ETHEREUM).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = bip44.PrivateKey().Raw().ToHex()
        acct = Account.from_key(private_key)
        return {
            "address": acct.address,
            "private_key": private_key,
            "public_key": acct._key_obj.public_key.to_hex(),
            "mnemonic": self.mnemonic,
        }

    def sign_message(self, message: str) -> Dict[str, str]:
        acct = Account.from_key(self.keypair()["private_key"])
        signed = Account.sign_message(encode_defunct(text=message), acct.key)
        return {
            "message": message,
            "signature": signed.signature.hex(),
            "address": acct.address,
        }

    def sign_transaction(self, transaction: Dict, chain_id: int = 1) -> Dict[str, str]:
        acct = Account.from_key(self.keypair()["private_key"])
        tx = {**transaction, "chainId": chain_id}
        signed = acct.sign_transaction(tx)
        return {
            "raw_transaction": signed.rawTransaction.hex(),
            "hash": signed.hash.hex(),
        }
