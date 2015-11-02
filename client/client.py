import pickle, socket, sys, threading
from PacketHandler import *
from clientClasses import *

def listenIncoming(clientSocket, packetHandler):
    if clientSocket:
        try:
            data = pickle.loads(clientSocket.recv(10000))
            if data != "":
                print(data)
                if data[0] == "dungeonUpdate":
                    packetHandler.dungeonHandler.update(data)

                elif data[0] == "wumpusUpdate":
                    packetHandler.wu.update(data)

                elif data[0] == "handshake":
                    x = ["handshake","McFritte"]
                    clientSocket.send(pickle.dumps(x))
                    print("Handshake recieved and response sent!")

        except:
            pass

def initSocket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def main():
    clientSocket = initSocket('localhost', 1337)
    packetHandler = PacketHandler()
    print("initiated")
    listenThread = threading.Thread(target=listenIncoming, args=(clientSocket, packetHandler))
    listenThread.start()

    while True:
        if not listenThread.isAlive:
            listenThread.run()

main()
