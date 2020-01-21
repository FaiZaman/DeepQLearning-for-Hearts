import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class DeepQNetwork(nn.Module):

    # initialises the networks with one hidden layer
    def __init__(self, learning_rate, input_size, hidden_size, n_actions):

        super(DeepQNetwork, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.n_actions = n_actions

        # connect layers
        self.input_hidden_connected_layer = nn.Linear(*self.input_size, self.hidden_size)
        self.hidden_output_connected_layer = nn.Linear(self.hidden_size, self.n_actions)

        # optimise the network
        self.optimiser = optim.Adam(self.parameters(), lr=learning_rate)
        self.loss = nn.MSELoss()    # mean square error loss function

        # perform actions on the GPU
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cuda:1')
        self.to(self.device)

    
    def forward(self, observation):

        # get state and run ReLu activation function
        state = T.Tensor(observation).to(self.device)
        x = F.relu(self.input_hidden_connected_layer(state))

        # get and return action
        actions = self.hidden_output_connected_layer(x)
        return actions
