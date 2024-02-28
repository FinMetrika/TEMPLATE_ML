from dataclasses import dataclass, asdict, field
from pathlib import Path


# Get the absolute path to the directory where config.py is located
BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class ProjectConfig:
    # Documenting experiments
    experiment_version: str = field(
        default="v0",
        metadata={'description': "Name of the training experiment"})
    
    experiment_description: str = field(
        default="This is test run",
        metadata={'description': "Describe the experiment in couple of sentences"})
    
    # General settings
    # General settings
    dir_input: Path = field(default_factory = lambda: BASE_DIR / "input")       # path of the input data
    dir_data: Path = field(default_factory=Path('/Users/icdonev/Developer/datasets/bank-trx/input/'))
    dir_output: Path = field(default_factory=lambda: BASE_DIR / "output")      # path to save training results
    dir_models: Path = field(default_factory=lambda: BASE_DIR / "models")
    dir_experiments: Path=Path("./output/experiments")
    
    verbose: bool=True                      # True: print all the statments
    seed: int=123                           # Random seed for training
      
    # Model parameters
    
    
    def __post_init__(self):
        directories = [
            self.dir_input,
            self.dir_models,
            self.dir_output,
            self.dir_experiments
        ]
        for directory in directories:
            if not os.path.exists(directory):
                directory.mkdir(parents=True, exist_ok=True)


    # Export parameters
    def export_params(self):
        """Export parameters used for a particular experiment
        so that it can be added into log documents.
        """
        exp_description = self.experiment_description
        exp_parameters = asdict(self)
        return exp_description, exp_parameters


# from argparse import ArgumentParser

# parser = ArgumentParser()

# def get_args():
#     parser.add_argument(
#         "--data_dir_path",
#         default="../input/",
#         help="File directory for input data."
#     )

#     parser.add_argument(
#         "--file_names",
#         help="File name or names to be imported. If more than one file enclose in a list. Concat index should be the same in all files."
#     )

#     return parser.parse_args()

