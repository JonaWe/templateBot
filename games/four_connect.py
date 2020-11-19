from random import randrange

class Game:
    def __init__(self):
        self.board = [[None for x in range(6)] for y in range(7)]
        self.current_player = randrange(1, 3)

    def add_coin(self, player: int, column: int):
        if self.current_player == player:
            for row in range(6):
                if not self.board[column][row]:
                    self.board[column][row] = player
                    if self.current_player == 1:
                        self.current_player = 2
                    elif self.current_player == 2:
                        self.current_player = 1
                    return True
        return False

    def check_for_win(self):
        # vertical
        for col in range(7):
            for row in range(6 - 3):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col][row+1] \
                        and self.board[col][row+1] == self.board[col][row+2] \
                        and self.board[col][row+2] == self.board[col][row+3]:
                    return self.board[col][row]

        # horizontal
        for col in range(7 - 3):
            for row in range(6):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row] \
                        and self.board[col+1][row] == self.board[col+2][row] \
                        and self.board[col+2][row] == self.board[col+3][row]:
                    return self.board[col][row]

        # positive diagonal
        for col in range(7 - 3):
            for row in range(6 - 3):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row+1] \
                        and self.board[col+1][row+1] == self.board[col+2][row+2] \
                        and self.board[col+2][row+2] == self.board[col+3][row+3]:
                    return self.board[col][row]

        # negative diagonals
        for col in range(7 - 3):
            for row in range(3, 6):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row-1] \
                        and self.board[col+1][row-1] == self.board[col+2][row-2] \
                        and self.board[col+2][row-2] == self.board[col+3][row-3]:
                    return self.board[col][row]

        all_filled = True
        for col in range(7):
            for row in range(6):
                all_filled &= self.board[col][row] is not None

        if all_filled:
            return -1


        return None

    def print(self):
        out = ""
        row = 5
        while row >= 0:
            for col in range(6):
                if self.board[col][row]:
                    out += f" |{self.board[col][row]}| "
                else:
                    out += " | | "
            out += "\n"
            row -= 1
        print(out[:])

    def to_embed_string(self):
        out = ""
        row = 5
        while row >= 0:
            for col in range(7):
                if self.board[col][row] == 1:
                    out += " :yellow_circle: \uFEFF"
                elif self.board[col][row] == 2:
                    out += " :red_circle: \uFEFF"
                else:
                    out += " :black_circle: \uFEFF"
            out += "\n"
            row -= 1
        return out + ":one: \uFEFF :two: \uFEFF :three: \uFEFF :four: \uFEFF :five: \uFEFF :six: \uFEFF :seven:"