
import numpy as np



def updateSyn(params, neurons, t_ind):  # Gives synaptic input to all neurons on connection list
    # Includes changes in synaptic strengths. t_start is the time at which the presynaptic neuron's voltage breaches -20 mV.
    # Has been changed to normalize strength of inputs to a neuron by number of inputs. I.e sum of all inputs comes to w_max.
    t_temp = 0

    # AMPA connections
    w_EE = 0.15
    w_EI = 0.15
    # GABA A connections
    w_II = 0.15
    w_IE = 0.15
    # GABA B connections
    w_II_B = 0.05
    w_IE_B = 0.05

    tau = 0.5  # Time constant for fast-acting receptors.
    tau_B = 50  # Time constant for GABA B receptors, slow-acting.

    stepSize = params.stepSize
    for nrn in neurons:  # presynaptic neurons.
        if len(nrn.spikeTimes) > 0:  # To prevent errors of calling [-1] from an array without any entries. Can change to be l > 2, 3 ...
            t_temp = nrn.spikeTimes[-1]  # grabs time this neuron spikes at.

            for conn in nrn.connections:  # Gives all postsynaptic neurons Isyn corrspondping to their voltage.
                V = neurons[int(conn[0])].solutions[
                    3]  # Voltage of postsynaptic neuron. Note conn[1] is the connection strength and conn[0] is the ID.
                Isyn = 0

                if nrn.category == 'SST' or nrn.category == 'PV+':  # Handles GABA A and B receptors in postsyn  neurons.
                    E_syn = -75  # Chloride reversal potential.
                    if neurons[int(conn[0])].category == 'SST' or neurons[
                        int(conn[0])].category == 'PV+':  # For I-I connections.
                        for w, t in (w_II, tau), (
                        w_II_B, tau_B):  # Sends two signals, one with w_II/tau and one with w_II_B/tau_B.
                            Isyn += conn[1] * (w) * np.exp(-stepSize * (t_ind - t_temp) / t) * (
                                        V - E_syn)  # t is tau here.
                    if neurons[int(conn[0])].category == 'Excitatory':  # For I->E connections.
                        for w, t in (w_IE, tau), (w_IE_B, tau_B):
                            Isyn += conn[1] * (w) * np.exp(-stepSize * (t_ind - t_temp) / t) * (
                                        V - E_syn)  # t = tau again.

                        # Recording inhibitory input to each LE neuron:
                        if neurons[int(conn[0])].backbone_ID == 0 and t_ind % (1 / stepSize) == 0:
                            for w, t in (w_IE, tau), (w_IE_B, tau_B):
                                neurons[int(conn[0])].i_current_hist[int(t_ind * stepSize)][0] += conn[1] * (
                                    w) * np.exp(-stepSize * (t_ind - t_temp) / t) * (V - E_syn)  # t = tau again.
                                # print(nrn.i_current_hist[int(t_ind*stepSize)][0], 'time ', t_ind*stepSize)

                if nrn.category == 'Excitatory':
                    E_syn = 0  # Sodium reversal potential. E_syn = 0 for excitory synapse and E_syn = -75 mV for inhibitory synapse
                    if neurons[int(conn[0])].category == 'SST' or neurons[
                        int(conn[0])].category == 'PV+':  # For E->I connections.
                        Isyn = conn[1] * (w_EI) * np.exp(-stepSize * (t_ind - t_temp) / tau) * (V - E_syn)
                    if neurons[int(conn[0])].category == 'Excitatory':  # For E-E connections.
                        Isyn = nrn.connectionWeights[int(conn[0])] * conn[1] * (w_EE) * np.exp(
                            -stepSize * (t_ind - t_temp) / tau) * (V - E_syn)

                neurons[int(conn[0])].Input_syn += Isyn  # Isyn going to Postsynaptic neuron.
