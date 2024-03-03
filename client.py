import random
from socket import *
import threading

  
#send message
def send_message():
    global connected 
    global clientUDPPort
    while connected:
        message = input()
        
        if message == DISCONNECT:
            connected = False
        
        if message.split(' ')[0] == "MESS":
            serverSocket.sendto(message[5:].encode(), clientUDPPort)
            continue
        
        if message.split(' ')[0] == "STOP":
            serverSocket.sendto("STOP".encode(), clientUDPPort)
            clientUDPPort = (0, 0)
            send("LISTENING")
            continue
        
        if message.split(' ')[0] == "CONN":
            message += " " + str(UDPPort)
            send(message)
            continue
        
        send(message)
    serverSocket.close()
    clientSocket.close()
    print("Connection closed")
    
def send(msg):
    message = msg.encode()
    message_length = len(message)
    send_length = str(message_length).encode()
    send_length += b' ' * (HEADER - len(send_length))
    clientSocket.send(send_length)
    clientSocket.send(message)

def udp_listner(serverSocket):
    global connected 
    global clientUDPPort
    while connected:
        msg, clientAddress = serverSocket.recvfrom(2048)
        if msg.decode() == "STOP":
            send("LISTENING")
            print(str(clientUDPPort) + " has stopped chatting, now listening")
            clientUDPPort = (0, 0)
            continue
        
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
            msg = "UDP " + str(UDPPort) + " " + message.decode().split(' ')[1] + " " + message.decode().split(' ')[2]
            send(msg)
            clientUDPPort = (message.decode().split(' ')[1], int(message.decode().split(' ')[3]))
            continue
            
        #UDP port received
        if (message.decode().split(' ')[0] == "SUCC"):
            print("UDP port received")
            clientUDPPort = (message.decode().split(' ')[1], int(message.decode().split(' ')[2]))
            serverSocket.sendto(("Now Chatting on " + str(UDPPort)).encode(), clientUDPPort)
            send("CHATTING")
            
            
        
    print("TCP listener closed")

def tcp_start():
    tcp = threading.Thread(target=tcp_listner)
    tcp.start()

#
HEADER = 64
    
#configure client
serverName = 'localhost'
serverPort = 12002
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




