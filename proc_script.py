import data
import plots
import utils
import consistency_plots


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

# create randomised plots for data checking + merge into single pdf
for plot, (subject_ID, current_subject_data) in enumerate(zip(subject_IDs, all_subject_data), start = 1):
    utils.create_subject_folder(subject_ID)
    plots.random_plot(plot, subject_ID, current_subject_data)
utils.merge_pdfs(Path('./randomised_plots_no_ID'))

# create result plots (reg lines and scatter plots) for each subject
for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    plots.plot_and_store(subject_ID, current_subject_data)

# create group plot of regression lines coloured by 'type' of participant per condition
plots.plot_subject_reg_lines_by_category(subject_IDs, all_subject_data)

# calculate area between line of reality and regression line as 'error' score per condition, per participant
for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    plots.plot_areas(subject_ID, current_subject_data)

# calculate area between regression lines for each participant
for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    consistency_plots.consistency_plot(subject_ID, current_subject_data)

# calculate and store r_square values for each participant in txt file
r_square_file = open("r_squared_values.txt", "w")
for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
    utils.r_squared(subject_ID, current_subject_data)

# plot area differences for each condition pair, for each participant on same figure
plots.group_consistency_plot(subject_IDs, all_subject_data)

# plot difference of differences for conditions (e.g between hands vs within day)
plots.plot_difference_of_differences(all_subject_data)

# plot area between reg line and reality line for each participant for each condition
plots.plot_area_across_conditions(all_subject_data)


