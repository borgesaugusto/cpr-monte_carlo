import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import simulation as simu
import hamilt as ham

from tqdm import tqdm

number_of_steps = 25000
trange = range(0, number_of_steps)

r = 0.01
s1 = 50
std1 = 5
std2 = 5

# Asymmetrical model
c1Minima = 0
c2Minima = np.pi
# Symmetrical model
# c2Minima = 0

temp = 0.05

angle1 = []
angle2 = []

angleMean = []
angleStd = []

replicates = 10

breaking_time = 10000

s2Range = np.arange(0, 26, 5)
for s2 in s2Range:
    angRes = []
    for rep in tqdm(range(0, replicates), desc="Running replicates"):
        params = [number_of_steps, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
        (energyArr, repulsion, stopTerm), cells = simu.step(params)

        # Angle between cells and x-axis
        a1 = cells[0].post[-1]
        if a1 > np.pi:
            a1 -= 2 * np.pi
        a2 = cells[1].post[-1]
        if a2 > np.pi:
            a2 -= 2 * np.pi
        angle1.append(abs(a1))
        angle2.append(abs(a2))

        # Angle converting to x-y
        x1 = np.cos(a1)
        y1 = np.sin(a1)
        x2 = np.cos(a2)
        y2 = np.sin(a2)

        vector = [abs(x1 - x2), abs(y1 - y2)]
        res = np.arctan2(vector[1], vector[0])
        angRes.append(res)
    angleMean.append(np.mean(angRes))
    angleStd.append(np.std(angRes))

    df_well = pd.DataFrame()
    df_well['angles'] = angRes
    # df_well.to_csv(f"res/angles_asym_{s1}_{s2}.csv", index=False)

df = pd.DataFrame()

df['depth'] = s2Range
df['mean'] = angleMean
df['std'] = angleStd
# two wells
plt.plot(df['depth'], df['mean'] * 180 / np.pi, ls="--", color="blue", label="Asymmetrical model")
plt.fill_between(df['depth'], df['mean'] * 180 / np.pi - df['std'] * 180 / np.pi,
                 df['mean'] * 180 / np.pi + df['std'] * 180 / np.pi, alpha=0.2, color="blue")
# color="#3D3A4B"
##########################################################################################
# Symmetrical model
c1Minima = 0
c2Minima = 0

angle1 = []
angle2 = []

angleMean = []
angleStd = []

for s2 in s2Range:
    angRes = []
    for rep in tqdm(range(0, replicates), desc="Running replicates"):
        params = [number_of_steps, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
        (energyArr, repulsion, stopTerm), cells = simu.step(params)

        # Angle between cells and x-axis
        a1 = cells[0].post[-1]
        if a1 > np.pi:
            a1 -= 2 * np.pi
        a2 = cells[1].post[-1]
        if a2 > np.pi:
            a2 -= 2 * np.pi
        angle1.append(abs(a1))
        angle2.append(abs(a2))

        # Angle converting to x-y
        x1 = np.cos(a1)
        y1 = np.sin(a1)
        x2 = np.cos(a2)
        y2 = np.sin(a2)

        vector = [abs(x1 - x2), abs(y1 - y2)]
        res = np.arctan2(vector[1], vector[0])
        angRes.append(res)

    df_well = pd.DataFrame()
    df_well['angles'] = angRes
    # df_well.to_csv(f"res/angles_sym_{s1}_{s2}.csv", index=False)

    angleMean.append(np.mean(angRes))
    angleStd.append(np.std(angRes))

df = pd.DataFrame()

df['depth'] = s2Range
df['mean'] = angleMean
df['std'] = angleStd

plt.plot(df['depth'], df['mean'] * 180 / np.pi, ls="--", color="red", label="Symmetrical model")
plt.fill_between(df['depth'], df['mean'] * 180 / np.pi - df['std'] * 180 / np.pi,
                 df['mean'] * 180 / np.pi + df['std'] * 180 / np.pi, alpha=0.2, color="red")
# color="#B19994"
plt.ylabel("Final angle [º]")
plt.ylim(0, 90)
plt.xlabel("Depth of second well")

plt.xticks([0, 5, 10, 15, 20, 25],
           ["50:0", "50:5", "50:10", "50:15", "50:20", "50:25"])
plt.legend()
# plt.tight_layout()
plt.xlim(0, 25)
plt.savefig("../img/both.pdf", dpi=300)
