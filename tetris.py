from game import Game
from colors import color
import random
import numpy as np
class Tetris(Game):
    def __init__(self, height, width):
       super(Tetris, self).__init__(w, h)
       Omino = [
               [[1,1],
                [1,1]],
               [[1,1],
                [1,1]],
               [[1,1],
                [1,1]],
               [[1,1],
                [1,1]]
               ]
       Jmino = [
               [[2,0,0],
                [2,2,2]],
               [[2,2],
                [2,0],
                [2,0]],
               [[2,2,2],
                [0,0,2]],
               [[0,2],
                [0,2],
                [2,2]]
               ]
       Imino = [
               [[3,3,3,3]],
               [[3],
                [3],
                [3],
                [3]],
               [[3,3,3,3]],
               [[3],
                [3],
                [3],
                [3]]
               ]
       Lmino = [
               [[0,0,4],
                [4,4,4]],
               [[4,0],
                [4,0],
                [4,4]],
               [[4,4,4],
                [4,0,0]].
               [[4,4],
                [0,4],
                [0,4]]
               ]
       Smino = [
               [[0,5,5],
                [5,5,0]],
               [[5,0],
                [5,5],
                [0,5]],
               [[0,5,5],
                [5,5,0]],
               [[5,0],
                [5,5],
                [0,5]]
               ]
       Zmino = [
               [[6,6,0],
                [0,6,6]],
               [[0,6],
                [6,6],
                [6,0]],
               [[6,6,0],
                [0,6,6]],
               [[0,6],
                [6,6],
                [6,0]]
               ]
       self.minos = [Omino, Jmino, Imino, Lmino, Smino, Zmino]
       self.placed = np.zeros((24, 10), dtype=int)
       self.tetrimino = None
       self.tetrimino_position = (4, 0)
       self.r = 0
       self.ticks = 0
       self.spawn()

    def spawn(self):
        self.tetrimino = self.minos[random.randint(0,5)]
        self.tetrimino_position = (4, 0)

    def rotate(self, direction, r):
        if direction = 'cw':
            if r < 3:
                return r + 1
            else:
                return 0
        else:
            if r > 0:
                return r - 1
            else:
                return 3

    def check_fall(self, potential):
        p_x, p_y = potential
        piece = self.tetrimino[self.r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 0:
                    if self.placed[p_y + y][p_x + x] != 0:
                        return False
                    if p_y + y >= len(self.placed):
                        return False
        return True
    
    def check_move(self, potential):
        p_x, p_y = potential
        piece = self.tetrimino[self.r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 1:
                    if self.placed[p_y + y][p_x + x] != 0:
                        return False
                    if p_x + x < 0 or p_x + x >= len(self.placed):
                        return False
        return True

    def check_rotate(self, potential_r):
        t_x, t_y = self.tetrimino_position
        piece = self.tetrimino[portential_r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] !=0:
                    if t_x + x < 0 or t_x + x >= len(self.placed[0]):
                        return False
                    if t_y + y >= len(self.placed):
                        return False
                    if self.placed[t_y + y][t_x + x] != 0:
                        return False
        return True

    def check_clear(self):
        clear_ind =[] 
        for y in range(len(self.placed)):
            cleared = True
            for x in range(len(self.placed[0])):
                if self.placed[y][x] = 0:
                    cleared = False
            if cleared:
                clear_ind.append(y)
        for i in clear_ind:
            self.placed.pop(i)
            self.placed.insert(0, np.zeros(len(self.placed[0])))


    def fall(self):
        x, y = self.tetrimino_position
        if self.check_fall((x, y+1)):
            self.tetrimino_position = (x, y+1)
        else:
            self.place()
            self.check_clear()
            self.spawn()

    def place(self):
        t_x, t_y = self.tetrimino_position
        piece = self.tetrimino[self.r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                self.placed[t_y + y][t_x + x] = piece[y][x]

    def on_right(self):
        t_x, t_y = self.tetrimino_position
        if self.check_move((t_x+1, t_y)):
            self.tetrimino_position = (t_x+1, t_y)

    def on_left(self):
        t_x, t_y = self.tetrimino_position
        if self.check_move((t_x-1, t_y)):
            self.tetrimino_position = (t_x-1, t_y)

    def on_down(self):
        t_x, t_y = self.tetrimino_position
        if self.check_move((t_x, t_y+1)):
            self.tetrimino_position = (t_x, t_y+1)

    def on_tick(self):
        speed = 15
        if ticks % speed == 0:
            self.fall()
        self.ticks += 1

    def draw_board(self):
        for y in range(len(self.h)):
            for x in range(len(self.w)):
                if y < 4:
                    self.board[y][x] = 0
                if x < len(self.placed[0]):
                    self.board[y][x] = self.placed[y][x]
        piece = self.tetrimino[self.r]
        t_x, t_y = self.tetrimino_position
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                self.board[t_y + y][t_x + x] = piece[y][x]

        board_state = [[color['cyber_yellow'] if val == 1 else
                        color['cobalt_blue'] if val == 2 else
                        color['cobalt_blue'] if val == 3 else
                        color['beer'] if val == 4 else
                        color['apple_green'] if val == 5 else
                        color['red2'] for val in row] for row in self.board]
        bytes_array = PixelUtils.board_to_bytes(board_state)
        return bytes_array
