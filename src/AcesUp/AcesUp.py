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
                elif self.menu.getCurrentMenu() == Menu.STATS:
                    parameters = self.game.getPlayerStats()

                self.menu.printMenu(parameters)

                if self.menu.getCurrentMenu() == Menu.GAME:
                    self.__loopGame()
                elif self.menu.getCurrentMenu() == Menu.PLAYER:
                    self.__changePlayer()
            except KeyboardInterrupt:
                if self.game.isInGame():
                    self.game.finishGame()
                break

        return 0

    def __loopGame(self):
        self.game.startGame()
        while self.game.isInGame():
            title = 'Aces Up!\n' + self.game.getPlayer().getName() + '\n'
            self.menu.printTitle(title + self.game.printCards())
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

    def __changePlayer(self):
        players = self.game.getPlayerNames()
        playersTable = self.__formatDataToTable(players)
        self.menu.printTable(playersTable)

        uInput = str(self.menu.getInput('Choose a player or create a new one: ', lower=False))

        self.game.loadPlayer(uInput)

        self.menu.setCurrentMenu(Menu.MAIN)

    def __formatDataToTable(self, data):
        count = 0
        table = []
        colWidth = []
        while len(data) > 0:
            item = data.pop()
            row = count % 10

            # Set the Player name in the row/column
            if len(table) == row:
                table.append([item])
            else:
                table[row].append(item)

            # Set the max string length for this column
            if len(table[0]) > len(colWidth):
                colWidth.append(len(item))
            else:
                key = len(colWidth) - 1
                if len(item) > colWidth[key]:
                    colWidth[key] = len(item)

            count += 1

        # Fill missing columns to print right border
        while count % 10 > 0:
            row = count % 10
            table[row].append('')
            count += 1

        return self.menu.getFormattedTableObj(table, colWidth)
