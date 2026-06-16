import argparse
import getpass
from wallet.ethereum import EthereumWallet
from wallet.bitcoin import BitcoinWallet
from wallet.solana import SolanaWallet
from wallet.storage import SecretStorage


def main() -> None:
    parser = argparse.ArgumentParser(description="Crypto wallet CLI for Ethereum, Bitcoin, and Solana")
    parser.add_argument("--chain", choices=["ethereum", "bitcoin", "solana"], help="Blockchain network")
    parser.add_argument("--action", choices=["create", "import", "keypair", "sign-message", "sign-tx", "save", "load"], required=True)
    parser.add_argument("--mnemonic", help="Mnemonic phrase for importing a wallet")
    parser.add_argument("--message", help="Message to sign")
    parser.add_argument("--tx", help="JSON string transaction object for Ethereum")
    parser.add_argument("--to", help="Destination address for Bitcoin or Solana")
    parser.add_argument("--amount", help="Amount to transfer or fee")
    parser.add_argument("--password", help="Password for encrypted storage")
    parser.add_argument("--file", default="wallet.dat", help="Local storage file path")
    args = parser.parse_args()

    if args.action == "create":
        if args.chain == "ethereum":
            wallet = EthereumWallet.create()
        elif args.chain == "bitcoin":
            wallet = BitcoinWallet.create()
        else:
            wallet = SolanaWallet.create()
        print(wallet.keypair())
        return

    if args.action == "import":
        if not args.mnemonic:
            raise SystemExit("Mnemonic is required for import.")
        if args.chain == "ethereum":
            wallet = EthereumWallet.from_mnemonic(args.mnemonic)
        elif args.chain == "bitcoin":
            wallet = BitcoinWallet.from_mnemonic(args.mnemonic)
        else:
            wallet = SolanaWallet.from_mnemonic(args.mnemonic)
        print(wallet.keypair())
        return

    if args.action == "keypair":
        if not args.mnemonic:
            raise SystemExit("Mnemonic is required to derive keypair.")
        if args.chain == "ethereum":
            print(EthereumWallet.from_mnemonic(args.mnemonic).keypair())
        elif args.chain == "bitcoin":
            print(BitcoinWallet.from_mnemonic(args.mnemonic).keypair())
        else:
            print(SolanaWallet.from_mnemonic(args.mnemonic).keypair())
        return

    if args.action == "sign-message":
        if not args.mnemonic or not args.message:
            raise SystemExit("Mnemonic and message are required to sign a message.")
        if args.chain == "ethereum":
            print(EthereumWallet.from_mnemonic(args.mnemonic).sign_message(args.message))
        elif args.chain == "bitcoin":
            print(BitcoinWallet.from_mnemonic(args.mnemonic).sign_message(args.message))
        else:
            print(SolanaWallet.from_mnemonic(args.mnemonic).sign_message(args.message))
        return

    if args.action == "sign-tx":
        if args.chain == "ethereum":
            if not args.mnemonic or not args.tx:
                raise SystemExit("Mnemonic and tx JSON string are required to sign Ethereum transactions.")
            import json

            tx = json.loads(args.tx)
            print(EthereumWallet.from_mnemonic(args.mnemonic).sign_transaction(tx))
        elif args.chain == "bitcoin":
            if not args.mnemonic or not args.to or not args.amount:
                raise SystemExit("Mnemonic, to, and amount are required to create a Bitcoin transaction.")
            print(BitcoinWallet.from_mnemonic(args.mnemonic).create_transaction(args.to, float(args.amount)))
        else:
            if not args.mnemonic or not args.to or not args.amount:
                raise SystemExit("Mnemonic, to, and amount are required to create a Solana transfer.")
            print(SolanaWallet.from_mnemonic(args.mnemonic).create_transfer(args.to, int(args.amount)))
        return

    if args.action == "save":
        if not args.mnemonic or not args.chain:
            raise SystemExit("Mnemonic and chain are required to save wallet content.")
        password = args.password or getpass.getpass("Password: ")
        storage = SecretStorage(args.file)
        storage.save({"chain": args.chain, "mnemonic": args.mnemonic}, password)
        print({"status": "saved", "file": args.file})
        return

    if args.action == "load":
        password = args.password or getpass.getpass("Password: ")
        storage = SecretStorage(args.file)
        payload = storage.load(password)
        print(payload)
        return

    raise SystemExit("Unknown action")
