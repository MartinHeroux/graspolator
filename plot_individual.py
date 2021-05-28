import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import numpy as np

import utils
import calculate_area
import plot_utils

general_constants = utils.create_general_constants()
plot_constants = plot_utils.create_plot_constants()
SMALLEST_WIDTH = 2
LARGEST_WIDTH = 10
YLIM = [0, 14]


def scatterplots_and_reg_lines(subject_ID, subject_data):
    path = Path('./plots/individual_plots/subject_regression_plots')
    d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
        subject_data)
    data_list = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))
    for condition_tuple in data_list:
        plt.subplot(2, 2, condition_tuple.PLOT_INDEX)
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
        x1 = SMALLEST_WIDTH
        x2 = LARGEST_WIDTH
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept
        plt.plot([x1, y1], [x2, y2])
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)
        plt.xticks(list(range(x1, x2)))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim(YLIM)
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
    path_to_save = path / f'reg_plots_{subject_ID}.png'
    plt.savefig(path_to_save, dpi=300)
    print(f'Saving scatter plots and regressions for {subject_ID}')
    plt.close()


def areas_between_regression_and_reality(subject_ID, subject_data):
    path = Path('./plots/individual_plots/area_plots/regression_vs_reality')
    d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
        subject_data)
    data_list = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Area Plots (reality vs. regression lines)'))
    for condition_tuple in data_list:
        plt.subplot(2, 2, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
        x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
        area = calculate_area.calculate_area(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)

        text = str(f'area_difference = {area:4.2f}')

        x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
        plt.plot([x1, x2], [y1, y2], color='royalblue')
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)

        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)
        plt.text(2, 9, text, fontsize=10)

        plt.xticks(plot_constants.ACTUAL_WIDTH_RANGE)
        plt.xlim([plot_constants.X_MIN, (plot_constants.X_MAX + 1)])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim([plot_constants.Y_MIN, plot_constants.Y_MAX])
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig(path / f'{subject_ID}_areas.png')
    plt.close()


def area_between_conditions_plot(subject_ID, subject_data):
    path = Path('./plots/individual_plots/area_plots/between_condition_comparison')
    dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2 = plot_utils.condition_pair_tuple(subject_data)
    data_pairs_tuple_list = dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2
    plt.figure(figsize=(15, 7))
    plt.suptitle(str(subject_ID + ' Consistency Plots'))

    for data_pair_tuple in data_pairs_tuple_list:
        print(data_pair_tuple.title)
        plt.subplot(1, 3, data_pair_tuple.subplot_index)

        total_area = calculate_area._condition_pair_area(data_pair_tuple)
        x1_x2_a, x1_x2_b, y1_y2_a, y1_y2_b = calculate_area.condition_pair_endpoints(data_pair_tuple)

        plt.plot(x1_x2_a, y1_y2_a, color=data_pair_tuple.colour_1, label=data_pair_tuple.label_1)
        plt.plot(x1_x2_b, y1_y2_b, color=data_pair_tuple.colour_2, label=data_pair_tuple.label_2)

        x_colour_points = np.array([2, 10])
        y_points_a = np.array(y1_y2_a)
        y_points_b = np.array(y1_y2_b)

        plt.fill_between(x_colour_points, y_points_a, y_points_b,
                         color='gray', alpha=0.3, interpolate=True)

        plt.xticks(plot_constants.ACTUAL_WIDTH_RANGE)
        plt.xlim([plot_constants.X_MIN, (plot_constants.X_MAX + 1)])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim([plot_constants.Y_MIN, plot_constants.Y_MAX])
        plt.text(2, 12, f'Area Difference = {total_area:4.2f}', fontsize=12)
        plt.title(data_pair_tuple.title, loc='right')
        plt.legend(handles=[data_pair_tuple.patch_1, data_pair_tuple.patch_2], loc='upper left')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
    plt.savefig('{}/{}'.format(path, subject_ID))
    plt.close()
