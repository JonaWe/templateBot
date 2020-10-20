class Game:
    def __init__(self):
        self.board = [[None for x in range(6)] for y in range(6)]

    def add_coin(self, player: int, column: int):
        for row in range(6):
            if not self.board[column][row]:
                self.board[column][row] = player
                return True
        return False

    def check_for_win(self):
        # vertical
        for col in range(6):
            for row in range(6 - 3):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col][row+1] \
                        and self.board[col][row+1] == self.board[col][row+2] \
                        and self.board[col][row+2] == self.board[col][row+3]:
                    print("v win")
                    return self.board[col][row]

        # horizontal
        for col in range(6 - 3):
            for row in range(6):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row] \
                        and self.board[col+1][row] == self.board[col+2][row] \
                        and self.board[col+2][row] == self.board[col+3][row]:
                    print("h win")
                    return self.board[col][row]

        # positive diagonal
        for col in range(6 - 3):
            for row in range(6 - 3):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row+1] \
                        and self.board[col+1][row+1] == self.board[col+2][row+2] \
                        and self.board[col+2][row+2] == self.board[col+3][row+3]:
                    print("p d win")
                    return self.board[col][row]

        # negative diagonals
        for col in range(6 - 3):
            for row in range(3, 6):
                if self.board[col][row] \
                        and self.board[col][row] == self.board[col+1][row-1] \
                        and self.board[col+1][row-1] == self.board[col+2][row-2] \
                        and self.board[col+2][row-2] == self.board[col+3][row-3]:
                    print("n d win")
                    return self.board[col][row]

        return None

    def print(self):
        print(self.board)

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