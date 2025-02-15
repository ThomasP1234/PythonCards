import socket
import random

class Server():
    def initConnect(self):
        tcp_port = 26100
        tcp_ip = '0.0.0.0'
        buf_size = 30

        x = 1
        playerLimit = 10
        players = []

        print("[INFO] Creating Socket...")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[INFO] Socket successfully created")

        s.bind((tcp_ip,tcp_port))
        print("[INFO] Socket is binded to port",tcp_port)

        s.listen(1)
        print("[INFO] Socket is listening")

        while x<=playerLimit:
            c,addr = s.accept()
            print("[INFO] Connection address from",addr)

            msg = f"{tcp_port+x}"
            print("[INFO] Encoding data...")
            msg = msg.encode('utf-8')

            print("[INFO] Sending data to Client...")
            c.send(msg)
            print("[INFO] Data sent successfully to Client")

            if x == 1:
                print("[INFO] Receiving Data from Client...")
                data = c.recv(buf_size)

                print("[INFO] Decoding received data...")
                data = data.decode('utf-8')

                print("[INFO] Received Data from Client : ",data)

                self.numPlayers = int(data)
                playerLimit = self.numPlayers

            players.append((addr[0], tcp_port+x))

            print("[INFO] Disconnecting Client connection...")
            c.close()

            x += 1

        print("[INFO] Disconnecting Socket...")
        s.close()
        print("[INFO] Socket disconnected successfully")
        self.players = players

    def game(self):
        self.deck = self.generateDeck()
        self.sendPlayerHand()

    def generateDeck(self):
        deck=[]
        for suit in ["spades", "clubs", "hearts", "diamonds"]:
            suitList = list(range(2,11))
            suitList.extend(["jack", "queen", "king", "ace"])
            for card in suitList:
                deck.append(suit+str(card))

        random.shuffle(deck)
        return deck
    
    def sendPlayerHand(self):
        for player in self.players:
            tcp_ip = player[0]
            tcp_port = player[1]
            buf_size = 30

            print("[INFO] Creating Socket...")
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print("[INFO] Socket successfully created")

            print("[INFO] Connecting Socket to port",tcp_port)
            s.connect((tcp_ip,tcp_port))
            print("[INFO] Socket connected successfully to port",tcp_port)

            for i in range(7):
                msg = self.deck[0]
                self.deck.pop(0)
                print("[INFO] Encoding data...")
                msg = msg.encode('utf-8')

                print("[INFO] Sending data to Client...")
                s.send(msg)
                print("[INFO] Data sent successfully to Client")

                print("[INFO] Receiving Data from server")
                data = s.recv(buf_size)

                if data == msg:
                    continue
                else:
                    raise Exception

    def run(self):
        self.initConnect()
        self.game()

if __name__ == "__main__":
    server = Server()
    server.run()