# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 00:58:33 2019

@author: Roland
"""

###############################################################################
###############################################################################

def Empirical_Data():
    
    T = 50
    File_Name = 'Data/CVX/Labeled_CVX_2011-03/'
    Day_Number = 23
    I = 7
    S = 4
    
    Storage = [[0, 0] for i in range((S*I))]
    
    for Day in range(Day_Number):
        
        print(Day)
        
        Storage = Get_State_Contribution(File_Name, Day, T, I, S, Storage)
        
    Averages = [i[0]/i[1] for i in Storage]
    
    return Averages

###############################################################################
###############################################################################

def Get_State_Contribution(File_Name, Day, T, I, S, Storage):
    
    import pandas as pd
    import numpy as np

    Book = pd.read_csv(File_Name + 'O_' + str(Day) + '.csv').values
    
    Imbalances = Book[:, [3]]/(Book[:, [1]] + Book[:, [3]])
    Spreads = ((Book[:, [0]] - Book[:, [2]])/100).astype(int)
    Mid_Prices = Book[:, [0]] + Book[:, [2]]/2
    
    State_Info = np.concatenate((Spreads, Imbalances, Mid_Prices), axis = 1)
    State_Info = State_Info[State_Info[:, 0] <= S]
    
    for i in range(len(State_Info) - T):
        
        I_1 = State_Info[i, 1]
        CS = State_Info[i, 0]
        
        M_1 = State_Info[i + T, 2] - State_Info[i, 2]
        M_2 = -M_1
        
        State_1 = Get_State(I_1, CS, I)
        State_2 = int(State_1/I)*I + ((I - 1) - (State_1 - int(State_1/I)*I))

        Storage[State_1][0] = Storage[State_1][0] + M_1
        Storage[State_1][1] = Storage[State_1][1] + 1
        Storage[State_2][0] = Storage[State_2][0] + M_2
        Storage[State_2][1] = Storage[State_2][1] + 1
    
    return Storage

###############################################################################
###############################################################################

def Get_State(Imbalance, Spread, I):
    
    Spread_Component = (Spread - 1)*I
    Imbalance_Component = int(Imbalance*I)
    
    return int(Spread_Component + Imbalance_Component)

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################