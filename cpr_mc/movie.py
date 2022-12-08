import numpy as np
import matplotlib.pyplot as plt

import simulation as simu
import os

number_of_steps = 30000
trange = range(0, number_of_steps)

r = 0.01
s1 = 50
s2 = 15
std1 = 5
std2 = 5

breaking_time = 10000
# Asymmetrical
c1Minima = 0
# c2Minima = np.pi
# Competition
c2Minima = 0

temperature = 0.05

angle1 = []
angle2 = []

params = [number_of_steps, temperature, r, s1, s2, std1, std2, c1Minima, c2Minima, breaking_time]
(energyArr, repulsion, stopTerm), cells = simu.step(params)

for t in trange[::100]:
    plt.scatter(np.cos(cells[0].post[t]), np.sin(cells[0].post[t]), s=1000, color="blue")
    plt.scatter(np.cos(cells[1].post[t]), np.sin(cells[1].post[t]), s=1000, color="green")

    plt.plot([0, np.cos(cells[0].post[t])], [0, np.sin(cells[0].post[t])], ls='--', color="black")
    plt.plot([0, np.cos(cells[1].post[t])], [0, np.sin(cells[1].post[t])], ls='--', color="black")

    plt.annotate(f"Time: {t} MCS", xy=(0.7, 0.05), xytext=(0.7, 0.05), textcoords='figure fraction')
    plt.xlim(-1.25, 1.25)
    plt.ylim(-1.25, 1.25)

    plt.axhline(0, ls="--", color="black")

    # Minima for cell 1
    plt.scatter(np.cos(c1Minima), np.sin(c1Minima), color="blue", facecolors="none", ls="--", s=s1 * 20)
    # Minima for cell 2
    plt.scatter(np.cos(c2Minima), np.sin(c2Minima), color="green", facecolors="none", ls="dotted", s=s2 * 20)

    plt.axis('off')
    plt.savefig("../img/movie/dummy/" + str(format(t, '05d')) + ".png", dpi=300)
    plt.close()

status = "asym" if c1Minima != c2Minima else "sym"
os.system(f"ffmpeg -framerate 30 -pattern_type glob -i '../img/movie/dummy/*.png' -c:v libx264"
          f" -pix_fmt yuv420p 'img/movie/{s1}_{s2}_{status}.mp4'")
