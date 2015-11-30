import pickle, socket, sys, threading, time
import tkinter as tk

def updateGui(labelList,rooms):
    print("Reciver started!")
    while True:
        try:
            data = pickle.loads(serverSocket.recv(2048))
            if data[0] == "GUI":
                labelList[-1].configure(text=data[-1])
                data.remove(data[-1])
                data.remove("GUI")
                i = 0
                for item in data:
                    labelList[i].configure(image=rooms[item])
                    i += 1
        except:
            pass

def mUp(event):
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

#Setting up a basic Socket connection.
global serverSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect(("localhost", 1337))
#After sucessfull connection we expect an Handshake.
data = pickle.loads(serverSocket.recv(2048))
#Now we start rendering the GUI
root = tk.Tk()
#Just basic image importing.
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
#To sum it up: For every "list" append 5 tkinter Labels
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
