import random
from datetime import datetime

class RandomAgent:


    def __init__(self, name, params = None):
        random.seed(datetime.now())
        self.name = name
        
        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False
    

    def perform_action(self, observation):

        self.print_info = False

        event = observation['event_name']
        
        if event == 'GameStart' or event == 'NewRound' or event == 'PassCards' or event == 'ShowPlayerHand':
            if self.print_info
                print(observation)
        
        if event == 'PassCards':

            passCards = random.sample(observation['data']['hand'], 3)
            
            if self.print_info:
                print(self.name, ' pass cards: ', passCards)
                
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }

        elif event == 'PlayTrick':
            
            if self.print_info:
                print("===========", observation, "==========")

            hand = observation['data']['hand']
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = random.choice(observation['data']['hand'])
                if self.print_info:
                    print(self.name, ' choose card: ', choose_card)
            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }

        if self.print_info:
            elif event == 'ShowTrickAction' or event == 'ShowTrickEnd'\
                or event == 'RoundEnd' or event == 'GameOver':
                print(observation)    


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
