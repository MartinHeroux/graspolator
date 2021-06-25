from collections import namedtuple
import matplotlib.patches as mpatches


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

subject_1_ID = 'SUB01L'
subject_2_ID = 'SUB25R'

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