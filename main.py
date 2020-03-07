import gym
from matplotlib import pyplot as plt

from Hearts import *
from Agents.humanAgent import HumanAgent
from Agents.randomAgent import RandomAgent
from Agents.greedyAgent import GreedyAgent
from Agents.PerfectedGreedyAgent import PerfectedGreedyAgent
from Agents.RLAgent import RLAgent

num_episodes = 10
max_score = 100

playersNameList = ['Agent', 'Boris', 'Calum', 'Diego']
agent_list = [0, 0, 0, 0]
gamma = 0.999
epsilon = 1
learning_rate = 0.001
batch_size = 64
n_actions = 52
score_list = [[], [], [], []]

# Human vs Random
"""
agent_list[0] = HumanAgent(playersNameList[0], {})
agent_list[1] = RandomAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
"""
# Greedy vs Random play
"""
agent_list[0] = Greedy(playersNameList[0], {'print_info': False})
agent_list[1] = RandomAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
"""
"""
# Greedy Agent
agent_list[0] = PerfectedGreedyAgent(playersNameList[0], {'print_info': False})
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

for episode_number in range(num_episodes):
        
    observation = env.reset()   # return initial observation
    done = False
    scores = [0, 0, 0, 0]

    while not done:

        print("=======================ep number:", episode_number)

        # render environment and initialise score and action
        env.render()        
        is_broadcast = observation['broadcast']
        action = None

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
            if isinstance(agent, RLAgent) and observation['event_name'] != 'GameOver':
                agent.store_transition(observation, action, reward, new_observation, done)
                agent.learn()
        observation = new_observation

        if reward:
            print('\nreward: {0}\n'.format(reward))
            scores[0] += reward['Agent']
            scores[1] += reward['Boris']
            scores[2] += reward['Calum']
            scores[3] += reward['Diego']

        if done:
            for i in range(0, len(score_list)):
                score_list[i].append(scores[i])
            print('\nGame Over!!\n')


# plot the results
print(score_list)

plt.ylim(-120, 20)
plt.plot(score_list[0], label="Agent")

for i in range(1, len(score_list)):
    plt.plot(score_list[i], label="Greedy " + str(i))

plt.title('Scores over episodes')
plt.xlabel('Episode number')
plt.ylabel('Reward')
plt.legend(loc="upper right")

plt.show()