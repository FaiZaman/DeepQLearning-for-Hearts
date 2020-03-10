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

# Rewards + actions

Check that rewards correspond to the correct specific actions
(if not, make it so that each action eg [0001000] corresponds to specific reward at whichever state)

# Plotting

Perhaps plot the average score per hand rather than per game

# Experience replay

Replay buffer with minibatches of experiences to sample and learn from

# This week

Fixed errors and now agent runs properly with equation
Related work in progress
Changed rewards to give them every trick rather than end of every round
Plotted average scores over a range rather than every single point and made it dynamic