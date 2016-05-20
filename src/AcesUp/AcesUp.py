from __future__ import print_function
from Game import Game
from Menu import Menu

class AcesUp:
    def __init__(self):
        self.__currentMenu = 'main'
        self.menu = Menu()
        self.game = Game()

    def main(self, argc, argv):
        while self.menu.hasMenu():
            parameters = []
            if self.menu.getCurrentMenu() == Menu.MAIN:
                parameters = self.game.getPlayer().getName()

            self.menu.printMenu(parameters)

            if (self.menu.getCurrentMenu() == Menu.GAME):
                self.__loopGame()

        return 0

    def __loopGame(self):
        self.game.startGame()
        while self.game.isInGame():
            self.game.printCards()
            action = self.menu.printMenu(self.game.getCurrentFacingCards())

            isInt = True
            try:
                action = int(action)
            except ValueError:
                pass

            if action in range(1, 5):
                self.game.removeCard(int(action) - 1)
            elif action == 'd':
                self.game.deal()
                continue
            elif action == 'q':
                self.game.quitGame()
                self.menu.setCurrentMenu(Menu.MAIN)


# TODO: write method to check if game was beatable (and how many different ways)
# TODO: record all games played?
