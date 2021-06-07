import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env

# Since opponent_model wasn't set, this environment uses a random
# opponent.
random_env = gym.make('custom_gyms:tictac4-v0')
check_env(random_env)
model = PPO2("MlpPolicy", random_env, verbose=False, learning_rate=0.0025, nminibatches=4)

for i in range(50):

    # If we have a trained model, pass it into env
    if model:
        env = gym.make('custom_gyms:tictac4-v0', opponent_model=model)
        check_env(env)
    else:
        env = random_env

    # batch_size (number of steps per NN training) = self.n_batch / self.nminibatches

    # we're just copying what's going on here:
    #  - https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/base_class.py#L78-L84
    model.set_env(DummyVecEnv([lambda: env])) # default is 2.5e-4
    model.learn(total_timesteps=2048) # only prints every 128 timesteps

    print(f'round {i}........')

    # Evaluate against random_env to see how it plays against a random opponent
    mean_reward, std_reward = evaluate_policy(model, random_env, n_eval_episodes=1000)
    print(f'random opponent: mean reward: {mean_reward}, std reward {std_reward}')

    # Evaluate against env to see how it plays against the current opponent
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=1000)
    print(f'last opponent: mean reward: {mean_reward}, std reward {std_reward}')




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
