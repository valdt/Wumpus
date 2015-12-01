import threading, pickle, time
class Player:
    def __init__(self,serverHandler,clientsocket,dungeonHandler): #Define initial varibles.
        self.dungeonHandler = dungeonHandler
        self.clientsocket = clientsocket
        self.alive = True
        self.y = int(0)
        self.x = int(0)
        self.bulletRange = int(4)
        self.score = int(0)
        self.spam = False
        payload = ["Handshake","404"] #Performing handshake, its not really that important but its good reminder that we need to keep security in mind.
        reData = serverHandler.pulse(payload,self.clientsocket)
        if reData[0] == "Handshake":
            self.name = reData[1]
            threading.Thread(target=self.playerInput).start() #As the handshake was sucessfull we go ahead and start a thread for reciving players inputs. (WASD and arrows)
        dungeonHandler.spawnPlayer(self) #And we spawn players to the two dimensional plan, notice we pass along "Self" this will result as a pointer to this instance
    #Notice these this function should and is run in a thread!
    def antiSpam(self): #Super speed could be achieved buy holding down a direction key. This limits the inputs processed to one every 0.05 second + cpu delay.
        self.spam = True
        time.sleep(0.05)
        self.spam= False

    def playerInput(self):
        while True:
            try:
                data = self.clientsocket.recv(256) #just waiting for players to send data/input/move
            except:
                self.alive = False
                return
            if data and data != "" and self.spam == False:
                threading.Thread(target=self.antiSpam, args=()).start()
                data = pickle.loads(data)
                if data[0]=="move": #Quick handling if players wants too shoot or move.
                    self.dungeonHandler.updatePlayer(self,data[1])
                if data[0]=="shoot":
                    threading.Thread(target=self.dungeonHandler.liveBullet , args=(self,data[1],)).start()
