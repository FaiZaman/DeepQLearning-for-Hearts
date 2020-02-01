import numpy

class GreedyAgent():


    def __init__(self, name, params = None):

        self.name = name
    

    def perform_action(self, observation):

        event = observation['event_name']

        if event == 'PassCards':
            
            hand = observation['data']['hand']
            pass_list = []

            # choose the cards with the greatest value to swap
            while len(pass_list) < 3:
                for card in hand:
                    if card[0] == 'A' or card[0] == 'K' or card[0] == 'Q' or card[0] == 'J':
                        pass_list.append(card)
            
            return {
                "event_name": "PassCards_Action",
                "data": {
                    'playerName': self.name,
                    'action': {'passCards': pass_list}
                }
            }

        elif event == 'PlayTrick':

            hand = observation['data']['hand']

            if '2c' in hand:
                smallest_card = '2c'
            else:
                hearts_broken = observation['data']['trickSuit']
                trick_suit = observation['data']['trickSuit']

                if trick_suit == "Unset":
                    if hearts_broken:
                        smallest_card = self.find_smallest_card(hand)
                    else:
                        no_hearts_hand = self.remove_hearts(hand)
                        smallest_card = self.find_smallest_card(no_hearts_hand)
                else:
                    legal_hand = self.remove_illegal_cards(hand, trick_suit, hearts_broken)
                    smallest_card = self.find_smallest_card(legal_hand)

            return {
                "event_name": "PlayTrick_Action",
                "data": {
                    'playerName': self.name,
                    'action': {'card': smallest_card}
                }
            }
    

    def find_smallest_card(self, hand):

        smallest_card = 14
        
        # choose the legal card with the smallest value to play
        for card in hand:
            if card[0] == 'A' and 14 <= smallest_card:
                smallest_card = card
            elif card[0] == 'K' and 13 <= smallest_card:
                smallest_card = card
            elif card[0] == 'Q' and 12 <= smallest_card:
                smallest_card = card
            elif card[0] == 'J' and 11 <= smallest_card:
                smallest_card = card
            elif card[0] == 'T' and 10 <= smallest_card:
                smallest_card = card
            else:
                if int(card[0]) < smallest_card:
                    smallest_card = card
        
        return smallest_card


    def remove_hearts(self, hand):

        no_hearts_hand = hand.copy()
        for card in no_hearts_hand:
            if card[1] == 'h':
                del no_hearts_hand[card]

        return no_hearts_hand


    def remove_illegal_cards(self, hand, trick_suit, hearts_broken):

        legal_present = False

        for card in hand:
            if card[1] == trick_suit:
                legal_present = True
                break
        
        legal_hand = hand.copy()
        if legal_present:
            for card in hand:
                if card[1] == trick_suit:
                    legal_hand.append(card)
        else:
            if not(hearts_broken):
                legal_hand = self.remove_hearts(legal_hand)
        
        return legal_hand
