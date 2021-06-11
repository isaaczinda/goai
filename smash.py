from tictac import RandomModel, TicTacEnv
from os import path
from stable_baselines import PPO2

FILE_PATH = path.dirname(path.realpath(__file__))

agent_piece = 0

model = PPO2.load(path.join(FILE_PATH, "models/13-model"))
test_env = TicTacEnv([model], agent_piece=agent_piece) # agent is O
# test_env = TicTacEnv([RandomModel(TicTacEnv.action_space)], agent_piece=agent_piece) # agent is O

agent_piece_name = "O"
opponent_piece_name = "X"
if agent_piece == 1:
    agent_piece_name = "X"
    opponent_piece_name = "O"

print(f'agent is {agent_piece_name}')

for n in range(5):
    print("")
    print(f'GAME {n}:')
    obs = test_env.reset()
    for i in range(1000):
        print(f'step {i}:')

        action, _ = model.predict(obs)
        obs, reward, done, info = test_env.step(action)

        test_env.render()

        if info.get("IllegalMove", False):
            print(f"({agent_piece_name} made an illegal move)")
        if info.get("OpponentIllegalMove", False):
            print(f"({opponent_piece_name} made an illegal move)")

        if done:
            break
