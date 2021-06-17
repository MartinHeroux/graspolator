from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
from random import random

import utils
import plot_utils
import calculate_area
import process

constants = utils.create_general_constants()
plot_constants = plot_utils.create_plot_constants()

## panel figure of individual subjects and group reg lines

def example_subjects_group_reg_summary(all_subject_data, subjects, experiment):
    plot = 'example_subjects_group_regression'
    path = utils.create_article_plot_save_path(plot)

    tuple_list = _store_example_subject_plot_info(all_subject_data, subjects, experiment)
    if experiment == 'exp1':
        condition_names = constants.CONDITION_NAMES_EXP1
        subplot_rows = 3
        subplot_cols = 4
        x_lims = [2, 10]
        subplot_bottom_rows = [10, 11, 12]
        group_plot_indices = [3, 6, 9, 12]
    else:
        condition_names = constants.CONDITION_NAMES_EXP2
        subplot_rows = 3
        subplot_cols = 3
        x_lims = [3, 9]
        subplot_bottom_rows = [7, 8, 9]
        group_plot_indices = [3, 6, 9, 12]

    plt.figure(figsize=(10, 10))
    for example_subject_tuple in tuple_list:
        for condition_data, condition_name, condition_plot_index in zip(example_subject_tuple.condition_data, example_subject_tuple.indices, condition_names):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     'k--')
            length_data = len(condition_data.PERCEIVED)
            jitter_values = [random() / 4 for _ in range(length_data)]
            x_data = np.array(condition_data.ACTUAL) + np.array(jitter_values)
            color = plot_utils.color_manip(condition_data.PLOT_INDEX)
            plt.plot(x_data, condition_data.PERCEIVED, 'o', color=example_subject_tuple.color, alpha=plot_constants.ALPHA)

            intercept, slope = utils.calculate_regression_general(condition_data.ACTUAL,
                                                                  condition_data.PERCEIVED)

            x1 = x_lims[0]
            x2 = x_lims[1]
            y1 = slope * x1 + intercept
            y2 = slope * x2 + intercept
            if y2 < 15:
                y_max = 15
            else:
                y_max = y2
            plt.plot([x1, x2], [y1, y2], color=color)

            area = calculate_area.actual_vs_perceived(condition_data.ACTUAL, condition_data.PERCEIVED, experiment)

            x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
            plt.plot([x1, x2], [y1, y2], color=example_subject_tuple.color)
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                             color=example_subject_tuple.color, alpha=0.3, interpolate=True)
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                             color=example_subject_tuple.color, alpha=0.3, interpolate=True)

            if condition_plot_index in [1, 4, 7, 10]:
                plt.yticks(list(range(0, int(y_max + 1))))
                plt.ylim([0, 14])
            else:
                plt.yaxis.set_visible(False)

            if condition_plot_index in subplot_bottom_rows:
                plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
                plt.xlim([x1 - 1, x2 + 1])
            else:
                plt.xaxis.set_visible(False)

    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, subplot_index in zip(data_list, group_plot_indices):
            plt.subplot(subplot_rows, subplot_cols, subplot_index)
            plt.grid(True)
            plt.title(condition_tuple.NAME, loc='right')
            intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
            intersect_x, intersect_y = calculate_area.point_of_intersection_with_reality(intercept, slope)
            x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                               experiment)

            line_colour = plot_utils.subject_line_colour(intersect_x, y1, experiment)
            plt.plot([x1, x2], [y1, y2], color=line_colour, linewidth=0.5)

    plt.savefig(path, dpi=300)
    print(f'Article figure 1 saved in for {experiment}')
    plt.close()


def _store_example_subject_plot_info(all_subject_data, subjects, experiment):
    example_data_tuple = namedtuple('EXAMPLE', 'condition_data indices')
    example_data_tuples = _return_example_subject_data(all_subject_data, subjects, experiment)

    example_1_condition_data = _return_data_pairs(experiment, example_data_tuples.example_1)
    example_2_condition_data = _return_data_pairs(experiment, example_data_tuples.example_1)

    example_1_indices = example_data_tuples.example_1.indices
    example_2_indices = example_data_tuples.example_2.indices

    example_1_tuple = example_data_tuple(condition_data = example_1_condition_data, indices = example_1_indices)
    example_2_tuple = example_data_tuple(condition_data=example_2_condition_data, indices=example_2_indices)

    tuple_list = [example_1_tuple, example_2_tuple]
    return tuple_list


def _return_example_subject_data(experiment):
    all_subject_data, subjects = process.return_data_and_subjects(experiment)
    all_subject_data_2, subjects_2 = process.return_data_and_subjects(experiment)

    example_subject_tuple = namedtuple('examples' 'name data indices color')
    example_subjects = namedtuple('examples', 'example_1, example_2')

    if experiment == 'exp1':
        for subject_data, subject in zip(all_subject_data, subjects):
            if subject == 'SUB05R':
                exp1_max_name = subject
                exp1_max_data = subject_data
            if subject == 'SUB01L':
                exp1_cross_name = subject
                exp1_cross_data = subject
        exp1_max = example_subject_tuple(name=exp1_max_name, data=exp1_max_data, indices=[1, 4, 7, 10], color = 'green')
        exp1_cross = example_subject_tuple(name=exp1_cross_name, data=exp1_cross_data, indices=[2, 5, 8, 11], color = 'blue')

        examples = example_subjects(example_1 = exp1_max, example_2 = exp1_cross)

    else:
        for subject_data, subject in zip(all_subject_data_2, subjects_2):
            if subject == 'sub04':
                exp2_min_name = subject
                exp2_min_data = subject_data
            if subject == 'sub23':
                exp2_cross_name = subject
                exp2_cross_data = subject

        exp2_min = example_subject_tuple(name=exp2_min_name, data=exp2_min_data, indices = [1, 4, 7], color = 'r')
        exp2_cross = example_subject_tuple(name=exp2_cross_name, data=exp2_cross_data, indices = [2, 5 ,8], color = 'orange')

        examples =  example_subjects(example_1 = exp2_min, example_2 = exp2_cross)

    return examples

def _return_data_pairs(experiment, tuple):
    if experiment == 'exp1':
        d1_dom = tuple.data.day1_dominant
        d1_non_dom = tuple.data.day1_non_dominant
        d2_dom_1 = tuple.data.day2_non_dominant_1
        d2_dom_2 = tuple.data.day2_non_dominant_2

        condition_data = d1_dom, d1_non_dom, d2_dom_1, d2_dom_2

    else:
        line_width = tuple.data.LINE_WIDTH
        width_line = tuple.data.WIDTH_LINE
        width_width = tuple.data.WIDTH_WIDTH

        condition_data = line_width, width_line, width_width

    return condition_data