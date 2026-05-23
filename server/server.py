import socket
import threading
from cryptography.fernet import Fernet
HOST = '0.0.0.0'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clients = []
with open("../keys/secret.key", "rb") as f:
    key = f.read()
cipher = Fernet(key)
print("[SERVER STARTED]")

def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            encrypted_message = client.recv(1024)
            decrypted = cipher.decrypt(encrypted_message)
            print("Message:", decrypted.decode())
            with open("../logs/chat.log", "a") as log:
                log.write(decrypted.decode() + "\n")
            broadcast(encrypted_message)
        except:
            clients.remove(client)
            client.close()
            break
while True:
    client, address = server.accept()
    print(f"[CONNECTED] {str(address)}")
    clients.append(client)
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()