##
#
##

import unittest
import AcesUp.Suit
import AcesUp.Card

class TestCardClass(unittest.TestCase):
    def test_cards_are_equal(self):
        card1 = Card(Suit.HEART, 2)
        card2 = Card(Suit.HEART, 2)
        self.assertTrue(card1 == card2)

    def test_cards_with_different_positions_are_not_equal(self):
        card1 = Card(Suit.HEART, 2)
        card2 = Card(Suit.HEART, 3)
        self.assertFalse(card1 == card2)

    def test_cards_with_different_suits_are_not_equal(self):
        card1 = Card(Suit.HEART, 2)
        card2 = Card(Suit.SPADE, 2)
        self.assertFalse(card1 == card2)

    def test_cards_with_different_suits_and_positions_are_not_equal(self):
        card1 = Card(Suit.HEART, 2)
        card2 = Card(Suit.SPADE, 3)
        self.assertFalse(card1 == card2)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
