import numpy as np
import math

# Here's now the Elo training scheme will work.
#
# We'll start out with N agents, which have learned nothing yet. They will all
# be initialized with ELO 800.
#
#  1. To train, each agent will train against against O other agents. These O agents
#     must be have a similar ELO to the agent (+/- 50)? After they have trained,
#     the wins / losses from trining will be used
#
# Because the player and the agents by definition don't learn during play (until
# the very end), we don't need to worry about the order that we apply the Elo
# updates in.

class Agent:
    def __init__(self, model, elo, index):
        self.games = 0
        self.model = model
        self.elo = elo
        self.index = index

K = 20

# TODO: convert model --> agent language

class Arena:
    def __init__(self):
        # contains index: Model
        self.models = {}
        self.next_idx = 0
        pass

    def addAgent(self, model, starting_rank=800):
        """ Adds a model to the arena, returns the index used to track
        this model. """

        modelIdx = self.next_idx
        self.models[modelIdx] = Agent(model, starting_rank, modelIdx)
        self.next_idx += 1
        return modelIdx

    # TODO: someday, make this method less jank :)
    def recordGames(self, firstModelIdx, secondModelIdx, firstModelWins, secondModelWins):
        self.models[firstModelIdx].games += firstModelWins + secondModelWins
        self.models[secondModelIdx].games += firstModelWins + secondModelWins

        # we don't want to replay all of the games at once, since there
        # are TONS and if we do this a player which clobbers its
        # opponent will get an unfair boost.
        #
        # In order to avoid this, we randomly shuffle the games up, since it
        # doesn't really matter which order they are played in anyway. Then,
        # we update the model game-by-game.
        games = [(1, 0) for i in range(int(firstModelWins))]
        games += [(0, 1) for i in range(int(secondModelWins))]

        if firstModelWins % 1 != 0:
            games.append((.5, 0))

        if secondModelWins % 1 != 0:
            games.append((0, .5))

        np.random.shuffle(games)

        # update the model game-by-game
        for game in games:
            gamesPlayed = game[0] + game[1] # either 1 or .5

            c_1 = 10**(self.models[firstModelIdx].elo/400)
            c_2 = 10**(self.models[secondModelIdx].elo/400)

            # chance that firstModel wins a game
            e_1 = c_1 / (c_1 + c_2)
            # chance that secondModel wins a game
            e_2 = 1 - e_1

            expectedFirstModelWins = e_1 * gamesPlayed
            expectedSecondModelWins = e_2 * gamesPlayed

            self.models[firstModelIdx].elo += K * (game[0] - expectedFirstModelWins)
            self.models[secondModelIdx].elo += K * (game[1] - expectedSecondModelWins)

    def getElo(self, modelIdx):
        return self.models[modelIdx].elo

    def pruneAgents(self, gameMinimum=10000, prune_percentage=.5):
        """ If a model has played `gameMinimum` games, and its in the bottom
        `prune_percentage` of Elo, delete it. """

        rankedModels = sorted([self.models[i] for i in self.models], key=lambda elem: elem.elo)

        numDeleted = 0

        for i in range(math.ceil(len(rankedModels) * prune_percentage)):
            if rankedModels[i].games > gameMinimum:
                print(f'deleting agent {rankedModels[i].index} which has played {rankedModels[i].games} with Elo {rankedModels[i].elo}')
                self.deleteAgent(rankedModels[i].index)
                numDeleted += 1

        return numDeleted

    def getSimilarAgents(self, modelIdx, maxModels=20, band=200):
        """ Gets models with similar Elo to the provided model. Returns at
        most maxModels which must have Elo within 200 of then provided model.
        """

        modelElo = self.models[modelIdx].elo

        matchingModels = []

        for idx in self.models:
            # don't return the model that was passed in
            if idx == modelIdx:
                continue

            if abs(self.models[idx].elo - modelElo) <= band:
                matchingModels.append(self.models[idx])

        # randomize which of the matching models are returned
        np.random.shuffle(matchingModels)

        return matchingModels[:maxModels]

    def deleteAgent(self, modelIdx):
        del self.models[modelIdx]
