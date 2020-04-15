# Greedy Agent

A better greedy agent can be created by first checking if hearts is broken
If true then choose biggest card, otherwise choose smallest card
If true choose biggest except for QoS
Riskier but better overall

# Illegal moves

Possibly allow the agent to play illegal moves, but disqualify it if it does to ensure it learns what
moves are illegal

# Training/Fine-tuning/Improvement

Tune the rewards, learning rate, gamma, and epsilon
Research an approporiate architecture for the neural network
Choose a better loss function   

# Plotting

Perhaps plot the average score per hand rather than per game

# Experience replay

Replay buffer with minibatches of experiences to sample and learn from

# This week

Allowing invalid actions takes too long for agent to learn - likely because of large number of changing invalid actions (can discuss attempt in paper)
Fixed the max/min error when filtering invalid actions
Limiting the agent's learning to once every 4 steps as in literature - optimisation
Settled on Huber loss as it is more accurate - show graphs
Plotted loss against episodes and it decreases - show graphs
Plotting loss against learning rate to find optimum learning rate
Refinement: use a copy target network as in DDQN paper to calculate target Q-value, replace every tau steps