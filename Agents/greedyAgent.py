import numpy

class GreedyAgent():


    def __init__(self, name, params = None):

        self.name = name
    

    def perform_action(self, observation):

        event = observation['event_name']
        hand = observation['data']['hand']

        if event == 'PassCards':
            
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

            if '2c' in hand:
                choose_card = '2c'
            else:
                # choose the legal card with the smallest value to play
                
