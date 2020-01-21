from PIL import Image, ImageDraw, ImageFont

class WallLight:
    def __init__(self):
        self.color = None

    def set_color(self, color):
        self.color = color

    def getImage(self):
        img = Image.new('RGB', (20, 25), color = '#'+self.color)
        draw = ImageDraw.Draw(img)
        return img
