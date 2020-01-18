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
        self.client.tls_set(ca_certs='/etc/ssl/certs/LetsEncrypt-AllCAs.pem', certfile=None,keyfile=None, cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) 
        self.client.tls_insecure_set(False)
        self.client.username_pw_set(config.username, config.password)
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('gBridge/u4267/d14453/#')
        
    def on_message(self, client, userdata, msg):
        print(msg.payload)
        last = msg.topic.split("/")[-1]
        print(last)
        if last == "colorsettingrgb":
            self.color = msg.payload
            self.paused = False
            self.needs = True
        if last == "onoff":
            if msg.payload == "0":
                self.color = "000000"
                self.needs = True
                self.paused = True
            else:
                self.paused = False

    def dissconnect(self):
        self.client.loop_stop()

    def needs_draw(self):
        if self.needs:
            self.needs = False
            return True
