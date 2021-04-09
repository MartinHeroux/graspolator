import data
import plots
import utils
import randomised_plots

from pathlib import Path


DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')

# --------------------------------------------
# EXPERIMENT 1
# --------------------------------------------
experiment = 'exp1'

all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)
subject_IDs = utils.exp1_subject_folders()

utils.create_exp_folder(experiment)
no_id_plot_numbers = list(range(1, 29))

for plot, (subject_ID, current_subject_data) in enumerate(zip(subject_IDs, all_subject_data), start = 1):
    #utils.create_subject_folder(subject_ID)
    randomised_plots.random_plot(plot, subject_ID, current_subject_data)

utils.merge_pdfs(Path('./randomised_plots_no_ID'))












