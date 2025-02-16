# Author: Thomas Preston

import socket
from os import path
import logging

class App():
    def __init__(self):
        self.init_tcpIp = '0.0.0.0'
        self.init_tcpPort = 26100
        self.init_buffSize = 30
        self.player1 = False

        scriptDir = path.dirname(path.abspath(__file__))
        logging.basicConfig(filename=f"{scriptDir}\\..\\logs\\client-{socket.gethostname()}.log", 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('client')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Init ran sucessfully")
        self.logger.debug(f"This client is {socket.gethostname()} [{socket.gethostbyname(socket.gethostname())}]")

    def createSocket(self):
        self.logger.info("Creating socket")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.logger.info("Socket successfully created")

        return s
    
    def endSocket(self, s):
        self.logger.info("Disconnecting socket")
        s.close()
        self.logger.info("Socket disconnected successfully")
    
    def setupSocket(self, s, tcpIp, tcpPort):
        s.bind((tcpIp,tcpPort))
        self.logger.info(f"Socket is binded to: {tcpIp}:{tcpPort}")

    def sendToServer(self, c, msg, buffSize, isSend=True):
        self.logger.info("Encoding data")
        e_msg = msg.encode('utf-8')

        self.logger.info("Sending data to server: {msg}")
        c.send(e_msg)

        if isSend:
            self.verifySendToServer(c, msg, buffSize)

    def verifySendToServer(self, c, msg, buffSize):
        self.logger.info("Verifying data send to server")
        data = self.reciveFromServer(c, buffSize, False)
        if data != msg:
            self.logger.critical("Mismatch in data sent back")
            self.logger.critical(f"Sent: {msg}")
            self.logger.critical(f"Recived {data}")
            raise IOError
        else:
            self.logger.info("Data sent successfully to server")

    def reciveFromServer(self, c, buffSize, isRecive=True):
        self.logger.info("Receiving data from server")
        data = c.recv(buffSize)

        self.logger.info("Decoding received data")
        data = data.decode('utf-8')

        self.logger.info("Received data from server: {data}")

        if isRecive:
            self.sendToServer(c, data, buffSize, False)

        return data

    def handshakeServer(self):
        self.logger.debug("Beginning handshake with server")
        tcpIp = '192.168.1.194'
        tcpPort = 26100
        buffSize = 30

        s = self.createSocket()

        self.logger.info(f"Connecting socket to port")
        s.connect((tcpIp,tcpPort))
        self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

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
        self.logger.info("Socket is listening")

        c,addr = s.accept()
        self.logger.info(f"Connection address: {addr}")

        while len(self.hand) < 7:
            data = self.reciveFromServer(c, buffSize)

            self.hand.append(data)

        self.logger.debug(f"Hand: {self.hand}")

        self.logger.info("Disconnecting client connection")
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
        self.logger.info("Socket is listening")

        if self.player1:
            myGo = True
        else:
            myGo=False

        exit = False
        while goAgain:
            while not myGo:
                c,addr = s.accept()
                self.logger.info(f"Connection address: {addr}")

                data = self.reciveFromServer(c, buffSize)

                self.logger.info("Disconnecting client connection")
                c.close()

                if data == "go":
                    myGo = True
                elif data == "exit":
                    exit = True
                    break
                else:
                    pass
                    # self.updateDiscard(data)

            if exit: break

            c,addr = s.accept()
            self.logger.info(f"Connection address: {addr}")

            self.sendToServer(c, input("hidden (h) or upturned (u) "), buffSize)

            self.logger.debug(f"Hand: {self.hand}")
            self.hand.append(self.reciveFromServer(c, buffSize))
            self.logger.debug(f"Hand: {self.hand}")

            self.sendToServer(c, card:=self.hand[int(input("0-7 "))], buffSize)
            self.hand.remove(card)
            self.logger.debug(f"Hand: {self.hand}")

            self.sendToServer(c, input("win? y,n "), buffSize)

            self.logger.info("Disconnecting client connection")
            c.close()

            myGo=False

    def run(self):
        self.handshakeServer()
        self.getHand()
        self.turn()

if __name__ == "__main__":
    application = App()
    try:
        application.run()
        application.logger.info('Program ran successfully')
        application.logger.info('Exited with error code 0')
        exit(0)
    except Exception as e:
        application.logger.fatal('Uh oh, a problem has occured')
        if e != "":
            application.logger.fatal(e)
        raise SystemExit