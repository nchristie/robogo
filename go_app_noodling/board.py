from pprint import pprint


class Board:
    def __init__(self, size=9):
        self.state = self.make_board(size)

    def make_board(self, size):
        board = []
        for i in size:
            for j in size:
                board[i][j] = "Foo"
        return board

    def draw(self):
        pprint(self.state)

    def make_move(self, x, y, player):
        self.state[x][y] = player

    def get_scores(self):
        x_score = 0
        y_score = 0


if __name__ == "__main__":
    my_board = Board()
    my_board.make_move(0, 0, "O")
    my_board.make_move(0, 1, "X")
    my_board.draw()
