import socket
import logging
import threading
import sys


class EchoServer:
    BUFFER_SIZE = 1024

    # size limit in bytes for the client message to be received
    MAX_MSG_SIZE = 1024 * 5

    # this maps connected clients socket objects returned from accept() to their address tuple
    connected_clients = {}

    def __init__(self, port):
        self.hostname = 'localhost'
        self.port = port

        try:
            self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockfd.bind((self.hostname, self.port))
            self.sockfd.listen(10)
            self.sockfd.setblocking(False)

        except socket.error as e:
            logging.critical(e)
            logging.critical('Could not start up server. Exiting.')
            sys.exit(-1)

    def look_for_connections(self):
        while True:
            try:
                client_connfd, client_addr = self.sockfd.accept()
                logging.info('Connection from client {!r}'.format(client_addr))
                self.connected_clients[client_connfd] = client_addr

                client_handling_thread = threading.Thread(target=self.handle_client, args=(client_connfd,))
                client_handling_thread.start()

            except BlockingIOError:
                # no active clients trying to connect, nothing to do
                continue

    def handle_client(self, connfd: socket.socket):
        msg = self.get_client_msg(connfd)
        logging.info('Client: {} sent {} bytes.'.format(self.connected_clients[connfd], len(msg)))

        sent_bytes_size = self.send_client_msg(connfd, msg)
        logging.info('Server sent {} bytes to client: {!r}'.format(sent_bytes_size, self.connected_clients[connfd]))

        del self.connected_clients[connfd]
        connfd.close()

    def startup_server_loop(self):
        # this starts the main event loop (accepting connections from client)
        # each client get handled by its own thread
        server_thread = threading.Thread(target= self.look_for_connections)
        server_thread.start()

    def get_client_msg(self, connfd: socket.socket):
        data = b''

        while True:
            try:
                buffer = connfd.recv(self.BUFFER_SIZE)
                if len(buffer) == 0 or len(data) >= self.MAX_MSG_SIZE:
                    break
                else:
                    data += buffer
            except BlockingIOError:
                break
        return data

    def send_client_msg(self, connfd: socket.socket, msg: str):
        sent_bytes = 0
        total_bytes = len(msg)
        total_sent = 0

        if len(msg) == 0:
            return total_sent

        while True:
            try:
                sent_bytes = connfd.send(msg[sent_bytes: total_bytes])
                total_sent += sent_bytes

                if sent_bytes == 0:
                    return total_sent
            except BlockingIOError:
                return total_sent

            # in case client disconnected before sending the echo
            except ConnectionResetError:
                logging.info('Client {!r} disconnected before sending echo.'.format(self.connected_clients[connfd]))
                return total_sent

    def __del__(self):
        for client in self.connected_clients.keys():
            del self.connected_clients[client]
        self.sockfd.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    my_server = EchoServer(50000)
    my_server.startup_server_loop()