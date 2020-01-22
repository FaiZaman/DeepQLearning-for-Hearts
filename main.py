import gym

from Hearts import *
from Agent.human import Human
from Agent.randomAI import RandomAI
from Agent.Agent import Agent

num_episodes = 10
max_score = 100

playersNameList = ['Aqua', 'Boris', 'Calum', 'Diego']
agent_list = [0, 0, 0, 0]
gamma = 0.999
epsilon = 1
learning_rate = 0.02
input_size = [2]
batch_size = 64
n_actions = 13

# Human vs Random
"""
agent_list[0] = Human(playersNameList[0], {})
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})
"""
# Random play
"""
agent_list[0] = RandomAI(playersNameList[0], {'print_info': False})
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})
"""
# My Agent

agent_list[0] = Agent(playersNameList[0], gamma, epsilon, learning_rate, input_size, batch_size, n_actions)
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})


env = gym.make('Hearts_Card_Game-v0')
env.__init__(playersNameList, max_score)
print(isinstance(agent_list[0], RandomAI))

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
                if isinstance(agent, RandomAI):
                    agent.Do_Action(observation)

        else:
            playName = observation['data']['playerName']
            for agent in agent_list:
                if agent.name == playName:
                    if isinstance(agent, RandomAI):
                        action = agent.Do_Action(observation)
                    elif isinstance(agent, Agent):
                        action = agent.choose_action(observation)

        observation, reward, done, info = env.step(action)

        if reward:
            print('\nreward: {0}\n'.format(reward))
            score += reward

        if done:
            print('\nGame Over!!\n')
            break
