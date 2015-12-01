class Wumpus:
    def __init__ (self,name): #Define initial varibles. Notice y,x -1,-1
        self.x = int(-1)
        self.y = int(-1)
        self.name = name
        self.dead = False
        self.score = int(0)
