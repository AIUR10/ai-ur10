"""
RL environment with PyRep for the UR10 arm.
In this case, the arm must do a circle around a virtual space in front of it.
This script contains :
    - RL environment.
    - Scene manipulation.
    - Environment resets.
    - Setting joint properties (control loop disabled, motor locked at 0 vel)
"""

import gym
import os
import numpy as np
from os.path import join
from pyrep import PyRep
from pyrep.robots.arms.ur10 import UR10

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


SCENE_FILE = join(os.getcwd(), 'scene_with_ur10.ttt')
EPISODES = 2
EPISODE_LENGTH = 3

class UR10Env(gym.Env):

    def __init__(self):
        super(UR10Env, self).__init__()
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=False) # headless=True introduces error in notebook
        self.pr.start()
        self.agent = UR10()
        print(self._get_state())
        
    def _get_state(self):
        # Return state containing arm joint angles/velocities & target position
        return np.concatenate([self.agent.get_joint_positions(),
                            self.agent.get_joint_velocities()])
        
    def reset(self):
        return self._get_state()

    def step(self, action):
        reward = 0
        return reward, self._get_state()
        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()
        
        
        
        
        
        
        
        
        
        
    

