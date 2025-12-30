import re

# class ClientValidator:
#     def validate_id(self, id_: UUID) -> bool:
#         return True


def validate_login_password(password: str) -> str:
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")  # noqa: TRY003
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number")  # noqa: TRY003
    if not re.search(r"[\W_]", password):
        raise ValueError("Password must contain at least one special character")  # noqa: TRY003
    return password
