##
# AcesUp
# Written by Patrick Barnum
##

import json
import os.path

class FileHandler:
    def __init__(self):
        self.__fileName = os.path.expanduser('~') + '/.acesup'
        self.__createFile()
        self.__readFile()

    def __createFile(self):
        if not os.path.isfile(self.__fileName):
            with open(self.__fileName, 'w') as outfile:
                json.dump('{"version":"v1.0.0","players":[{"name":"Player 1","score":0,"time":0,"gamesWon":0,"gamesLost":0,"statResets":0}],"lastPlayer":"Player 1"}', outfile)

    def __readFile(self):
        file = ''
        with open(self.__fileName, 'r') as jsonData:
            file = json.load(jsonData)
        self.__file = json.loads(file)

    def __loadPlayerFromFile(self, playerName):
        for player in self.__getPlayers():
            if player['name'] == playerName:
                return player
        return None

    def __getPlayers(self):
        return self.__file['players'] if len(self.__file['players']) else []

    def getLatestPlayerByName(self):
        return self.__file['lastPlayer']

    def loadPlayerByName(self, playerName):
        return self.__loadPlayerFromFile(playerName)

    def savePlayer(self, player):
        stats = {
            'name': player.getName(),
            'score': player.getScore(),
            'time': player.getTime(),
            'gamesWon': player.getGamesWon(),
            'gamesLost': player.getGamesLost(),
            'statResets': player.getStatResets()
        }

        self.__setPlayer(stats)

        with open(self.__fileName, 'w') as outfile:
            json.dump(str(self.__file), outfile)

    def __setPlayer(self, stats):
        for index in range(0, len(self.__getPlayers())):
            if self.__getPlayers()[index]['name'] == stats['name']:
                self.__getPlayers()[index] = stats
                return
        return self.__getPlayers().append(stats)

    def __getPlayerAttribute(self, attr):
        # TODO: get player name with attribute
        values = []
        for player in self.__getPlayers():
            value = player[attr] if len(player[attr]) else 0
            values.append(value)
        return values

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
