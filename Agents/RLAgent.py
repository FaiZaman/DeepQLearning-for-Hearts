import torch as T
import random as rand
import numpy as np
from Network import DeepQNetwork
from Dictionaries import Dictionary

class RLAgent(object):

    # batch size = number of experiences sampled
    # gamma = discount factor
    # epsilon for epsilon greedy
    def __init__(self, name, gamma, epsilon, learning_rate, batch_size, n_actions,   
                 max_mem_size=1000000, epsilon_min=0.01, epsilon_decrement = 0.996):

        self.name = name
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.n_actions = n_actions

        # e_end is the lowest value epsilon will decrease to, e_dec is factor by which epsilon decreases
        self.epsilon_min = epsilon_min              
        self.epsilon_decrement = epsilon_decrement

        self.memory_size = max_mem_size
        self.memory_counter = 0     # index of how many memories are stored
        self.action_space = [i for i in range(n_actions)]
        self.Network = DeepQNetwork(learning_rate, n_actions=52)

        self.state_memory = np.zeros((self.memory_size, *[2, 52]))
        self.action_memory = np.zeros((self.memory_size, self.n_actions), dtype=np.uint8)
        self.reward_memory = np.zeros(self.memory_size)
        self.new_state_memory = np.zeros((self.memory_size, *[2, 52]))   # overwrite memories as acquired
        self.terminal_memory = np.zeros(self.memory_size, dtype=np.uint8)   # sequence of done flags

        self.action_number_dict = Dictionary()    # for converting actions to a tensor number
        self.action_number_dict.choose_dict(dict_type="action")

        self.number_action_dict = Dictionary()    # for converting a number back to an action
        self.number_action_dict.choose_dict(dict_type="number")

        # for keeping track until reward is reached
        self.stored_state = None
        self.last_action = None
        self.safe_state = None

        # for dealing with invalid actions
        self.num_of_invalid_actions = 0
        self.invalid_action_buffer = 3


    # function for storing memories
    def store_transition(self, current_state, action, reward, next_state, terminal):
                
        index = self.memory_counter % self.memory_size    # find position in memory

        # convert state to tensor
        current_state_tensor = self.convert_state_to_tensor(current_state)
        next_state_tensor = self.convert_state_to_tensor(next_state)

        # convert action to int
        action = self.convert_action_to_number(action)

        # one hot encoding
        actions = np.zeros(self.n_actions)
        if current_state['event_name'] == 'PassCards':
            action = rand.sample(self.action_space, 1)
        
        if action:
            actions[action] = 1
        
        # add to memories and increment counter
        self.state_memory[index] = current_state_tensor
        self.action_memory[index] = actions
        self.reward_memory[index] = reward[0]   # only store agent's reward
        self.new_state_memory[index] = next_state_tensor
        self.terminal_memory[index] = 1 - terminal

        self.memory_counter += 1

    
    def choose_action(self, observation):

        # get event and hand name
        event = observation['event_name']
        hand = observation['data']['hand']

        # choose 3 random cards to pass if passing event
        if event == 'PassCards':
            passCards = rand.sample(hand, 3)
            
            return {
                "event_name": "PassCards_Action",
                "data": {
                    'playerName': self.name,
                    'action': { 'passCards': passCards }
                }
            }
        
        elif event == 'PlayTrick':


            if '2c' in hand:
                card_chosen = '2c'
                self.num_of_invalid_actions = 0
            else:

                trick_suit = observation['data']['trickSuit']
                trick_number = observation['data']['trickNum']
                hearts_broken = observation['data']['IsHeartsBroken']
                print("Agent", hand, self.num_of_invalid_actions, trick_number)
                playable_hand = self.get_real_hand(hand, trick_suit, trick_number, hearts_broken)
                playable_action_space = []

                for legal_card in playable_hand:
                    for card in hand:
                        if legal_card == card:
                            playable_action_space.append(hand.index(card))      

                # epsilon greedy policy
                if rand.random() < self.epsilon:

                    #print("random action taken")
                    card_chosen = np.random.choice(hand)

                    if card_chosen in playable_hand:
                        self.num_of_invalid_actions = 0
                    else:
                        self.num_of_invalid_actions += 1

                    if self.num_of_invalid_actions >= self.invalid_action_buffer:
                        self.num_of_invalid_actions = 0
                        card_chosen = np.random.choice(playable_hand)

                else:

                    #print("not random action chosen")
                    data_tensor = self.convert_state_to_tensor(observation)
                    actions = self.Network.forward(data_tensor)      # get action list from neural network

                    action = T.argmax(actions).item()               # choose action with greatest value
                    card_chosen = self.convert_number_to_action(action)

                    # deal with invalid action
                    if card_chosen in playable_hand:
                        self.num_of_invalid_actions = 0
                    else:
                        self.num_of_invalid_actions += 1

                    if self.num_of_invalid_actions >= self.invalid_action_buffer:

                        # redo action choice with invalid actions filtered out
                        actions = self.filter_output_actions(hand, actions)
                        action = T.argmax(actions).item()
                        card_chosen = self.convert_number_to_action(action)

            return {
                "event_name": "PlayTrick_Action",
                "data": {
                    'playerName': self.name,
                    'action': { 
                        'card': card_chosen,
                    }
                }
            }

    
    def learn(self):

        if self.memory_counter > self.batch_size:  # improves correlation - learning with enough memories
            
            # reset grad and set maximum memory
            self.Network.optimiser.zero_grad()
            if self.memory_counter < self.memory_size:
                max_memory = self.memory_counter
            else:
                max_memory = self.memory_size

            # get a batch of experiences from replay memory
            batch = np.random.choice(max_memory, self.batch_size)
            state_batch = self.state_memory[batch]
            action_batch = self.action_memory[batch]
            action_values = np.array(self.action_space, dtype=np.uint8)
            action_indices = np.dot(action_batch, action_values)
            reward_batch = self.reward_memory[batch]
            new_state_batch = self.new_state_memory[batch]
            terminal_batch = self.terminal_memory[batch]

            reward_batch = T.Tensor(reward_batch).to(self.Network.device)
            terminal_batch = T.Tensor(terminal_batch).to(self.Network.device)

            # input: (64, 2, 52), (64, 2, 52) outputs
            q_predicted = self.Network.forward(state_batch).to(self.Network.device)
            q_target = self.Network.forward(state_batch).to(self.Network.device)
            q_next = self.Network.forward(new_state_batch).to(self.Network.device)

            # update the Q-values using the equation Q(s, a) = r(s, a) + gamma*max(Q(s', a))
            batch_index = np.arange(self.batch_size, dtype=np.int32)
            action_indices = T.Tensor(action_indices).long().to(self.Network.device)

            q_target[batch_index, action_indices] =\
                reward_batch + self.gamma * T.max(q_next, dim=1)[0] * terminal_batch

            # update epsilon for epsilon greedy
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decrement
            else:
                self.epsilon = self.epsilon_min
            
            # set loss function (mean squared error), backwards propagation, and optimiser step
            loss = self.Network.loss(q_target, q_predicted).to(self.Network.device)
            
            #print(loss, self.memory_counter) # geospace
            loss.backward()
            self.Network.optimiser.step()


    def get_real_hand(self, hand, trick_suit, trick_number, hearts_broken):

        if trick_suit == "Unset":
            if hearts_broken and trick_number > 1:
                # agent can play card of any suit since hearts is broken
                return hand
            else:
                # agent plays first card of any suit except for hearts
                no_hearts_hand = self.remove_hearts(hand)
                return no_hearts_hand
        else:
            # agent plays second/third/fourth card
            # if at least one card of tricksuit in hand, limit to cards of tricksuit
            legal_hand = self.remove_illegal_cards(hand, trick_suit, trick_number, hearts_broken)
            return legal_hand
            

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


    def convert_state_to_tensor(self, state):

        event = state['event_name']
        data_tensor = T.zeros(2, 52)   # 52 cards in deck - first row for hand, second for table

        if event == 'PassCards':    # encode hand and leave table cards empty
            
            hand = state['data']['hand']
            data_tensor = self.convert_cards(hand, data_tensor, row=0)
        
        elif event == 'PlayTrick':  # encode both hand and table cards

            hand = state['data']['hand']
            trick_suit = state['data']['trickSuit']
            data_tensor = self.convert_cards(hand, data_tensor, row=1)

            # if no cards played yet no encoding; leave as zeros
            if trick_suit == "Unset":
                pass
            else:
                current_trick = state['data']['currentTrick']
                table_cards = []

                for i in current_trick:
                    table_cards.append(i['card'])
                
                self.convert_cards(table_cards, data_tensor, row=1)

        return data_tensor
     

    def convert_cards(self, card_list, tensor, row):

        for card in card_list:

            card_value = card[0]
            card_suit = card[1]

            if card_value == "T":
                card_value = 10
            elif card_value == "J":
                card_value = 11
            elif card_value == "Q":
                card_value = 12
            elif card_value == "K":
                card_value = 13
            elif card_value == "A":
                card_value = 14

            card_value = int(card_value)

            # encode clubs, diamonds, hearts, spades
            # encoding agent's hand
            if card_suit == 'c':    # clubs
                index = (card_value - 2) + 0
            elif card_suit == 'd':  # diamonds
                index = (card_value - 2) + 13
            elif card_suit == 'h':  # hearts
                index = (card_value - 2) + 26
            else:                   # spades
                index = (card_value - 2) + 39

            tensor[row][index] = 1
            return tensor


    def convert_action_to_number(self, action_state_dict):

        index = 0
        if action_state_dict:

            card = action_state_dict['data']['action']['card']
            index = self.action_number_dict.dict_object[card]
        
        return index

    
    def convert_number_to_action(self, number):

        action = self.number_action_dict.dict_object[number]
        return action


    # set values for actions not in hand to be infinite so not chosen
    def filter_output_actions(self, hand, actions):

        for number in range(0, len(actions[0])):
            action = self.convert_number_to_action(number)
            if action not in hand:
                actions[0][number] = 1000
        return actions
