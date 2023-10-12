import sys, logging
from datetime import datetime
import torch
from config import ProjectConfig


def update_config(FLAGS):
    """
    Update config arguments if any change was done via CLI when
    running "sh run.sh". FLAGS argument is instantiation of the
    Config dataclass.
    """
    for i in range(1, len(sys.argv),2):
        attr_name = sys.argv[i]
        attr_value = sys.argv[i+1]
    
        if hasattr(FLAGS, attr_name):
            setattr(FLAGS, attr_name, attr_value)
        else:
            logging.warning(F'No such attribute: {attr_name}')

      
def check_device():
    """
    Check which device is available to use.
    """
    FLAGS = ProjectConfig()
    
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    if FLAGS.verbose: 
        print(f'Using {device} device!')

    return device


def create_experiment_descr_file(config: ProjectConfig):
    """Create a txt file to include information on
    experiment including all the parameters used.

    Args:
        config (ProjectConfig): project parameters
    """
    # Get the parameters
    exp_description, exp_params = config.export_params()
    
    # Where to create the file
    file_path = config.dir_experiments/config.experiment_version/"experiment_info.txt"
    
    with open(file_path, "w") as f:
        f.write(f'EXPERIMENT DESCRIPTION:\n{exp_description}\
            \n\nMODEL PARAMETERS:\n')
        for key, value in exp_params.items():
            # Exclude already used information
            if key not in ["experiment_version",
                           "experiment_description"]:
                f.write(f"{key}:{value}\n")


def add_runtime_experiment_info(start_time, config:ProjectConfig):
    exp_file_path = config.dir_experiments/config.experiment_version/"experiment_info.txt"
    end_time = datetime.now()
    dtime = end_time-start_time
    with open(exp_file_path, "a") as f:
        f.write(f'\nTIME END: {end_time.strftime("%Y-%m-%d %H:%M:%S")}\nRUN TIME: {dtime}')
