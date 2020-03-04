from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math
import requests
import logging
import http.client

http.client.HTTPConnection.debuglevel = 1

class Clock:
    def __init__(self):
        self.now = datetime.now()
        self.background = [255, 0, 0]
        self.time_color = [0,255,0]
        self.edge_color = [0,0,255]

    def getImage(self):
        self.now = datetime.now()
        hour = self.now.strftime('%H')
        minu = self.now.strftime('%M')
        sec = self.now.strftime('%S')
        color = 'rgb('+','.join(str(v) for v in self.background)+')'
        img = Image.new('RGB', (20, 25), color = color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/home/ulimartinez/.fonts/Roboto-Bold.ttf', size = 12)
        color = 'rgb(' + ','.join(str(v) for v in self.time_color) + ')'
        draw.text((3, 1), hour, fill=color, font=font)
        draw.text((3, 12), minu, fill=color, font=font)
        self.seconds_to_frame(int(sec), draw)
        return img


    def set_color(self, rgb):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        url = 'http://colormind.io/api/'
        params = {'input': [[int(rgb[:2], 16),
                                int(rgb[2:4], 16),
                                int(rgb[4:6], 16)], "N", "N", "N", "N"], 
                'model':'default'}
        print(params)
        r = requests.post(url = url, json = params)
        d = r.json()
        print(d)
        data = d['result']
        self.background = data[0]
        self.time_color = data[-1]
        self.edge_color = data[2]

    def seconds_to_frame(self, seconds, draw):
        start_x = 10
        start_y = 0
        off = 0
        if seconds < 7:
            off = math.floor(seconds *(1.4))+start_x
            draw.line(((start_x, start_y), (off, start_y)), fill='rgb(0,0,255)', width=1)
        elif seconds < 23:
            off=math.floor((seconds-7) *(1.56))
            draw.line(((start_x, start_y), 
                    (19, 0),
                    (19,off)), fill='rgb(0,0,255)', width=1)
        elif seconds < 37:
            off=19-math.floor((seconds-24) *(1.4))
            draw.line(((start_x, start_y), 
                    (19, 0),
                    (19,24),
                    (off,24)), fill='rgb(0,0,255)', width=1)
        elif seconds < 53:
            off = 24-math.floor((seconds-37) *(1.56))
            draw.line(((start_x, start_y), 
                    (19, 0),
                    (19,24),
                    (0,24),
                    (0,off)), fill='rgb(0,0,255)', width=1)
        else:
            off = math.floor((seconds-53) *(1.4))
            draw.line(((start_x, start_y), 
                    (19, 0),
                    (19,24),
                    (0,24),
                    (0,0),
                    (off,0)), fill='rgb(0,0,255)', width=1)
