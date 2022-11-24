import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
# import matplotlib.cm as cm

import pandas as pd


import simulation as simu

## functions to calculate onset and stop
def logistic(x, a, b, c, d):
    # return (a-d)/((1 + x/c)**b) + d
    num = d-c
    # denom = 1 + np.exp(b*(np.log(x) - a))
    denom = 1 + (x/a)**b
    return c + num/denom

def slope(a, b, c, d):
    return (c-d)*b/(4*a)

def line(x, m, x0):
    return m * (x - x0[0]) + x0[1]


def plot_circle(c1, c2, fname):
    cmap = plt.get_cmap("magma")
    plt.scatter(2 * np.cos(c1.post[0]),
                2 * np.sin(c1.post[0]), marker="x", color="black")
    plt.scatter(2 * np.cos(c1.post), 2 * np.sin(c1.post),
                s=100*np.arange(0, len(c1.post), 1)/nstep,
                color=cmap(np.arange(0, len(c2.post), 1)/nstep),
                alpha=0.7)

    plt.scatter(2 * np.cos(c2.post[0]),
                2 * np.sin(c2.post[0]), marker="x", color="black")
    plt.scatter(2 * np.cos(c2.post), 2 * np.sin(c2.post),
                s=100*np.arange(0, len(c2.post), 1)/nstep,
                color=cmap(np.arange(0, len(c2.post), 1)/nstep),
                alpha=0.7)
    plt.xlabel("Position AP")
    plt.ylabel("Position DV")
    plt.xlim(-2.1, 2.1)
    plt.ylim(-2.1, 2.1)
    plt.savefig(fname, dpi=500)
    plt.clf()

def plot_real(c1, c2, fname):
    plt.scatter(np.arange(0, len(c1.post), 1), np.array(c1.post) * 180/np.pi, s=5, color="green")
    plt.scatter(np.arange(0, len(c2.post), 1), np.array(c2.post) * 180/np.pi, s=5, color="blue")
    plt.xlabel("Time [MCS]")
    plt.ylabel("Angle")
    plt.savefig(fname, dpi=500)
    plt.clf()

def angle_between(th1, th2):
    # return np.arctan((np.sin(th2) - np.sin(th1))/(np.cos(th2) - np.cos(th1)))
    return np.arctan2(np.sin(th2) - np.sin(th1), np.cos(th2) - np.cos(th1))

def sin_sum(th1, th2):
    return np.sin(th1)*np.cos(th2) + np.sin(th2)*np.cos(th1)

def cos_sum(th1, th2):
    return np.cos(th1)*np.cos(th2) - np.sin(th2)*np.sin(th1)

def angle_diff(th1, th2):
    return np.arctan2(sin_sum(th1, th2), cos_sum(th1, th2))

def plot_cumulative_angle(c1, c2, fname):
    angle = [angle_between(c1.post[t], c2.post[t]) for t in range(0, len(c1.post))]
    # angle_differences = np.diff(angle)
    angle_differences = [angle_diff(angle[t+1], - angle[t]) for t in range(0, len(angle) - 1)]
    

    cumsum_angle = np.cumsum(angle_differences)
    
    if cumsum_angle[-1] < 0:
        cumsum_angle = - np.array(cumsum_angle)

    plt.scatter(np.arange(0, len(cumsum_angle), 1), cumsum_angle*180/np.pi, s=5)

    values, _ = sco.curve_fit(logistic, np.arange(0, len(cumsum_angle), 1), cumsum_angle)
    if values[1]<0:
        values = [values[0], abs(values[1]), values[3], values[2]]

    #gives the fit to time given the four parameters
    function_values = logistic(np.arange(0, len(cumsum_angle), 1), values[0], values[1], values[2], values[3])
    inflection = [values[0], logistic(values[0], values[0], values[1], values[2], values[3])]
    int1 = (values[2] - inflection[1]) / slope(values[0], values[1], values[2], values[3]) + inflection[0]
    int2 = (values[3] - inflection[1]) / slope(values[0], values[1], values[2], values[3]) + inflection[0]
    
    plt.scatter(inflection[0], inflection[1]*180/np.pi, marker="x", color="red")
    plt.plot(np.arange(0, len(cumsum_angle), 1), function_values*180/np.pi, ls="--", alpha=0.7, color="red")
    plt.plot(np.arange(0, len(cumsum_angle), 1), 
                line(np.arange(0, len(cumsum_angle), 1), slope(values[0], values[1], values[2], values[3]), inflection)*180/np.pi, color="green")
    plt.scatter(int1, values[2]*180/np.pi, color="green", marker="x")
    plt.scatter(int2, values[3]*180/np.pi, color="pink", marker="x")

    plt.axhline(values[2] * 180/np.pi, color="black", alpha=0.5, ls="--")
    plt.axhline(values[3] * 180/np.pi, color="black", alpha=0.5, ls="--")

    print("onset: ", int2)
    print("terminatioin: ", int1)
    

    plt.ylim(min(cumsum_angle*180/np.pi) - abs(min(cumsum_angle*180/np.pi))*0.1, max(cumsum_angle*180/np.pi) + abs(max(cumsum_angle*180/np.pi))*0.1)
    plt.xlim(np.arange(0, len(cumsum_angle), 1)[0] - 1, np.arange(0, len(cumsum_angle), 1)[-1]+1)

    plt.xlabel("Time [MCS]")
    plt.ylabel("Cumulative angle")
    plt.savefig(fname, dpi=500)
    plt.clf()



nstep = 40000
trange = range(0, nstep)
r = 0.01
s1 = 50
s2 = 50
std1 = 5
std2 = 5
temp = 0.25
breaking_time = 10000
# Asymmetrical model
c1Minima = 0
c2Minima = np.pi
# Competition
#c2Minima = 0

print("Asymmetrical: ")
params = [nstep, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
(energyArr, repulsion, stopTerm), cells = simu.step(params)


plot_circle(cells[0], cells[1], "../img/trayectories/trayectories-asym-converted.png")
plot_real(cells[0], cells[1], "../img/trayectories/trayectories-asym.png")
plot_cumulative_angle(cells[0], cells[1], "../img/trayectories/cumulative-asym.png")

# export angle vs time
df_angles = pd.DataFrame()
df_angles['t'] = range(0, len(cells[0].post))
df_angles['x1'] = 2 * np.cos(cells[0].post)
df_angles['y1'] = 2 * np.sin(cells[0].post)
df_angles['x2'] = 2 * np.cos(cells[1].post)
df_angles['y2'] = 2 * np.sin(cells[1].post)

df_angles.to_csv("../angle_tray.csv", index=False)
print("----------------")



exit()


######################
######################
# Symmetrical model
print("Symmetrical 50-15")

c1Minima = 0
c2Minima = 0
s1 = 50
s2 = 15
params = [nstep, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
(energyArr, repulsion, stopTerm), cells = simu.step(params)

plot_circle(cells[0], cells[1], "img/trayectories/symmetrical-50-15-converted.png")
plot_real(cells[0], cells[1], "img/trayectories/symmetrical-50-15.png")
plot_cumulative_angle(cells[0], cells[1], "img/trayectories/cumulative-50-15.png")

print("----------------")

######################
######################

# Symmetrical model
print("Symmetrical 50-0")

c1Minima = 0
c2Minima = 0
s1 = 50
s2 = 50
params = [nstep, temp, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
(energyArr, repulsion, stopTerm), cells = simu.step(params)

plot_circle(cells[0], cells[1], "img/trayectories/trayectories-sym-converted.png")
plot_real(cells[0], cells[1], "img/trayectories/trayectories-sym.png")
plot_cumulative_angle(cells[0], cells[1], "img/trayectories/cumulative-sym.png")
print("----------------")

