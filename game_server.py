#!/usr/bin/python3
import socket
import websockets
import asyncio
from event import Event
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
        self.server = None
        self.game_playing = None
        self.ticks = 0

    def start(self):
        print("starting web socket on port "+str(self.s_port))
        self.server  = websockets.serve(self.game, None, self.s_port)
        print("started websocket")
        self.c.connect((self.c_host, self.c_port))
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()
        self.s.close()

    async def game(self, websocket, path):
        while True:
            message = await websocket.recv()
            self.consumer(message)
        #self.close_conn()
            

    def consumer(self, msg):
        if self.game_playing is None:
            if 'snake' in msg:
                self.game_playing = Snake(20, 25)
        else:
            # fire all of the events
            if self.ticks >= 0:
                self.eventwatcher += self.game_playing.on_tick
                self.ticks = 0
            if 'left' in msg:
                self.eventwatcher += self.game_playing.on_left
            elif 'right' in msg:
                self.eventwatcher += self.game_playing.on_right
            elif 'up' in msg:
                self.eventwatcher += self.game_playing.on_up
            elif 'down' in msg:
                self.eventwatcher += self.game_playing.on_down

            self.eventwatcher()
            game_bytes = self.game_playing.draw_board()
            self.c.sendall(game_bytes)
            self.eventwatcher.clear_handlers()
        self.ticks +=1
        time.sleep(0.1)

    def is_playing(self):
        if self.game_playing is None:
            return True
        else:
            return self.game_playing.playing

    def close_conn(self):
        self.c.close()

def main():
    server = GameServer('localhost', 3400, 'localhost', 8080)
    print("going to start the game server")
    server.start()

if __name__ == '__main__':
    main()
