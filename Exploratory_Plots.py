# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 13:32:32 2019

@author: Roland
"""

###############################################################################
###############################################################################

def Spread_Plot():
    
    File_Name = 'Data/BAC/Labeled_BAC_2011-03/'
    Day_Number = 23
    
    Spreads = [0]*8
    
    for Day in range(Day_Number):
        
        print(Day)
        
        Spread_Contribution = Get_Spread_Contribution(File_Name, Day)
        
        for i in range(8):
            
            Spreads[i] += Spread_Contribution[i]
    
    Plot_Spreads(Spreads)

###############################################################################
###############################################################################

def Get_Spread_Contribution(File_Name, Day):
    
    import pandas as pd
    import numpy as np
    
    Times = pd.read_csv(File_Name + 'M_' + str(Day) + '.csv').values[:, [0]]
    Prices = pd.read_csv(File_Name + 'O_' + str(Day) + '.csv').values[:, [0, 2]]
    
    Spreads = np.concatenate((Times, Prices[:, [0]] - Prices[:, [1]]), axis = 1)
    Spread_List = [100, 200, 300, 400, 500, 600, 700, 800]
    Spread_Amount = [0]*8
    
    for i in range(len(Spreads) - 1):
    
        if Spread_List.count(Spreads[i, 1]) == 1:
        
            Index = Spread_List.index(Spreads[i, 1])
            Time = Spreads[i+1, 0] - Spreads[i, 0]
            Spread_Amount[Index] += Time
            
    return Spread_Amount
    
###############################################################################
###############################################################################

def Plot_Spreads(Spreads):
    
    import matplotlib.pyplot as plt
    
    Spreads = [100*i/sum(Spreads) for i in Spreads]
    
    print(Spreads)
    plt.bar([1, 2, 3, 4, 5, 6, 7, 8], Spreads)
    plt.title("Spread Data for INTC")
    plt.xlabel('Spread (in cents)')
    plt.ylabel('Percent of time spent with spread')

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################

###############################################################################
###############################################################################