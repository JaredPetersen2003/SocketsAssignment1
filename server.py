from socket import *
import selectors


# Accept incoming connections
def accept(sock, mask):
    conn, addr = sock.accept()  
    print("Client " + str(addr) + " connected!")
    print("Active client" + str(clients))
    conn.setblocking(False)
    # Register the socket to be monitored with the selector
    sel.register(conn, selectors.EVENT_READ, read)

# Read incoming messages
def read(conn, mask):
    data = conn.recv(1024)  
    if data:
        print(data)


#Configure Server
print("Setting up server")
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
serverSocket.setblocking(False)

clients = []
sel = selectors.DefaultSelector()
sel.register(serverSocket, selectors.EVENT_READ, accept) # Register socket to selector
print("Server ready")

def main():
    
    # Receive incoming messages
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == "__main__":
    main()
