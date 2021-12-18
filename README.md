# EngramsCompetition
MATH 568 Course Project

## How to start

Simply run 
`python main.py -c engrams.yaml`


## About Experiment logging

A simple parameter parser to help  record each experiment's setting and results, it basically has 3 parts:

1. `parameter_parser.py` script, all default parameters are stored in it. It was called in the main script and returns a parameter set. We should try to avoid directly change parameters in this file, instead we could use configuration files as below.
2. `configs` folder contains all the experiment configuration files. Only parameters different from default need to be written in the config file(You might feel like to change the 'expt_name' in each config file). You could check the `example.yaml` for reference.
3. `logs` folder stores all experiments we want to preserve or upload. Each experiment results will be stored in a folder with the name "expt_name" in the configuration file.

To use a customized config file, simpy run
``python main.py -c your_configuration_file.yaml``
Note that the full path to the configuration file is not necessary, only use file name is also fine.

If no customized config file is provided, the model will run on default parameters and store in `logs/expt` folder
