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
        self.__modCounter = 0;
        self.__modifier = 0;
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
            return 'Player 1'
        return name

    def getPlayer(self):
        return self.__player

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
        self.__setGameStatus(Game.IN_MENU)

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
        self.__player = Player(playerInfo['name'])
        if playerInfo is not None:
            self.__player.setScore(playerInfo['score'])
            self.__player.setTime(playerInfo['time'])

    ##
    # Returns the 10 top scores from file
    ##
    def getTopScores(self):
        scores = self.__file.getScores()
        scores.sort(reverse = True)
        return scores[0, 10]

    ##
    # Returns the 10 top times from file
    ##
    def getTopTimes(self):
        times = self.__file.getTimes()
        times.sort(reverse = True)
        return times[0, 10]

    ##
    # Returns all Players from file
    ##
    def getAllPlayers(self):
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
        found = True
        num = 0
        while found:
            found = False
            row = ''
            for deck in self.__discardPiles:
                row += ' '
                card = deck.getCardAt(num)
                if card is not None:
                    found = True
                    row += str(card)
                else:
                    row += '   '
            num += 1
            print(row)

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
    def removeCard(self, index):
        if self.__canRemoveCardFromPile(index):
            self.incrementModCounter()
            self.__discardPiles[index].popCard()
            self.addRemovedCardPoints()

    def __canRemoveCardFromPile(self, index):
        if index in range(0, 4):
            cardInQuestion = self.__discardPiles[index].getFacingCard()
            if cardInQuestion is not None:
                for pile in self.__discardPiles:
                    if pile.dominatesCard(cardInQuestion):
                        return True

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
    def resetModCounter(self):
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
