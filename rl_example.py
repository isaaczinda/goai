import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env

# Since opponent_model wasn't set, this environment uses a random
# opponent.
env = gym.make('custom_gyms:tictac4-v0')

print("CHECKING ENV")
check_env(env)
print("CHECKED, MF")

# Optional: PPO2 requires a vectorized environment to run
# the env is now wrapped automatically when passing it to the constructor
# env = DummyVecEnv([lambda: env])

# what we've tried:
#  - CnnLstmPolicy
#  - CnnPolicy
#  - MlpPolicy
#


# nminibatches


# batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
model = PPO2("MlpPolicy", env, verbose=False, learning_rate=0.0025, nminibatches=4) # default is 2.5e-4
model.learn(total_timesteps=100000) # only prints every 128 timesteps

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=1000)
print(f'mean reward: {mean_reward}, std reward {std_reward}')

#
# for n in range(5):
#     print(f'GAME {n}:')
#     obs = env.reset()
#     for i in range(1000):
#         print(f'on step {i}:')
#         action, _states = model.predict(obs)
#         obs, reward, done, info = env.step(action)
#
#         if info.get("IllegalMove", False):
#             print("Agent made an illigal move, spanking...")
#             break
#         else:
#             env.render()
#
#         if done:
#             break



env.close()
