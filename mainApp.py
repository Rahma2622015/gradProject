from RSAEncryption import RSAEncryptor
from Sender import sender
from User import user

if __name__ == "__main__":
    # Step 1: Setup the RSA encryptor
    encryptor = RSAEncryptor()

    # Step 2: Get input from the user for email and password
    sender_email = input("Please enter your email: ")
    sender_password = input("Please enter your password: ")

    # Step 3: Create a sender with email and password
    my_sender = sender(encryptor, sender_email, sender_password)

    # Step 4: Print the email and password
    print("\n--- User Info ---")
    print(f"Email: {sender_email}")
    print(f"Password: {sender_password}")

    # Input message
    message = input("Enter a message to encrypt: ")

    # Encrypt the message
    encrypted_message = encryptor.encrypt(message)
    print("\n Encrypted Message (bytes):", encrypted_message)

    # Decrypt the message
    decrypted_message = encryptor.decrypt(encrypted_message)
    print("\n Decrypted Message:", decrypted_message)

    # Sign the original message
    signature = encryptor.signData(message)
    print("\n Signature (bytes):", signature)
    # Manually insert the encrypted message here
    encrypted_bytes = b'J\x1d-T\xed\x1cm\x08\x91u*\xb2\xb7\xeb\x86)...'

    try:
        decrypted = encryptor.decrypt(encrypted_bytes)
        print("Decrypted Message:", decrypted)
    except Exception as e:
        print("Failed to decrypt:", str(e))


    my_sender.login(sender_email, sender_password)






