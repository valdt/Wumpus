import pickle, socket, sys, threading, time
import tkinter as tk

def updateGui(labelList,rooms): #Going through all the data, as data is package in the same structure as labels a created i just run a for loop over the hole thing.
    print("Reciver started!")   #data[0] => labelList[0].
    while True:
        try:
            data = pickle.loads(serverSocket.recv(2048)) #Waiting for payload aka data
            if data[0] == "GUI": #Checking so thats its not a false package, i hade security in mind when i started this project. Yeah i aint geting hacked.
                labelList[-1].configure(text=data[-1]) #grabing the last data item as it will always be the status text.
                data.remove(data[-1]) #Removing to not interfere with the labels.
                data.remove("GUI") #Removing to not interfere with the labels.
                i = 0
                for item in data: #item will be an string corresponding to a code for a sprite.
                    labelList[i].configure(image=rooms[item])  #Just magic.
                    i += 1
        except:
            pass

def mUp(event): #Binding keys, its ugly, but its the tkinter way of doing stuff.
    serverSocket.send(pickle.dumps(["move","up"]))
def mDown(event):
    serverSocket.send(pickle.dumps(["move","down"]))
def mRight(event):
    serverSocket.send(pickle.dumps(["move","right"]))
def mLeft(event):
    serverSocket.send(pickle.dumps(["move","left"]))
def special(event):
    serverSocket.send(pickle.dumps(["special","special"]))
def sUp(event):
    serverSocket.send(pickle.dumps(["shoot","sUp"]))
def sDown(event):
    serverSocket.send(pickle.dumps(["shoot","sDown"]))
def sLeft(event):
    serverSocket.send(pickle.dumps(["shoot","sLeft"]))
def sRight(event):
    serverSocket.send(pickle.dumps(["shoot","sRight"]))

#Setting up Socket connection.
global serverSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect(("localhost", 1337))
#After sucessfull connection we expect an Handshake.
data = pickle.loads(serverSocket.recv(2048))
#Now we start rendering the GUI
root = tk.Tk()
#image importing.
rooms = {}
rooms["e"] = tk.PhotoImage(file="img/floor1.gif")
rooms["bat"] = tk.PhotoImage(file="img/bat.gif")
rooms["end"] = tk.PhotoImage(file="img/wall.gif")
rooms["player"] = tk.PhotoImage(file="img/player.gif")
rooms["wumpus"] = tk.PhotoImage(file="img/wumpus2.gif")
rooms["bullet"] = tk.PhotoImage(file="img/bullet.gif")
rooms["death"] = tk.PhotoImage(file="img/death.gif")
rooms["spawn"] = tk.PhotoImage(file="img/spawn.gif")
rooms["server"] = tk.PhotoImage(file="img/server.gif")
rooms["power"] = tk.PhotoImage(file="img/powerup.gif")

frameList = []
labelList = []
#We make 10 frames, in these we make additional 9 labels execept the last one we only make one (the status info label) Resulting a 9x9 area. plus one row of information
for i in range(10):
    frameList.append( tk.Frame(bg="blue") )
for item in frameList[0:-1]:
    for i in range(9):
        labelList.append( tk.Label(item, image=rooms["e"], bd=0) )
for item in labelList:
    item.pack(side=tk.LEFT)
labelList.append(tk.Label(frameList[-1], height=3, text="Servers not read yet...", bd=0))
labelList[-1].pack(side=tk.LEFT)
labelList[40].configure(image=rooms["player"])
for item in frameList:
    item.pack()
#We start ouer GUI updater.
updateGuiThread = threading.Thread(target=updateGui, args=(labelList,rooms)).start()
#And we tell the server everything went well.
serverSocket.send(pickle.dumps(["Handshake","GenericPlayer"]))
#Binding keys, its ugly, but its the tkinter way of doing stuff.
root.bind("<w>", mUp)
root.bind("<s>", mDown)
root.bind("<a>", mLeft)
root.bind("<d>", mRight)
root.bind("<space>", special)
root.bind("<Up>", sUp)
root.bind("<Down>", sDown)
root.bind("<Right>", sRight)
root.bind("<Left>", sLeft)

root.mainloop()
