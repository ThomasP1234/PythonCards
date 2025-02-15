import socket

class App():
    def __init__(self):
        self.init_tcpIp = '0.0.0.0'
        self.init_tcpPort = 26100
        self.init_buffSize = 30
        self.player1 = False

    def createSocket(self):
        print("[INFO] Creating socket...")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[INFO] Socket successfully created")

        return s
    
    def endSocket(self, s):
        print("[INFO] Disconnecting Socket...")
        s.close()
        print("[INFO] Socket disconnected successfully")
    
    def setupSocket(self, s, tcpIp, tcpPort):
        s.bind((tcpIp,tcpPort))
        print("[INFO] Socket is binded to port",tcpPort)

    def sendToServer(self, c, msg, buffSize, isSend=True):
        print("[INFO] Encoding data...")
        e_msg = msg.encode('utf-8')

        print(f"[INFO] Sending data to server... {msg}")
        c.send(e_msg)

        if isSend:
            self.verifySendToServer(c, msg, buffSize)

    def verifySendToServer(self, c, msg, buffSize):
        print("[INFO] Verifying data send to server")
        data = self.reciveFromServer(c, buffSize, False)
        if data != msg:
            print("[ERROR] Data recived from server did not match data send")
            raise IOError
        else:
            print("[INFO] Data sent successfully to server")

    def reciveFromServer(self, c, buffSize, isRecive=True):
        print("[INFO] Receiving data from Server...")
        data = c.recv(buffSize)

        print("[INFO] Decoding received data...")
        data = data.decode('utf-8')

        print("[INFO] Received data from server : ",data)

        if isRecive:
            self.sendToServer(c, data, buffSize, False)

        return data

    def handshakeServer(self):
        tcpIp = '192.168.1.194'
        tcpPort = 26100
        buffSize = 30

        s = self.createSocket()

        print("[INFO] Connecting Socket to port",tcpPort)
        s.connect((tcpIp,tcpPort))
        print("[INFO] Socket connected successfully to port",tcpPort)

        data = self.reciveFromServer(s, buffSize)

        self.port = int(data)

        if data == "26101":
            msg = input("Enter the number of players ")
            self.sendToServer(s, msg, buffSize)
            self.player1 = True

        self.endSocket(s)

    def getHand(self):
        self.hand=[]

        tcpPort = self.port
        tcpIp = '0.0.0.0'
        buffSize = 30

        s = self.createSocket()
        self.setupSocket(s, tcpIp, tcpPort)

        s.listen(1)
        print("[INFO] Socket is listening")

        c,addr = s.accept()
        print("[INFO] Connection address from",addr)

        while len(self.hand) < 7:
            data = self.reciveFromServer(c, buffSize)

            self.hand.append(data)

        print("[INFO] Hand from server is",self.hand)

        print("[INFO] Disconnecting Client connection...")
        c.close()

        self.endSocket(s)

    def turn(self):
        goAgain = True

        tcpPort = self.port
        tcpIp = '0.0.0.0'
        buffSize = 30

        s = self.createSocket()
        self.setupSocket(s, tcpIp, tcpPort)

        s.listen(1)
        print("[INFO] Socket is listening")

        if self.player1:
            myGo = True
        else:
            myGo=False

        while goAgain:
            while not myGo:
                c,addr = s.accept()
                print("[INFO] Connection address from",addr)

                data = self.reciveFromServer(c, buffSize)

                print("[INFO] Disconnecting Client connection...")
                c.close()

                if data != "go":
                    pass
                    # self.updateDiscard(data)
                else:
                    myGo = True

            c,addr = s.accept()
            print("[INFO] Connection address from",addr)

            self.sendToServer(c, input("hidden (h) or upturned (u) "), buffSize)

            print(self.hand)
            self.hand.append(self.reciveFromServer(c, buffSize))
            print(self.hand)

            self.sendToServer(c, card:=self.hand[int(input("0-7"))], buffSize)
            self.hand.remove(card)
            print(self.hand)

            self.sendToServer(c, input("win? y,n"), buffSize)

            print("[INFO] Disconnecting Client connection...")
            c.close()

            myGo=False

    def run(self):
        self.handshakeServer()
        self.getHand()
        self.turn()

if __name__ == "__main__":
    application = App()
    application.run()