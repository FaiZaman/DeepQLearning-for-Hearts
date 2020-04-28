
class HumanAgent:

    def __init__(self):

        self.name = self.choose_name()


    def choose_name(self):

        name = str(input("Please choose a name: "))
        return name


    def perform_action(self, observation):

        event = observation['event_name']

        if event == 'GameStart' or event == 'NewRound' or event == 'PassCards':
            print(observation)

        if event == 'PassCards':

            passCards = []
            for i in range(3):
                passCards.append(input('{0}, choose card {1} to pass: '.format(self.name, i+1)))
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
                print("You played 2c")
            else:
                choose_card = input('Choose a card to play: ')

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }

        elif event == 'ShowTrickAction' or event == 'ShowTrickEnd'\
            or event == 'RoundEnd' or event == 'GameOver':
            print(observation)
