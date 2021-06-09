import gym

from stable_baselines.common.policies import MlpPolicy, FeedForwardPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env

class CustomMlpPolicy(FeedForwardPolicy):
    """
    Policy object that implements actor critic, using a MLP (2 layers of 64)

    :param sess: (TensorFlow session) The current TensorFlow session
    :param ob_space: (Gym Space) The observation space of the environment
    :param ac_space: (Gym Space) The action space of the environment
    :param n_env: (int) The number of environments to run
    :param n_steps: (int) The number of steps to run for each environment
    :param n_batch: (int) The number of batch to run (n_envs * n_steps)
    :param reuse: (bool) If the policy is reusable or not
    :param _kwargs: (dict) Extra keyword arguments for the nature CNN feature extraction
    """

    # see here for a description of how the net_arch param should be used.
    # https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/policies.py#L32-L48
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **_kwargs):
        super(CustomMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                        feature_extraction="mlp", net_arch=[256, 256], **_kwargs)


# Since opponent_model wasn't set, this environment uses a random
# opponent.

agent_piece = 1 # for X
past_models = []

# startng environment, will son change
random_env = gym.make('custom_gyms:tictac4-v0')
check_env(random_env)
env = random_env

# batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
model = PPO2(CustomMlpPolicy, random_env, verbose=False, learning_rate=0.00025, nminibatches=4)



for i in range(50):
    # If we have a trained model, pass it into env
    if len(past_models) > 0:
        agent_piece = not agent_piece

        env = gym.make('custom_gyms:tictac4-v0', opponent_models=past_models, bias_toward_recent=True, agent_piece=agent_piece)
        check_env(env)


    # we're just copying what's going on here:
    #  - https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/base_class.py#L78-L84
    model.set_env(DummyVecEnv([lambda: env])) # default is 2.5e-4
    model.learn(total_timesteps=10000) # only prints every 128 timesteps

    print(f'round {i} -- agent is {agent_piece}')

    # Evaluate against random_env to see how it plays against a random opponent
    mean_reward, std_reward = evaluate_policy(model, random_env, n_eval_episodes=1000)
    print(f'random opponent: mean reward: {mean_reward}, std reward {std_reward}')

    # Evaluate against env to see how it plays against the current opponent
    if len(past_models) > 0:
        mean_reward, std_reward = evaluate_policy(past_models[-1], env, n_eval_episodes=1000)
        print(f'last opponent: mean reward: {mean_reward}, std reward {std_reward}')

    # past_models = [model]
    past_models.append(model)

for n in range(15):
    print(f'GAME {n}:')
    obs = env.reset()
    for i in range(1000):
        print(f'on step {i}:')
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)

        if info.get("IllegalMove", False):
            print("Agent made an illigal move, spanking...")
            break
        if info.get("OpponentIllegalMove", False):
            print("Opponent made an illigal move")
            break

        env.render()

        if done:
            break
