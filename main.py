
from init_neurons import nc_Matrix, neurons
from parameters import Ntimes
from update_spike_time import updateSpikeTime
from update_synapses import updateSyn
from raster import plot_conn_raster
from runge_kutta import RK4
from tqdm import tqdm # use tqdm to estimate total running time
import argparse

def zeroTempVars():  # Zeros all variables to prevent accidental accumulation of unwanted terms. Just a safety measure, good habit.
    # Note: Do not zero solutions, because they are used in calculating next solutions.
    for nrn in neurons:
        nrn.Input_syn = 0  # Zeroed because ISyn must be added to account for input from multiple neurons. If Isyn was
        # simply assigned, the Isyn would not accumulate. But now it must be zeroed.

def mainProgramLoop():
    for t_ind in tqdm(range(Ntimes)):
        # Records timing of spikes (in t/stepSize)
        updateSpikeTime(t_ind)
        # Updates the input synaptic current to be used in RK4
        updateSyn(t_ind)
        # A function to update the solutions for all neurons' D.E.s
        RK4()
        zeroTempVars()  # Resets temporary variables like Isyn

    plot_conn_raster(0, nc_Matrix)
    return



if __name__ == "__main__":
    
    # Run Program
    mainProgramLoop()
