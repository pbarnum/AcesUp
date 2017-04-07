##
# Aces Up
# Written by Patrick Barnum
##


class Card:
    def __init__(self, suit, position):
        self.suit = suit
        self.position = position

    def getSuit(self):
        return self.suit.value

    def getPosition(self):
        return self.position

    def __sameSuit(self, other):
        return self.getSuit() == other.getSuit()

    def __samePos(self, other):
        return self.getPosition() == other.getPosition()

    def __eq__(self, other):
        return self.__samePos(other) and self.__sameSuit(other)

    def __ne__(self, other):
        return not self.__samePos(other) or not self.__sameSuit(other)

    def __lt__(self, other):
        return (self.__sameSuit(other) and self != other and
                (self.getPosition() != 1 and self.getPosition() < other.getPosition()))

    def __gt__(self, other):
        return (self.__sameSuit(other) and self != other and
                (other.getPosition() != 1 and (self.getPosition() == 1 or self.getPosition() > other.getPosition())))

    def __str__(self):
        value = self.getPosition()
        if value == 1:
            value = 'A'
        elif value == 11:
            value = 'J'
        elif value == 12:
            value = 'Q'
        elif value == 13:
            value = 'K'

        return str(str(value) + self.getSuit())
