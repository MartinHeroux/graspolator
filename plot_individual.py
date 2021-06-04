import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

import utils
import calculate_area
import plot_utils

general_constants = utils.create_general_constants()
plot_constants = plot_utils.create_plot_constants()
SMALLEST_WIDTH = 2
LARGEST_WIDTH = 10
YLIM = [0, 15]


def scatterplots_and_reg_lines(subject_ID, subject_data, experiment):
    plot = 'scatterplot_regression'
    path = utils.create_individual_plot_save_path(experiment, plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)
    subplot_width, subplot_length, x_lims, fig_size = utils.subplot_dimensions(experiment)

    plt.figure(figsize=fig_size)
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))
    for condition_tuple in data_list:
        plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')
        length_data = len(condition_tuple.PERCEIVED)
        jitter_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_tuple.ACTUAL) + np.array(jitter_values)
        plt.plot(x_data, condition_tuple.PERCEIVED, 'o', alpha=plot_constants.ALPHA)

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL,
                                                              condition_tuple.PERCEIVED)

        # Creating points to plot regression line [x1, y1][x2, y2]
        x1 = x_lims[0]
        x2 = x_lims[1]
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept
        if y2 < 15:
            y_max = 15
        else:
            y_max = y2
        plt.plot([x1, x2], [y1, y2], color='b')
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)
        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim([0, y_max])
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.grid()

    plt.savefig(path, dpi=300, bbox_inches='tight')
    print(f'Saving scatter plots and regressions for {subject_ID}')
    plt.close()


def areas_between_regression_and_reality(subject_ID, subject_data, experiment):
    plot = 'area_between_reg_and_reality'
    path = utils.create_individual_plot_save_path(experiment, plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)
    subplot_width, subplot_length, x_lims, fig_size = utils.subplot_dimensions(experiment)

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

        area = calculate_area.actual_vs_perceived(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)

        x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
        plt.plot([x1, x2], [y1, y2], color='royalblue')
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)

        legend_handles = [Line2D([0], [0], color='royalblue', lw=2, label=f'Regression Line\n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], color='black', linestyle='--', label='Reality Line (y = x)', lw=2),
                          mpatches.Patch(color='royalblue', alpha = 0.3, label=f'Area = {area:4.2f}')]

        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(list(range(0, int(y_max + 1))))
        plt.ylim(YLIM)
        plt.grid()
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.legend(handles=legend_handles, loc='upper left')
    print(f'area between regression and reality saved for {subject_ID} in {path}')
    plt.savefig(path)
    plt.close()


def area_between_conditions_plot(subject_ID, subject_data):
    path = Path('./plots/individual_plots/area_plots/between_condition_comparison')
    dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2 = plot_utils.condition_pair_tuple(subject_data)
    data_pairs_tuple_list = dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2
    dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area = calculate_area.between_conditions(subject_data)
    data_pairs_area_list = dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area

    plt.figure(figsize=(15, 7))
    plt.suptitle(str(subject_ID + ' Consistency Plots'))
    y_points = []
    y_text_points = []

    for data_pair_tuple, data_pair_area in zip(data_pairs_tuple_list, data_pairs_area_list):
        plt.subplot(1, 3, data_pair_tuple.subplot_index)

        x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = calculate_area.condition_pair_endpoints(data_pair_tuple)
        y_points.append(y1_y2_b)
        y_points.append(y1_y2_a)
        y_text_points.append(int(y1_y2_a[1]))

        plt.plot(x1_x2_a, y1_y2_a, color=data_pair_tuple.colour_1, label=data_pair_tuple.label_1)
        plt.plot(x1_x2_b, y1_y2_b, color=data_pair_tuple.colour_2, label=data_pair_tuple.label_2)

        x_colour_points = np.array([2, 10])
        y_points_a = np.array(y1_y2_a)
        y_points_b = np.array(y1_y2_b)

        plt.fill_between(x_colour_points, y_points_a, y_points_b,
                         color='gray', alpha=0.3, interpolate=True)

        plt.xticks(plot_constants.ACTUAL_WIDTH_RANGE)
        plt.xlim([(plot_constants.SMALLEST_WIDTH - 1), (plot_constants.LARGEST_WIDTH + 1)])
        plt.title(data_pair_tuple.title, loc='right')
        plt.legend(handles=[data_pair_tuple.patch_1, data_pair_tuple.patch_2], loc='upper left')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.grid()

    y_max, y_min = utils.max_min(y_points)
    y_text_point = max(y_text_points)

    for data_pair_tuple, data_pair_area in zip(data_pairs_tuple_list, data_pairs_area_list):
        plt.subplot(1, 3, data_pair_tuple.subplot_index)
        plt.ylim([y_min, (y_max + 2)])
        plt.yticks(range(int(y_min), int((y_max + 2))))
        plt.text(2, (y_text_point - 1), f'Area Difference = {data_pair_area:4.2f}', fontsize=12)

    print(f'area between condition plot saved for {subject_ID} in {path}')
    plt.savefig('{}/{}'.format(path, subject_ID))
    plt.close()
