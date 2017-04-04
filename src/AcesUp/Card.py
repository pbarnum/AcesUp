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
        if self.getPosition() == 1:
            return str(self.getSuit() + '|A')
        zero = '0' if self.getPosition() < 10 else ''
        return str(self.getSuit() + zero + str(self.getPosition()))
