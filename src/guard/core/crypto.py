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
