import gym
from matplotlib import pyplot as plt

from Hearts import *
from Agents.humanAgent import HumanAgent
from Agents.randomAgent import RandomAgent
from Agents.greedyAgent import GreedyAgent
from Agents.PerfectedGreedyAgent import PerfectedGreedyAgent
from Agents.RLAgent import RLAgent

num_episodes = 100
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
agent_list[0] = RLAgent(playersNameList[0], gamma, epsilon, learning_rate, batch_size, n_actions)
agent_list[1] = HumanAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
"""

# RL vs Random play
"""
agent_list[0] = RLAgent(playersNameList[0], gamma, epsilon, learning_rate, batch_size, n_actions)
agent_list[1] = RandomAgent(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAgent(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAgent(playersNameList[3], {'print_info': False})
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
    if episode_number % 1 == 0:
        print("=======================ep number:", episode_number)

    while not done:

        # render environment and initialise score and action
        env.render()        
        is_broadcast = observation['broadcast']
        action = None

        # let other players know of state if state is public
        # otherwise if action then only player performing knows
        if is_broadcast:
            for agent in agent_list:
                if not isinstance(agent, RLAgent):
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
                if observation['event_name'] != 'GameOver':

                    if observation['event_name'] == 'PlayTrick':
                        if observation['data']['currentTrick'] == []:

                            # store current state to be used in experience replay
                            agent.last_current_state = new_observation
                        
                        if observation['data']['playerName'] == "Agent":
                            
                            # store action to be used in experience replay
                            agent.last_action = action

                    if new_observation['event_name'] == 'ShowTrickEnd':
                        
                        #print("showtrickend", agent.num_of_invalid_actions)
                        # if action was invalid give large negative reward with no state change
                        if agent.num_of_invalid_actions > 0:
                            reward = [30, 0, 0, 0]
                            stored_next_state = agent.last_current_state
                        else:
                            stored_next_state = new_observation

                        # store reward and commence storing the transition
                        stored_current_state = agent.last_current_state
                        stored_action = agent.last_action
                        stored_reward = reward
                        stored_next_state = new_observation

                        agent.store_transition(stored_current_state, stored_action, \
                                                stored_reward, stored_next_state, done)
                        agent.learn()
                    
                    else:
                        break;
            else:
                break;

        for agent in agent_list:
            if isinstance(agent, RLAgent):
                if observation['event_name'] == 'ShowTrickEnd':
                    if agent.num_of_invalid_actions == 0:
                        observation = new_observation
                        break;
                    else:
                        observation = agent.last_current_state
                else:
                    observation = new_observation
                    break;

        if reward:
            #print('\nreward: {0}\n'.format(reward))
            for r in range(0, 4):
                scores[r] -= reward[r]
        if done:
            for i in range(0, len(score_list)):
                score_list[i].append(scores[i])
            #print('\nGame Over!\n')

print(score_list)
plottable_score_list = [[], [], [], []]
plot_range = int(num_episodes / 10)

for player in range(0, 4):
    for i in range(1, num_episodes + 1):
        if i % plot_range == 0:
            average_over_past_range = sum(score_list[player][i - plot_range:i])/plot_range
            plottable_score_list[player].append(average_over_past_range)

# plot the results
#plt.ylim(-120, 20)
plt.plot([x for x in range(1, num_episodes + 1) if x % plot_range == 0],\
        plottable_score_list[0], label="Agent")

for i in range(1, len(plottable_score_list)):
    plt.plot([x for x in range(1, num_episodes + 1) if x % plot_range == 0],\
        plottable_score_list[i], label="Greedy " + str(i))

plt.title('Scores over episodes')
plt.xlabel('Episode number')
plt.ylabel('Reward')
plt.legend(loc="upper right")

plt.show()
