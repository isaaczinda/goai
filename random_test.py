import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env

import numpy as np

from gym import spaces

# Since opponent_model wasn't set, this environment uses a random
# opponent.
random_env = gym.make('custom_gyms:tictac4-v0')
check_env(random_env)

# set n_cpu_tf_sess so that this will just run on 1 thread. We need this for determinism. 
model = PPO2("MlpPolicy", random_env, verbose=False, learning_rate=0.0025, nminibatches=4, n_cpu_tf_sess=1, seed=1)

mean_reward, std_reward = evaluate_policy(model, random_env, n_eval_episodes=2, deterministic=True, render=True)
print(f'random opponent: mean reward: {mean_reward}, std reward {std_reward}')
