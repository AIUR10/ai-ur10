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

SCENE_FILE = join(os.getcwd(), 'scene_robots_ur10_circular_easystart.ttt')
EPISODES = 2
EPISODE_LENGTH = 3
DISTANCE_BONUS = 1 # 10
BONUS_THRESHOLD = 0.05
BONUS_REWARD = 10
VELOCITY_PENALTY = 0.01
ORIENTATION_PENALTY = 10 #1000 #0.01

DONE_DISTANCE = 0.025
DONE_ORIENTATION = 0.1 # quite arbitrary for now

class UR10Env(gym.Env):

    def __init__(self, headless=True, responsive_ui=False, max_steps=1000):#, nb_steps_first_position=100):
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
        # number of steps to reach the first position
        #self.nb_steps_first_position = nb_steps_first_position
        self.max_steps = max_steps # beware it does not include reaching the first position
        # count down from the maximum number of steps for the whole scene
        self.count_down = self.max_steps #+ self.nb_steps_first_position

        # observation space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(18,), dtype=np.float32)
        # action space
        self.action_space = spaces.Box(low=-0.05, high=0.05, shape=(6,), dtype=np.float32)

        #print(f"Simulation time step: {self.pr.get_simulation_timestep()} seconds")
        
    def get_obs(self):
        # Return state containing arm joint angles/velocities & target position
        obs = np.concatenate([self.agent.get_joint_positions(),
                            self.agent.get_joint_velocities(), 
                            self.target.get_position() - self.agent_ee_tip.get_position(),
                            self.agent_ee_tip.get_orientation(relative_to=self.target)])
        #print(obs)
        return obs

    def reset(self):
        print("RESET")
        self.agent.set_joint_positions(self.initial_joint_positions, disable_dynamics=True)
        # Reset the first position to reach
        path_position = self.path.get_pose_on_path(0)[0]
        path_orientation = self.path.get_pose_on_path(0)[1]
        self.target.set_position(path_position)
        self.target.set_orientation(path_orientation)
        self.target.set_orientation([np.pi/2, 0, 0], relative_to=self.target) # after observation, I found this is the correct orientation
        # Reset count down
        self.count_down = self.max_steps #+ self.nb_steps_first_position
        return self.get_obs()

    def step(self, action):
        '''
        if self.count_down > self.max_steps:
            # Reach first position within predefined number of steps
            path_position = self.path.get_pose_on_path(0)[0]    
            path_orientation = self.path.get_pose_on_path(0)[1]
        else:
            # Reach the following positions 
            path_position = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[0] # Get the next position on the path 
            path_orientation = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[1]
        '''

        # Reach position
        path_position = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[0] # Get the next position on the path 
        path_orientation = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[1]

        # set the target 
        self.target.set_position(path_position)
        self.target.set_orientation(path_orientation)
        # Adjust orientation to get the one desired for the tip
        self.target.set_orientation([np.pi/2, 0, 0], relative_to=self.target) # after observation, I found this is the correct orientation
        target_position = self.target.get_position()
        #print(f"Target position {target_position}")

        # Act
        self.agent.set_joint_target_velocities(action)  # Apply action, which contains velocities
        self.pr.step()  # Step the physics simulation forward
        ee_position = self.agent_ee_tip.get_position()  # Get the final position of the end effector

        # Calculate distance to the target
        distance = np.linalg.norm(np.array(target_position) - np.array(ee_position))

        # Check if the arm has moved the required distance
        reward = DISTANCE_BONUS*(1/distance)
        #if distance < BONUS_THRESHOLD:  # Add a bonus for reaching the target
        #    reward += BONUS_REWARD
        # Penalize incorrect orientation
        # Should match target orientation
        orientation = (1/distance)*np.linalg.norm(self.agent_ee_tip.get_orientation(relative_to=self.target))
        #print(f"Tip orientation relatively to target {orientation}")
        reward -= orientation #* ORIENTATION_PENALTY # As for now it looks at the center of the circular motion
        # Penalize high velocities
        reward -= np.linalg.norm(action) * VELOCITY_PENALTY 

        # Update the count down
        if distance < DONE_DISTANCE and orientation < DONE_ORIENTATION:
            self.count_down -= 1
            print("TARGET REACHED")

        # Check if the episode is done
        done = self.count_down == 0
        return self.get_obs(), reward, done, {}
        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()
        