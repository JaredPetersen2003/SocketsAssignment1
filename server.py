from socket import *
import threading

#Configure Server
print("Setting up server")
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Server ready")
clients = []

def main():
    
    while True:
        #Accept client connection
        connectionSocket, addr = serverSocket.accept()
        clients.append(connectionSocket)
        
        #Start client thread
        client = threading.Thread(target=handle_client, args=(connectionSocket,addr))
        client.start()
        print("Client " + str(addr) + " connected!")
        print("Active client" + str(clients))

        

def handle_client(connectionSocket, addr):
    connected = True

    while connected:
        #Receive message
        message = connectionSocket.recv(1024).decode()

        if (message == "DISCONNECT"):
            connected = False
            continue
        

    connectionSocket.close()

if __name__ == "__main__":
    main()
