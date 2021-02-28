#!/usr/bin/env python 

# from enforce_typing import enforce_types # type: ignore[import]
from enforce_typing import enforce_types # type: ignore[import]
import logging
import os
import sys
import pandas as pd

INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING

sys.setrecursionlimit(1500)

# Removing enforce. enforce_typing should be much faster so we don't need the safety toggle.
# enforce.config({'enabled': False})  # Turn off runtime type-checking, for speed

if __name__== '__main__':            
    #set up logging
    logging.basicConfig()
    
    logging.getLogger('master').setLevel(INFO) #INFO, DEBUG
    
    #set help message
    help = """
Usage: run_cadcad MAX_DAYS OUTPUT_DIR [DO_PROFILE]

 MAX_DAYS -- float -- # days to simulate
 OUTPUT_DIR -- string -- output directory for csv file & state db files.
 DO_PROFILE -- bool -- if True, profile. Otherwise don't. Defalt=False.
 """

    #got the right number of args?  If not, output help
    num_args = len(sys.argv) - 1
    num_args_needed = [2, 3]
    if num_args not in num_args_needed:
        print(help)
        if num_args > 0:
            print("Got %d argument(s), need %s.\n" % (num_args, num_args_needed))
        sys.exit(0)
    
    #extract inputs
    max_days = eval(sys.argv[1])
    output_dir = sys.argv[2]
    do_profile = False
    if num_args == 3 and sys.argv[3] == 'True':
        do_profile = True

    print("Arguments: MAX_DAYS=%s, OUTPUT_DIR=%s, DO_PROFILE=%s\n" %
          (max_days, output_dir, do_profile))

    #handle corner cases
    if os.path.exists(output_dir):
        print("\nOutput path '%s' already exists.  Exiting.\n" % output_dir)
        sys.exit(0)

    # make directory
    # os.mkdir(output_dir)


    # Experiments
    import run

    experiments = run.run()

    # Get the ABM results
    agent_ds = experiments.dataset[0].agents
    state_ds = experiments.dataset[0].state
    staked_ds = experiments.dataset[0].total_staked
    
    for staked in staked_ds:
        print(staked)
    
    # for stats in state_ds:
    #     # for state in stats.values():
    #         for k, val in stats.__dict__.items():
    #             if k == 'kpis':
    #                 print(val.__dict__)
