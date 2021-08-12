import matplotlib.pyplot as plt
from random import random
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from termcolor import colored

import old_python_files.old_functions
import utils
import calculate_area

general_constants = utils.create_general_constants()
plot_constants = old_python_files.old_functions.create_plot_constants()
SMALLEST_WIDTH = 2
LARGEST_WIDTH = 10
YLIM = [0, 15]


def scatterplots_and_reg_lines(subject_ID, subject_data, experiment):
    plot = 'scatterplot_regression'
    path = old_python_files.old_functions.create_individual_plot_save_path(experiment, plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)
    subplot_width, subplot_length, x_lims, fig_size = old_python_files.old_functions.plot_constants_regressions_ind(experiment)

    plt.figure(figsize=fig_size)
    plt.suptitle(str(subject_ID + ' Scatterplot + Regression Line'))
    for condition_tuple in data_list:
        plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')
        length_data = len(condition_tuple.PERCEIVED)
        jitter_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_tuple.ACTUAL) + np.array(jitter_values)
        color = old_python_files.old_functions.color_manip(condition_tuple.PLOT_INDEX)
        plt.plot(x_data, condition_tuple.PERCEIVED, 'o', color = color, alpha=plot_constants.ALPHA)

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL,
                                                              condition_tuple.PERCEIVED)

        legend_handles = [Line2D([0], [0], color=color, lw=2,
                                 label=f'Regression \n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], color='black', linestyle='--', label='Reality (y = x)', lw=2),
                          Line2D([0], [0], color=color, marker = 'o', linestyle = 'none', alpha=0.3, label=f'Trial (n = {length_data})')]

        # Creating points to plot regression line [x1, y1][x2, y2]
        x1 = x_lims[0]
        x2 = x_lims[1]
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept
        if y2 < 15:
            y_max = 15
        else:
            y_max = y2
        plt.plot([x1, x2], [y1, y2], color=color)
        plt.legend(handles = legend_handles, loc = 'upper left')
        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim([0, y_max])
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.grid()

    plt.savefig(path, dpi=300, bbox_inches='tight')
    #text = colored(f'{path}', 'blue')
    #print(f'scatterplot and regression line saved for {subject_ID} in {text}')
    plt.close()


def areas_between_regression_and_reality(subject_ID, subject_data, experiment):
    plot = 'area_between_reg_and_reality'
    path = old_python_files.old_functions.create_individual_plot_save_path(experiment, plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)
    subplot_width, subplot_length, x_lims, fig_size = old_python_files.old_functions.plot_constants_regressions_ind(experiment)

    plt.figure(figsize=fig_size)
    plt.suptitle(str(subject_ID + ' Area Plots (reality vs. regression lines)'))
    for condition_tuple in data_list:
        plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
        x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                           experiment)
        if y2 < 15:
            y_max = 14
        else:
            y_max = y2

        area = calculate_area.normalised(condition_tuple.ACTUAL, condition_tuple.PERCEIVED, experiment)
        color = old_python_files.old_functions.color_manip(condition_tuple.PLOT_INDEX)

        x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
        plt.plot([x1, x2], [y1, y2], color=color)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                         color=color, alpha=0.3, interpolate=True)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                         color=color, alpha=0.3, interpolate=True)

        legend_handles = [Line2D([0], [0], color='royalblue', lw=2,
                                 label=f'Regression Line\n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], color='black', linestyle='--', label='Reality Line (y = x)', lw=2),
                          mpatches.Patch(color=color, alpha=0.3, label=f'Area = {area:4.2f}')]

        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(list(range(0, int(y_max + 1))))
        plt.ylim(YLIM)
        plt.grid()
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.legend(handles=legend_handles, loc='upper left')

    plt.savefig(path)
    #text = colored(f'{path}', 'blue')
    #print(f'area between regression and reality saved for {subject_ID} in {text}')
    plt.close()


def area_between_conditions_plot(subject_ID, subject_data, experiment):
    plot = 'area_difference_between_conditions'
    path = old_python_files.old_functions.create_individual_plot_save_path(experiment, plot, subject_ID)

    data_pair_tuples = old_python_files.old_functions.condition_pair_tuple(experiment, subject_data)
    data_pair_areas = old_python_files.old_functions.between_conditions(experiment, subject_data)

    subplot_width, subplot_length, x_lims, fig_size = old_python_files.old_functions.subplot_dimensions_area_differences(experiment)

    if experiment == 'exp1':
        plt.figure(figsize=(15, 5))
        plt.suptitle(str(subject_ID + ' Consistency Plot'))

        for data_pair_tuple, data_pair_area in zip(data_pair_tuples, data_pair_areas):
            y_points = []

            area_patch = mpatches.Patch(color='gray', alpha=0.3, label=f'Area = {data_pair_area:4.2f}')

            plt.subplot(subplot_width, subplot_length, data_pair_tuple.subplot_index)

            x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = old_python_files.old_functions.condition_pair_endpoints(data_pair_tuple, experiment)
            y_points.append(y1_y2_b)
            y_points.append(y1_y2_a)

            plt.plot(x1_x2_a, y1_y2_a, color=data_pair_tuple.colour_1, label=data_pair_tuple.label_1)
            plt.plot(x1_x2_b, y1_y2_b, color=data_pair_tuple.colour_2, label=data_pair_tuple.label_2)

            x_colour_points = np.array(x_lims)
            y_points_a = np.array(y1_y2_a)
            y_points_b = np.array(y1_y2_b)

            plt.fill_between(x_colour_points, y_points_a, y_points_b,
                             color='gray', alpha=0.3, interpolate=True)

            plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
            plt.xlim([x_lims[0] - 1, x_lims[1] + 1])
            plt.title(data_pair_tuple.title, loc='right')
            plt.legend(handles=[data_pair_tuple.patch_1, data_pair_tuple.patch_2, area_patch], loc='upper left')
            plt.ylabel('Perceived width (cm)')
            plt.xlabel('Actual width (cm)')
            plt.grid()

            y_max, y_min = old_python_files.old_functions.max_min(y_points)

            plt.ylim([y_min, (y_max + 2)])
            plt.yticks(range(int(y_min), int((y_max + 2))))

        plt.savefig(path)
        #text = colored(f'{path}', 'blue')
        #print(f'area between condition plot saved for {subject_ID} in {text}')
        plt.close()

    elif experiment == 'exp2':
        plt.figure(figsize=(5, 7))
        _plot_between_conditions_exp2(data_pair_tuples, data_pair_areas, experiment, x_lims,
                                      subplot_width, subplot_length, path, subject_ID)




def _plot_between_conditions_exp2(data_pair_tuples, data_pair_areas, experiment, x_lims,
                                  subplot_width, subplot_length, path, subject_ID):

    y_points = []

    area_line_first, area_width_first = data_pair_areas[0], data_pair_areas[1]
    area_difference = abs(area_line_first - area_width_first)
    text = f'Absolute Area Difference = {area_difference:4.2f}'

    legend_handles = [Line2D([0], [0], color='green', lw=2, label='Show Line Pick Width'),
                      Line2D([0], [0], color='firebrick', label='Present Width Pick Line', lw=2),
                      Line2D([0], [0], color='black', linestyle='--', label='Reality Line (y = x)', lw=2),
                      mpatches.Patch(color='green', alpha=0.3, label=f'Area = {area_line_first:4.2f}'),
                      mpatches.Patch(color='firebrick', alpha=0.3, label=f'Area = {area_width_first:4.2f}'),
                      mpatches.Patch(color='none', label=text)]

    plt.subplot(subplot_width, subplot_length, data_pair_tuples.subplot_index)

    x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = old_python_files.old_functions.condition_pair_endpoints(data_pair_tuples, experiment)
    x1_x2_reality, y1_y2_reality = [3, 9], [3, 9]

    y_points.append(y1_y2_b)
    y_points.append(y1_y2_a)

    plt.plot(x1_x2_a, y1_y2_a, color='green', label=data_pair_tuples.label_1)
    plt.plot(x1_x2_b, y1_y2_b, color='firebrick', label=data_pair_tuples.label_2)
    plt.plot(x1_x2_reality, y1_y2_reality, color='black', linestyle='--', label='Reality line')

    x_colour_points = np.array(x_lims)
    y_points_a = np.array(y1_y2_a)
    y_points_b = np.array(y1_y2_b)
    y_points_reality = np.array(y1_y2_reality)

    plt.fill_between(x_colour_points, y_points_a, y_points_reality,
                     color='green', alpha=0.3, interpolate=True)
    plt.fill_between(x_colour_points, y_points_b, y_points_reality,
                     color='firebrick', alpha=0.3, interpolate=True)

    plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
    plt.xlim([x_lims[0] - 1, x_lims[1] + 1])
    plt.title(f'Reciprocal Condition Area Difference {subject_ID}', loc='right')
    plt.legend(handles=legend_handles, loc='upper left')
    plt.ylabel('Perceived width (cm)')
    plt.xlabel('Actual width (cm)')
    plt.grid()

    y_max, y_min = old_python_files.old_functions.max_min(y_points)

    plt.ylim([y_min, (y_max + 2)])
    plt.yticks(range(int(y_min), int((y_max + 2))))

    plt.savefig(path)
    #text = colored(f'{path}', 'blue')
    #print(f'area between condition plot saved for {subject_ID} in {text}')
    plt.close()
