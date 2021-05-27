import data
import directories
import plots
import utils
import individual_plots
import group_plots
import plot_funcs

from pathlib import Path
import matplotlib.pyplot as plt


DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')

# --------------------------------------------
# EXPERIMENT 1
# --------------------------------------------
# load in constant values
constants = utils.create_general_constants()
plot_constants = plot_funcs.create_plot_constants()

# set up directory structure
directories.create_plot_subdirectories()

# set default plot style
#plt.style.use('graspolator_style')

# read and process data
all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)

# create randomised plots for data checking + merge into single pdf
for plot, (subject_ID, current_subject_data) in enumerate(zip(constants.SUBJECT_IDS, all_subject_data), start = 1):
    utils.create_subject_folder(subject_ID)
    plots.random_plot(plot, subject_ID, current_subject_data)
utils.merge_pdfs(Path('./randomised_plots_no_ID'))

# create regression line and scatter plots for each subject
##TODO fix truth error
for subject_ID, current_subject_data in zip(constants.SUBJECT_IDS, all_subject_data):
    individual_plots.plot_subject_scatterplots_and_reg_lines(subject_ID, current_subject_data)

# create group plot of regression lines coloured by 'type' of participant per condition
##TODO begin reformat
group_plots.plot_subject_reg_lines_by_category(constants.SUBJECT_IDS, all_subject_data)

# calculate area between line of reality and regression line as 'error' score per condition, per participant
##TODO fix truth error
for subject_ID, current_subject_data in zip(constants.SUBJECT_IDS, all_subject_data):
    individual_plots.plot_areas_between_reg_and_reality_lines(subject_ID, current_subject_data)

# calculate area between regression lines for each participant
##TODO fix truth error
for subject_ID, current_subject_data in zip(constants.SUBJECT_IDS, all_subject_data):
    individual_plots.area_between_conditions_plot(subject_ID, current_subject_data)

# calculate and store r_square values for each participant in txt file
r_square_file = open("r_squared_values.txt", "w")
for subject_ID, current_subject_data in zip(constants.SUBJECT_IDS, all_subject_data):
    utils.r_squared(subject_ID, current_subject_data)

# plot area differences for each condition pair, for each participant on same figure
##TODO begin reformat
group_plots.group_consistency_plot(constants.SUBJECT_IDS, all_subject_data)

# plot difference of differences for conditions (e.g between hands vs within day)
##TODO begin reformat
group_plots.plot_difference_of_differences(all_subject_data)

# plot area between reg line and reality line for each participant for each condition
# reformatted and runs
group_plots.plot_area_across_conditions(all_subject_data)

# plot regression between area between lines and r^2 value
##TODO begin reformat
group_plots.area_vs_r2_plot(all_subject_data)

# plot summary of R^2 values for each condition
# reformatted and runs
group_plots.r2_group_plot(all_subject_data, constants.SUBJECT_IDS)
