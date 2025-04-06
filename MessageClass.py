from Sender import sender

class Message:
    def __init__(self, sender: sender, encrypted_content: str, signature: str, receiver_username: str = ""):
        self.sender = s
        self.encrypted_content = encrypted_content
        self.signature = signature
        self.receiver_username = receiver_username

    def get_encrypted_content(self) -> str:
        return self.encrypted_content

    def get_signature(self) -> str:
        return self.signature

    def get_receiver_username(self) -> str:
        return self.receiver_username

    def set_encrypted_content(self, content: str):
        self.encrypted_content = content

    def set_signature(self, signature: str):
        self.signature = signature

    def set_receiver_username(self, username: str):
        self.receiver_username = username
