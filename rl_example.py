import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy

# Since opponent_model wasn't set, this environment uses a random
# opponent.
env = gym.make('custom_gyms:tictac4-v0')

# Optional: PPO2 requires a vectorized environment to run
# the env is now wrapped automatically when passing it to the constructor
# env = DummyVecEnv([lambda: env])

model = PPO2("MlpPolicy", env, verbose=True) # default is 2.5e-4
model.learn(total_timesteps=1000000)

mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f'mean reward: {mean_reward}, std reward {std_reward}')


for n in range(15):
    print(f'GAME {n}:')
    obs = env.reset()
    for i in range(1000):
        print(f'on step {i}:')
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)

        if info.get("IllegalMove", False):
            print("Agent made an illigal move, retrying...")
        else:
            env.render()

        if done:
            break



env.close()
