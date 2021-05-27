from pathlib import Path
import statsmodels.api as sm
import yaml
from PyPDF2 import PdfFileMerger
import scipy.stats as scp
import numpy as np
from scipy.stats import sem, t
from collections import namedtuple

import directories
import plot_funcs
import area_calcs

def calculate_regression(block):
    x = block.actual_widths
    y = block.perceived_widths
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope


def calculate_regression_general(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope


def calculate_regression_all_data(actual, perceived):
    actual = sm.add_constant(actual)
    model = sm.OLS(perceived, actual).fit()
    intercept, slope = model.params
    return intercept, slope


def read_yaml_corrections_file(fix_yaml):
    if not fix_yaml.is_file():
        return
    with open(fix_yaml) as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def merge_pdfs(source_directory):
    filenames = directories.get_filename_list(source_directory)
    merger = PdfFileMerger()
    for filename in filenames:
        pdf_path = str(Path('./randomised_plots_no_ID/', filename))
        merger.append(pdf_path)
    merger.write("concatenated.pdf")
    merger.close()


def r_squared(subject_ID, current_subject_data):
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


def confidence_interval(data):
    confidence = 0.95
    n = len(data)
    std_err = sem(data)
    ci = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return ci

def store_r2_lists_per_condition(all_subject_data):
    d1_dom_r2s, d1_non_dom_r2s, d2_dom_1_r2s, d2_dom_2_r2s = [], [], [], []
    r2_area_list_tuple = namedtuple('r2s_area',
                                    'd1_dom_r2_list d1_non_dom_r2_list d2_dom_1_r2_list d2_dom_2_r2_list')

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_funcs.store_index_condition_data_tuple(
            subject_data)

        d1_dom_r2s.append(calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)),
        d1_non_dom_r2s.append(calculate_r2(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)),
        d2_dom_1_r2s.append(calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)),
        d2_dom_2_r2s.append(calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED))

    r2_lists_per_condition = r2_area_list_tuple(d1_dom_r2_list=d1_dom_r2s,
                                                d1_non_dom_r2_list=d1_non_dom_r2s,
                                                d2_dom_1_r2_list=d2_dom_1_r2s,
                                                d2_dom_2_r2_list=d2_dom_2_r2s)
    return r2_lists_per_condition

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
    r2_lists = store_r2_lists_per_condition(all_subject_data)
    d1_dom_mean, d1_dom_ci = calculate_mean_ci(r2_lists.d1_dom_r2_list)
    d1_non_dom_mean, d1_non_dom_ci = calculate_mean_ci(r2_lists.d1_non_dom_r2_list)
    d2_dom_1_mean, d2_dom_1_ci = calculate_mean_ci(r2_lists.d2_dom_1_r2_list)
    d2_dom_2_mean, d2_dom_2_ci = calculate_mean_ci(r2_lists.d2_dom_2_r2_list)
    mean_lists = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
    ci_lists = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]
    return mean_lists, ci_lists

def store_area_means_CIs_per_condition(all_subject_data):
    area_lists = area_calcs.store_area_lists_per_condition(all_subject_data)
    d1_dom_mean, d1_dom_ci = calculate_mean_ci(area_lists.d1_dom_area_list)
    d1_non_dom_mean, d1_non_dom_ci = calculate_mean_ci(area_lists.d1_non_dom_area_list)
    d2_dom_1_mean, d2_dom_1_ci = calculate_mean_ci(area_lists.d2_dom_1_area_list)
    d2_dom_2_mean, d2_dom_2_ci = calculate_mean_ci(area_lists.d2_dom_2_area_list)
    mean_lists = [d1_dom_mean, d1_non_dom_mean, d2_dom_1_mean, d2_dom_2_mean]
    ci_lists = [d1_dom_ci, d1_non_dom_ci, d2_dom_1_ci, d2_dom_2_ci]
    return mean_lists, ci_lists


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

max_min([[1,2,3,4], [4,5,6,7]])
