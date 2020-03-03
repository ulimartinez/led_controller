import config
import paho.mqtt.client as mqtt
import ssl

class MqttCli:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.color = None
        self.needs = False
        self.paused= False

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(config.username, config.password)
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('wall/rgb1/#')
        self.client.message_callback_add('wall/rgb1/rgb/set', self.on_message_set)
        
    def on_message(self, client, userdata, msg):
        print(msg.payload)
        last = msg.topic.split("/")[-1]
        print(last)
        if last == "switch":
            if msg.payload == "OFF":
                self.color = "000000"
                self.needs = True
                self.paused = True
            else:
                self.paused = False

    def on_message_set(self, client, userdata, msg):
        self.color = self.str2hex(msg.payload)
        self.paused = False
        self.needs = True
        print(self.color)


    def dissconnect(self):
        self.client.loop_stop()

    def needs_draw(self):
        if self.needs:
            self.needs = False
            return True

    def str2hex(self, strng):
        colors = strng.split(",")
        str = "%2x%2x%2x00" % (int(colors[0]), int(colors[1]), int(colors[2]))
        print(str)
        return str.replace(' ', '0')
