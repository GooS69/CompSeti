#coding: utf-8
import socket

f = open('output.txt', 'w+')

sock = socket.socket()
sock.connect(('82.179.130.30', 80))
request = "GET / HTTP/1.1\r\n" \
          "Host: pmk.tversu.ru\r\n" \
          "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) " \
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36\r\n" \
          "Accept: */*\r\n\r\n"
sock.send(request.encode())


while True:
    data = sock.recv(1024)
    if not data:
        break
    f.write(data.decode('windows-1251', 'ignore'))

f.close()
sock.close()
