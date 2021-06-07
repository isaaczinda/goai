import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env

# Since opponent_model wasn't set, this environment uses a random
# opponent.
firstEnv = gym.make('custom_gyms:tictac4-v0')
check_env(firstEnv)

# batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
firstModel = PPO2("MlpPolicy", firstEnv, verbose=False, learning_rate=0.0025, nminibatches=4) # default is 2.5e-4
firstModel.learn(total_timesteps=10000) # only prints every 128 timesteps

mean_reward, std_reward = evaluate_policy(firstModel, firstEnv, n_eval_episodes=1000)
print(f'mean reward: {mean_reward}, std reward {std_reward}')

print("*****meta-training*****")

secondEnv = gym.make('custom_gyms:tictac4-v0', opponent_model=firstModel)
check_env(secondEnv)

# TODO: continue training OG model

# batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
secondModel = PPO2("MlpPolicy", secondEnv, verbose=False, learning_rate=0.0025, nminibatches=4) # default is 2.5e-4
secondModel.learn(total_timesteps=10000) # only prints every 128 timesteps

# Evaluate model against random opponent
mean_reward, std_reward = evaluate_policy(secondModel, firstEnv, n_eval_episodes=1000)
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
