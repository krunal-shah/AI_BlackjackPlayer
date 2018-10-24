from Util import *
import pdb


class GameState:
    """

    Blackjack Game state

    """

    def __init__(self, HandType, Value, OppCard):
        
        # if you add other members add them to the hash and eq as well
        self.HandType = HandType
        # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
        self.OppCard = OppCard
        self.Value = Value

    def __hash__(self):
        return hash((self.OppCard,
                        self.Value,
                        self.HandType))

    def __eq__(self, other):
        return (self.OppCard,
                self.Value,
                self.HandType) == (other.OppCard,
                                    other.Value,
                                    other.HandType)


# maps states to float values
def InitializeValueDict():
    ValueDict = {}
    StateSet = []
    for summ in range(5,20):
        for opp in range(2,12):
            StateSet.append(GameState("HardFresh", summ, opp))
            StateSet.append(GameState("HardStaleAce", summ, opp))
            StateSet.append(GameState("HardStale", summ, opp))
    for summ in range(2,10):
        for opp in range(2,12):
            StateSet.append(GameState("AceFresh", summ, opp))
    for summ in range(2,12):
        for opp in range(2,12):
            StateSet.append(GameState("Pair", summ, opp))
    for state in StateSet:
        ValueDict[state] = 0
    return ValueDict


def PerformValueIteration( ValueDict, p):
    for state in ValueDict.keys():
        if state.SecondCard == -1:
            PerformValueIterationHard(ValueDict, state, p)
        elif state.FirstCard == state.SecondCard:
            PerformValueIterationPair(ValueDict, state, p)
        else:
            PerformValueIterationSoft(ValueDict, state, p)

def IsPolicySame( OldValueDict, NewValueDict):
    epsilon = 0.00001
    for state in OldValueDict:
        if (OldValueDict[state] - NewValueDict) > epsilon:
            return False
    return True


def GetStandValue(state):
    # handle ace
    # First convert the state to the form where only the total, ace presence and freshness matters
    if state.OppCard == 11:
        return 1
    else:
        return 0

def PerformValueIterationHard(ValueDict, state, p):
    ActionList = ["Hit","Stand","Double","Split"]

    # for action Hit
    HitValue = CalculateHitValue(ValueDict, state, p)

    # for action Stand
    StandValue = GetStandValue(state)
    
    # for action Double
    DoubleValue = 0
    if state.FreshHand:
        DoubleValue = CalculateDoubleValue(ValueDict, state, p)

    ValueDict[state] = max(HitValue, StandValue, DoubleValue)

def PerformValueIterationPair(ValueDict, state, p):
    # TODO: Handle Ace pair
    ActionList = ["Hit","Stand","Double","Split"]

    state_hard = ConvertPairToHard(state)
    # for action Hit
    HitValue = CalculateHitValue(ValueDict, state_hard, p)
    
    # for action Stand
    StandValue = GetStandValue(state_hard)

    # for action Double
    DoubleValue = 0
    if state.FreshHand:
        DoubleValue = CalculateDoubleValue(ValueDict, state_hard, p)
    
    # for action Split (TODO: Handle ace pair)
    SplitValue = CalculateSplitValue(ValueDict, state, p)

    ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)


if __name__ == '__main__':
    ValueDict = InitializeValueDict()
    p = 4/13
    while True:
        NewValueDict = ValueDict.copy()
        PerformValueIteration(NewValueDict, p)
        break
        if IsPolicySame(ValueDict, NewValueDict):
            break
        ValueDict = NewValueDict
