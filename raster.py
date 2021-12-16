import numpy as np

# from parameters import stepSize, numnrn
# from init_neurons import neurons

import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import vlines
# from parameters import stepSize, numnrn


def plot_conn_raster(params, neurons, nc_Matrix):  # Plots raster plot and connectivity matrix.
    
    start_time = 0
    stepSize, numnrn = params.stepSize, params.numnrn
    
    plot_raster = True
    plot_connection_mat = True

    list_i, list_e = [], []
    for nrn in neurons:  # Separates neuron IDs into a list of inhibitory and excitatory.
        if nrn.category == 'SST' or nrn.category == 'PV+':
            list_i.append(nrn)  # Appends full nrn object (not just the ID) to make sorting by gsyn easier.
        if nrn.category == 'Excitatory':
            list_e.append(nrn)

    neuron_list = list_i + list_e  # Adds the two lists such that inhibitory neurons come first and excitory second.

    # Define legend attributes
    custom_lines = [Line2D([0], [0], color='purple', lw=4),
                    Line2D([0], [0], color='orange', lw=4),
                    Line2D([0], [0], color='green', lw=4),
                    Line2D([0], [0], color='blue', lw=4),
                    Line2D([0], [0], color='red', lw=4)]

    # TODO: Uncomment for custom_lines_fig1 = [Line2D([0], [0], color='olive', lw=4),
    #                     Line2D([0], [0], color='blue', lw=4),
    #                     Line2D([0], [0], color='red', lw=4)]

    if plot_raster:  # Plots raster plot of neuron spikes. Ordered with inhibitory on the bottom, followed by sorted E neurons.
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(20, 10), sharex=True)
        # TODO: Uncomment for fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 5), sharex=True)

        start = start_time / stepSize  # time to start plotting from.

        for index, nrn in enumerate(neuron_list):
            spikeTimes_toplot = []

            for t in nrn.spikeTimes:  # Runs through spike times of every neuron in 'neuron_list', starting with inhibitory.3
                if t >= start:  # only selects times greater than 'start' for plotting.
                    spikeTimes_toplot = np.append(spikeTimes_toplot, t * stepSize)

            index_plot_list = [index] * len(spikeTimes_toplot)

            color = nrn.color  # Color of spikes plotted for this neuron on raster plot.

            ax1.scatter((spikeTimes_toplot), index_plot_list, c=color,
                        s=10)  # c controls nrn dot color, s controls dot size.

        ax1.set_title('No Engram Stimuli Active')
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Neurons Sorted by Group')
        # TODO: Uncomment for initial - ax1.legend(custom_lines_fig1, ['Winners', 'Losers', 'Inhibitory'], loc='upper left')
        ax1.legend(custom_lines, ['engram 1', 'engram 2', 'engram 1&2', 'non-engram', 'inhibitory'], loc='upper left')

        for i in range(len(params.ex_phases)):
            x = np.linspace(0, params.simLength, int(params.simLength/params.stepSize))
            y = params.ex_amp * np.sin(params.ex_phases[i] + 2 * np.pi * params.ex_freq * x) + params.base
            ax2.plot(x, y, color=params.eng_color_list[i])

        ax2.set_title('Neuron Excitability')
        ax2.set_xlabel('Time (ms)')
        ax2.set_ylabel('Neuron Intrinsic $I_{drive}$')

        eng_color_list = params.eng_color_list
        overlap_color_list = params.overlap_color_list

        for eng_id in range(params.eng_num):
            if params.eng_amps[eng_id] > 0.0:
                plt.axvline(x=params.eng_starts[eng_id], color=eng_color_list[eng_id])
                plt.axvline(x=params.eng_ends[eng_id], color=eng_color_list[eng_id])

        img_path = os.path.join(params.expt_file_path, "{}_raster.png".format(params.expt_name))
        plt.savefig(img_path)


    # Reorders the rows of the connection matrix so as to match the sorted raster plot.
    # Then plots the new matrix.
    if plot_connection_mat:
        reorder_list = []

        for nrn in neuron_list:
            reorder_list.append(nrn.ID)

        reorder_list.reverse()  # Reverses order to match the setup of raster plot.
        reor_mat = nc_Matrix[reorder_list]  # Creates new matrix reor_mat that is the reordered version of nc_Matrix.

        # Plots pixel-plot of neuron connectivities.
        fig, ax_conn = plt.subplots(1, figsize=(12, 12))
        ax_conn.imshow(reor_mat[:, :, 1], extent=(0, numnrn, 0, numnrn),
                                  cmap='cividis')  # Generates pixel-like plot of connection strengths.
        ax_conn.grid(which='both', axis='both', color='black', linewidth=1)
        ax_conn.set_xticks(np.arange(0, numnrn, 1))  # Sets lines for axes, off of which the grid is based.
        ax_conn.set_yticks(np.arange(0, numnrn, 1))
        ax_conn.set_title('Reordered Neuron Connectivity Graphic', size=20)
        ax_conn.set_xlabel('Postsynaptic Neuron ID', size=12)
        ax_conn.set_ylabel('(numnrn - Presynaptic Neuron ID)', size=12)
        
        img_path = os.path.join(params.expt_file_path, "{}_conn_mat.png".format(params.expt_name))
        plt.savefig(img_path)



def frequency(params, neurons, t_start,t_stop): # Function for updating the frequency of excitatory neurons in a network within a given time
    # interval [t_start,t_stop].
    # global neuron
    stepSize = params.stepSize
    ind_start, ind_stop = t_start/stepSize, t_stop/stepSize #Turns times into indices.
    
    for nrn in neurons:
        nrn.frequency = 0 #Resets firing frequency of neuron.

        spikeTimes = np.array(nrn.spikeTimes)
        spikeTimes_in_interval = spikeTimes[(ind_start < spikeTimes) & (spikeTimes < ind_stop)] #Selects only spike time indices that fall
        # between ind_start and ind_stop.

        if len(spikeTimes_in_interval) > 1: # Only considers neurons that have spiked at least twice in the interval.
            # Calculates frequency of neuron firing in the interval and updates attribute. 
            nrn.frequency = round((len(spikeTimes_in_interval)-1)*1000/(stepSize*(spikeTimes_in_interval[-1]-spikeTimes_in_interval[0])) ,3)

    return neurons

def apply_freq_plot(params, neurons, nc_Matrix): # Runs frequency calculation and color changing
    
    for nrn in neurons: #Sets all E neurons to blue initially. 
        if nrn.category == 'Excitatory':
            nrn.color = 'blue'
    
    freq_threshold = 40 #Threshold of neuron frequency to be considered part of an engram (in Hz).
    
    # eng_color_list = ['purple', 'orange']
    # overlap_color_list = ['green']

    eng_color_list = params.eng_color_list
    overlap_color_list = params.overlap_color_list

    for eng_id in range(params.eng_num):    
        neurons = frequency(params, neurons, params.eng_starts[eng_id], params.eng_ends[eng_id])
        for nrn in neurons:
            if nrn.category == 'Excitatory' and nrn.frequency > freq_threshold:
                if eng_id > 0:
                    if nrn.color == eng_color_list[eng_id-1]:
                        nrn.color = overlap_color_list[eng_id-1]
                    else:
                        nrn.color = eng_color_list[eng_id]
                else:
                    nrn.color = eng_color_list[eng_id]

    plot_conn_raster(params, neurons, nc_Matrix)