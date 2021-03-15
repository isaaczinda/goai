import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

#
env = gym.make('custom_gyms:tictac4-v0')

print(env)

# Optional: PPO2 requires a vectorized environment to run
# the env is now wrapped automatically when passing it to the constructor
# env = DummyVecEnv([lambda: env])

model = PPO2(MlpPolicy, env, verbose=0)
model.learn(total_timesteps=10000)

obs = env.reset()
for i in range(1000):
    print(f'on step {i}:')
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)

    if done:
        break

    env.render()

env.close()
