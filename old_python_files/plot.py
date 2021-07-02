from pathlib import Path

import old_python_files.old_functions
import utils
from old_python_files import plot_group, plot_individual

CONSTANTS = utils.create_general_constants()


def blinded_scatterplots(all_subject_data):
    for plot, (subject_ID, current_subject_data) in enumerate(zip(CONSTANTS.SUBJECT_IDS, all_subject_data), start=1):
        utils.create_subject_folder(subject_ID)
        plot_group.random_plot(plot, subject_ID, current_subject_data)
    old_python_files.old_functions.merge_pdfs(Path('./randomised_plots_no_ID'))


# done
def individual_regressions(all_subject_data, experiment, subjects):
    print('Note - this takes a while')
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        plot_individual.scatterplots_and_reg_lines(subject_ID, subject_data, experiment)
    path = old_python_files.old_functions.generic_plot_save_path(experiment, 'individual_plots', 'scatterplot_regression')
    print(f'All individual regression plots saved in {path}\n')


def group_regression_lines_per_condition(all_subject_data, experiment, subjects):
    plot_group.subject_reg_lines_by_category(experiment, subjects, all_subject_data)


# done
def individual_areas_to_reality(all_subject_data, experiment, subjects):
    print('Note - this takes a while')
    for subject_ID, current_subject_data in zip(subjects, all_subject_data):
        plot_individual.areas_between_regression_and_reality(subject_ID, current_subject_data, experiment)
    path = old_python_files.old_functions.generic_plot_save_path(experiment, 'individual_plots', 'area_between_reg_and_reality')
    print(f'All individual areas between regression line and reality saved in {path}\n')


# done
def individual_areas_between_conditions(all_subject_data, experiment, subjects):
    print('Note - this takes a while')
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        plot_individual.area_between_conditions_plot(subject_ID, subject_data, experiment)
    path = old_python_files.old_functions.generic_plot_save_path(experiment, 'individual_plots', 'area_between_conditions')
    print(f'All individual areas between conditions saved in {path}\n')


def group_areas_between_conditions(all_subject_data, experiment, subjects):
    plot_group.consistency_between_conditions(all_subject_data, experiment)


def group_areas_difference_of_differences(all_subject_data, experiment, subjects):
    plot_group.kathy_difference_of_differences(all_subject_data, experiment)


# done
def group_areas_per_conditions(all_subject_data, experiment, subjects):
    plot_group.area_per_condition_plot(all_subject_data, experiment)


# done
def group_areas_vs_r2_per_condition(all_subject_data, experiment, subjects):
    plot_group.area_vs_r2_plot(all_subject_data, experiment)


# done
def group_r2_per_condition(all_subject_data, experiment, subjects):
    plot_group.r2_per_condition_plot(all_subject_data, experiment)


# done
def lovia_reciprocal_condition_regression(all_subject_data, experiment, subjects):
    plot_group.lovisa_between_condition_regression(all_subject_data, experiment)


def slope_comparison(all_subject_data, experiment, subjects):
    plot_group.slope_comparison(all_subject_data, experiment)