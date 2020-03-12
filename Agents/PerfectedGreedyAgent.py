import numpy

class PerfectedGreedyAgent():


    def __init__(self, name, params = None):

        self.name = name
    

    def perform_action(self, observation):

        event = observation['event_name']

        if event == 'PassCards':
            
            hand = observation['data']['hand']
            pass_list = []

            # choose the cards with the greatest value to swap
            for card in hand:
                if card[0] == 'A' or card[0] == 'K' or card[0] == 'Q' or card[0] == 'J':
                    if len(pass_list) < 3:
                        pass_list.append(card)
                    else:
                        break
            if len(pass_list) < 3:
                for card in hand:
                    if card[0] == 'T' or card[0] == '9' or card[0] == '8':
                        if len(pass_list) < 3:
                            pass_list.append(card)
                        else:
                            break
            if len(pass_list) < 3:
                for card in hand:
                    if card[0] == '7' or card[0] == '6' or card[0] == '5':
                        if len(pass_list) < 3:
                            pass_list.append(card)
                        else:
                            break

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
                card = '2c'
            else:
                hearts_broken = observation['data']['IsHeartsBroken']
                trick_suit = observation['data']['trickSuit']
                trick_number = observation['data']['trickNum']
                if trick_suit == "Unset":
                    if hearts_broken and trick_number > 1:
                        # agent plays first card of any suit since hearts is broken
                        card = self.find_smallest_card(hand)
                    else:
                        # agent plays first card of any suit except for hearts
                        no_hearts_hand = self.remove_hearts(hand)
                        card = self.find_largest_card(no_hearts_hand)
                else:
                    # agent plays second/third/fourth card
                    # if at least one card of tricksuit in hand, limit to cards of tricksuit
                    legal_hand = self.remove_illegal_cards(hand, trick_suit, trick_number, hearts_broken)
                    card = self.find_largest_card(legal_hand)

            return {
                "event_name": "PlayTrick_Action",
                "data": {
                    'playerName': self.name,
                    'action': {
                        'card': card,
                    }
                }
            }
    

    def find_smallest_card(self, hand):

        smallest_card_value = 15
        smallest_card_suit = 'c'

        # choose the legal card with the smallest value to play
        for card in hand:
            if card[0] == 'A':
                if 14 <= smallest_card_value:
                    smallest_card_value = 14
                    smallest_card_suit = card[1]
            elif card[0] == 'K':
                if 13 <= smallest_card_value:
                    smallest_card_value = 13
                    smallest_card_suit = card[1]
            elif card[0] == 'Q':
                if 12 <= smallest_card_value:
                    smallest_card_value = 12
                    smallest_card_suit = card[1]
            elif card[0] == 'J':
                if 11 <= smallest_card_value:
                    smallest_card_value = 11
                    smallest_card_suit = card[1]
            elif card[0] == 'T':
                if 10 <= smallest_card_value:
                    smallest_card_value = 10
                    smallest_card_suit = card[1]
            else:
                if int(card[0]) < smallest_card_value:
                    smallest_card_value = int(card[0])
                    smallest_card_suit = card[1]
        
        if smallest_card_value == 10:
            smallest_card_value = 'T'
        elif smallest_card_value == 11:
            smallest_card_value = 'J'
        elif smallest_card_value == 12:
            smallest_card_value = 'Q'
        elif smallest_card_value == 13:
            smallest_card_value = 'K'
        elif smallest_card_value == 14:
            smallest_card_value = 'A'

        smallest_card = str(smallest_card_value) + smallest_card_suit
        return smallest_card

    
    def find_largest_card(self, hand):

        largest_card_value = 2
        largest_card_suit = 'c'

        # choose the legal card with the largest value to play
        for card in hand:
            if card[0] == 'A':
                if largest_card_value < 14:
                    largest_card_value = 14
                    largest_card_suit = card[1]
            elif card[0] == 'K':
                if largest_card_value < 13:
                    largest_card_value = 13
                    largest_card_suit = card[1]
            elif card[0] == 'Q':
                if largest_card_value < 12:
                    largest_card_value = 12
                    largest_card_suit = card[1]
            elif card[0] == 'J':
                if largest_card_value < 11:
                    largest_card_value = 11
                    largest_card_suit = card[1]
            elif card[0] == 'T':
                if largest_card_value < 10:
                    largest_card_value = 10
                    largest_card_suit = card[1]
            else:
                if largest_card_value < int(card[0]):
                    largest_card_value = int(card[0])
                    largest_card_suit = card[1]
        
        if largest_card_value == 10:
            largest_card_value = 'T'
        elif largest_card_value == 11:
            largest_card_value = 'J'
        elif largest_card_value == 12:
            largest_card_value = 'Q'
        elif largest_card_value == 13:
            largest_card_value = 'K'
        elif largest_card_value == 14:
            largest_card_value = 'A'

        largest_card = str(largest_card_value) + largest_card_suit
        return largest_card
    

    def remove_hearts(self, hand):

        no_hearts_hand = hand.copy()
        for card_index in range(len(no_hearts_hand) - 1, -1, -1):
            if no_hearts_hand[card_index][1] == 'h':
                del no_hearts_hand[card_index]

        if no_hearts_hand == []:
            return hand
        return no_hearts_hand


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
                return self.remove_hearts(hand.copy())
            else:
                return hand


    def is_legal_present(self, hand, trick_suit):

        for card in hand:
            if card[1] == trick_suit:
                return True
        return False
                