#!/usr/bin/python
import socket
import thread
from snake import Snake
from event import Event
import time
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
        self.s.bind(('', self.s_port))
        self.c.connect((self.c_host, self.c_port))
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            c.setblocking(0)
            thread.start_new_thread(self.on_new_client, (c,addr))
        self.s.close()

    def on_new_client(self, client_sock, addr):
        print('got a new client lol')
        msg = "lNone"
        ticks = 0
        while self.is_playing():
            try:
                msg = client_sock.recv(1024)
            except socket.error:
                pass
            # do stuff with client messages
            if self.game is None:
                print("cake")
                if 'snake' in msg:
                    print("whats")
                    self.game = Snake(20, 25)
                    print("sacalo   ")
            else:
                # fire all of the events
                print("Hello my loved")
                if ticks >= 5:
                    self.eventwatcher += self.game.on_tick
                    ticks = 0
                if 'left' in msg:
                    self.eventwatcher += self.game.on_left
                elif 'right' in msg:
                    self.eventwatcher += self.game.on_right
                elif 'up' in msg:
                    self.eventwatcher += self.game.on_up
                elif 'down' in msg:
                    self.eventwatcher += self.game.on_down

                print("going to call the fire lol")
                self.eventwatcher()
                game_bytes = self.game.draw_board()
                print(''.join(format(x, '02X') for x in game_bytes))
                self.c.sendall(game_bytes)
                self.eventwatcher.clear_handlers()
            ticks +=1
            time.sleep(0.1)
        print("game over")
        self.close_conn()

    def is_playing(self):
        if self.game is None:
            return True
        else:
            return self.game.playing

    def close_conn(self):
        self.c.close()

def main():
    server = GameServer('localhost', 3400, 'localhost', 8080)
    print("going to start the game server")
    server.start()

if __name__ == '__main__':
    main()
