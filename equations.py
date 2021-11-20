import numpy as np

# Hodgkin-Huxley Model
def equations(solns_, eqn, Isyn, Idrive, nrn):
    # These equations are parameters are adjusted to fit fast-spiking interneurons.

    tempVal = 0

    category = nrn.category
    Inoise = nrn.Input_noise  # Noise from neuron. Maybe I should put Idrive, solns, etc here as well?

    if category == 'Excitatory':
        gks = 0  # We are not modeling ACh in this project
        C = 1
        gna = 24
        gkdr = 3
        gl = 0.02
        Vna = 55
        Vk = -90
        Vl = -60
        if (eqn == 0):
            hinf = 1 / (1 + np.exp((solns_[3] + 53) / 7))
            tauh = .37 + 2.78 / (1 + np.exp((solns_[3] + 40.5) / 6))
            tempVal = (hinf - solns_[0]) / tauh
        elif (eqn == 1):
            ninf = 1 / (1 + np.exp((-solns_[3] - 30) / 10))
            taun = .37 + 1.85 / (1 + np.exp((solns_[3] + 27) / 15))
            tempVal = (ninf - solns_[1]) / taun
        elif (eqn == 2):
            zinf = 1 / (1 + np.exp((-solns_[3] - 39) / 5))
            tempVal = (zinf - solns_[2]) / 75
        elif (eqn == 3):
            m = 1 / (1 + np.exp((-solns_[3] - 30) / 9.5))
            tempVal = (-gna * (m ** 3) * solns_[0] * (solns_[3] - Vna) - gkdr * (solns_[1] ** 4) * (solns_[3] - Vk)
                       - gks * solns_[2] * (solns_[3] - Vk) - gl * (solns_[3] - Vl) + Idrive - Isyn + Inoise) / C

    elif category == 'SST':
        gks = 0  # We are not modeling ACh in this project
        C = 1
        gna = 24
        gkdr = 3
        gl = 0.02
        Vna = 55
        Vk = -90
        Vl = -60
        if (eqn == 0):
            hinf = 1 / (1 + np.exp((solns_[3] + 53) / 7))
            tauh = .37 + 2.78 / (1 + np.exp((solns_[3] + 40.5) / 6))
            tempVal = (hinf - solns_[0]) / tauh
        elif (eqn == 1):
            ninf = 1 / (1 + np.exp((-solns_[3] - 30) / 10))
            taun = .37 + 1.85 / (1 + np.exp((solns_[3] + 27) / 15))
            tempVal = (ninf - solns_[1]) / taun
        elif (eqn == 2):
            zinf = 1 / (1 + np.exp((-solns_[3] - 39) / 5))
            tempVal = (zinf - solns_[2]) / 75
        elif (eqn == 3):
            m = 1 / (1 + np.exp((-solns_[3] - 30) / 9.5))
            tempVal = (-gna * (m ** 3) * solns_[0] * (solns_[3] - Vna) - gkdr * (solns_[1] ** 4) * (solns_[3] - Vk)
                       - gks * solns_[2] * (solns_[3] - Vk) - gl * (solns_[3] - Vl) + Idrive - Isyn) / C

    elif category == 'PV+':
        C = 1
        gna = 35
        gkdr = 9
        gl = 0.1
        Vna = 55
        Vk = -90
        Vl = -65
        if (eqn == 0):
            a_h = 0.07 * np.exp(-(solns_[3] + 58) / 20)
            b_h = 1 / (np.exp(-0.1 * (solns_[3] + 28)) + 1)
            phi = 5
            tempVal = phi * (a_h * (1 - solns_[0]) - b_h * solns_[0])
        elif (eqn == 1):
            a_n = -0.01 * (solns_[3] + 34) / (np.exp(-0.1 * (solns_[3] + 34)) - 1)
            b_n = 0.125 * np.exp(-(solns_[3] + 44) / 80)
            phi = 5
            tempVal = phi * (a_n * (1 - solns_[1]) - b_n * solns_[1])
        elif (eqn == 2):
            zinf = 1 / (1 + np.exp((-solns_[3] - 39) / 5))
            tempVal = (zinf - solns_[2]) / 75
        elif (eqn == 3):
            a_m = -0.1 * (solns_[3] + 35) / (np.exp(-0.1 * (solns_[3] + 35)) - 1)
            b_m = 4 * np.exp(-(solns_[3] + 60) / 18)
            m = a_m / (a_m + b_m)
            tempVal = (-gna * (m ** 3) * solns_[0] * (solns_[3] - Vna) - gkdr * (solns_[1] ** 4) * (solns_[3] - Vk)
                       - gl * (solns_[3] - Vl) + Idrive - Isyn) / C

    return tempVal
