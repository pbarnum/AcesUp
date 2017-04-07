##
# AcesUp
# Written by Patrick Barnum
##

from Deck import Deck
from FileHandler import FileHandler
from Player import Player


class Game:
    PAUSED = 0
    IN_GAME = 1
    FINISHED = 2
    IN_MENU = 3
    QUIT = 4

    def __init__(self):
        self.__file = FileHandler()

        playerName = self.__getLastPlayer()

        self.loadPlayer(playerName)

        self.__status = self.IN_MENU

        # Points
        self.__modCounter = 0
        self.__modifier = 0
        self.__resetPointModifier()
        self.__initializeDeck()

    ##
    # Builds the deck and temporary deck piles
    ##
    def __initializeDeck(self):
        # Initialize discard columns
        self.__discardPiles = [
            Deck(),
            Deck(),
            Deck(),
            Deck()
        ]

        deck = Deck()
        deck.buildFullDeck()
        deck.shuffle()
        self.__deck = deck

    ##
    # Sets the current game status
    ##
    def __setGameStatus(self, status):
        self.__status = status

    ##
    # Returns the last recorded player or the default
    ##
    def __getLastPlayer(self):
        name = self.__file.getLatestPlayerByName()
        if name is None:
            return Player.DEFAULT_PLAYER
        return name

    def getPlayer(self):
        return self.__player

    def getPlayerStats(self):
        stats = self.__player.getAllStats()
        table = []
        for stat in stats:
            table.append([
                stat,
                stats[stat]
            ])
        return table

    ##
    # Sets the current game status to running
    ##
    def startGame(self):
        self.deal()
        self.__setGameStatus(Game.IN_GAME)

    def isInGame(self):
        return self.getGameStatus() == Game.IN_GAME

    def isPaued(self):
        return self.getGameStatus() == Game.PAUSED

    def isFinished(self):
        return self.getGameStatus() == Game.FINISHED

    def isInMenu(self):
        return self.getGameStatus() == Game.IN_MENU

    def quit(self):
        return self.getGameStatus() == Game.QUIT

    ##
    # Sets the current game status to paused
    ##
    def pauseGame(self):
        self.__setGameStatus(Game.PAUSED)

    ##
    # Sets the current game status to finished
    ##
    def finishGame(self):
        self.__setGameStatus(Game.FINISHED)
        self.savePlayer(self.__player)

    def quitGame(self):
        # TODO: mark game as failure
        # set score and increase number of lost games
        # set time
        self.__setGameStatus(Game.QUIT)
        self.__initializeDeck()

    ##
    # Saves the active Player to file
    ##
    def savePlayer(self, player):
        self.__file.savePlayer(player)

    ##
    # Loads a Player from file
    ##
    def loadPlayer(self, playerName):
        playerInfo = self.__file.loadPlayerByName(playerName)
        if playerInfo is not None:
            self.__player = Player(
                playerInfo['name'],
                playerInfo['score'],
                playerInfo['time'],
                playerInfo['gamesWon'],
                playerInfo['gamesLost'],
                playerInfo['statResets'],
            )
            self.__file.saveLatestPlayer(playerName)
        else:
            self.__player = Player(playerName)
            self.__file.savePlayer(self.__player)

    ##
    # Returns the 10 top scores from file
    ##
    def getTopScores(self):
        scores = self.__file.getScores()
        scores.sort(reverse=True)
        return scores[0, 10]

    ##
    # Returns the 10 top times from file
    ##
    def getTopTimes(self):
        times = self.__file.getTimes()
        times.sort(reverse=True)
        return times[0, 10]

    ##
    # Returns all Players from file
    ##
    def getPlayerNames(self):
        return self.__file.listAllPlayers()

    ##
    # Returns the current game status
    ##
    def getGameStatus(self):
        return self.__status

    ##
    # Returns the current facing playable Cards
    ##
    def getCurrentFacingCards(self):
        cards = []
        for deck in self.__discardPiles:
            cards.append(deck.getCardAt(-1))
        return cards

    def printCards(self):
        printableDecks = []
        for deck in self.__discardPiles:
            printableDecks.append(deck.getDeckPrint())

        output = ''
        found = True
        index = 0
        while found:
            found = False
            row = ''
            for deck in printableDecks:
                row += ' '
                try:
                    card = deck[index]
                except IndexError:
                    card = None
                if card is not None:
                    found = True
                    row += str(card)
                else:
                    row += ' ' * 7
            index += 1
            output += '\n' + row
        return output

    ##
    # Deals four Cards from the deck
    ##
    def deal(self):
        if self.__deck.cardsRemaining() > 0:
            for el in range(len(self.__discardPiles)):
                card = self.__deck.popCard()
                self.__discardPiles[el].pushCard(card)

            return self.getCurrentFacingCards()

        # no more cards left, game over
        self.finishGame()
        return None

    ##
    # Removes a Card from its pile
    ##
    def rmCard(self, index):
        if self.__canRemoveCardFromPile(index):
            self.incrementModCounter()
            self.__discardPiles[index].popCard()
            self.addRemovedCardPoints()

    def mvCard(self, index):
        if index in range(0, len(self.__discardPiles)):
            cardInQuestion = self.__discardPiles[index].getFacingCard()
            if cardInQuestion is not None:
                for pile in self.__discardPiles:
                    if pile.getFacingCard() is None:
                        self.__discardPiles[index].popCard()
                        pile.pushCard(cardInQuestion)
                        return True
            print(str(cardInQuestion) + ' cannot be moved')
        print('Invalid column selected')

    def __canRemoveCardFromPile(self, index):
        if index in range(0, len(self.__discardPiles)):
            cardInQuestion = self.__discardPiles[index].getFacingCard()
            print('card in question: ' + str(cardInQuestion))
            if cardInQuestion is not None:
                for pile in self.__discardPiles:
                    if pile.dominatesCard(cardInQuestion):
                        return True
            print(str(cardInQuestion) + ' cannot be removed')
        print('Invalid column selected')
        return False

    ##
    # Adds points to the Player's score multiplied by the mod counter
    ##
    def addRemovedCardPoints(self):
        if self.__modCounter == 5:
            self.__resetModCounter()
            self.__modifier += 1
        self.__player.addToScore((10 * self.__modifier))

    ##
    # Adds one to the mod counter
    ##
    def incrementModCounter(self):
        self.__modCounter += 1

    ##
    # Resets the mod counter back to default (0)
    ##
    def __resetModCounter(self):
        self.__modCounter = 0

    ##
    # Resets the modifier back to default (1)
    ##
    def __resetPointModifier(self):
        self.__modifier = 1

    ##
    # Increases the point modifier by 1
    ##
    def increasePointModifier(self):
        self.__modifier += 1

    ##
    # Adds a static number of points when winning the game
    ##
    def addGameWonPoints(self):
        self.__player.addToScore(100)
