class Game(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.board = [[0 for x in range(w)] for y in range(h)]

    def clear_board(self):
        self.board = [[0 for x in range(self.w)] for y in range(self.h)]
