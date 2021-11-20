
import numpy as np

# It is important to leave numEquations and stepSize here, as they affect the integration.
numEquations = 4
stepSize = 0.1
simLength = 200
tarray = np.arange(0,simLength,stepSize)
Ntimes = len(tarray)

spikeThreshold = 5 # Sets the voltage(mV) at which a spike is recorded.

numnrn = 50 # Number of neurons in the model.

numPV = 10 # Number of SST neurons to be forced into the model.


c_e, c_i = 0.1, 0.5 # Percent connectivity. Excitatory, Inhibitory.
p_e, p_i = 0.8, 0 # Probability of an existing connection breaking and forming a new connection. Excitory, Inhibitory.
# NOTE inhibitory connections are assigned randomly from the start, so there is no need to rewire.
local_conn = True # When true, new connections can be formed with local connections. When false, only non-local new
# connections are formed.

RD_seed = True # When true, a seed is used to generate connections
seed = 1 # The seed for generating random numbers/list indices. NOTE: defining a seed before a sequence of random events will
# not only define the outcome of the first random choice/event, but ALSO the following ones. So we only need one seed.

Idrive_E_min, Idrive_E_max = 0.1, 0.1 # Applied current range for excitatory neurons.
Idrive_PV_min,Idrive_PV_max = -0.1, -0.1 # Applied current range for inhibitory PV+ neurons.