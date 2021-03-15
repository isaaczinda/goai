from gym.envs.registration import register

# Preexisting Tic Tac Toe environment
register(
    id='tictac4-v0',
    entry_point='custom_gyms.envs:TicTac4',
)
