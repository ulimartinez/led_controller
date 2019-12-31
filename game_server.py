import socket
import thread
import .event
class GameServer:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        while True:
            c, addr = s.accept()
            thread.start_new_thread(self.on_new_client, (c,addr))
        self.s.close()

    def on_new_client(self, client_sock, addr):
        while True:
            msg = client_sock.recv(1024)
            # do stuff with client messages
