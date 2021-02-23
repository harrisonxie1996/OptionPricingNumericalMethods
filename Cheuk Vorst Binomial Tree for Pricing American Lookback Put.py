import numpy as np
import math
from scipy.stats import norm
import seaborn as sns
from matplotlib import pyplot as plt

# A pricing program for American lookback options using the Cheuk-Vorst binomial algorithm

class lookback_option:
    def __init__(self, S0, K, rf, N, T, vol):
        self.S0 = S0  # spot price
        self.K = K  # initial strike price
        self.r = rf  # risk-free rate
        self.N = N  # number of steps
        self.T = T  # maturity
        self.vol = vol  # volatility
        self.dt = self.T/self.N  # delta t
        self.u = math.exp(self.vol*math.sqrt(self.dt)) # proportional up-jump factor
        self.d = 1/self.u # proportional down-jump factor
        self.R = math.exp(self.r*self.dt) # growth factor per step
        self.p = (self.R - self.d)/(self.u - self.d) # risk-neutral probability of up-move

    def build_lattice(self):
        '''
        build a Cheuck Vorst lattice
        '''
        self.lattice = np.zeros((self.N + 1, self.N + 1))
        self.lattice[:,0] = 1.0000
        for i in range(self.N):
            for j in range(i + 1):
                self.lattice[i + 1][j + 1] = round(math.pow(self.u, j+1),4)

        vTree = np.zeros((self.N+1, self.N+1))
        vTree[self.N][0] = 0
        for i in range(self.N, -1, -1):
            for j in range(i,-1,-1):
                if i == self.N:
                    if j == 0:
                        vTree[i][j] = 0
                    else:
                        vTree[i][j] = self.lattice[i][j] - 1
                else:
                    if j >= 1:
                        vTree[i][j] = max(self.lattice[i][j]-1, 1/self.R*((1-self.p)*vTree[i+1][j+1]*self.d+self.p*vTree[i+1][j-1]*self.u))
                    if j == 0:
                        vTree[i][j] = max(self.lattice[i][j]-1, 1/self.R*((1-self.p)*vTree[i+1][j+1]*self.d +self.p*vTree[i+1][j]*self.u))
        return vTree


        # def max_prices(t, S):
        #     '''
        #     This function is used to find a maximum prices in a price list over time interval [0,t]
        #     :param t: t is the ending time, included
        #     :param S: the price path
        #     :return: maximum prices from time 0 to time t
        #     '''
        #     Smax = np.zeros(t)
        #     Smax[0] = S[0]
        #     for i in range(1,t+1):
        #         Smax[i] = max(Smax[i-1], S[i])
        #     return Smax

        # # construct Cheuk Vorst tree
        # Y = np.zeros((self.N+1, self.N+1))
        # Y[:, 0] = 1.0000
        # for i in range(1,self.N):
        #     for j in range(i+1):
        #         Y[i][j] = max_prices(i, self.lattice[:i, j])/self.lattice[i][j]



S0 = 50
K = 50
rf = 0.1
N = 3
T = 0.25
vol = 0.4

lookback = lookback_option(S0, K, rf, N, T, vol)
lattice = lookback.build_lattice()
print(u'Option price: %.4f' % lattice[0][0])
# print(lattice)
