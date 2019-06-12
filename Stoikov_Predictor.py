# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 00:01:59 2019

@author: Roland
"""

###############################################################################
###############################################################################

def Stoikov_Predictor():
    
    import numpy as np
    
    File_Name = 'Data/CVX/Labeled_CVX_2011-03/'
    Day_Number = 23
    I = 7
    S = 4
    NN = np.zeros((S*I, S*I))
    _NN_ = np.zeros((S*I, S*I))
    N2 = np.zeros((S*I, 2))
    N = np.zeros((S*I, 1))
    
    for Day in range(Day_Number):
        
        print(Day)
        A, B, C, D = Extract_Data(Day, File_Name, I, S)
        
        NN += A
        _NN_ += B
        N2 += C
        N += D
    
    R, Q, T, K = Obtain_Matrices(NN, _NN_, N2, N)
    
    print(R)
    print(Q)
    print(T)
    
    Adjustments = Obtain_Adjustments(R, Q, T, K)
    
    return Adjustments, R, Q, T, NN, _NN_, N2, N

###############################################################################
###############################################################################

def Extract_Data(Day, File_Name, I, S):
    
    import pandas as pd
    import numpy as np

    Book = pd.read_csv(File_Name + 'O_' + str(Day) + '.csv').values
    
    Imbalances = Book[:, [3]]/(Book[:, [1]] + Book[:, [3]])
    Spreads = ((Book[:, [0]] - Book[:, [2]])/100).astype(int)
    Mid_Prices = Book[:, [0]] + Book[:, [2]]/2
    
    State_Info = np.concatenate((Spreads, Imbalances, Mid_Prices), axis = 1)
    State_Info = State_Info[State_Info[:, 0] <= S]
    
    NN = np.zeros((S*I, S*I))
    _NN_ = np.zeros((S*I, S*I))
    N2 = np.zeros((S*I, 2))
    N = np.zeros((S*I, 1))
    
    for i in range(len(State_Info) - 1):
        
        I_1 = State_Info[i, 1]
        FI_1 = State_Info[i + 1, 1]
        CS, FS = State_Info[i, 0], State_Info[i + 1, 0]
        
        M_1 = State_Info[i + 1, 2] - State_Info[i, 2]
        
        State_1 = Get_State(I_1, CS, I)
        FState_1 = Get_State(FI_1, FS, I)
        
        State_2 = int(State_1/I)*I + ((I - 1) - (State_1 - int(State_1/I)*I))
        FState_2 = int(FState_1/I)*I + ((I - 1) - (FState_1 - int(FState_1/I)*I))
        
        N[State_1, 0] += 1
        N[State_2, 0] += 1
        
        if M_1 == 0:
            
            NN[State_1, FState_1] += 1
            NN[State_2, FState_2] += 1
        
        if M_1 < 0:
            
            N2[State_1, 0] += 1
            N2[State_2, 1] += 1
            _NN_[State_1, FState_1] +=1
            _NN_[State_2, FState_2] +=1
        
        if M_1 > 0:
            
            N2[State_1, 1] += 1
            N2[State_2, 0] += 1
            _NN_[State_1, FState_1] +=1
            _NN_[State_2, FState_2] +=1
        
    return NN, _NN_, N2, N

###############################################################################
###############################################################################

def Get_State(Imbalance, Spread, I):
    
    Spread_Component = (Spread - 1)*I
    Imbalance_Component = int(Imbalance*I)
    
    return int(Spread_Component + Imbalance_Component)

###############################################################################
###############################################################################

def Obtain_Matrices(NN, _NN_, N2, N):
    
    import numpy as np
    
    R = N2/N
    Q = NN/N
    T = _NN_/N
    K = np.array([[-50, 50]]).T
    
    return R, Q, T, K

###############################################################################
###############################################################################

def Obtain_Adjustments(R, Q, T, K):
    
    import numpy as np
    
    G = np.matmul(np.linalg.inv(np.identity(len(Q)) - Q), np.matmul(R, K))
    B = np.matmul(np.linalg.inv(np.identity(len(Q)) - Q), T)
    
    Adjustments = Power_Series(B, G)
    
    return Adjustments

###############################################################################
###############################################################################

def Power_Series(B, G):
    
    import numpy as np
    
    N = 100
    print(G)
    Value = G
    
    for i in range(1, N):
        
        Value = Value + np.matmul(np.linalg.matrix_power(B, i), G)
        
    print(np.matmul(np.linalg.matrix_power(B, 100), G))
    print(G)
    print(np.linalg.matrix_power(B, 100))
    
    return Value

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################