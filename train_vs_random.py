from rl_example import SaveTrainingScores, makePolicy, trainPolicy, evaluateAgainstRandomPolicy
from tictac import RandomModel, TicTacEnv
from os import path

FILE_PATH = path.dirname(path.realpath(__file__))

policy = makePolicy()

while True:
    trainPolicy(policy, [RandomModel(TicTacEnv.action_space)], timesteps=10000)

    mean, sd = evaluateAgainstRandomPolicy(policy)
    print(mean, sd)

    if mean >= 9.9:
        break

policy.save(path.join(FILE_PATH, f'models/random-trained-model'))
