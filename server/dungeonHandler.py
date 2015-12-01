import threading, pickle, time, random
from wumpus import *
class DungeonHandler:
    def __init__(self,serverHandler): #Define initial varibles. Notice all rooms are the same on client.
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
        self.activeWumpus = {}
        self.rPowerup = "power"
        self.numWumpus = 0
        self.playerNames = {}
        self.restarting = False
    def newDungeon(self): #Generate new dungeon. Two dimensional lists.
        self.dungeon = []
        for i in range(self.size):
            self.dungeon.append([])
        for item in self.dungeon:
                item.extend(self.rEmpty*self.size)
        self.dungeonDetails()
    def dungeonDetails(self): #Adding details to the map, might update this to a more advanced algorythm.
        k = 0
        n = 200
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
    def spawnPlayer(self,player,a=0,b=0): #Random cordinates until the fields is empty, also restart feature too make sure board is clean, all new Wumpus's starts with x,y -1,-1
        if player.y != -1:
            self.dungeon[player.y][player.x] = self.rEmpty
        while True:
            y = random.randint(0,self.size-1)
            x = random.randint(0,self.size-1)
            if self.dungeon[y][x] == self.rEmpty:
                self.dungeon[y][x] = self.rSpawn
                #time.sleep(0.5)
                print(player.name)
                self.dungeon[y][x] = player.name
                player.y = y
                player.x = x
                return
    def createWumpus(self): #Creating na new instance of the wumpus class, using the numWumpus to make sure that every wumpus has a unique ID to handle triggers.
        if self.restarting != True:
            self.numWumpus += 1
            identifier = self.numWumpus
            name = "wumpus"+str(identifier)
            self.activeWumpus[name] = Wumpus(name)
            self.spawnPlayer(self.activeWumpus[name])  #Also sending the new intance to spawn, notice cords of all new wumpus's is y,x -1,-1
    def wumpusAi(self): #Random int used as a key to pick and move to be passed to updatePlayer,
        options = ["up","down","left","right","pass"]
        while True:
            time.sleep(0.5)
            try:
                for key,wumpus in self.activeWumpus.items():
                    threading.Thread(target=self.wumpusAiupdate, args=(wumpus,options[random.randint(0,4)] )).start() #Threads make everything more fun.
            except:
                pass #Wupus might die during iteration.
    def wumpusAiupdate(self,wumpus,option): #Function purley used to applie Threading package, to keep programing from blocking.
        if option != "pass":
            self.updatePlayer(wumpus,option)
    def dungeonStream(self,activePlayers): #The very heart of the program, from here everything is packaged and checked through diffrent filters.
        for i in range(10):
            self.createWumpus()
        threading.Thread(target=self.wumpusAi,args=()).start() #After initiating the fist 10 Wumpu's we start the AI thread.
        print("System Online Commander!") #Notify user that server is ready to handle clients, clients can connect earlier, but the client will not render.
        while True:
            for player in activePlayers: #Going through every player and packing/checking/tuneing and sending. Also checks for highscore mets requierments for restart.
                payload = ['GUI']
                roomList = [self.rEmpty, self.rBat, self.rWumpus, self.rEnd, self.rBullet,self.rSpawn,self.rServer, self.rPowerup]
                for z in range(9):
                    for i in range(9):
                        try:
                            if (player.y-4+z < 0) or (player.x-4+i < 0): #Make sure the field is in the two dimensional plan.
                                payload.append(self.rEnd)
                            else:
                                cordValue = self.dungeon[player.y-4+z][player.x-4+i] #grabbing the value in the field corresponding to the given cords
                                if cordValue in roomList:
                                    payload.append(cordValue)

                                elif cordValue[0:6] == self.rWumpus:
                                    payload.append(self.rWumpus)
                                else: #If no requierments are meet, the only possibility left is a unique playername.
                                    payload.append(self.rPlayer)
                        except: #If somehow we get out of range on the two dimensional plan, we will just append a sprite code for End aka "out of bounds"
                            payload.append(self.rEnd)
                score = self.getScore(activePlayers) #grabbing the score of all activePlayers.
                if score[0] >= 20000: #Trigger amount for restart.
                    self.restart(activePlayers)
                score.append(player.score)
                score.append(len(self.activeWumpus))
                infoPayload = "1:{} 2:{} 3:{} You:{} #Wumpus:{}".format(*score) #Unpacking the score list to match the format format.
                payload.append(infoPayload)
                try: #Sending payload twice, before removing player from the stream list.
                    player.clientsocket.send(pickle.dumps(payload))
                except:
                    try:
                        player.clientsocket.send(pickle.dumps(payload))
                    except:
                        del activePlayers[activePlayers.index(player)]
    def restart(self,activePlayers): #Re-generates the dungeon, re-spawns 10 wumpus, and re-spawns players.
        self.restarting = True
        time.sleep(2)
        self.activeWumpus.clear() #Clears old wumpus's. I dont know if Pacman eats this.
        self.newDungeon()
        self.restarting = False
        while len(self.activeWumpus) < 10:
            self.createWumpus()
        for player in activePlayers:
            self.dungeon[player.y][player.x] = self.rEmpty
            player.score = 0
            self.spawnPlayer(player)
    def getScore(self,activePlayers):#Grab it,sort it, tune it, return it.
        score = []
        for player in activePlayers:
            score.append(player.score)
        score.sort()
        score.reverse()
        returnScore=[0,0,0] #Default values.
        for i in range(len(score)):
            returnScore[i] = score[i]
        return returnScore


    def updatePlayer(self,player,move): #So you made it this far? Following ? Okey...
        triggers={}                     #This function is heavy, saving functions pointers in lists and using lambda functions.
        triggers[self.rBat] = self.spawnPlayer #Saving a pointer to the function spawnPlayer with the key corresponding to room identifier for bat
        triggers[self.rPowerup] = self.powerup #Saving a pointer to the function powerup with the key corresponding to room identifier for power up
        d = {} #Empty dictionary.
        d["up"]    = lambda y,x,c : [y-c, x] #This
        d["down"]  = lambda y,x,c : [y+c, x] #is
        d["left"]  = lambda y,x,c : [y, x-c] #just
        d["right"] = lambda y,x,c : [y, x+c] #Math
        a,b = d[move](player.y,player.x,1) #Parsing player current cordinates to dictionary using move as the key, The lambda alters them corresponding the direction of travel.
        try:
            if self.dungeon[a][b] == self.rEmpty and a >= 0 and b >= 0 and a <= self.size and b <= self.size: #Making sure we dont handle cords "out of bounds"
                self.dungeon[player.y][player.x] = self.rEmpty #As the players tried to move to and empty field we just reset the current field and set the new.
                self.dungeon[a][b] = player.name #Setting the new field to player information key, in this program its the name
                player.y = a  #Keeping track of player current position
                player.x = b
            elif self.dungeon[a][b] in self.activeWumpus: #running into WUmpus costs you 1000 points.
                player.score -= 1000
            elif self.dungeon[a][b] in self.playerNames and player.name[0:6] == "wumpus": #If wumpus runs into you it also costs you 1000 points.
                self.playerNames[self.dungeon[a][b]].score -= 1000

            elif self.dungeon[a][b] in triggers and player.name not in self.activeWumpus: #Wumpus cannot triggers events. But if field value is in dictionary
                triggers[self.dungeon[a][b]](player,a,b)                                  #of functions, it will pass the players instace and the field value.
            else:                                                                         #At the time i write this only bat and power up exists.
                pass                                                                      #Might also wanna notice that bat function works as an teleportation option.
                #this takes walls and other non triggers objects.
        except:
            pass

    def liveBullet(self,player,direction): #Cant kill wumpus if you cant shoot right ?
        bulletStep = 1 #Amount of fields the bullet travel per tick.
        x = player.x
        y = player.y
        d={} #Empty dictionary.
        d["sUp"]    = lambda y,x,c : [y-c, x] #This
        d["sDown"]  = lambda y,x,c : [y+c, x] #is
        d["sLeft"]  = lambda y,x,c : [y, x-c] #just
        d["sRight"] = lambda y,x,c : [y, x+c] #Math
        for i in range(player.bulletRange): #Using the bullet range from the players instance, we get limits for how long the bullet will travel.
            a,b = d[direction](y,x,bulletStep) #Doing the math.
            if a >= self.size or b >= self.size: #No point shooting "out of bounds", like wumpus would hide in the shadows ?
                return
            if self.dungeon[a][b] in self.playerNames: #Shooting other players yeilds 500 points >:)
                self.playerNames[self.dungeon[a][b]].score -= 500
                player.score += 500
                return
            if self.dungeon[a][b] in self.activeWumpus: #Shooting wumpus of course wumpus explodes on hit, we would not have it any other way.
                wumpus = self.activeWumpus[self.dungeon[a][b]]
                wumpus.dead = True
                self.dungeon[a][b] = self.rEmpty
                self.wumpusExplosion(wumpus) #Wumpus goes booooom. Also pasing along the self.playerNames to save cpu. (hehe)
                del self.activeWumpus[wumpus.name] #Dead wumpus must go away. Hopefully packman eats this. I dont know.
                player.score += 500
                threading.Thread(target=self.createWumpus, args=()).start() #Threads make
                threading.Thread(target=self.createWumpus, args=()).start() # everything fun.
                return                                                      #As the spawn function searches for a empty field, it would be blocking the rest of the function.
            if self.dungeon[a][b] in  [self.rBat,self.rServer,self.rPowerup]: #Somethings you cant shoot through, and dont trigger events.
                return
            self.dungeon[a][b] = self.rBullet #Animate the bullet.
            time.sleep(0.2)
            if self.dungeon[a][b] == self.rBullet:
                self.dungeon[a][b] = self.rEmpty
            bulletStep += 1 #Next animation frame, going through the hole function again.
    def powerup(self,player,a,b): #If players move into the image of Inggo, the players.bulletRange will increase with one.
        self.dungeon[player.y][player.x] = self.rEmpty
        player.y = a
        player.x = b
        self.dungeon[a][b] = player.name
        player.bulletRange += 1
    def wumpusExplosion(self,wumpus): #This functon grabs an area of 3x3 arround dieing wumpus and passing them one and one to wumpusExplosionCheck in individual functions
        y = wumpus.y
        x = wumpus.x
        cords = [ [y-1,x-1], [y-1,x], [y-1,x+1], [y,x-1],[y,x], [y,x+1], [y+1,x-1], [y+1,x], [y+1,x+1] ]
        for cord in cords:
            threading.Thread(target=self.wumpusExplosionCheck,args=(cord[0],cord[1],)).start() #By now you must love threads ?
    def wumpusExplosionCheck(self,y,x): #Only running animation over empty fields. If player in current field that players losses 2000 points.
        try:
            if self.dungeon[y][x] == self.rEmpty:
                self.dungeon[y][x] = self.rSpawn
                time.sleep(1)
                self.dungeon[y][x] = self.rEmpty
                return
            if self.dungeon[y][x] in self.playerNames:
                self.playerNames[self.dungeon[y][x]].score -= 2000 #As self.dungeon[x][y] would return a name, and players names are used as keys... the hole block returns a player instance
                name = self.dungeon[y][x]
                self.dungeon[y][x] = self.rSpawn
                time.sleep(1)
                if self.playerNames[name].y == y and self.playerNames[name].x == x:
                    self.dungeon[y][x] = self.playerNames[name].name
                else:
                    self.dungeon[y][x] = self.rEmpty
        except:
            pass
