import paho.mqtt.client as mqtt

class MqttCli:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('gBridge/u4267/d14453/#')
        
    def on_message(self, client, userdata, msg):
        print(msg.topic)
