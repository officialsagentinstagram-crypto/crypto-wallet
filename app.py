from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def get_wallet_classes():
    from wallet.ethereum import EthereumWallet
    from wallet.bitcoin import BitcoinWallet
    from wallet.solana import SolanaWallet
    from wallet.storage import SecretStorage
    return EthereumWallet, BitcoinWallet, SolanaWallet, SecretStorage


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/wallet/create", methods=["POST"])
def create_wallet():
    data = request.json
    chain = data.get("chain", "ethereum")
    
    try:
        if chain == "ethereum":
            wallet = EthereumWallet.create()
        elif chain == "bitcoin":
            wallet = BitcoinWallet.create()
        elif chain == "solana":
            wallet = SolanaWallet.create()
        else:
            return jsonify({"error": "Unknown chain"}), 400
        
        kp = wallet.keypair()
        return jsonify(kp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wallet/import", methods=["POST"])
def import_wallet():
    data = request.json
    chain = data.get("chain")
    mnemonic = data.get("mnemonic")
    
    if not chain or not mnemonic:
        return jsonify({"error": "chain and mnemonic required"}), 400
    
    try:
        if chain == "ethereum":
            wallet = EthereumWallet.from_mnemonic(mnemonic)
        elif chain == "bitcoin":
            wallet = BitcoinWallet.from_mnemonic(mnemonic)
        elif chain == "solana":
            wallet = SolanaWallet.from_mnemonic(mnemonic)
        else:
            return jsonify({"error": "Unknown chain"}), 400
        
        kp = wallet.keypair()
        return jsonify(kp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wallet/sign-message", methods=["POST"])
def sign_message():
    data = request.json
    chain = data.get("chain")
    mnemonic = data.get("mnemonic")
    message = data.get("message")
    
    if not chain or not mnemonic or not message:
        return jsonify({"error": "chain, mnemonic, and message required"}), 400
    
    try:
        if chain == "ethereum":
            wallet = EthereumWallet.from_mnemonic(mnemonic)
        elif chain == "bitcoin":
            wallet = BitcoinWallet.from_mnemonic(mnemonic)
        elif chain == "solana":
            wallet = SolanaWallet.from_mnemonic(mnemonic)
        else:
            return jsonify({"error": "Unknown chain"}), 400
        
        sig = wallet.sign_message(message)
        return jsonify(sig)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wallet/save", methods=["POST"])
def save_wallet():
    data = request.json
    chain = data.get("chain")
    mnemonic = data.get("mnemonic")
    password = data.get("password")
    
    if not chain or not mnemonic or not password:
        return jsonify({"error": "chain, mnemonic, and password required"}), 400
    
    try:
        storage = SecretStorage("wallet.dat")
        storage.save({"chain": chain, "mnemonic": mnemonic}, password)
        return jsonify({"status": "saved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/wallet/load", methods=["POST"])
def load_wallet():
    data = request.json
    password = data.get("password")
    
    if not password:
        return jsonify({"error": "password required"}), 400
    
    try:
        storage = SecretStorage("wallet.dat")
        payload = storage.load(password)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
