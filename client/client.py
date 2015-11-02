import pickle, socket, sys, threading
from PacketHandler import *
from clientClasses import *

def listenIncoming(clientSocket, packetHandler):
    if clientSocket:
        print("socket")
        try:
            data = pickle.loads(clientSocket.recv(10000))
            print("data tried and succeeded")
            x = ["handshake","McFritte"]
            clientSocket.send(pickle.dumps(x))
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
        listenThread = threading.Thread(target=listenIncoming, args = (clientSocket, packetHandler))
        listenThread.start()

    while True:
        #print(clientSocket.recv(10000))
        listenThread.run()
        
main()
