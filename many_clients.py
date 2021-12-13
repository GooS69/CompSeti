import socket

sock1 = socket.socket()
sock1.connect(('localhost', 5050))
sock1.send('hello, world!'.encode())

sock2 = socket.socket()
sock2.connect(('localhost', 5050))
sock2.send('hello, world!'.encode())

sock3 = socket.socket()
sock3.connect(('localhost', 5050))
sock3.send('hello, world!'.encode())

data1 = sock1.recv(1024)
data2 = sock2.recv(1024)
data3 = sock3.recv(1024)
sock1.close()
sock2.close()
sock3.close()

print(data1, data2, data3)