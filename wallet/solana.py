from dataclasses import dataclass
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39WordsNum
from solana.publickey import PublicKey
from solana.system_program import TransferParams
from solana.transaction import Transaction
from solana.keypair import Keypair
from typing import Dict


@dataclass
class SolanaWallet:
    mnemonic: str
    path: str = "m/44'/501'/0'/0'"

    @classmethod
    def create(cls, words: int = 12) -> "SolanaWallet":
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        return cls(str(mnemonic))

    @classmethod
    def from_mnemonic(cls, mnemonic: str, path: str = "m/44'/501'/0'/0'") -> "SolanaWallet":
        return cls(mnemonic, path)

    def _seed(self) -> bytes:
        return Bip39SeedGenerator(self.mnemonic).Generate()

    def keypair(self) -> Dict[str, str]:
        bip44 = Bip44.FromSeed(self._seed(), Bip44Coins.SOLANA).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_bytes = bip44.PrivateKey().Raw().ToBytes()
        keypair = Keypair.from_seed(private_bytes)
        return {
            "address": str(keypair.public_key),
            "secret_key": private_bytes.hex(),
            "mnemonic": self.mnemonic,
        }

    def sign_message(self, message: str) -> Dict[str, str]:
        keypair = Keypair.from_secret_key(bytes.fromhex(self.keypair()["secret_key"]))
        signed = keypair.sign(message.encode("utf-8"))
        return {
            "message": message,
            "signature": signed.signature.hex(),
            "address": str(keypair.public_key),
        }

    def create_transfer(self, to_address: str, lamports: int) -> Dict[str, str]:
        keypair = Keypair.from_seed(bytes.fromhex(self.keypair()["secret_key"]))
        transaction = Transaction()
        transaction.add(
            TransferParams(
                from_pubkey=keypair.public_key,
                to_pubkey=PublicKey(to_address),
                lamports=lamports,
            )
        )
        transaction.sign(keypair)
        return {
            "raw_transaction": transaction.serialize().hex(),
            "from_address": str(keypair.public_key),
            "to_address": to_address,
            "lamports": lamports,
        }
