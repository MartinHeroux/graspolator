import os
from pathlib import Path
import statsmodels.api as sm
import yaml
from PyPDF2 import PdfFileMerger
import scipy.stats as scp
import numpy as np
from scipy.stats import sem, t
from collections import namedtuple
from termcolor import colored

import plot_utils


def calculate_regression(block):
    x = block.ACTUAL
    y = block.PERCEIVED
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope


def calculate_regression_general(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope

def regression_summary(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    print(model.summary())


def read_yaml_corrections_file(fix_yaml):
    if not fix_yaml.is_file():
        return
    with open(fix_yaml) as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def merge_pdfs(source_directory):
    filenames = get_filename_list(source_directory)
    merger = PdfFileMerger()
    for filename in filenames:
        pdf_path = str(Path('./randomised_plots_no_ID/', filename))
        merger.append(pdf_path)
    merger.write("concatenated.pdf")
    merger.close()


def calculate_r2(actual, perceived):
    r_score, p_value = scp.pearsonr(actual, perceived)
    r_squared = r_score ** 2
    return r_squared


def calculate_mean_ci(data_list):
    mean = np.mean(data_list)
    confidence = 0.95
    n = len(data_list)
    std_err = sem(data_list)
    ci = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return mean, ci


def calculate_ci(data_list):
    confidence = 0.95
    n = len(data_list)
    std_err = sem(data_list)
    ci = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return ci


def store_r2_means_CIs_per_condition(all_subject_data, experiment):
    r2_lists = store_r2_tuples(all_subject_data, experiment)
    mean_list = []
    ci_list = []
    for r2_list in r2_lists:
        mean_list.append(np.mean(r2_list))
        ci_list.append(calculate_ci(r2_list))
    return mean_list, ci_list


def store_r2_tuples(all_subject_data, experiment):
    if experiment == 'exp1':
        r2_lists = _store_r2_tuples_exp1(all_subject_data)
    else:
        r2_lists = _store_r2_tuples_exp2(all_subject_data)
    return r2_lists


def _store_r2_tuples_exp1(all_subject_data):
    d1_dom_r2s, d1_non_dom_r2s, d2_dom_1_r2s, d2_dom_2_r2s = [], [], [], []
    r2_list_tuple = namedtuple('r2', 'd1_dom_r2_list d1_non_dom_r2_list d2_dom_1_r2_list d2_dom_2_r2_list')

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)

        d1_dom_r2s.append(calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)),
        d1_non_dom_r2s.append(calculate_r2(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)),
        d2_dom_1_r2s.append(calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)),
        d2_dom_2_r2s.append(calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED))

    r2_tuples = r2_list_tuple(d1_dom_r2_list=d1_dom_r2s,
                             d1_non_dom_r2_list=d1_non_dom_r2s,
                             d2_dom_1_r2_list=d2_dom_1_r2s,
                             d2_dom_2_r2_list=d2_dom_2_r2s)
    return r2_tuples


def _store_r2_tuples_exp2(all_subject_data):
    line_width_r2s, width_line_r2s, width_width_r2s = [], [], []
    r2_list_tuple = namedtuple('r2s',
                               'line_width_r2_list width_line_r2_list, width_width_r2_list')

    for subject_data in all_subject_data:
        data_tuples = condition_plot_inputs(subject_data)

        line_width, width_line, width_width = data_tuples[0], data_tuples[1], data_tuples[2]

        line_width_r2s.append(calculate_r2(line_width.ACTUAL, line_width.PERCEIVED)),
        width_line_r2s.append(calculate_r2(width_line.ACTUAL, width_line.PERCEIVED)),
        width_width_r2s.append(calculate_r2(width_width.ACTUAL, width_width.PERCEIVED))

    r2_tuples = r2_list_tuple(line_width_r2_list=line_width_r2s,
                             width_line_r2_list=width_line_r2s,
                             width_width_r2_list=width_width_r2s)
    return r2_tuples

def create_general_constants():
    general_constants = namedtuple('constants', 'CONDITION_NAMES_EXP1 CONDITION_NAMES_EXP2 CONDITION_PAIRS SUBJECT_IDS')
    return general_constants(CONDITION_NAMES_EXP1=['day1_dominant',
                                                   'day1_non_dominant',
                                                   'day2_dominant_1',
                                                   'day2_dominant_2'],
                             CONDITION_NAMES_EXP2=['line_width', 'width_line', 'width_width'],
                             CONDITION_PAIRS=['between_hands',
                                              'between_days',
                                              'within_day'],
                             SUBJECT_IDS=["SUB01L",
                                          "SUB01R",
                                          "SUB02L",
                                          "SUB02R",
                                          "SUB03L",
                                          "SUB03R",
                                          "SUB04R",
                                          "SUB05R",
                                          "SUB06R",
                                          "SUB07R",
                                          "SUB08R",
                                          "SUB09R",
                                          "SUB10R",
                                          "SUB11R",
                                          "SUB12R",
                                          "SUB13R",
                                          "SUB14R",
                                          "SUB16R",
                                          "SUB17R",
                                          "SUB18R",
                                          "SUB19R",
                                          "SUB20R",
                                          "SUB21R",
                                          "SUB22R",
                                          "SUB23R",
                                          "SUB24R",
                                          "SUB25R",
                                          "SUB26R",
                                          "SUB27R",
                                          "SUB28R"])


def max_min(list_of_lists):
    maximums_list = []
    minimums_list = []
    for data_list in list_of_lists:
        maximums_list.append(max(data_list))
        minimums_list.append(min(data_list))
    maximum, minimum = max(maximums_list), min(minimums_list)
    return maximum, minimum


def calculate_and_save_r_squared_to_txt(all_subject_data):
    constants = create_general_constants()
    for subject_ID, current_subject_data in zip(constants.SUBJECT_IDS, all_subject_data):
        _r_squared(subject_ID, current_subject_data)


def _r_squared(subject_ID, current_subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    r_square_file = open("r_squared_values.txt", "a")
    r_square_file.write(f'subject: {subject_ID} \n')
    for condition_name, condition_data in zip(condition_names, current_subject_data):
        r_square_file = open("r_squared_values.txt", "a")
        actual_widths = condition_data.actual_widths
        perceived_widths = condition_data.perceived_widths
        r_score, p_value = scp.pearsonr(actual_widths, perceived_widths)
        r_squared = r_score ** 2
        line_to_write = [f" {condition_name} r_squared: {r_squared:4.2f} \n"]
        r_square_file.writelines(line_to_write)
    r_square_file.close


def get_filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames


def get_directory_list(directory):
    directories = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directories.append(directory)
    return directories


def create_data_tuples(experiment, subject_data):
    if experiment == 'exp1':
        plot_inputs = plot_utils.store_index_condition_data_tuple(subject_data)
    else:
        plot_inputs = condition_plot_inputs(subject_data)
    return plot_inputs


def create_individual_plot_save_path(experiment, plot, subject_ID):
    path = Path(f'./plots/{experiment}/individual_plots/{plot}')
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f'./plots/{experiment}/individual_plots/{plot}/{plot}_{subject_ID}.png')
    return savepath


def create_group_plot_save_path(experiment, plot):
    path = Path(f'./plots/{experiment}/group_plots/')
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f'./plots/{experiment}/group_plots/{plot}.png')
    return savepath

def generic_plot_save_path(experiment, type, plot):
    path = f'./plots/{experiment}/{type}/{plot}'
    path_text = colored(path, 'blue')
    return path_text

def plot_constants_regressions_ind(experiment):
    if experiment == 'exp1':
        subplot_width = 1
        subplot_length = 4
        x_range = [2, 10]
        fig_size = [7, 20]
    else:
        subplot_width = 1
        subplot_length = 3
        x_range = [3, 9]
        fig_size = [15, 5]
    return subplot_width, subplot_length, x_range, fig_size


def subplot_dimensions_area_differences(experiment):
    if experiment == 'exp1':
        subplot_width = 1
        subplot_length = 3
        x_range = [2, 10]
        fig_size = (15, 7)
    else:
        subplot_width = 1
        subplot_length = 1
        x_range = [3, 9]
        fig_size = [15, 5]
    return subplot_width, subplot_length, x_range, fig_size


def x_points_group_plot(experiment):
    if experiment == 'exp1':
        x_points = [1, 2, 3, 4]
    else:
        x_points = [1, 2, 3]
    return x_points


def x_ticks_group_plot(experiment):
    if experiment == 'exp1':
        x_ticks = ['day1_dominant', 'day1_non_dominant', 'day2_dominant_1', 'day2_dominant_2']
    else:
        x_ticks = ['line_width', 'width_line', 'width_width']
    return x_ticks


def remove_missing_data(actual_list, perceived_list, subject_ID, name):
    indices_to_remove = []
    for trial in perceived_list:
        if trial == "":
            indices_to_remove.append(perceived_list.index(trial))
    indices_to_remove.reverse()
    for index in indices_to_remove:
        actual_list.pop(index)
        perceived_list.pop(index)
        # TODO figure out why below statement prints even when Exp1 is running
        print(f'removed missing data at index {index}, {subject_ID}, condition {name}')
    return actual_list, perceived_list


def condition_plot_inputs(subject_data):
    plot_inputs = namedtuple('INPUTS', 'NAME ACTUAL PERCEIVED PLOT_INDEX')
    line_width_inputs = plot_inputs(NAME='Show Line Pick Width', ACTUAL=subject_data.LINE_WIDTH.ACTUAL,
                                    PERCEIVED=subject_data.LINE_WIDTH.PERCEIVED, PLOT_INDEX=1)
    width_line_inputs = plot_inputs(NAME='Present Width Pick Line', ACTUAL=subject_data.WIDTH_LINE.ACTUAL,
                                    PERCEIVED=subject_data.WIDTH_LINE.PERCEIVED, PLOT_INDEX=2)
    width_width_inputs = plot_inputs(NAME='Present Width Pick Width', ACTUAL=subject_data.WIDTH_WIDTH.ACTUAL,
                                    PERCEIVED=subject_data.WIDTH_WIDTH.PERCEIVED, PLOT_INDEX=3)
    tuples = line_width_inputs, width_line_inputs, width_width_inputs
    return tuples