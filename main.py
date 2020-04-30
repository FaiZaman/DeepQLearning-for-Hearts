import gym
import time
import torch as T
from matplotlib import pyplot as plt

from Hearts import *
from Agents.humanAgent import HumanAgent
from Agents.randomAgent import RandomAgent
from Agents.greedyAgent import GreedyAgent
from Agents.DQLAgent import DQLAgent

# change this to the directory you want to save and load your own models
PATH = "C:/Users/faizz/University Work/Year 3/Individual Project TH86/Triple_New_Model"

training = False
num_episodes = 2000
max_score = 100

playersNameList = ['Agent', 'Boris', 'Calum', 'Diego']
agent_list = [0, 0, 0, 0]

# hyperparameters
gamma = 0.99
epsilon = 1
learning_rate = 0.0001

batch_size = 32
n_actions = 52
score_list = [[], [], [], []]
average_scores_per_round = [[], [], [], []]


# saving and loading the models
def save_model(model, episode_number):

    save_path = PATH + "/model_" + str(episode_number) + ".pth"
    T.save(model.state_dict(), save_path)


def load_model(model, load_number):

    load_path = PATH + "/model_" + str(load_number) + ".pth"
    model.load_state_dict(T.load(load_path))

    return model


# DQL Agent Training

agent_list[0] = DQLAgent(gamma, epsilon, learning_rate, batch_size, n_actions, training)
agent_list[1] = GreedyAgent(playersNameList[1])
agent_list[2] = GreedyAgent(playersNameList[2])
agent_list[3] = GreedyAgent(playersNameList[3])

# DQL Agent Testing v Random
"""
agent_list[0] = DQLAgent(gamma, epsilon, learning_rate, batch_size, n_actions, training)
agent_list[1] = RandomAgent(playersNameList[1])
agent_list[2] = RandomAgent(playersNameList[2])
agent_list[3] = RandomAgent(playersNameList[3])
"""
# DQL Agent Testing v Human and Random
"""
agent_list[0] = HumanAgent()
agent_list[1] = DQLAgent(gamma, epsilon, learning_rate, batch_size, n_actions, training)
agent_list[2] = RandomAgent(playersNameList[2])
agent_list[3] = RandomAgent(playersNameList[3])
"""

dql_agent_index = 0
for index in range(0, len(agent_list)):
    if isinstance(agent_list[index], DQLAgent):
        dql_agent_index = index

env = gym.make('Hearts_Card_Game-v0')
env.__init__([agent.name for agent in agent_list], max_score)

if not training:
    model = load_model(agent_list[dql_agent_index].Q_network, load_number=2500)

start_time = time.time()

for episode_number in range(num_episodes + 1):
        
    observation = env.reset()   # return initial observation
    done = False
    scores = [0, 0, 0, 0]

    if training:
        if episode_number % 100 == 0:
            print("Training Episode Number:", episode_number)
            model = agent_list[dql_agent_index].Q_network
            save_model(model, episode_number)
    else:
        if episode_number % 10 == 0:
            print("Testing Episode Number:", episode_number)

    while not done:

        # render environment and initialise score and action
        env.render()        
        is_broadcast = observation['broadcast']
        event = observation['event_name']
        data = observation['data']
        action = None
        dql_agent = agent_list[dql_agent_index]

        # let other players know of state if state is public 
        # otherwise if action then only player performing knows
        if is_broadcast:
            for agent in agent_list:
                if isinstance(agent, HumanAgent):
                    agent.choose_action(observation)

        else:
            playerName = data['playerName']
            for agent in agent_list:
                if agent.name == playerName:
                    action = agent.choose_action(observation)

        # get and store environment data after making action, then learn and reset observation
        new_observation, reward, done, info = env.step(action)

        if event != 'GameOver' and training:

            if event == 'PlayTrick' and \
                data['playerName'] == "Agent":
                
                # store current state and action to be used in experience replay
                dql_agent.last_current_state = observation
                dql_agent.last_action = action

            elif new_observation['event_name'] == 'ShowTrickEnd':

                # store reward and commence storing the transition
                stored_current_state = dql_agent.last_current_state
                stored_action = dql_agent.last_action
                stored_reward = reward[dql_agent_index]
                stored_next_state = new_observation

                dql_agent.store_transition(stored_current_state, stored_action, \
                                            stored_reward, stored_next_state, done)
                
                # agent learns every 4 steps
                if dql_agent.learn_step % 4 == 0:
                    dql_agent.learn()
                dql_agent.learn_step += 1

        elif event == 'GameOver':

            # keep track of average score per round
            round_number = data['Round']
            
            for pair in range(0, len(average_scores_per_round)):

                score = data['players'][pair]['score']
                average_score = score/round_number
                average_scores_per_round[pair].append(-average_score)

        observation = new_observation

        if reward:
            for r in range(0, 4):
                scores[r] -= reward[r]
        if done:
            for i in range(0, len(score_list)):
                score_list[i].append(scores[i])


loss_list = agent_list[dql_agent_index].loss_list
lr_list = agent_list[dql_agent_index].lr_list

loss_plot_range = int(len(loss_list) / 10)
score_plot_range = int(num_episodes / 10)

def plot_loss_episodes():
    
    plottable_loss_list = []
    
    for i in range(1, len(loss_list)):
        if i % loss_plot_range == 0:
            average_loss_range = sum(loss_list[i - loss_plot_range:i])/loss_plot_range
            plottable_loss_list.append(average_loss_range)

    # plotting loss over episodes
    plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0], plottable_loss_list)
    plt.title('Loss over episodes')
    plt.xlabel('Episode number')
    plt.ylabel('Loss')
    plt.show()


def plot_loss_lr():

    plottable_loss_list = []
    plottable_lr_list = []

    # plotting loss over learning rate
    for i in range(1, len(loss_list)):
        if i % loss_plot_range == 0:
            average_loss_range = sum(loss_list[i - loss_plot_range:i])/loss_plot_range
            plottable_loss_list.append(average_loss_range)
            plottable_lr_list.append(lr_list[i])


    plt.plot(lr_list, loss_list)
    plt.title('Loss over learning rate')
    plt.xlabel('Learning rate')
    plt.ylabel('Loss')
    plt.show()


def plot_total_scores(training):

    # plot the results
    plottable_score_list = [[], [], [], []]
    opponent_label = "Greedy Agent " if training else "Random Agent "
    y_label = "Reward" if training else "Score"

    for player in range(0, 4):
        for i in range(1, num_episodes + 1):
            if i % score_plot_range == 0:
                average_score_range = sum(score_list[player][i - score_plot_range:i])/score_plot_range
                plottable_score_list[player].append(average_score_range)

    plt.ylim(-100, 0)
    plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
             plottable_score_list[dql_agent_index], label="DQL Agent")

    for i in range(1, len(plottable_score_list)):
        plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
                 plottable_score_list[i], label=opponent_label + str(i))

    plt.title('Scores over episodes')
    plt.xlabel('Episode number')
    plt.ylabel(y_label)
    plt.legend(loc="upper right")

    plt.show()


def plot_round_scores(training):

    # plot the results
    plottable_score_list = [[], [], [], []]
    opponent_label = "Greedy Agent " if training else "Random Agent "
    y_label = "Reward" if training else "Score"

    for player in range(0, 4):
        for i in range(1, num_episodes + 1):
            if i % score_plot_range == 0:
                average_score_range =\
                    sum(average_scores_per_round[player][i - score_plot_range:i])/score_plot_range
                plottable_score_list[player].append(average_score_range)

    plt.ylim(-15, 0)
    plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
             plottable_score_list[dql_agent_index], label="DQL Agent")

    for i in range(1, len(plottable_score_list)):
        plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
                 plottable_score_list[i], label=opponent_label + str(i))

    plt.title('Average round scores over episodes')
    plt.xlabel('Episode number')
    plt.ylabel(y_label)
    plt.legend(loc="upper right")

    plt.show()

time_taken = time.time() - start_time

plot_total_scores(training)
plot_round_scores(training)

print("The program took %s seconds to %s %s episodes" % \
    (time_taken, "run" if training else "test", num_episodes))
