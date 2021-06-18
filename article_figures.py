from collections import namedtuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    plot = f'example_subjects_group_regression_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    tuple_list = _store_example_subject_plot_info(all_subject_data, subjects, experiment)

    # set up experiment specific parameters
    if experiment == 'exp1':
        condition_names = constants.CONDITION_NAMES_EXP1
        subplot_rows = 3
        subplot_cols = 4
        x_lims = [2, 10]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9, 12]
        colors = ['royalblue', 'seagreen']
        example_subjects = ['SUB05R', 'SUB01L']
    else:
        condition_names = constants.CONDITION_NAMES_EXP2
        subplot_rows = 3
        subplot_cols = 3
        x_lims = [3, 9]
        subplot_left_col = [1, 4, 7]
        subplot_bottom_row = [7, 8, 9]
        group_plot_indices = [3, 6, 9]
        colors = ['darkblue', 'darkorange']
        example_subjects = ['sub04', 'sub23']

    plt.figure(figsize=(10, 15))
    # plot example subjects in left and centre subplot cols
    for col, (example_subject_tuple, color) in enumerate(zip(tuple_list, colors), start = 1):
        for condition_data, condition_plot_index, condition_name in zip(example_subject_tuple.condition_data,
                                                                        example_subject_tuple.indices, condition_names):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            if condition_plot_index == 1:
                plt.title(example_subjects[0], loc='right', size=10, fontfamily='arial')
            if condition_plot_index == 2:
                plt.title(example_subjects[1], loc='right', size=10, fontfamily='arial')
            plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     'k--')

            length_data = len(condition_data.PERCEIVED)
            jitter_values = [random() / 4 for _ in range(length_data)]
            x_data = np.array(condition_data.ACTUAL) + np.array(jitter_values)
            plt.plot(x_data, condition_data.PERCEIVED, 'o', color=color,
                     alpha=plot_constants.ALPHA, markersize=3)

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
            plt.grid(axis='both')
            area = calculate_area.actual_vs_perceived(condition_data.ACTUAL, condition_data.PERCEIVED, experiment)

            legend_handles = [mpatches.Patch(color='darkgrey', alpha=0.3, label=f'Area = {area:4.2f}')]
            plt.legend(handles=legend_handles, loc='upper left')

            x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                             color='darkgrey', alpha=0.3, interpolate=True)
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                             color='darkgrey', alpha=0.3, interpolate=True)

            plt.yticks(list(range(0, int(y_max + 1))), fontfamily='arial')
            plt.ylim([0, 14])
            plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))), fontfamily='arial')
            plt.xlim([x1 - 1, x2 + 1])

            # remove ticks from subplots where unneeded
            if condition_plot_index not in subplot_left_col:
                ax = plt.gca()
                ax.set_yticklabels([])
                #ax.yaxis.set_ticks([])

            if condition_plot_index not in subplot_bottom_row:
                ax = plt.gca()
                ax.set_xticklabels([])
                #ax.xaxis.set_ticks([])

            if condition_plot_index in subplot_left_col:
                ax = plt.gca()
                ax.set_ylabel(condition_name)

    # plot the group regression lines in the rightmost subplots
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, subplot_index in zip(data_list, group_plot_indices):
            plt.subplot(subplot_rows, subplot_cols, subplot_index)
            plt.grid(True)
            plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                     'k--')
            if subplot_index == 3:
                plt.title('All subject regression lines', loc='right', size=10, fontfamily='arial')

            x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                               experiment)

            if subject_ID == example_subjects[0]:
                line_color = colors[0]
                line_width = 1
                order = 10
            elif subject_ID == example_subjects[1]:
                line_color = colors[1]
                line_width = 1
                order = 10
            else:
                line_color = 'darkgrey'
                line_width = 0.5
                order = 5

            plt.plot([x1, x2], [y1, y2], color=line_color, linewidth=line_width, zorder = order)
            plt.yticks(list(range(0, 14)), fontfamily='arial')
            plt.ylim([0, 14])
            plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))), fontfamily='arial')
            plt.xlim([x1 - 1, x2 + 1])

            ax = plt.gca()
            # draw separating lines on the figure by using the 'draw arrow to text' functionality without text being printed
            # line is drawn between xy and xytext with the numbers representing a fraction of the axes
            ax.annotate('', xy=(-0.1, -0.2), xycoords='axes fraction', xytext=(-0.1, 1.2), arrowprops=dict(arrowstyle='-', color='black'))

            # remove ticks from subplots where unneeded
            if subplot_index not in subplot_left_col:
                ax = plt.gca()
                ax.set_yticklabels([])
                # TODO figure out how to remove ticks without also removing grid lines (below line removes but messes up the grid)
                #ax.yaxis.set_ticks([])

            if subplot_index not in subplot_bottom_row:
                ax = plt.gca()
                ax.set_xticklabels([])
                #ax.xaxis.set_ticks([])
    plt.show
    plt.savefig(path, dpi=300)
    print(f'Saving {plot}')
    plt.close()


def _store_example_subject_plot_info(all_subject_data, subjects, experiment):
    example_data_tuple = namedtuple('EXAMPLE', 'condition_data indices')
    example_data_tuples = _extract_example_subject_data(all_subject_data, subjects, experiment)
    example_data_tuples.example_2
    example_1_condition_data = _return_condition_data_list(experiment, example_data_tuples.example_1)
    example_2_condition_data = _return_condition_data_list(experiment, example_data_tuples.example_2)

    example_1_indices = example_data_tuples.example_1.indices
    example_2_indices = example_data_tuples.example_2.indices

    example_1_tuple = example_data_tuple(condition_data=example_1_condition_data, indices=example_1_indices)
    example_2_tuple = example_data_tuple(condition_data=example_2_condition_data, indices=example_2_indices)

    tuple_list = [example_1_tuple, example_2_tuple]
    return tuple_list


def _extract_example_subject_data(all_subject_data, subjects, experiment):
    example_subject_tuple = namedtuple('examples', 'name data indices')
    example_subjects = namedtuple('examples', 'example_1, example_2')

    if experiment == 'exp1':
        for subject_data, subject in zip(all_subject_data, subjects):
            if subject == 'SUB05R':
                exp1_max_name = subject
                exp1_max_data = subject_data
            if subject == 'SUB01L':
                exp1_cross_name = subject
                exp1_cross_data = subject
        exp1_max = example_subject_tuple(name=exp1_max_name, data=exp1_max_data, indices=[1, 4, 7, 10])
        exp1_cross = example_subject_tuple(name=exp1_cross_name, data=exp1_cross_data, indices=[2, 5, 8, 11])

        examples = example_subjects(example_1=exp1_max, example_2=exp1_cross)

    else:
        for subject_data, subject in zip(all_subject_data, subjects):
            if subject == 'sub04':
                exp2_min_name = subject
                exp2_min_data = subject_data
            if subject == 'sub23':
                exp2_cross_name = subject
                exp2_cross_data = subject_data

        exp2_min = example_subject_tuple(name=exp2_min_name, data=exp2_min_data, indices=[1, 4, 7])
        exp2_cross = example_subject_tuple(name=exp2_cross_name, data=exp2_cross_data, indices=[2, 5, 8])

        examples = example_subjects(example_1=exp2_min, example_2=exp2_cross)

    return examples


def _return_condition_data_list(experiment, tuple):
    if experiment == 'exp1':
        # condition_data = namedtuple('condition', 'd1_dom d1_non_dom d2_dom_1 d2_dom_2')
        d1_dom = tuple.data.day1_dominant
        d1_non_dom = tuple.data.day1_non_dominant
        d2_dom_1 = tuple.data.day2_non_dominant_1
        d2_dom_2 = tuple.data.day2_non_dominant_2

        # condition_data_tuple = condition_data(d1_dom=d1_dom, d1_non_dom=d1_non_dom, d2_dom_1=d2_dom_1, d2_dom_2=d2_dom_2)
        condition_data = d1_dom, d1_non_dom, d2_dom_1, d2_dom_2

    else:
        # condition_data = namedtuple('condition', 'line_width width_line width_width')
        line_width = tuple.data.LINE_WIDTH
        width_line = tuple.data.WIDTH_LINE
        width_width = tuple.data.WIDTH_WIDTH

        # condition_data_tuple = condition_data(line_width=line_width, width_line=width_line, width_width=width_width)
        condition_data = line_width, width_line, width_width

    return condition_data
