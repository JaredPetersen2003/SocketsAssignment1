from socket import *
import selectors


def handle_login(conn, mask):
    data = conn.recv(1024)
    if data:
        print(data.decode()[:3])
        if data.decode()[:5] == "login":
            print("Login request received")
            # TODO implement login
            conn.send("Login successful".encode())
            sel.unregister(conn)
            sel.register(conn, selectors.EVENT_READ, read)
        if data.decode()[:5] == "regis":
            print("Registration request received")
            # TODO implement registration
            conn.send("Registration successful".encode())
            sel.unregister(conn)
            sel.register(conn, selectors.EVENT_READ, read)
    

# Accept incoming connections
def accept(sock, mask):
    conn, addr = sock.accept()  
    clients.append(conn)
    
    print("Client " + str(addr) + " connected!")
    print("Active client" + str(clients))
    # TODO better way to handle an active list of clients
    conn.setblocking(False)
    # Register the socket to be monitored with the selector
    sel.register(conn, selectors.EVENT_READ, handle_login)

# Read incoming messages
def read(conn, mask):
    data = conn.recv(1024)  
    if data:
        print(data)
        if data.decode() == "DISCONNECT":
            print("Client " + str(conn.getpeername()) + " disconnected!")
            sel.unregister(conn)
            clients.remove(conn)
            conn.close()
            
        #Send list of clients
        if data.decode() == "GETC":
            print("GET request received")
            active_clients = [str(client.getpeername()) for client in clients if client.fileno() != conn.fileno()]
            conn.send("\n".join(active_clients).encode())


#Configure Server
print("Setting up server")
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
serverSocket.setblocking(False)

clients = []
sel = selectors.DefaultSelector()
sel.register(serverSocket, selectors.EVENT_READ, accept) # Register socket to selector


UDPSocket = socket(AF_INET, SOCK_DGRAM)

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
