import random
from socket import *
import threading

#configure client
serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
DISCONNECT = 'DISCONNECT'
connected = True
message = 'login'


    
#send message
def send_message():
    global connected 
    while connected:
        message = input()
        clientSocket.send(message.encode())
        if message == DISCONNECT:
            connected = False
            break
    serverSocket.close()
    clientSocket.close()
    print("Connection closed")

def udp_listner(serverSocket):
    global connected 
    while connected:
        msg, clientAddress = serverSocket.recvfrom(2048)
        print(msg.decode())
    print("UDP listener closed")
        
def tcp_listner():
    global connected 
    while connected:
        message = clientSocket.recv(1024)
        print(message.decode())
    print("TCP listener closed")

def tcp_start():
    tcp = threading.Thread(target=tcp_listner)
    tcp.start()
    

# Configure UDP server
serverPort = random.randint(8000, 12003)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
udp = threading.Thread(target=udp_listner, args=(serverSocket,))
udp.start()



tcp_start()

send_message()




