from Util import *
import pdb


class GameState:
    """

    Blackjack Game state

    """

    def __init__(self, FirstCard, SecondCard, OppCard, FreshHand, AcePresent):
        
        # if you add other members add them to the hash and eq as well
        self.OppCard = OppCard
        self.FirstCard = FirstCard
        self.SecondCard = SecondCard
        self.FreshHand = FreshHand
        self.AcePresent = AcePresent


    def __hash__(self):
            return hash((self.OppCard,
                        self.FirstCard,
                        self.SecondCard,
                        self.FreshHand,
                        self.AcePresent))

    def __eq__(self, other):
        return (self.OppCard,
                self.FirstCard,
                self.SecondCard,
                self.FreshHand,
                self.AcePresent) == (other.OppCard,
                                    other.FirstCard,
                                    other.SecondCard,
                                    other.FreshHand,
                                    other.AcePresent)


# maps states to float values
def InitializeValueDict():
    # TODO: Please finish this and the function GetStandValue
    ValueDict = {}
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
    epsilon = 0.0001
    for state in OldValueDict:
        if (OldValueDict[state] - NewValueDict) > epsilon:
            return False
    return True


def GetStandValue(state):
    # handle ace
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

    # for action Hit
    HitValue = CalculateHitValue(ValueDict, state, p)
    
    # for action Stand
    StandValue = GetStandValue(state)

    # for action Double
    DoubleValue = 0
    if state.FreshHand:
        DoubleValue = CalculateDoubleValue(ValueDict, state, p)
    
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
