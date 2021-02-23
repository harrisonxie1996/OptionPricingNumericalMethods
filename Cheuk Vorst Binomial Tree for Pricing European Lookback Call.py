import numpy as np
import math
from scipy.stats import norm
import seaborn as sns
from matplotlib import pyplot as plt

# A pricing program for American lookback options using the Cheuk-Vorst binomial algorithm

class lookback_option:
    def __init__(self, S0, K, rd, rf, N, T, vol):
        self.S0 = S0  # spot price
        self.K = K  # initial strike price
        self.rd = rd  # domestic interest rate
        self.rf = rf  # foreign interest rate
        self.N = N  # number of steps
        self.T = T  # maturity
        self.vol = vol  # volatility
        self.dt = self.T/self.N  # delta t
        self.u = math.exp(self.vol*math.sqrt(self.dt)) # proportional up-jump factor
        self.d = 1/self.u # proportional down-jump factor
        self.r = math.exp(self.rd*self.dt)  # domestic growth factor
        self.R = math.exp((self.rd-self.rf)*self.dt) # no arbitrage growth rate of the currency
        self.p = (self.R - self.d)/(self.u - self.d) # risk-neutral probability of up-move
        self.q = (self.R*self.u-1)/(self.R*(self.u-self.d))

    def build_lattice(self):
        '''
        build a Cheuck Vorst lattice
        '''
        self.lattice = np.zeros((self.N + 1, self.N + 1))
        sTree = np.zeros((self.N + 1, self.N + 1))
        sTree[0][0] = self.S0
        for i in range(self.N):
            for j in range(i + 1):
                sTree[i + 1][j + 1] = self.u * sTree[i][j]
                sTree[i + 1][0] = self.d * sTree[i][0]
        for i in range(self.N, -1, -1):
            for j in range(i, -1, -1):
                if i == self.N:
                    self.lattice[i][j] = 1 - round(math.pow(self.u, -j), 4)
                else:
                    if j >= 1:
                        self.lattice[i][j] = 1/self.r*self.R*(self.q*self.lattice[i+1][j+1]+(1-self.q)*self.lattice[i+1][j-1])
                    if j == 0:
                        self.lattice[i][j] = 1 / self.r * self.R * (self.q * self.lattice[i + 1][j + 1] + (1 - self.q) * self.lattice[i + 1][j])


        vTree = np.zeros((self.N + 1, self.N + 1))
        for i in range(self.N, -1, -1):
            for j in range(i, -1, -1):
                if i == self.N:
                    vTree[i][j] = sTree[i][j]*self.lattice[i][j]
                else:
                    if j >= 1:
                        vTree[i][j] = 1 / self.r * (self.p * sTree[i][j]*self.u*self.lattice[i + 1][j + 1] + (1-self.p) * sTree[i][j]*self.d*self.lattice[i + 1][j - 1])
                    if j == 0:
                        vTree[i][j] = 1 / self.r * (self.p * sTree[i][j]*self.u*self.lattice[i + 1][j + 1] + (1-self.p) * sTree[i][j]*self.d*self.lattice[i + 1][j])
        return vTree


S0 = 100
K = 100
rd = 0.04
rf = 0.07
N = 10000
T = 0.5
vol = [0.1, 0.2, 0.3]

for each in vol:
    lookback = lookback_option(S0, K, rd, rf, N, T, each)
    lattice = lookback.build_lattice()
    print(u'Option price: %.4f' % lattice[0][0])

