import data
import directories

from pathlib import Path


DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')


def import_and_parse_data():
    # set up directory structure
    directories.create_plot_subdirectories()
    # read and process data
    all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)
    return all_subject_data
