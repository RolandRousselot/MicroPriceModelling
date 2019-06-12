# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 20:01:04 2019

@author: Roland
"""

def Spread_Distribution():
    
    import matplotlib.pyplot as plt
    
    T = 5
    
    File_Name = 'Data/BAC/Labeled_BAC_2011-03/'
    Day_Number = 23

    MD = []
    
    for Day in range(Day_Number):
        
        print(Day)
        
        MD_Contribution = Get_MD_Contribution(File_Name, Day, T)
        [MD.append(i) for i in MD_Contribution]
    
    
    A = sorted(set(MD))
    print(A)
    B = [MD.count(i) for i in A]
    print(B)
    
    plt.hist(MD, bins = 70)
###############################################################################
###############################################################################

def Get_MD_Contribution(File_Name, Day, T):
    
    import pandas as pd
    import numpy as np
    
    Prices = pd.read_csv(File_Name + 'O_' + str(Day) + '.csv').values[:, [0, 2]]
    
    MD = []
    
    for i in range(len(Prices) - T):
        
        MP = (Prices[i, 0] + Prices[i, 1])/2
        FMP = (Prices[i + T, 0] + Prices[i + T, 1])/2
        
        MD.append(FMP - MP)
    
    return MD

###############################################################################
###############################################################################


###############################################################################
###############################################################################


###############################################################################
###############################################################################
