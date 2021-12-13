import socket

udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_client_socket.sendto("Hello UDP Server".encode(), ("127.0.0.1", 25565))

msg_from_server = udp_client_socket.recvfrom(1024)
print("Message from Server {}".format(msg_from_server[0]))
