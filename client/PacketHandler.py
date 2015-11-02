from DungeonHandler import *
from WumpusHandler import *

class PacketHandler:
    def __init__(self):
        self.dungeonHandler = DungeonHandler()
        self.wumpusHandler = WumpusHandler()
