from gym.envs.registration import register

register(
    id="gym_examples/UR10-v0",
    entry_point="gym_examples.envs:UR10Env",
)
