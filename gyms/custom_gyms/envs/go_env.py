import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from board import BoardState, WHITE, BLACK, EMPTY, generate_empty_board

ILLEGAL_MOVE_REWARD = -69

DIM = 9


"""A 'model' that chooses a random action from the given action_space."""
class RandomModel:
	def __init__(self, action_space):
		self.action_space = action_space

	def predict(self, _):

		# The sample() method returns a random action from the space
		action = self.action_space.sample()
		return action, None

# translate board state --> observation space
# translate action space --> place call (easy)
#

def get_move_from_array(action):
	passed = action[0]

	flat_action = action[1].flatten()
	target = np.argmax(flat_action)

	# Returns row, column
	return target//DIM, target%DIM



class Go(gym.Env):
	metadata = {'render.modes': ['human']}

	# 2 since we can either pass or not pass
	action_space = spaces.Tuple(spaces.Discrete(2), spaces.Box(low=-1, high=1, shape=(DIM**2,), dtype=np.float32))

	# allowed values are 0 - 2 to represent BLACK, WHITE, EMPTY states
	observation_space = spaces.Tuple(spaces.Discrete(2), spaces.Box(low=0, high=2, shape=(DIM**2,), dtype=np.int8))


	def __init__(self, opponent_model=None, agent_piece=BLACK):

		# since black always starts
		self.state = BoardState(generate_empty_board(DIM, DIM), BLACK):


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

	def _makeOpponentMove(self):
		action, _ = self.opponent_model.predict(self.state.board.flatten())
		return get_move_from_array(action)


	def step(self, action):

		# Get score before action for diff (self - opponent)
		prev_score = self.state.score(self.agent_piece) - self.state.score(not self.agent_piece)

		row, col = get_move_from_array(action)

		# If this returns None due to invalid placement, you lose
		if self.state.place(row, col) is None:
			return self.state.board.flatten(), ILLEGAL_MOVE_REWARD, True, {'IllegalMove': True}

		# Then choose the square opponent will play on
		opp_row, opp_col = self._makeOpponentMove()

		# Check legality; if it's illegal opponent loses.
		if self.state.place(opp_row, opp_col) is None:
			return self.state.board.flatten(), -1 * ILLEGAL_MOVE_REWARD, True, {'IllegalMove': 'opponent'}

		# You get the difference between new score and previous score
		new_score = self.state.score(self.agent_piece) - self.state.score(not self.agent_piece)
		return self.state.flatten(), new_score - prev_score, False, {}


	def reset(self):
		self.counter = 0 # counts the pieces on the board

		self.state = np.array([[EMPTY for i in range(3)] for s in range(3)])

		# If our piece is O, this means the opponent is X and they should
		# go first.
		# We put this here because the starting environment which the agent
		# first looks at should already have the opponent's move.
		if self.agent_piece == O:
			self._makeOpponentMove()

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
