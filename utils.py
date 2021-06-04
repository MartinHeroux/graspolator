import os
from pathlib import Path
import statsmodels.api as sm
import yaml
from PyPDF2 import PdfFileMerger
import scipy.stats as scp
import numpy as np
from scipy.stats import sem, t
from collections import namedtuple

import plot_utils
import utils_lovisa


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


def store_r2_means_CIs_per_condition(all_subject_data):
    r2_lists = store_r2_lists(all_subject_data)
    d1_dom_mean, d1_dom_ci = calculate_mean_ci(r2_lists.d1_dom_r2_list)
    d1_non_dom_mean, d1_non_dom_ci = calculate_mean_ci(r2_lists.d1_non_dom_r2_list)
    d2_dom_1_mean, d2_dom_1_ci = calculate_mean_ci(r2_lists.d2_dom_1_r2_list)
    d2_dom_2_mean, d2_dom_2_ci = calculate_mean_ci(r2_lists.d2_dom_2_r2_list)
    mean_lists = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
    ci_lists = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]
    return mean_lists, ci_lists


def store_r2_lists(all_subject_data):
    d1_dom_r2s, d1_non_dom_r2s, d2_dom_1_r2s, d2_dom_2_r2s = [], [], [], []
    r2_area_list_tuple = namedtuple('r2s_area',
                                    'd1_dom_r2_list d1_non_dom_r2_list d2_dom_1_r2_list d2_dom_2_r2_list')

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)

        d1_dom_r2s.append(calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)),
        d1_non_dom_r2s.append(calculate_r2(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)),
        d2_dom_1_r2s.append(calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)),
        d2_dom_2_r2s.append(calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED))

    r2_lists = r2_area_list_tuple(d1_dom_r2_list=d1_dom_r2s,
                                  d1_non_dom_r2_list=d1_non_dom_r2s,
                                  d2_dom_1_r2_list=d2_dom_1_r2s,
                                  d2_dom_2_r2_list=d2_dom_2_r2s)
    return r2_lists


def create_general_constants():
    general_constants = namedtuple('constants', 'CONDITION_NAMES CONDITION_PAIRS SUBJECT_IDS')
    return general_constants(CONDITION_NAMES=['day1_dominant',
                                              'day1_non_dominant',
                                              'day2_dominant_1',
                                              'day2_dominant_2'],
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


def create_directory(directory):
    if not os.path.exists(f'./{directory}'):
        os.makedirs(f'./{directory}')
        print(f'created directory {directory}')


def create_sub_directory(directory, sub_diretory):
    if not os.path.exists(f'./{directory}/{sub_diretory}'):
        os.makedirs(f'./{directory}/{sub_diretory}')
        print(f'created directory {directory}/{sub_diretory}')


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


def create_plot_subdirectories():
    plot_subdirectories = ['group_plots',
                           'individual_plots',
                           'individual_plots/subject_regression_plots',
                           'individual_plots/area_plots',
                           'individual_plots/area_plots/regression_vs_reality',
                           'individual_plots/area_plots/between_condition_comparison']
    plot_path = Path('./plots')
    for subdirectory in plot_subdirectories:
        path = plot_path / subdirectory
        if not os.path.exists(path):
            os.makedirs(path)

def create_data_tuples(experiment, subject_data):
    if experiment == 'exp1':
        plot_inputs = plot_utils.store_index_condition_data_tuple(subject_data)
    else:
        plot_inputs = utils_lovisa.condition_plot_inputs(subject_data)
    return plot_inputs

def create_individual_plot_save_path(experiment, plot, subject_ID):
    path = Path(f'./plots/{experiment}/individual_plots/{plot}')
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f'./plots/{experiment}/individual_plots/{plot}/{plot}_{subject_ID}.png')
    return savepath

def subplot_dimensions_regressions(experiment):
    if experiment == 'exp1':
        subplot_width = 2
        subplot_length = 2
        x_range = [2, 10]
        fig_size = [10,10]
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
