from random import randrange

from random import randrange
import copy
import numpy as np


class Game:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = randrange(1, 3)

    def add_coin(self, player: int, column: int):
        if self.current_player == player:
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = player
                    if self.current_player == 1:
                        self.current_player = 2
                    elif self.current_player == 2:
                        self.current_player = 1
                    return True
        return False

    def check_for_win(self):
        # horizontal
        for row in range(6):
            for col in range(7 - 3):
                if self.board[row][col] != 0\
                        and self.board[row][col] == self.board[row][col + 1] \
                        and self.board[row][col + 1] == self.board[row][col + 2] \
                        and self.board[row][col + 2] == self.board[row][col + 3]:
                    return self.board[row][col]

        # vertical
        for row in range(6 - 3):
            for col in range(7):
                if self.board[row][col] != 0\
                        and self.board[row][col] == self.board[row + 1][col] \
                        and self.board[row + 1][col] == self.board[row + 2][col] \
                        and self.board[row + 2][col] == self.board[row + 3][col]:
                    return self.board[row][col]

        # positive diagonal
        for row in range(6 - 3):
            for col in range(7 - 3):
                if self.board[row][col] != 0\
                        and self.board[row][col] == self.board[row + 1][col + 1] \
                        and self.board[row + 1][col + 1] == self.board[row + 2][col + 2] \
                        and self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    return self.board[row][col]

        # negative diagonals
        for row in range(6 - 3):
            for col in range(3, 7):
                if self.board[row][col] != 0 \
                        and self.board[row][col] == self.board[row + 1][col - 1] \
                        and self.board[row + 1][col - 1] == self.board[row + 2][col - 2] \
                        and self.board[row + 2][col - 2] == self.board[row + 3][col - 3]:
                    return self.board[row][col]

        all_filled = True
        for row in range(6):
            for col in range(7):
                all_filled &= self.board[row][col] == 0

        if all_filled:
            return -1

        return None

    def print(self):
        out = ""
        for row in range(6):
            for col in range(7):
                out += f" {self.board[row][col]} "
            out += "\n"
        print(out)

    def to_embed_string(self):
        out = ""
        for row in range(6):
            first = ""
            second = ""
            for col in range(7):
                if self.board[row][col] == 1:
                    first += ":yellow_circle:"
                elif self.board[row][col] == 2:
                    first += ":red_circle:"
                else:
                    first += ":black_circle:"
            out += first + "\n" + second
        return out + ":one:\uFEFF:two:\uFEFF:three:\uFEFF:four:\uFEFF:five:\uFEFF:six:\uFEFF:seven:"



if __name__ == "__main__":
    game = Game()
    game.add_coin(player=2, column=3)
    game.add_coin(player=1, column=2)
    game.add_coin(player=2, column=2)
    game.add_coin(player=1, column=1)
    game.add_coin(player=1, column=1)
    game.add_coin(player=2, column=1)
    game.add_coin(player=1, column=0)
    game.add_coin(player=1, column=0)
    game.add_coin(player=1, column=0)
    game.add_coin(player=2, column=0)
    game.print()
    print(game.check_for_win())
