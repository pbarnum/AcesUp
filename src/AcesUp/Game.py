##
# AcesUp
# Written by Patrick Barnum
##

import time
from Deck import Deck
from FileHandler import FileHandler
from Player import Player
from Recorder import Recorder
from copy import deepcopy


class Game:
    PAUSED = 0
    IN_GAME = 1
    FINISHED = 2
    IN_MENU = 3
    QUIT = 4

    def __init__(self):
        # Initialize the file
        self.__file = FileHandler()
        self.options = self.__file.getOptions()

        # Get the last player
        playerName = self.__getLastPlayer()
        self.loadPlayer(playerName)

        # Set the Game menu
        self.__status = self.IN_MENU

        self.resetTimer()

        # Points
        self.__resetModCounter()
        self.__resetPointModifier()

        # Deck
        self.__initializeDeck()

        self.__recorder = Recorder(self.__player.get('options.undo'))

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

    def undo(self):
        if self.__recorder.canUndo():
            state = self.__recorder.undo()
            if state is not None:
                self.__applyState(state)

    def __applyState(self, state):
        self.__player.set('score', state['score'])
        self.__deck = state['deck']
        self.__discardPiles = state['discardPiles']

    def __saveState(self):
        state = {
            'score': self.__player.get('score'),
            'deck': deepcopy(self.__deck),
            'discardPiles': deepcopy(self.__discardPiles)
        }
        self.__recorder.pushState(state)

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
        stats = self.__player.getAllStats(options=False)

        # Pretty print time
        stats['time'] = time.strftime("%M:%S", time.gmtime(int(stats['time'])))

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
        self.__setGameStatus(Game.IN_GAME)
        self.__initializeDeck()
        self.deal()
        # First deal of the game, reset the state
        self.__recorder.toggleUndos(self.__player.get('options.undo'))
        self.__recorder.reset()
        self.__resetModCounter()
        self.__resetPointModifier()
        self.resetTimer()
        self.__startTimer()

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
        self.__player.addTo('time', self.__pauseTimer())
        self.__setGameStatus(Game.PAUSED)

    ##
    # Sets the current game status to finished
    ##
    def finishGame(self):
        self.__setGameStatus(Game.FINISHED)
        if self.didPlayerWin():
            self.__player.addTo('gamesWon', 1)
        else:
            self.__player.addTo('gamesLost', 1)
        self.__player.addTo('time', self.__pauseTimer())
        self.savePlayer(self.__player)

    def quitGame(self):
        self.__setGameStatus(Game.QUIT)
        self.savePlayer(self.__player)

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
            self.__player = Player(playerInfo)
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
            self.__saveState()
            for el in range(len(self.__discardPiles)):
                card = self.__deck.popCard()
                self.__discardPiles[el].pushCard(card)

            self.__resetModCounter()
            self.__resetPointModifier()
            return self.getCurrentFacingCards()

        # no more cards left, game over
        self.finishGame()
        return None

    ##
    # Removes a Card from its pile
    ##
    def rmCard(self, index):
        if self.__canRemoveCardFromPile(index):
            self.__saveState()
            self.incrementModCounter()
            self.__discardPiles[index].popCard()
            self.addRemovedCardPoints()

    def mvCard(self, index):
        if index in range(0, len(self.__discardPiles)):
            cardInQuestion = self.__discardPiles[index].getFacingCard()
            if cardInQuestion is not None:
                for pile in self.__discardPiles:
                    if pile.getFacingCard() is None:
                        self.__saveState()
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
        if self.__modCounter == 2:
            self.__resetModCounter()
            self.__modifier += 1
        updated = self.__player.get('score') + (10 * self.getModifier())
        self.__player.set('score', updated)

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

    def getModifier(self):
        return self.__modifier

    ##
    # Adds a static number of points when winning the game
    ##
    def addGameWonPoints(self):
        self.__player.set('score', 100)

    def getCurrentTime(self):
        return time.strftime("%M:%S", time.gmtime(int(time.time() - self.__startTime)))

    def resetTimer(self):
        self.__startTime = 0
        self.__pausedTime = 0

    def __startTimer(self):
        diff = 0
        if self.__pausedTime > 0:
            diff = int(self.__pausedTime - self.__startTime)
        self.__pausedTime = 0
        self.__startTime = time.time() - diff

    def __pauseTimer(self):
        self.__pausedTime = time.time()
        return int(self.__pausedTime - self.__startTime)

    def didPlayerWin(self):
        for deck in self.__discardPiles:
            if deck.cardsRemaining() != 1 or deck.getFacingCard().getPosition() != 1:
                return False
        return True
