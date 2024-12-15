from cryptography.fernet import Fernet

# Generate and save encryption key (do this once and save securely)
def generateKey():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)