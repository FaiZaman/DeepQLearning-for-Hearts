# Greedy Agent

A better greedy agent can be created by first checking if hearts is broken
If true then choose biggest card, otherwise choose smallest card
If true choose biggest except for QoS
Riskier but better overall

# Training/Fine-tuning/Improvement

Tune the rewards, learning rate, gamma, and epsilon
Research an approporiate architecture for the neural network

# This week

Allowing invalid actions takes too long for agent to learn - likely because of large number of changing invalid actions (can discuss attempt in paper)
Fixed the max/min error when filtering invalid actions
Limiting the agent's learning to once every 4 steps as in literature - optimisation
Settled on Huber loss as it is more accurate - show graphs
Plotted loss against episodes and it decreases - show graphs
Plotting loss against learning rate to find optimum learning rate
Refinement: use a copy target network as in DDQN paper to calculate target Q-value, replace every tau steps

# Paper - Solution

Other agent types
Q-network and Target network
Epsilon greedy
Network Architecture
Invalid actions
Training 
    - loss function and equation from file:///C:/Users/faizz/Downloads/978-1-61499-672-9-1362.pdf
    - hyperparameter optimisation
4 step learning - ref https://arxiv.org/pdf/1609.05521.pdf section 5.1
