from socket import *
import threading

def main():
    #Configure Server
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("Server ready")
    clients = []

    while True:
        #Accept client connection
        connectionSocket, addr = serverSocket.accept()
        clients.append(connectionSocket)
        
        #Receive message
        message = connectionSocket.recv(1024).decode()

        connectionSocket.close()

if __name__ == "__main__":
    main()
