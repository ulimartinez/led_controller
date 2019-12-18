from .MqttCli import MqttCli

class MasterController:
    def __init__(self, clock, mqtt):
        self.clock = clock
        self.mqtt = mqtt
       
def main():
    mqtt = MqttCli('mqtt.gbridge.io', 8883)
if __name__ == '__main__':
    main()
