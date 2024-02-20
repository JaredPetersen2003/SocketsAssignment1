from socket import *

#configure client
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = 'login'
clientSocket.send(message.encode())



