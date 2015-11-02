class Player:
    def __init__(self,serverHandler,clientsocket):
        payload = ["handshake","404"]
        reData = serverHandler.pulse(payload,clientsocket)
        print(reData)
        if reData[0] == "handshake":
            self.name = reData[1]
