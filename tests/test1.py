
from cryptography.fernet import Fernet
a = Fernet.generate_key()
print(a.decode("utf-8"))