from black import GameState

def PrintState(state):
    print("First Card = %d \n Second Card = %d \n" % (state.FirstCard, state.SecondCard))

def CalculateHitValue(ValueDict, state, p):
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    
    HitValue = 0
    for card in cards:
        NewState = GameState(state.FirstCard + card, -1, state.OppCard, False, state.AcePresent)
        HitValue += ValueDict[NewState] * np
    
    # to handle face cards
    NewState = GameState(state.FirstCard + 10, -1, state.OppCard, False, state.AcePresent)
    HitValue += ValueDict[NewState] * p
    
    # to handle ace
    NewState = GameState(state.FirstCard + 1, -1, state.OppCard, False, True)
    HitValue += ValueDict[NewState] * np

    return HitValue

def CalculateDoubleValue(ValueDict, state, p):
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    
    DoubleValue = 0
    for card in cards:
        NewState = GameState(state.FirstCard + card, -1, state.OppCard, True)
        DoubleValue += 2 * GetStandValue(NewState) * np
    # to handle face cards
    NewState = GameState(state.FirstCard+10, -1, state.OppCard, False, state.AcePresent)
    DoubleValue += 2 * GetStandValue(NewState) * p
    # to handle ace
    NewState = GameState(state.FirstCard+1, -1, state.OppCard, False, True)
    DoubleValue += 2 * GetStandValue(NewState) * np

    return DoubleValue

def CalculateSplitValue(ValueDict, state, p):
    np = (1-p)/9.0
    cards = [2,3,4,5,6,7,8,9]
    
    SplitValue = 0
    for card in cards:
        if card != self.FirstCard:
            NewState = GameState(state.FirstCard + card, -1, state.OppCard, True)
            SplitValue += 2 * ValueDict[NewState] * np
        else:
            NewState = GameState(state.FirstCard, state.FirstCard, state.OppCard, False)
            SplitValue += 2 * ValueDict[NewState] * np
    # to handle face cards
    NewState = GameState(state.FirstCard+10, -1, state.OppCard, False, state.AcePresent)
    SplitValue += 2 * ValueDict[NewState] * p
    # to handle ace
    NewState = GameState(state.FirstCard+1, -1, state.OppCard, False, True)
    SplitValue += 2 * ValueDict[NewState] * np

    return SplitValue
