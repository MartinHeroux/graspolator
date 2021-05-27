from pathlib import Path
import utils
import individual_plots
import group_plots

CONSTANTS = utils.create_general_constants()


def blinded_scatterplots(all_subject_data):
    for plot, (subject_ID, current_subject_data) in enumerate(zip(CONSTANTS.SUBJECT_IDS, all_subject_data), start=1):
        utils.create_subject_folder(subject_ID)
        group_plots.random_plot(plot, subject_ID, current_subject_data)
    utils.merge_pdfs(Path('./randomised_plots_no_ID'))


def individual_regressions(all_subject_data):
    for subject_ID, subject_data in zip(CONSTANTS.SUBJECT_IDS, all_subject_data):
        individual_plots.plot_subject_scatterplots_and_reg_lines(subject_ID, subject_data)


def regression_lines_per_condition(all_subject_data):
    ##TODO begin reformat
    group_plots.plot_subject_reg_lines_by_category(CONSTANTS.SUBJECT_IDS, all_subject_data)


def individual_areas_to_reality(all_subject_data):
    for subject_ID, current_subject_data in zip(CONSTANTS.SUBJECT_IDS, all_subject_data):
        individual_plots.plot_areas_between_reg_and_reality_lines(subject_ID, current_subject_data)


def individual_areas_between_conditions(all_subject_data):
    for subject_ID, subject_data in zip(CONSTANTS.SUBJECT_IDS, all_subject_data):
        individual_plots.area_between_conditions_plot(subject_ID, subject_data)


def group_areas_between_conditions(all_subject_data):
    # plot area differences for each condition pair, for each participant on same figure
    ##TODO begin reformat
    group_plots.group_consistency_plot(CONSTANTS.SUBJECT_IDS, all_subject_data)


def group_areas_difference_of_differences(all_subject_data):
    ##TODO begin reformat
    group_plots.plot_difference_of_differences(all_subject_data)


def group_areas_per_conditions(all_subject_data):
    # reformatted and runs
    group_plots.plot_area_across_conditions(all_subject_data)


def group_areas_vs_r2_per_condition(all_subject_data):
    ##TODO begin reformat
    group_plots.area_vs_r2_plot(all_subject_data)


def group_r2_per_condition(all_subject_data):
    group_plots.r2_group_plot(all_subject_data, CONSTANTS.SUBJECT_IDS)
