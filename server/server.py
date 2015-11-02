from serverHandler import *
from player import *
import socket, pickle, threading

def acceptPlayers(serverHandler):
    while True:
        clientsocket, address = serverHandler.serverSocket.accept()
        serverHandler.clientSocketList.append(Player(serverHandler,clientsocket))
        print("New connection established from {}".format(address))

def main():
    serverHandler = ServerHandler('',1337)
    acceptPlayersThread = threading.Thread(target=acceptPlayers, args=(serverHandler,)).start()






main()
