

class HumanAgent:


    def __init__(self, name, params):

        self.name = name
    
    
    def perform_action(self, observation):

        event = observation['event_name']

        if event == 'GameStart':
            print(observation)

        elif event == 'NewRound':
            print(observation)

        elif event == 'PassCards':
            
            hand = observation['data']['hand']
            print(hand)
            passCards = []
            for i in range(3):
                passCards.append(input('Pass Card {0}: '.format(i+1)))
            
            print('passCards: ', passCards)
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }
        
        elif event == 'ShowPlayerHand':

            print("New Hand:", observation['data']['hand'])
        
        elif event == 'PlayTrick':

            hand = observation['data']['hand']
            print(hand)
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = input('choose card: ')

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {
                            'card': choose_card,
                        }
                    }
                }
        elif event == 'ShowTrickAction':
            print("Current Trick:", observation['data']['currentTrick'])

        elif event == 'ShowTrickEnd':
            print(observation)

        elif event == 'RoundEnd':
            print(observation)

        elif event == 'GameOver':
            print(observation)
