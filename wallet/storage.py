import base64
import json
import os
from dataclasses import dataclass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


@dataclass
class SecretStorage:
    path: str

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    def save(self, payload: dict, password: str) -> None:
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        token = Fernet(key).encrypt(json.dumps(payload).encode("utf-8"))
        with open(self.path, "wb") as handle:
            handle.write(salt + token)

    def load(self, password: str) -> dict:
        with open(self.path, "rb") as handle:
            data = handle.read()
        salt = data[:16]
        token = data[16:]
        key = self._derive_key(password, salt)
        decrypted = Fernet(key).decrypt(token)
        return json.loads(decrypted.decode("utf-8"))
