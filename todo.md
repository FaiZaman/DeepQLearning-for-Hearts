# Greedy Agent

A better greedy agent can be created by first checking if hearts is broken
If true then choose biggest card, otherwise choose smallest card
If true choose biggest except for QoS
Riskier but better overall

# Bug fixing

Figure out why episodes take so long

# Illegal moves

Give a large negative reward for an invalid action and don't progress the game until a valid one is chosen
So store transition = current_state, invalid_action, large_negative_reward, current_state
Can cap it so after a couple of invalid moves you force it to choose a valid one

# Training/Fine-tuning/Improvement

Tune the rewards, learning rate, gamma, and epsilon
Research an approporiate architecture for the neural network
Choose a better loss function   

# Plotting

Perhaps plot the average score per hand rather than per game

# This week

Fixed errors and now agent runs properly with equation
Fixed other bugs that popped up (< rather than >)
Related work finished
Changed rewards to give them every trick rather than end of every round
Plotted average scores over a range rather than every single point and made it dynamic
Stored transitions better with each state, action, reward, next state corresponding properly

question: who's second marker?