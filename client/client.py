import pickle, socket, sys
from PacketHandler import *
from clientClasses import *

def listenIncoming(socket, packetHandler):
    if socket:
        print("socket")
        try:
            data = pickle.load(socket.recv(10000))
            print("data tried and succeeded")
            if data != "":
                print(data)
                if data[0] == "dungeonUpdate":
                    packetHandler.dungeonHandler.update(data)

                elif data[0] == "wumpusUpdate":
                    packetHandler.wu.update(data)
        except Exception:
            print("exception")

def initSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def main():
    clientSocket = initSocket('192.168.1.108', 1337)
    packetHandler = PacketHandler()
    print("initiated")
    while True:
        listenIncoming(clientSocket, packetHandler)

main()
