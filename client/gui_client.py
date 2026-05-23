import socket
import threading
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import scrolledtext
HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)
client.connect((HOST,PORT))
with open("../keys/secret.key", "rb") as f:
    key = f.read()
cipher = Fernet(key)
window = tk.Tk()
window.title("Secure Chat App")
window.geometry("500x500")
chat_area = scrolledtext.ScrolledText(window)
chat_area.pack(padx=10, pady=10)
chat_area.config(state='disabled')
message_box = tk.Entry(window, width=40)
message_box.pack(side=tk.LEFT, padx=10, pady=10)

def receive_messages():
    while True:
        try:
            encrypted_message = client.recv(1024)
            decrypted_message = cipher.decrypt(encrypted_message).decode()
            chat_area.config(state='normal')
            chat_area.insert(tk.END, "Friend: " + decrypted_message + "\n")
            chat_area.config(state='disabled')

        except:
            break

def send_message():
    message = message_box.get()
    encrypted_message = cipher.encrypt(message.encode())
    client.send(encrypted_message)
    chat_area.config(state='normal')
    chat_area.insert(tk.END, "You: " + message + "\n")
    chat_area.config(state='disabled')
    message_box.delete(0, tk.END)
send_button = tk.Button(window, text="Send",
command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()
window.mainloop()