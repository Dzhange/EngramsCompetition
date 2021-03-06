import numpy as np



def updateSpikeTime(params, neurons, t_ind):
    tau = 10  # Time constant for exponential function in ms.

    skip_time = 20  # Time before spikes start being recorded (in ms).

    for nrn in neurons:

        # Recording spike times:
        if nrn.solutions[3] >= params.spikeThreshold and nrn.spike == False and (
                t_ind * params.stepSize) > skip_time:  # Selects spikes, skips anything before the first "skip_time" ms.
            nrn.spikeTimes = np.append(nrn.spikeTimes, t_ind)  # Records (time/stepSize) of a spike.
            nrn.spike = True

        if nrn.solutions[
            3] <= -30 and nrn.spike == True:  # Resets the spiking status, allows for next spike to be recorded.
            nrn.spike = False