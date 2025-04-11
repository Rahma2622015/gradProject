from RSAEncryption import RSAEncryptor
from AESEncryption import AESEncryptor

class EncryptionFactory:
    def __init__(self, method="RSA"):
        if method.upper() == "RSA":
            self.encryptor = RSAEncryptor()
        elif method.upper() == "AES":
            self.encryptor = AESEncryptor()
        else:
            raise ValueError("Unsupported encryption method")

    def get_encryptor(self):
        return self.encryptor
