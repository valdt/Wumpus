from serverClasses import *
import socket

def newPayer():





port = 1337
host = ''
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(5)
while True:
    clientsocket, address = serversocket.accept()
    newPayer(clientsocket)
