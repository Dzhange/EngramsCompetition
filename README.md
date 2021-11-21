# EngramsCompetition
MATH 568 Course Project


## About Experiment logging

Ge: I guess in the very near future we will need to do a bunch of experiments with different parameters, so I wrote a simple parameter parser to help us record each experiment's setting and results, it basically has 3 parts:

1. `parameter_parser.py` script, all default parameters are stored in it. It was called in the main script and returns a paramer set.
2. `configs` folder contains all the experiment configuration files. Only parameters different from default need to be written in the config file(You might feel like to change the 'expt_name' in each config file). You could check the `example.yaml` for reference.
3. `logs` folder stores all experiments we want to preserve or upload. Each experiment results will be stored in a folder with the name "expt_name" in ythr configuration file.

To use a customized config file, simpy run
``python main.py -c your_configuration_file.yaml``
Note that the full path to the configuration file is not necessary, only use file name is also fine.