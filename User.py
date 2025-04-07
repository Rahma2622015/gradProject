from cryptoManager import RSAEncryptor
class user:
    def __init__(self, encryptor:RSAEncryptor):
        self.publicKey=encryptor.public_key

    def getPublicKey(self):
        return self.publicKey