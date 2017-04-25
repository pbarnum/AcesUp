##
# AcesUp
# Written by Patrick Barnum
##

import json
import os.path
from version import __version__
from Player import Player


class FileHandler:
    def __init__(self):
        self.__fileName = os.path.expanduser('~') + '/.acesup'
        self.__createFile()
        self.__readFile()

    def __createFile(self):
        if not os.path.isfile(self.__fileName):
            self.__file = self.__generateData()
            self.savePlayer(Player(Player.DEFAULT_PLAYER))

    def __readFile(self):
        file = ''
        with open(self.__fileName, 'r') as jsonData:
            file = json.load(jsonData)
        self.__file = json.loads(file)

    def __generateData(self):
        return {
            'version': __version__,
            'players': [],
        }

    def __loadPlayerFromFile(self, playerName):
        for player in self.__getPlayers():
            if player['name'] == playerName:
                return player
        return None

    def __getPlayerCount(self):
        return len(self.__getPlayers())

    def __getPlayers(self):
        if self.__file['players'] is None or type(self.__file['players']) is not list:
            self.__file['players'] = []
        return self.__file['players']

    def __setPlayer(self, playerStats):
        self.__file.update({'lastPlayer': playerStats['name']})
        for index in range(0, self.__getPlayerCount()):
            if self.__getPlayers()[index]['name'] == playerStats['name']:
                return self.__getPlayers()[index].update(playerStats)

        return self.__getPlayers().append(playerStats)

    def __getPlayerAttribute(self, attr):
        # TODO: get player name with attribute
        values = []
        for player in self.__getPlayers():
            value = player[attr] if len(player[attr]) else 0
            values.append(value)
        return values

    def listAllPlayers(self):
        names = []
        for player in self.__getPlayers():
            names.append(player['name'])
        return names

    def getLatestPlayerByName(self):
        return self.__file['lastPlayer']

    def loadPlayerByName(self, playerName):
        return self.__loadPlayerFromFile(playerName)

    def savePlayer(self, player):
        self.__setPlayer(player.getAllStats())
        self.__saveFile()

    def saveLatestPlayer(self, playerName):
        self.__file['lastPlayer'] = playerName
        self.__saveFile()

    def __saveFile(self):
        with open(self.__fileName, 'w') as outfile:
            json.dump(json.dumps(self.__file), outfile)

    def getScores(self):
        return self.__getPlayerAttribute('score')

    def getTimes(self):
        return self.__getPlayerAttribute('time')

    def getGamesWon(self):
        return self.__getPlayerAttribute('gamesWon')

    def getGamesLost(self):
        return self.__getPlayerAttribute('gamesLost')

    def getStatResets(self):
        return self.__getPlayerAttribute('statResets')

    def getDifficulty(self):
        return self.__getPlayerAttribute('difficulty')

    def getOptions(self):
        return self.__getPlayerAttribute('options')
