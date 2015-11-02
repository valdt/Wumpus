class WumpusHandler:
    def __init__(self):
        self.activeWumpus = []
        self.uid = 0

    def newWumpus(x, y):
        self.activeWumpus.append(Wumpus(x, y, self.uid))
        self.uid += 1

    def update():
        for wumpus in activeWumpus:
            wumpus.update()
