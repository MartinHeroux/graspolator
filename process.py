from pathlib import Path
from collections import namedtuple

import utils
import data
import plot
import data_lovisa

DATA_FOLDER_EXP1 = Path('./data/exp1')
DATA_FOLDER_EXP2 = Path('./data/exp2')


def import_and_parse_data():
    # set up directory structure
    utils.create_plot_subdirectories()
    # read and process data
    all_subject_data, widest_lines = data.read_exp1(DATA_FOLDER_EXP1)
    return all_subject_data

def plot_by_dispatcher_key(all_subject_data, experiment, subjects):
    dispatcher = _create_plot_dispatcher()

    for key in dispatcher:
        if key.COMMAND == 'run':
            print(f'\n{key.PLOT} initiated')
            key.PLOT(all_subject_data, experiment, subjects)
        else:
            print(f'\n{key.PLOT} skipped')
    print('\n All done :)')

def _create_plot_dispatcher():
    plot_dispatch = namedtuple('plot_dispatch', 'PLOT COMMAND')
    plot_summary = namedtuple('plots', 'individual_regressions regression_lines_per_condition '
                                       'individual_areas_to_reality individual_areas_between_conditions '
                                       'group_areas_between_conditions group_areas_difference_of_differences '
                                       'group_areas_per_conditions group_areas_vs_r2_per_condition '
                                       'group_r2_per_condition')
    # change 'run' to 'skip' to alter which plots are made
    A = plot_dispatch._make([plot.individual_regressions, 'run'])
    B = plot_dispatch._make([plot.regression_lines_per_condition, 'run'])
    C = plot_dispatch._make([plot.individual_areas_to_reality, 'run'])
    D = plot_dispatch._make([plot.individual_areas_between_conditions, 'run'])
    E = plot_dispatch._make([plot.group_areas_between_conditions, 'run'])
    F = plot_dispatch._make([plot.group_areas_difference_of_differences, 'run'])
    G = plot_dispatch._make([plot.group_areas_per_conditions, 'run'])
    H = plot_dispatch._make([plot.group_areas_vs_r2_per_condition, 'run'])
    I = plot_dispatch._make([plot.group_r2_per_condition, 'run'])

    plot_summary = plot_summary._make([A, B, C, D, E, F, G, H, I])
    return plot_summary

def return_data_and_subjects(experiment):
    if experiment == 'exp1':
        all_subject_data = import_and_parse_data()
        subjects = utils.get_directory_list(Path('./data/exp1'))

    elif experiment == 'exp2':
        all_subject_data = data_lovisa.process_blocked_data()
        subjects = utils.get_directory_list(Path('./data/exp2'))

    else: print('no experiment name defined')

    return all_subject_data, subjects

all_subject_data, subjects = return_data_and_subjects('exp2')