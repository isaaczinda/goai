import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

EMPTY = 0
O = 1
X = 2

class TicTac4(gym.Env):
	metadata = {'render.modes': ['human']}


	def __init__(self):
		self.state = []
		for i in range(3):
			self.state += [[]]
			for j in range(3):
				self.state[i] += [EMPTY]
		self.counter = 0
		self.done = 0
		self.add = {}
		self.reward = 0
		self.action_space = spaces.Discrete(9)
		self.observation_space = spaces.Box(0, 2, (3, 3), dtype=np.int8)

	def check(self):

		if(self.counter<5):
			return 0
		for i in range(3):
			if(self.state[i][0] != EMPTY and self.state[i][1] == self.state[i][0] and self.state[i][1] == self.state[i][2]):
				if(self.state[i][0] == O):
					return 1
				else:
					return 2
			if(self.state[0][i] != EMPTY and self.state[1][i] == self.state[0][i] and self.state[1][i] == self.state[2][i]):
				if(self.state[0][i] == O):
					return 1
				else:
					return 2
		if(self.state[0][0] != EMPTY and self.state[1][1] == self.state[0][0] and self.state[1][1] == self.state[2][2]):
			if(self.state[0][0] == O):
				return 1
			else:
				return 2
		if(self.state[0][2] != EMPTY and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
			if(self.state[1][1] == O):
				return 1
			else:
				return 2


	#
	def step(self, target):
		if self.done == 1:
			print("Game Over")
			return [self.state, self.reward, self.done, self.add]


		elif self.state[int(target/3)][target%3] != EMPTY:
			print("Invalid Step")
			return [self.state, self.reward, self.done, self.add]
		else:
			if(self.counter%2 == 0):
				self.state[int(target/3)][target%3] = O
			else:
				self.state[int(target/3)][target%3] = X
			self.counter += 1
			if(self.counter == 9):
				self.done = 1;
			self.render()

		# returns 1 if O wins, 2 is X wins
		win = self.check()
		if win:
			self.done = True

			print("Player ", win, " wins.", sep = "", end = "\n")
			# self.add[win-1] = 1;

			turn = self.counter % 2 # if turn == 0, its O's turn

			# if its the current person that won
			if turn + 1 == win:
				self.reward = 100
			

		return [self.state, self.reward, self.done, self.add]

	def reset(self):
		for i in range(3):
			for j in range(3):
				self.state[i][j] = EMPTY
		self.counter = 0
		self.done = 0
		self.add = {}
		self.reward = 0
		return self.state

	def render(self):
		for i in range(3):
			for j in range(3):
				print(self.state[i][j], end = " ")
			print("")
