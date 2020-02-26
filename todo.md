# Greedy Agent

A better greedy agent can be created by first checking if hearts is broken
If true then choose biggest card, otherwise choose smallest card
If true choose biggest except for QoS
Riskier but better overall

# Action space

Modify the action space so that it only contains the values that the agent can legally play 
at the specific state - size 13 still, but keep some as -1 or 0 to determine which ones are usable
Done this - hits error on line 87 for infinite loop - needs fixing

# Bug fixing

- Currently equation bug is fixed by using batch size = 1 instead of 64. Obviously a temp solution so
we need to find the real one.
- Matrix size mismatch bug needs fixing too; may be harder

# Network inputs

Experiment with different inputs, eg [52, 13] or [1, 52] etc

# Testing

Test with DQN agent from stable baselines to check whether environment is fine

# Illegal moves

Possibly allow the agent to play illegal moves, but disqualify it if it does to ensure it learns what
moves are illegal

# Rewards

Add rewards in between hands, not just at the end of a hand

# Plotting

Plot the score graphs