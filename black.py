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
    # TODO: Please finish this and the function GetStandValue
    ValueDict = {}
    StateSet = set()
    for summ in range(5,20):
        StateSet.insert()
    state = GameState(4,-1,2,True,False)
    ValueDict[state] = 1
    return ValueDict

def PerformValueIteration( ValueDict, p):
    for state in ValueDict.keys():
        if state.HandType == "HardFresh":
            PerformValueIterationHardFresh(ValueDict, state, p)
        elif state.HandType == "HardStale":
            PerformValueIterationHardStale(ValueDict, state, p)
        elif state.HandType == "Pair":
            PerformValueIterationPair(ValueDict, state, p)
        elif state.HandType == "AceFresh":
            PerformValueIterationAceFresh(ValueDict, state, p)
        else:
            PerformValueIterationHardStaleAce(ValueDict, state, p)

def IsPolicySame( OldValueDict, NewValueDict):
    epsilon = 0.0001
    for state in OldValueDict:
        if (OldValueDict[state] - NewValueDict[state]) > epsilon:
            return False
    return True


def GetStandValue(state):
    # handle ace
    # First convert the state to the form where only the total, ace presence and freshness matters
    if state.OppCard == 11:
        return 1
    else:
        return 0

def PerformValueIterationHardFresh(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    HitValue += ValueDict[NewState] * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ValueDict[NewState] * np



    # for action Stand
    StandValue = GetStandValue(state)
    
    

    # for action Double
    DoubleValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.FirstCard + 1, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState) * np

    
    ValueDict[state] = max(HitValue, StandValue, DoubleValue)

def PerformValueIterationHardStale(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    HitValue += ValueDict[NewState] * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ValueDict[NewState] * np



    # for action Stand
    StandValue = GetStandValue(state)
    
    ValueDict[state] = max(HitValue, StandValue)

def PerformValueIterationPair(ValueDict, state, p):
    # TODO: Handle Ace pair
    ActionList = ["Hit","Stand","Double","Split"]
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]

    if(state.Value != 1):
        
        # for action Hit 
        HitValue = 0
        for card in cards:
            NewState = GameState("HardStale", state.Value + card, state.OppCard)
            HitValue += ValueDict[NewState] * np
        # to handle face cards
        NewState = GameState("HardStale", state.Value + 10, state.OppCard)
        HitValue += ValueDict[NewState] * p
        # to handle ace
        NewState = GameState("HardStaleAce", state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
        
        
        # for action Stand
        StandValue = GetStandValue(state_hard)


        # for action Double
        DoubleValue = 0
        for card in cards:
            NewState = GameState("HardStale", 2 * state.Value + card, state.OppCard)
            DoubleValue += 2 * GetStandValue(NewState) * np
        # to handle face cards
        NewState = GameState("HardStale", 2 * state.Value + 10, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.FirstCard + 1, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * np
        
        
        SplitValue = 0
        for card in cards:
            if card != self.Value:
                NewState = GameState("HardFresh", state.Value + card, state.OppCard)
                SplitValue += 2 * ValueDict[NewState] * np
            else:
                NewState = GameState("Pair", state.Value, state.OppCard)
                SplitValue += 2 * ValueDict[NewState] * np
        
        # to handle face cards
        NewState = GameState("HardFresh", state.Value + 10, state.OppCard)
        SplitValue += 2 * ValueDict[NewState] * p
        # to handle ace
        NewState = GameState("FreshAce", state.Value, state.OppCard)
        SplitValue += 2 * ValueDict[NewState] * np

        ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)
    else:
        
        # for action Hit
        HitValue = 0
        for card in cards:
            NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
            HitValue += ValueDict[NewState] * np
        # to handle face cards
        NewState = GameState("HardStaleAce", 2 * state.Value + 10, state.OppCard)
        HitValue += ValueDict[NewState] * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
        
        
        # for action Stand
        StandValue = GetStandValue(state_hard)


        # for action Double
        DoubleValue = 0
        for card in cards:
            NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
            DoubleValue += 2 * GetStandValue(NewState) * np
        # to handle face cards
        NewState = GameState("HardStaleAce", 2 * state.Value + 10, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.FirstCard + 1, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * np
        
        
        # for action split
        SplitValue = 0
        for card in cards:
            NewState = GameState("FreshAce", card, state.OppCard)
            SplitValue += 2 * GetStandValue(NewState) * np
        
        # to handle face cards
        NewState = GameState("FreshAce", 10, state.OppCard)
        SplitValue += 2 * GetStandValue(NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.FirstCard, state.OppCard)
        SplitValue += 2 * GetStandValue(NewState) * np

        
        ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)

def PerformValueIterationAceFresh(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", 1 + state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
    # to handle face cards
    NewState = GameState("HardStaleAce", 1 + state.Value + 10, state.OppCard)
    HitValue += ValueDict[NewState] * p
    # to handle ace
    NewState = GameState("HardStaleAce", 1 + state.Value + 1, state.OppCard)
    HitValue += ValueDict[NewState] * np


    # for action Stand
    StandValue = GetStandValue(state)
    

    # for action Double
    DoubleValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", 1 + state.Value + card, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState) * np
    # to handle face cards
    NewState = GameState("HardStaleAce", 1 + state.Value + 10, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", 1 + state.FirstCard + 1, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState) * np

    
    ValueDict[state] = max(HitValue, StandValue, DoubleValue)

def PerformValueIterationHardStaleAce(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", state.Value + card, state.OppCard)
        HitValue += ValueDict[NewState] * np
    # to handle face cards
    NewState = GameState("HardStaleAce", state.Value + 10, state.OppCard)
    HitValue += ValueDict[NewState] * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ValueDict[NewState] * np


    # for action Stand
    StandValue = GetStandValue(state)

    ValueDict[state] = max(HitValue, StandValue)


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
