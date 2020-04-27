import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class DeepQNetwork(nn.Module):

    # initialises the networks with one hidden layer
    def __init__(self, learning_rate, n_actions):

        super(DeepQNetwork, self).__init__()
        self.n_actions = n_actions

        # connect layers
        self.input_hidden_connected_layer = nn.Linear(2 * 52, 1024)    # input = [2, 52]
        self.hidden_hidden_connected_layer_1 = nn.Linear(1024, 512)
        self.hidden_hidden_connected_layer_2 = nn.Linear(512, 416)
        self.hidden_hidden_connected_layer_3 = nn.Linear(416, 256)
        self.hidden_hidden_connected_layer_4 = nn.Linear(256, 104)
        self.hidden_output_connected_layer = nn.Linear(104, self.n_actions)

        # optimise the network
        self.optimiser = optim.Adam(self.parameters(), lr=learning_rate)
        self.loss = nn.SmoothL1Loss()    # Huber loss function

        # perform actions on the GPU
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cuda:1')
        self.to(self.device)

    
    def forward(self, observation):

        # get state and run ReLu activation function
        state = T.Tensor(observation).to(self.device).reshape(-1, 2*52)
        x = F.relu(self.input_hidden_connected_layer(state))
        x = F.relu(self.hidden_hidden_connected_layer_1(x))
        x = F.relu(self.hidden_hidden_connected_layer_2(x))
        x = F.relu(self.hidden_hidden_connected_layer_3(x))
        x = F.relu(self.hidden_hidden_connected_layer_4(x))

        # get and return action
        actions = self.hidden_output_connected_layer(x)
        return actions
