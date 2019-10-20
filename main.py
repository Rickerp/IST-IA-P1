import math
import pickle
import time

# Ex1. 1 agent, no limits: goal=[56], init=[30], limitexp=2000
# Ex2. 1 agent, w/ limits: goal=[56], init=[30], limitexp=2000, tickets=[5, 5, 2]
# Ex3. 3 agents, no limits: goal=[2, 21, 9]/[61, 60, 71], init=[1, 3, 7]/[30, 40, 109], limitexp=2000
# Ex4. 3 agents, w/ limits: goal=[63, 61, 70], init=[5, 20, 2], limitexp=3000

class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.h = \
			[[0, 1, 2, 3, 2, 1, 2, 2, 3, 4, 4, 4, 3, 7, 6, 6, 5, 6, 4, 4, 3, 3, 4, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 3, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 7, 6, 5, 4, 5, 2, 3, 3, 3, 4, 4, 5, 6, 6, 6, 6, 7, 7, 6, 5, 6, 4, 3, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 6, 7, 7, 7, 6, 7, 6, 6, 4, 5, 5, 5, 5, ], [1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 2, 2, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 2, 3, 3, 4, 5, 5, 6, 5, 6, 7, 6, 7, 6, 5, 3, 4, 3, 4, 4, 4, 5, 5, 6, 7, 6, 6, 6, 7, 7, 6, 5, 7, 5, 4, 5, 5, 5, 5, 5, 6, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 7, 6, 6, 7, 7, 7, 6, 7, 6, 7, 5, 6, 6, 6, 6, ], [2, 1, 0, 1, 3, 2, 2, 1, 2, 3, 3, 3, 2, 6, 5, 5, 4, 5, 3, 3, 2, 3, 3, 3, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 3, 4, 3, 3, 4, 4, 4, 4, 5, 6, 5, 5, 5, 6, 6, 5, 4, 6, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 4, 5, 5, 5, 5, ], [3, 2, 1, 0, 4, 3, 3, 2, 1, 2, 2, 3, 3, 7, 6, 6, 5, 6, 4, 2, 3, 4, 3, 3, 4, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 3, 2, 4, 3, 3, 4, 5, 5, 6, 5, 6, 7, 6, 7, 6, 5, 3, 4, 4, 4, 5, 5, 5, 5, 6, 7, 6, 6, 6, 7, 7, 6, 5, 7, 5, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 7, 6, 6, 7, 7, 7, 6, 7, 6, 7, 5, 6, 6, 6, 6, ], [2, 3, 3, 4, 0, 1, 2, 2, 3, 4, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 3, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 3, ], [1, 2, 2, 3, 1, 0, 1, 1, 2, 3, 3, 3, 2, 6, 5, 5, 4, 5, 3, 3, 2, 2, 3, 3, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 2, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 3, 4, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 3, 3, 2, 6, 5, 5, 4, 5, 3, 2, 1, 1, 2, 3, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 3, 2, 1, 2, 2, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 2, 3, 2, 3, 3, 3, 4, 4, 5, 6, 5, 5, 5, 6, 6, 5, 4, 6, 4, 3, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 4, 5, 5, 5, 5, ], [2, 2, 1, 2, 2, 1, 1, 0, 1, 2, 2, 2, 1, 5, 4, 4, 3, 4, 2, 2, 1, 2, 2, 2, 3, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 3, 3, 2, 2, 1, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 4, 3, 2, 3, 2, 2, 3, 3, 3, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 4, 4, 4, 4, ], [3, 3, 2, 1, 3, 2, 2, 1, 0, 1, 1, 2, 2, 6, 5, 5, 4, 5, 3, 1, 2, 3, 2, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 2, 1, 3, 2, 2, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 2, 3, 3, 3, 4, 4, 4, 4, 5, 6, 5, 5, 5, 6, 6, 5, 4, 6, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 4, 5, 5, 5, 5, ], [4, 4, 3, 2, 4, 3, 3, 2, 1, 0, 1, 2, 2, 6, 5, 5, 4, 5, 3, 2, 3, 4, 3, 1, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 3, 2, 4, 3, 3, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 3, 4, 4, 4, 5, 5, 5, 4, 5, 6, 5, 5, 5, 6, 6, 5, 4, 6, 5, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 6, 5, 6, 5, 6, 6, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 5, 6, 6, 6, 6, ], [4, 4, 3, 2, 4, 3, 3, 2, 1, 1, 0, 1, 1, 5, 4, 4, 3, 4, 2, 2, 2, 3, 2, 1, 3, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 3, 2, 1, 3, 2, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 4, 3, 2, 3, 3, 3, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 5, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [4, 4, 3, 3, 4, 3, 3, 2, 2, 2, 1, 0, 1, 5, 4, 4, 3, 4, 2, 3, 3, 4, 3, 2, 2, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 3, 1, 2, 4, 2, 3, 2, 3, 3, 4, 3, 4, 5, 4, 5, 4, 3, 3, 4, 3, 3, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 5, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [3, 3, 2, 3, 3, 2, 2, 1, 2, 2, 1, 1, 0, 4, 3, 3, 2, 3, 1, 2, 2, 3, 2, 1, 2, 1, 2, 2, 2, 1, 3, 4, 3, 4, 2, 2, 2, 2, 3, 1, 2, 1, 2, 2, 3, 2, 3, 4, 3, 4, 3, 2, 2, 3, 2, 2, 3, 3, 3, 2, 3, 4, 3, 3, 3, 4, 4, 3, 2, 4, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 4, 3, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, ], [4, 4, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 1, 0, 1, 4, 3, 4, 2, 3, 3, 4, 3, 2, 3, 2, 3, 2, 3, 2, 4, 5, 4, 5, 3, 3, 3, 3, 4, 2, 3, 2, 3, 3, 3, 3, 4, 5, 4, 4, 4, 3, 3, 4, 3, 3, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 5, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 1, 0, 5, 4, 3, 3, 4, 4, 5, 4, 3, 3, 2, 2, 1, 4, 3, 3, 4, 3, 4, 2, 3, 4, 4, 5, 3, 4, 3, 4, 3, 2, 3, 3, 4, 4, 3, 4, 4, 4, 5, 4, 4, 5, 5, 5, 4, 4, 4, 3, 4, 4, 5, 4, 5, 4, 4, 5, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 6, 5, 4, 5, 5, 6, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 6, 6, 6, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 0, 1, 2, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 1, 2, 3, 3, 3, 4, 3, 5, 5, 5, 6, 4, 5, 4, 5, 4, 3, 2, 3, 4, 3, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 3, 5, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 5, 6, 5, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 6, 6, 6, 6, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 5, 4, 1, 0, 1, 3, 4, 4, 5, 4, 3, 4, 3, 4, 3, 2, 1, 2, 2, 2, 3, 2, 4, 4, 4, 5, 3, 4, 3, 4, 4, 3, 2, 3, 3, 3, 4, 4, 3, 4, 4, 4, 4, 5, 4, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 2, 4, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 5, 5, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 2, 1, 0, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 1, 1, 1, 2, 1, 4, 5, 5, 6, 4, 5, 4, 5, 4, 3, 3, 2, 2, 4, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 5, 4, 4, 3, 3, 2, 3, 3, 5, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 5, 6, 5, 5, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 4, 6, 6, 6, 6, ], [4, 4, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 1, 4, 3, 4, 3, 4, 0, 3, 3, 4, 3, 2, 3, 2, 1, 2, 3, 2, 4, 5, 4, 5, 3, 3, 3, 3, 4, 2, 3, 2, 3, 3, 3, 3, 4, 5, 4, 4, 4, 3, 3, 4, 3, 3, 4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 5, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [4, 3, 3, 2, 3, 3, 2, 2, 1, 2, 2, 3, 2, 6, 5, 5, 4, 5, 3, 0, 1, 2, 1, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 3, 2, 1, 2, 1, 1, 2, 3, 4, 5, 4, 5, 6, 5, 6, 5, 3, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [3, 2, 2, 3, 3, 2, 1, 1, 2, 3, 2, 3, 2, 6, 5, 5, 4, 5, 3, 1, 0, 1, 1, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 3, 2, 1, 1, 1, 1, 2, 3, 4, 5, 4, 5, 6, 5, 6, 5, 3, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [2, 2, 3, 4, 2, 1, 1, 2, 3, 4, 3, 4, 3, 7, 6, 6, 5, 6, 4, 2, 1, 0, 2, 3, 4, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 4, 3, 2, 1, 2, 2, 3, 4, 5, 6, 5, 6, 7, 6, 7, 6, 4, 2, 3, 2, 3, 3, 3, 4, 4, 5, 6, 6, 6, 6, 7, 7, 6, 5, 6, 4, 3, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 6, 7, 7, 7, 6, 7, 6, 6, 4, 5, 5, 5, 5, ], [4, 3, 3, 3, 3, 3, 2, 2, 2, 3, 2, 3, 2, 6, 5, 5, 4, 5, 3, 1, 1, 2, 0, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 3, 2, 1, 1, 1, 1, 2, 3, 4, 5, 4, 5, 6, 5, 6, 5, 3, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [5, 4, 4, 3, 4, 4, 3, 3, 2, 1, 1, 2, 2, 6, 5, 5, 4, 5, 3, 2, 2, 3, 2, 0, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 2, 1, 3, 2, 2, 3, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 2, 3, 3, 3, 4, 4, 4, 4, 5, 6, 5, 5, 5, 6, 6, 5, 4, 6, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 4, 5, 5, 5, 5, ], [5, 5, 4, 4, 5, 4, 4, 3, 3, 4, 3, 2, 2, 4, 3, 5, 4, 4, 3, 3, 3, 4, 3, 3, 0, 1, 2, 2, 4, 3, 4, 5, 4, 5, 3, 2, 1, 2, 4, 3, 3, 2, 3, 2, 3, 4, 4, 5, 5, 4, 3, 3, 3, 4, 4, 4, 5, 5, 4, 3, 3, 4, 4, 5, 5, 6, 5, 5, 4, 5, 4, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 5, 4, 4, 5, 5, 5, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 6, 5, 5, 6, 6, 6, 5, 6, 5, 6, 5, 6, 6, 6, 6, ], [4, 4, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 1, 3, 2, 4, 3, 3, 2, 3, 3, 4, 3, 2, 1, 0, 1, 1, 3, 2, 3, 4, 3, 4, 2, 1, 2, 3, 4, 2, 3, 2, 2, 1, 2, 3, 3, 4, 4, 3, 2, 3, 3, 4, 3, 3, 4, 4, 4, 3, 2, 3, 3, 4, 4, 5, 4, 4, 3, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 5, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 3, 2, 5, 4, 3, 1, 4, 4, 5, 4, 3, 2, 1, 0, 1, 4, 3, 3, 4, 3, 4, 2, 2, 3, 4, 5, 3, 4, 3, 3, 2, 2, 3, 3, 4, 4, 3, 3, 4, 4, 5, 4, 4, 5, 5, 5, 4, 3, 4, 3, 4, 4, 5, 4, 5, 4, 4, 5, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 6, 5, 4, 5, 5, 6, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 6, 6, 6, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 2, 1, 4, 3, 2, 2, 4, 4, 5, 4, 3, 2, 1, 1, 0, 3, 2, 2, 3, 2, 3, 1, 2, 3, 4, 5, 3, 4, 3, 3, 2, 1, 2, 2, 3, 3, 2, 3, 4, 4, 5, 4, 4, 5, 5, 4, 3, 3, 3, 2, 3, 3, 4, 3, 4, 3, 3, 4, 4, 5, 6, 5, 5, 5, 6, 5, 5, 5, 5, 4, 3, 4, 4, 5, 6, 6, 6, 6, 5, 5, 6, 5, 6, 5, 5, 4, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 6, 6, 6, 6, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 5, 4, 1, 2, 3, 3, 4, 4, 5, 4, 3, 4, 3, 4, 3, 0, 1, 3, 4, 3, 4, 2, 4, 4, 4, 5, 3, 4, 3, 4, 3, 2, 1, 2, 3, 2, 3, 4, 3, 4, 4, 4, 4, 5, 4, 3, 2, 3, 4, 3, 3, 3, 4, 4, 3, 2, 4, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 5, 5, ], [4, 4, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 1, 4, 3, 2, 1, 2, 2, 3, 3, 4, 3, 2, 3, 2, 3, 2, 1, 0, 2, 3, 2, 3, 1, 3, 3, 3, 4, 2, 3, 2, 3, 3, 2, 1, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 4, 3, 2, 1, 2, 3, 2, 2, 2, 3, 3, 2, 1, 3, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 3, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5, 3, 4, 3, 3, 3, 2, 2, 3, 3, 3, 2, 3, 2, 3, 2, 4, 4, 4, 4, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 3, 2, 1, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 0, 1, 2, 3, 1, 4, 5, 5, 6, 4, 5, 4, 5, 4, 3, 3, 2, 3, 4, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 5, 4, 4, 3, 4, 3, 4, 3, 5, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 5, 6, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 6, 6, 6, 6, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 3, 2, 1, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 2, 0, 1, 2, 1, 4, 5, 5, 6, 4, 5, 4, 5, 4, 3, 3, 2, 2, 4, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 5, 4, 4, 3, 3, 2, 3, 3, 5, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 5, 6, 5, 5, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 4, 6, 6, 6, 6, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 3, 2, 1, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 2, 1, 0, 1, 1, 4, 5, 5, 6, 4, 5, 4, 5, 4, 3, 3, 2, 1, 3, 4, 4, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 3, 2, 2, 1, 2, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 3, 3, 3, 2, 3, 2, 3, 3, 4, 3, 5, 5, 6, 6, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 4, 3, 2, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 2, 2, 1, 0, 1, 4, 5, 5, 6, 4, 5, 4, 5, 4, 3, 3, 2, 2, 4, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 5, 4, 4, 3, 3, 2, 3, 3, 5, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 5, 6, 5, 5, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 4, 6, 6, 6, 6, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 3, 2, 3, 2, 1, 3, 4, 4, 5, 4, 3, 3, 2, 2, 1, 2, 1, 1, 2, 1, 2, 0, 3, 4, 4, 5, 3, 4, 3, 4, 3, 2, 2, 1, 2, 3, 3, 4, 3, 4, 4, 4, 4, 5, 4, 3, 2, 3, 4, 3, 3, 2, 3, 2, 3, 2, 4, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 3, 4, 3, 5, 5, 5, 5, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 4, 3, 5, 4, 4, 3, 3, 3, 4, 3, 3, 2, 1, 2, 2, 4, 3, 4, 5, 4, 5, 3, 0, 2, 3, 4, 3, 2, 1, 1, 1, 2, 3, 3, 4, 4, 3, 2, 2, 3, 4, 4, 4, 5, 4, 3, 2, 2, 3, 3, 4, 4, 5, 5, 4, 3, 4, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [5, 4, 4, 3, 4, 4, 3, 3, 2, 3, 2, 1, 2, 5, 4, 5, 4, 5, 3, 2, 2, 3, 2, 2, 1, 2, 3, 3, 4, 3, 5, 6, 5, 6, 4, 2, 0, 1, 3, 2, 2, 1, 2, 3, 4, 4, 5, 6, 5, 5, 4, 2, 2, 3, 3, 3, 4, 4, 3, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 5, 3, 3, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 3, 4, 4, 5, 4, 5, 5, 5, 5, 4, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, ], [4, 3, 3, 2, 3, 3, 2, 2, 1, 2, 1, 2, 2, 6, 5, 5, 4, 5, 3, 1, 1, 2, 1, 1, 2, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 3, 1, 0, 2, 1, 1, 2, 3, 4, 5, 4, 5, 6, 5, 6, 5, 3, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [3, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 4, 3, 7, 6, 6, 5, 6, 4, 2, 1, 1, 1, 3, 4, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 4, 3, 2, 0, 2, 2, 3, 4, 5, 6, 5, 6, 7, 6, 6, 6, 4, 2, 3, 1, 2, 3, 2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [3, 3, 2, 3, 2, 2, 2, 1, 2, 3, 2, 2, 1, 5, 4, 4, 3, 4, 2, 1, 1, 2, 1, 2, 3, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 3, 2, 1, 2, 0, 1, 2, 3, 3, 4, 3, 4, 5, 4, 5, 4, 3, 1, 2, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 2, 3, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 2, 2, 3, 2, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 3, 3, 3, ], [4, 3, 3, 3, 3, 3, 2, 2, 2, 3, 2, 3, 2, 6, 5, 5, 4, 5, 3, 1, 1, 2, 1, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 2, 2, 1, 2, 1, 0, 1, 2, 3, 4, 4, 5, 6, 5, 5, 4, 2, 1, 2, 2, 2, 3, 3, 3, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 4, 4, 4, 4, ], [4, 4, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 1, 5, 4, 4, 3, 4, 2, 2, 2, 3, 2, 2, 2, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 1, 1, 2, 3, 2, 1, 0, 1, 2, 3, 3, 4, 5, 4, 4, 3, 1, 2, 3, 3, 3, 4, 3, 2, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 4, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 5, 3, 4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, ], [5, 5, 4, 5, 4, 4, 4, 3, 4, 4, 3, 3, 2, 5, 4, 4, 3, 4, 3, 3, 3, 4, 3, 3, 3, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 3, 4, 4, 3, 2, 2, 3, 3, 3, 3, 4, 3, 2, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 4, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 5, 3, 4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 4, 3, 4, 4, 4, 3, 4, 4, 5, 4, 3, 2, 1, 2, 2, 3, 3, 4, 5, 4, 5, 3, 1, 3, 4, 5, 3, 3, 2, 1, 0, 1, 2, 2, 3, 3, 2, 1, 3, 4, 4, 4, 4, 5, 4, 3, 2, 1, 2, 2, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 2, 4, 3, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 4, 4, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 5, 5, 5, 5, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 3, 2, 3, 3, 3, 3, 5, 5, 6, 5, 4, 3, 2, 2, 1, 2, 2, 3, 4, 3, 4, 2, 2, 4, 5, 6, 4, 4, 3, 2, 1, 0, 1, 1, 2, 2, 1, 2, 4, 5, 5, 5, 5, 6, 5, 4, 3, 2, 2, 1, 2, 2, 3, 3, 3, 2, 2, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 4, 3, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 6, 6, ], [5, 5, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 4, 3, 2, 2, 3, 3, 4, 4, 5, 4, 3, 4, 3, 3, 2, 1, 1, 3, 4, 3, 4, 2, 3, 4, 4, 5, 3, 4, 3, 3, 2, 1, 0, 1, 2, 1, 2, 3, 3, 4, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 2, 3, 3, 3, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 5, 5, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 3, 3, 2, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 2, 2, 2, 3, 2, 3, 1, 3, 5, 5, 6, 4, 5, 4, 3, 2, 1, 1, 0, 1, 2, 2, 3, 4, 5, 5, 5, 5, 6, 5, 4, 3, 3, 3, 2, 2, 1, 2, 2, 3, 2, 3, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 3, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 3, 4, 3, 5, 5, 6, 6, ], [7, 7, 6, 7, 7, 6, 6, 5, 6, 6, 5, 5, 4, 5, 4, 4, 3, 2, 5, 6, 6, 7, 6, 5, 5, 4, 4, 3, 3, 3, 3, 2, 1, 2, 2, 4, 6, 6, 7, 5, 6, 5, 4, 3, 2, 2, 1, 0, 3, 3, 4, 5, 6, 6, 6, 6, 7, 6, 5, 4, 4, 4, 3, 3, 2, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 7, 7, 8, 7, 6, 6, 6, 5, 4, 4, 5, 6, 6, 7, 7, 7, 7, 7, 8, 6, 6, 5, 5, 5, 4, 4, 4, 3, 2, 3, 4, 4, 5, 4, 6, 6, 7, 7, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 5, 4, 3, 3, 4, 4, 5, 5, 6, 5, 4, 5, 4, 4, 3, 2, 2, 4, 4, 3, 4, 3, 4, 5, 5, 6, 4, 5, 4, 4, 3, 2, 1, 2, 3, 0, 1, 2, 4, 5, 5, 5, 5, 6, 5, 4, 3, 3, 2, 1, 1, 1, 2, 2, 2, 2, 2, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 4, 3, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 3, 3, 3, 3, 3, 3, 3, 4, 3, 4, 3, 5, 5, 6, 6, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 4, 3, 4, 4, 4, 4, 6, 6, 7, 6, 5, 4, 3, 3, 2, 3, 3, 4, 5, 4, 5, 3, 3, 5, 6, 6, 5, 5, 4, 3, 2, 1, 2, 2, 3, 1, 0, 1, 4, 6, 5, 5, 5, 6, 5, 4, 3, 3, 2, 1, 2, 2, 3, 3, 3, 2, 2, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 4, 3, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 6, 6, ], [6, 6, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 5, 4, 5, 4, 5, 4, 5, 5, 6, 5, 4, 3, 2, 3, 3, 4, 3, 5, 6, 5, 6, 4, 2, 4, 5, 6, 4, 4, 3, 2, 1, 2, 3, 3, 4, 2, 1, 0, 4, 5, 5, 5, 5, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 2, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 4, 3, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 5, 5, 6, 6, ], [5, 5, 4, 5, 4, 4, 4, 3, 4, 4, 3, 3, 2, 6, 5, 4, 3, 4, 3, 3, 3, 4, 3, 3, 3, 3, 4, 4, 3, 2, 4, 5, 4, 5, 3, 2, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 4, 5, 4, 4, 4, 0, 3, 3, 3, 3, 4, 3, 2, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 4, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 5, 3, 4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, ], [4, 3, 3, 3, 3, 3, 2, 2, 2, 3, 2, 3, 2, 6, 5, 5, 4, 5, 3, 1, 1, 2, 1, 2, 3, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 2, 2, 1, 2, 1, 1, 1, 2, 3, 4, 4, 5, 6, 5, 5, 4, 2, 0, 1, 2, 2, 3, 3, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 5, 3, 2, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 4, 4, 4, 4, ], [3, 4, 4, 4, 3, 2, 3, 3, 3, 4, 3, 4, 3, 7, 6, 5, 4, 5, 4, 2, 2, 3, 2, 3, 4, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 3, 3, 2, 2, 2, 2, 2, 3, 4, 5, 4, 5, 6, 5, 5, 5, 3, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 5, 2, 2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 4, 3, 4, 5, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 4, 4, 4, 4, ], [2, 3, 3, 4, 2, 1, 2, 2, 3, 4, 3, 3, 2, 6, 5, 5, 4, 5, 3, 2, 2, 2, 2, 3, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 2, 3, 0, 1, 2, 1, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 2, 2, 3, 2, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 3, 3, 3, ], [3, 4, 3, 4, 1, 2, 3, 2, 3, 4, 3, 3, 2, 6, 5, 5, 4, 5, 3, 2, 2, 3, 2, 3, 4, 3, 4, 4, 4, 3, 5, 6, 5, 6, 4, 4, 3, 2, 2, 1, 2, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 2, 3, 1, 0, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 3, 3, 3, 4, 3, 3, 3, 3, 3, 2, 1, 1, 2, 2, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 3, 3, 2, ], [3, 4, 4, 5, 1, 2, 3, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 0, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 3, ], [3, 4, 4, 5, 3, 2, 3, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 3, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 2, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 3, 3, 1, 2, 3, 0, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 1, 1, 2, 3, 3, 4, 2, 2, 2, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 3, 3, 3, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 3, 3, 4, 3, 4, 4, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 4, 3, 4, 5, 4, 4, 4, 2, 2, 1, 2, 2, 3, 2, 0, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 4, 1, 1, 2, 3, 3, 3, 3, 4, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 3, 2, 3, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 2, 3, 3, 3, 3, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 4, 3, 3, 2, 5, 4, 3, 2, 3, 3, 3, 3, 4, 3, 3, 3, 3, 4, 3, 2, 1, 3, 4, 3, 4, 2, 2, 2, 3, 3, 2, 2, 1, 2, 2, 3, 2, 3, 4, 3, 3, 3, 1, 3, 2, 2, 2, 3, 2, 1, 0, 1, 2, 2, 2, 2, 3, 3, 2, 1, 3, 1, 1, 2, 3, 3, 3, 3, 4, 3, 2, 2, 2, 1, 2, 2, 3, 2, 3, 3, 3, 3, 3, 3, 4, 2, 3, 2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 2, 3, 2, 3, 3, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 5, 4, 4, 3, 5, 4, 4, 3, 4, 4, 4, 4, 5, 4, 4, 3, 2, 3, 3, 3, 2, 4, 5, 4, 5, 3, 2, 3, 4, 4, 3, 3, 2, 2, 1, 2, 3, 3, 4, 3, 3, 2, 2, 4, 3, 3, 3, 4, 3, 2, 1, 0, 1, 2, 3, 3, 4, 4, 3, 2, 2, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 1, 3, 2, 3, 4, 4, 4, 4, 4, 4, 5, 3, 4, 3, 3, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 2, 4, 4, 4, 4, ], [6, 7, 6, 7, 5, 5, 6, 5, 6, 6, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, 6, 5, 5, 4, 3, 4, 3, 4, 3, 5, 6, 5, 6, 4, 3, 4, 5, 5, 4, 4, 3, 3, 2, 2, 3, 3, 4, 2, 2, 1, 3, 5, 4, 4, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 4, 3, 2, 1, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 2, 3, 3, 4, 5, 5, 5, 5, 5, 5, 6, 4, 5, 4, 3, 2, 3, 3, 4, 4, 4, 3, 4, 3, 3, 3, 5, 5, 5, 5, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 4, 3, 4, 3, 4, 4, 5, 5, 6, 5, 4, 4, 3, 3, 2, 3, 2, 4, 5, 4, 5, 3, 3, 4, 5, 5, 4, 4, 3, 3, 2, 1, 2, 2, 3, 1, 1, 1, 3, 5, 4, 4, 4, 5, 4, 3, 2, 2, 1, 0, 1, 2, 3, 3, 2, 1, 1, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 3, 2, 1, 2, 2, 3, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 2, 2, 2, 3, 3, 3, 2, 3, 2, 3, 2, 4, 4, 5, 5, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 4, 5, 4, 4, 3, 3, 2, 4, 4, 3, 4, 3, 4, 4, 5, 5, 4, 4, 3, 4, 3, 2, 2, 2, 3, 1, 2, 2, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 2, 1, 0, 1, 2, 2, 1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 2, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 2, 2, 2, 3, 3, 2, 3, 2, 3, 2, 4, 4, 5, 5, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 5, 4, 4, 3, 3, 4, 5, 5, 6, 5, 4, 5, 4, 4, 3, 3, 2, 3, 3, 2, 3, 2, 4, 4, 5, 5, 4, 4, 3, 4, 3, 2, 2, 1, 2, 1, 2, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 1, 0, 1, 1, 2, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 3, 2, 4, 4, 5, 5, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 6, 5, 5, 4, 3, 5, 6, 6, 7, 6, 5, 6, 5, 5, 4, 4, 3, 4, 3, 2, 3, 3, 5, 5, 6, 6, 5, 5, 4, 5, 4, 3, 3, 2, 1, 2, 3, 4, 4, 6, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 2, 1, 0, 2, 3, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 3, 3, 4, 3, 1, 2, 3, 3, 4, 3, 5, 5, 6, 6, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 5, 4, 4, 3, 2, 4, 5, 5, 6, 5, 4, 5, 4, 4, 3, 3, 2, 3, 2, 1, 2, 2, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 2, 2, 2, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 1, 2, 0, 1, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 2, 2, 2, 1, 2, 1, 2, 2, 3, 2, 4, 4, 5, 5, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 3, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 3, 2, 4, 3, 2, 3, 3, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 3, 3, 2, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 1, 2, 3, 1, 0, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 2, 2, 1, 2, 3, 2, 2, 2, 3, 2, 4, 4, 5, 5, ], [5, 5, 4, 5, 4, 4, 4, 3, 4, 4, 3, 3, 2, 5, 4, 3, 2, 3, 3, 4, 4, 5, 4, 3, 4, 3, 4, 3, 2, 1, 3, 4, 3, 4, 2, 3, 3, 4, 4, 3, 3, 2, 3, 3, 2, 2, 2, 3, 2, 2, 2, 2, 4, 3, 3, 3, 4, 3, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 0, 2, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 2, 1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 3, 3, 4, 4, ], [6, 7, 6, 7, 5, 5, 6, 5, 6, 6, 5, 5, 4, 5, 4, 5, 4, 5, 5, 5, 5, 6, 5, 5, 5, 4, 4, 3, 4, 3, 5, 6, 5, 6, 4, 4, 5, 5, 5, 4, 5, 4, 4, 3, 2, 3, 3, 4, 2, 2, 2, 4, 5, 5, 4, 4, 5, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 0, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 3, 2, 1, 2, 2, 3, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 2, 1, 3, 3, 4, 4, 4, 3, 4, 3, 2, 2, 4, 4, 5, 5, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 3, 3, 4, 3, 4, 4, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 4, 3, 4, 5, 4, 4, 4, 2, 3, 2, 2, 2, 3, 2, 1, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 3, 0, 1, 2, 3, 3, 3, 3, 4, 3, 2, 2, 1, 1, 2, 3, 3, 2, 2, 3, 3, 3, 3, 3, 4, 2, 3, 2, 3, 4, 3, 3, 4, 4, 4, 3, 4, 3, 4, 2, 3, 3, 3, 3, ], [3, 4, 3, 4, 2, 2, 3, 2, 3, 4, 3, 3, 2, 6, 5, 4, 3, 4, 3, 2, 2, 3, 2, 3, 4, 3, 4, 4, 3, 2, 4, 5, 4, 5, 3, 3, 3, 2, 2, 1, 2, 2, 3, 3, 4, 3, 4, 5, 4, 4, 4, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 3, 2, 3, 1, 0, 1, 2, 2, 2, 2, 3, 2, 1, 1, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 2, 1, 2, 3, 2, 3, 4, 4, 4, 3, 4, 3, 3, 1, 2, 2, 2, 2, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 3, 3, 2, 2, 3, 1, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 0, 1, 2, 3, 3, 3, 1, 1, 2, 3, 3, 3, 4, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 3, 3, 3, ], [4, 5, 5, 6, 3, 3, 4, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 4, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 3, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 2, 2, 3, 1, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 1, 0, 1, 2, 3, 3, 2, 2, 3, 4, 4, 4, 5, 4, 4, 4, 3, 3, 3, 3, 3, 4, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 4, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 2, 1, 0, 1, 2, 2, 1, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 3, 2, 2, 2, 3, 2, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 3, 3, 3, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 2, 1, 0, 2, 1, 2, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 3, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 2, 2, 0, 1, 2, 3, 3, 4, 4, 4, 5, 4, 4, 4, 4, 4, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 4, 4, 4, 3, ], [5, 6, 5, 6, 3, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 7, 6, 7, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 6, 5, 7, 8, 7, 8, 6, 6, 5, 4, 4, 3, 4, 5, 6, 6, 7, 6, 7, 8, 7, 7, 7, 5, 4, 5, 3, 2, 3, 4, 4, 4, 5, 6, 6, 6, 6, 7, 7, 6, 5, 6, 4, 3, 3, 3, 2, 1, 1, 0, 2, 4, 4, 5, 5, 5, 6, 5, 5, 5, 4, 4, 3, 1, 1, 2, 3, 5, 4, 5, 6, 5, 6, 7, 7, 7, 6, 7, 6, 6, 4, 4, 3, 3, 2, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 1, 2, 1, 2, 2, 2, 0, 2, 3, 4, 4, 4, 5, 4, 4, 4, 3, 2, 1, 1, 2, 2, 1, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 3, 2, 2, 2, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 1, 2, 3, 3, 3, 4, 2, 0, 2, 3, 3, 3, 4, 3, 3, 3, 1, 1, 2, 3, 3, 4, 2, 2, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 2, 3, 3, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 2, 3, 3, 3, 3, 4, 3, 2, 0, 1, 2, 3, 4, 3, 3, 1, 1, 2, 3, 3, 3, 4, 2, 2, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 3, 2, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 7, 6, 5, 4, 5, 5, 4, 4, 5, 4, 5, 5, 5, 6, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 4, 4, 3, 4, 3, 4, 4, 4, 4, 5, 6, 4, 4, 4, 3, 4, 3, 3, 3, 4, 3, 2, 2, 3, 4, 3, 4, 4, 5, 5, 4, 3, 3, 1, 2, 3, 4, 4, 4, 4, 5, 4, 3, 1, 0, 1, 2, 4, 3, 2, 1, 2, 3, 4, 4, 4, 5, 3, 3, 2, 4, 4, 4, 4, 5, 5, 5, 4, 5, 4, 5, 3, 3, 3, 4, 4, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 4, 4, 5, 4, 4, 4, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 3, 3, 4, 4, 3, 3, 2, 3, 3, 3, 3, 4, 5, 3, 3, 3, 2, 4, 3, 3, 3, 4, 3, 2, 1, 2, 3, 2, 3, 3, 4, 4, 3, 2, 2, 1, 2, 3, 4, 4, 4, 4, 5, 4, 3, 2, 1, 0, 1, 3, 2, 1, 2, 3, 3, 4, 4, 4, 4, 3, 2, 1, 3, 3, 3, 3, 4, 4, 4, 3, 4, 3, 4, 2, 2, 2, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 5, 4, 5, 4, 5, 5, 4, 4, 5, 4, 5, 4, 3, 4, 3, 4, 3, 5, 6, 5, 6, 4, 3, 4, 4, 4, 3, 4, 3, 3, 2, 2, 3, 3, 4, 2, 2, 2, 3, 4, 4, 3, 3, 4, 3, 3, 2, 1, 2, 1, 2, 3, 4, 4, 3, 2, 1, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 2, 1, 0, 3, 1, 2, 3, 4, 4, 4, 4, 4, 5, 3, 3, 2, 2, 2, 2, 3, 4, 4, 4, 3, 4, 3, 3, 1, 3, 3, 4, 4, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 1, 2, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 0, 2, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 2, 1, 1, 2, 3, 3, 3, 2, 3, 2, 2, 2, 4, 4, 5, 5, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 6, 5, 5, 4, 5, 5, 4, 4, 5, 4, 5, 5, 4, 5, 4, 4, 3, 5, 6, 5, 6, 4, 4, 5, 4, 4, 3, 4, 4, 4, 3, 3, 4, 4, 5, 3, 3, 3, 4, 4, 4, 3, 3, 4, 3, 3, 3, 2, 3, 2, 3, 3, 4, 4, 3, 2, 2, 3, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 3, 2, 1, 2, 0, 3, 3, 4, 4, 4, 4, 4, 5, 3, 3, 2, 2, 1, 2, 3, 4, 4, 4, 3, 4, 3, 2, 1, 3, 3, 4, 4, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 7, 6, 5, 4, 5, 5, 4, 4, 5, 4, 5, 5, 5, 6, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 4, 4, 3, 4, 3, 4, 4, 4, 4, 5, 6, 4, 4, 4, 3, 4, 4, 3, 3, 4, 3, 3, 2, 3, 4, 3, 4, 4, 5, 5, 4, 3, 3, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 2, 1, 2, 4, 3, 0, 2, 3, 3, 4, 4, 4, 4, 3, 2, 1, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 2, 2, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 5, 5, 5, 6, 5, 5, 5, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 4, 2, 2, 3, 4, 4, 4, 4, 5, 4, 3, 1, 1, 2, 3, 4, 3, 2, 0, 2, 3, 4, 4, 4, 4, 3, 2, 1, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 2, 2, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 2, 3, 4, 4, 4, 4, 3, 1, 1, 2, 3, 4, 5, 4, 3, 2, 0, 1, 2, 3, 3, 3, 2, 1, 2, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 2, 1, 2, 2, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 2, 3, 3, 4, 4, 4, 2, 1, 2, 3, 3, 4, 5, 4, 3, 3, 1, 0, 1, 3, 3, 3, 1, 2, 2, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 2, 1, 2, 2, ], [5, 6, 5, 6, 3, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 3, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 2, 3, 2, 3, 3, 3, 1, 2, 3, 4, 4, 4, 5, 4, 4, 4, 2, 1, 0, 2, 3, 3, 1, 3, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 3, 2, 2, 2, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 2, 3, 2, 2, 2, 1, 1, 3, 3, 4, 4, 4, 5, 4, 4, 4, 3, 3, 2, 0, 1, 1, 2, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 3, 2, 2, 1, ], [4, 5, 4, 5, 2, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 6, 5, 6, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 5, 4, 6, 7, 6, 7, 5, 5, 4, 3, 3, 2, 3, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 3, 4, 2, 1, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 3, 2, 2, 2, 1, 2, 3, 3, 4, 4, 4, 5, 4, 4, 4, 3, 3, 3, 1, 0, 1, 2, 4, 3, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 3, 2, 2, 1, ], [5, 6, 5, 6, 3, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 7, 6, 7, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 6, 5, 7, 8, 7, 8, 6, 6, 5, 4, 4, 3, 4, 5, 6, 6, 7, 6, 7, 8, 7, 7, 7, 5, 4, 5, 3, 2, 3, 4, 4, 4, 5, 6, 6, 6, 6, 7, 7, 6, 5, 6, 4, 3, 3, 4, 3, 3, 3, 2, 2, 4, 4, 5, 4, 5, 6, 5, 4, 4, 3, 3, 3, 1, 1, 0, 2, 4, 3, 5, 6, 5, 6, 7, 7, 7, 6, 7, 6, 6, 4, 3, 2, 2, 1, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 5, 4, 5, 6, 5, 5, 5, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 4, 3, 4, 2, 1, 2, 3, 2, 3, 3, 3, 1, 2, 2, 3, 3, 3, 4, 3, 3, 3, 2, 1, 1, 2, 2, 2, 0, 3, 2, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 2, 1, 1, 1, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 5, 5, 5, 6, 5, 5, 5, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 4, 3, 2, 3, 4, 4, 4, 4, 5, 4, 2, 2, 3, 2, 3, 4, 3, 2, 2, 1, 2, 3, 4, 4, 4, 3, 0, 1, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 1, 2, 3, 3, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 7, 6, 5, 4, 5, 4, 3, 3, 4, 3, 4, 5, 4, 5, 5, 4, 3, 5, 6, 5, 6, 4, 4, 4, 3, 3, 2, 3, 3, 4, 4, 4, 4, 4, 5, 4, 4, 4, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 4, 3, 3, 3, 4, 4, 3, 2, 3, 2, 1, 2, 3, 3, 3, 3, 4, 3, 2, 2, 2, 1, 2, 3, 2, 1, 1, 2, 2, 3, 3, 3, 3, 2, 1, 0, 2, 3, 2, 3, 4, 4, 4, 3, 4, 3, 3, 1, 1, 1, 2, 2, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 7, 6, 5, 4, 5, 5, 4, 4, 5, 4, 5, 6, 5, 6, 5, 4, 3, 5, 6, 5, 6, 4, 5, 5, 4, 4, 3, 4, 4, 5, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 2, 2, 3, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 4, 3, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 5, 3, 3, 2, 0, 1, 2, 3, 4, 4, 4, 3, 3, 2, 1, 1, 3, 3, 4, 4, ], [6, 7, 6, 7, 5, 5, 6, 5, 6, 6, 5, 5, 4, 6, 5, 5, 4, 5, 5, 5, 5, 6, 5, 5, 6, 5, 5, 4, 4, 3, 5, 6, 5, 6, 4, 5, 5, 5, 5, 4, 5, 4, 5, 4, 3, 4, 4, 5, 3, 3, 3, 4, 5, 5, 4, 4, 5, 4, 4, 3, 3, 2, 2, 3, 3, 4, 4, 3, 2, 1, 4, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 2, 1, 1, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 1, 0, 2, 3, 4, 4, 4, 3, 3, 2, 1, 2, 4, 4, 5, 5, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 4, 4, 5, 4, 4, 5, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 4, 4, 4, 4, 3, 4, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 3, 4, 4, 3, 3, 4, 3, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 1, 3, 3, 2, 3, 4, 4, 4, 4, 5, 4, 3, 3, 4, 3, 2, 1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 3, 3, 2, 2, 2, 0, 1, 2, 3, 3, 2, 3, 2, 1, 1, 3, 3, 4, 4, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 1, 0, 1, 2, 3, 2, 2, 1, 2, 2, 4, 4, 5, 5, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 7, 6, 5, 4, 4, 5, 6, 6, 7, 6, 5, 6, 5, 6, 5, 4, 3, 5, 4, 3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 4, 4, 3, 4, 4, 4, 6, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 2, 3, 4, 2, 1, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 2, 1, 0, 1, 3, 2, 1, 2, 3, 3, 5, 5, 6, 6, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 6, 5, 5, 4, 3, 5, 6, 6, 7, 6, 5, 6, 5, 5, 4, 4, 3, 4, 3, 2, 3, 3, 5, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 3, 3, 4, 4, 4, 6, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 3, 2, 3, 1, 2, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 3, 2, 1, 0, 2, 1, 2, 2, 3, 3, 5, 5, 6, 6, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 7, 6, 5, 4, 4, 5, 6, 6, 7, 6, 5, 6, 5, 6, 5, 4, 3, 5, 4, 3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 3, 2, 3, 4, 4, 4, 6, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 3, 2, 1, 2, 3, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 4, 4, 3, 3, 3, 2, 0, 1, 2, 2, 3, 3, 5, 5, 6, 6, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 3, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 3, 2, 4, 3, 2, 3, 3, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 2, 2, 1, 2, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0, 1, 1, 2, 2, 4, 4, 5, 5, ], [7, 7, 6, 7, 6, 6, 6, 5, 6, 6, 5, 5, 4, 7, 6, 5, 4, 4, 5, 6, 6, 7, 6, 5, 6, 5, 6, 5, 4, 3, 5, 4, 3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 6, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 3, 3, 3, 2, 2, 2, 4, 4, 4, 5, 6, 6, 6, 6, 7, 6, 5, 5, 5, 4, 4, 3, 4, 5, 5, 6, 6, 6, 6, 6, 7, 5, 5, 4, 3, 3, 3, 2, 1, 2, 2, 1, 0, 1, 2, 3, 5, 5, 6, 6, ], [6, 6, 5, 6, 5, 5, 5, 4, 5, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 5, 5, 6, 5, 4, 5, 4, 5, 4, 3, 2, 4, 4, 3, 4, 3, 4, 4, 5, 5, 4, 4, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 3, 5, 4, 4, 4, 5, 4, 3, 2, 3, 3, 2, 2, 2, 3, 2, 2, 1, 3, 3, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 4, 3, 3, 2, 3, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 2, 2, 2, 1, 2, 2, 2, 1, 1, 0, 1, 2, 4, 4, 5, 5, ], [6, 7, 6, 7, 5, 5, 6, 5, 6, 6, 5, 5, 4, 7, 6, 5, 4, 5, 5, 5, 5, 6, 5, 5, 6, 5, 6, 5, 4, 3, 5, 5, 4, 5, 4, 5, 5, 5, 5, 4, 5, 4, 5, 5, 4, 4, 4, 5, 4, 4, 4, 4, 5, 5, 4, 4, 5, 4, 4, 3, 4, 3, 3, 3, 3, 4, 3, 3, 2, 2, 4, 3, 4, 5, 5, 5, 5, 6, 5, 4, 4, 5, 4, 3, 2, 2, 4, 4, 5, 5, 5, 5, 5, 6, 4, 4, 3, 1, 1, 1, 2, 3, 3, 3, 2, 2, 1, 0, 2, 4, 4, 5, 5, ], [4, 5, 4, 5, 3, 3, 4, 3, 4, 5, 4, 4, 3, 6, 5, 4, 3, 4, 4, 3, 3, 4, 3, 4, 5, 4, 5, 4, 3, 2, 4, 5, 4, 5, 3, 4, 4, 3, 3, 2, 3, 3, 4, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 2, 1, 2, 2, 1, 2, 3, 3, 3, 3, 4, 3, 2, 2, 3, 2, 1, 2, 1, 2, 2, 3, 3, 3, 3, 3, 4, 2, 2, 1, 1, 2, 1, 2, 3, 3, 3, 2, 3, 2, 2, 0, 2, 2, 3, 3, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 5, 5, 5, 6, 5, 5, 5, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 4, 3, 2, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 3, 4, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 0, 1, 2, 2, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 5, 5, 5, 6, 5, 5, 5, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 4, 4, 4, 5, 5, 4, 3, 4, 3, 2, 3, 4, 4, 4, 4, 3, 3, 2, 2, 3, 2, 3, 4, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 3, 4, 3, 4, 5, 5, 5, 4, 5, 4, 4, 2, 1, 0, 1, 1, ], [5, 6, 5, 6, 4, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 3, 3, 4, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 4, 4, 3, 2, 3, 3, 4, 3, 4, 5, 4, 3, 3, 2, 2, 2, 2, 2, 2, 1, 3, 2, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 2, 1, 0, 1, ], [5, 6, 5, 6, 3, 4, 5, 4, 5, 6, 5, 5, 4, 8, 7, 6, 5, 6, 5, 4, 4, 5, 4, 5, 6, 5, 6, 6, 5, 4, 6, 7, 6, 7, 5, 5, 5, 4, 4, 3, 4, 4, 5, 5, 6, 5, 6, 7, 6, 6, 6, 4, 4, 4, 3, 2, 3, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 5, 4, 5, 3, 2, 3, 4, 3, 3, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 3, 2, 4, 5, 4, 5, 6, 6, 6, 5, 6, 5, 5, 3, 2, 1, 1, 0, ], ]
		self.sel = list()
		self.exp = list()
		self.gen = list()
		
		self.goal = goal
		self.graph = model
		return

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
		self.source = init
		
		return []