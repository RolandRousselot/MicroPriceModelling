# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 03:25:33 2019

@author: Roland
"""

###############################################################################
###############################################################################

def Plot_P():
    
    import matplotlib.pyplot as plt
    
    T = [i/100 for i in range(1, 82)]
    
    MICRO = [Get_P(t) for t in T]
    
    plt.plot(T, MICRO)
    
    return MICRO

###############################################################################
###############################################################################

def Get_P(t):
    
    from scipy.optimize import minimize
    print(t)
    if t <= 0.4:
        
        X = minimize(Likelihood1, x0 = 100, args = (t, 100)).x[0]
        
    if 0.4 < t <= 0.8:
        
        X = minimize(Likelihood2, x0 = 100, args = (t, 100)).x[0]
        
    if 0.8 < t <= 1:
        
        X = minimize(Likelihood3, x0 = 100, args = (t, 100)).x[0]
    
    return X

###############################################################################
###############################################################################

def Likelihood1(Mu, t, m):
    
    A = [l(k, Mu, m, t) for k in range(4)]
    
    return -sum(A)
    
###############################################################################
###############################################################################

def Likelihood2(Mu, t, m):
    
    from scipy.stats import norm
    B = []
    
    for i in range(30):
        z = 99 + i/10
        L1 = -Likelihood1(z, 0.2, m)
        L2 = -Likelihood1(Mu, t - 0.2, z)
        N = norm.cdf(101, z, 1)
        
        B.append(L1*L2*N)
    
    return -sum(B)
    
###############################################################################
###############################################################################

def Likelihood3(Mu, t, m):
    
    from scipy.stats import norm
    B = []
    
    for i in range(30):
        for j in range(30):
            y = 99 + i/10    
            z = 99 + j/10
            L1 = -Likelihood1(y, 0.2, m)
            L2 = -Likelihood1(z, 0.6, y)
            L3 = -Likelihood1(Mu, t - 0.8, z)
            N1 = norm.cdf(101, y, 1)
            N2 = 1 - norm.cdf(101, z, 1)
        
            B.append(L1*L2*L3*N1*N2)
    
    return -sum(B)

###############################################################################
###############################################################################

def l(k, Mu, m, t):
    
    from scipy.stats import norm
    import scipy as sc
    
    if k == 0:
        
        return sc.e**(-5*t)*norm.pdf(Mu - m, t)
    
    if k != 0:
    
        S = [(1 + 2*i)/(2*k) for i in range(k)]
        M = [m + (Mu - m)*i for i in S]
        T = [0 + t*i for i in S]
        
        DIST = ((norm.pdf((Mu - m)/(k), 0, 3*t/(k)))**(k - 1))*((norm.pdf((Mu - m)/2*(k), 0, 3*t/2*(k)))**(2))
        IN = mult([norm.cdf(101, M[i], 1) - norm.cdf(100, M[i], 1) for i in range(k)])
        EXP = (sc.e**(-5*t)*(5*t)**(k))/sc.special.factorial(k)
        
        return DIST*IN*EXP

###############################################################################
###############################################################################

def mult(List):
    
    M = 1
    
    for i in range(len(List)):
        
        M = M*List[i]
        
    return M

###############################################################################
###############################################################################