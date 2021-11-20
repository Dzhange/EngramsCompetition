
import numpy as np
import parameters as param

# Defines attributes of each neuron
class neuron:
    def __init__(self):
        self.ID = 0
        self.position = []
        self.connections = []  # List of (1 or 0) connection strengths to other neurons. Is tuple like [[postsyn,conn],[postsyn,conn]...].
        # DO NOT CHANGE self.connections from values of only 1 and 0 because many apects of the program rely on it.
        self.connectionWeights = []  # Holds changes made from plasticity. For self as presynaptic nrn. Values are strengths of
        # signal to other neurons from this neuron.
        self.Input_syn = 0
        self.Input_noise = 0
        self.Input_external = 0
        self.spikeTimes = []  # Set to record a spike when membrane voltage breaches variable spikeThreshold.
        self.prevActivity = 0
        self.neuronsInRange = []  # Tracks the # of neurons in range so as to minimize looping time during connection growth function
        self.solutions = np.zeros(param.numEquations)  # Why does nrn.solutions still function as a comment?

        # Things I have added in myself:
        self.spike = False  # Determines whether the neuron has already spiked or not.
        self.Idrive = 0
        self.color = ''  # Color of neuron for graphing.
        self.conn_in = []  # Connections coming in from other neurons. Sum is the in-degree of the neuron. Note, not tuple like self.connections.
        # Format is 1D list of connection strengths, where list index is presynaptic neuron.
        self.category = 'Excitatory'  # Labels the neuron type. Default is excitatory, can be chanegd to inhibitory.
        self.gsyn = 1  # Connection strength multiplier.
        self.pair_spiketimes = np.zeros(
            param.numnrn)  # Pair spike times for outgoing connections. Note that this only holds the most recent pair spiketime for each conn.
        self.start_noise = 0  # Starting step time for noise when it occurs (mV/stepSize).
        self.backbone_ID = 0  # backbone_ID=0 will be used to designate lower E neurons and -1 for inhibitory neurons.
        self.spike_gaussian = []  # List of gaussian curves, each centered at the time a neuron spikes. Each index in list corresponds to a t_ind time.
        self.plas_on = True  # Boolean determining whether or not to change plasticity of connections TO and FROM this nrn.
        self.cw_in_history = []  # Connection weight history. Holds plasticity connection weights coming IN (this nrn as postsyn).
        # Set up as [[[weight from nrn 0, weight from nrn 1, ... ],time(ms)] ,...], one weight list for each milisecond.
        # List set up to skip first 500 ms because we don't want plasticity due to transient behaviors. Note the default
        # value for connections and non-existent connections is 1.
        self.scatter_color = 'grey'
        self.scatter_quad_color = 'grey'
        self.i_current_hist = np.array(
            [[0, time] for time in range(param.simLength)])  # Net inhibitory current to this neuron
        # every ms. [ [net current, time(ms)] , ...]
