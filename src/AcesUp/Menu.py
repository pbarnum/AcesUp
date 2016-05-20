##
# AcesUp
# Written by Patrick Barnum
##

import sys
import re

class Menu:
    MAIN = 'main'
    PLAYER = 'player'
    STATS = 'stats'
    GAME = 'game'
    DELETE = 'delete'
    QUIT = 'quit'

    def __init__(self):
        self.__currentMenu = self.MAIN

    def setCurrentMenu(self, menu):
        # TODO check if menu matches any constant value
        self.__currentMenu = menu

    def getCurrentMenu(self):
        return self.__currentMenu

    def printMenu(self, *args):
        if len(args[0]) > 0:
            return getattr(self, self.getCurrentMenu() + 'Menu')(args)
        else:
            return getattr(self, self.getCurrentMenu() + 'Menu')()

    def getInput(self, inputText):
        return str(raw_input('\n' + inputText)).lower()

    def hasMenu(self):
        return self.__currentMenu is not None

    ##
    #
    ##
    def mainMenu(self, args):
        playerName = args[0]

        print('Welcome to AcesUp')
        print('Written by Patrick Barnum')
        print('Build v1.0.0\n')

        print('Currently playing as "' + playerName + '"\n')

        print('Please select an option from the following menu:')
        print('[N]ew game')
        print('[C]hange Player')
        print('[P]rint statistics')
        print('[S]how top 10 scores')
        print('[D]elete all scores')
        print('[Q]uit')

        userInput = str(self.getInput('Enter your choice: ')).lower()
        if userInput == 'n':
            self.setCurrentMenu(Menu.GAME)
        elif userInput == 'q':
            self.setCurrentMenu(Menu.QUIT)

    def gameMenu(self, args):
        card1, card2, card3, card4 = args[0]
        print('Actions:')

        if card1 is not None:
            print('[1] Remove ' + str(card1))
        if card2 is not None:
            print('[2] Remove ' + str(card2))
        if card3 is not None:
            print('[3] Remove ' + str(card3))
        if card4 is not None:
            print('[4] Remove ' + str(card4))

        print('[D]eal again')
        print('[Q]uit game')
        return self.getInput('What would you like to do? ')

    def quitMenu(self):
        answer = self.getInput('Are you sure you want to quit? [y/n] ')
        if answer == 'n' or answer == 'no':
            self.setCurrentMenu(self.MAIN)
        elif answer == 'y' or answer == 'yes':
            self.setCurrentMenu(None)
