import socket

sock = socket.socket()
sock.connect(('localhost', 5050))
sock.send('hello, world!'.encode())

data = sock.recv(1024)
sock.close()

print(data)