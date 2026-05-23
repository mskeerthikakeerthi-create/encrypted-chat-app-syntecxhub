from cryptography.fernet import Fernet
key = Fernet.generate_key()
with open("keys/secret.key", "wb") as file:
    file.write(key)
print("Secret Key Generated")