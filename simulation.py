import numpy as np

import cell as ce
import hamilt as ham


def step(params):
    # params = [number_of_steps, temperature, repulsion, attraction1,
    #           attraction2, std1, std2, c1_minima, c2_minima, breaking_time]

    temperature = params[1]
    number_of_steps = params[0]

    breaking_time = params[9]

    energy_arr = []
    rep = []
    stop_term = []

    # Create two cells:
    # initial conditions from experimental almost-normal distribution
    # The second cell is positioned at a \pm np.pi distance
    # well = [height, mean, std]

    c1_minima = params[7]
    c2_minima = params[8]

    c1 = ce.Cell(np.random.default_rng().normal(
        np.pi, 50 * np.pi / 180), [params[3], c1_minima, params[5]])

    c2 = ce.Cell(c1.pos + np.pi if (c1.pos + np.pi) < 2 *
                                   np.pi else c1.pos - np.pi, [params[4], c2_minima, params[6]])

    cells = [c1, c2]

    energy, others = ham.energy(params, cells[0], cells[1])
    energy_arr.append(energy)
    rep.append(others[0])
    stop_term.append(others[1])

    update_arr = [False, False]
    for t in range(0, number_of_steps - 1):
        if t > breaking_time:
            cells[0].break_symmetry()
            cells[1].break_symmetry()

        e0, _ = ham.energy(params, cells[0], cells[1])

        nv = np.random.choice([1, -1], 2)
        # Test possible updates
        for i in range(0, 2):
            cells[i].virtual_update(nv[i])
            cells[i - 1].virtual_update(0)
            e1, _ = ham.energy(params, cells[0], cells[1], virtual=True)

            if check_metropolis(e0, e1, temperature):
                update_arr[i] = True
            else:
                update_arr[i] = False

        # Update the corresponding cell
        for ii in range(0, 2):
            if update_arr[ii]:
                cells[ii].update(nv[ii])
            else:
                cells[ii].update(0)

        energy, others = ham.energy(params, c1, c2)

        energy_arr.append(energy)
        rep.append(others[0])
        stop_term.append(others[1])

    return (energy_arr, rep, stop_term), (cells[0], cells[1])


def check_metropolis(e0, e1, temperature):
    if e1 < e0:
        return True
    else:
        if temperature != 0:
            rng = np.random.default_rng().uniform(0, 1)
            prob = ham.probability(e0, e1, 1 / temperature)
            if rng < prob:
                return True
            else:
                return False
        else:
            return False
