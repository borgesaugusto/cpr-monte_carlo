
import numpy as np
import pandas as pd
import os
import simulation as simu

# functions to calculate onset and stop


def logistic(x, a, b, c, d):
    # return (a-d)/((1 + x/c)**b) + d
    num = d-c
    denom = 1 + (x/a)**b
    return c + num/denom


def slope(a, b, c, d):
    return (c-d)*b/(4*a)


def line(x, m, x0):
    return m * (x - x0[0]) + x0[1]


def angle_between(th1, th2):
    return np.arctan2(np.sin(th2) - np.sin(th1), np.cos(th2) - np.cos(th1))


def sin_sum(th1, th2):
    return np.sin(th1)*np.cos(th2) + np.sin(th2)*np.cos(th1)


def cos_sum(th1, th2):
    return np.cos(th1)*np.cos(th2) - np.sin(th2)*np.sin(th1)


def angle_diff(th1, th2):
    return np.arctan2(sin_sum(th1, th2), cos_sum(th1, th2))


number_of_steps = 40000
trange = range(0, number_of_steps)
r = 0.01
std1 = 5
std2 = 5
temp = 0.05
breaking_time = 10000
# Asymmetrical model
# s2 = 0
s1 = 50
replicates = range(0, 40)
for s2 in [0, 5, 10, 15, 20, 25, 30]:
    current_folder = f"{s1}_{s2}/005_temp"
    if not os.path.exists(f"../res/{current_folder}/asymmetrical"):
        os.makedirs(f"../res/{current_folder}/asymmetrical")
    if not os.path.exists(f"../res/{current_folder}/symmetrical"):
        os.makedirs(f"../res/{current_folder}/symmetrical")

    print("Asymmetrical: ")
    for rep in replicates:
        # params = [number_of_steps, temperature, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
        params = [number_of_steps, temp, r, s1, s2, std1, std2, 0, np.pi, breaking_time]
        (energyArr, repulsion, stopTerm), cells = simu.step(params)

        # export angle vs time
        df_angles = pd.DataFrame()
        df_angles['t'] = range(0, len(cells[0].post))
        df_angles['x1'] = 2 * np.cos(cells[0].post)
        df_angles['y1'] = 2 * np.sin(cells[0].post)
        df_angles['x2'] = 2 * np.cos(cells[1].post)
        df_angles['y2'] = 2 * np.sin(cells[1].post)
        df_angles['th1'] = cells[0].post
        df_angles['th2'] = cells[1].post

        df_angles.to_csv(f"../res/{current_folder}/asymmetrical/{rep}_tray.csv", index=False)
    print("----------------")

    # Symmetrical model
    print(f"Symmetrical {s1}-{s2}")

    c1Minima = 0
    c2Minima = 0
    # s1 = 50
    # s2 = 20
    for rep in replicates:
        params = [number_of_steps, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
        (energyArr, repulsion, stopTerm), cells = simu.step(params)
        # export angle vs time
        df_angles = pd.DataFrame()
        df_angles['t'] = range(0, len(cells[0].post))
        df_angles['x1'] = 2 * np.cos(cells[0].post)
        df_angles['y1'] = 2 * np.sin(cells[0].post)
        df_angles['x2'] = 2 * np.cos(cells[1].post)
        df_angles['y2'] = 2 * np.sin(cells[1].post)
        df_angles['th1'] = cells[0].post
        df_angles['th2'] = cells[1].post

        df_angles.to_csv(f"../res/{current_folder}/symmetrical/{rep}_tray.csv", index=False)
    print("----------------")

