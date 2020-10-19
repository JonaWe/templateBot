class Game:
    def __init__(self):
        self.field = [[None for x in range(6)] for y in range(6)]

    def add_coin(self, player: int, column: int):
        for row in range(6):
            if not self.field[column][row]:
                self.field[column][row] = player
                return True
        return False

    def check_for_win(self):
        # check for vertical wins
        for row in range(6):
            player = self.check_vertical(row)
            if player:
                print(f"Vertical win {player}")

        # check for horizontal wins
        for col in range(6):
            player = self.check_horizontal(col)
            if player:
                print(f"Horizontal win {player}")

    def check_vertical(self, row: int, col=0, length=0, player=None):
        # win found
        if length == 4:
            return player

        # out of range
        elif col > 5:
            return None

        # resetting because the field is empty
        elif not self.field[col][row]:
            return self.check_vertical(row, col+1)

        # if the previous and current player are the same
        elif player == self.field[col][row]:
            return self.check_vertical(row, col+1, length+1, player)

        # starting for a new player
        else:
            return self.check_vertical(row, col+1, 1, self.field[col][row])

    def check_horizontal(self, col, row=0, length=0, player=None):
        # win found
        if length == 4:
            return player

        # out of range
        elif row > 5:
            return None

        # resetting because the field is empty
        elif not self.field[col][row]:
            return self.check_horizontal(col, row + 1)

        # if the previous and current player are the same
        elif player == self.field[col][row]:
            return self.check_horizontal(col, row + 1, length + 1, player)

        # starting for a new player
        else:
            return self.check_horizontal(col, row + 1, 1, self.field[col][row])

    def print(self):
        print(self.field)

if __name__ == "__main__":
    game = Game()
    game.add_coin(1, 0)
    game.add_coin(2, 0)
    game.add_coin(2, 0)
    game.add_coin(2, 0)
    game.add_coin(2, 0)
    game.add_coin(1, 0)
    game.add_coin(1, 0)
    game.print()
    game.check_for_win()