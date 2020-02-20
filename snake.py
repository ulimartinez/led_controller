from game import Game
from pixelutils import PixelUtils
from colors import color
import random
class Snake(Game):
    def __init__(self, w, h):
        super(Snake, self).__init__(w, h)
        self.snake = [(1,1)]
        self.snake_len = 1
        self.dir = 'r'
        self.playing = True
        self.food = self.generate_food()
        self.place_snake()
        self.place_food()
        
    def isValid(self, tup):
        x, y = tup
        return self.board[y][x] == 0

    def generate_food(self):
        r1 = random.randint(0, self.w-1)
        r2 = random.randint(0, self.h-1)
        while not self.isValid((r1, r2)):
            r1 = random.randint(0, self.w-1)
            r2 = random.randint(0, self.h-1)

        return (r1, r2)

    def place_snake(self):
        for tup in self.snake:
            x, y = tup
            self.board[y][x] = 1

    def place_food(self):
        x, y = self.food
        self.board[y][x] = 3

    def move_snake(self):
        head_x, head_y = self.snake[self.snake_len-1]
        next_x = head_x
        next_y = head_y
        if self.dir == 'r':
            if head_x == len(self.board[0])-1:
                self.playing = False
                return
            next_x = head_x + 1
        elif self.dir == 'l':
            if head_x == 0:
                self.playing = False
                return
            next_x = head_x - 1
        elif self.dir == 'u':
            if head_y == 0:
                self.playing = False
                return
            next_y = head_y - 1
        elif self.dir == 'd':
            if head_y == len(self.board)-1:
                self.playing = False
                return
            next_y = head_y+1

        if self.board[next_y][next_x] not in (0, 3):
            self.playing = False
            return
        self.snake.append((next_x, next_y))

        if self.board[next_y][next_x] != 3:
            self.snake.pop(0)
        else:
            self.snake_len+= 1
            self.food = self.generate_food()


    def on_tick(self):
        self.clear_board()
        self.place_food()
        self.place_snake()
        self.move_snake()


    def on_left(self):
        if self.dir != 'r':
            self.dir = 'l'
    def on_right(self):
        if self.dir != 'l':
            self.dir = 'r'
    def on_up(self):
        if self.dir != 'd':
            self.dir = 'u'
    def on_down(self):
        if self.dir != 'u':
            self.dir = 'd'

    def draw_board(self):
        board_state = [[color['white'] if x>0 else color['black'] for x in row] for row in self.board]
        bytes_array = PixelUtils.board_to_bytes(board_state)
        return bytes_array

