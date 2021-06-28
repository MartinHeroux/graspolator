from pathlib import Path
from collections import namedtuple
from termcolor import colored

import process_data_exp1

DATA_FOLDER_EXP1 = Path('../data/exp1')
DATA_FOLDER_EXP2 = Path('../data/exp2')


def import_and_parse_data():
    # set up directory structure
    #utils.create_plot_subdirectories()
    # read and process data
    all_subject_data, widest_lines = process_data_exp1.read_exp1(DATA_FOLDER_EXP1)
    return all_subject_data


def plot_by_dispatcher_key(plot_summary, all_subject_data, experiment, subjects):
    print('\nSTARTING PLOTS')
    for key in plot_summary:
        print(key)
        if key.COMMAND == 'run':
            text = colored(f'{key.PLOT} initiated\n', 'green')
            print(text)
            key.PLOT(all_subject_data, experiment, subjects)
        else:
            text = colored(f'{key.PLOT} skipped\n', 'red')
            print(text)
    print('\n All done :)')


def create_plot_dispatcher(experiment, A, B, C, D, E, F, G, H, I, J, K):
    plot_summary_exp1, plot_summary_exp2 = _return_plot_tuples()

    if experiment == 'exp1':
        plot_summary = plot_summary_exp1._make([A, B, C, D, E, F, G, H, I])
    elif experiment == 'exp2':
        plot_summary = plot_summary_exp2._make([A, B, C, D, E, F, G, J, K])

    return plot_summary


def _return_plot_tuples():
    plot_summary_exp1 = namedtuple('plots', 'A_individual_regressions '
                                            'B_individual_areas_to_reality '
                                            'C_individual_areas_between_conditions '
                                            'D_group_regression_lines_per_condition '
                                            'E_group_areas_per_conditions '
                                            'F_group_areas_vs_r2_per_condition '
                                            'G_group_r2_per_condition '
                                            'H_group_areas_between_conditions '
                                            'I_group_areas_difference_of_differences')

    plot_summary_exp2 = namedtuple('plots', 'A_individual_regressions '
                                            'B_individual_areas_to_reality '
                                            'C_individual_areas_between_conditions '
                                            'D_group_regression_lines_per_condition '
                                            'E_group_areas_per_conditions '
                                            'F_group_areas_vs_r2_per_condition '
                                            'G_group_r2_per_condition '
                                            'J_group_reciprocal_regression '
                                            'K_slope_comparison')

    return plot_summary_exp1, plot_summary_exp2


