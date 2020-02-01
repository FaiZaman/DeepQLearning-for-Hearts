import torch as T
import random as rand
import numpy as np
from Network import DeepQNetwork

class RLAgent(object):

    # batch size = number of experiences sampled
    def __init__(self, name, gamma, epsilon, learning_rate, input_size, batch_size, n_actions,    # gamma = discount factor
                 max_mem_size=1000000, epsilon_min=0.01, epsilon_decrement = 0.996):        # epsilon for epsilon greedy

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
        self.Q_eval = DeepQNetwork(learning_rate, input_size, hidden_size=4, n_actions=13)
        self.state_memory = np.zeros((self.memory_size, *input_size))
        self.new_state_memory = np.zeros((self.memory_size, *input_size))   # used to overwrite memories as agent acquires them
        self.action_memory = np.zeros((self.memory_size, self.n_actions), dtype=np.uint8)
        self.reward_memory = np.zeros(self.memory_size)
        self.terminal_memory = np.zeros(self.memory_size, dtype=np.uint8)   # sequence of done flags


    # function for storing memories
    def store_transition(self, state, action, reward, state_, terminal):

        index = self.memory_counter % self.memory_size    # find position in memory
        self.state_memory[index] = state

        # one hot encoding
        actions = np.zeros(self.n_actions)
        actions[action] = 1.0
        self.action_memory[index] = actions

        # setting memory
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - terminal
        self.new_state_memory[index] = state_
        
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
            else:

                # epsilon greedy policy
                if rand.random() < self.epsilon:
                    action = np.random.choice(self.action_space)
                else:
                    actions = self.Q_eval.forward(observation)      # get action list from neural network
                    action = T.argmax(actions).item()               # choose action with greatest value
                
                print(action, hand)
                card_chosen = hand[action]
                return {
                    "event_name": "PlayTrick_Action",
                    "data": {
                        'playerName': self.name,
                        'action': { 'card': card_chosen }
                    }
                }

    
    def learn(self):

        if self.memory_counter < self.batch_size:   # improves correlation
            
            # reset grad and set maximum memory
            self.Q_eval.optimiser.zero_grad()
            if self.memory_counter < self.memory_size:
                max_memory = self.memory_counter
            else:
                max_memory = self.memory_size

        # get batch memories
        batch = np.random.choice(max_memory, self.batch_size)
        state_batch = self.state_memory[batch]
        action_batch = self.action_memory[batch]
        action_values = np.array(self.action_space, dtype=uint8)
        action_indices = np.dot(action_batch, action_values)
        reward_batch = self.reward_memory[batch]
        terminal_batch = self.terminal_memory[batch]
        new_state_batch = self.new_state_memory[batch]

        reward_batch = T.Tensor(reward_batch).to(self.Q_eval.device)
        terminal_batch = T.Tensor(terminal_batch).to(self.Q_eval.device)

        q_predicted = self.Q_eval.forward(state_batch).to(self.Q_eval.device)
        q_target = self.Q_eval.forward(state_batch).to(self.Q_eval.device)
        q_next = self.Q_eval.forward(new_state_batch).to(self.Q_eval.device)

        # update the Q-values using the equation Q(s, a) = r(s, a) + gamma*max(Q(s', a))
        batch_index = np.arrange(self.batch_size, dtype=np.int32)
        q_target[batch_index, action_indices] = reward_batch + self.gamma * T.max(q_next, dim=1)[0] * terminal_batch

        # update epsilon for epsilon greedy
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decrement
        else:
            self.epsilon = self.epsilon_min
        
        # set loss function (mean squared error), backwards propagation, and optimiser step
        loss = self.Q_eval.loss(q_target, q_predicted).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimiser.step()
