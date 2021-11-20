import numpy as np
from parameters import numEquations, stepSize
import equations as eq
from init_neurons import neurons


def RK4():

    for nrn in neurons:

        solns = nrn.solutions
        Isyn = nrn.Input_syn
        Idrive = nrn.Idrive
        k1 = np.zeros(numEquations)
        k2 = np.zeros(numEquations)
        k3 = np.zeros(numEquations)
        k4 = np.zeros(numEquations)

        init_solns = solns

        # Calculates the k1 variables
        for ii in range(len(solns)):
            k1[ii] = stepSize * eq.equations(solns, ii, Isyn, Idrive, nrn)

        # Calculates the k2 variables
        for ii in range(len(solns)):
            k2[ii] = stepSize * eq.equations(solns + k1 / 2, ii, Isyn, Idrive,
                                               nrn)  # important fix done here. solns must be advanced by k
            # for calculation of the next k variable.
        # Calculates the k3 variables
        for ii in range(len(solns)):
            k3[ii] = stepSize * eq.equations(solns + k2 / 2, ii, Isyn, Idrive, nrn)

            # Calculates the k4 variables
        for ii in range(len(solns)):
            k4[ii] = stepSize * eq.equations(solns + k3, ii, Isyn, Idrive, nrn)

        # Updates the general solution
        for ii in range(len(solns)):
            solns[ii] = init_solns[ii] + (k1[ii] + 2 * k2[ii] + 2 * k3[ii] + k4[ii]) / 6
            nrn.solutions[ii] = solns[ii]