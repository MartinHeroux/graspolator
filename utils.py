from pathlib import Path
import statsmodels.api as sm
import yaml
from PyPDF2 import PdfFileMerger
import scipy.stats as scp
import numpy as np
from scipy.stats import sem, t
from collections import namedtuple

import directories


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
