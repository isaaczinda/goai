import gym

from stable_baselines.common.policies import MlpPolicy, FeedForwardPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.schedules import LinearSchedule
from stable_baselines.common.callbacks import BaseCallback

from tictac import TicTacEnv, RandomModel

from elo import Agent, Arena

from os import path

import numpy as np

FILE_PATH = path.dirname(path.realpath(__file__))

class CustomMlpPolicy(FeedForwardPolicy):
    # see here for a description of how the net_arch param should be used.
    # https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/policies.py#L32-L48
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **_kwargs):
        super(CustomMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                        feature_extraction="mlp", net_arch=[128, 128], **_kwargs)

lastTrainingScores = None

class SaveTrainingScores(BaseCallback):
    def __init__(self, verbose=1):
        super(SaveTrainingScores, self).__init__(verbose)

    def _on_training_end(self):
        global lastTrainingScores
        lastTrainingScores = self.training_env.get_attr('scores')[0]

RANDOM = 2
O = 0
X = 1

MIN_SIMILAR_AGENTS = 5
NUM_AGENTS = 20

LEARNING_RATE = .0005
N_MINIBATCHES = 4





# This is a placeholder env. It won't actually be used.
random_env = TicTacEnv([RandomModel(TicTacEnv.action_space)], agent_piece=RANDOM)



def evaluateAgainstRandomOpponent(model):
    model.set_env(DummyVecEnv([lambda: random_env]))

    # Evaluate against random_env to see how it plays against a random opponent
    return evaluate_policy(model, random_env, n_eval_episodes=500)

# Add 10 agents to the Area, where they will play eachother and compete
# for dominance!
arena = Arena()

for _ in range(NUM_AGENTS):
    # random_env won't actually be used, bu we still need to pass it to PPO2 so
    # that the model can be initialized with the right dimensions.
    model = PPO2(CustomMlpPolicy, random_env, verbose=False, learning_rate=LEARNING_RATE, nminibatches=N_MINIBATCHES)
    arena.addAgent(model)

for _ in range(25):
    # make each agent play against a bunch of other agents

    # randomize the indexes so that training happens in a different order
    # each time.
    agentIndexes = [idx for idx in arena.models]
    np.random.shuffle(agentIndexes)

    for agentIdx in agentIndexes:
        agentModel = arena.models[agentIdx].model

        # Since there might not be enough (or any) agents within the starting
        # band of +/- 100 ELO, we keep expanding the search space until we
        # get enough.
        similarAgents = []
        band = 0
        while len(similarAgents) < MIN_SIMILAR_AGENTS:
            band += 100
            similarAgents = arena.getSimilarAgents(agentIdx, band=band)


        print(f'training agent {agentIdx} against {len(similarAgents)} others within +/- {band} Elo')

        similarAgentModels = [agent.model for agent in similarAgents]

        env = TicTacEnv(similarAgentModels, agent_piece=RANDOM)
        agentModel.set_env(DummyVecEnv([lambda: env])) # default is 2.5e-4
        agentModel.learn(total_timesteps=2000, callback=SaveTrainingScores()) # only prints every 128 timesteps

        # Now that many games have been played, we need to get the win / loss ratio
        # and use this to update everyone's Elo rating.
        for index in range(len(lastTrainingScores)):
            score = lastTrainingScores[index]

            arenaIndex = similarAgents[index].index
            arena.recordGames(agentIdx, arenaIndex, score[0], score[1])

    # print all of the ELOs
    for agentIdx in arena.models:
        mean_reward, std_redward = evaluateAgainstRandomOpponent(arena.models[agentIdx].model)
        gamesPlayed = arena.models[agentIdx].games

        print(f'{agentIdx}: ELO {arena.getElo(agentIdx)}, mean reward vs. random player: {mean_reward}, games played: {gamesPlayed}')

    numDeleted = arena.pruneAgents()
    for _ in range(numDeleted):
        model = PPO2(CustomMlpPolicy, random_env, verbose=False, learning_rate=LEARNING_RATE, nminibatches=N_MINIBATCHES)
        arena.addAgent(model)

for i in arena.models:
    arena.models[i].model.save(path.join(FILE_PATH, f'models/{i}-model'))

#
#
# # batch_size (number of steps per NN training) = self.n_batch / self.nminibatches
# #
# # LinearSchedule(100000, final_p=.0000025, initial_p=.0005).value
#
#
#
# for i in range(50):
#     # If we have a trained model, pass it into env
#     if len(past_models) > 0:
#         check_env(env)
#
#
#     # we're just copying what's going on here:
#     #  - https://github.com/hill-a/stable-baselines/blob/master/stable_baselines/common/base_class.py#L78-L84
#     model.set_env(DummyVecEnv([lambda: env])) # default is 2.5e-4
#     model.learn(total_timesteps=5000, callback=SaveTrainingScores()) # only prints every 128 timesteps
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
