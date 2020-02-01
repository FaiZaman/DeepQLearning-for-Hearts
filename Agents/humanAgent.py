

class HumanAgent:


    def __init__(self, name, params):

        self.name = name
    
    
    def Do_Action(self, observation):

        event = observation['event_name']

        if event == 'GameStart':
            print(observation)
        elif event == 'NewRound':
            print(observation)
        elif event == 'PassCards':
            print(observation)
            passCards = []
            for i in range(3):
                passCards.append(input('{0} pass card{1}: '.format(self.name, i+1)))
            
            print('passCards: ', passCards)
            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }
        
        elif event == 'ShowPlayerHand':
            print(observation)
        
        elif event == 'PlayTrick':
            print(observation)
            hand = observation['data']['hand']
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = input('choose card: ')

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }
        elif event == 'ShowTrickAction':
            print(observation)
        elif event == 'ShowTrickEnd':
            print(observation)
        elif event == 'RoundEnd':
            print(observation)
        elif event == 'GameOver':
            print(observation)            