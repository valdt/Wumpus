from serverHandler import *
from dungeonHandler import *
from player import *
import socket, pickle, threading

#This function runs in its own thread.
def acceptPlayers(serverHandler,dungeonHandler):
    while True:
        clientsocket, address = serverHandler.serverSocket.accept() #Accepting new players, in this program we only use clientsocket
        serverHandler.activePlayers.append(Player(serverHandler,clientsocket,dungeonHandler)) #Appending an new instance of the Players class, to ServerHandler's activePlayers list.
        dungeonHandler.playerNames = serverHandler.getPlayerNames()                           #This goes straight to handshaking the client/player in the Player class
def main():
    print("Loading....")
    serverHandler = ServerHandler('',1337) #creating a new instance of ServerHandler parsing ''  will make the server lissten to all tcp/ip sources.
    dungeonHandler = DungeonHandler(serverHandler) #passing the pointer of socket when creating the DungeonHandler instance.
    dungeonHandler.newDungeon() #Creating the field.
    threading.Thread(target=acceptPlayers, args=(serverHandler,dungeonHandler,)).start() #Threading the acceptPlayers thread.
    threading.Thread(target=dungeonHandler.dungeonStream, args=(serverHandler.activePlayers,)).start() #Threading the streaming fucntion, the function thats sends data to players


main() #If i need to comment this, you should not review this.
