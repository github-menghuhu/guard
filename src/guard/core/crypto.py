import base64
import hashlib

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


class PasswordHasher:
    def __init__(self) -> None:
        self.password_hash = PasswordHash(
            (
                Argon2Hasher(),
                # BcryptHasher(), # 预留
            )
        )

    def verify_and_update(
        self, plain_password, hashed_password
    ) -> tuple[bool, str | None]:
        return self.password_hash.verify_and_update(plain_password, hashed_password)

    def hash(self, password) -> str:
        return self.password_hash.hash(password)


password_hasher = PasswordHasher()


class SecureRandomGenerator:
    def hash_code_verifier(
        self, code_verifier: str, code_challenge_method: str = "S256"
    ) -> str:
        """目前只支持S256"""
        h = hashlib.sha256()
        h.update(code_verifier.encode("utf-8"))
        hashed = h.digest()
        encoded = base64.urlsafe_b64encode(hashed).decode("utf-8")
        return encoded.rstrip("=")


secure_random_generator = SecureRandomGenerator()
