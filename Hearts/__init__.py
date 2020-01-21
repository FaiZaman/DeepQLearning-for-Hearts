from .Hearts import *

from gym.envs.registration import register

register(
    id='Hearts_Card_Game-v0',
    entry_point='Hearts.Hearts:HeartsEnv',
    kwargs={'playersName': ['Aqua', 'Boris', 'Calum', 'Diego'], 'maxScore': 100}
)