import gym

from Hearts import *
from Agents.humanAgent import HumanAgent
from Agents.randomAgent import RandomAgent
from Agents.greedyAgent import GreedyAgent
from Agents.RLAgent import RLAgent

num_episodes = 10
max_score = 100

playersNameList = ['Agent', 'Boris', 'Calum', 'Diego']
agent_list = [0, 0, 0, 0]
gamma = 0.999
epsilon = 1
learning_rate = 0.02
batch_size = 64
n_actions = 52

# Human vs Random
"""
agent_list[0] = HumanAgent(playersNameList[0], {})
agent_list[1] = RandomAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
"""
# Random play
"""
agent_list[0] = RandomAgent(playersNameList[0], {'print_info': False})
agent_list[1] = RandomAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
"""
"""
# Greedy Agent
agent_list[0] = GreedyAgent(playersNameList[0], {'print_info': False})
agent_list[1] = GreedyAgent(playersNameList[1], {'print_info': False})
agent_list[2] = GreedyAgent(playersNameList[2], {'print_info': False})
agent_list[3] = GreedyAgent(playersNameList[3], {'print_info': False})
"""
# RL Agent

agent_list[0] = RLAgent(playersNameList[0], gamma, epsilon, learning_rate, batch_size, n_actions)
agent_list[1] = GreedyAgent(playersNameList[1], {'print_info': False})
agent_list[2] = GreedyAgent(playersNameList[2], {'print_info': False})
agent_list[3] = GreedyAgent(playersNameList[3], {'print_info': False})


env = gym.make('Hearts_Card_Game-v0')
env.__init__(playersNameList, max_score)

for _ in range(num_episodes):
    
    observation = env.reset()   # return initial observation
    
    while True:

        # render environment and initialise score and action
        env.render()        
        is_broadcast = observation['broadcast']
        action = None
        score = 0

        # let other players know of state if state is public, otherwise if action then only player performing knows
        if is_broadcast:
            for agent in agent_list:
                if isinstance(agent, RandomAgent) or isinstance(agent, GreedyAgent) or isinstance(agent, HumanAgent):
                    agent.perform_action(observation)

        else:
            playerName = observation['data']['playerName']
            for agent in agent_list:
                if agent.name == playerName:
                    if isinstance(agent, RLAgent):
                        action = agent.choose_action(observation)
                    else:
                        action = agent.perform_action(observation)

        # get and store environment data after making action, then learn and reset observation
        new_observation, reward, done, info = env.step(action)
        for agent in agent_list:
            if isinstance(agent, RLAgent):
                agent.store_transition(observation, action, reward, new_observation, done)
                agent.learn()
        observation = new_observation

        if reward:
            print('\nreward: {0}\n'.format(reward))
            score += reward['Agent']

        if done:
            print('\nGame Over!!\n')
            break
