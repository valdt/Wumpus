from serverHandler import *
from dungeonHandler import *
from player import *
import socket, pickle, threading

#This function runs in its own thread.
def acceptPlayers(serverHandler,dungeonHandler):
    while True:
        clientsocket, address = serverHandler.serverSocket.accept()
        serverHandler.activePlayers.append(Player(serverHandler,clientsocket,dungeonHandler))
def main():
    serverHandler = ServerHandler('',1337)
    dungeonHandler = DungeonHandler()
    dungeonHandler.newDungeon()
    acceptPlayersThread = threading.Thread(target=acceptPlayers, args=(serverHandler,dungeonHandler,)).start()
    time.sleep(4)
    dungeonStreamThread = threading.Thread(target=dungeonHandler.dungeonStream, args=(serverHandler.activePlayers,)).start()






main()
