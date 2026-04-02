import gym
import numpy as np
from acme import wrappers
import monoped_env

class AcmeCompatibilityWrapper(gym.Wrapper):
    def step(self, action):
        return self.env.step(action)
    def reset(self, **kwargs):
        result = self.env.reset(**kwargs)
        return result[0] if isinstance(result, tuple) else result


def make_env(evaluation: bool = False):
    env = monoped_env.MonopedEnv()
    env = AcmeCompatibilityWrapper(env)
    env = wrappers.GymWrapper(env)
    env = wrappers.SinglePrecisionWrapper(env)
    return env

