from RSAEncryption import RSAEncryptor

class sender:
    def __init__(self, encryptor: RSAEncryptor):
        self.encryptor = encryptor

    def encryptRecipientPart(self, recipient_name: str) -> bytes:
        return self.encryptor.encrypt(recipient_name)

    def signMessage(self, message: str) -> bytes:
        return self.encryptor.signData(message)

    def sendMessage(self, message: str, name: str):
        name = self.encryptRecipientPart(name)
        signature = self.signMessage(message)


        return message, name, signature