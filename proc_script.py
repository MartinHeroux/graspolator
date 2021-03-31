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

subject_data = data.read_exp1(DATA_FOLDER_EXP1)[0]
widest_lines = data.read_exp1(DATA_FOLDER_EXP1)[1]

subject_IDs = utils.exp1_subject_folders()
names_and_data_zip = zip(subject_IDs, subject_data)

for ID, data in names_and_data_zip:
    plots.visual_check_and_store(ID, data)

for ID, data in names_and_data_zip:
    plots.regplots(ID, data)