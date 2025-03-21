"""
The Hearts environment was taken from https://github.com/zmcx16/OpenAI-Gym-Hearts 
and adapted for this project. This file was taken directly from the environment
"""

from .Hand import Hand

class Player:

    def __init__(self, name):

        self.name = name
        self.hand = Hand()
        self.score = 0
        self.tricksWon = []
        self.CardsInRound = []
        self.wonCurrentTrick = False


    def addCard(self, card):
        self.hand.addCard(card)


    def play(self, card):
        return self.hand.playCard(card)


    def trickWon(self, cards):
        self.CardsInRound += cards


    def hasSuit(self, suit):
        return len(self.hand.hand[suit.iden]) > 0


    def removeCard(self, card):
        self.hand.removeCard(card)


    def discardTricks(self):
        self.tricksWon = []


    def resetRoundCards(self):
        self.CardsInRound = []


    def hasOnlyHearts(self):
        return self.hand.hasOnlyHearts()
