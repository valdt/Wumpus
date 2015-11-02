import pickle, socket, sys, threading, time
import tkinter as tk

def updateGui(labelList):
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
roomEmpty = tk.PhotoImage(file="img/floor1.gif")
roomBat = tk.PhotoImage(file="img/bat.gif")
roomPlayer = tk.PhotoImage(file="img/player.gif")

frameList = []
labelList = []
#To sum it up: For every "list" append 5 tkinter Labels
for i in range(6):
    frameList.append( tk.Frame(bg="blue") )
for item in frameList[0:-1]:
    for i in range(5):
        labelList.append( tk.Label(item, image=roomEmpty, bd=0) )
for item in labelList:
    item.pack(side=tk.LEFT)
labelList.append( tk.Label(frameList[-1], height=3, text="I made this, but idk why.", bd=0).pack(side=tk.LEFT) )
labelList[12].configure(image=roomPlayer)
for item in frameList:
    item.pack()

#We start ouer GUI updater.
updateGuiThread = threading.Thread(target=updateGui, args=(labelList))
#And we tell the server everything went well.
serverSocket.send(pickle.dumps(["Handshake","iShouldPutAnInputHere"]))

root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<space>", space)


root.mainloop()
