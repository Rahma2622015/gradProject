from cryptoManager import EncryptionFactory
from MessageClass import Message
from User import user
import re

class sender(user):
    def __init__(self, encryption_factory: EncryptionFactory, email, password):
        encryptor_instance = encryption_factory.get_encryptor()
        super().__init__(encryptor_instance, email, password)
        self.encryptor = encryptor_instance
        self.sessions = []
        self.logged_in = False

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = r"(^[A-Za-z0-9]+@[A-Za-z0-9]+\.(com|net))"
        return re.match(email_regex, email) is not None

    def login(self, email, password):
        if not self.is_valid_email(email):
            print("Invalid email format.")
            return False
        if self.email == email and self.password == password and self.password.strip() != "":
            self.logged_in = True
            return True
        else:
            print("Invalid email or password.")
            return False

    def create_message(self, content, receiver):
        if not self.logged_in:
            return None
        encrypted_content = self.encryptor.encrypt(content)
        encrypted_receiver_name = self.encryptor.encrypt(receiver)
        signature = self.encryptor.signData(receiver)
        message = Message(encrypted_content, signature, encrypted_receiver_name)
        self.sessions.append(message)
        return message

    def send_message(self):
        if not self.sessions:
            return "", "", "", ""
        message = self.sessions[-1]
        return self.encryptor, message.get_encrypted_content(), message.get_signature(), message.get_receiver_username()
