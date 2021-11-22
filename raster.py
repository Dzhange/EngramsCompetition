
import os
import numpy as np
import matplotlib.pyplot as plt
# from parameters import stepSize, numnrn


def plot_conn_raster(params, neurons, start_time, nc_Matrix):  # Plots raster plot and connectivity matrix.
    
    stepSize, numnrn = params.stepSize, params.numnrn
    
    plot_raster = True
    plot_connection_mat = True

    list_i, list_e = [], []
    for nrn in neurons:  # Seperates neuron IDs into a list of inhibtory and excitory.
        if nrn.category == 'SST' or nrn.category == 'PV+':
            list_i.append(nrn)  # Appends full nrn object (not just the ID) to make sorting by gsyn easier.
        if nrn.category == 'Excitatory':
            list_e.append(nrn)

    neuron_list = list_i + list_e  # Adds the two lists such that inhibitory neurons come first and excitory second.

    if plot_raster:  # Plots raster plot of neuron spikes. Ordered with inhibitory on the bottom, followed by sorted E neurons.
        fig, ax1 = plt.subplots(1, figsize=(20, 5))
        start = start_time / stepSize  # time to start plotting from.

        for index, nrn in enumerate(neuron_list):
            spikeTimes_toplot = []

            for t in nrn.spikeTimes:  # Runs through spike times of every neuron in 'neuron_list', starting with inhibitory.3
                if t >= start:  # only selects times greater than 'start' for plotting.
                    spikeTimes_toplot = np.append(spikeTimes_toplot, t * stepSize)

            index_plot_list = [index] * len(spikeTimes_toplot)

            color = nrn.color  # Color of spikes plotted for this neuron on raster plot.

            ax1.scatter((spikeTimes_toplot), index_plot_list, c=color,
                        s=2)  # c controls nrn dot color, s controls dot size.

        ax1.set_title('BB Raster Plot')
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Neurons Sorted by Group')        
        
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
