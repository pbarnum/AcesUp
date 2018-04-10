##
# Aces Up
# Written by Patrick Barnum
##

import copy


class Player:
    DEFAULT_PLAYER = u'Player 1'
    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_HARD = 'hard'

    def __init__(self, info):
        self.props = self.__defaultProperties()
        # Convert string to dict
        if (type(info) is str):
            info = {'name': info}

        # Throw error if argument is not a dict
        if type(info) is not dict:
            raise AttributeError

        self.__setProps(info)

    def defaultOptions(self):
        return {
            'undo': True,
            'confirmQuit': True
        }

    def __defaultProperties(self):
        return {
            'name': '',
            'score': 0,
            'time': 0,
            'gamesWon': 0,
            'gamesLost': 0,
            'statResets': 0,
            'difficulty': self.DIFFICULTY_EASY,
            'options': {
                'undo': True,
                'confirmQuit': True
            }
        }

    def __mergeProps(self, first, second):
        first.update(second)
        return first

    def __setProps(self, props):
        shell = self.__defaultProperties()
        allProps = self.__mergeProps(shell, props)
        for key in allProps:
            if key in shell:
                self.set(key, allProps[key])

    ##
    # Gets an appropriate member variable from the Player object
    #
    # This method will error out if the variable constructed is not found
    ##
    def get(self, key):
        if key in self.__defaultProperties():
            return copy.deepcopy(self.props[key])

        if '.' in key:
            return self.getDeep(key)

    def getDeep(self, key):
        keys = key.split('.')
        keys.reverse()
        value = self.props

        while len(keys) > 0:
            value = value[keys.pop()]

        return copy.deepcopy(value)

    ##
    # Sets an appropriate member variable on the Player object
    ##
    def set(self, key, value):
        if key in self.__defaultProperties():
            if type(self.__defaultProperties()[key]) == dict:
                self.setDictProp(key, value)
            else:
                self.props[key] = value

    def addTo(self, key, value):
        original = self.get(key)
        self.set(key, original + value)

    def getAllStats(self, **excludes):
        stats = copy.deepcopy(self.props)
        for key in excludes:
            if key in stats and excludes[key] is False:
                del stats[key]

        return stats

    def setDictProp(self, key, obj):
        for option in obj:
            if option in self.props[key]:
                self.props[key][option] = obj[option]

    def resetStats(self):
        name = copy.copy(self.props['name'])
        self.props = copy.deepcopy(self.__defaultProperties())
        self.props['name'] = name
