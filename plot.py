from pathlib import Path

import data_lovisa
import process
import utils
import plot_individual
import plot_group
import utils_lovisa
from collections import namedtuple

CONSTANTS = utils.create_general_constants()



def blinded_scatterplots(all_subject_data):
    for plot, (subject_ID, current_subject_data) in enumerate(zip(CONSTANTS.SUBJECT_IDS, all_subject_data), start=1):
        utils.create_subject_folder(subject_ID)
        plot_group.random_plot(plot, subject_ID, current_subject_data)
    utils.merge_pdfs(Path('./randomised_plots_no_ID'))

# done
def individual_regressions(all_subject_data, experiment, subjects):
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        plot_individual.scatterplots_and_reg_lines(subject_ID, subject_data, experiment)

# done
def regression_lines_per_condition(all_subject_data, experiment, subjects):
    plot_group.subject_reg_lines_by_category(experiment, subjects, all_subject_data)

# done
def individual_areas_to_reality(all_subject_data, experiment, subjects):
    for subject_ID, current_subject_data in zip(subjects, all_subject_data):
        plot_individual.areas_between_regression_and_reality(subject_ID, current_subject_data, experiment)

# done
def individual_areas_between_conditions(all_subject_data, experiment, subjects):
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        plot_individual.area_between_conditions_plot(subject_ID, subject_data, experiment)


def group_areas_between_conditions(all_subject_data):
    plot_group.consistency_between_conditions(all_subject_data)


def group_areas_difference_of_differences(all_subject_data):
    plot_group.difference_of_differences(all_subject_data)

# done
def group_areas_per_conditions(all_subject_data, experiment):
    plot_group.area_per_condition_plot(all_subject_data, experiment)

# done
def group_areas_vs_r2_per_condition(all_subject_data):
    plot_group.area_vs_r2_plot(all_subject_data)

# done
def group_r2_per_condition(all_subject_data, subjects):
    plot_group.r2_per_condition_plot(all_subject_data, subjects)





