import pdb
import time
import sys

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

    def printme(self):
        print("State (Type: %s, Value: %d, OppCard: %d) : " % (self.HandType, self.Value, self.OppCard), end='')


# maps states to float values
def InitializeValueDict():
    ValueDict = {}
    StateSet = []
    for summ in range(2,22):
        for opp in range(1,11):
            StateSet.append(GameState("HardFresh", summ, opp))
            StateSet.append(GameState("HardStaleAce", summ, opp))
            StateSet.append(GameState("HardStale", summ, opp))
    for summ in range(2,11):
        for opp in range(1,11):
            StateSet.append(GameState("AceFresh", summ, opp))
    for summ in range(1,11):
        for opp in range(1,11):
            StateSet.append(GameState("Pair", summ, opp))
    for state in StateSet:
        ValueDict[state] = 0
    return ValueDict


def PerformValueIteration( ValueActionDict, ValueDict, p):
    for state in ValueDict.keys():
        if state.HandType == "HardFresh":
            PerformValueIterationHardFresh(ValueActionDict, ValueDict, state, p)
        elif state.HandType == "HardStale":
            PerformValueIterationHardStale(ValueActionDict, ValueDict, state, p)
        elif state.HandType == "Pair":
            PerformValueIterationPair(ValueActionDict, ValueDict, state, p)
        elif state.HandType == "AceFresh":
            PerformValueIterationAceFresh(ValueActionDict, ValueDict, state, p)
        else:
            PerformValueIterationHardStaleAce(ValueActionDict, ValueDict, state, p)

def IsPolicySame( OldValueDict, NewValueDict):
    epsilon = 1e-11
    for state in OldValueDict:
        if abs(OldValueDict[state] - NewValueDict[state]) > epsilon:
            #print("Returning false")
            return False
    return True

def GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh):
    
    if acefresh and (MyHandValue==11):
        if (NumDealerCards==2) and DealerHasAce and (DealerHandValue==11):
            return 0
        else:
            return 1.5
    if WeHaveAce:
        if MyHandValue+10 <= 21:
            MyHandValue = MyHandValue + 10
    if DealerHasAce:
        if DealerHandValue+10 <= 21:
            DealerHandValue = DealerHandValue + 10
    if MyHandValue > 21:
        return -1
    if DealerHandValue > 21:
        return 1
    if DealerHandValue > MyHandValue:
        return -1
    if MyHandValue > DealerHandValue:
        return 1
    if (NumDealerCards==2) and DealerHasAce and (DealerHandValue==21):
        return -1
    if DealerHandValue == MyHandValue:
        return 0
    else:
        print("Damn")
        return 0



def GetStandValueHardStale(p, MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards = 1, acefresh = False): # both values count aces as 1
    # base case - dealer stands

    if DealerHasAce:
        if (DealerHandValue + 10 >= 17 and DealerHandValue + 10 <= 21):
            return GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh)
        elif DealerHandValue >= 17:
            return GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh)
    else:
        if (DealerHandValue >= 17):
            return GetFinalPayoff(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh)

    if (MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh) in MemoizationDict:
        return MemoizationDict[(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh)]

    #deal more (hit)
    np = (1-p)/9.0
    TotalReward = 0
    for DealerCard in range(2,10): # no ace
        TotalReward += np * GetStandValueHardStale(p, MyHandValue, WeHaveAce, DealerHandValue + DealerCard, DealerHasAce, NumDealerCards = NumDealerCards + 1, acefresh = acefresh)
    TotalReward += p * GetStandValueHardStale(p, MyHandValue, WeHaveAce, DealerHandValue + 10, DealerHasAce, NumDealerCards = NumDealerCards + 1, acefresh = acefresh)
    # Dealer Ace
    TotalReward += np * GetStandValueHardStale(p, MyHandValue, WeHaveAce, DealerHandValue + 1, True, NumDealerCards = NumDealerCards + 1, acefresh = acefresh)

    MemoizationDict[(MyHandValue, WeHaveAce, DealerHandValue, DealerHasAce, NumDealerCards, acefresh)] = TotalReward
    return TotalReward

def GetStandValue(state, p):
    # handle ace
    # First convert the state to the form where only the total, ace presence and freshness matters

    if state.HandType == "HardStaleAce":
        if state.OppCard == 1:
            ret = GetStandValueHardStale(p, state.Value, True, state.OppCard, True)
        else:
            ret = GetStandValueHardStale(p, state.Value, True, state.OppCard, False)
    elif state.HandType == "AceFresh":
        if state.OppCard == 1:
            ret = GetStandValueHardStale(p, state.Value+1, True, state.OppCard, True, acefresh = True)
        else:
            ret = GetStandValueHardStale(p, state.Value+1, True, state.OppCard, False, acefresh = True)
    else:
        if state.OppCard == 1:
            ret = GetStandValueHardStale(p, state.Value, False, state.OppCard, True)
        else:
            ret = GetStandValueHardStale(p, state.Value, False, state.OppCard, False)

    # print("Returning ", ret)
    return ret

def ReferenceValueDict(ValueDict, state):
    if state.Value > 21:
        return -1
    elif state not in ValueDict:
        print("Logical Error: State (Type: %s, Value: %d, OppCard: %d)not in dict" % (state.HandType, state.Value, state.OppCard))
        return 0
    else:
        return ValueDict[state]

def PerformValueIterationHardFresh(ValueActionDict, ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    # print("HardFresh")
    # state.printme()

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
    state_temp = GameState("HardStale", state.Value, state.OppCard)
    StandValue = GetStandValue(state_temp, p)
    

    # for action Double
    DoubleValue = 0
    for card in cards:
        NewState = GameState("HardStale", state.Value + card, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * np
    # to handle face cards
    NewState = GameState("HardStale", state.Value + 10, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState, p) * p
    # to handle ace
    NewState = GameState("HardStaleAce", state.Value + 1, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState, p) * np
    
    ValueDict[state] = max(HitValue, StandValue, DoubleValue)
    if ValueDict[state] == HitValue:
        ValueActionDict[state] = "H"
    elif ValueDict[state] == StandValue:
        ValueActionDict[state] = "S"
    else:
        ValueActionDict[state] = "D"

def PerformValueIterationHardStale(ValueActionDict, ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    # print("HardStale")
    # state.printme()

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
    StandValue = GetStandValue(state, p)
    
    ValueDict[state] = max(HitValue, StandValue)
    if ValueDict[state] == HitValue:
        ValueActionDict[state] = "H"
    elif ValueDict[state] == StandValue:
        ValueActionDict[state] = "S"

def PerformValueIterationPair(ValueActionDict, ValueDict, state, p):
    # TODO: Handle Ace pair
    ActionList = ["Hit","Stand","Double","Split"]
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    # print("Pair")
    # state.printme()

    if(state.Value != 1):
        
        # for action Hit 
        HitValue = 0
        for card in cards:
            NewState = GameState("HardStale", 2 * state.Value + card, state.OppCard)
            HitValue += ReferenceValueDict(ValueDict, NewState) * np
        # to handle face cards
        NewState = GameState("HardStale", 2 * state.Value + 10, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value + 1, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
        
        
        # for action Stand
        state_temp = GameState("HardStale", 2 * state.Value, state.OppCard)
        StandValue = GetStandValue(state_temp, p)


        # for action Double
        DoubleValue = 0
        for card in cards:
            NewState = GameState("HardStale", 2 * state.Value + card, state.OppCard)
            DoubleValue += 2 * GetStandValue(NewState, p) * np
        # to handle face cards
        NewState = GameState("HardStale", 2 * state.Value + 10, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value + 1, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * np
        
        
        SplitValue = 0
        for card in cards:
            if card != state.Value:
                NewState = GameState("HardFresh", state.Value + card, state.OppCard)
                SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np
            else:
                NewState = GameState("Pair", state.Value, state.OppCard)
                SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np
        # to handle face cards
        NewState = GameState("HardFresh", state.Value + 10, state.OppCard)
        SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * p
        # to handle ace
        NewState = GameState("AceFresh", state.Value, state.OppCard)
        SplitValue += 2 * ReferenceValueDict(ValueDict, NewState) * np

        ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)
        if ValueDict[state] == HitValue:
            ValueActionDict[state] = "H"
        elif ValueDict[state] == StandValue:
            ValueActionDict[state] = "S"
        elif ValueDict[state] == DoubleValue:
            ValueActionDict[state] = "D"
        else:
            ValueActionDict[state] = "P"

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
        NewState = GameState("HardStaleAce", 2 * state.Value + 1, state.OppCard)
        HitValue += ReferenceValueDict(ValueDict, NewState) * np
        
        
        # for action Stand
        state_temp = GameState("HardStaleAce", 2 * state.Value, state.OppCard)
        StandValue = GetStandValue(state_temp, p)


        # for action Double
        DoubleValue = 0
        for card in cards:
            NewState = GameState("HardStaleAce", 2 * state.Value + card, state.OppCard)
            DoubleValue += 2 * GetStandValue(NewState, p) * np
        # to handle face cards
        NewState = GameState("HardStaleAce", 2 * state.Value + 10, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value + 1, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * np
        
        
        # for action split
        SplitValue = 0
        for card in cards:
            NewState = GameState("HardStaleAce", state.Value + card, state.OppCard)
            SplitValue += 2 * GetStandValue(NewState, p) * np
        # to handle face cards
        NewState = GameState("HardStaleAce", state.Value + 10, state.OppCard)
        SplitValue += 2 * GetStandValue(NewState, p) * p
        # to handle ace
        NewState = GameState("HardStaleAce", 2 * state.Value, state.OppCard)
        SplitValue += 2 * GetStandValue(NewState, p) * np

        
        ValueDict[state] = max(HitValue, StandValue, DoubleValue, SplitValue)
        if ValueDict[state] == HitValue:
            ValueActionDict[state] = "H"
        elif ValueDict[state] == StandValue:
            ValueActionDict[state] = "S"
        elif ValueDict[state] == DoubleValue:
            ValueActionDict[state] = "D"
        else:
            ValueActionDict[state] = "P"

def PerformValueIterationAceFresh(ValueActionDict, ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    # print("AceFresh")
    # state.printme()

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
    StandValue = GetStandValue(state, p)
    

    # for action Double
    DoubleValue = 0
    for card in cards:
        NewState = GameState("HardStaleAce", 1 + state.Value + card, state.OppCard)
        DoubleValue += 2 * GetStandValue(NewState, p) * np
    # to handle face cards
    NewState = GameState("HardStaleAce", 1 + state.Value + 10, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState, p) * p
    # to handle ace
    NewState = GameState("HardStaleAce", 1 + state.Value + 1, state.OppCard)
    DoubleValue += 2 * GetStandValue(NewState, p) * np

    ValueDict[state] = max(HitValue, StandValue, DoubleValue)
    if ValueDict[state] == HitValue:
        ValueActionDict[state] = "H"
    elif ValueDict[state] == StandValue:
        ValueActionDict[state] = "S"
    elif ValueDict[state] == DoubleValue:
        ValueActionDict[state] = "D"

def PerformValueIterationHardStaleAce(ValueActionDict, ValueDict, state, p):
    # [ "HardFresh", "HardStaleAce", "HardStale", "AceFresh", "Pair" ] 
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    # print("HardStaleAce")
    # state.printme()

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
    StandValue = GetStandValue(state, p)

    ValueDict[state] = max(HitValue, StandValue)
    if ValueDict[state] == HitValue:
        ValueActionDict[state] = "H"
    elif ValueDict[state] == StandValue:
        ValueActionDict[state] = "S"

if __name__ == '__main__':
    MemoizationDict = {}
    ValueDict = InitializeValueDict()
    ValueActionDict = InitializeValueDict()
    p = float(sys.argv[1])
    iteration = 0
    while True:
        NewValueDict = ValueDict.copy()
        NewValueActionDict = ValueActionDict.copy()
        # print("Iteration ", iteration)
        iteration += 1
        PerformValueIteration(ValueActionDict, NewValueDict, p)
        # print(NewValueDict.values())
        # print(ValueDict.values())
        if IsPolicySame(ValueDict, NewValueDict):
            break
        ValueDict = NewValueDict
        ValueActionDict = NewValueActionDict
    
    for summ in range(5,20):
        print(summ, "\t", end="",sep="")
        for opp in range(2,11):
            state = GameState("HardFresh", summ, opp)
            print(ValueActionDict[state]," ",end='',sep="")
        state = GameState("HardFresh", summ, 1)
        print(ValueActionDict[state])
    for summ in range(2,10):
        print("A%d\t" %(summ), end='')
        for opp in range(2,11):
            state = GameState("AceFresh", summ, opp)
            print(ValueActionDict[state]," ",end='',sep="")
        state = GameState("AceFresh", summ, 1)
        print(ValueActionDict[state])
    for summ in range(2,11):
        print("%d%d\t" %(summ,summ), end='')
        for opp in range(2,11):
            state = GameState("Pair", summ, opp)
            print(ValueActionDict[state]," ",end='',sep="")
        state = GameState("Pair", summ, 1)
        print(ValueActionDict[state])
    print("AA\t" , end='')
    for opp in range(2,11):
        state = GameState("Pair", 1, opp)
        print(ValueActionDict[state]," ",end='',sep="")
    state = GameState("Pair", 1, 1)
    print(ValueActionDict[state],end="")

    # for state in StateSet:
    #     ValueDict[state] = 0

    # for state in ValueDict:
    #     state.printme()
    #     print(ValueActionDict[state])
    # print("MemoizationDict\n",MemoizationDict.values())
