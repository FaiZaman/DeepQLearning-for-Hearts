
class HumanAgent:

    def __init__(self):

        self.name = self.choose_name()


    def choose_name(self):

        name = str(input("Please enter your name: "))
        return name


    def choose_action(self, observation):

        event = observation['event_name']

        if event == 'NewRound':
            
            round_number = observation['data']['roundNumber']
            print("\n==========Round " + str(round_number) + "==========")
            print("Current Scores:")
            for pair in observation['data']['players']:
                print(pair['playerName'] + ": " + str(pair['score']))

        if event == 'PassCards':

            hand = observation['data']['hand']
            print("\n====Pass Cards Phase====")
            print("Your Hand:", hand)

            passCards = []
            i = 0
            while i < 3:
                pass_card = input('{0}, choose card {1} to pass: '.format(self.name, i+1))
                if len(pass_card) > 1:
                    pass_card = pass_card[0].upper() + pass_card[1]
                    if pass_card in hand:
                        passCards.append(pass_card)
                        i += 1
                    else:
                        print("This card is not in your hand. Please choose another card.")
                else:
                    print("Invalid card. Please try again.")
                
            print('Cards passed:', passCards)

            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }
        
        elif event == 'PlayTrick':
            
            hand = observation['data']['hand']
            current_trick = observation['data']['currentTrick']
            trick_number = observation['data']['trickNum']
            trick_suit = observation['data']['trickSuit']
            hearts_broken = observation['data']['IsHeartsBroken']
            playable_hand = self.get_real_hand(hand, trick_suit, trick_number, hearts_broken)

            if trick_number == 1:
                print("\n======Playing Phase======")

            print("\n===Trick " + str(trick_number) + " Of Suit " + str(trick_suit).upper() + "===")

            if hearts_broken:
                print("Hearts has been broken")
            else:
                print("Hearts has not yet been broken")
            
            for pair in reversed(current_trick):
                print(pair['playerName'] + ": " + pair['card'])

            print("Your Full Hand:", hand)
            print("Your Playable Hand:", playable_hand)

            if '2c' in hand:
                choose_card = '2c'
                print("You played 2c")
            else:
                choosing = True
                while choosing:
                    choose_card = input(self.name + ', choose a card to play: ')
                    if len(choose_card) > 1:
                        choose_card = choose_card[0].upper() + choose_card[1]
                        if choose_card in hand:
                            if choose_card not in playable_hand:
                                print("This card is not allowed to be played right now - " +\
                                "please choose another.")
                            else:
                                choosing = False
                        else:
                            print("This card is not in your hand. Please choose another card.")
                    else:
                        print("Invalid card. Please try again.")

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }

        elif event == 'ShowTrickEnd':
            data = observation['data']
            print("\nTrick Winner - " + data['trickWinner'] + ": " + str(data['cards']))
        
        elif event == 'GameOver':
            
            data = observation['data']
            lowest_score = 1000
            print("\nGame Over!")
            print("Final Scores:")

            for pair in data['players']:
                score = pair['score']
                if score < lowest_score:
                    lowest_score = score
                print(pair['playerName'] + ": " + str(score))

            print("The winner is " + data['Winner'] + " with a score of " + str(lowest_score) + "!")


    def get_real_hand(self, hand, trick_suit, trick_number, hearts_broken):

        if trick_suit == "Unset":
            if hearts_broken and trick_number > 1:
                # agent can play card of any suit since hearts is broken
                return hand
            else:
                # agent plays first card of any suit except for hearts
                legal_hand = self.remove_hearts(hand)
        else:
            # agent plays second/third/fourth card
            # if at least one card of tricksuit in hand, limit to cards of tricksuit
            legal_hand = self.remove_illegal_cards(hand, trick_suit, trick_number, hearts_broken)

        # remove Queen of Spades from hand so not played in first round
        if trick_number == 1 and 'Qs' in legal_hand:
            legal_hand.remove('Qs')
        return legal_hand


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
