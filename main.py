import os
from init_neurons import init_nrn
# import parameters as param
from update_spike_time import updateSpikeTime
from update_synapses import updateSyn
from raster import plot_conn_raster, apply_freq_plot
from runge_kutta import RK4

import matplotlib.pyplot as plt


from update_engrams import *
from parameter_parser import *
from tqdm import tqdm # use tqdm to estimate total running time
import argparse

def zeroTempVars(neurons):  # Zeros all variables to prevent accidental accumulation of unwanted terms. Just a safety measure, good habit.
    # Note: Do not zero solutions, because they are used in calculating next solutions.
    for nrn in neurons:
        nrn.Input_syn = 0  # Zeroed because ISyn must be added to account for input from multiple neurons. If Isyn was
        # simply assigned, the Isyn would not accumulate. But now it must be zeroed.


def mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends):

    for t_ind in tqdm(range(params.Ntimes)):

        if params.use_trigo:
            updateExcitability(params, neurons, t_ind)
            applyEngramCurrent(params, neurons, t_ind, eng_starts, eng_ends)
        # Records timing of spikes (in t/stepSize)
        updateSpikeTime(params, neurons, t_ind)
        # Updates the input synaptic current to be used in RK4
        updateSyn(params, neurons, t_ind)
        # A function to update the solutions for all neurons' D.E.s
        RK4(params, neurons)
        zeroTempVars(neurons)  # Resets temporary variables like Isyn

    # apply_freq_plot(params, neurons, nc_Matrix)
    # plot_conn_raster(params, neurons, nc_Matrix)
    if params.eng_num == 2:
        res = dotp_ortho(params, neurons, eng_starts, eng_ends)
    return res



if __name__ == "__main__":
    
    parser = parameter_parser()
    params = parser.get_cfg()

    eng_starts = [50, 175]
    eng_ends = [150, 275]

    close = 0
    for seed in params.seed:
        neurons, nc_Matrix = init_nrn(params, seed)

        # Run Program
        close += mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    close /= len(params.seed)

    eng_starts = [100, 350]
    eng_ends = [200, 450]

    distant = 0
    for seed in params.seed:
        neurons, nc_Matrix = init_nrn(params, seed)

        # Run Program
        distant += mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    distant /= len(params.seed)

    x = ['Close', 'Distant']
    y = [close, distant]
    plt.bar(x, y)
    plt.title('Mean Orthogonality over 5 seeds')
    plt.xlabel('Temporal Separation between Engrams')
    plt.ylabel('Orthogonality Measure')
    plt.savefig('bar_chart_ortho.png')


