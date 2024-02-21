from socket import *
import threading

#configure client
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
DISCONNECT = 'DISCONNECT'

message = 'login'



clientSocket.send(message.encode())


def udp_start():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print('The server is ready to receive')
    udp = threading.Thread(target=udp_listner, args=(serverSocket,))
    udp.start()

def udp_listner(serverSocket):
    while True:
        msg, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(),
        clientAddress)

#udp_start()

clientSocket.close()


