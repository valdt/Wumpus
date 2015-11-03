import threading, pickle
class DungeonHandler:
    def __init__(self):
        self.size = 25
        self.rEmpty = "e"
    def newDungeon(self):
        self.dungeon = []
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
        print (self.dungeon)
    def newPlayer(self,player):
        self.dungeon[13][0] = player.name
    def updatePlayer(self,player,move):
        print(self.dungeon[player.y][player.x])
        self.dungeon[player.y][player.x+1] = player.name
        print (self.dungeon)
