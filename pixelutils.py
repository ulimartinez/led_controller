class PixelUtils:
    def __init__(self):
        pass

    def image_to_bytearray(self, image):
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
