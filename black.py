import random


class GameState:
	"""

	Blackjack Game state

	"""

	def __init__(self, FirstCard, SecondCard, OppCard):
		pass


ActionList = ["Hit","Stand","Double","Split"]

# ValueDict = {}
# maps states to float values

#p = 4/13

def InitializeValueDict():
	pass

def PerformValueIteration( ValueDict ):
	for state in ValueDict.keys():
		if state.type == "Hard":
			PerformValueIterationHard(ValueDict, state, p)
		elif state.type == "Soft":
			PerformValueIterationSoft(ValueDict, state, p)
		else:
			PerformValueIterationPair(ValueDict, state, p)
def IsPolicySame( OldValueDict, NewValueDict):
	pass
def main():
	ValueDict = InitializeValueDict()
	p = 4/13
	while True:
		NewValueDict = ValueDict.copy()
		PerformValueIteration(NewValueDict, p)
		if IsPolicySame(ValueDict, NewValueDict):
			break
		ValueDict = NewValueDict
