import os, logging, random
from datetime import datetime
import numpy as np
import torch
from src.pconfig import ProjectConfig
from finmetrika_ml import utils


logging.basicConfig(filename="program_log.txt",
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


#################################
def main():
    stime = datetime.now()
    
    # Instantiate the config dataclass
    FLAGS = ProjectConfig()
    utils.update_config(FLAGS)
    logging.info(f"Configuration: {FLAGS}")

    # Random seeds
    utils.set_all_seeds(FLAGS.seed)
        
    # Create a folder for the experiment if there is None
    if not os.path.isdir(FLAGS.dir_experiments/FLAGS.experiment_version):
        os.mkdir(FLAGS.dir_experiments/FLAGS.experiment_version)
    
    # Create a file with the description and experiment parameters
    utils.create_experiment_descr_file(FLAGS)
    
    # ===== MAIN CODE =====





    # ===== END OF MAIN CODE =====
    # Update the experiment_info.txt file
    utils.add_runtime_experiment_info(stime, FLAGS)
    
if __name__ == '__main__':
    #logging.info(f"Program started with arguments: {FLAGS}")
    main()