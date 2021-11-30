import os
from init_neurons import init_nrn
# import parameters as param
from update_spike_time import updateSpikeTime
from update_synapses import updateSyn
from raster import plot_conn_raster
from runge_kutta import RK4


from update_engrams import *
from parameter_parser import *
from tqdm import tqdm # use tqdm to estimate total running time
import argparse

def zeroTempVars(neurons):  # Zeros all variables to prevent accidental accumulation of unwanted terms. Just a safety measure, good habit.
    # Note: Do not zero solutions, because they are used in calculating next solutions.
    for nrn in neurons:
        nrn.Input_syn = 0  # Zeroed because ISyn must be added to account for input from multiple neurons. If Isyn was
        # simply assigned, the Isyn would not accumulate. But now it must be zeroed.


def mainProgramLoop(params, neurons, nc_Matrix):

    for t_ind in tqdm(range(params.Ntimes)):

        if params.use_trigo:
            updateExcitability(params, neurons, t_ind)
            applyEngramCurrent(params, neurons, t_ind)
        # Records timing of spikes (in t/stepSize)
        updateSpikeTime(params, neurons, t_ind)
        # Updates the input synaptic current to be used in RK4
        updateSyn(params, neurons, t_ind)
        # A function to update the solutions for all neurons' D.E.s
        RK4(params, neurons)
        zeroTempVars(neurons)  # Resets temporary variables like Isyn

    plot_conn_raster(params, neurons, 0, nc_Matrix)
    return



if __name__ == "__main__":
    
    parser = parameter_parser()
    params = parser.get_cfg()
    
    neurons, nc_Matrix = init_nrn(params)

    # Run Program
    mainProgramLoop(params, neurons, nc_Matrix)
