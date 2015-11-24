import threading, pickle, time, random
from wumpus import *
class DungeonHandler:
    def __init__(self,serverHandler):
        self.serverHandler = serverHandler
        self.size = 50
        self.rEmpty = "e"
        self.rBat = "bat"
        self.rWumpus = "wumpus"
        self.rEnd = "end"
        self.rPlayer = "player"
        self.rBullet = "bullet"
        self.rSpawn = "spawn"
        self.rServer= "server"
        self.activeWumpus = []
    def newDungeon(self):
        self.dungeon = []
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
    def dungeonDetails(self):
        i = 0
        z = 0
        rowList = []
        for row in self.dungeon:
            rowList.append(self.dungeon[i][z])
            i += 1
        rowList
    def spawnPlayer(self,player):
        while True:
            y = random.randint(0,self.size-1)
            x = random.randint(0,self.size-1)
            if self.dungeon[y][x] == self.rEmpty:
                self.dungeon[y][x] = self.rSpawn
                time.sleep(0.5)
                self.dungeon[y][x] = player.name
                player.y = y
                player.x = x
                return
    def createWumpus(self):
        self.activeWumpus.append(Wumpus())
        self.spawnPlayer(self.activeWumpus[-1])
    def wumpusAi(self):
        options = ["up","down","left","right","pass"]
        while True:
            time.sleep(0.5)
            print("wumpusAi:{}".format(len(self.activeWumpus)))
            try:
                for wumpus in self.activeWumpus:
                    threading.Thread(target=self.wumpusAiupdate, args=(wumpus,options[random.randint(0,4)] )).start()
            except:
                pass #Wupus might die during iteration.
    def wumpusAiupdate(self,wumpus,option):
        if option != "pass":
            self.updatePlayer(wumpus,option)

    def dungeonStream(self,activePlayers):
        for i in range(10):
            self.createWumpus()
        threading.Thread(target=self.wumpusAi,args=()).start()
        while True:
            for player in activePlayers:
                payload = ['GUI']
                for z in range(9):
                    for i in range(9):
                        try:
                            if (player.y-4+z < 0) or (player.x-4+i < 0):
                                payload.append(self.rEnd)
                            else:
                                if self.dungeon[player.y-4+z][player.x-4+i] in [self.rEmpty, self.rBat, self.rWumpus, self.rEnd, self.rBullet,self.rSpawn,self.rServer]:
                                    payload.append(self.dungeon[player.y-4+z][player.x-4+i])
                                else:
                                    payload.append(self.rPlayer)
                        except:
                            payload.append(self.rEnd)
                score = self.getScore(activePlayers)
                score.append(player.score)
                infoPayload = "1:{} 2:{} 3:{} You:{}".format(*score)
                payload.append(infoPayload)
                player.clientsocket.send(pickle.dumps(payload))
    def bat():
        pass
    def getScore(self,activePlayers):
        score = []
        for player in activePlayers:
            score.append(player.score)
        score.sort()
        score.reverse()
        returnScore=["n/a","n/a","n/a"]
        try:
            returnScore[0] = score[0]
        except:
            pass
        try:
            returnScore[1] = score[1]
        except:
            pass
        try:
            returnScore[2] = score[2]
        except:
            pass
        return returnScore

    def gameOver(player):
        player.score - 1000
    def getPlayerNames(self):
        playerNames = {}
        for classPlayer in self.serverHandler.activePlayers:
            playerNames[classPlayer.name] = classPlayer
        return playerNames
    def triggerGameOver():
        pass
    def updatePlayer(self,player,move):
        triggers={}
        triggers[self.rBat] = self.spawnPlayer


        d = {}
        d["up"]    = lambda y,x,c : [y-c, x]
        d["down"]  = lambda y,x,c : [y+c, x]
        d["left"]  = lambda y,x,c : [y, x-c]
        d["right"] = lambda y,x,c : [y, x+c]
        a,b = d[move](player.y,player.x,1)
        try:
            if self.dungeon[a][b] == self.rEmpty and a >= 0 and b >= 0 and a <= self.size and b <= self.size:
                self.dungeon[player.y][player.x] = self.rEmpty
                self.dungeon[a][b] = player.name
                player.y = a
                player.x = b
            elif self.dungeon[a][b] == self.rWumpus:
                player.score -= 1000
            elif self.dungeon[a][b] in triggers:
                triggers[self.dungeon[a][b]](player)
            else:
                pass
                #this takes walls and other non triggers objects.
        except:
            pass

    def liveBullet(self,player,direction):
        print("Bullet fired")
        ttl = 1
        x = player.x
        y = player.y
        playerNames = self.getPlayerNames()
        d={}
        d["sUp"]    = lambda y,x,c : [y-c, x]
        d["sDown"]  = lambda y,x,c : [y+c, x]
        d["sLeft"]  = lambda y,x,c : [y, x-c]
        d["sRight"] = lambda y,x,c : [y, x+c]
        for i in range(player.bulletRange):
            a,b = d[direction](y,x,ttl)
            if self.dungeon[a][b] in playerNames:
                playerNames[self.dungeon[a][b]].score - 500
                player.score + 500
                return
            if self.dungeon[a][b] == self.rWumpus:
                for i in range(len(self.activeWumpus)-1):
                    wumpus = self.activeWumpus[i]
                    if wumpus.y == a and wumpus.x == b:
                        wumpus.dead = True
                        del self.activeWumpus[i]
                        self.dungeon[a][b] = self.rEmpty
                        threading.Thread(target=self.createWumpus, args=()).start()
                        threading.Thread(target=self.createWumpus, args=()).start()
                        return
            self.dungeon[a][b] = self.rBullet
            time.sleep(0.2)
            if self.dungeon[a][b] == self.rBullet:
                self.dungeon[a][b] = self.rEmpty
            ttl += 1
