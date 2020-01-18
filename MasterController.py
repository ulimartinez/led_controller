#!/usr/bin/python
from mqttcli import MqttCli
from clock import Clock
from pixelutils import PixelUtils
from walllight import WallLight
from time import sleep
import socket

class MasterController:
    def __init__(self, clock, mqtt, host, port):
        self.clock = clock
        self.mqtt = mqtt
        self.host = host
        self.port = port
        self.utils = PixelUtils()
        self.light = WallLight()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wait = 11

    def run(self):
        self.mqtt.connect()
        self.s.connect((self.host, self.port))
        img = None
        while True:
            if self.mqtt.needs_draw():
                color = self.mqtt.color
                self.light.set_color(color)
                img = self.light.getImage()
                self.wait = 0
            if self.mqtt.paused:
                self.s.sendall(self.utils.image_to_bytearray(img))
                sleep(5)
                continue
            if self.wait> 10:
                img = self.clock.getImage()
            self.s.sendall(self.utils.image_to_bytearray(img))
            self.wait += 1
            sleep(0.5)
        
       
def main():
    mqttcli = MqttCli('mqtt.gbridge.io', 8883)
    clock = Clock()
    master = MasterController(clock, mqttcli, 'localhost', 8080)
    master.run()

if __name__ == '__main__':
    main()
