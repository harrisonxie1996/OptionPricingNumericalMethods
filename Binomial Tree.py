import numpy as np
import math
import pandas as pd
import statistics as stat
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'serif'

S0 = 50
K = 50
rf = 0.1
vol = 0.4
T = 5 / 12
N = 5
dT = T / N
u = math.exp(vol * math.sqrt(dT))
d = 1 / u
R = math.exp(rf * dT)
p = (R - d) / (u - d)

sTree = np.zeros((N + 1, N + 1))
vTree = np.zeros((N + 1, N + 1))
tempLs = np.zeros(N)

sTree[0][0] = S0
for i in range(N):
    for j in range(i + 1):
        sTree[i + 1][j + 1] = u * sTree[i][j]
    sTree[i + 1][0] = d * sTree[i][0]

for i in range(N, -1, -1):
    for j in range(i, -1, -1):
        if i == N:
            vTree[i][j] = max(K - sTree[i][j], 0)
        else:
            continuationValue = 1 / R * (p * vTree[i + 1][j + 1] + (1 - p) * vTree[i + 1][j])
            exerciseValue = max(K - sTree[i][j], 0)
            vTree[i][j] = max(continuationValue, exerciseValue)
            if exerciseValue > continuationValue:
                if i != 0:
                    tempLs[i - 1] = 0.5 * (sTree[i][j] + sTree[i][j + 1])
                    # print(tempLs[i-1])
                else:
                    tempLs[i - 1] = sTree[i][j]
                    # print(tempLS[i-1])

print("Option tenor is", T, " years")
print("Time step is", dT)
print("Proportional up-jump factor is", u)
print("Proportional down-jump factor is", d)
print("Growth factor per step is", R)
print("Risk neutral probability of up-move is", p)
print("Risk neutral probability of down-move is", 1 - p)
print("Discount factor per step is", 1 / R)
print("The American put option price is", vTree[0][0])