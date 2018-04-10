##
# AcesUp
# Written by Patrick Barnum
##

from version import __version__


class Menu:
    MAIN = 'main'
    GAME = 'game'
    STATS = 'stats'
    OPTIONS = 'options'
    PLAYER = 'player'
    RESET = 'reset'
    DELETE = 'delete'
    QUIT = 'quit'

    def __init__(self):
        self.__width = 58
        self.__padding = 5
        self.__colPadding = 2
        self.__border = '+'
        for i in range(0, self.__width):
            self.__border = self.__border + '-'
        self.__border = self.__border + '+'

        self.__currentMenu = self.MAIN

    def setCurrentMenu(self, menu):
        # TODO check if menu matches any constant value
        self.__currentMenu = menu

    def getCurrentMenu(self):
        return self.__currentMenu

    def printMenu(self, *args):
        if type(args[0]) == bool or len(args[0]) > 0:
            return getattr(self, self.getCurrentMenu() + 'Menu')(args[0])
        else:
            return getattr(self, self.getCurrentMenu() + 'Menu')()

    def getInput(self, inputText, **kwargs):
        value = input('\n' + inputText)
        if 'lower' not in kwargs or kwargs['lower'] is True:
            value = value.lower()
        return value

    def hasMenu(self):
        return self.__currentMenu is not None

    def __titleLengthIsGood(self, title):
        return len(title) < (self.__width - self.__padding)

    def __findClosestSpace(self, title, index):
        if index is ' ':
            return index

        before = index - 1
        after = index + 1
        while before >= 0 and after < len(title):
            if title[before] is ' ':
                return before
            if title[after] is ' ':
                return after
            before = before - 1
            after = after + 1
        return index

    def __formatTitle(self, title, split=2):
        if self.__titleLengthIsGood(title) is False:
            titles = []
            titleLength = len(title)
            segmentLength = int(titleLength / split)

            index = 0
            while len(titles) != split:
                beginningIndex = index
                index = (segmentLength * split) + 1
                index = self.__findClosestSpace(title, index)
                titles.append(title[beginningIndex:index])

            for string in titles:
                if self.__titleLengthIsGood(string) is False:
                    titles = self.__formatTitle(title, split + 1)
                    break

            return titles
        else:
            return [title]

    def __addPadding(self, string):
        string = (' ' * self.__padding) + string + (' ' * self.__padding)
        addToEnd = True
        while len(string) < (self.__width):
            if addToEnd is True:
                string = string + ' '
            else:
                string = ' ' + string
            addToEnd = not addToEnd
        return string

    def printTitle(self, title):
        if '\n' in title:
            titles = title.splitlines()
        else:
            titles = self.__formatTitle(title)

        print(self.__border)
        for string in titles:
            print('|' + self.__addPadding(string) + '|')
        print(self.__border + '\n')

    def __formatTable(self, table):
        formatted = self.getFormattedTableObj(table, [0] * len(table[0]))

        for row in range(0, len(table)):
            for col in range(0, len(table[row])):
                if formatted['colWidth'][col] < len(str(table[row][col])):
                    formatted['colWidth'][col] = len(str(table[row][col]))

        return formatted

    def printTable(self, table):
        # Number of columns * padding on both sides + number of dividers
        totalPadding = len(table['colWidth']) * (self.__colPadding * 2)
        sumOfColValues = sum(table['colWidth'])
        numberOfDividers = len(table['colWidth']) - 1
        tableWidth = totalPadding + sumOfColValues + numberOfDividers
        border = '+' + ('-' * tableWidth) + '+'
        padding = ' ' * self.__colPadding

        print(border)
        for row in range(0, len(table['table'])):
            string = '|'
            for col in range(0, len(table['table'][row])):
                value = str(table['table'][row][col])
                multiply = table['colWidth'][col] - len(str(table['table'][row][col]))
                spaces = ' ' * multiply
                string += padding + value + spaces + padding + '|'
            print(string)
            print(border)

    def getFormattedTableObj(self, data=None, widths=None):
        return {
            'table': data,
            'colWidth': widths
        }

    ##
    #
    ##
    def mainMenu(self, args):
        playerName = args

        self.printTitle('Welcome to AcesUp\nWritten by Patrick Barnum\nBuild ' + __version__)

        print('Currently playing as "' + playerName + '"\n')

        print('Please select an option from the following menu:')
        print('[N]ew game')
        print('[S]tatistics')
        print('[R]eset statistics')
        print('[O]ptions')
        print('[C]hange Player')
        print('[T]op 10 scores')
        print('[Q]uit')

        userInput = self.getInput('Enter your choice: ')
        if userInput == 'n':
            self.setCurrentMenu(self.GAME)
        elif userInput == 's':
            self.setCurrentMenu(self.STATS)
        elif userInput == 'r':
            self.setCurrentMenu(self.RESET)
        elif userInput == 'o':
            self.setCurrentMenu(self.OPTIONS)
        elif userInput == 'c':
            self.setCurrentMenu(self.PLAYER)
        # elif userInput == 't':
        #     self.setCurrentMenu(self.TOP)
        elif userInput == 'q':
            self.setCurrentMenu(self.QUIT)

    def gameMenu(self, args):
        card1, card2, card3, card4 = args
        print('Actions:')

        if card1 is not None:
            print('[mv|rm 1] ' + str(card1))
        if card2 is not None:
            print('[mv|rm 2] ' + str(card2))
        if card3 is not None:
            print('[mv|rm 3] ' + str(card3))
        if card4 is not None:
            print('[mv|rm 4] ' + str(card4))

        print('[U]ndo last action')
        print('[D]eal again')
        print('[Q]uit game')
        return self.getInput('What would you like to do? ')

    def optionsMenu(self, args):
        return

    def statsMenu(self, args):
        stats = args
        self.printTitle('Player Statistics\n')

        # Format the data and get it ready for printing
        formattedStats = self.__formatTable(stats)

        # Print the table
        self.printTable(formattedStats)

        self.setCurrentMenu(self.MAIN)

    def quitMenu(self, args):
        confirm = args
        if confirm is False:
            self.setCurrentMenu(None)
            return

        answer = self.getInput('Are you sure you want to quit? [y/n] ')
        if answer == 'n' or answer == 'no':
            self.setCurrentMenu(self.MAIN)
        elif answer == 'y' or answer == 'yes':
            self.setCurrentMenu(None)
