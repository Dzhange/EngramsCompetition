import numpy as np

def updateExcitability(params, neurons, t_ind):
    
    for nrn in neurons:
        if nrn.category == 'Excitatory':            
            nrn.Idrive = nrn.ex_amp * np.sin(nrn.ex_phase + 2*np.pi * nrn.ex_freq * t_ind * params.stepSize) + params.base

def applyEngramCurrent(params, neurons, t_ind):

    assert params.eng_num == len(params.eng_amps)

    for eng_id in range(params.eng_num):
        if params.eng_starts[eng_id] <= t_ind < params.eng_ends[eng_id]:            
            for nrn in neurons:
                if nrn.category == 'Excitatory':
                    nrn.Idrive = nrn.Idrive + params.eng_amps[eng_id]
