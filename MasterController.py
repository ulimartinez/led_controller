from .MqttCli import MqttCli
from .clock import Clock
from .pixelutils import PixelUtils
from time import sleep
import socket

class MasterController:
    def __init__(self, clock, mqtt, host, port):
        self.clock = clock
        self.mqtt = mqtt
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.mqtt.connect()
        self.s.connect((self.host, self.port))
        while True:
            img = self.clock.getImage()
            s.sendall(PixelUtils.image_to_bytearray(img))
            sleep(0.5)
       
def main():
    mqtt = MqttCli('mqtt.gbridge.io', 8883)
    clock = Clock()
    master = MasterController(clock, mqtt, 'localhost', 8080)

if __name__ == '__main__':
    main()
