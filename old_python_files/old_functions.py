import os
from collections import namedtuple
from pathlib import Path

import matplotlib as mpl
from matplotlib import patches as mpatches
from statsmodels import api as sm
from termcolor import colored

import utils
from calculate_area import normalised, trapezium_area, reg_line_endpoints

mpl.get_configdir()
import matplotlib.pyplot as plt

#plt.style.use('graspolator_style')

# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)
plt.plot([2,4], [2,4])
# Show empty plot
plt.show()

def between_condition_pair(data_pair):
    x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b = utils.compute_area_calc_inputs(
        data_pair)
    group = utils.subject_group_reg_lines(x_intersect)

    if group == 'cross':
        total_area = reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a,
                                           y_at_x2_b,
                                           y_at_x10_b)
    else:
        total_area = reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b)
    return total_area

def compute_area_calc_inputs(data_pair):
    intercept_a, slope_a = calculate_regression(data_pair.data_1)
    intercept_b, slope_b = calculate_regression(data_pair.data_2)

    x2_a, x10_a, y_at_x2_a, y_at_x10_a = reg_line_endpoints(intercept_a, slope_a)
    x2_b, x10_b, y_at_x2_b, y_at_x10_b = reg_line_endpoints(intercept_b, slope_b)
    x_intersect, y_intersect = point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)

    return x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b


def create_directory(directory):
    if not os.path.exists(f'./{directory}'):
        os.makedirs(f'./{directory}')
        print(f'created directory {directory}')


def create_sub_directory(directory, sub_diretory):
    if not os.path.exists(f'./{directory}/{sub_diretory}'):
        os.makedirs(f'./{directory}/{sub_diretory}')
        print(f'created directory {directory}/{sub_diretory}')



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


def merge_pdfs(source_directory):
    filenames = get_filename_list(source_directory)
    merger = PdfFileMerger()
    for filename in filenames:
        pdf_path = str(Path('./randomised_plots_no_ID/', filename))
        merger.append(pdf_path)
    merger.write("concatenated.pdf")
    merger.close()


def store_r2_and_area_tuples_exp1(all_subject_data, subject_IDs):
    experiment = 'exp1'
    r2s_areas = namedtuple('r2s_area',
                           'subject_ID d1_dom_r2 d1_non_dom_r2 d2_dom_1_r2 d2_dom_2_r2 d1_dom_area d1_non_dom_area '
                           'd2_dom_1_area d2_dom_2_area')
    r2_area_tuples = []

    for subject_data, subject_ID in zip(all_subject_data, subject_IDs):
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = utils.store_condition_data_tuples_exp1(
            subject_data)

        r2s_areas_tuple = r2s_areas(subject_ID=subject_ID,
                                    d1_dom_r2=utils.calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED),
                                    d1_non_dom_r2=utils.calculate_r2(d1_non_dom_tuple.ACTUAL,
                                                                     d1_non_dom_tuple.PERCEIVED),
                                    d2_dom_1_r2=utils.calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED),
                                    d2_dom_2_r2=utils.calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED),
                                    d1_dom_area=normalised(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED,
                                                           experiment),
                                    d1_non_dom_area=normalised(d1_non_dom_tuple.ACTUAL,
                                                               d1_non_dom_tuple.PERCEIVED, experiment),
                                    d2_dom_1_area=normalised(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED,
                                                             experiment),
                                    d2_dom_2_area=normalised(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED,
                                                             experiment))

        r2_area_tuples.append(r2s_areas_tuple)

    return r2_area_tuples


def store_r2_and_area_tuples_exp2(all_subject_data, subject_IDs):
    experiment = 'exp2'
    r2s_areas = namedtuple('r2s_area',
                           'subject_ID line_width_r2 width_line_r2 width_width_r2 line_width_area width_line_area '
                           'width_width_area')
    r2_area_tuples = []

    for subject_data, subject_ID in zip(all_subject_data, subject_IDs):
        data_tuples = utils.condition_plot_inputs(subject_data)

        line_width, width_line, width_width = data_tuples[0], data_tuples[1], data_tuples[2]

        r2s_areas_tuple = r2s_areas(subject_ID=subject_ID,
                                    line_width_r2=utils.calculate_r2(line_width.ACTUAL, line_width.PERCEIVED),
                                    width_line_r2=utils.calculate_r2(width_line.ACTUAL, width_line.PERCEIVED),
                                    width_width_r2=utils.calculate_r2(width_width.ACTUAL, width_width.PERCEIVED),
                                    line_width_area=normalised(line_width.ACTUAL, line_width.PERCEIVED,
                                                               experiment),
                                    width_line_area=normalised(width_line.ACTUAL, width_line.PERCEIVED,
                                                               experiment),
                                    width_width_area=normalised(width_width.ACTUAL, width_width.PERCEIVED,
                                                                experiment))

        r2_area_tuples.append(r2s_areas_tuple)

    return r2_area_tuples


def between_conditions(experiment, subject_data):
    tuple_list = condition_pair_tuple(experiment, subject_data)

    if experiment == 'exp1':

        dom_vs_non_dom_area = _condition_pair_area_exp1(tuple_list[0], experiment)
        dom_d1_vs_d2_area = _condition_pair_area_exp1(tuple_list[1], experiment)
        dom_d2_vs_d2_area = _condition_pair_area_exp1(tuple_list[2], experiment)

        areas = dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area

    elif experiment == 'exp2':

        areas = _condition_pair_area_exp2(tuple_list, experiment)

    return areas


def _condition_pair_area_exp1(condition_pair_tuple, experiment):
    intercept_a, slope_a = calculate_regression(condition_pair_tuple.data_1)
    intercept_b, slope_b = calculate_regression(condition_pair_tuple.data_2)

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = condition_pair_endpoints(condition_pair_tuple, experiment)
    intersect_x, intersect_y = _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)
    group = _subject_group_reg_lines_exp1(intersect_x)
    if group == 'cross':
        total_area = _reg_line_crosser_area(intersect_x, intersect_y, y1_y2_a[0], y1_y2_a[1], y1_y2_b[0], y1_y2_b[1],
                                            experiment)
    else:
        total_area = _reg_line_no_cross_area(y1_y2_a[0], y1_y2_a[1], y1_y2_b[0], y1_y2_b[1], experiment)
    return total_area


def _condition_pair_area_exp2(condition_pair_tuple, experiment):
    intercept_a, slope_a = calculate_regression(condition_pair_tuple.data_1)
    intercept_b, slope_b = calculate_regression(condition_pair_tuple.data_2)
    intercept_reality, slope_reality = 0, 1

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = condition_pair_endpoints(condition_pair_tuple, experiment)
    x1_x2_reality, y1_y2_reality = [3, 9], [3, 9]

    intersect_x_1, intersect_y_1 = _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_reality,
                                                                    slope_reality)
    intersect_x_2, intersect_y_2 = _point_of_intersection_reg_lines(intercept_b, slope_b, intercept_reality,
                                                                    slope_reality)

    area_line_first = _reg_reality_area(intersect_x_1, intersect_y_1, y1_y2_a, y1_y2_reality, experiment)
    area_width_first = _reg_reality_area(intersect_x_2, intersect_y_2, y1_y2_b, y1_y2_reality, experiment)

    areas = area_line_first, area_width_first

    return areas


def _reg_reality_area(intersection_x, intersection_y, y_coordinates_1, y_coordinates_2, experiment):
    group = _subject_group_reg_lines_exp2(intersection_x)
    if group == 'cross':
        total_area = _reg_line_crosser_area(intersection_x, intersection_y, y_coordinates_1[0], y_coordinates_1[1],
                                            y_coordinates_2[0], y_coordinates_2[1], experiment)
    else:
        total_area = _reg_line_no_cross_area(y_coordinates_1[0], y_coordinates_1[1], y_coordinates_2[0],
                                             y_coordinates_2[1], experiment)
    return total_area


def _point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b):
    m1, b1 = slope_a, intercept_a
    m2, b2 = slope_b, intercept_b
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope_a) + intercept_a
    return x_intersect, y_intersect


def _subject_group_reg_lines_exp1(x_intersect):
    if 2 <= x_intersect <= 10:
        group = 'cross'
    else:
        group = 'no_cross'
    return group


def _subject_group_reg_lines_exp2(x_intersect):
    if 3 <= x_intersect <= 9:
        group = 'cross'
    else:
        group = 'no_cross'
    return group


def _reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b, experiment):
    if experiment == 'exp1':
        x1 = 2
        x2 = 10
    elif experiment == 'exp2':
        x1 = 3
        x2 = 9
    else:
        print('experiment not defined reg line crosser area')

    h_left_trapezium = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    left_trap_area_a = trapezium_area(y_at_x2_a, y_intersect, h_left_trapezium)
    right_trap_area_a = trapezium_area(y_intersect, y_at_x10_a, h_right_trapezium)

    left_trap_area_b = trapezium_area(y_at_x2_b, y_intersect, h_left_trapezium)
    right_trap_area_b = trapezium_area(y_intersect, y_at_x10_b, h_right_trapezium)

    left_area = abs(left_trap_area_a - left_trap_area_b)
    right_area = abs(right_trap_area_a - right_trap_area_b)

    total_area = abs(left_area + right_area)
    return total_area


def _reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b, experiment):
    if experiment == 'exp1':
        h = 8
    elif experiment == 'exp2':
        h = 6
    else:
        print("experiment not defined reg line no cross area")

    area_a = trapezium_area(y_at_x2_a, y_at_x10_a, h)
    area_b = trapezium_area(y_at_x2_b, y_at_x10_b, h)

    total_area = abs(area_a - area_b)
    return total_area


def condition_pair_endpoints(condition_pair_tuple, experiment):
    x1_a, x2_a, y1_a, y2_a = reg_line_endpoints(condition_pair_tuple.data_1[0], condition_pair_tuple.data_1[1],
                                                experiment)
    x1_b, x2_b, y1_b, y2_b = reg_line_endpoints(condition_pair_tuple.data_2[0], condition_pair_tuple.data_2[1],
                                                experiment)
    x1_x2_a = [x1_a, x2_a]
    x1_x2_b = [x1_b, x2_b]
    y1_y2_a = [y1_a, y2_a]
    y1_y2_b = [y1_b, y2_b]
    return x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b


def calculate_regression(block):
    x = block.ACTUAL
    y = block.PERCEIVED
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope


def max_min(list_of_lists):
    maximums_list = []
    minimums_list = []
    for data_list in list_of_lists:
        maximums_list.append(max(data_list))
        minimums_list.append(min(data_list))
    maximum, minimum = max(maximums_list), min(minimums_list)
    return maximum, minimum


def get_filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames


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
                        title='D2 dominant a - D2 dominant b', colour_1='red', colour_2='green', patch_1=d2_dom_a,
                        patch_2=d2_dom_b,
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


def difference_of_difference_areas(experiment, subject_data):
    dom_vs_non_dom_area, dom_d1_vs_d2_area, d2_dom_vs_dom_area = between_conditions(experiment,
                                                                                    subject_data)
    hands_vs_day = dom_vs_non_dom_area - d2_dom_vs_dom_area
    hands_vs_days = dom_vs_non_dom_area - dom_d1_vs_d2_area
    day_vs_days = d2_dom_vs_dom_area - dom_d1_vs_d2_area
    return hands_vs_day, hands_vs_days, day_vs_days