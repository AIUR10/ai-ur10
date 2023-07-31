from stable_baselines3.common.callbacks import CheckpointCallback


class TensorboardCallback(CheckpointCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """
    def __init__(self, env, save_freq: int, save_path: str, name_prefix: str = "rl_model", save_replay_buffer: bool = False, save_vecnormalize: bool = False, verbose: int = 0):
        super().__init__(save_freq, save_path, name_prefix, save_replay_buffer, save_vecnormalize, verbose)
        self.env = env

    def _on_step(self) -> bool:
        super()._on_step()
        # Log scalar values
        self.logger.record("distance", self.env.distance)
        self.logger.record("orientation_penalty", self.env.orientation_penalty)
        self.logger.record("orientation_coef", self.env.orientation_coef)
        self.logger.record("velocity penalty", self.env.velocity_penalty)
        self.logger.record("bonus_reward_distance", self.env.current_bonus_reward_distance)
        self.logger.record("bonus_reward_orientation", self.env.current_bonus_reward_orientation)
        self.logger.record("bonus_reward_distance_orientation", self.env.current_bonus_reward_distance_orientation)
        self.logger.record("count_down", self.env.count_down)
        return True