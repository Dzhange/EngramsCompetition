"""
Set default configurations and read user_defined files
"""
import os
import shutil
from os.path import join
from yacs.config import CfgNode as CN
import numpy as np
import argparse


class parameter_parser():
    
    def __init__(self):
        self.set_default_cfg()
        self.load_cfg()
        self.check_cfg()
    
    def get_cfg(self):
        cfg = self.cfg
        cfg.freeze()
        return cfg

    def set_default_cfg(self):
        self.cfg = CN()
        # dataset    
        # It is important to leave numEquations and stepSize here, as they affect the integration.
        self.cfg.numEquations = 4
        self.cfg.stepSize = 0.1
        self.cfg.simLength = 200
        
        
        self.cfg.spikeThreshold = 5 # Sets the voltage(mV) at which a spike is recorded.
        
        self.cfg.numnrn = 50 # Number of neurons in the model.
        self.cfg.numPV = 10 # Number of SST neurons to be forced into the model.
        
        self.cfg.c_e, self.cfg.c_i = 0.1, 0.5 # Percent connectivity. Excitatory, Inhibitory.
        self.cfg.p_e, self.cfg.p_i = 0.8, 0 # Probability of an existing connection breaking and forming a new connection. Excitory, Inhibitory.
        
        # NOTE inhibitory connections are assigned randomly from the start, so there is no need to rewire.
        self.cfg.local_conn = True # When true, new connections can be formed with local connections. When false, only non-local new
        
        # connections are formed.
        self.cfg.RD_seed = True # When true, a seed is used to generate connections
        self.cfg.seed = 1 # The seed for generating random numbers/list indices. NOTE: defining a seed before a sequence of random events will
        
        # not only define the outcome of the first random choice/event, but ALSO the following ones. So we only need one seed.
        self.cfg.Idrive_E_min, self.cfg.Idrive_E_max = 0.1, 0.1 # Applied current range for excitatory neurons.
        self.cfg.Idrive_PV_min, self.cfg.Idrive_PV_max = -0.1, -0.1 # Applied current range for inhibitory PV+ neurons.
        
        self.cfg.random_activate = False # Randomly apply stronger current to some excitatory neurons and lower current to the rest
        self.cfg.activate_rate = 0.2 # The ratio of neurons applied with higher neurons at initialization
        self.cfg.activate_strengthen_scale = 1.5
        self.cfg.activate_weaken_scale = 0.6

        
        #experiment configs
        self.cfg.log_parent_dir = "./logs"
        self.cfg.config_parent_dir = "./configs"
        self.cfg.expt_name = "expt"

        # AMPA connections
        self.cfg.w_EE = 0.15
        self.cfg.w_EI = 0.15
        # GABA A connections
        self.cfg.w_II = 0.15
        self.cfg.w_IE = 0.15
        # GABA B connections
        self.cfg.w_II_B = 0.05
        self.cfg.w_IE_B = 0.05
        self.cfg.tau = 0.5  # Time constant for fast-acting receptors.
        self.cfg.tau_B = 50  # Time constant for GABA B receptors, slow-acting.


    def check_cfg(self):
        pass

    def merge_from_cmdline(self):        
        """
        Merge some usually changed setting from comand line
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', '-c', type=str, default='None', help="Choose a config file")
        cmd = vars(parser.parse_args())  # use as dict                
        return cmd
        

    def load_cfg(self):                
        # First merger from cmdline
        cmd = self.merge_from_cmdline()                
        # merge local file, cmd>file
        if cmd['config'] != 'None':            
            if os.path.exists(cmd['config']): # full path
                self.cfg.config_file = cmd['config']
            else: #only file name
                self.cfg.config_file = os.path.join(self.cfg.config_parent_dir, cmd['config'])
            self.cfg.merge_from_file(self.cfg.config_file)
            
        if self.cfg.expt_name == "time_now":
            from datetime import datetime
            now = datetime.now()
            self.cfg.expt_name = now.strftime("D%dM%mY%Y_H%HM%MS%S")

        self.cfg.expt_file_path = os.path.join(self.cfg.log_parent_dir, self.cfg.expt_name)        
        # make a second copy, sometimes the origin params file could be accidentally lost
    
        if not os.path.exists(self.cfg.expt_file_path):
            os.mkdir(str(self.cfg.expt_file_path))
        shutil.copy(self.cfg.config_file, self.cfg.expt_file_path)
        self.gen_secondary_parameters()
        
    def gen_secondary_parameters(self):
        # generate parameters that dependent on others
        self.cfg.tarray = list(np.arange(0,self.cfg.simLength,self.cfg.stepSize))
        self.cfg.Ntimes = len(self.cfg.tarray)