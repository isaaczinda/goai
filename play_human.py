# TODO: fix numpy warnings instead of just suppressing them
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
from os import path
from stable_baselines import PPO2
from tictac import X, O, TicTacEnv

MODEL_NUM = 25
HUMAN_PIECE = O

FILE_PATH = path.dirname(path.realpath(__file__))


def get_human_move():

    # Takes number 1-9 and translates to action space
    action_num = int(input('Where to place (1-9):'))
    return np.array(
        [1 if i == action_num - 1 else 0 for i in range(9)]
    )


def main():
    model = PPO2.load(path.join(FILE_PATH, f"models/{MODEL_NUM}-model"))

    env = TicTacEnv([model], agent_piece=HUMAN_PIECE)

    env.reset()
    env.render()
    done = False
    while not done:
        action = get_human_move()
        obs, reward, done, info = env.step(action)

        env.render()

        if info.get("IllegalMove", False):
            print("(Human made an illegal move)")
        if info.get("OpponentIllegalMove", False):
            print("(AI made an illegal move)")


if __name__ == '__main__':
    main()
