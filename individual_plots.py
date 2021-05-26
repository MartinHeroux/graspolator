import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import numpy as np

import utils
import area_calcs
import plot_funcs

general_constants = utils.create_general_constants()
plot_constants = plot_funcs.create_plot_constants()


def plot_subject_scatterplots_and_reg_lines(subject_ID, subject_data):

    path = Path('./plots/individual_plots/subject_regression_plots')
    d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_funcs.store_index_condition_data_tuple(subject_data)
    data_list = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple

    perceived_max, perceived_min = utils.max_min([d1_dom_tuple.PERCEIVED, d1_non_dom_tuple.PERCEIVED, d2_dom_1_tuple.PERCEIVED, d2_dom_2_tuple.PERCEIVED])
    actual_max, actual_min = utils.max_min([d1_dom_tuple.ACTUAL, d1_non_dom_tuple.ACTUAL, d2_dom_1_tuple.ACTUAL, d2_dom_2_tuple.ACTUAL])

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))
    for condition_tuple in data_list:
        plt.subplot(2, 2, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')
        length_data = len(condition_tuple.PERCEIVED)
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_tuple.ACTUAL) + np.array(random_values)
        plt.plot(x_data, condition_tuple.PERCEIVED, 'o', alpha=plot_constants.ALPHA)

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL,
                                                              condition_tuple.PERCEIVED)

        x_min_plot, x_max_plot = perceived_min, perceived_max
        y_min_plot = slope * x_min_plot + intercept
        y_max_plot = slope * x_max_plot + intercept
        plt.plot([x_min_plot, x_max_plot], [y_min_plot, y_max_plot])
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)
        plt.xticks(list(range(actual_min, actual_max)))
        plt.xlim([actual_min, actual_max+1])
        plt.yticks(plot_constants.PERCEIVED_WIDTH_RANGE)
        plt.ylim(plot_constants.Y_MIN, (plot_constants.Y_MAX + 1))
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    path_to_save = str(str(path) + '/reg_lines_by_group_by_condition')
    plt.savefig(path_to_save, dpi=300)
    print(f'Saving scatter plots and regressions for {subject_ID}')
    plt.close()


def plot_areas_between_reg_and_reality_lines(subject_ID, subject_data):
    path = Path('./plots/area_plots/regression_vs_reality')
    d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_funcs.store_index_condition_data_tuple(subject_data)
    data_list = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple

    perceived_max, perceived_min = utils.max_min(
        [d1_dom_tuple.PERCEIVED, d1_non_dom_tuple.PERCEIVED, d2_dom_1_tuple.PERCEIVED, d2_dom_2_tuple.PERCEIVED])
    actual_max, actual_min = utils.max_min(
        [d1_dom_tuple.ACTUAL, d1_non_dom_tuple.ACTUAL, d2_dom_1_tuple.ACTUAL, d2_dom_2_tuple.ACTUAL])

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Area Plots (reality vs. regression lines)'))
    for condition_tuple in data_list:
        plt.subplot(2, 2, condition_tuple.PLOT_INDEX)
        plt.plot([plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 [plot_constants.REALITY_LINE_MIN, plot_constants.REALITY_LINE_MAX],
                 'k--')

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)

        area_total, x2, x10, y_at_x2, y_at_x10 = area_calcs.calculate_area_and_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
        text = str(f'area_difference = {area_total:4.2f}')

        x_colour_points, y_points_reality, y_points_reg  = np.array([x2, x10]), np.array([x2, x10]), np.array([y_at_x2, y_at_x10])
        plt.plot([x2, x10], [y_at_x2, y_at_x10], color='royalblue')
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

    plt.savefig(f'{path}/{subject_ID}_')
    plt.close()

def area_between_conditions_plot(subject_ID, subject_data):
    path = Path('./plots/individual_plots/area_plots/between_condition_comparison')
    data_pairs_tuple_list = plot_funcs.create_data_pair_plot_tuple(subject_data)
    plt.figure(figsize=(15, 7))
    plt.suptitle(str(subject_ID + ' Consistency Plots'))

    for data_pair_tuple in data_pairs_tuple_list:
        print(data_pair_tuple.title)
        plt.subplot(1, 3, data_pair_tuple.subplot_index)

        total_area, x_pair_a, x_pair_b, y_pair_a, y_pair_b = area_calcs.calculate_data_pair_area_and_endpoints(data_pair_tuple)

        plt.plot(x_pair_a, y_pair_a, color=data_pair_tuple.colour_1, label=data_pair_tuple.label_1)
        plt.plot(x_pair_b, y_pair_b, color=data_pair_tuple.colour_2, label=data_pair_tuple.label_2)

        x_colour_points = np.array([2, 10])
        y_points_a = np.array(y_pair_a)
        y_points_b = np.array(y_pair_b)

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
    plt.show()
    plt.savefig('{}/{}'.format(path, subject_ID))
    plt.close()