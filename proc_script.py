from pathlib import Path

import data
import plots
import utils
from pathlib import Path

DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')

# --------------------------------------------
# EXPERIMENT 1
# --------------------------------------------

all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)

subject_IDs = utils.exp1_subject_folders()

for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    plots.visual_check_and_store(subject_ID, current_subject_data)
    #plots.regplots(subject_ID, current_subject_data)










