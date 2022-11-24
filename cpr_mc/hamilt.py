import numpy as np


def boundary_condition(a1, a2):
    if (a1 - a2) > np.pi:
        a2 += 2 * np.pi
    if (a1 - a2) < -np.pi:
        a1 += 2 * np.pi
    return a1, a2


def energy_repulsion(a1, a2):
    a1, a2 = boundary_condition(a1, a2)
    return ((a1 - a2) ** 2 - np.pi ** 2) ** 2


def spheres_potential(a1, a2, repulsion_type='hard'):
    a1, a2 = boundary_condition(a1, a2)
    sigma = np.pi
    n = 12
    if abs(a1 - a2) <= sigma:
        if repulsion_type == 'hard':
            ret = 100
        elif repulsion_type == "soft":
            # soft spheres
            if a1 == a2:
                a1 += 0.0001
            ret = (sigma / abs(a1 - a2)) ** n
        else:
            print("No repulsion potential")
            exit()
    else:
        ret = 0
    return ret


def gaussian_well(x0, minima, std):
    x0, minima = boundary_condition(x0, minima)
    return -np.exp(-((x0 - minima) ** 2) / (2 * std))


def attraction(c1, c2, virtual):
    if virtual:
        a1, a2 = c1.posv, c2.posv
    else:
        a1, a2 = c1.pos, c2.pos

    p0 = c1.well[0] * gaussian_well(a1, c1.well[1], c1.well[2])
    p1 = c2.well[0] * gaussian_well(a2, c2.well[1], c2.well[2])
    return p0 + p1


def energy(p, c1, c2, virtual=False):
    if not virtual:
        rep = p[2] * spheres_potential(c1.pos, c2.pos, 'soft')
    else:
        rep = p[2] * spheres_potential(c1.posv, c2.posv, 'soft')

    attr = attraction(c1, c2, virtual)

    hamiltonian = rep + attr
    return hamiltonian, (rep, attr)


def probability(e1, e2, beta):
    prob = np.exp(-beta * (e2 - e1))
    return prob


def ave_coupling(c1, c2):
    """Calculate coupling from the cells' history. Avoid the last 10 steps after v = 0

    Args:
        c1 (object): Cell 1 object
        c2 (object): Cell 2 object

    Returns:
        float: Coupling normalized by the amount of steps
    """
    coup = 0
    for t in range(0, len(c1.velt)):
        if (t > 10) and (not np.any(c1.velt[t - 10:t])) and (not np.any(c2.velt[t - 10:t])):
            break
        if c1.velt[t] == c2.velt[t]:
            coup += 1
    return coup / t


def ave_pers_sum(c1, c2):
    pers = 0
    for t in range(1, len(c1.velt)):
        p1 = 0
        p2 = 0
        if (t > 10) and (not np.any(c1.velt[t - 10:t])) and (not np.any(c2.velt[t - 10:t])):
            break
        if c1.velt[t] == c1.velt[t - 1]:
            p1 = 1
        if c2.velt[t] == c2.velt[t - 1]:
            p2 = 1
        pers += p1 + p2
    return pers / 2 * t


def ave_pers_mult(c1, c2):
    pers = 0
    for t in range(1, len(c1.velt)):
        p1 = 0
        p2 = 0
        if (t > 10) and (not np.any(c1.velt[t - 10:t])) and (not np.any(c2.velt[t - 10:t])):
            break
        if c1.velt[t] == c1.velt[t - 1]:
            p1 = 1
        if c2.velt[t] == c2.velt[t - 1]:
            p2 = 1
        pers += p1 * p2
    return pers / t


def equilibrium_time(c1, c2):
    for t in range(0, len(c1.velt)):
        if (t > 10) and (not np.any(c1.velt[t - 10:t])) and (not np.any(c2.velt[t - 10:t])):
            break
    return t


def coordination(c1, c2):
    coord = []
    for t in range(0, len(c1.velt)):
        coord.append((c1.velt[t] + c2.velt[t]) / 2)
    return coord
