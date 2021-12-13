import socket
from threading import Thread

sock = socket.socket()
sock.bind(('127.0.0.1', 5050))
sock.listen(5)


def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data)
        conn.sendall(data)
    conn.close()


while True:
    conn, addr = sock.accept()
    print("Connection from " + str(addr))
    t = Thread(target=handle_connection, args=(conn,))
    t.start()

sock.close()