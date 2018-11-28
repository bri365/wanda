
from wandapi import config

# default values
BASE_DIR = config.wanda['base_dir']


def init_config(base_dir):
    """Initialization, called at application startup."""
    global BASE_DIR

    BASE_DIR = base_dir


def get_base_dir():
    """Fetch current base directory, production or test, set by initialization."""
    global BASE_DIR
    return BASE_DIR
