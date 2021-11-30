import numpy as np

def updateExitability(params, neurons, t_ind):
    
    for nrn in neurons:
        if nrn.category == 'Excitatory':
            nrn.Idrive = nrn.ex_amp * np.cos(nrn.phase + 2*np.pi * nrn.freq * t_ind) 