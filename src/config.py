from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ProjectConfig:
    experiment_version: str="v0"            # name of the training experiment
    experiment_description: str="This is proba."
    
    # General settings
    dir_input: Path=Path("./input/")        # path of the input data
    dir_output: Path=Path("./output/")      # path to save training results
    dir_experiments: Path=Path("./output/experiments")
    verbose: bool=True                      # True: print all the statments
    seed: int=123                           # Random seed for training
    
    
    # Model parameters
    
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

