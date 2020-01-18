import socket
import thread
from .event import Event
class GameServer:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.eventwatcher = Event()
        self.game = None

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
                self.eventwatcher.clear_handlers()
