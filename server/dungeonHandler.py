import threading, pickle, time
class DungeonHandler:
    def __init__(self):
        self.dungeon = []
        self.size = 25
        self.rEmpty = "e"
        self.rBat = "bat"
        self.rWumpus = "wumpus"
        self.rEnd = "end"
        self.rPlayer = "player"
    def newDungeon(self):
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
    def newPlayer(self,player):
        self.dungeon[0][0] = player.name
    def dungeonStream(self,activePlayers):
        self.dungeon[2][4] = self.rWumpus
        self.dungeon[4][2] = self.rWumpus
        while True:
            for player in activePlayers:
                payload = ['GUI']
                for z in range(5):
                    for i in range(5):
                        try:
                            if (player.y-2+z < 0) or (player.x-2+i < 0):
                                payload.append(self.rEnd)
                            else:
                                if self.dungeon[player.y-2+z][player.x-2+i] in [self.rEmpty, self.rBat, self.rWumpus, self.rEnd]:
                                    payload.append(self.dungeon[player.y-2+z][player.x-2+i])
                                else:
                                    payload.append(self.rPlayer)
                        except:
                            payload.append(self.rEnd)
                player.clientsocket.send(pickle.dumps(payload))

    def updatePlayer(self,player,move):
        try:
            # -----Up--------
            if move == "up":
                if self.dungeon[player.y-1][player.x] in [self.rEmpty,self.rBat] and player.y-1 >= 0 :
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y-1][player.x] = player.name
                    player.y -= 1
                    print("{}: {}".format(player.name,move))
                elif self.dungeon[player.y-1][player.x] == self.rWumpus:
                    print("ohh you dead!")
            # -----Down--------
            if move == "down":
                if self.dungeon[player.y+1][player.x] in [self.rEmpty,self.rBat] and player.y+1 < self.size:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y+1][player.x] = player.name
                    player.y += 1
                    print("{}: {}".format(player.name,move))
                elif self.dungeon[player.y+1][player.x] == self.rWumpus:
                    print("ohh you dead!")
            # -----Left--------
            if move == "left":
                if self.dungeon[player.y][player.x-1] in [self.rEmpty,self.rBat] and player.x-1 >= 0:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y][player.x-1] = player.name
                    player.x -= 1
                    print("{}: {}".format(player.name,move))
                elif self.dungeon[player.y][player.x-1] == self.rWumpus:
                    print("ohh you dead!")
            #---- Right -------
            if move == "right":
                if self.dungeon[player.y][player.x+1] in [self.rEmpty,self.rBat] and player.x+1 < self.size:
                    self.dungeon[player.y][player.x] = self.rEmpty
                    self.dungeon[player.y][player.x+1] = player.name
                    player.x += 1
                    print("{}: {}".format(player.name,move))
                elif self.dungeon[player.y][player.x+1] == self.rWumpus:
                    print("ohh you dead!")

        except:
            pass
