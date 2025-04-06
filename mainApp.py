from User import user
from Sender import sender
from RSAEncryption import RSAEncryptor


if __name__ == "__main__":
    encryptor = RSAEncryptor()
    sender = sender(encryptor)
    user = user("Alice")
    message = "Hello, this is a secret message."
    recipient_name = user.getUsername()
    original_message, encrypted_name, signature = sender.sendMessage(message, recipient_name)

    # طباعة النتائج
    print("\n--- Test Output ---")
    print(f"Original message: {original_message}")
    print(f"Encrypted recipient: {encrypted_name}")
    print(f"Signature: {signature}")