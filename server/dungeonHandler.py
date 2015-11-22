import threading, pickle, time, random
class DungeonHandler:
    def __init__(self,serverHandler):
        self.serverHandler = serverHandler
        self.dungeon = []
        self.size = 50
        self.rEmpty = "e"
        self.rBat = "bat"
        self.rWumpus = "wumpus"
        self.rEnd = "end"
        self.rPlayer = "player"
        self.rBullet = "bullet"
    def newDungeon(self):
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
    def spawnPlayer(self,player):
        while True:
            y = random.randint(0,self.size)
            x = random.randint(0,self.size)
            if self.dungeon[y][x] == self.rEmpty:
                player.y = y
                player.x = x
                return
    def dungeonStream(self,activePlayers):
        self.dungeon[2][4] = self.rWumpus
        self.dungeon[4][2] = self.rWumpus
        while True:
            for player in activePlayers:
                payload = ['GUI']
                for z in range(9):
                    for i in range(9):
                        try:
                            if (player.y-4+z < 0) or (player.x-4+i < 0):
                                payload.append(self.rEnd)
                            else:
                                if self.dungeon[player.y-4+z][player.x-4+i] in [self.rEmpty, self.rBat, self.rWumpus, self.rEnd, self.rBullet]:
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
        trigger = {}
        trigger[self.rWumpus] = player.score - 2000
        thingsYouWantToMoveInto = [self.rEmpty,self.rBat]
        thingsYouDontWantoMoveInto = [self.rWumpus,self.rBullet]
        try:
            # -----Up--------
            print("{}: {}".format(player.name,move))
            if move == "up":
                if self.dungeon[player.y-1][player.x] in thingsYouWantToMoveInto and player.y-1 >= 0 :
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y-1][player.x] = player.name
                    player.y -= 1
                elif self.dungeon[player.y-1][player.x] in thingsYouDontWantoMoveInto:
                    player.score - 1000
            # -----Down--------
            if move == "down":
                if self.dungeon[player.y+1][player.x] in thingsYouWantToMoveInto and player.y+1 < self.size:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y+1][player.x] = player.name
                    player.y += 1
                elif self.dungeon[player.y+1][player.x] in thingsYouDontWantoMoveInto:
                    player.score - 1000
            # -----Left--------
            if move == "left":
                if self.dungeon[player.y][player.x-1] in thingsYouWantToMoveInto and player.x-1 >= 0:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y][player.x-1] = player.name
                    player.x -= 1
                elif self.dungeon[player.y][player.x-1] in thingsYouDontWantoMoveInto:
                    player.score - 1000
            #---- Right -------
            if move == "right":
                if self.dungeon[player.y][player.x+1] in thingsYouWantToMoveInto and player.x+1 < self.size:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y][player.x+1] = player.name
                    player.x += 1
                elif self.dungeon[player.y][player.x+1] in thingsYouDontWantoMoveInto:
                    player.score - 1000

        except:
            pass
    def liveBullet(self,player,direction):
        print("Bullet fired")
        ttl = 1
        x = player.x
        y = player.y
        playerNames = self.getPlayerNames()
        d={ "sUp":self.dungeon[y-ttl][x], "sDown":self.dungeon[y+ttl][x], "sLeft":self.dungeon[y][x-ttl], "sRight":self.dungeon[y][x+ttl] }
        print("------------")
        print(d[direction])
        print("------------")
        for i in range(player.bulletRange):
            if d[direction] in playerNames:
                playerNames[d[direction]].score - 500
                player.score + 500
            d[direction] = self.rBullet
            time.sleep(0.2)
            if d[direction] == self.rBullet:
                d[direction] = self.rEmpty
            ttl += 1
