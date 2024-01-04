import sys, logging, platform, random
from datetime import datetime
import numpy as np
import torch
from config import ProjectConfig


def set_all_seeds(seed):
    """Set the seed for all packages.

    Args:
        seed (int): Positive integer value.
    """
    random.seed(seed)  # python 
    np.random.seed(seed)  # numpy
    torch.manual_seed(seed)  # torch
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)  # torch.cuda
    torch.mps.manual_seed(seed) # mps


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


def moveTo(obj:list, device:str):
    """Move an object to a specified device if the object if of certain type.
    Ref: Inside Deep Learning by E. Raff (page 15)
    Args:
        obj (list): list of Python objects
        device (str): the compute device to move objects to
        
    Examples:
        some_tensors = [torch.tensor(1), torch.tensor(2)] 
        print(some_tensors) 
        print(moveTo(some_tensors, device)) 
        [tensor(1), tensor(2)]
        [tensor(1, device='cuda:0'), tensor(2, device='cuda:0')]
    
    Explanation of the example:
        This is a recursive algorithm. It takes in a list of objects,
        in this case a list of tensors, so a first isinstance is envoked.
        Then it return a list comprehension which iterated over each
        element in a list and applies the same recursive algorithm, i.e. 
        it starts to check again. Now since we have a tensor, it is not a list,
        a tuple, a set or a dict, but a tensor which has a "to" method, and hence
        it returns obj.to(device) and sends it to a device specified.
        The base for this recursive algorithm is that i is neither of the above
        and returns the initial object unchanged.
    """
    if isinstance(obj, list): 
        return [moveTo(x, device) for x in obj] 
    elif isinstance(obj, tuple): 
        return tuple(moveTo(list(obj), device)) 
    elif isinstance(obj, set): 
        return set(moveTo(list(obj), device)) 
    elif isinstance(obj, dict): 
        to_ret = dict() 
        for key, value in obj.items(): 
            to_ret[moveTo(key, device)] = moveTo(value, device) 
        return to_ret 
    elif hasattr(obj, "to"): 
        return obj.to(device) 
    else: 
        return obj


def get_python_version():
    return sys.version.split()[0]


def get_package_version(package_name):
    try:
        package = __import__(package_name)
        return package.__version__
    except ImportError:
        return "Not Installed"
    

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
        f.write(f'\n\nPython Version: {get_python_version()}')
        f.write(f'\nOS: {platform.system()} {platform.release()}')
        f.write(f'\nTorch Version: {get_package_version("torch")}')
        f.write(f'\nTransformers Version: {get_package_version("transformers")}')
        f.write(f'\nNumPy Version: {get_package_version("numpy")}')
        f.write(f'\nPandas Version: {get_package_version("pandas")}')