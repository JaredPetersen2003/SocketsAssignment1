from socket import *
import selectors
import threading

# Define a dictionary to store the state of each client
client_states = {}
chatroom = []
    

# Accept incoming connections
def accept(sock, mask):
    conn, addr = sock.accept()  
    clients.append(conn)
    
    print("Client " + str(addr) + " connected!")
    print("Active client" + str(clients))
    # TODO better way to handle an active list of clients
    conn.setblocking(False)
 
    

# Read incoming messages
def read(conn, mask):
    while True:
        data = conn.recv(HEADER)  # Receive the message length header
        if data:
            msg_length = int(data)  # Unpack the message length as an unsigned integer
            full_data = b""
            while len(full_data) < msg_length:
                remaining_bytes = min(msg_length - len(full_data), 1024)
                try:
                    data = conn.recv(remaining_bytes)
                except:
                    print("Error receiving message")
             
                if not data:
                    break
                full_data += data

            if len(full_data) == msg_length:
                handle_received_message(full_data, conn)
            else:
                print("Incomplete message received")
    
    
            
def handle_received_message(msg, conn):
        # client disconnected
        msg = msg.decode()
        print("Received message: " + msg)
        if msg == "DISCONNECT":
            print("Client " + str(conn.getpeername()) + " disconnected!")
            clients.remove(conn)
            conn.close()
            
            
        if msg == "LISTENING":
            print("Client " + str(conn.getpeername()) + " is listening!")
            client_states[conn] = "listening"
            
        if msg == "CHATTING":
            print("Client " + str(conn.getpeername()) + " is chatting!")
            client_states[conn] = "chatting"
            
        #Send list of clients
        if msg == "GETC":
            print("GET request received")
            active_clients = [(str(client.getpeername()) + " " + client_states[client])  for client in clients if client.fileno() != conn.fileno()]
            conn.send("\n".join(active_clients).encode())
            
        #Connect to client
        if msg.split(' ')[0] == "CONN":
            print("Connection request received")
            # TODO implement 
            for client in clients:
                if (client.getpeername() == (msg.split(' ')[1], int(msg.split(' ')[2]))):
                    
                    # Stops connection request if client is not listening
                    if (client_states[client] != "listening"):
                        print("Client is not listening")
                        conn.send("Client is not listening".encode())
                        break
                    
                    # REQ UDP details
                    print("Connection request sent")
                    client.send(("REQ " + conn.getpeername()[0] + " " + str(conn.getpeername()[1]) + " " + msg.split(' ')[3]).encode()) 
                    conn.send("Connection request sent".encode())
                    break
            
            
        # Receive UDP port from client
        if msg.split(' ')[0] == "UDP":
            print("UDP port received")
            for client in clients:
                if client.getpeername() == (msg.split(' ')[2], int(msg.split(' ')[3])):
                    print("UDP port sent")
                    client.send(("SUCC " + conn.getpeername()[0] + " " + msg.split(' ')[1]).encode())
                    client_states[conn] = "chatting"
                    break
                
        if msg.split(' ')[0] == "CHAT":
            if conn not in chatroom:
                chatroom.append(conn)
                client_states[conn] = "chatting"
                
        
                


# Message header length
HEADER = 64

#Configure Server
print("Setting up server")
serverPort = 12002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)


# Keep a list of clients
clients = []



UDPSocket = socket(AF_INET, SOCK_DGRAM)

print("Server ready")

def main():
    
    # Receive incoming messages
    while True:
        conn, addr = serverSocket.accept()
        client = threading.Thread(target=read, args=(conn, addr))
        client.start()
        clients.append(conn)
    
        print("Client " + str(addr) + " connected!")
        client_states[conn] = "online"
    
        

if __name__ == "__main__":
    main()
