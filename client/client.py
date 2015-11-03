import pickle, socket, sys, threading, time
import tkinter as tk

def updateGui(labelList,rooms):
    while True:
        try:
            data = pickle.loads(serverSocket.recv(2048))
            if data[0] == "GUI":
                data.remove("GUI")
                i = 0
                for item in data:
                    labelList[i].configure(image=rooms[item])
                    i += 1
                labelList[12].configure(image=rooms["player"])
        except:
            pass

def up(event):
    serverSocket.send(pickle.dumps(["move","up"]))
def down(event):
    serverSocket.send(pickle.dumps(["move","down"]))
def right(event):
    serverSocket.send(pickle.dumps(["move","right"]))
def left(event):
    serverSocket.send(pickle.dumps(["move","left"]))
def space(event):
    serverSocket.send(pickle.dumps(["move","space"]))

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
rooms["wumpus"] = tk.PhotoImage(file="img/wumpus.gif")




frameList = []
labelList = []
#To sum it up: For every "list" append 5 tkinter Labels
for i in range(6):
    frameList.append( tk.Frame(bg="blue") )
for item in frameList[0:-1]:
    for i in range(5):
        labelList.append( tk.Label(item, image=rooms["e"], bd=0) )
for item in labelList:
    item.pack(side=tk.LEFT)
labelList.append( tk.Label(frameList[-1], height=3, text="I made this, but idk why.", bd=0).pack(side=tk.LEFT) )
labelList[12].configure(image=rooms["player"])
for item in frameList:
    item.pack()
#We start ouer GUI updater.
updateGuiThread = threading.Thread(target=updateGui, args=(labelList,rooms)).start()
#And we tell the server everything went well.
serverSocket.send(pickle.dumps(["Handshake","iShouldPutAnInputHere"]))

root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<space>", space)


root.mainloop()
