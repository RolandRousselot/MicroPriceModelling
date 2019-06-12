# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 02:16:59 2019

@author: Roland
"""

###############################################################################
###############################################################################

def Single_Markov_Predictor():
    
    import numpy as np
    
    File_Name = 'Data/BAC/Labeled_BAC_2011-03/'
    Day_Number = 5
    I = 7
    S = 2
    Time = 1
    NNN3 = np.zeros((S*I, S*I, S*I, 3))
    NN = np.zeros((S*I, S*I, 1))
    
    for Day in range(Day_Number):
        
        print(Day)
        A, B = Extract_Data(Day, File_Name, I, S)
        
        NNN3 = NNN3 + A
        NN += NN + B
    
    Distribution, G = Obtain_Distribution(NNN3, NN, Time)
    
    return Distribution, G

###############################################################################
###############################################################################

def Extract_Data(Day, File_Name, I, S):
    
    import pandas as pd
    import numpy as np

    Times = pd.read_csv(File_Name + 'M_' + str(Day) + '.csv').values[:, [0]]
    Book = pd.read_csv(File_Name + 'O_' + str(Day) + '.csv').values
    
    Imbalances = Book[:, [3]]/(Book[:, [1]] + Book[:, [3]])
    Spreads = ((Book[:, [0]] - Book[:, [2]])/100).astype(int)
    Mid_Prices = Book[:, [0]] + Book[:, [2]]/2
    
    State_Info = np.concatenate((Spreads, Imbalances, Mid_Prices, Times), axis = 1)
    State_Info = State_Info[State_Info[:, 0] <= S]
    
    NNN3 = np.zeros((S*I, S*I, S*I, 3))
    NN = np.zeros((S*I, S*I, 1))
    
    for i in range(len(State_Info) - 2):
        
        T = State_Info[i + 2, 3] - State_Info[i + 1, 3]
        
        I_1 = State_Info[i, 1]
        FI_1 = State_Info[i + 1, 1]
        FFI_1 = State_Info[i + 2, 1]
        CS, FS, FFS = State_Info[i, 0], State_Info[i + 1, 0], State_Info[i + 2, 0]
        
        M_1 = State_Info[i + 2, 2] - State_Info[i + 1, 2]
        
        State_1 = Get_State(I_1, CS, I)
        FState_1 = Get_State(FI_1, FS, I)
        FFState_1 = Get_State(FFI_1, FFS, I) 
        
        State_2 = int(State_1/I)*I + ((I - 1) - (State_1 - int(State_1/I)*I))
        FState_2 = int(FState_1/I)*I + ((I - 1) - (FState_1 - int(FState_1/I)*I))
        FFState_2 = int(FFState_1/I)*I + ((I - 1) - (FFState_1 - int(FFState_1/I)*I))
        
        NN[State_1, FState_1, 0] += T
        NN[State_2, FState_2, 0] += T
        
        if M_1 == 0:
            
            NNN3[State_1, FState_1, FFState_1, 1] += 1
            NNN3[State_2, FState_2, FFState_2, 1] += 1
        
        if M_1 < 0:
            
            NNN3[State_1, FState_1, FFState_1, 0] += 1
            NNN3[State_2, FState_2, FFState_2, 2] += 1
        
        if M_1 > 0:
            
            NNN3[State_1, FState_1, FFState_1, 2] += 1
            NNN3[State_2, FState_2, FFState_2, 0] += 1
        
    return NNN3, NN

###############################################################################
###############################################################################

def Get_State(Imbalance, Spread, I):
    
    Spread_Component = (Spread - 1)*I
    Imbalance_Component = int(Imbalance*I)
    
    return int(Spread_Component + Imbalance_Component)

###############################################################################
###############################################################################

def Obtain_Distribution(NNN3, NN, Time):
    
    import numpy as np
    
    L = len(NN)
    Distribution = [[0 for i in range(L)] for i in range(L)]
    G = (NNN3)/(NN + 0.001)

    for i1 in range(L):
        
        for i2 in range(L):
            
            Final_Values = []
            
            for j in range(10000):
                
                t = 0
                State = [i1, i2]
                M_Delta = 0
                while t < Time:
                    
                    Outward_Intensity = np.sum(G, axis = (2, 3))[State[0], State[1]]
                    State[0] = State[1]
                    Step = np.random.exponential(1/Outward_Intensity)
                    if t + Step < Time:
                        P = G[State[0], State[1], :, :].reshape(3*L)
                        P = P/sum(P)
                        K = np.random.choice(list(range(3*L)), 1, p = P)[0]
                        State[1] = int(K/3)
                        M_Delta = M_Delta + (K - State[1]*3 - 1)*50
                    t = t + Step
                Final_Values.append(M_Delta)
            
            Distribution[i1][i2] = Final_Values
        
    return Distribution, G

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################