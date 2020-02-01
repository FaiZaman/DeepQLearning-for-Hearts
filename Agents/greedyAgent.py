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
                smallest_card = 14

                if trick_suit == "Unset":
                    if hearts_broken:
                        smallest_card = find_smallest_card(hand)
                    else:
                        no_hearts_hand = self.remove_illegal_cards(hand)
                        smallest_card = find_smallest_card(no_hearts_hand)
                else:
                    # first check if trick suit present in hand; if it is then limit cards to that suit
                    # otherwise let any card be played (except for hearts if hearts not broken)


            return {
                "event_name": "PlayTrick_Action",
                "data": {
                    'playerName': self.name,
                    'action': {'card': smallest_card}
                }
            }
    

    def find_smallest_card(self):

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


    def remove_illegal_cards(self, hand):

        legal_hand = hand.copy()
        for card in legal_hand:
            if card[1] == 'h':
                del legal[card]

        return legal
