import random
from socket import *
import threading

  
#send message
def send_message():
    global connected 
    while connected:
        message = input()
        
        if message == DISCONNECT:
            connected = False
        
        if message.split(' ')[0] == "MESS":
            serverSocket.sendto(message.split(' ')[1].encode(), clientUDPPort)
            continue
        
        clientSocket.send(message.encode())
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
    global clientUDPPort
    while connected:
        message = clientSocket.recv(1024)
        print(message.decode())
        #Connection request received, send UDP port to client
        if (message.decode().split(' ')[0] == "REQ"):
            clientSocket.send(("UDP " + str(UDPPort) + " " + message.decode().split(' ')[1] + " " + message.decode().split(' ')[2]).encode())
            clientUDPPort = (message.decode().split(' ')[1], int(message.decode().split(' ')[2]))
            clientSocket.send("CHATTING".encode())
            
        #UDP port received
        if (message.decode().split(' ')[0] == "CONN"):
            print("UDP port received")
            #TODO implement P2P communication
            clientUDPPort = (message.decode().split(' ')[1], int(message.decode().split(' ')[2]))
            serverSocket.sendto(("Now Chatting on " + str(UDPPort)).encode(), clientUDPPort)
            clientSocket.send("CHATTING".encode())
        
    print("TCP listener closed")

def tcp_start():
    tcp = threading.Thread(target=tcp_listner)
    tcp.start()
    
#configure client
serverName = 'localhost'
serverPort = 12005
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
DISCONNECT = 'DISCONNECT'
connected = True


# Configure UDP server
UDPPort = random.randint(8000, 12003)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', UDPPort))
print('The server is ready to receive')
udp = threading.Thread(target=udp_listner, args=(serverSocket,))
udp.start()

clientUDPPort =  (0, 0)


tcp_start()

send_message()




