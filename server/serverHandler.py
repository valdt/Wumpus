import pickle, socket, time, threading
class ServerHandler:
    def __init__(self,host,port):
        self.activePlayers = []
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #I am still researching, it lets me reuse the port.
        self.serverSocket.bind((host, port)) #Lock'n'Load ... bind*
        self.serverSocket.listen(10) #lissening for new connections

    def pulse(self,payload,clientsocket): #Testing connection to client.
        try:
            defaultError = ["error","Replie took to long and TTL expired."]
            clientsocket.send(pickle.dumps(payload, -1))
            ttl = 0
            while True:
                ttl += 1
                data = clientsocket.recv(2048)
                if data and data != "":
                    return pickle.loads(data)
                elif ttl > 10:
                    return defaultError
        except:
            defaultError = ["error","Function failed"]
            return defaultError
    def getPlayerNames(self): #Going through all active players grabbing there names and appending them to a list, used in filters arround the program.
        playerNames = {}
        for player in self.activePlayers:
            playerNames[player.name] = player
        return playerNames
