import numpy as np


class Cell:
    dx = 0.25 * np.pi / 180

    def __init__(self, p0, well=None):
        # well = [height, mean, std]
        if well is None:
            well = [0, 0, 0]
        self.well = well
        self.well_original = self.well.copy()

        self.well[0] = 0

        self.pos = p0

        self.posv = 0

        self.turn = 0
        self.turns = []

        self.post = []
        self.velt = []

        self.post.append(self.pos)
        self.velt.append(0)
        self.turns.append(0)

    def break_symmetry(self):
        self.well = self.well_original

    def update(self, vel):
        self.pos += vel * self.dx
        if self.pos > 2 * np.pi:
            self.pos -= 2 * np.pi
            self.turn += 1
        elif self.pos < 0:
            self.pos += 2 * np.pi
            self.turn -= 1

        self.posv = self.pos

        self.post.append(self.pos)
        self.velt.append(vel)
        self.turns.append(self.turn)

    def virtual_update(self, vel):
        self.posv = self.pos + vel * self.dx
        if self.posv > 2 * np.pi:
            self.posv -= 2 * np.pi
        elif self.posv < 0:
            self.posv += 2 * np.pi
