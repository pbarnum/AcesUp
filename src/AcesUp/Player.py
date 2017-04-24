##
# Aces Up
# Written by Patrick Barnum
##


class Player:
    DEFAULT_PLAYER = 'Player 1'

    def __init__(self, name, score=0, time=0, won=0, lost=0, resets=0, options={}):
        self.__name = name
        self.__score = score
        self.__time = time
        self.__gamesWon = won
        self.__gamesLost = lost
        self.__statResets = resets
        self.__options = self.defaultOptions() if len(options) == 0 else options

    def defaultOptions(self):
        return {
            'undo': True,
            'confirmQuit': True
        }

    def getName(self):
        return self.__name

    def getScore(self):
        return self.__score

    def getTime(self):
        return self.__time

    def getGamesWon(self):
        return self.__gamesWon

    def getGamesLost(self):
        return self.__gamesLost

    def getStatResets(self):
        return self.__statResets

    def setScore(self, score):
        self.__score = score

    def addToScore(self, score):
        self.__score += score

    def setTime(self, time):
        self.__time = time

    def addGameWon(self):
        ++self.__gamesWon

    def addGameLost(self):
        ++self.__gamesLost

    def addStatReset(self):
        ++self.__statResets

    def getAllStats(self, **excludes):
        stats = {
            'name': self.getName(),
            'score': self.getScore(),
            'time': self.getTime(),
            'gamesWon': self.getGamesWon(),
            'gamesLost': self.getGamesLost(),
            'statResets': self.getStatResets(),
            'options': self.getOptions()
        }

        for key in excludes:
            if key in stats and excludes[key] is False:
                del stats[key]

        return stats

    def getOptions(self):
        return self.__options

    def setOptions(self, options):
        for option in options:
            if option in self.__options:
                self.__options[option] = options[option]
