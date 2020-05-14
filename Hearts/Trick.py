"""
The Hearts environment was taken from https://github.com/zmcx16/OpenAI-Gym-Hearts 
and adapted for this project. This file was taken directly from the environment
"""

from .Card import Suit

hearts = 3 # the corresponding index to the suit hearts
spades = 2
queen = 12

class Trick:
    def __init__(self):
        self.trick = [0, 0, 0, 0]
        self.suit = Suit(-1)
        self.cardsInTrick = 0
        self.highest = 0 # rank of the high trump suit card in hand
        self.winner = -1

    def reset(self):
        self.trick = [0, 0, 0, 0]
        self.suit = -1
        self.cardsInTrick = 0
        self.highest = 0
        self.winner = -1

    def setTrickSuit(self, card):
        self.suit = card.suit

    def addCard(self, card, index):
        if self.cardsInTrick == 0: # if this is the first card added, set the trick suit
            self.setTrickSuit(card)

        self.trick[index] = card
        self.cardsInTrick += 1

        if card.suit == self.suit:
            if card.rank.rank > self.highest:
                self.highest = card.rank.rank
                self.winner = index
