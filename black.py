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
    for summ in range(5,22):
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
    print("Iteration 1")
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
    epsilon = 0.00001
    for state in OldValueDict:
        if (OldValueDict[state] - NewValueDict[state]) > epsilon:
            return False
    return True

def GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards):
    if WeHaveAce:
        if MyHandValue+10 <= 21:
            MyHandValue = MyHandValue + 10
    if DealerHasAce:
        if DealerHandValue+10 <= 21:
            DealerHandValue = DealerHandValue + 10
    if MyHandValue > 21:
        return 0
    if DealerHandValue > 21:
        return 2
    if DealerHandValue > MyHandValue:
        return 0
    if MyHandValue > DealerHandValue:
        return 2
    if (NumDealerCards==2) and DealerHasAce and (DealerHandValue==11) and MyHandValue==21:
        return 0
    else:
        return 1

def GetStandValueHardStale(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards = 1): # both values count aces as 1
    # base case - dealer stands
    if DealerHasAce:
        if (DealerHandValue+10>=17):
            return GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards)
    else:
        if (DealerHandValue>=17):
            return GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards)

    #deal more (hit)
    TotalReward = 0
    NumberAdded = 11
    for DealerCard in range(1,11): # no ace
            TotalReward += GetStandValueHardStale(MyHandValue, WeHaveAce, DealerHandValue + DealerCard, DealerHasAce, NumDealerCards = NumDealerCards + 1)
    # Dealer Ace
    TotalReward += GetStandValueHardStale(MyHandValue, WeHaveAce, DealerHandValue + 1, True, NumDealerCards = NumDealerCards + 1)
    return (TotalReward/NumberAdded)

def GetStandValue(state):
    # handle ace
    # First convert the state to the form where only the total, ace presence and freshness matters
    if state.HandType == "HardStaleAce":
        if state.OppCard == 11:
            return GetStandValueHardStale(state.Value, True, state.OppCard, True)
        else:
            return GetStandValueHardStale(state.Value, True, state.OppCard, False)
    else:
        if state.OppCard == 11:
            return GetStandValueHardStale(state.Value, False, state.OppCard, True)
        else:
            return GetStandValueHardStale(state.Value, False, state.OppCard, False)

def ReferenceValueDict(ValueDict, state):
    if state.Value > 21:
        return 0
    elif state not in ValueDict:
        print("Logical Error: State (Type: %s, Value: %d, OppCard: %d)not in dict" % (state.HandType, state.Value, state.OppCard))
        return 0
    else:
        return ValueDict[state]

def PerformValueIterationHardFresh(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    print("HardFresh")

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * np



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
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState) * np

    
    ValueDict[state] = max(HitValue, StandValue, DoubleValue)

def PerformValueIterationHardStale(ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    print("HardStale")

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * np



    # for action Stand
    StandValue = GetStandValue(state)
    
    ValueDict[state] = max(HitValue, StandValue)

def PerformValueIterationPair(ValueDict, state, p):
    # TODO: Handle Ace pair
    ActionList = ["Hit","Stand","Double","Split"]
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    print("Pair")

    if(state.Value != 1):
        
        # for action Hit 
        HitValue = 0
        for card in cards:
            NewState = GameState("HardStale", state.Value + card, state.OppCard)
            HitValue += ReferenceValueDict(ValueDict, NewState) * np
        # to handle face cards
        NewState = GameState("HardStale", state.Value + 10, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
        
        
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
                SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np
            else:
                NewState = GameState("Pair", state.Value, state.OppCard)
                SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np
        
        # to handle face cards
        NewState = GameState("HardFresh", state.Value + 10, state.OppCard)
        SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * p
        # to handle ace
        NewState = GameState("FreshAce", state.Value, state.OppCard)
        SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np

        ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)
    else:
        
        # for action Hit
        HitValue = 0
        for card in cards:
            NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
            HitValue += ReferenceValueDict(ValueDict, NewState) * np
        # to handle face cards
        NewState = GameState("HardStaleAce", 2 * state.Value + 10, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
        
        
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
    print("AceFresh")

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", 1 + state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
    # to handle face cards
    NewState = GameState("HardStaleAce", 1 + state.Value + 10, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", 1 + state.Value + 1, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * np


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
    print("HardStaleAce")

    # for action Hit    
    HitValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", state.Value + card, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
    # to handle face cards
    NewState = GameState("HardStaleAce", state.Value + 10, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    HitValue += ReferenceValueDict(ValueDict, NewState) * np


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
