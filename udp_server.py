import socket

udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_server_socket.bind(("127.0.0.1", 25565))

print("UDP server up and listening")

while True:
    message, address = udp_server_socket.recvfrom(1024)
    print(f"Message from Client:{message}")
    print(f"Client IP Address:{address}")
    udp_server_socket.sendto("Hello UDP Client".encode(), address)
