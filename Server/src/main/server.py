import socket
import thread

tcp_port = 26100
tcp_ip = '0.0.0.0'
buf_size = 30

x = 1

print("[INFO] Creating Socket...")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("[INFO] Socket successfully created")

s.bind((tcp_ip,tcp_port))
print("[INFO] Socket is binded to port",tcp_port)

s.listen(1)
print("[INFO] Socket is listening")

while x<=10:
    c,addr = s.accept()
    print("[INFO] Connection address from",addr)

    msg = f"{tcp_port+x}"
    print("[INFO] Encoding data...")
    msg = msg.encode('utf-8')

    print("[INFO] Sending data to Client...")
    c.send(msg)
    print("[INFO] Data sent successfully to Client")

    print("[INFO] Disconnecting Client connection...")
    c.close()

    x += 1

print("[INFO] Disconnecting Socket...")
s.close()
print("[INFO] Socket disconnected successfully")
