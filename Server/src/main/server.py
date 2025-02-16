# Author: Thomas Preston

import socket
import random
from os import path
import logging

class Server():
    def __init__(self):
        self.init_tcpIp = '0.0.0.0'
        self.init_tcpPort = 26100
        self.init_buffSize = 30
        
        scriptDir = path.dirname(path.abspath(__file__))
        logging.basicConfig(filename=f"{scriptDir}\\..\\logs\\server.log", format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('server')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Init ran sucessfully")
        self.logger.debug(f"This server is {socket.gethostname()} [{socket.gethostbyname(socket.gethostname())}]")

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

    def sendToClient(self, c, msg, buffSize, isSend=True):
        self.logger.info("Encoding data")
        e_msg = msg.encode('utf-8')

        self.logger.info("Sending data to client: {msg}")
        c.send(e_msg)

        if isSend:
            self.verifySendToClient(c, msg, buffSize)

    def verifySendToClient(self, c, msg, buffSize):
        self.logger.info("Verifying data send to client")
        data = self.reciveFromClient(c, buffSize, False)
        if data != msg:
            self.logger.critical("Mismatch in data sent back")
            self.logger.critical("Sent: {msg}")
            self.logger.critical("Recived {data}")
            raise IOError
        else:
            self.logger.info("Data sent successfully to client")

    def reciveFromClient(self, c, buffSize, isRecive=True):
        self.logger.info("Receiving data from client")
        data = c.recv(buffSize)

        self.logger.info("Decoding received data")
        data = data.decode('utf-8')

        self.logger.info("Received data from client: {data}")

        if isRecive:
            self.sendToClient(c, data, buffSize, False)

        return data

    def handshakeClients(self):
        self.logger.debug("Beginning handshake with clients")
        playerCounter = 1
        playerLimit = 10
        players = []

        s = self.createSocket()
        self.setupSocket(s, self.init_tcpIp, self.init_tcpPort)

        s.listen(1)
        self.logger.info("Socket is listening")

        while playerCounter<=playerLimit:
            c,addr = s.accept()
            self.logger.info(f"Connection address: {addr}")

            msg = f"{self.init_tcpPort+playerCounter}"
            self.sendToClient(c, msg, self.init_buffSize)

            if playerCounter == 1:
                data = self.reciveFromClient(c, self.init_buffSize)

                self.numPlayers = int(data)
                playerLimit = self.numPlayers

            players.append((addr[0], self.init_tcpPort+playerCounter))
            self.logger.info(f"Player {playerCounter} has joined")
            self.logger.debug(f"{players}")

            self.logger.info("Disconnecting client connection")
            c.close()

            playerCounter += 1

        self.endSocket(s)
        self.players = players

    def game(self):
        self.logger.debug("Begining game")
        self.deck = self.generateDeck()
        self.discardDeck = []
        self.logger.debug(f"Main Deck: {self.deck}")
        self.logger.debug(f"Discard Deck: {self.discardDeck}")
        self.sendPlayerHand()
        self.discardDeck.append(self.deck[0])
        self.deck.pop(0)
        won = False
        while not won:
            won = self.turn()

    def generateDeck(self):
        deck=[]
        for suit in ["Spade", "Club", "Heart", "Diamonds"]:
            suitList = list(range(2,11))
            suitList.extend(["Jack", "Queen", "King", "Ace"])
            for card in suitList:
                deck.append(suit+str(card))

        random.shuffle(deck)
        return deck
    
    def sendPlayerHand(self):
        for player in self.players:
            tcpIp = player[0]
            tcpPort = player[1]
            buffSize = 30

            s = self.createSocket()

            self.logger.info(f"Connecting socket to port")
            s.connect((tcpIp, tcpPort))
            self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

            for i in range(7):
                msg = self.deck[0]
                self.deck.pop(0)
                self.sendToClient(s, msg, buffSize)
                self.logger.debug(f"Card: {msg}")

            self.endSocket(s)

    def turn(self):
        self.logger.debug(f"Main Deck: {self.deck}")
        self.logger.debug(f"Discard Deck: {self.discardDeck}")
        tcpIp = self.players[0][0]
        tcpPort = self.players[0][1]
        buffSize = 30

        s = self.createSocket()

        self.logger.info(f"Connecting socket to port")
        s.connect((tcpIp, tcpPort))
        self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

        data = self.reciveFromClient(s, buffSize)

        if data == "u":
            self.sendToClient(s, self.discardDeck[-1], buffSize)
            self.discardDeck.pop(-1)
        elif data == "h":
            self.sendToClient(s, self.deck[0], buffSize)
            self.deck.pop(0)

        self.logger.debug(f"Main Deck: {self.deck}")
        self.logger.debug(f"Discard Deck: {self.discardDeck}")

        data = self.reciveFromClient(s, buffSize)
        self.discardDeck.append(data)

        self.logger.debug(f"Main Deck: {self.deck}")
        self.logger.debug(f"Discard Deck: {self.discardDeck}")

        data = self.reciveFromClient(s, buffSize)
        if data == "y":
            for player in self.players:
                tcpIp = player[0]
                tcpPort = player[1]
                buffSize = 30

                s = self.createSocket()

                self.logger.info(f"Connecting socket to port")
                s.connect((tcpIp, tcpPort))
                self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

                msg = "exit"
                self.sendToClient(s, msg, buffSize)

                self.endSocket(s)
            return True
        
        self.endSocket(s)
        
        if len(self.deck) == 0:
            self.deck, self.discardDeck = self.discardDeck[:-1], [].append(self.discardDeck[-1])

        self.logger.debug(f"Main Deck: {self.deck}")
        self.logger.debug(f"Discard Deck: {self.discardDeck}")

        for player in self.players:
            tcpIp = player[0]
            tcpPort = player[1]
            buffSize = 30

            s = self.createSocket()

            self.logger.info(f"Connecting socket to port")
            s.connect((tcpIp, tcpPort))
            self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

            msg = self.discardDeck[-1]
            self.sendToClient(s, msg, buffSize)

            self.endSocket(s)
        
        self.logger.debug(f"Players: {self.players}")
        self.players.append(self.players.pop(0))
        self.logger.debug(f"Players: {self.players}")

        tcpIp = self.players[0][0]
        tcpPort = self.players[0][1]
        buffSize = 30

        s = self.createSocket()

        self.logger.info(f"Connecting socket to port")
        s.connect((tcpIp, tcpPort))
        self.logger.info(f"Socket connected successfully: {tcpIp}:{tcpPort}")

        msg = "go"
        self.sendToClient(s, msg, buffSize)

        self.endSocket(s)

    def run(self):
        self.handshakeClients()
        self.game()

if __name__ == "__main__":
    server = Server()
    try:
        # server.run()
        server.logger.info('Program ran successfully')
        server.logger.info('Exited with error code 0')
        exit(0)
    except Exception as e:
        server.logger.fatal('Uh oh, a problem has occured')
        if e != "":
            server.logger.fatal(e)
        raise SystemExit