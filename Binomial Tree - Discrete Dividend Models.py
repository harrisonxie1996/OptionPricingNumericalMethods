import numpy as np
import math
import pandas as pd
import statistics as stat
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'serif'

S0 = 52
K = 50
rf = 0.1
D = 2.06  # in dollars
exDiv = 0.2917  # the ex-dividend date is in 3 and a half months
vol = 0.4
T = 5 / 12
N = 5
dT = T / N
u = math.exp(vol * math.sqrt(dT))
d = 1 / u
R = math.exp(rf * dT)
p = (R - d) / (u - d)
pvDiv = D * math.exp(-exDiv * rf)  # present value of the discrete dividend is 2
Stilde0 = 50  # thus, the initial value of S^tilde is 50.00

sTree = np.zeros((N + 1, N + 1))
vTree = np.zeros((N + 1, N + 1))
tempLs = np.zeros(N)

sTree[0][0] = Stilde0
for i in range(N):
    for j in range(i + 1):
        sTree[i + 1][j + 1] = u * sTree[i][j]
    sTree[i + 1][0] = d * sTree[i][0]

for i in range(4):
    for j in range(i + 1):
        sTree[i][j] = sTree[i][j] + pvDiv
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

df1 = pd.DataFrame(sTree)
df1

df2 = pd.DataFrame(vTree)
df2

Delta = (vTree[1][1]-vTree[1][0])/(sTree[1][1]-sTree[1][0])
print("An estimate of Delta is", Delta)

h = 0.5*(S0*u**2-S0*d**2)
Gamma = 1/h*((vTree[2][2]-vTree[2][1])/(S0*u**2-S0) - ((vTree[2][1]-vTree[2][0])/(S0-S0*d**2)))
print("An estimate of Gamma is", Gamma)

Theta = (vTree[2][1] - vTree[0][0])/(2*dT)
print("An estimate of Theta is", Theta)

def americanOptionPrice(sigma):
    S0 = 50
    K = 50
    rf = 0.1
    vol = sigma
    T = 5 / 12
    N = 100
    dT = T / N
    u = math.exp(vol * math.sqrt(dT))
    d = 1 / u
    R = math.exp(rf * dT)
    p = (R - d) / (u - d)

    sTree = np.zeros((N + 1, N + 1))
    vTree = np.zeros((N + 1, N + 1))

    sTree[0][0] = S0
    for i in range(N):
        for j in range(i + 1):
            sTree[i + 1][j + 1] = u * sTree[i][j]
        sTree[i + 1][0] = d * sTree[i][0]

    for i in range(N, -1, -1):
        for j in range(i,-1,-1):
            if i == N:
                vTree[i][j] = max(K - sTree[i][j], 0)
            else:
                continuationValue = 1 / R * (p * vTree[i + 1][j + 1] + (1 - p) * vTree[i + 1][j])
                exerciseValue = max(K - sTree[i][j], 0)
                vTree[i][j] = max(continuationValue, exerciseValue)
    return vTree[0][0]
Vega = (americanOptionPrice(vol+0.01) - americanOptionPrice(vol))/0.01
print("An estimate of Vega is", Vega)