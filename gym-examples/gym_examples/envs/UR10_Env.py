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

DONE_DISTANCE = 0.01
VELOCITY_COEF = 0.01
DONE_ORIENTATION = 0.05

class UR10Env(gym.Env):

    def __init__(self, headless=True, responsive_ui=False, max_steps=1000, 
                 orientation_coef=1000, 
                 bonus_reward_distance=100, 
                 bonus_reward_orientation=10, 
                 bonus_reward_distance_orientation=1000):
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
        self.max_steps = max_steps # number of steps of the path ie number of targets on the path
        # count down from the maximum number of steps for the whole scene
        self.count_down = self.max_steps
        # observation space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(18,), dtype=np.float32)
        # action space
        self.action_space = spaces.Box(low=-0.025, high=0.025, shape=(6,), dtype=np.float32)
        # Coefs and bonuses vary during the learning
        self.orientation_coef = orientation_coef 
        self.bonus_reward_distance = bonus_reward_distance
        self.bonus_reward_orientation = bonus_reward_orientation
        self.bonus_reward_distance_orientation = bonus_reward_distance_orientation
        self.current_bonus_reward_distance = 0
        self.current_bonus_reward_orientation = 0
        self.current_bonus_reward_distance_orientation = 0
        self.current_orientation_coef = 1 
        # reward factors
        # change after a step
        self.distance = 0
        self.velocity_penalty = 0
        self.orientation_penalty = 0
        print(f"Simulation time step: {self.pr.get_simulation_timestep()} seconds")
        
    def get_obs(self):
        # Return state containing arm joint angles/velocities & target position
        obs = np.concatenate([self.agent.get_joint_positions(),
                            self.agent.get_joint_velocities(), 
                            self.target.get_position() - self.agent_ee_tip.get_position(),
                            self.path.get_position(relative_to=self.agent_ee_tip),])
        #print(f"OBSERVATION : {obs}")
        return obs

    def reset(self):
        #print("RESET")
        self.agent.set_joint_positions(self.initial_joint_positions, disable_dynamics=True)
        # Reset the first position to reach
        path_position = self.path.get_pose_on_path(0)[0]
        path_orientation = self.path.get_pose_on_path(0)[1]
        self.target.set_position(path_position)
        self.target.set_orientation(path_orientation)
        self.target.set_orientation([np.pi/2, 0, 0], relative_to=self.target) # after observation, I found this is the correct orientation
        # Reset count down
        self.count_down = self.max_steps
        # Reset bonuses and coefs
        self.current_bonus_reward_distance = 0
        self.current_bonus_reward_orientation = 0
        self.current_bonus_reward_distance_orientation = 0
        self.current_orientation_coef = 1 
        return self.get_obs()

    def step(self, action):
        # Get the next position on the path 
        path_position = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[0]
        path_orientation = self.path.get_pose_on_path(1-self.count_down/self.max_steps)[1]

        # set the target 
        self.target.set_position(path_position)
        self.target.set_orientation(path_orientation)
        # Adjust orientation to get the one desired for the tip
        self.target.set_orientation([np.pi/2, 0, 0], relative_to=self.target) # after observation, I found this is the correct orientation
        target_position = self.target.get_position()
        #print(f"TARGET POSITION {target_position}")

        # Act to reach position
        self.agent.set_joint_target_velocities(action)  # Apply action, which contains velocities
        self.pr.step()  # Step the physics simulation forward

        # Distance
        # Calculate distance to the target
        ee_position = self.agent_ee_tip.get_position()  # Get the final position of the end effector
        self.distance = np.linalg.norm(np.array(target_position) - np.array(ee_position))
        # Reward proximity to the target
        reward = -self.distance
        #print(f"DISTANCE REWARD : {distance}")

        # Velocity
        # Penalize high velocities
        self.velocity_penalty = np.sum(np.abs(action)) * VELOCITY_COEF 
        reward -= self.velocity_penalty
        #print(f"VELOCITY PENALTY : {velocity_penalty}")


        # Orientation
        path_center = self.path.get_position(relative_to=self.agent_ee_tip) # path center position relative to the tip
        # Penalize incorrect orientation
        self.orientation_penalty = np.square(path_center[0]) + np.square(path_center[1])
        if path_center[2] <= 0:
            self.orientation_penalty += np.square(path_center[2])
        self.orientation_penalty = np.sqrt(self.orientation_penalty)
        #print(f"ORIENTATION PENALTY : {orientation_penalty}") 
        reward -= self.orientation_penalty * self.current_orientation_coef

        # Reward seperatly the distance and the orientation
        if self.distance < DONE_DISTANCE:
            self.current_bonus_reward_distance = self.bonus_reward_distance
            self.current_orientation_coef = self.orientation_coef
            #print(f"BONUS DISTANCE : {self.current_bonus_reward_distance}")
        else:
            self.current_bonus_reward_distance = 0

        if self.orientation_penalty < DONE_ORIENTATION:
            self.current_bonus_reward_orientation = self.bonus_reward_orientation
            self.current_orientation_coef = 1
            #print(f"BONUS ORIENTATION : {self.current_bonus_reward_orientation}")
        else:
            self.current_bonus_reward_orientation = 0

        # Update the count down when distance and orientation are achieved
        if self.distance < DONE_DISTANCE and self.orientation_penalty < DONE_ORIENTATION:
            self.current_bonus_reward_distance_orientation = self.bonus_reward_distance_orientation
            self.current_orientation_coef = 1
            self.count_down -= 1
            #print(f"BONUS DISTANCE ORIENTATION : {self.current_bonus_reward_distance_orientation}")
        else:
            self.current_bonus_reward_distance_orientation = 0

        reward += self.current_bonus_reward_distance + self.current_bonus_reward_orientation + self.current_bonus_reward_distance_orientation
            
        # Check if the episode is done
        done = self.count_down == 0
        return self.get_obs(), reward, done, {}
        
    def shutdown(self):
        self.pr.stop()
        self.pr.shutdown()
        