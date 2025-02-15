import socket

class App():
    def initConnect(self):
        tcp_port = 26100
        tcp_ip = '192.168.1.194'
        buf_size = 30

        print("[INFO] Creating Socket...")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[INFO] Socket successfully created")

        print("[INFO] Connecting Socket to port",tcp_port)
        s.connect((tcp_ip,tcp_port))
        print("[INFO] Socket connected successfully to port",tcp_port)

        print("[INFO] Receiving Data from server")
        data = s.recv(buf_size)

        print("[INFO] Decoding received data...")
        data = data.decode('utf-8')

        print('[INFO] Data received from Server : ',data)

        self.port = int(data)

        if data == "26101":
            msg = input("Enter the number of players ")
            print("[INFO] Encoding data...")
            msg = msg.encode('utf-8')

            print("[INFO] Sending data to Server...")
            s.send(msg)
            print("[INFO] Data sent successfully to Server")

        print("[INFO] Disconnecting Socket...")
        s.close()
        print("[INFO] Socket disconnected successfully")

    def getHand(self):
        hand=[]

        tcp_port = self.port
        tcp_ip = '0.0.0.0'
        buf_size = 30

        print("[INFO] Creating Socket...")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[INFO] Socket successfully created")

        s.bind((tcp_ip,tcp_port))
        print("[INFO] Socket is binded to port",tcp_port)

        s.listen(1)
        print("[INFO] Socket is listening")

        c,addr = s.accept()
        print("[INFO] Connection address from",addr)

        while len(hand) < 7:
            print("[INFO] Receiving Data from Client...")
            data = c.recv(buf_size)

            print("[INFO] Decoding received data...")
            data = data.decode('utf-8')

            print("[INFO] Received Data from Client : ",data)

            hand.append(data)

            msg = f"{data}"
            print("[INFO] Encoding data...")
            msg = msg.encode('utf-8')

            print("[INFO] Sending data to Client...")
            c.send(msg)
            print("[INFO] Data sent successfully to Client")

        print(hand)

    def run(self):
        self.initConnect()
        self.getHand()

if __name__ == "__main__":
    application = App()
    application.run()