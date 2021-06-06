import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


O = 0
X = 1
EMPTY = 2

WIN_REWARD = 10
LOSS_REWARD = 10
DRAW_REWARD = 10
ILLEGAL_MOVE_REWARD = -1000
LEGAL_MOVE_REWARD = 10

# WIN_REWARD = 100
# LOSS_REWARD = -100
# DRAW_REWARD = -50
# ILLEGAL_MOVE_REWARD = -10

"""A 'model' that chooses a random action from the given action_space."""
class RandomModel:
	def __init__(self, action_space):
		self.action_space = action_space

	def predict(self, _):

		# The sample() method returns a random action from the space
		action = self.action_space.sample()
		return action, None

class TicTac4(gym.Env):
	metadata = {'render.modes': ['human']}

	# 0 corresponds self.state[0][0]
	# 1 corresponds to self.state[0][1]
	# generally, N corresponds to self.state[N/3][N%3]
	action_space = spaces.Discrete(9)

	# allowed values are 0 - 2 to represent EMPTY, O, and X states
	observation_space = spaces.Box(0, 2, (3, 3), dtype=np.int8)

	def __init__(self, opponent_model=None, agent_piece=X): #TODO what is X, undefined
		# contains the piece type that the agent will use
		self.agent_piece = agent_piece

		# If an opponent model was provided, use that. If not, just use a
		# model that makes random choices.
		if opponent_model == None:
			print("Using random opponent model.")
			self.opponent_model = RandomModel(self.action_space)
		else:
			print("Using provided opponent model.")
			self.opponent_model = opponent_model

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
		while True:
			action, _ = self.opponent_model.predict(self)

			if self.state[action//3][action%3] == EMPTY:
				# place the opponent's piece
				self.state[action//3][action%3] = not self.agent_piece
				self.counter += 1
				break


	def step(self, target):
		# print("step")
		# If this is an illegal move, penalize.
		if self.state[target//3][target%3] != EMPTY:
			return np.array(self.state), ILLEGAL_MOVE_REWARD, False, {"IllegalMove": True}

		# If this is a legal move, play it!
		# TODO: what if agent piece is None ?
		self.state[target//3][target%3] = self.agent_piece
		self.counter += 1

		# Check to see if the agent just won
		if self._checkWinner() == self.agent_piece:
			# print("win")
			return np.array(self.state), WIN_REWARD, True, {}

		# If its a draw
		if self.counter == 9:
			# print("draw")
			return np.array(self.state), DRAW_REWARD, True, {}

		# Then play the opponent's move
		self._makeOpponentMove()

		# Check to see if the opponent just won
		if self._checkWinner() == (not self.agent_piece):
			# print("loss")
			return np.array(self.state), LOSS_REWARD, True, {}

		# If its a draw
		if self.counter == 9:
			# print("draw")
			return np.array(self.state), DRAW_REWARD, True, {}

		# If neither player has won yet
		return np.array(self.state), LEGAL_MOVE_REWARD, False, {}


	def reset(self):
		# print("reset")
		self.counter = 0 # counts the pieces on the board

		self.state = [[EMPTY for i in range(3)] for s in range(3)]

		# If our piece is O, this means the opponent is X and they should
		# go first.
		# We put this here because the starting environment which the agent
		# first looks at should already have the opponent's move.
		if self.agent_piece == O:
			self._makeOpponentMove()

		return np.array(self.state)

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
