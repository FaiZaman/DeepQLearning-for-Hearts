import random
from datetime import datetime

class RandomAgent:

    def __init__(self, name):
        
        random.seed(datetime.now())
        self.name = name


    def choose_action(self, observation):

        event = observation['event_name']
        
        if event == 'PassCards':

            passCards = random.sample(observation['data']['hand'], 3)
                
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }

        elif event == 'PlayTrick':

            hand = observation['data']['hand']
            if '2c' in hand:
                random_card = '2c'
            else:

                hearts_broken = observation['data']['IsHeartsBroken']
                trick_suit = observation['data']['trickSuit']
                trick_number = observation['data']['trickNum']

                if trick_suit == "Unset":

                    if hearts_broken and trick_number > 1:
                        # agent plays first card of any suit since hearts is broken
                        random_card = random.choice(hand)

                    else:
                        # agent plays first card of any suit except for hearts
                        no_hearts_hand = self.remove_hearts(hand)
                        random_card = random.choice(no_hearts_hand)

                else:
                    # agent plays second/third/fourth card
                    # if at least one card of tricksuit in hand, limit to cards of tricksuit
                    legal_hand = self.remove_illegal_cards(hand, trick_suit, trick_number, hearts_broken)
                    random_card = random.choice(legal_hand)

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': random_card}
                    }
                }  


    # removes and returns the hand with no hearts
    def remove_hearts(self, hand):

        no_hearts_hand = hand.copy()
        for card_index in range(len(no_hearts_hand) - 1, -1, -1):
            if no_hearts_hand[card_index][1] == 'h':
                del no_hearts_hand[card_index]

        if no_hearts_hand == []:
            return hand
        return no_hearts_hand


    # removes and returns a hand containing only legal cards
    def remove_illegal_cards(self, hand, trick_suit, trick_number, hearts_broken):

        legal_present = self.is_legal_present(hand, trick_suit)

        if legal_present:
            legal_hand = []
            for card in hand:
                if card[1] == trick_suit:
                    legal_hand.append(card)
            return legal_hand
        else:
            if trick_number == 1:
                if 'Qs' in hand:
                    hand.remove('Qs')
                return self.remove_hearts(hand.copy())
            else:
                return hand


    # returns a boolean verifying whether the hand contains any legal cards
    def is_legal_present(self, hand, trick_suit):

        for card in hand:
            if card[1] == trick_suit:
                return True
        return False
