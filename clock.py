from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math
class Clock:
    def __init__(self):
        self.now = datetime.now()

    def getImage(self):
        self.now = datetime.now()
        hour = self.now.strftime('%H')
        minu = self.now.strftime('%M')
        sec = self.now.strftime('%S')
        img = Image.new('RGB', (20, 25), color = 'red')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/home/ulimartinez/.fonts/Roboto-Bold.ttf', size = 12)
        color = 'rgb(0, 255, 0)'
        draw.text((3, 1), hour, fill=color, font=font)
        draw.text((3, 12), minu, fill=color, font=font)
        self.seconds_to_frame(int(sec), draw)
        return img


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
