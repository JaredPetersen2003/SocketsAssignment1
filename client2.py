import random
from socket import *
import threading

def receive_messages():
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            print("Received message from server: " + message)
        except:
            break

def send_custom_messages():
    while True:
        user_input = input("Enter custom message for client2: ")
        if user_input.lower() == 'exit':
            break
        else:
            clientSocket.send(user_input.encode())

#configue client
serverName = 'localhost'
serverPort = 12002
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_custom_messages()

clientSocket.close()
