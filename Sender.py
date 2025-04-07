from cryptoManager import RSAEncryptor
from MessageClass import Message
from User import user
import re

class sender(user):
    def __init__(self,encryptor:RSAEncryptor,email, password):
        super.__init__(encryptor.public_key)
        self.encryptor = encryptor
        self.sent_messages = []
        self.email=email
        self.password=password
        self.logged_in = False
        self.users_list = []


    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = r"(^[A-Za-z0-9]+@[A-Za-z0-9]+\.(com|net))"
        return re.match(email_regex, email) is not None


    def login(self, email, password):
        if not self.is_valid_email(email):
            print("Invalid email format.")
            return False

        if self.email == email:
            self.logged_in = True
            print(f"Login successful for {self.email}!")
            return True
        else:
            print("Invalid email.")
            return False

    def create_message(self, content, receiver):
        if not self.logged_in:
            print("You must login first.")
            return None

        encrypted_content = self.encryptor.encrypt(content)
        encrypted_reciver_name = self.encryptor.encrypt(receiver)
        signature = self.encryptor.signData(encrypted_content)
        message = Message(encrypted_content, signature, encrypted_reciver_name)
        self.sent_messages.append(message)
        return message

    def send_message(self, message: Message):
            return message.get_encrypted_content(), message.get_signature(), message.get_receiver_username()

