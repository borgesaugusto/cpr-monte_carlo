import os
import numpy as np
import matplotlib.pyplot as plt

import simulation as simu

number_of_steps = 25000
trange = range(0, number_of_steps)

r = 0.01
s1 = 50
s2 = 0
std1 = 5
std2 = 5

c1Minima = 0
c2Minima = np.pi
# Symmetrical model
# c2Minima = 0

temperature = 0.25

angle1 = []
angle2 = []

params = [number_of_steps, temperature, r, s1, s2, std1, std2, c1Minima, c2Minima, 5000]
(energyArr, repulsion, stopTerm), cells = simu.step(params)

for t in trange:
    if t % 500 == 0:
        print(t)

    if t % 100 == 0:
        plt.scatter(np.cos(cells[0].post[t]), np.sin(cells[0].post[t]), s=1000, color="blue")
        plt.scatter(np.cos(cells[1].post[t]), np.sin(cells[1].post[t]), s=1000, color="green")

        plt.plot([0, np.cos(cells[0].post[t])], [0, np.sin(cells[0].post[t])], ls='--', color="black")
        plt.plot([0, np.cos(cells[1].post[t])], [
            0, np.sin(cells[1].post[t])], ls='--', color="black")

        plt.xlim(-1.25, 1.25)
        plt.ylim(-1.25, 1.25)

        plt.axhline(0, ls="--", color="black")

        # Minima for cell 1
        plt.scatter(np.cos(c1Minima), np.sin(c1Minima), color="blue", facecolors="none", ls="--", s=1200)
        # Minima for cell 2
        plt.scatter(np.cos(c2Minima), np.sin(c2Minima), color="green", facecolors="none", ls="--", s=1000)

        plt.axis('off')
        plt.savefig("../img/movie/dummy/" + str(format(t, '05d')) + ".png", dpi=300)
        plt.close()

status = "asym" if c1Minima != c2Minima else "sym"
os.system(
    f"ffmpeg -framerate 30 -pattern_type glob -i '../img/movie/dummy/*.png' -c:v libx264 -pix_fmt yuv420p "
    f"'../img/movie/{s1}_{s2}_{status}.mp4'")
