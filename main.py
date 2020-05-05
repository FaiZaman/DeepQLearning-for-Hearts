import sys
import gym
import time
import torch as T
import PySimpleGUI as gui
from matplotlib import pyplot as plt

from Hearts import *
from Agents.humanAgent import HumanAgent
from Agents.randomAgent import RandomAgent
from Agents.greedyAgent import GreedyAgent
from Agents.DQLAgent import DQLAgent

# hyperparameters
num_episodes = 2500
gamma = 0.99
epsilon = 1
learning_rate = 0.0001
batch_size = 32
tau = 10000
learn_step = 4

# change this to the directory you want to save and load your own models
save_path = "C:/Users/faizz/University Work/Year 3/Individual Project TH86/Model"
load_path = "C:/Users/faizz/University Work/Year 3/Individual Project TH86/Model/model_2400.pth"

agent_list = [0, 0, 0, 0]
n_actions = 52
playersNameList = ['Arthur', 'Boris', 'Calum', 'Diego']
dql_agent_choice_list = ['DQL Agent', 'Human Player', 'Greedy Agent', 'Random Agent']
agent_choice_list = ['Human Player', 'Greedy Agent', 'Random Agent']

training = None
selecting = True

selecting_layout = [
    [gui.Text('Deep Q-Learning for Hearts', font=('Helvetica', 16), justification='center')],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Text('Please select whether you would like to train or test the model.')],
    [gui.Button('Train'), gui.Button('Test'), gui.Cancel()]
]

training_layout = [
    [gui.Text('Training', font=('Helvetica', 16))],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Text('Saving the Model', font=('Helvetica', 12))],
    [gui.Text('Save Model Directory for Training: ')],
    [gui.InputText('Save Folder', disabled=True), gui.FolderBrowse()],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Text('Hyperparameters', font=('Helvetica', 12))],
    [gui.Text('Episodes', size=(7, 1)), gui.In(default_text=num_episodes, size=(10, 1)),
     gui.Text('   '), gui.Text('Learning Rate', size=(10, 1)), 
     gui.In(default_text=learning_rate, size=(10, 1))],
    [gui.Text('Gamma', size=(7, 1)), gui.In(default_text=gamma, size=(10, 1)), 
     gui.Text('   '), gui.Text('Batch Size', size=(10, 1)),
     gui.In(default_text=batch_size, size=(10, 1))],
    [gui.Text('C', size=(7, 1)), gui.In(default_text=tau, size=(10, 1)),
     gui.Text('   '), gui.Text('Learn Step', size=(10, 1)),
     gui.In(default_text=learn_step, size=(10, 1))],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Button('Run'), gui.Button('Back to Main Menu')]
]

testing_layout = [  
    [gui.Text('Testing', font=('Helvetica', 15), justification='left')],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Text('Episode Number & Model Loading', font=('Helvetica', 12))],
    [gui.Text('Episodes', size=(7, 1)), gui.In(default_text=num_episodes, size=(10, 1))],
    [gui.Text('Load Model for Testing: ')],
    [gui.InputText('Model File', disabled=True), gui.FileBrowse()],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Text('Agent Selection', font=('Helvetica', 12))],
    [gui.Text('Agent 1', size=(7,1)), gui.Combo(["DQL Agent"], size=(13, 1)),
     gui.Text('   '), gui.Text('Agent 3', size=(7,1)), gui.Combo(agent_choice_list, size=(13, 1))],
    [gui.Text('Agent 2', size=(7,1)), gui.Combo(agent_choice_list, size=(13, 1)),
     gui.Text('   '), gui.Text('Agent 4', size=(7,1)), gui.Combo(agent_choice_list, size=(13, 1))],
    [gui.Text('_'  * 100, size=(65, 1))],
    [gui.Button('Run'), gui.Button('Back to Main Menu')]
]

while selecting:

    window = gui.Window('Deep Q-Learning for Hearts', selecting_layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):	# if user closes window
            sys.exit()
            break;
        if event == 'Train':
            training = True
            break;
        if event == 'Test':
            training = False
            break;

    window.close()

    if training:

        window = gui.Window('Deep Q-Learning for Hearts - Training', training_layout)

        while True:

            event, values = window.read()

            if event is None:	# if user closes window
                sys.exit()
                break;

            if event == 'Run':

                test_path, num_episodes, learning_rate, gamma, batch_size, tau, learn_step =\
                    values[0], int(values[1]), float(values[2]), float(values[3]),\
                        int(values[4]), int(values[5]), int(values[6])
                if test_path != 'Save Folder':
                    save_path = test_path
                selecting = False
                break;

            if event == 'Back to Main Menu':
                break;

        window.close()

    else:

        window = gui.Window('Deep Q-Learning for Hearts - Testing', testing_layout)

        while True:
            event, values = window.read()

            if event is None:	# if user closes window or clicks cancel
                sys.exit()
                break;

            if event == 'Run':

                num_episodes, test_path, agent_1, agent_2, agent_3, agent_4 =\
                    int(values[0]), values[1], values[2], values[3], values[4], values[5]
                agent_test_list = [agent_1, agent_2, agent_3, agent_4]
                if test_path != "Model File":
                    load_path = test_path
                selecting = False
                break;

            if event == 'Back to Main Menu':
                break;

        window.close()


# DQL Agent Training
if training:

    agent_list[0] = DQLAgent(gamma, epsilon, learning_rate, batch_size, n_actions, tau, training)
    agent_list[1] = GreedyAgent(playersNameList[1])
    agent_list[2] = GreedyAgent(playersNameList[2])
    agent_list[3] = GreedyAgent(playersNameList[3])

else:

    for agent_index in range(0, len(agent_list)):
        if agent_test_list[agent_index] == "DQL Agent":
            agent_list[agent_index] =\
                DQLAgent(gamma, epsilon, learning_rate, batch_size, n_actions, tau, training)
        elif agent_test_list[agent_index] == "Human Player":
            agent_list[agent_index] = HumanAgent()
        elif agent_test_list[agent_index] == "Greedy Agent":
            agent_list[agent_index] = GreedyAgent(playersNameList[agent_index])
        elif agent_test_list[agent_index] == "Random Agent":
            agent_list[agent_index] = RandomAgent(playersNameList[agent_index])

dql_agent_index = 0
for index in range(0, len(agent_list)):
    if isinstance(agent_list[index], DQLAgent):
        dql_agent_index = index

max_score = 100
score_list = [[], [], [], []]
average_scores_per_round = [[], [], [], []]


# saving and loading the models
def save_model(model, save_path, episode_number):

    save_path = save_path + "/model_" + str(episode_number) + ".pth"
    T.save(model.state_dict(), save_path)


def load_model(model):

    model.load_state_dict(T.load(load_path))
    return model

env = gym.make('Hearts_Card_Game-v0')
env.__init__([agent.name for agent in agent_list], max_score)

if not training:
    model = load_model(agent_list[dql_agent_index].Q_network)

start_time = time.time()

for episode_number in range(num_episodes + 1):

    observation = env.reset()   # return initial observation
    done = False
    scores = [0, 0, 0, 0]

    if training:
        if episode_number % 10 == 0:
            print("Training Episode Number:", episode_number)
            model = agent_list[dql_agent_index].Q_network
            save_model(model, save_path, episode_number)
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

            if event == 'PlayTrick' and data['playerName'] == "DQLAgent":
                
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
                
                # agent learns every learn_step steps
                if dql_agent.learn_step % learn_step == 0:
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


def plot_total_scores(agent_list):

    # plot the results
    plottable_score_list = [[], [], [], []]

    for player in range(0, 4):
        for i in range(1, num_episodes + 1):
            if i % score_plot_range == 0:
                average_score_range = sum(score_list[player][i - score_plot_range:i])/score_plot_range
                plottable_score_list[player].append(average_score_range)

    plt.ylim(-126, 0)
    plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
             plottable_score_list[dql_agent_index], label="DQL Agent")
    
    del plottable_score_list[dql_agent_index]
    del agent_list[dql_agent_index]

    for opponent_index in range(0, len(plottable_score_list)):
        
        opponent_label = agent_list[opponent_index].agent_type
        plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
                 plottable_score_list[opponent_index], label=opponent_label)

    #plt.title('Scores over episodes')
    plt.xlabel('Episode number')
    plt.ylabel('Score')
    plt.legend(loc="upper right")

    plt.show()


def plot_round_scores(agent_list):

    # plot the results
    plottable_score_list = [[], [], [], []]

    for player in range(0, 4):
        for i in range(1, num_episodes + 1):
            if i % score_plot_range == 0:
                average_score_range =\
                    sum(average_scores_per_round[player][i - score_plot_range:i])/score_plot_range
                plottable_score_list[player].append(average_score_range)

    plt.ylim(-26, 0)
    plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
             plottable_score_list[dql_agent_index], label="DQL Agent")

    del plottable_score_list[dql_agent_index]
    del agent_list[dql_agent_index]

    for opponent_index in range(0, len(plottable_score_list)):
        
        opponent_label = agent_list[opponent_index].agent_type
        plt.plot([x for x in range(1, num_episodes + 1) if x % score_plot_range == 0],\
                 plottable_score_list[opponent_index], label=opponent_label)

    #plt.title('Average round scores over episodes')
    plt.xlabel('Episode number')
    plt.ylabel('Score')
    plt.legend(loc="upper right")

    plt.show()


def calculate_average_score(agents_score_list):

    dql_agent_score_list = agents_score_list[dql_agent_index]
    average_score = sum(dql_agent_score_list)/len(dql_agent_score_list)

    return average_score


time_taken = time.time() - start_time

plot_total_scores(agent_list.copy())
plot_round_scores(agent_list)

average_episode_score = calculate_average_score(score_list)
average_round_score = calculate_average_score(average_scores_per_round)

print("The program took %s seconds to %s %s episodes" % \
    (time_taken, "run" if training else "test", num_episodes))
print("The average episode score of the DQL agent was %f" % average_episode_score)
print("The average round score of the DQL agent was %f" % average_round_score)
