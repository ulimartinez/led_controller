from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080
    s.connect(('192.168.2.4', port))
    
    while True:
        now = datetime.now()
        hour = now.strftime('%H')
        minu = now.strftime('%M')
        img = Image.new('RGB', (20, 25), color = 'red')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/TTF/Koruri-Bold.ttf', size = 12)
        color = 'rgb(0, 255, 0)'
        draw.text((3, -3), hour, fill=color, font=font)
        draw.text((3, 10), minu, fill=color, font=font)
        s.sendall(image_to_bytearray(img))
        sleep(5)

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
           

if __name__ == "__main__":
    main()
