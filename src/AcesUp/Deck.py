##
# Aces Up
# Written by Patrick Barnum
##

import random
from Card import Card
from Suits import Suits


class Deck:
    DECK_MAX = 52
    SUIT_MAX = 13

    def __init__(self):
        self.__cards = []

    def buildFullDeck(self):
        # Add Cards 1 - 13 to for each Suit
        for suit in Suits:
            for position in range(1, self.SUIT_MAX + 1):
                card = Card(suit, position)
                self.pushCard(card)

    def cardsRemaining(self):
        return len(self.__cards)

    def getCardAt(self, position):
        # Return the dereferenced pointer if position is in the vector's bounds
        try:
            return self.__cards[position]
        except IndexError:
            return None

    def getFacingCard(self):
        return self.getCardAt(-1)

    def dominatesCard(self, card):
        if self.cardsRemaining() > 0:
            return self.getFacingCard() > card
        return False

    def popCard(self):
        # Return nothing if nothing to return
        if self.cardsRemaining() == 0:
            return None

        card = self.getCardAt(self.cardsRemaining() - 1)
        del self.__cards[-1]
        return card

    def pushCard(self, card):
        # Add Card if the Deck is not full
        if self.cardsRemaining() < self.DECK_MAX:
            self.__cards.append(card)

    def shuffle(self):
        random.shuffle(self.__cards)

    def getDeckPrint(self):
        if self.cardsRemaining() == 0:
            return [None]

        cardWidth = 5
        printList = []
        for card in self.__cards:
            space = '   ' if len(str(card)) == 2 else '  '

            # Remove the last printable row to look as if this card is lying on the last card
            if len(printList) > 0:
                printList.pop()

            printList.append('+' + ('-' * cardWidth) + '+')
            printList.append('|' + str(card) + space + '|')
            printList.append('|' + (' ' * cardWidth) + '|')
            printList.append('|' + space + str(card) + '|')
        printList.append('+' + ('-' * cardWidth) + '+')
        return printList
