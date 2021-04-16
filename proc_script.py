import data
import plots
import utils

from pathlib import Path


DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')

# --------------------------------------------
# EXPERIMENT 1
# --------------------------------------------
# set up environment variables
experiment = 'exp1'
utils.create_exp_folder(experiment)
no_id_plot_numbers = list(range(1, 29))
subject_IDs = utils.exp1_subject_folders()

# read and process data
all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)

# create randomised plots for data checking
for plot, (subject_ID, current_subject_data) in enumerate(zip(subject_IDs, all_subject_data), start = 1):
    utils.create_subject_folder(subject_ID)
    plots.random_plot(plot, subject_ID, current_subject_data)

utils.merge_pdfs(Path('./randomised_plots_no_ID'))

# create result plots for each subject
for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    plots.plot_and_store(subject_ID, current_subject_data)

# create group plot of regression lines coloured by 'type' of participant
plots.plot_subject_reg_lines_by_category(subject_IDs, all_subject_data)









