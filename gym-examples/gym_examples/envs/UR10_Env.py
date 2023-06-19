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
from gym import spaces
import os
import numpy as np
from os.path import join
from pyrep import PyRep
from pyrep.robots.arms.ur10 import UR10
from pyrep.objects.dummy import Dummy 
from pyrep.objects.cartesian_path import CartesianPath

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


#SCENE_FILE = join(os.getcwd(), 'scene_with_ur10.ttt')
SCENE_FILE = join(os.getcwd(), 'test_scene_robots_ur10_copy.ttt')
EPISODES = 2
EPISODE_LENGTH = 3
BONUS_THRESHOLD = 0.1
BONUS_REWARD = 100
VELOCITY_PENALTY = 0.01

class UR10Env(gym.Env):

    def __init__(self, headless=True, responsive_ui=False, max_steps=100):
        super(UR10Env, self).__init__()
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=headless, responsive_ui=responsive_ui) # headless=True not to display the CoppeliaSim interface
        self.pr.start()
        self.agent = UR10()
        self.agent.set_control_loop_enabled(False)
        self.agent.set_motor_locked_at_zero_velocity(True)
        self.target = Dummy('UR10_target')
        self.path = CartesianPath('CircularPath')
        self.agent_ee_tip = self.agent.get_tip()
        self.initial_joint_positions = self.agent.get_joint_positions()
        # count down from the maximum number of steps
        self.max_steps = max_steps 
        self.count_down = self.max_steps

        # observation space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(15,), dtype=np.float32)
        # action space
        self.action_space = spaces.Box(low=-10, high=10, shape=(6,), dtype=np.float32)

        #print(f"Simulation time step: {self.pr.get_simulation_timestep()} seconds")
        
    def get_obs(self):
        # Return state containing arm joint angles/velocities & target position
        return np.concatenate([self.agent.get_joint_positions(),
                            self.agent.get_joint_velocities(), 
                            self.target.get_position() - self.agent_ee_tip.get_position()])

    def reset(self):
        self.agent.set_joint_positions(self.initial_joint_positions, disable_dynamics=True)
        # Reset count down
        self.count_down = self.max_steps
        return self.get_obs()

    def step(self, action):
        path_position = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[0] # Get the next position on the path 
        # set the target 
        self.target.set_position(path_position)
        target_position = self.target.get_position()

        self.agent.set_joint_target_velocities(action)  # Apply action, which contains velocities
        self.pr.step()  # Step the physics simulation forward
        ee_position = self.agent_ee_tip.get_position()  # Get the final position of the end effector

        # Calculate distance to the target
        distance = np.linalg.norm(np.array(target_position) - np.array(ee_position))

        # Check if the arm has moved the required distance
        reward = np.exp(-distance)
        if distance < BONUS_THRESHOLD:  # Add a bonus for reaching the target
            reward += BONUS_REWARD
        # Penalize high velocities
        reward -= np.sum(np.abs(action)) * VELOCITY_PENALTY 

        # Update the count down
        self.count_down -= 1

        # Check if the episode is done
        done = self.count_down == 0

        return self.get_obs(), reward, done, {}
        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()
        
        
        
        
        
        
        
        
        
        
    

