#!/usr/bin/python
from mqttcli import MqttCli
from clock import Clock
from pixelutils import PixelUtils
from walllight import WallLight
from time import sleep
import socket

class MasterController:
    def __init__(self, mqtt, host, port):
        self.mqtt = mqtt
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.mqtt.connect()
        self.s.connect((self.host, self.port))
        img = None
        while True:
            img = self.mqtt.get_image()
            self.s.sendall(PixelUtils.image_to_bytearray(img))
            sleep(0.5)
        
       
def main():
    mqttcli = MqttCli('web.ulimartech.com', 1883)
    master = MasterController(mqttcli, 'localhost', 8080)
    master.run()

if __name__ == '__main__':
    main()
