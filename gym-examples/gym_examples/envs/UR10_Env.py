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


#SCENE_FILE = join(os.getcwd(), 'scene_with_ur10.ttt')
SCENE_FILE = join(os.getcwd(), 'test_scene_robots_ur10.ttt')
EPISODES = 2
EPISODE_LENGTH = 3

class UR10Env(gym.Env):

    def __init__(self):
        super(UR10Env, self).__init__()
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=False) # headless=True not to display the CoppeliaSim interface
        self.pr.start()
        self.agent = UR10()
        self.agent.set_control_loop_enabled(False)
        self.agent.set_motor_locked_at_zero_velocity(True)
        #print(self._get_state())
        #print(f"Simulation time step: {self.pr.get_simulation_timestep()} seconds")
        self.agent_ee_tip = self.agent.get_tip()
        self.initial_joint_positions = self.agent.get_joint_positions()
        self.total_distance_moved = 0  # Add a counter for total distance moved
        
    def _get_state(self):
        # Return state containing arm joint angles/velocities & target position
        return np.concatenate([self.agent.get_joint_positions(),
                            self.agent.get_joint_velocities()])
        
    def reset(self):
        self.agent.set_joint_positions(self.initial_joint_positions)
        return self._get_state()

    def step(self, action):
        initial_position = self.agent_ee_tip.get_position()  # Get the initial position of the end effector
        velocities = [10, 10, 10, 10, 10, 10]  # Adjust these velocities until the arm moves in the desired direction
        self.agent.set_joint_target_velocities(velocities)  # Apply velocities
        self.pr.step()  # Step the physics simulation forward
        final_position = self.agent_ee_tip.get_position()  # Get the final position of the end effector

        # Calculate distance moved and add to total
        distance_moved = np.linalg.norm(np.array(final_position) - np.array(initial_position))
        self.total_distance_moved += distance_moved

        # Check if the arm has moved the required distance
        done = self.total_distance_moved >= 0.5  # Check if arm has moved 50 cm
        reward = distance_moved

        return self._get_state(), reward, done, {}
        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()
        
        
        
        
        
        
        
        
        
        
    

