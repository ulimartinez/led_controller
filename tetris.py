from game import Game
from colors import color
from pixelutils import PixelUtils
import random
import numpy as np
class Tetris(Game):
    def __init__(self, w, h):
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
                    [4,0,0]],
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
       Tmino = [
               [[0,7,0],
                [7,7,7]],
               [[7,0],
                [7,7],
                [7,0]],
               [[7,7,7],
                [0,7,0]],
               [[0,7],
                [7,7],
                [0,7]]
               ]
       self.minos = [Omino, Jmino, Imino, Lmino, Smino, Zmino, Tmino]
       self.placed = np.zeros((24, 10), dtype=int).tolist()
       self.tetrimino = None
       self.next_tetrimino = self.minos[random.randint(0,len(self.minos)-1)]
       self.tetrimino_position = (4, 0)
       self.r = 0
       self.ticks = 0
       self.spawn()
       self.playing = True

    def spawn(self):
        self.tetrimino = self.next_tetrimino
        self.next_tetrimino = self.minos[random.randint(0,len(self.minos)-1)]
        self.tetrimino_position = (4, 3)
        self.r = 0

    def rotate(self, direction, r):
        if direction == 'cw':
            if r < 3:
                return r + 1
            else:
                return 0
        else:
            if r > 0:
                return r - 1
            else:
                return 3

    def check_over(self):
        for i in self.placed[4]:
            if i != 0:
                self.playing = False
                return True
        return False
    
    def check_fall(self, potential):
        p_x, p_y = potential
        piece = self.tetrimino[self.r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 0:
                    if p_y + y > len(self.placed)-1:
                        return False
                    if self.placed[p_y + y][p_x + x] != 0:
                        return False
        return True
    
    def check_move(self, potential):
        p_x, p_y = potential
        piece = self.tetrimino[self.r]
        #if p_x + len(piece[0]) >= len(self.placed[0])-1:
            #return False
        #if p_y + len(piece) >= len(self.placed):
            #return False
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 0:
                    if p_x + x < 0 or p_x + x > len(self.placed[0])-1:
                        return False
                    if p_y + y > len(self.placed)-1:
                        return False
                    if self.placed[p_y + y][p_x + x] != 0:
                        return False
        return True

    def check_rotate(self, potential_r):
        t_x, t_y = self.tetrimino_position
        piece = self.tetrimino[potential_r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] !=0:
                    if t_x + x < 0 or t_x + x > len(self.placed[0])-1:
                        return False
                    if t_y + y >= len(self.placed)-1:
                        return False
                    if self.placed[t_y + y][t_x + x] != 0:
                        return False
        return True

    def check_clear(self):
        clear_ind =[] 
        for y in range(len(self.placed)):
            cleared = True
            for x in range(len(self.placed[0])):
                if self.placed[y][x] == 0:
                    cleared = False
            if cleared:
                self.placed.pop(y)
                self.placed.insert(0, np.zeros(len(self.placed[0])).tolist())



    def fall(self):
        x, y = self.tetrimino_position
        if self.check_fall((x, y+1)):
            self.tetrimino_position = (x, y+1)
        else:
            self.place()
            self.check_clear()
            self.check_over()
            self.spawn()

    def place(self):
        t_x, t_y = self.tetrimino_position
        piece = self.tetrimino[self.r]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 0:
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

    def on_up(self):
        t_x, t_y = self.tetrimino_position
        while self.check_move((t_x, t_y+1)):
            t_y = t_y+1
        self.tetrimino_position = (t_x, t_y)
        pass

    def on_a(self):
        pot_r = self.rotate('cc', self.r)
        if self.check_rotate(pot_r):
            self.r = pot_r

    def on_b(self):
        pot_r = self.rotate('cw', self.r)
        if self.check_rotate(pot_r):
            self.r = pot_r

    def on_tick(self):
        speed = 15
        if self.ticks % speed == 0:
            self.fall()
        self.ticks += 1

    def draw_board(self):
        for y in range(self.h):
            for x in range(self.w):
                if y < 4:
                    self.board[y][x] = 0
                elif x < len(self.placed[0]) and y < len(self.placed):
                    self.board[y][x] = self.placed[y][x]
        piece = self.tetrimino[self.r]
        t_x, t_y = self.tetrimino_position
        if t_y > 3:
            for y in range(len(piece)):
                for x in range(len(piece[0])):
                    if piece[y][x] != 0:
                        self.board[t_y + y][t_x + x] = piece[y][x]

        piece = self.next_tetrimino[0]

        for y in range(len(piece)):
            for x in range(len(piece[0])):
                self.board[10+y][11+x] = piece[y][x]

        board_state = [[color['black'] if val == 0 else
                        color['cyber_yellow'] if val == 1 else
                        color['cobalt_blue'] if val == 2 else
                        color['cyan'] if val == 3 else
                        color['beer'] if val == 4 else
                        color['apple_green'] if val == 5 else
                        color['red'] if val == 6 else
                        color['purple'] for val in row] for row in self.board]
        bytes_array = PixelUtils.board_to_bytes(board_state)
        return bytes_array
