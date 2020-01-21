import socket
import thread
from .event import Event
class GameServer:
    def __init__(self, server_host, server_port, client_host, client_port):
        self.s = socket.socket()
        self.s_host = server_host
        self.s_port = server_port
        self.c_host = client_host
        self.c_port = client_port
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.eventwatcher = Event()
        self.game = None

    def start(self):
        self.s.bind((self.s_host, self.s_port))
        self.c.connect((self.c_host, self.c_port))
        self.s.listen(5)
        while True:
            c, addr = s.accept()
            thread.start_new_thread(self.on_new_client, (c,addr))
        self.s.close()

    def on_new_client(self, client_sock, addr):
        while True:
            msg = client_sock.recv(1024)
            # do stuff with client messages
            if self.game is None:
                if 'snake' in msg:
                    self.game = Snake(20, 25)
            else:
                # fire all of the events
                self.eventwatcher += self.game.on_tick
                if 'left' in msg:
                    self.eventwatcher += self.game.on_left
                elif 'right' in msg:
                    self.eventwatcher += self.game.on_right
                elif 'up' in msg:
                    self.eventwatcher += self.game.on_up
                elif 'down' in msg:
                    self.eventwatcher += self.game.on_down

                self.eventwatcher()
                game_bytes = self.game.drawboard()
                self.c.sendall(game_bytes)
                self.eventwatcher.clear_handlers()


def main():
    server = GameServer('localhost', 8081, 'localhost', 8080)

if __name__ == '__main__':
    main()
