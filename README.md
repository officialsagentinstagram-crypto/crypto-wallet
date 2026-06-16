# Crypto Wallet CLI

A Python command-line wallet supporting Ethereum, Bitcoin, and Solana.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Create a new wallet:

```bash
python -m wallet --chain ethereum --action create
```

Import from mnemonic:

```bash
python -m wallet.cli --chain bitcoin --action import --mnemonic "your twelve word phrase"
```

Sign a message:

```bash
python -m wallet.cli --chain solana --action sign-message --mnemonic "..." --message "hello"
```

Sign a transaction:

```bash
python -m wallet.cli --chain ethereum --action sign-tx --mnemonic "..." --tx '{"nonce":0,"gasPrice":1000000000,"gas":21000,"to":"0x...","value":0}'
```

Save encrypted wallet data:

```bash
python -m wallet.cli --chain ethereum --action save --mnemonic "..." --file wallet.dat
```

Load encrypted wallet data:

```bash
python -m wallet.cli --action load --file wallet.dat
```

## Notes

- The wallet only derives the first standard address for each chain.
- The `save` command encrypts mnemonic data with a password.
- The `sign-tx` flow only builds raw payloads; broadcasting requires an external node or API.
