import gym

from stable_baselines.common.policies import MlpPolicy, FeedForwardPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.schedules import LinearSchedule

class CustomMlpPolicy(FeedForwardPolicy):
    # see here for a description of how the net_arch param should be used.
    # https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/policies.py#L32-L48
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **_kwargs):
        super(CustomMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                        feature_extraction="mlp", net_arch=[128, 128], **_kwargs)

RANDOM = 2
O = 0
X = 1

# Since opponent_model wasn't set, this environment uses a random
# opponent.

agent_piece = 1 # for X
past_models = []

# startng environment, will son change
random_env = gym.make('custom_gyms:tictac4-v0')
check_env(random_env)
env = random_env

# batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
model = PPO2(CustomMlpPolicy, random_env, verbose=False, learning_rate=LinearSchedule(100000, final_p=.0000025, initial_p=.0005).value, nminibatches=4)





for i in range(50):
    # If we have a trained model, pass it into env
    if len(past_models) > 0:
        env = gym.make('custom_gyms:tictac4-v0', opponent_models=past_models, bias_toward_recent=True, agent_piece=RANDOM)
        check_env(env)


    # we're just copying what's going on here:
    #  - https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/base_class.py#L78-L84
    model.set_env(DummyVecEnv([lambda: env])) # default is 2.5e-4
    model.learn(total_timesteps=10000) # only prints every 128 timesteps

    print(f'round {i}')

    # Evaluate against random_env to see how it plays against a random opponent
    mean_reward, std_reward = evaluate_policy(model, random_env, n_eval_episodes=1000)
    print(f'random opponent: mean reward: {mean_reward}, std reward {std_reward}')

    # Evaluate against env to see how it plays against the current opponent
    if len(past_models) > 0:
        mean_reward, std_reward = evaluate_policy(past_models[-1], env, n_eval_episodes=1000)
        print(f'last opponent: mean reward: {mean_reward}, std reward {std_reward}')

    # past_models = [model]
    past_models.append(model)


# NOW WE PLAY SOME SAMPLE GAMES:
# the latest model plays itself

# agent piece is X, opponent piece is O
test_env = gym.make('custom_gyms:tictac4-v0', opponent_models=[past_models[-1]], agent_piece=X)
check_env(test_env)

for n in range(15):
    print("")
    print(f'GAME {n}:')
    obs = test_env.reset()
    for i in range(1000):
        print(f'step {i}:')
        # use 2 ago, since better for O
        action, _ = past_models[-1].predict(obs)
        obs, reward, done, info = test_env.step(action)

        agent_piece_name = "X"
        opponent_piece_name = "O"
        if agent_piece == O:
            agent_piece_name = "O"
            opponent_piece_name = "X"

        test_env.render()

        if info.get("IllegalMove", False):
            print(f"({agent_piece_name} made an illegal move)")
        if info.get("OpponentIllegalMove", False):
            print(f"({opponent_piece_name} made an illegal move)")

        if done:
            break
