from Game import Game
from Menu import Menu


class AcesUp:
    def __init__(self):
        self.__currentMenu = 'main'
        self.menu = Menu()
        self.game = Game()

    def main(self, argc, argv):
        while self.menu.hasMenu():
            try:
                parameters = []
                if self.menu.getCurrentMenu() == Menu.MAIN:
                    parameters = self.game.getPlayer().getName()
                elif self.menu.getCurrentMenu() == Menu.PLAYER:
                    parameters = (
                        self.game.getPlayer().getName(),
                        self.game.getPlayerStats()
                    )

                self.menu.printMenu(parameters)

                if (self.menu.getCurrentMenu() == Menu.GAME):
                    self.__loopGame()
            except KeyboardInterrupt:
                if self.game.isInGame():
                    self.game.finishGame()
                break

        return 0

    def __loopGame(self):
        self.game.startGame()
        while self.game.isInGame():
            self.menu.printTitle(self.game.printCards())
            uInput = str(self.menu.printMenu(self.game.getCurrentFacingCards())).strip()

            action = uInput[:2]
            if action == 'mv' or action == 'rm':
                try:
                    column = int(uInput[-1:])
                except ValueError:
                    print('Column must be an integer')
                    continue

                # Call the proper function to handle the action
                getattr(self.game, action + 'Card')(column - 1)
            elif action == 'd':
                self.game.deal()
            elif action == 'q':
                self.game.quitGame()
                self.menu.setCurrentMenu(Menu.MAIN)

        # Return to the main menu
        self.menu.setCurrentMenu(Menu.MAIN)
