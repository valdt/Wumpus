#Wumpus 2.0
As final project for my introductory course in Python at the royal institute of technology i developed a more advanced version of the classic Wumpus assignment. This project deepen and broaded my knowledge of Python and programming in general. I also spent a lot of time going back rewriting code to be more fluent and less repeating. Which turn out to be a challenge in itself, as many of the problems were new to me, and so were many of the solutions i used.

The code starts of with building its environment by utilizing threading as it creates different threads to handle both the socket server and the generating of the two dimensional playfield. The playfield is generated as a nine by nine square, which allows for the usage of y and x coordinates. As the playfield completes the program continues spawning in details like walls, monsters, teleports and power ups. Objects interact with the players in specific manners. For example the teleport symbol will teleport any player that steps on it to a random coordinate on the playfield. And the power up will increase the range of which a bullet fired by the player will travel. When a player manage to kill a monster that player's score increases some, however the monster will explode violently, the explosion creates a three by three area around the corps that will reduce the current score of players trapped in the area also additional to the explosion two new monsters will be spawned at random locations in the map. The client displays small leaderboards at the bottom of the graphical interface, to let the player know whos in the lead, it also displays the number of monsters in the playfield. The first player to reach 20.000 points wins, which automatically triggers a restart function. The restart function generates a new map and resets the amount of monsters to default starting value of ten.

The program is separated in two different parts client and server, the client is then separated into two main threads. Were the first thread handles receiving data from the server, tuning it up and parsing it along to a function that updates the graphical interface. The speed of this determines the frames per second (fps), the latency between the server sending the data and the user getting it rendered on his or hers screen has proven to be significant low under perfect conditions. The second thread of the client handles keyboard input and creating a payload to be sent to the server. As you may figure the client is very lightweight as all the calculations are design to be executed on the server to eliminate interference from the user, with the intentions of preventing alterations to the gameplay. The client also have an buildin anti spam function to prevent the player's character from moving equally fast as the players can press the movement keys, this was discovered by holding down any of the keys.

The server however is divided in four different main threads who then in different stages spawns even more threads for handling everything from monster movements, players being spawned and bullets being fired. First of we create an instance of the serverhandler instance this will be the very core of handling connections. After that we create an instance of the dungeon handler class which starts generating the two dimensional playfield and spawning in details. Then we fire up one of the main threads which essentially handle new connections, saves their information down as the “clientsocket” object. This object is then used as an argument for creating an instance of the player class corresponding to the new connection that came in. This new player instance is then passed into the serverhandler instance. And finally as there's a new player joining we run a function that goes through a list of player instances in the serverhandler instance and pulls out all the players name, and passes this over to the dungeon handler instance, where it will be used for different filters and in playfield structure.
Then we fire up the second main thread which is a function inside the dungeon handler instance called dungeon stream, this thread grabs the current dungeon data then cuts out a nine by nine area where the player's position is in the center, the function does this for every player, then starts over. This cutout is then packaged in a list corresponding to the structure of the receiving client, the function also appends one extra item of status information shown at the bottom of the client. The dungeon streamer also keeps a track of the player's score and checks if anyone has reached the triggering amount for a restart to take place. The anti spam thread is simple in its design but fills a very important purpose as it limits the amount of moves a player can make to one move every 0.05 second plus cpu delay. The final main thread is to catch and handle player inputs, however this threads is created for every player, which allows the players to all move at the same time. After receiving an input from a player's client, the function figures out if the player wanted to shoot or move, and parses the information to the corresponding function alongside the needed player information. The corresponding function then handles all the animations and the detections without blocking the player continuing on.
Now the wumpus AI is still being developed but for now the mainframe is down and wumpus moves around and you lose points if you bumped into him. Every wumpus that gets spawned also gets new threaded instance of the wumpus AI function, so that every wumpus monster can generate individual moves at the same time. All the monsters constantly tries to figure out if they want to go up,down,left,right  or stay put. When wumpus finally has made up his mind he will send the decision to the function corresponding for handling the updating of players positions. And finally every bullet fired by every player gets its own threaded instance of the live bullet function, which then runs the animation and collision detection. So the numbers of threads are actually the combination of
3+(n * Players)+(n * Wumpus)+(n * Bullets). The system has no built in limit for how many players that can join, but i expect the server to commit suicide at some point.

How to start:
1: as Server run the server.py in the server folder.
2: Start client.py in the client folder. Make sure to use a new terminal for this.
