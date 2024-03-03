from socket import *
import selectors

# Define a dictionary to store the state of each client
client_states = {}


def handle_login(conn, mask):
    data = conn.recv(1024)
    if data:
        print(data.decode()[:3])
        if data.decode().split(' ')[0] == "login":
            print("Login request received")
            # TODO implement login
            conn.send("Login successful".encode())
            sel.unregister(conn)
            sel.register(conn, selectors.EVENT_READ, read)
            # Set the state of the client to "online"
            client_states[conn] = "online"
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
        # client disconnected
        if data.decode() == "DISCONNECT":
            print("Client " + str(conn.getpeername()) + " disconnected!")
            sel.unregister(conn)
            clients.remove(conn)
            conn.close()
            
        if data.decode() == "LISTENING":
            print("Client " + str(conn.getpeername()) + " is listening!")
            client_states[conn] = "listening"
            
        if data.decode() == "CHATTING":
            print("Client " + str(conn.getpeername()) + " is chatting!")
            client_states[conn] = "chatting"
            
        #Send list of clients
        if data.decode() == "GETC":
            print("GET request received")
            active_clients = [(str(client.getpeername()) + " " + client_states[client])  for client in clients if client.fileno() != conn.fileno()]
            conn.send("\n".join(active_clients).encode())
            
        #Connect to client
        if data.decode().split(' ')[0] == "CONN":
            print("Connection request received")
            # TODO implement 
            for client in clients:
                if (client.getpeername() == (data.decode().split(' ')[1], int(data.decode().split(' ')[2]))):
                    
                    # Stops connection request if client is not listening
                    if (client_states[client] != "listening"):
                        print("Client is not listening")
                        conn.send("Client is not listening".encode())
                        break
                    
                    # REQ UDP details
                    print("Connection request sent")
                    client.send(("REQ " + conn.getpeername()[0] + " " + str(conn.getpeername()[1])).encode()) 
                    conn.send("Connection request sent".encode())
                    break
            
            
        # Receive UDP port from client
        if data.decode().split(' ')[0] == "UDP":
            print("UDP port received")
            for client in clients:
                if client.getpeername() == (data.decode().split(' ')[2], int(data.decode().split(' ')[3])):
                    print("UDP port sent")
                    client.send(("CONN " + conn.getpeername()[0] + " " + data.decode().split(' ')[1]).encode())
                    client_states[conn] = "chatting"
                    break


#Configure Server
print("Setting up server")
serverPort = 12008
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
serverSocket.setblocking(False)

# Keep a list of clients
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
