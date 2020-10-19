class Game:
    def __init__(self):
        self.field = [[None for x in range(6)] for y in range(6)]

    def add_coin(self, player: int, column: int):
        for row in range(6):
            if not self.field[column][row]:
                self.field[column][row] = player
                return True
        return False

    def print(self):
        print(self.field)

if __name__ == "__main__":
    game = Game()
    game.add_coin(1, 1)
    game.add_coin(player=1, column=1)
    game.add_coin(1, 1)
    game.add_coin(1, 1)
    game.add_coin(1, 1)
    print(game.add_coin(1, 1))
    print(game.add_coin(1, 1))
    game.print()