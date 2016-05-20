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

    def __eq__(self, other):
        return self.getPosition() == other.getPosition() and self.getSuit() == other.getSuit()

    def __ne__(self, other):
        return self.getPosition() != other.getPosition() or self.getSuit() != other.getSuit()

    def __lt__(self, other):
        return self.getSuit() == other.getSuit() and self.getPosition() < other.getPosition()

    def __gt__(self, other):
        return self.getSuit() == other.getSuit() and self.getPosition() > other.getPosition()

    def __str__(self):
        zero = '0' if self.getPosition() < 10 else ''
        return str(self.getSuit() + zero + str(self.getPosition()))
