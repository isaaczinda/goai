# TODO: fix numpy warnings instead of just suppressing them
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import gym

from stable_baselines.common.policies import MlpPolicy, FeedForwardPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.schedules import LinearSchedule
from stable_baselines.common.callbacks import BaseCallback

from tictac import TicTacEnv, RandomModel

import numpy as np
import time
from os import path

FILE_PATH = path.dirname(path.realpath(__file__))


class CustomMlpPolicy(FeedForwardPolicy):
    # see here for a description of how the net_arch param should be used.
    # https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/policies.py#L32-L48
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **_kwargs):
        super(CustomMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                        feature_extraction="mlp", net_arch=[128, 128], **_kwargs)

lastScores = None
class SaveTrainingScores(BaseCallback):
    def __init__(self, verbose=1):
        super(SaveTrainingScores, self).__init__(verbose)

    def _on_training_end(self):
        global lastScores
        lastScores = []

        numEnvs = len(self.training_env.get_attr('scores'))
        scores = self.training_env.get_attr('scores')

        for i in range(len(scores[0])):
            combinedScore = (0, 0)
            for k in range(numEnvs):
                combinedScore = (combinedScore[0] + scores[k][i][0], combinedScore[1] + scores[k][i][1])
            lastScores.append(combinedScore)

RANDOM = 2
O = 0
X = 1

def makePolicy():
    # startng environment, will son change
    env = TicTacEnv([RandomModel(TicTacEnv.action_space)])
    check_env(env)
    return PPO2(CustomMlpPolicy, env, verbose=False, learning_rate=.0005, nminibatches=4)

def trainPolicy(policy, opponentPolicies, timestamps=5000):
    """ Returns (wins, losses) from the games that we just played. """

    env = TicTacEnv(opponentPolicies, bias_toward_recent=False, agent_piece=RANDOM)
    policy.set_env(DummyVecEnv([lambda: env]))
    policy.learn(total_timesteps=timestamps, callback=SaveTrainingScores()) # only prints every 128 timesteps

    wins = sum([score[0] for score in lastScores])
    losses = sum([score[1] for score in lastScores])

    return (wins, losses)

def evaluateAgainstRandomPolicy(policy):
    """ Returns mean reward, std reward against random agent. """
    random_env = TicTacEnv([RandomModel(TicTacEnv.action_space)])
    return evaluate_policy(policy, random_env, n_eval_episodes=500)


fixed_policies = [RandomModel(TicTacEnv.action_space)]

# the 0th one of these is the lowest active policy
active_policies = [makePolicy(), makePolicy(), makePolicy()]

for i in range(25):
    winFractions = []

    while True:
        print("___training_loop___")

        # train lowest active policy against all fixed policies
        wins, losses = trainPolicy(active_policies[0], fixed_policies)
        winFractions.append(wins / (losses + wins))

        # exit if the win fraction this evaluation improves by less than 1% over
        # the last win fraction.
        if len(winFractions) >= 2:
            print(f'win fraction: previous: {winFractions[-2]}, current: {winFractions[-1]}')

            if abs(winFractions[-1]-winFractions[-2]) < .01:
                break

        # train non-lowest active policies against lowest active policy and fixes policied
        for policy in active_policies:
            trainPolicy(policy, [active_policies[0]] + fixed_policies)

        # print result of all agents vs. random policy
        print("active policies vs random agent: ", end="")
        for policy in active_policies:
            meanReward, _ = evaluateAgainstRandomPolicy(policy)
            print(meanReward, end=", ")
        print("")

    # make the lowest active policy a fixed policy, then add a new random
    # policy
    fixed_policies.append(active_policies[0])
    active_policies = active_policies[1:]
    active_policies.append(makePolicy())
    print(f'THERE ARE NOW {len(fixed_policies)} FIXED POLICIES')

# don't save the 0th model, since this is a random one and won't save.
for i, policy in enumerate(fixed_policies[1:]):
    policy.save(path.join(FILE_PATH, f'models/{i+1}-model'))


#
#
#
#
#     print(f'round {i}')
#
#     # Evaluate against random_env to see how it plays against a random opponent
#     mean_reward, std_reward = evaluate_policy(model, random_env, n_eval_episodes=500)
#     print(f'random opponent: mean reward: {mean_reward}, std reward {std_reward}')
#
#     # Evaluate against env to see how it plays against the current opponent
#     if len(past_models) > 0:
#         mean_reward, std_reward = evaluate_policy(past_models[-1], env, n_eval_episodes=500)
#         print(f'last opponent: mean reward: {mean_reward}, std reward {std_reward}')
#
#     # past_models = [model]
#
#     if len(past_models) < 5:
#         print("adding to the hall of fame")
#
#         past_models.append(model)
#         past_model_scores.append(mean_reward)
#
#     elif mean_reward > min(past_model_scores):
#         print(f'adding to the hall of fame since {min(past_model_scores)} < {mean_reward}')
#
#         idx = np.argmin(past_model_scores)
#         past_model_scores[idx] = mean_reward
#         past_models[idx] = model
#
#
# # NOW WE PLAY SOME SAMPLE GAMES:
# # the latest model plays itself
#
# # agent piece is X, opponent piece is O
# for description, opponents in [("agent plays itself", [past_models[-1]]), ("agent plays hall of fame", past_models)]:
#     for agent_piece in [X, O]:
#         agent_piece_name = "X"
#         opponent_piece_name = "O"
#         if agent_piece == O:
#             agent_piece_name = "O"
#             opponent_piece_name = "X"
#
#         print('')
#         print(f'--- {description} as {agent_piece_name} ---')
#
#         test_env = TicTacEnv(opponents, agent_piece=agent_piece)
#         check_env(test_env)
#
#         for n in range(5):
#             print("")
#             print(f'GAME {n}:')
#             obs = test_env.reset()
#             for i in range(1000):
#                 print(f'step {i}:')
#                 # use 2 ago, since better for O
#                 action, _ = past_models[-1].predict(obs)
#                 obs, reward, done, info = test_env.step(action)
#
#
#
#                 test_env.render()
#
#                 if info.get("IllegalMove", False):
#                     print(f"({agent_piece_name} made an illegal move)")
#                 if info.get("OpponentIllegalMove", False):
#                     print(f"({opponent_piece_name} made an illegal move)")
#
#                 if done:
#                     break
