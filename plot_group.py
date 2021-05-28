import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import random as rd
import numpy as np
from matplotlib.lines import Line2D
from matplotlib import cm

import utils
import calculate_area
import plot_utils

constants = utils.create_general_constants()
plot_constants = plot_utils.create_plot_constants()


def plot_subject_reg_lines_by_category(subject_IDs, all_subject_data):
    path = Path('./plots/group_plots')
    legend_handles = [plot_constants.MINIMISER_PATCH,
                      plot_constants.MAXIMISER_PATCH,
                      plot_constants.CROSSER_PATCH]
    y_points = []
    x_points = []
    subplot_indices = [1, 2, 3, 4]

    plt.figure(figsize=(15, 5))
    plt.suptitle(str('Participant Regression Lines'))

    for subject_ID, subject_data in zip(subject_IDs, all_subject_data):
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)
        data_list = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple
        for condition_tuple in data_list:
            plt.subplot(1, 4, condition_tuple.PLOT_INDEX)
            plt.title(condition_tuple.NAME, loc='right')
            intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
            intersect_x, intersect_y = calculate_area.point_of_intersection_with_reality(intercept, slope)
            x1, x2, y1, y2 = utils.reg_line_endpoints(intercept, slope)
            y_points.append(y1)
            y_points.append(y2)
            x_points.append(x1)
            x_points.append(x2)
            line_colour = plot_utils.subject_line_colour(intersect_x, y1)
            print(f'{subject_ID} is {line_colour} on {condition_tuple.NAME}')
            plt.plot([x1, x2], [y1, y2], color=line_colour, linewidth=0.5)
        print(f'Reg line plotted subject {subject_ID}')

    y_min, y_max = min(y_points) - 1, max(y_points) + 1
    x_min, x_max = min(x_points) - 1, max(x_points) + 1

    for subplot in subplot_indices:
        plt.subplot(1, 4, subplot)
        plt.xticks(list(range(x_min, x_max)))
        plt.xlim([x_min, x_max])
        plt.yticks(list(range(int(y_min), int(y_max))))
        plt.ylim([y_min, y_max])
        plt.grid()
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.legend(handles=legend_handles, loc='upper left')
        plt.plot([2, 10], [2, 10], 'k--', linewidth=1.5)

    plt.savefig('{}/{}'.format(path, 'regression_lines_per_condition.png'), dpi=300)
    print(f'Saving whole group regression plots')
    plt.close()


def consistency_between_conditions(all_subject_data):
    path = Path('./plots/group_plots/')
    color_map = cm.get_cmap('copper', 12)
    # TODO decide on method of colouring lines in figure

    plt.figure(figsize=(7, 10))
    plt.suptitle(str('Area Difference Between Conditions'))
    plt.ylabel('Area Difference Between Regression Lines (cm^2)')
    plt.xlabel('Condition Comparison')
    plt.grid()
    x_points_base = [1, 2, 3]
    plt.xticks(x_points_base, labels=['D1 dom - D1 non dom', 'D1 dom - D2 dom', 'D2 dom (a) - D2 dom (b)'])

    for line_number, subject_data in enumerate(all_subject_data, start=1):
        jitter_values = [random() / 40 for _ in range(len(x_points_base))]
        if line_number < 15:
            x_points_jitter = np.array(x_points_base) + np.array(jitter_values)
        else:
            x_points_jitter = np.array(x_points_base) - np.array(jitter_values)
        colour_index = rd.uniform(0, 1)
        dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area = calculate_area.between_conditions(subject_data)
        y_points = [dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area]
        plt.plot(x_points_jitter, y_points, color=color_map(colour_index), marker='o', alpha=0.4)

    plt.savefig('{}/group_consistency_plot.png'.format(path))
    print(f'Saving group consistency plots')
    plt.close()


def difference_of_differences(all_subject_data):
    path = Path('./plots/group_plots/difference_of_differences_plot')

    plt.figure(figsize=(7, 10))
    plt.suptitle(str('Difference of Differences'))
    plt.ylabel('Difference Between Areas (cm^2)')
    plt.xlabel('Difference Pair')
    plt.grid()
    x_points_base = [1, 2, 3]
    plt.xticks(x_points_base,
               labels=['Between Hands - Within Day', 'Between Hands - Between Days', 'Within Day - Between Days'])
    # TODO discuss how best to label the differences on x axis
    plt.yticks(range(-10, 10))
    key_text = str('Between Hands = difference between hands in two test sessions the same day \n'
                   'Within Day = difference between right hand in two test sessions on different days \n'
                   'Between Days = difference between the right hand in two test sessions the same day')
    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    hands_vs_day_list, hands_vs_days_list, day_vs_days_list = [], [], []

    for subject_data in all_subject_data:
        hands_vs_day, hands_vs_days, day_vs_days = calculate_area.difference_of_difference_areas(subject_data)

        hands_vs_day_list.append(hands_vs_day)
        hands_vs_days_list.append(hands_vs_days)
        day_vs_days_list.append(day_vs_days)

        y_points = [hands_vs_day, hands_vs_days, day_vs_days]

        plt.plot(x_points_base, y_points, color='silver', alpha=0.5)

    area_diff_list = [hands_vs_day_list, hands_vs_days_list, day_vs_days_list]
    area_max, area_min = utils.max_min(area_diff_list)
    y_range = range(int(-area_max), int(area_max + 2))
    print(y_range)

    for x_point, area_list in zip(x_points_base, area_diff_list):
        mean, ci = utils.calculate_mean_ci(area_list)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec='r', markersize=8)

    plt.hlines(y=0, xmin=1, xmax=3, color='dimgrey', linestyle='--', lw=2)
    plt.ylim(-area_max, (area_max + 1))
    plt.yticks(y_range)
    plt.legend(handles=legend_elements, loc='upper right')
    plt.text(0.08, 0.01, key_text, fontsize=10, bbox=dict(facecolor='none', edgecolor='red'),
             transform=plt.gcf().transFigure)
    plt.savefig(path, bbox_inches='tight')
    print(f'Saving difference of area differences plots')
    plt.close()


def area_per_condition_plot(all_subject_data):
    path = Path('./plots/group_plots/all_subject_areas_by_condition')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str('Area Between Regression and Reality Per Condition'))
    plt.ylabel('Area Between Lines (cm^2)')
    plt.xlabel('Condition')
    x_points = [1, 2, 3, 4]
    plt.xticks(x_points,
               labels=constants.CONDITION_NAMES)

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    all_area_lists = []

    for subject_data in all_subject_data:
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = plot_utils.store_index_condition_data_tuple(
            subject_data)

        d1_dom_area = calculate_area.actual_vs_perceived(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED)
        d1_non_dom_area = calculate_area.actual_vs_perceived(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED)
        d2_dom_1_area = calculate_area.actual_vs_perceived(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED)
        d2_dom_2_area = calculate_area.actual_vs_perceived(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED)

        y_points = [d1_dom_area, d1_non_dom_area, d2_dom_1_area, d2_dom_2_area]
        all_area_lists.append(y_points)

        plt.plot(x_points, y_points, color='darkgrey', alpha=0.5)

    area_means, area_CIs = utils.store_area_means_CIs_per_condition(all_subject_data)
    for mean, ci, x_point in zip(area_means, area_CIs, x_points):
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec='r', markersize=8)

    area_max, area_min = utils.max_min(all_area_lists)
    plt.ylim(area_min - 1, area_max + 1)
    plt.legend(handles=legend_elements, loc='upper left')
    plt.grid()
    plt.savefig(path)
    print(f'Saving difference of area difference by condition plots')
    plt.close()


def area_vs_r2_plot(all_subject_data):
    path = Path('./plots/group_plots/area_vs_r2')
    area_lists = calculate_area.group_areas(all_subject_data)
    r2_lists = utils.store_r2_lists(all_subject_data)

    plt.figure(figsize=(10, 10))
    plt.suptitle('Area Between Reg Line + Reality Line vs. R^2 Value')
    for subplot_index, (condition_r2_data, condition_area_data, condition_name) in enumerate(
            zip(r2_lists, area_lists, constants.CONDITION_NAMES), start=1):
        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)
        plt.subplot(2, 2, subplot_index)
        x_vals = np.array([1, 26])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, 'k--')
        plt.scatter(condition_area_data, condition_r2_data, marker='o', color='royalblue', alpha=0.5)
        plt.text(15, 0.75, f'{slope:6.5f}*x + {intercept:4.2f}', fontsize=12)
        plt.xlim([1, 26])
        plt.ylim([0.7, 1])
        plt.grid()
        plt.title(condition_name, loc='right')
        plt.xlabel('Area (cm^2)')
        plt.ylabel('R^2 Value')
        plt.tight_layout()
    plt.savefig(path, dpi=300)
    print(f'Saving area vs r2 plots')
    plt.close()


def r2_per_condition_plot(all_subject_data, subject_IDs):
    path = Path('./plots/group_plots/')

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='o', label='Mean R^2', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    r2_area_tuples = calculate_area.store_r2_and_area_tuples(all_subject_data, subject_IDs)

    plt.figure(figsize=(10, 10))
    plt.suptitle('R^2 (actual vs perceived widths) Values Per Condition')
    plt.ylabel('R^2')
    plt.xlabel('Condition')
    x_points = [1, 2, 3, 4]

    for r2_area_tuple in r2_area_tuples:
        y_points = [r2_area_tuple.d1_dom_r2,
                    r2_area_tuple.d1_non_dom_r2,
                    r2_area_tuple.d2_dom_1_r2,
                    r2_area_tuple.d2_dom_2_r2]
        plt.plot(x_points, y_points, color='darkgrey', alpha=0.5)

    means, cis = utils.store_r2_means_CIs_per_condition(all_subject_data)

    for mean, ci, x_point in zip(means, cis, x_points):
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="o", markerfacecolor='r', mec='r', markersize=8)

    plt.legend(handles=legend_elements, loc='lower right')
    plt.xticks(x_points,
               labels=['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"])
    plt.grid()
    plt.savefig(f'{path}/r2_summary.png')
    print(f'Saving difference of area difference by condition plots')
    plt.close()
