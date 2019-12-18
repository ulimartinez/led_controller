#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime
from time import sleep
import socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    s.connect(('localhost', port))
    
    while True:
        now = datetime.now()
        hour = now.strftime('%H')
        minu = now.strftime('%M')
        sec = now.strftime('%S')
        img = Image.new('RGB', (20, 25), color = 'red')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/home/ulimartinez/.fonts/Roboto-Bold.ttf', size = 12)
        color = 'rgb(0, 255, 0)'
        draw.text((3, 1), hour, fill=color, font=font)
        draw.text((3, 12), minu, fill=color, font=font)
        seconds_to_frame(int(sec), draw)
        s.sendall(image_to_bytearray(img))
        sleep(0.5)

def image_to_bytearray(image):
    byt = None
    width, height = image.size
    for x in range(width):
        if x % 2 == 0:
            for y in range(height-1, -1, -1):
                r, g, b = image.getpixel((x, y))
                pixelstr= '%2X%2X%2X00' % (g, r, b)
                pixelstr= pixelstr.replace(' ', '0')
                if byt is None:
                    byt = bytearray.fromhex(pixelstr)
                else:
                    byt += bytearray.fromhex(pixelstr)
        else:
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                pixelstr= '%2X%2X%2X00' % (g, r, b)
                pixelstr= pixelstr.replace(' ', '0')
                if byt is None:
                    byt = bytearray.fromhex(pixelstr)
                else:
                    byt += bytearray.fromhex(pixelstr)
    return byt

def seconds_to_frame(seconds, draw):
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

           

if __name__ == "__main__":
    main()
