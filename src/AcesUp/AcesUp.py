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
                elif self.menu.getCurrentMenu() == Menu.QUIT:
                    parameters = self.game.getPlayer().getOptions()['confirmQuit']

                self.menu.printMenu(parameters)

                if self.menu.getCurrentMenu() == Menu.GAME:
                    self.__loopGame()
                elif self.menu.getCurrentMenu() == Menu.PLAYER:
                    self.__changePlayer()
                elif self.menu.getCurrentMenu() == Menu.OPTIONS:
                    self.__loopOptions()
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

    def __loopOptions(self):
        playerName = self.game.getPlayer().getName()
        options = self.game.getPlayer().getOptions()

        while self.menu.getCurrentMenu() == Menu.OPTIONS:
            self.menu.printTitle('Options: ' + playerName)

            print('Enter the option name followed by the new value')
            print('Each option will display the appropriate value range\n')

            print('undo [true|false]: ' + str(options['undo']))
            print('confirm_quit_menu [true|false]: ' + str(options['confirmQuit']))

            print('\n[S]ave and quit options')
            print('\n[Q]uit without saving options')

            uInput = self.menu.getInput('Update option: ')
            option = str(uInput).split(None, 1)[0].lower()
            if option == 'undo':
                try:
                    value = str(uInput.split(None, 1)[1]).lower()
                except ValueError:
                    print('Undo option only accepts boolean values (true|false)')
                    continue

                if value == 't' or value == 'True':
                    value = True
                elif value == 'f' or value == 'false':
                    value = False
                else:
                    value = options['undo']
                self.game.getPlayer().setOptions({'undo': value})
            elif option == 'confirm_quit_menu':
                try:
                    value = str(uInput.split(None, 1)[1]).lower()
                except ValueError:
                    print('Confirm quit menu option only accepts boolean values (true|false)')
                    continue

                if value == 't' or value == 'True':
                    value = True
                elif value == 'f' or value == 'false':
                    value = False
                else:
                    value = options['confirmQuit']
                self.game.getPlayer().setOptions({'confirmQuit': value})
            elif uInput == 's':
                self.game.savePlayer(self.game.getPlayer())
                self.menu.setCurrentMenu(Menu.MAIN)
            elif uInput == 'q':
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
        if len(table) == 10:
            while count % 10 > 0:
                row = count % 10
                table[row].append('')
                count += 1

        return self.menu.getFormattedTableObj(table, colWidth)
