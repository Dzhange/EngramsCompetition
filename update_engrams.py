import numpy as np

def updateExcitability(params, neurons, t_ind):
    
    for nrn in neurons:
        if nrn.category == 'Excitatory':            
            nrn.Idrive = nrn.ex_amp * np.sin(nrn.ex_phase + 2*np.pi * nrn.ex_freq * t_ind * params.stepSize) + params.base

def applyEngramCurrent(params, neurons, t_ind):

    assert params.eng_num == len(params.eng_amps)

    for eng_id in range(params.eng_num):
        if params.eng_starts[eng_id] <= t_ind*params.stepSize < params.eng_ends[eng_id]:
            for nrn in neurons:
                if nrn.category == 'Excitatory' and nrn.use_engram[eng_id]:
                    nrn.Idrive = nrn.Idrive + params.eng_amps[eng_id]


def dotp_ortho(params, neurons, engram_starts, engram_ends):
    # Defines vec of E neuron objects
    E_neurons = []
    for nrn in neurons:
        if nrn.category == 'Excitatory':
            E_neurons.append(nrn)

    assert len(engram_starts) == len(engram_ends)

    # Holds two vectors, one for each engram. Each element of each vec will hold the number of times a neuron spikes in the engram
    # stimulus time span
    engram_vecs = np.array([np.zeros(len(E_neurons)), np.zeros(len(E_neurons))])

    for i, (start_time, end_time) in enumerate(zip(engram_starts, engram_ends)):  # Loops over engram stimulus times
        for index, E_nrn in enumerate(E_neurons):  # Loop over all E neurons

            for spike_ind in E_nrn.spikeTimes:  # Loops through the spike times of each E neuron
                if start_time < spike_ind * params.stepSize < end_time:  # Selects spikes that occur within engram stimulus time

                    engram_vecs[i][index] += 1  # Adds one count to vector element

    # Now we normalize the vectors
    for i in range(len(engram_vecs)):
        engram_vecs[i] = engram_vecs[i] / np.sqrt(np.dot(engram_vecs[i], engram_vecs[i]))

    print(np.dot(engram_vecs[0], engram_vecs[1]))  # Prints dotp result
