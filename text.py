import re
from PIL import Image, ImageDraw, ImageFont
import math
from pixelutils import PixelUtils


class Text:
    def __init__(self):
        self.img = Image.new('RGB', (25, 20), color = 'rgb(0,0,0)')
        self.text = 'cheer1'
        self.x = 20
        self.ticks = 0
        self.color = 'rgb(0, 0, 102)'
        self.usr = 'cheer1'

    def setText(self, text, usr):
        p = re.compile('cheer[0-9]*')
        self.text = p.sub('', text)
        self.usr = usr

    def getImage(self):
        self.img = Image.new('RGB', (25, 20), color = 'rgb(0,0,0)')
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype('/home/ulimartinez/.fonts/Roboto-Bold.ttf', size = 15)
        font2 = ImageFont.truetype('/home/ulimartinez/.fonts/Roboto-Bold.ttf', size = 10)
        for i, c in enumerate(self.text):
            if c == ' ':
                draw.text((self.x+(i*7), 4), c, fill=self.color, font=font)
            else:
                draw.text((self.x+(i*11), 4), c, fill=self.color, font=font)

        self.img = self.img.transpose(Image.ROTATE_270)

        bytes_array = PixelUtils.image_to_bytearray(self.img)
        return bytes_array 

    def on_tick(self):
        self.moveText()

    def on_tick2(self):
        speed =1 
        if self.ticks > 100:
            self.ticks = 0
        self.ticks = self.ticks + 1
        if self.ticks % speed == 0:
            self.moveText()

    def moveText(self):
        if self.x < len(self.text) * -20:
            self.x = 20
        self.x = self.x - 2

    def getBlank(self):
        return PixelUtils.empty_bytes(20, 25)
