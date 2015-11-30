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
        self.rPowerup = "power"
    def newDungeon(self):
        self.dungeon = []
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
        self.dungeonDetails(200)
    def dungeonDetails(self,n):
        k = 0
        while k <= n:
            i = random.randint(0,self.size-1)
            z = random.randint(0,self.size-1)
            if self.dungeon[i][z] == self.rEmpty:
                self.dungeon[i][z] = self.rServer
                k += 1
        k = 1
        while k <= 2:
            i = random.randint(0,self.size-1)
            z = random.randint(0,self.size-1)
            if self.dungeon[i][z] == self.rEmpty:
                self.dungeon[i][z] = self.rBat
                k += 1
        k=1
        while k <= 10:
            i = random.randint(0,self.size-1)
            z = random.randint(0,self.size-1)
            if self.dungeon[i][z] == self.rEmpty:
                self.dungeon[i][z] = self.rPowerup
                k += 1
    def spawnPlayer(self,player,a=0,b=0):
        try:
            self.dungeon[player.y][player.x] = self.rEmpty
        except:
            pass
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
            try:
                for wumpus in self.activeWumpus:
                    threading.Thread(target=self.wumpusAiupdate, args=(wumpus,options[random.randint(0,4)] )).start()
            except:
                pass #Wupus might die during iteration.
    def wumpusAiupdate(self,wumpus,option):
        if option != "pass":
            self.updatePlayer(wumpus,option)
    def timer():
        time.sleep(60)
        restart = True
    def dungeonStream(self,activePlayers):
        for i in range(10):
            self.createWumpus()
        threading.Thread(target=self.wumpusAi,args=()).start()
        print("System Online Commander!")
        while True:
            for player in activePlayers:
                payload = ['GUI']
                roomList = [self.rEmpty, self.rBat, self.rWumpus, self.rEnd, self.rBullet,self.rSpawn,self.rServer, self.rPowerup]
                for z in range(9):
                    for i in range(9):
                        try:
                            if (player.y-4+z < 0) or (player.x-4+i < 0):
                                payload.append(self.rEnd)
                            else:
                                if self.dungeon[player.y-4+z][player.x-4+i] in roomList:
                                    payload.append(self.dungeon[player.y-4+z][player.x-4+i])
                                else:
                                    payload.append(self.rPlayer)
                        except:
                            payload.append(self.rEnd)
                score = self.getScore(activePlayers)
                if score[0] >= 20000:
                    self.restart(activePlayers)
                score.append(player.score)
                score.append(len(self.activeWumpus))
                infoPayload = "1:{} 2:{} 3:{} You:{} #Wumpus:{}".format(*score)
                payload.append(infoPayload)
                try:
                    player.clientsocket.send(pickle.dumps(payload))
                except:
                    try:
                        player.clientsocket.send(pickle.dumps(payload))
                    except:
                        del activePlayers[activePlayers.index(player)]
    def restart(self,activePlayers):
        for wumpus in self.activeWumpus:
            i = self.activeWumpus.index(wumpus)
            del self.activeWumpus[i]
        self.newDungeon()
        while len(self.activeWumpus) < 10:
            self.createWumpus()
        for player in activePlayers:
            self.dungeon[player.y][player.x] = self.rEmpty
            player.score = 0
            self.spawnPlayer(player)
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

    def getPlayerNames(self):
        playerNames = {}
        for classPlayer in self.serverHandler.activePlayers:
            playerNames[classPlayer.name] = classPlayer
        return playerNames
    def updatePlayer(self,player,move):
        triggers={}
        triggers[self.rBat] = self.spawnPlayer
        triggers[self.rPowerup] = self.powerup

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
            elif self.dungeon[a][b] in triggers and player.name != "wumpus":
                triggers[self.dungeon[a][b]](player,a,b)
            else:
                pass
                #this takes walls and other non triggers objects.
        except:
            pass

    def liveBullet(self,player,direction):
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
            if a >= self.size or b >= self.size:
                return
            if self.dungeon[a][b] in playerNames:
                playerNames[self.dungeon[a][b]].score -= 500
                player.score += 500
                return
            if self.dungeon[a][b] == self.rWumpus:
                for i in range(len(self.activeWumpus)-1):
                    wumpus = self.activeWumpus[i]
                    if wumpus.y == a and wumpus.x == b:
                        wumpus.dead = True
                        del self.activeWumpus[i]
                        self.dungeon[a][b] = self.rEmpty
                        self.wumpusExplosion(wumpus,playerNames)
                        player.score += 500
                        threading.Thread(target=self.createWumpus, args=()).start()
                        threading.Thread(target=self.createWumpus, args=()).start()
                        return
            if self.dungeon[a][b] in  [self.rBat,self.rServer]:
                return
            self.dungeon[a][b] = self.rBullet
            time.sleep(0.2)
            if self.dungeon[a][b] == self.rBullet:
                self.dungeon[a][b] = self.rEmpty
            ttl += 1
    def powerup(self,player,a,b):
        self.dungeon[player.y][player.x] = self.rEmpty
        player.y = a
        player.x = b
        self.dungeon[a][b] = player.name
        player.bulletRange += 1
    def wumpusExplosion(self,wumpus,playerNames):
        y = wumpus.y
        x = wumpus.x
        cords = [ [y-1,x-1], [y-1,x], [y-1,x+1], [y,x-1],[y,x], [y,x+1], [y+1,x-1], [y+1,x], [y+1,x+1] ]
        for cord in cords:
            threading.Thread(target=self.wumpusExplosionCheck,args=(cord[0],cord[1],playerNames,)).start()
    def wumpusExplosionCheck(self,y,x,playerNames):
        if self.dungeon[y][x] == self.rEmpty:
            self.dungeon[y][x] = self.rSpawn
            time.sleep(1)
            self.dungeon[y][x] = self.rEmpty
            return
        if self.dungeon[y][x] in playerNames:
            playerNames[self.dungeon[y][x]].score -= 2000
            name = self.dungeon[y][x]
            self.dungeon[y][x] = self.rSpawn
            time.sleep(1)
            if playerNames[name].y == y and playerNames[name].x == x:
                self.dungeon[y][x] = playerNames[name].name
            else:
                self.dungeon[y][x] = self.rEmpty
