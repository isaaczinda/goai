import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from numpy.random import default_rng


O = 0
X = 1
EMPTY = 2

WIN_REWARD = 10
LOSS_REWARD = -10
DRAW_REWARD = 0

# WIN_REWARD = 100
# LOSS_REWARD = -100
# DRAW_REWARD = -50
# ILLEGAL_MOVE_REWARD = -10

def get_move_from_array(action):
	flat_action = action.flatten()
	target = np.argmax(flat_action)

	# Returns row, column
	return target//3, target%3

"""A 'model' that chooses a random action from the given action_space."""
class RandomModel:
	def __init__(self, action_space):
		self.action_space = action_space
		self.action_space.seed(123)

	def predict(self, _):
		# The sample() method returns a random action from the space
		action = self.action_space.sample()
		return action, None



class TicTac4(gym.Env):
	metadata = {'render.modes': ['human']}

	action_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.float32)

	# allowed values are 0 - 2 to represent EMPTY, O, and X states
	observation_space = spaces.Tuple((spaces.Discrete(2), spaces.Box(low=0, high=2, shape=(9,), dtype=np.float32)))

	def __init__(self, opponent_models=[RandomModel(action_space)], agent_piece=X, bias_toward_recent=False):
		# contains the piece type that the agent will use
		self.agent_piece = agent_piece
		self.bias_toward_recent = bias_toward_recent

		self.opponent_models = opponent_models

		self.reset()

	def _checkWinner(self):
		""" Returns None if neither player has won. Returns 0 if O has won
		and 1 if X has won. """

		# If there are less than 5 pieces on the board, there can't be a winner.
		if(self.counter<5):
			return None

		# Check for vertical and horizontal three-in-a-row
		for i in range(3):
			if(self.state[i][0] != EMPTY and self.state[i][1] == self.state[i][0] and self.state[i][1] == self.state[i][2]):
				return self.state[i][0]

			if(self.state[0][i] != EMPTY and self.state[1][i] == self.state[0][i] and self.state[1][i] == self.state[2][i]):
				return self.state[0][i]

		# check for diagonal three-in-a-row
		if(self.state[0][0] != EMPTY and self.state[1][1] == self.state[0][0] and self.state[1][1] == self.state[2][2]):
			return self.state[0][0]

		if(self.state[0][2] != EMPTY and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
			return self.state[1][1]

		return None

	def _makeOpponentMove(self):
		# try moves until one of them is legal
		action, _ = self.current_opponent_model.predict(self.state.flatten())
		return get_move_from_array(action)


	def step(self, action):
		row, col = get_move_from_array(action)

		# If this is an illegal move, you lose.
		if self.state[row][col] != EMPTY:
			return self.state.flatten(), LOSS_REWARD, True, {"IllegalMove": True}

		# If this is a legal move, play it!
		# TODO: what if agent piece is None ?
		self.state[row][col] = self.agent_piece
		self.counter += 1

		# Check to see if the agent just won
		if self._checkWinner() == self.agent_piece:
			return self.state.flatten(), WIN_REWARD, True, {}

		# If its a draw
		if self.counter == 9:
			return self.state.flatten(), DRAW_REWARD, True, {}

		# Then choose the square opponent will play on
		opp_row, opp_col = self._makeOpponentMove()

		# Check legality; if it's illegal opponent loses.
		if self.state[opp_row][opp_col] != EMPTY:
			return self.state.flatten(), WIN_REWARD, True, {"OpponentIllegalMove": True}

		# Opponent plays and increment counter
		self.state[opp_row][opp_col] = not self.agent_piece
		self.counter += 1

		# Check to see if the opponent just won
		if self._checkWinner() == (not self.agent_piece):
			return self.state.flatten(), LOSS_REWARD, True, {}

		# If its a draw
		if self.counter == 9:
			return self.state.flatten(), DRAW_REWARD, True, {}

		# If neither player has won yet
		return self.state.flatten(), 0, False, {}


	def reset(self):
		self.counter = 0 # counts the pieces on the board

		self.state = np.array([[EMPTY for i in range(3)] for s in range(3)])

		# choose a random opponent to play for this game
		index = np.random.randint(0, high=len(self.opponent_models), dtype=int)

		# at most 2 first entries are kept "high-priority" (at least 50% of weight)
		if self.bias_toward_recent:
			bias = []
			for i in range(len(self.opponent_models)):
				if i < 2:
					bias.append(.5)
				else:
					bias.append(1/len(self.opponent_models))

			# normalize bias
			bias = np.array(bias) / sum(bias)
			index = np.random.choice(len(self.opponent_models), p=bias)

		self.current_opponent_model = self.opponent_models[index]

		# If our piece is O, this means the opponent is X and they should
		# go first.
		# We put this here because the starting environment which the agent
		# first looks at should already have the opponent's move.
		if self.agent_piece == O:
			opp_row, opp_col = self._makeOpponentMove()

			# Actually place the opponent piece. Since this is the first
			# piece played, it can't be illegal and it can't be a winner!
			self.state[opp_row][opp_col] = not self.agent_piece
			self.counter += 1

		return self.state.flatten()

	def render(self):
		stateToPic = {
			O: "O",
			X: "X",
			EMPTY: ".",
		}

		for i in range(3):
			for j in range(3):
				print(stateToPic[self.state[i][j]], end = " ")
			print("")
		print("---")
