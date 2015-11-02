class ServerSocket:
    def __init__(self,host,port):
        import pickle, socket, time, threading
        self.clientSocketList = []
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((host, port))
        serverSocket.listen(10)
        acceptPlayersThread = threading.Thread(target=self.acceptPlayers, args=(serverSocket,))
        acceptPlayersThread.start()

    def acceptPlayers(self,serverSocket):
        clientsocket, address = serverSocket.accept()
        clientSocketList.append(Player(clientsocket))
        print("New connection established from {}".format(address))
    def pulse(payload,clientsocket):
        try:
            defaultError = ["error","Replie took to long and TTL expired."]
            clientsocket.send(pickle.dump(payload))
            ttl = 0
            while True:
                ttl += 1
                data = clientsocket.recv(2048)
                if data and data != "":
                    return pickle.load(data)
                elif ttl > 1000:
                    return defaultError
        except:
            defaultError = ["error","Function failed"]
            return defaultError


class Player:
    def __init__(clientsocket):
        data = ["handshake"]
        data = pickle.dump(data)
        reData = pulse(payload,clientsocket)
        if reData[0] == "handshake":
            self.name = reData[1]

class Dungeon:
    pass
