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
            send("EXIT")
            break
        elif user_input.lower() == 'get_clients':
            send("GETC")
        else:
            send("CUSTOM " + user_input)

def send(msg):
    message = msg.encode()
    message_length = len(message)
    send_length = str(message_length).encode()
    send_length += b' ' * (HEADER - len(send_length))
    clientSocket.send(send_length)
    clientSocket.send(message)

#configue client
serverName = 'localhost'
serverPort = 12002
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_custom_messages()

clientSocket.close()
