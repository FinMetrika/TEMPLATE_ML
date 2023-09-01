import sys
import logging
from config import ProjectConfig
from utils import update_config


logging.basicConfig(filename="program_log.txt",
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


#################################
def main():
    # Instantiate the config dataclass
    FLAGS = ProjectConfig()
    update_config(FLAGS)
    logging.info(f"Configuration: {FLAGS}")




if __name__ == '__main__':
    #logging.info(f"Program started with arguments: {FLAGS}")
    main()