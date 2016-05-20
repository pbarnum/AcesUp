##
# Aces Up
# Written by Patrick Barnum
##

class Player:
    def __init__(self, name):
        self.__name = name
        self.__score = 0
        self.__time = 0
        self.__gamesWon = 0
        self.__gamesLost = 0
        self.__statResets = 0

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
