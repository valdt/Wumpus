import threading, pickle, time
class Player:
    def __init__(self,serverHandler,clientsocket,dungeonHandler):
        self.dungeonHandler = dungeonHandler
        self.clientsocket = clientsocket
        self.alive = True
        self.y = int(0)
        self.x = int(0)
        self.bulletRange = int(3)
        self.score = int(0)
        self.spam = False
        #self.antiSpamThread = threading.Thread(target=self.antiSpam, args=())
        #self.antiSpamThread.start()
        payload = ["Handshake","404"]
        reData = serverHandler.pulse(payload,self.clientsocket)
        print(reData)
        if reData[0] == "Handshake":
            self.name = reData[1]
            threading.Thread(target=self.playerInput).start()
    #Notice thats this function should and is run in a thread!
    def antiSpam(self):
        self.spam = True
        time.sleep(0.05)
        self.spam= False

    def playerInput(self):
        while True:
            try:
                data = self.clientsocket.recv(256)
            except:
                self.alive = False
                return
            if data and data != "" and self.spam == False:
                threading.Thread(target=self.antiSpam, args=()).start()
                data = pickle.loads(data)
                if data[0]=="move":
                    self.dungeonHandler.updatePlayer(self,data[1])
                if data[0]=="shoot":
                    threading.Thread(target=self.dungeonHandler.liveBullet , args=(self,data[1],)).start()
                    #self.dungeonHandler.liveBullet(self,data[1])
