import config
import paho.mqtt.client as mqtt
import ssl
from walllight import WallLight
from clock import Clock

class MqttCli:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.needs_clock = False
        self.needs_wall = False
        self.paused= False
        self.light = WallLight()
        self.clock = Clock()

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(config.username, config.password)
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("connected")
        topics = [("wall/rgb1/#", 0), ("clock/rgb1/#", 0)]
        self.client.subscribe(topics)
        self.client.message_callback_add('wall/rgb1/rgb/set', self.on_message_wall_set)
        self.client.message_callback_add('clock/rgb1/rgb/set', self.on_message_clock_set)
        
    def on_message(self, client, userdata, msg):
        parts = msg.topic.split("/")
        last = parts[-1]
        first = parts[0]
        if last == "switch":
            msg1 = "OFF"
            msg2 = "OFF"
            print(msg.payload)

            if msg.payload.decode() == "OFF":
                self.needs_wall = False
                self.needs_clock = False
                msg1 = "OFF"
                msg2 = "OFF"
            elif first == "wall":
                self.needs_wall = True
                msg1 = "ON"
                msg2 = "OFF"
            elif first == "clock":
                self.needs_clock = True
                msg1 = "OFF"
                msg2 = "ON"
            self.client.publish("wall/rgb1/light/status", msg1)
            self.client.publish("clock/rgb1/light/status", msg2)

    def on_message_wall_set(self, client, userdata, msg):
        self.light.set_color(self.str2hex(msg.payload))
        self.needs_wall = True
        self.needs_clock = False
        self.client.publish("wall/rgb1/light/status", "ON")
        self.client.publish("clock/rgb1/light/status", "OFF")

    def on_message_clock_set(self, client, userdata, msg):
        self.clock.set_color(self.str2hex(msg.payload))
        self.needs_wall = False
        self.needs_clock = True 
        self.client.publish("wall/rgb1/light/status", "OFF")
        self.client.publish("clock/rgb1/light/status", "ON")


    def dissconnect(self):
        self.client.loop_stop()

    def needs_draw(self):
        return self.needs_wall or self.needs_clock

    def get_image(self):
        if self.needs_clock:
            return self.clock.getImage()
        if self.needs_wall:
            return self.light.getImage()
        self.light.set_color("00000000")
        return self.light.getImage()


    def str2hex(self, strng):
        colors = strng.decode().split(",")
        str = "%2x%2x%2x00" % (int(colors[0]), int(colors[1]), int(colors[2]))
        return str.replace(' ', '0')
