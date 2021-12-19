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

    means = np.zeros(4)
    std = np.zeros(4)

    temp_list = np.zeros(5)

    prob_engrams = [1.0, 0.0]

    eng_starts = [250, 450]
    eng_ends = [350, 550]

    for i, seed in enumerate(params.seed):
        neurons, nc_Matrix = init_nrn(params, seed, prob_engrams)

        # Run Program
        temp_list[i] = mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    means[0] = np.mean(temp_list)
    std[0] = np.std(temp_list)


    eng_starts = [400, 1400]
    eng_ends = [500, 1500]

    for i, seed in enumerate(params.seed):
        neurons, nc_Matrix = init_nrn(params, seed, prob_engrams)

        # Run Program
        temp_list[i] = mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    means[1] = np.mean(temp_list)
    std[1] = np.std(temp_list)


    prob_engrams = [0.5, 0.5]

    eng_starts = [250, 450]
    eng_ends = [350, 550]

    for i, seed in enumerate(params.seed):
        neurons, nc_Matrix = init_nrn(params, seed, prob_engrams)

        # Run Program
        temp_list[i] = mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    means[2] = np.mean(temp_list)
    std[2] = np.std(temp_list)


    eng_starts = [400, 1400]
    eng_ends = [500, 1500]

    for i, seed in enumerate(params.seed):
        neurons, nc_Matrix = init_nrn(params, seed, prob_engrams)

        # Run Program
        temp_list[i] = mainProgramLoop(params, neurons, nc_Matrix, eng_starts, eng_ends)
    means[3] = np.mean(temp_list)
    std[3] = np.std(temp_list)



    fig, ax = plt.subplots()
    x = ['Close (100%)', 'Distant (100%)', 'Close (50%)', 'Distant (50%)']
    ax.bar(x, means, yerr=[np.zeros(4), std], capsize=7)
    ax.set_title('Mean Orthogonality over 5 seeds - Large Simulation')
    ax.set_xlabel('Temporal Separation between Engrams (% Selection)')
    ax.set_ylabel('Orthogonality Measure')
    plt.savefig('bar_chart_ortho_large.png')


