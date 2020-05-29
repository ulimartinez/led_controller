#!/usr/bin/python3
import socket
import websockets
import asyncio
from text import Text
from event import Event
from threading import Lock, Thread 
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
        self.game = Text()
        self.lock = Lock()

    def start(self):
        self.server  = websockets.serve(self.game_messages, None, self.s_port)
        self.c.connect((self.c_host, self.c_port))
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()
        self.s.close()

    async def game_messages(self, websocket, path):
        while True:
            message = await websocket.recv()
            self.consumer(message)
        #self.close_conn()
            

    def consumer(self, msg):
            # fire all of the events
            [message, nick] = msg.split('|')
            print(nick)
            if len(nick) > 0 and nick != 'null' and nick != 'undefined':
                if len(message) > 0:
                    #with self.lock:
                    self.game.setText(message, nick)
            self.run_thread()



    def game_thread(self):
        if self.game is not None:
            #with self.lock:
            while True:
                self.eventwatcher += self.game.on_tick
                self.eventwatcher()
                game_bytes = self.game.getImage()
                self.c.sendall(game_bytes)
                self.eventwatcher.clear_handlers()
                time.sleep(1/4)
            self.game = None

    def run_thread(self):
        game_thread = Thread(target = self.game_thread)
        game_thread.start()

    def is_playing(self):
        if self.game is None:
            return True
        else:
            return self.game.playing


def main():
    server = GameServer('localhost', 3500, 'localhost', 8080)
    print("going to start the cheer server")
    server.start()

if __name__ == '__main__':
    main()
