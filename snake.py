import .game
from .colors import colors
import random
class Snake(Game):
    def __init__(self, w, h):
        super().__init__(w, h)
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
        r1 = random.randint(0, len(board))
        r2 = random.randint(0, len(board[0]))
        while !isValid((r2, r1)):
            r1 = random.randint(0, len(board))
            r2 = random.randint(0, len(board[0]))

        return (r2, r1)

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
            next_y = head_y + 1
        elif self.dir == 'd':
            if head_y == len(self.board)-1:
                self.playing = False
                return
            next_y = head_y+1

        self.snake.append((next_x, next_y))

        if board[next_y][next_x] != 3:
            self.snake.pop(0)
        else:
            self.snake_len+= 1

    def on_tick(self):
            self.clear_board()
            self.move_snake()
            self.place_snake()
            self.place_food()

    def on_keypress(self, data):
        if data in 'lrud':
            self.dir = data

    def draw_board(self):
        board_state = [[color.white if x > 0 for x in row] for row in self.board]
        bytes_array = PixelUtils.board_to_bytes(board_state)
        return bytes_array

