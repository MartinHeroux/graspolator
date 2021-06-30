import os
from pathlib import Path
import statsmodels.api as sm
import yaml
import scipy.stats as scp
import numpy as np
from matplotlib import patches as mpatches
from scipy.stats import sem, t
from collections import namedtuple
from termcolor import colored
import math


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


def calculate_r2(actual, perceived):
    r_score, p_value = scp.pearsonr(actual, perceived)
    r_squared = r_score ** 2
    return r_squared

def pearson_r_ci(x, y):
    # TODO check
    if len(x) != len(y):
        print('Lists of uneven length in pearson calc')

    r_value, p_value = scp.pearsonr(x, y)

    alpha = 0.05 / 2  # Two-tail test

    z_critical = scp.norm.ppf(1 - alpha) # z score for 95% CI
    z_sample = 0.5 * np.log((1 + r_value) / (1 - r_value)) # z score of r value

    n = len(x)
    std_err = 1 / np.sqrt(n - 3)

    z_ci_lower = z_sample - z_critical * std_err
    z_ci_upper = z_sample + z_critical * std_err

    r_ci_lower = (math.exp(2*z_ci_lower) - 1) / (math.exp(2*z_ci_lower) + 1)
    r_ci_upper = (math.exp(2 * z_ci_upper) + 1) / (math.exp(2 * z_ci_upper) - 1)

    ci = str(f'[{r_ci_lower} - {r_ci_upper}')

    return r_value, ci


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
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = store_index_condition_data_tuple(
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
    return general_constants(CONDITION_NAMES_EXP1=['D1 dominant',
                                                   'D1 non-dominant',
                                                   'D2 dominant 1',
                                                   'D2 dominant 2'],
                             CONDITION_NAMES_EXP2=['Line to width', 'Width to line', 'Width to width'],
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
    r_square_file = open("old_python_files/r_squared_values.txt", "a")
    r_square_file.write(f'subject: {subject_ID} \n')
    for condition_name, condition_data in zip(condition_names, current_subject_data):
        r_square_file = open("old_python_files/r_squared_values.txt", "a")
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
        plot_inputs = store_index_condition_data_tuple(subject_data)
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

def create_article_plot_save_path(plot):
    path = Path(f'./plots/article_plots/')
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f'./plots/article_plots/{plot}.png')
    return savepath

def generic_plot_save_path(experiment, type, plot):
    path = f'./plots/{experiment}/{type}/{plot}'
    path_text = colored(path, 'blue')
    return path_text

def plot_constants_regressions_ind(experiment):
    if experiment == 'exp1':
        subplot_width = 4
        subplot_length = 1
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
        x_ticks = ['Dominant', 'Non-dominant', 'Dominant', 'Dominant']
    else:
        x_ticks = ['Line-to-width', 'Width-to-line', 'Width-to-width']
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
        #print(f'removed missing data at index {index}, {subject_ID}, condition {name}')
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


def create_plot_constants():
    plot_constants = namedtuple('plot_constants', 'PLOT_SUBDIRECTORIES ACTUAL_WIDTH_RANGE PERCEIVED_WIDTH_RANGE ALPHA '
                                                  'SMALLEST_WIDTH LARGEST_WIDTH Y_MIN Y_MAX REALITY_LINE_MIN '
                                                  'REALITY_LINE_MAX '
                                                  'MINIMISER_PATCH MAXIMISER_PATCH CROSSER_PATCH WIDE_SIZE SQUARE_SIZE')
    return plot_constants(PLOT_SUBDIRECTORIES=['group_plots',
                                               'regression_plots',
                                               'consistency_plots',
                                               'area_plots'],
                          ACTUAL_WIDTH_RANGE=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                          PERCEIVED_WIDTH_RANGE=[0.5] + list(range(1, 15)),
                          ALPHA=0.5,
                          SMALLEST_WIDTH=2, LARGEST_WIDTH=10, Y_MIN=0, Y_MAX=14, REALITY_LINE_MIN=0,
                          REALITY_LINE_MAX=14,
                          MINIMISER_PATCH=mpatches.Patch(color='firebrick', label='Minimiser'),
                          MAXIMISER_PATCH=mpatches.Patch(color='green', label='Maximiser'),
                          CROSSER_PATCH=mpatches.Patch(color='royalblue', label='Crosser'),
                          WIDE_SIZE=[15, 5], SQUARE_SIZE=[10, 10])


def store_index_condition_data_tuple(subject_data):
    index_name_data = namedtuple('index_name_data', 'PLOT_INDEX DATA_INDEX NAME ACTUAL PERCEIVED')
    d1_dom_tuple = index_name_data(PLOT_INDEX=1, DATA_INDEX=0, NAME='d1_dominant',
                                   ACTUAL=subject_data.day1_dominant.ACTUAL,
                                   PERCEIVED=subject_data.day1_dominant.PERCEIVED)
    d1_non_dom_tuple = index_name_data(PLOT_INDEX=2, DATA_INDEX=1, NAME='d2_non_dominant',
                                       ACTUAL=subject_data.day1_non_dominant.ACTUAL,
                                       PERCEIVED=subject_data.day1_non_dominant.PERCEIVED)
    d2_dom_1_tuple = index_name_data(PLOT_INDEX=3, DATA_INDEX=2, NAME='d2_dominant_1',
                                     ACTUAL=subject_data.day2_dominant_1.ACTUAL,
                                     PERCEIVED=subject_data.day2_dominant_1.PERCEIVED)
    d2_dom_2_tuple = index_name_data(PLOT_INDEX=4, DATA_INDEX=3, NAME='d2_dominant_2',
                                     ACTUAL=subject_data.day2_dominant_2.ACTUAL,
                                     PERCEIVED=subject_data.day2_dominant_2.PERCEIVED)
    tuples = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple
    return tuples


def condition_pair_tuple(experiment, subject_data):
    if experiment == 'exp1':
        tuple_list = _condition_pair_tuple_exp1(subject_data)
    elif experiment == 'exp2':
        tuple_list = _condition_pair_tuple_exp2(subject_data)
    else:
        print('experiment not defined tuple list')

    return tuple_list


def _condition_pair_tuple_exp1(subject_data):
    d1_dom = mpatches.Patch(color='blue', label='Day 1 Dominant')
    d1_non_dom = mpatches.Patch(color='orange', label='Day 1 Non Dominant')
    d2_dom_a = mpatches.Patch(color='red', label='Day 2 Dominant A')
    d2_dom_b = mpatches.Patch(color='green', label='Day 2 Dominant B')

    Pair = namedtuple('Pair', 'data_1 data_2 label_1 label_2 title colour_1 colour_2 patch_1 patch_2 subplot_index')
    dom_vs_non_dom = Pair(data_1=subject_data.day1_dominant, data_2=subject_data.day1_non_dominant, label_1='d1_dom',
                          label_2='d1_non_dom',
                          title='D1 dominant - D1 non-dominant', colour_1='blue', colour_2='orange', patch_1=d1_dom,
                          patch_2=d1_non_dom, subplot_index=1)
    dom_d1_vs_d2 = Pair(data_1=subject_data.day1_dominant, data_2=subject_data.day2_dominant_1, label_1='d1_dom',
                        label_2='d2_dom_a',
                        title='D1 dominant - D2 dominant', colour_1='blue', colour_2='red',
                        patch_1=d1_dom, patch_2=d2_dom_a, subplot_index=2)
    dom_d2_vs_d2 = Pair(data_1=subject_data.day2_dominant_1, data_2=subject_data.day2_dominant_2, label_1='d2_dom_a',
                        label_2='d2_dom_b',
                        title='D2 dominant a - D2 dominant b', colour_1='red', colour_2='green', patch_1=d2_dom_a, patch_2=d2_dom_b,
                        subplot_index=3)
    tuple_list = dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2
    return tuple_list


def _condition_pair_tuple_exp2(subject_data):
    line_width = mpatches.Patch(color='blue', label='Show Line Pick Width')
    width_line = mpatches.Patch(color='orange', label='Present Width Pick Line')

    Pair = namedtuple('Pair', 'data_1 data_2 label_1 label_2 title colour_1 colour_2 patch_1 patch_2 subplot_index')

    linefirst_vs_widthfirst = Pair(data_1=subject_data.LINE_WIDTH, data_2=subject_data.WIDTH_LINE, label_1='line_width',
                                   label_2='width_line',
                                   title='Reciprocal Condition Area Difference', colour_1='blue', colour_2='orange',
                                   patch_1=line_width,
                                   patch_2=width_line, subplot_index=1)
    return linefirst_vs_widthfirst


def subject_line_colour(intersection_x_value, y_when_x_equals_2, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9

    if x1 <= intersection_x_value <= x2:
        line_colour = 'royalblue'
    elif y_when_x_equals_2 < x1:
        line_colour = 'firebrick'
    else:
        line_colour = 'green'
    return line_colour


def color_manip(plot_index):
    if plot_index == 1:
        colour = 'firebrick'
    elif plot_index == 2:
        colour = 'firebrick'
    else:
        colour = 'firebrick'
    return colour


def store_example_subject_data_exp1(all_subject_data, subjects, subject_1_ID, subject_2_ID):
    experiment = 'exp1'
    for subject_data, subject_name in zip(all_subject_data, subjects):
        if subject_name == subject_1_ID:
            condition_data_list_1 = extract_condition_data(subject_data, experiment)
        if subject_name == subject_2_ID:
            condition_data_list_2 = extract_condition_data(subject_data, experiment)

    return [condition_data_list_1, condition_data_list_2]


def store_example_subject_data_exp2(all_subject_data, subjects, subject_1_ID, subject_2_ID):
    experiment = 'exp2'
    for subject_data, subject_name in zip(all_subject_data, subjects):
        if subject_name == subject_1_ID:
            condition_data_list_1 = extract_condition_data(subject_data, experiment)
        if subject_name == subject_2_ID:
            condition_data_list_2 = extract_condition_data(subject_data, experiment)

    return [condition_data_list_1, condition_data_list_2]


def extract_condition_data(subject_data, experiment):
    dummy_data = namedtuple('condition', 'ACTUAL PERCEIVED')
    if experiment == 'exp1':
        D1_DOM = subject_data.day1_dominant
        D1_NON_DOM = subject_data.day1_non_dominant
        D2_DOM_1 = subject_data.day2_dominant_1
        D2_DOM_2 = subject_data.day2_dominant_2

        condition_data_list = [D1_DOM, D1_NON_DOM, D2_DOM_1, D2_DOM_2]

    else:
        LINE_WIDTH = subject_data.LINE_WIDTH
        WIDTH_LINE = subject_data.WIDTH_LINE
        WIDTH_WIDTH = subject_data.WIDTH_WIDTH
        DUMMY_DATA = dummy_data(ACTUAL=[3, 6, 9], PERCEIVED=[3, 6, 9])

        condition_data_list = [LINE_WIDTH, WIDTH_LINE, WIDTH_WIDTH, DUMMY_DATA]

    return condition_data_list


def r2_area_constants():
    constants = namedtuple('constants', 'y_labels y_ticks y_lims subplot_indices r2_mean r2_ci_lower r2_ci_upper '
                                        'area_mean area_ci_lower area_ci_upper exp_1_colors exp_2_colors '
                                        'exp_1_subjects exp_2_subjects font')

    r2_area_constants = constants(y_labels=['R$^2$', 'Area (cm$^2$)'], y_ticks=[[0.6, 0.7, 0.8, 0.9, 1], [0, 5, 10, 15, 20, 25]],
                                  y_lims=[[0.6, 1.01], [0, 25]], subplot_indices=[2, 1], r2_mean=0.946, r2_ci_lower=0.9306, r2_ci_upper=0.9613,
                                  area_mean=1.320, area_ci_lower=0.9660, area_ci_upper=1.674, exp_1_colors=['royalblue', 'darkblue'],
                                  exp_2_colors=['darkred', 'red'], exp_1_subjects=['SUB05R', 'SUB01L'], exp_2_subjects=['sub04', 'sub23'],
                                  font='arial')

    return r2_area_constants