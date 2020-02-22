class Game(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.board = [[0 for x in range(w)] for y in range(h)]

    def clear_board(self):
        self.board = [[0 for x in range(self.w)] for y in range(self.h)]

    def on_left(self):
        pass

    def on_right(self):
        pass

    def on_down(self):
        pass

    def on_up(self):
        pass

    def on_a(self):
        pass

    def on_b(self):
        pass
