import socket

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

print("[INFO] Disconnecting Socket...")
s.close()
print("[INFO] Socket disconnected successfully")