# Greedy Agent

A better greedy agent can be created by first checking if hearts is broken
If true then choose biggest card, otherwise choose smallest card
If true choose biggest except for QoS
Riskier but better overall

# Network inputs

Experiment with different inputs, eg [52, 13] or [1, 52] etc

# Illegal moves

Possibly allow the agent to play illegal moves, but disqualify it if it does to ensure it learns what
moves are illegal

# Rewards

Add rewards in between hands, not just at the end of a hand

# Training/Fine-tuning/Improvement

Tune the rewards, learning rate, gamma, and epsilon
Research an approporiate architecture for the neural network

# Experience replay

Replay buffer with minibatches of experiences to sample and learn from

# This week

Fixed errors and now agent runs properly with equation
Related work in progress
