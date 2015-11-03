import threading, pickle
class Player:
    def __init__(self,serverHandler,clientsocket,dungeonHandler):
        self.dungeonHandler = dungeonHandler
        self.clientsocket = clientsocket
        self.alive = True
        self.y = int(13)
        self.x = int(0)
        payload = ["Handshake","404"]
        reData = serverHandler.pulse(payload,self.clientsocket)
        print(reData)
        if reData[0] == "Handshake":
            self.name = reData[1]
            threading.Thread(target=self.playerInput).start()
    #Notice thats this function should and is run in a thread!
    def playerInput(self):
        while True:
            try:
                data = self.clientsocket.recv(2048)
            except:
                self.alive = False
                return
            if data and data != "":
                 data = pickle.loads(data)
                 if data[0]=="move":
                    self.dungeonHandler.updatePlayer(self,data[1])
