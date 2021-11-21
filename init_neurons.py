
import numpy as np
import parameters as param
from neuron import neuron
import random as rd


# initializes neurons and assigns ID, connections, weights, etc.
def init_nrn(numnrn):
    neurons = []  # List containing neuron objects
    nconn_Mat = [np.empty(3)]  # 2D matrix for storing new connections.

    if param.RD_seed:  # When true, the simulation will be reproducable entirely (all connections, neuron assignments, initial coniditions).
        rd.seed(param.seed)

    def count_PV(neurons):  # A function for counting the number of SST neurons.
        count = 0
        for nrn in neurons:
            if nrn.category == 'PV+':
                count += 1
        return count

    for i in range(numnrn):
        neurons = np.append(neurons, neuron())  # Initializes numnrn number of neurons

    # This for loop ensures that exactly numPV number of E neurons are changed to PV.
    for i in range(param.numPV):
        changed_to_PV = False  # Keeps loop running until excitatory neuron is found to change to PV neuron.
        while changed_to_PV == False:  # Loop mentioned above.
            nrn = rd.choice(neurons)  # grabs one neuron object at random (available for editing)
            if nrn.category == 'Excitatory':  # If true, turns excitatory neuron to PV. If neuron is not Excitatory, while loop runs again.
                nrn.category = 'PV+'
                changed_to_PV = True

    # Create list of only E neurons.
    Eneurons = []
    for nrn in neurons:
        if nrn.category == 'Excitatory':
            Eneurons.append(
                nrn)  # Note that even though this is a different list than neurons, the neuron objects within can be
            # changed all the same like they were in neurons.

    ID = 0
    for nrn in neurons:  # assigns neurons in list their IDs, init voltage, Idrive, etc.
        nrn.ID = ID
        ID += 1
        nrn.spikeTimes = []
        nrn.solutions = [rd.random(), rd.random(), rd.random(), rd.uniform(-55,
                                                                           -20)]  # Initial conditions of each neuron. Initial voltage randomly assigned between -55 and -20 mV.
        nrn.connectionWeights = [1] * numnrn  # Creates a list of all connection weights to other neurons at value 1.

        if nrn.category == 'Excitatory':
            if param.random_activate:
                drive_scale = param.activate_strengthen_scale if rd.random() <= param.activate_rate else param.activate_weaken_scale
                nrn.Idrive = drive_scale * round(rd.uniform(param.Idrive_E_min, param.Idrive_E_max),
                                3)  # Random value between min and max rounded to 1 decimal places
            else:
                nrn.Idrive = round(rd.uniform(param.Idrive_E_min, param.Idrive_E_max),
                                3)  # Random value between min and max rounded to 1 decimal places
            nrn.color = 'Blue'

        if nrn.category == 'PV+':
            nrn.Idrive = round(rd.uniform(param.Idrive_PV_min, param.Idrive_PV_max), 3)
            nrn.color = 'darkorange'

    conn_Matrix = np.zeros((numnrn,
                            numnrn))  # initializes matrix of zeros with numnrn x numnrn size. Row = nrn ID, Column = connected nrn ID.

    # Fills matrix with connectivity based on proximity. conn_span neurons to right and left are given connections.
    for row_index, row in enumerate(conn_Matrix):
        for column_index, conn in enumerate(row):

            if neurons[
                row_index].category == 'Excitatory':  # Determines which connectivity percent to use based on neuron category.
                conn_span = int(param.c_e * numnrn / 2)  # number of neurons to be connected on either side of a neuron.

                # sets neurons at +- conn_span from diagonal to full connectivity.
                if column_index >= row_index - conn_span and column_index <= row_index + conn_span:
                    conn = 1
                    # Full connectivity at edge case of first neurons connected to last neurons in ring.
                elif row_index - conn_span < 0 and column_index >= numnrn + row_index - conn_span:
                    conn = 1
                # Full connectivity at edge case of last neurons connected to first neurons in ring.
                elif row_index + conn_span > (numnrn - 1) and column_index <= row_index - numnrn + conn_span:
                    conn = 1
                    # All other neurons have zero connectivity.
                else:
                    conn = 0
                # Sets diagonal entries to zero.
                if column_index == row_index:
                    conn = 0

            elif neurons[row_index].category == 'SST' or neurons[
                row_index].category == 'PV+':  # If the presynaptic neuron is inhibitory.
                if rd.random() <= param.c_i and column_index != row_index:  # if a random between 0 and 1 is less than the connectivity percent.
                    conn = 1
                else:
                    conn = 0

            row[column_index] = conn  # Assigns the local connections.
        conn_Matrix[row_index] = row

    # Changes connections based on probability p.
    for row_index, row in enumerate(conn_Matrix):
        row_temp = row.copy()  # used to store changes while deleting connections from new_conn_list. VERY IMPORTANT TO USE .copy()
        # otherwise row will change when row_temp is changed. This is how assignment works.
        if neurons[
            row_index].category == 'Excitatory':  # Determines which connectivity percent to use based on neuron category.
            conn_span = int(param.c_e * numnrn / 2)  # number of neurons to be connected on either side of a neuron.
            p = param.p_e
        elif neurons[row_index].category == 'SST' or neurons[row_index].category == 'PV+':
            conn_span = int(param.c_i * numnrn / 2)
            p = param.p_i

        for column_index, conn in enumerate(row):

            if conn != 0:  # only for existing connections.
                if rd.random() <= p:  # rd.random() selects random float between 0 and 1.

                    if param.local_conn == True:  # Allows new local connections.
                        new_conn_list = np.append(np.arange(0, row_index, 1),
                                                  np.arange(row_index + 1, numnrn, 1))  # Creates list of
                        # all nrn IDs besides self.
                    if param.local_conn == False:  # No new local connections.
                        # List of all nrns except local and self. Very gross and uses heaviside functions. May be simplifiable.
                        new_conn_list = np.append(np.arange(numnrn - numnrn * np.heaviside(row_index - conn_span - 1, 1)
                                                            + (row_index + conn_span - numnrn + 1) * np.heaviside(
                            row_index + conn_span - numnrn, 1), row_index - conn_span, 1),
                                                  np.arange(row_index + conn_span + 1,
                                                            (numnrn + row_index - conn_span) -
                                                            (row_index - conn_span) * np.heaviside(
                                                                row_index - conn_span, 1), 1))

                    for index, val in enumerate(
                            row_temp):  # Deletes established conns from new_conn_list, preventing double connections.

                        if val != 0:  # Sorts out only established conns.
                            delindex = np.where(new_conn_list == index)  # Finds where est. conn lies in new_conn_list.
                            if len(delindex[
                                       0]) > 0:  # Stops error from having nothing to delete when local_conn = False.
                                delindex = delindex[0][0]  # grabs useful integer.
                                new_conn_list = np.delete(new_conn_list, delindex)  # deletes from possible conns.

                    nconn = rd.choice(new_conn_list)  # Randomly selects one neuron to connect to.
                    nconn_info = [
                        [row_index, column_index, nconn]]  # [neuron #, old connection, new connection]. Must be 2D.
                    nconn_Mat = np.concatenate((nconn_Mat, nconn_info))  # Adds this info to a matrix for later use.

                    # Updates values of the array used in determining new connections.
                    row_temp[int(column_index)] = 0
                    row_temp[int(nconn)] = 1

    nconn_Mat = np.delete(nconn_Mat, 0, 0)  # Removes np.empty dummy row from matrix.

    # Apply new connection changes.
    for info in nconn_Mat:
        conn_Matrix[int(info[0]), int(info[1])] = 0  # Sets old connection to zero.
        conn_Matrix[int(info[0]), int(info[2])] += 1  # Establishes connection or adds another connection.

    nc_Matrix = np.empty(
        (numnrn, numnrn, 2))  # Empty matrix to hold final values. nc means neuron # and connection strength.
    count = 0

    # Creates 3D array, nc_matrix, storing (nrn #, conn strength to nrn receiving Isyn)
    for row in conn_Matrix:
        conn_tuple = list(enumerate(row))  # list of tuples with info (postsyn nrn #, recieving nrn conn strength)
        nc_Matrix[count] = conn_tuple
        count += 1

    # Assigns neuron objects the list of tuple connections.
    for nrn in neurons:
        nrn.connections = nc_Matrix[nrn.ID]  # Outgoing connections for nrn.
        nrn.conn_in = nc_Matrix[:, nrn.ID][:,
                      1]  # Incoming connections for nrn. [0,0,1,1] would mean this neuron recieves no
        # signal from neurons 0 and 1, and full signal from neurons 2 and 3.

    return neurons, nc_Matrix


neurons, nc_Matrix = init_nrn(param.numnrn)  # initializes neurons and creates universal list.
