import socket
import threading
from cryptography.fernet import Fernet
HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
with open("../keys/secret.key", "rb") as f:
    key = f.read()
cipher = Fernet(key)

def receive():
    while True:
        try:
            encrypted_message = client.recv(1024)
            decrypted = cipher.decrypt(encrypted_message)
            print(".\nFriend:", decrypted.decode())
        except:
            print("Disconnected")
            client.close()
            break
def write():
    while True:
        message = input("You: ")
        encrypted = cipher.encrypt(message.encode())
        client.send(encrypted)
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()