import socket

class App():
    def __init__(self):
        self.init_tcpIp = '0.0.0.0'
        self.init_tcpPort = 26100
        self.init_buffSize = 30

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

        print("[INFO] Sending data to server...")
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

    def initConnect(self):
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

        print("[INFO] Disconnecting Socket...")
        s.close()
        print("[INFO] Socket disconnected successfully")

    def getHand(self):
        hand=[]

        tcpPort = self.port
        tcpIp = '0.0.0.0'
        buffSize = 30

        s = self.createSocket()
        self.setupSocket(s, tcpIp, tcpPort)

        s.listen(1)
        print("[INFO] Socket is listening")

        c,addr = s.accept()
        print("[INFO] Connection address from",addr)

        while len(hand) < 7:
            data = self.reciveFromServer(c, buffSize)

            hand.append(data)

            # msg = f"{data}"
            # print("[INFO] Encoding data...")
            # msg = msg.encode('utf-8')

            # print("[INFO] Sending data to Client...")
            # c.send(msg)
            # print("[INFO] Data sent successfully to Client")

        print(hand)

    def run(self):
        self.initConnect()
        self.getHand()

if __name__ == "__main__":
    application = App()
    application.run()