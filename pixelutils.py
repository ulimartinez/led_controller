class PixelUtils:
    def __init__(self):
        pass

    @staticmethod
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
    
    @staticmethod
    def board_to_bytes(board):
        byt = None
        width, height = len(board[0]), len(board) 
        for x in range(width):
            if x % 2 == 0:
                for y in range(height-1, -1, -1):
                    pixelstr=board[y][x]
                    if byt is None:
                        byt = bytearray.fromhex(pixelstr)
                    else:
                        byt += bytearray.fromhex(pixelstr)
            else:
                for y in range(height):
                    pixelstr= board[y][x]
                    if byt is None:
                        byt = bytearray.fromhex(pixelstr)
                    else:
                        byt += bytearray.fromhex(pixelstr)
        return byt

    @staticmethod
    def empty_bytes(width, height):
        byt = bytearray.fromhex('00000000')
        for x in range(width*height-1):
            byt += bytearray.fromhex('00000000')
        return byt
