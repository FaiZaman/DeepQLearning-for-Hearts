This project applies Deep Q-Learning (DQL) to the card game Hearts

# Setup & Running

 Clone the repository into a local folder. Run the program by navigating to this root folder in the command prompt and typing `python main.py`. Choose whether you would like to `train` or `test` the model at the main menu.

# Training

 On the `Training` screen, choose the directory in which to save the model during training. The model is saved automatically to this directory every 100 episodes. 
 Adjust the hyperparameters to any values desired. The default values are the optimal ones.
 
 NOTE - train for a minimum of 10 episodes. 

# Testing
 
 On the `Testing` screen, choose the model file to load in for testing, and select the number of episodes to be tested for. Choose any selection of opponents to play against the DQL agent using the dropdown menus.

 NOTE - test for a minimum of 10 episodes.

# The Project

The aim of this project was to apply a Deep Q-Learning algorithm to a game that is difficult for it to learn purposefully, i.e. a multi-agent imperfect information game. Scores are plotted at the end of the iteration.
